# Experiment Design Handbook

    handbook_version: "0.7.2"

Guidance for designing and interpreting computer-system performance experiments.
Read `## Navigation` first, then the chapters relevant to the question.

## Navigation

This handbook supplies a reusable method. A new question changes the objective,
workload, factors and measurements; it need not require a new handbook. Rules
have applicability conditions, so system independence does not mean that every
rule applies to every experiment.

The identifiers M1.1 through M8.5 provide stable references. Each guideline
links to a source and a passage where possible. Read those links as follows:

- An unmarked guideline summarizes the cited methodological recommendation.
- **Application** marks our deduction or adaptation of the cited background.
  The source supports the underlying principle, not necessarily the exact rule.
- **Policy** marks an operating choice with an explicit rationale. It is not
  presented as a finding from the literature.

The procedures and applications have not been shown to improve language-model
performance across systems or benchmarks. A source's empirical findings retain
its original scope. In particular, findings about particular cloud platforms or
request generators do not establish universal performance behavior.

An **operation** is a unit of work, such as a request, transaction or job. A
**component** is an identifiable part of the measured workload or system. Use
component breakdowns where the measurements support them; do not invent missing
measurements. Source details and link definitions are in `## Sources`.

Each chapter can be requested separately using its exact heading.

| Chapter | Read it when the question involves |
| --- | --- |
| M1. The claim | defining an objective, hypothesis or decision |
| M2. Factors and controls | comparisons, attribution or parameter sweeps |
| M3. The load model | arrivals, throughput, capacity, concurrency or responsiveness |
| M4. Data and state | input scale, caching, storage, preparation or warm-up |
| M5. Repetition and noise | variation, uncertainty or repeatability |
| M6. The environment | placement, shared infrastructure or measurement interference |
| M7. Metrics | selecting, combining or interpreting measurements |
| M8. Feasibility | costs, execution limits or follow-up experiments |

For design, start with M1 and M8. For interpretation, apply the same principles
and use the M7 verdict procedure. For another experiment, use the M8 follow-up
procedure. These routes are reading aids, not an exhaustive substitute for
considering the question.

### Local agent interface and policies

This subsection describes this agent's implementation, separately from the
methodology. Its catalog restricts available experiments, and its result
contract governs evidence access and accepted claims. Passing those checks does
not establish scientific validity.

The current validator implements restricted checks associated with M1.1, M2.1,
M2.3, M2.6 and M5.1: a heuristic against vague adequacy claims, separable declared
resource factors, equal resource requests and limits, agreement between declared and
varied factors, and a minimum repetition count. These are local interface rules
and operating policies. Equal requests and limits are not a universal condition
for a valid experiment, and a minimum repetition count does not guarantee useful
precision. A joint resource change can answer a joint-effect question even
where the current interface rejects it. If the interface cannot express a
scientifically appropriate design, record that limitation.

For YCSB, the catalog's `max_execution_time` caps the benchmarking phase and
`operations_scale` sets the total operation count, which is split across the
pods. Without a cap each pod receives a fixed share and may finish at a
different time, while the report's phase throughput adds up the pods' separate
rates (M7.2). A capped pod still stops early once its share of operations is
exhausted, so a cap needs enough operations to keep every pod busy. Neither
control excludes warm-up (M4.5). **Policy:** the validator warns, without
refusing, when a YCSB round runs several pods without a cap. The interpretation
assessor withholds a throughput shape or ranking when a phase's summed rate
exceeds its pods' work spread over the longest pod duration by more than 20%, or
when that cannot be checked. The threshold targets large distortions; it is not
a scientific boundary.

Before a verdict can be recorded, the harness requires this Navigation chapter
and M2, M3, M5 and M7 to have been read. The verdict procedure also draws on
M1, M4 and M6, which can be requested by heading in the same way.

## M1. The claim

**Purpose.** Define the question and what observations can answer it.

**Read this when.** Planning or interpreting any experiment.

**Questions to answer.** Is the objective description, comparison, prediction,
explanation or exploration? What evidence and precision would answer it?

**Related chapters.** M2 addresses attribution, M5 uncertainty, and M7 metrics.

**Guidelines**

- **M1.1** **Application.** State an answerable objective. For a hypothesis, name
  an observable outcome that would contradict it. Terms such as “adequate” need
  a criterion; without one, the judgment is undefined. Descriptive and
  exploratory objectives need not assert a hypothesis. [NIST, §5.3.1][nist-objectives]
- **M1.2** **Application.** For causal or diagnostic questions, identify competing
  explanations and observations that distinguish them. A descriptive comparison
  can estimate a difference without establishing its mechanism.
  [NIST, §5.3.3][nist-design]
- **M1.3** **Application.** For a confirmatory decision, specify the metric,
  decision rule and practically important difference before examining the
  results. Disclose criteria developed during exploration and seek independent
  confirmation. Statistical significance, meaning evidence against a specified
  statistical hypothesis, is distinct from practical importance.
  [NIST, §1.3.5][nist-testing]; [Nosek et al., “Preregistration Distinguishes Prediction and Postdiction”][preregistration]
- **M1.4** **Application.** Distinguish estimating performance, comparing
  alternatives and explaining differences. Each needs a stated scope and
  uncertainty; explanation additionally needs evidence bearing on causes.
  [NIST, §5.3.1][nist-objectives]
- **M1.5** **Application.** Match the question to measurable inputs and outcomes.
  If required evidence is unavailable, obtain it or narrow the question.
  [NIST, §5.3.2][nist-variables]

**Common pitfalls.** An undefined success criterion cannot support a decision.
A criterion chosen after seeing the result needs to be disclosed. Measuring a
related quantity does not automatically answer the original question.

## M2. Factors and controls

**Purpose.** Decide what varies and which effects the design can separate.
A **factor** is an input varied deliberately. **Confounding** occurs when effects
cannot be distinguished by the design.

**Read this when.** Comparing alternatives, attributing effects or varying inputs.

**Questions to answer.** Which effects are of interest? What else differs?
Which combinations and controls are needed for the intended inference?

**Related chapters.** M4 addresses state, M5 variation, and M6 the environment.

**Guidelines**

- **M2.1** **Application.** Choose combinations that identify the intended effects.
  A full factorial design tests every combination of selected factor levels.
  For reduced designs, state which effects cannot be separated and the
  assumptions used. Changing inputs together can estimate their joint effect;
  it does not by itself identify their individual effects.
  [NIST, §5.3.3.3][nist-factorial]
- **M2.2** Control relevant differences or account for them through design.
  Blocking groups comparable experimental units; randomization assigns
  treatments without a systematic ordering. Literal identity of every setting
  is not required when a difference is deliberately studied or accounted for.
  [NIST, §5.3.3.2][nist-blocking]
- **M2.3** **Application.** Account for interference from shared resources through
  controlled allocations, deliberate contention, or suitable replication and
  analysis. State what is guaranteed and what can vary. Resource limits alone
  do not establish isolation. [Leitner and Cito, §§2, 5.2][cloud]
- **M2.4** Give alternatives comparable tuning effort and disclose that effort.
  **Application:** A comparison of defaults is legitimate when explicitly scoped
  to defaults. [Raasveldt et al., §3.2][dbtest]
- **M2.5** Check equivalent semantics and correct results before attributing a
  difference to performance. **Application:** If guarantees intentionally differ,
  describe the resulting tradeoff. [Raasveldt et al., §§3.3, 3.8][dbtest]
- **M2.6** **Application.** Record actual settings and distinguish deliberately
  varied factors from unintended systematic differences and random variation.
  A declared varied factor must vary. Random variation alone does not establish
  confounding. [Hoefler and Belli, Rule 9][scientific]
- **M2.7** **Application.** Distinguish observations at tested levels from
  predictions elsewhere. Broader predictions require stated modeling assumptions
  and validation; otherwise bound the conclusion to the tested range.
  [NIST, §5.5.9.9.8][nist-prediction]
- **M2.8** Consider conditions where an alternative might perform worse. Justify
  workload subsets and limit the scope of their conclusions.
  [Heiser, §§1.1–1.2][heiser]
- **M2.9** **Application.** Consider interactions, where one factor's effect depends
  on another. Other settings or demand may limit a resource increase's benefit.
  Separate changing allocation with settings fixed from changing allocation and
  tuning together. A flat result describes the tested conditions; low average
  utilization alone does not identify its cause. Use M6.4 for a mechanism claim.
  [NIST, §5.3.2, model matrix and interaction term][nist-variables]

**Common pitfalls.** A joint change does not identify separate effects. A hidden
change in guarantees undermines a claim of equivalent work. An observed flat
series does not establish independence under untested conditions.

## M3. The load model

**Purpose.** Describe how work arrives and what demand the measurement represents.

**Read this when.** Arrival behavior, throughput, concurrency or responsiveness
matters. For batch work, describe job submission and scheduling instead of
assuming an external request generator.

In a **closed** model, a fixed population waits for completions before submitting
more work, possibly after a delay called think time. In an **open** model,
arrivals do not depend on earlier completions. Partly open models combine these
features. [Schroeder et al., §2][load]

**Questions to answer.** Which population is represented? Is demand prescribed?
Does the question concern performance at that demand or maximum capacity?

**Related chapters.** M5 addresses uncertainty and M7 measurement boundaries.

**Guidelines**

- **M3.1** Match the load model to the population and arrival behavior being
  studied. Either capacity or responsiveness can be studied under different
  models; the objective alone does not select one.
  [Schroeder et al., §§2, 7][load]
- **M3.2** **Application.** A prescribed arrival rate can support a valid
  performance measurement. Report offered and achieved rates; performance at
  that demand does not by itself establish maximum capacity.
  [Tene, introduction and “Basic Usage”][wrk2]
- **M3.3** **Application.** Define sustainable performance through explicit
  requirements for completion, delay, failures, backlog and observation duration
  as applicable. Report the highest tested demand meeting them. A throughput
  plateau alone does not identify the limiting resource. TPC-C illustrates
  explicit response-time and sustained-measurement requirements; its particular
  thresholds are benchmark-specific. [TPC-C 5.11, §§5.2.5, 5.5][tpc-c]
- **M3.4** For intended independent arrivals, account for delays between scheduled
  and actual submission. Starting latency only at late submission can omit
  waiting. **Application:** Report work that could not be issued or completed.
  [Tene, “Discussion”][wrk2]
- **M3.5** Report population and think time for closed models, and arrival behavior
  for open models. **Application:** Varying concurrency is legitimate when the
  question concerns the resulting closed-population behavior.
  [Schroeder et al., §§2, 5, Figure 7][load]
- **M3.6** **Application.** Include the work generator in the measurement boundary
  when it might limit delivered demand. Compare intended with delivered work
  and investigate generator limits before attributing a plateau to the target.
  [NIST, §5.3.2, selecting factors and responses][nist-variables]

**Common pitfalls.** Performance under a rate cap is not automatically maximum
capacity. A waiting population does not represent independent arrivals. Missing
submissions must not silently become successful observations.

## M4. Data and state

**Purpose.** Specify inputs, preparation and state at measurement time.

**Read this when.** Input scale, caching, storage or initialization matters.

**Questions to answer.** What data and state are actually accessed? Which costs
and transient behavior belong to the question?

**Related chapters.** M2 addresses comparability and M8 budget allocation.

**Guidelines**

- **M4.1** **Application.** Distinguish total input size from the working set, the
  data and state actually accessed. Describe relevant memory and cache behavior
  rather than inferring it from input size alone.
  [Raasveldt et al., §§3.5–3.6][dbtest]
- **M4.2** **Application.** Show that the workload exercises the storage behavior
  named by the claim. Cached reads do not exclude durable writes, so fitting
  inputs in memory does not rule out every storage experiment. This is a
  deduction from the distinction between reads and durability obligations, not a
  result measured for every system. [TPC-C 5.11, §3.5][tpc-c]
- **M4.3** State the cache preparation protocol. **Application:** Establish
  comparable states unless state is itself a factor under study.
  [Raasveldt et al., §§3.5–3.6][dbtest]
- **M4.4** State whether preparation costs are included, including automatic
  preparation, and apply the same accounting boundary to alternatives.
  [Raasveldt et al., §3.7][dbtest]
- **M4.5** **Application.** Select initialization, transient or steady behavior
  according to the question. Define the measurement window and, for a claimed
  steady state, explain how it was established. Disclose when it was not reached.
  [Kalibera and Jones, §6][repetition]
- **M4.6** Check result correctness before comparing speed. **Application:** Report
  incomplete work separately; any comparison of successful work must identify
  its restricted scope. [Raasveldt et al., §3.8][dbtest]

**Common pitfalls.** Input volume alone does not establish cache behavior.
Unequal preparation accounting changes the comparison. Skipping work cannot be
counted as faster completion of that work.

## M5. Repetition and noise

**Purpose.** Estimate relevant variation and the precision of the answer.

**Read this when.** Observations may vary or an inference needs uncertainty.

**Questions to answer.** At which level does variation occur? How precise must
the answer be? Which observations share conditions or depend on one another?

**Related chapters.** M6 addresses environmental variation and M7 summaries.

**Guidelines**

- **M5.1** Repeat at relevant levels and choose effort for useful precision.
  A single run cannot estimate between-run variation from replication.
  [Kalibera and Jones, §§3, 9][repetition]
- **M5.2** Report uncertainty in estimated effects. Distinguish uncertainty of an
  estimate from the spread of individual observations.
  [Kalibera and Jones, §4][repetition]
- **M5.3** Compare with an appropriate interval for the effect or statistical
  analysis. Overlap of separate confidence intervals does not establish equality.
  **Application:** A flat-looking series does not establish practical equivalence,
  meaning differences smaller than a stated important margin.
  [Kalibera and Jones, §§4, 10][repetition]; [NIST, §1.3.5][nist-testing]
- **M5.4** Check distributional assumptions. **Application:** Choose means,
  medians or percentiles according to the quantity of interest and analysis;
  none is universally preferable. A percentile describes a threshold below
  which a stated fraction of observations falls.
  [Hoefler and Belli, Rules 6–8][scientific]
- **M5.5** Account for dependence and levels of repetition. Iterations within one
  process do not replace independent repetitions of deployment or compilation
  when those are relevant sources of variation.
  [Kalibera and Jones, §§3, 6–9][repetition]
- **M5.6** **Application.** Estimate variation within and between allocations
  rather than assuming which is larger. Cloud measurements are conditional on
  the providers, instance types and workloads studied.
  [Leitner and Cito, §§5.2.1–5.2.2, Table VI][cloud]
- **M5.7** Use randomization or blocking to address nuisance variation, variation
  from factors outside the main question. **Application:** A fixed alternating
  order does not guarantee removal of time effects.
  [NIST, §5.3.3.2][nist-blocking]

**Common pitfalls.** More dependent observations do not necessarily provide
more independent evidence. A nonsignificant difference does not establish
practical equality. Discarding inconvenient observations without disclosing the
selection rule changes the evidence being summarized.

## M6. The environment

**Purpose.** Specify execution conditions and investigate measurement interference.

**Read this when.** Placement, shared resources or instrumentation matters.

**Questions to answer.** What could alter the measurement? What is recorded?
What would distinguish a proposed cause from another explanation?

**Related chapters.** M2 addresses controls and M5 variation.

**Guidelines**

- **M6.1** **Application.** Account for competition between the target, generator
  and instrumentation. Separation is one control; co-location may itself be the
  intended deployment. Disclose and investigate interference relevant to the
  claim. [Mytkowicz et al., §§1, 7, measurement bias][bias]
- **M6.2** **Application.** Account for placement through fixed or paired
  conditions, randomization, or replication as appropriate. Pinning is one
  possible control, not a universal requirement.
  [NIST, §5.3.3.2][nist-blocking]
- **M6.3** Record hardware, software versions and configuration sufficiently for
  another investigator to understand and attempt to reproduce the conditions.
  [Raasveldt et al., §3.1 and Appendix A][dbtest]
- **M6.4** **Application.** Use monitoring to investigate proposed mechanisms.
  Association between resource use and performance does not by itself establish
  causation: another factor could affect both. Identify the intervention or
  additional evidence that distinguishes explanations, and label untested
  mechanisms as hypotheses. [Mytkowicz et al., §§1, 7][bias]
- **M6.5** Disclose and assess variation associated with shared infrastructure.
  **Application:** State what isolation is known and what remains uncontrolled.
  [Leitner and Cito, §§2, 5.2][cloud]

**Common pitfalls.** An unrecorded environmental difference can undermine
attribution. Monitoring alone does not prove a mechanism. Missing telemetry is
not evidence that interference was absent.

## M7. Metrics

**Purpose.** Define the measured quantity and preserve its meaning in summaries.

**Read this when.** Selecting, combining or interpreting measurements.

**Questions to answer.** What is counted? Over which population and interval?
Which differences would a summary conceal?

**Related chapters.** M3 addresses demand and M5 uncertainty.

**Guidelines**

- **M7.1** **Application.** Define units, timing boundaries, included work and cost
  components. Record constituent measurements when reporting derived quantities.
  [NIST, §5.3.2, selecting responses][nist-variables]
- **M7.2** Match the summary and weighting to the quantity claimed. Explain how
  rates and ratios are combined. **Application:** Overall completed work per
  common elapsed interval differs from an average of normalized scores. A
  geometric mean summarizes multiplicative ratios; it is not generally the
  speedup in total elapsed time. Adding rates measured over different durations
  does not give the rate over their common interval, and similar durations alone
  do not show that the measurements overlapped or reached steady operation.
  [Hoefler and Belli, §3.1.1, Rules 3–4][scientific]
- **M7.3** Provide absolute measurements and the baseline behind relative
  comparisons. [Hoefler and Belli, Rule 1][scientific]
- **M7.4** For questions about slow outcomes, report relevant named percentiles
  and their population. **Application:** Include uncertainty when supported by
  the observations. [Hoefler and Belli, Rule 8][scientific]; [NIST, §1.3.5][nist-testing]
- **M7.5** Inspect and report relevant component results alongside summaries.
  Identify subsets and opposing component trends before generalizing an aggregate.
  [Heiser, §§1.2, 5.2][heiser]
- **M7.6** **Application.** A component experiment supports a whole-system claim
  only through a justified link between that component and the whole-system
  outcome. [Heiser, §2.1][heiser]
- **M7.7** State the denominator for relative changes. Distinguish throughput
  reductions from increases in time or cost per unit of work, and percentages
  from percentage points. [Heiser, §§2.2–2.3][heiser]

**Common pitfalls.** An aggregate ranking need not hold for every component.
Unknown aggregate membership prevents a reliable statement of coverage. Failed
or missing work is not successful work with a measured latency.

### Procedure before writing a verdict

This is our application of M1, M2 and M4–M7. Its background is component coverage
and uncertainty reporting, not evidence that this sequence improves a language
model. [Heiser, benchmark subsetting and component results][heiser];
[Kalibera and Jones, §4][repetition]

1. Restate the objective and the scope actually measured. Distinguish the
   original hypothesis from an explanation developed after seeing the result.
2. Identify each metric's unit, membership and comparable conditions. If
   membership is unknown, do not assume complete or matched coverage.
3. Inspect available component results and opposing trends. State repetition
   counts, dependencies and uncertainty relevant to the conclusion.
4. Locate failures at their observed operations and conditions. Separate
   completion from speed. Describe the usable subset and what is missing;
   successful observations alone do not establish that a disruption was harmless.
5. Bound conclusions by measured conditions and uncertainty. Distinguish
   observations, predictions and proposed mechanisms. A flat series alone does
   not establish practical equivalence.
6. Keep conclusions and structured claims at the same supported scope. State
   unresolved questions and use M8 before proposing additional work.

## M8. Feasibility

**Purpose.** Allocate resources to a design that can answer its stated question.

**Read this when.** Planning execution or considering a follow-up experiment.

**Questions to answer.** What costs evidence? Which observations are essential?
Would another experiment change a decision or reduce relevant uncertainty?

**Related chapters.** M1 defines the objective, M2 coverage and M5 precision.

**Guidelines**

- **M8.1** **Application.** Estimate preparation, measurement and recovery costs
  before execution, including elapsed time and resource occupancy.
  [NIST, §5.3.3, resource constraints and backup plans][nist-design]
- **M8.2** **Application.** Balance factor coverage and repetition against the
  objective and required precision. There is no universal order for cutting
  levels versus repetitions. Preserve the effects the design must identify.
  [NIST, §5.3.3][nist-design]; [Kalibera and Jones, §9][repetition]
- **M8.3** **Application.** Budget for preparation that establishes the intended
  state or is itself part of the objective. Its cost is not inherently wasted.
  [Raasveldt et al., §§3.5–3.7][dbtest]
- **M8.4** **Application.** Prefer an economical design that can meet the objective
  with useful precision. Small size alone does not establish adequacy.
  [NIST, §5.3.3][nist-design]
- **M8.5** **Policy.** Set execution limits appropriate to the available budget
  and recovery options. Record timeouts and incomplete outcomes. The rationale
  is bounded resource use; dropping interrupted work would change the population
  being compared. No universal deadline is asserted.

**Common pitfalls.** A small design may leave the intended effects inseparable.
Omitting essential preparation changes the experiment. Removing unfinished work
without disclosure misstates completion.

### Procedure for a follow-up

This is our synthesis of M1, M2, M5 and M8. NIST supports selecting objectives
and designs appropriate to available resources. The sequence below is an
adaptation, not a demonstrated language-model result.
[NIST, §§5.3.1, 5.3.3][nist-objectives]; [design selection][nist-design]

1. Name the unresolved question. It may concern a mechanism, precision, coverage
   or repeatability. Name competing explanations when diagnosis is the objective.
2. State which observations would resolve it, contradict a proposed explanation,
   or leave it unresolved. Keep suspected mechanisms separate from measured ones.
3. Justify the components, conditions and repetitions needed. Expand coverage
   when the objective requires it; retain enough repetition for useful precision.
4. Distinguish diagnosis from comparison under revised conditions. Applying a
   change to all alternatives supports a comparison in those conditions; it does
   not by itself isolate the original cause. For diagnosis, identify evidence
   that discriminates between explanations.
5. Estimate cost and state what decision or knowledge the result could change.
   If further work cannot usefully reduce the relevant uncertainty, finish with
   an explicit limitation.

## Sources

These sources include primary research, methodological guidance and technical
specifications. They do not all constitute empirical validation of each rule.
Applications extending a source beyond its original domain are labeled above;
operating policies are identified separately. Section and rule references point
to the editions linked here. The list includes sources cited by individual
guidelines and the foundational and framework literature identified separately
below. A system-specific source can inform general methodology when the scope
of its contribution is made explicit.

- **NIST/SEMATECH.** *e-Handbook of Statistical Methods*. Sections 5.3.1
  (objectives), 5.3.2 (factors and responses), 5.3.3 (design selection), 5.3.3.2
  (blocking), 5.3.3.3 (full factorial designs), 5.5.9.9.8 (prediction beyond
  measured points), and 1.3.5 (quantitative techniques).
  These are methodological guidance, not benchmark-specific experimental results.
- **Nosek, Brian A., et al. (2018).** “The preregistration revolution.”
  *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606.
  DOI: 10.1073/pnas.1708274114. [Article][preregistration].
- **Raasveldt, Mark, Pedro Holanda, Tim Gubner and Hannes Mühleisen (2018).**
  “Fair Benchmarking Considered Difficult: Common Pitfalls in Database
  Performance Testing.” *DBTest '18*. DOI: 10.1145/3209950.3209955.
  [Paper][dbtest]. Database-specific examples supply the background for the
  explicitly labeled broader applications.
- **Kalibera, Tomas, and Richard Jones (2013).** “Rigorous Benchmarking in
  Reasonable Time.” *ISMM '13*. DOI: 10.1145/2464157.2464160.
  [Authors' updated version, Kent Academic Repository][repetition].
- **Hoefler, Torsten, and Roberto Belli (2015).** “Scientific Benchmarking of
  Parallel Computing Systems: Twelve Ways to Tell the Masses When Reporting
  Performance Results.” *SC '15*. DOI: 10.1145/2807591.2807644.
  [Paper][scientific].
- **Heiser, Gernot.** “Systems Benchmarking Crimes.” [Author's guidance][heiser].
  This is methodological commentary, not a controlled empirical study.
- **Schroeder, Bianca, Adam Wierman and Mor Harchol-Balter (2006).** “Open Versus
  Closed: A Cautionary Tale.” *NSDI '06*. [Paper][load]. Its measured outcomes
  concern the systems and load models studied.
- **Tene, Gil.** *wrk2*. [Author-maintained documentation][wrk2], particularly
  “Basic Usage” and “Discussion.” This illustrates intended-arrival accounting
  and fixed-rate measurement; it does not mandate this tool.
- **Leitner, Philipp, and Jürgen Cito (2016).** “Patterns in the Chaos—A Study
  of Performance Variation and Predictability in Public IaaS Clouds.”
  *ACM Transactions on Internet Technology*, 16(3).
  DOI: 10.1145/2885497. [Preprint][cloud].
- **Mytkowicz, Todd, Amer Diwan, Matthias Hauswirth and Peter F. Sweeney (2009).**
  “Producing Wrong Data Without Doing Anything Obviously Wrong!” *ASPLOS XIV*.
  DOI: 10.1145/1508244.1508275. [Publisher version][bias].
- **Transaction Processing Performance Council (2010).** *TPC Benchmark C*,
  revision 5.11. [Specification][tpc-c]. Durability and measurement requirements
  are cited as concrete examples, not universal settings or thresholds.

### Foundational and framework literature

These works provide foundational methodology and research context for the
benchmarking framework.

- **Jain, Raj (1991).** *The Art of Computer Systems Performance Analysis:
  Techniques for Experimental Design, Measurement, Simulation, and Modeling*.
  Wiley-Interscience. The [author's book contents][jain-book] identify Chapter 2
  on evaluation methodology and Chapters 16–19 on experimental and factorial
  designs. These provide foundational background for M1, M2 and M5.
- **Gray, Jim, editor (1993).** *The Benchmark Handbook for Database and
  Transaction Processing Systems*, second edition. Morgan Kaufmann.
  The [edition contents][gray-book] link to Gray's [introductory chapter][gray-intro].
  Its Sections 3 and 6 discuss benchmark quality criteria and misleading
  benchmark comparisons. This supplies foundational context for objectives,
  coverage and fair comparison in M1 and M2.
- **Erdelt, Patrick K. (2021; TPCTC 2020).** “A Framework for Supporting
  Repetition and Evaluation in the Process of Cloud-Based DBMS Performance
  Benchmarking.” *Performance Evaluation and Benchmarking*, pp. 75–92.
  DOI: 10.1007/978-3-030-84924-5_6. [Publisher record and abstract][erdelt2020].
  This provides framework background on repeated experiments, runtime and
  hardware measurements, and evaluation reports, relevant to M5–M7.
- **Erdelt, Patrick K. (2022; TPCTC 2021).** “Orchestrating DBMS Benchmarking
  in the Cloud with Kubernetes.” *Performance Evaluation and Benchmarking*,
  pp. 81–97. DOI: 10.1007/978-3-030-94437-7_6.
  [Publisher record and abstract][erdelt2021]. This provides framework background
  on arranging and executing database benchmarking workflows, relevant to
  execution environments and feasibility in M6 and M8.
- **Erdelt, Patrick K. (2024; TPCTC 2023).** “A Cloud-Native Adoption of
  Classical DBMS Performance Benchmarks and Tools.” *Performance Evaluation
  and Benchmarking*, pp. 124–142. DOI: 10.1007/978-3-031-68031-1_9.
  [Publisher record and abstract][erdelt2023]. This provides framework background
  on adapting benchmark tools, observing resource use including drivers, and
  studying scaling, relevant to M3 and M6.

For the three Erdelt papers, the first year in each entry is the proceedings
publication year; the TPCTC year identifies the conference.

[nist-objectives]: https://www.itl.nist.gov/div898/handbook/pri/section3/pri31.htm
[nist-variables]: https://www.itl.nist.gov/div898/handbook/pri/section3/pri32.htm
[nist-design]: https://www.itl.nist.gov/div898/handbook/pri/section3/pri33.htm
[nist-factorial]: https://www.itl.nist.gov/div898/handbook/pri/section3/pri333.htm
[nist-blocking]: https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm
[nist-testing]: https://www.itl.nist.gov/div898/handbook/eda/section3/eda35.htm
[nist-prediction]: https://www.itl.nist.gov/div898/handbook/pri/section5/pri5998.htm
[preregistration]: https://pmc.ncbi.nlm.nih.gov/articles/5856500/
[dbtest]: https://hannes.muehleisen.org/publications/DBTEST2018-performance-testing.pdf
[repetition]: https://kar.kent.ac.uk/33611/
[scientific]: https://htor.inf.ethz.ch/publications/img/hoefler-scientific-benchmarking.pdf
[heiser]: https://gernot-heiser.org/benchmarking-crimes.html
[load]: https://www.usenix.org/legacy/event/nsdi06/tech/full_papers/schroeder/schroeder.pdf
[wrk2]: https://github.com/giltene/wrk2
[cloud]: https://arxiv.org/pdf/1411.2429
[bias]: https://doi.org/10.1145/1508244.1508275
[tpc-c]: https://www.tpc.org/tpc_documents_current_versions/pdf/tpc-c_v5.11.0.pdf
[jain-book]: https://www.cs.wustl.edu/~jain/books/perf_toc.htm
[gray-book]: https://jimgray.azurewebsites.net/benchmarkhandbook/toc.htm
[gray-intro]: https://jimgray.azurewebsites.net/benchmarkhandbook/chapter1.pdf
[erdelt2020]: https://link.springer.com/chapter/10.1007/978-3-030-84924-5_6
[erdelt2021]: https://link.springer.com/chapter/10.1007/978-3-030-94437-7_6
[erdelt2023]: https://link.springer.com/chapter/10.1007/978-3-031-68031-1_9
