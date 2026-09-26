# Experiment Design Handbook

    handbook_version: "0.8.3"

Guidance on how to turn a research question into a sound benchmark experiment,
and on how to read the evidence once it exists. Read the `## Navigation` section
first; it explains what this document is and routes you to the chapters your
question needs.

## Navigation

Three documents shape an experiment here, and they do different work. The
catalog contract defines which experiments are **legal**: the workloads, systems
and parameters that exist in this deployment, and the values they may take. The
result contract defines which claims are **supportable** once a run has
finished, and how the evidence has to be read before anything is claimed. This
handbook supplies the third thing, which is neither a question of legality nor
of claiming: the methodological knowledge that separates an experiment which
answers its question from one that merely runs. Passing the contracts' checks
does not by itself establish scientific validity.

It is guidance rather than a binding interface. The two contracts are checked;
this document is knowledge you are expected to apply with judgment. It gives no
values to copy, because a benchmark experiment is not a form to fill in, and a
principle applied without its reason is as likely to spoil a design as to
improve it. Every principle below is therefore stated together with the reason
it exists, and where that reason does not hold for the question in front of you,
the reason is what governs, not the sentence. Rules have applicability
conditions: being system-independent does not mean that every rule applies to
every experiment.

These principles apply to reading a measurement as much as to planning one. The
mechanics of that reading belong elsewhere: which files a result folder holds,
which checks decide whether a run is valid, and how a verdict must be structured
and its evidence cited are the result contract's subject. But what a finished
number may be said to show, at what scope, against how much variation, and how
far beyond the levels actually run a conclusion may reach, are questions the
chapters below answer — and they do not stop applying once the run is over.

The method chapters name no workload, system or setting, because anything
specific enough to copy would be a rule to follow rather than a reason to think
with. How this particular agent's validator and harness implement some of these
rules is described separately, in `## Appendix L. Local agent interface`.

**Evidential status.** Each guideline cites a source and, where possible, a
passage. Read the citations as follows:

- An **unmarked** guideline summarizes a recommendation the cited source makes.
- **Application** marks our deduction or adaptation. The source supports the
  underlying principle, not necessarily the exact rule as worded here.
- **Policy** marks an operating choice with a stated rationale. It is not
  presented as a finding from the literature.

The sources themselves differ in kind — empirical studies, peer-reviewed
methodology papers, textbooks, standards, expert commentary and the author's own
infrastructure papers — and `## Sources` tags each accordingly. Empirical
findings keep their original scope: a result about particular cloud providers or
load generators does not establish universal performance behaviour. The two
procedures in M7 and M8 are local policy; they have not been shown to improve a
language model's performance.

**Scope.** This handbook is pitched at cloud and cluster benchmarking. Some
vocabulary (storage class, node, image, allocation, network path) and M2.3 in
particular assume a shared, allocation-based substrate. On bare metal those
specifics may not apply, though the reasons behind them still do.

**Terms.** A **factor** is an input varied deliberately. **Confounding** occurs
when the design cannot distinguish the effects of two inputs. An **operation**
is a unit of work, such as a request, transaction or job. A **component** is an
identifiable part of the measured workload or system, such as one query, request
type or job class of a suite. Use component breakdowns where the measurements support them; do not
invent missing measurements.

Principles carry identifiers such as `M1.1` or `M4.3` so that a design decision,
a review comment or a rejection can point at one precisely. Each chapter below is
a Markdown section that can be requested on its own by its exact heading.

When designing, two chapters bear on every experiment: **M1** because every
experiment makes a claim, and **M8** because every design has to fit a budget.
**M2** and **M5** apply to anything that compares. The rest depend on the shape
of the question.

| Chapter | Read it when the question involves |
| --- | --- |
| M1. The claim | any objective, hypothesis or decision criterion — that is, every design |
| M2. Factors and controls | any comparison between alternatives, any attribution of an effect to a cause, or any sweep over levels |
| M3. The load model | throughput, capacity, concurrency, arrival rate, or responsiveness under load |
| M4. Data and state | dataset scale, caching, storage, loading, or warm-up |
| M5. Repetition and noise | any comparison, or any measurement that could come out differently on a second run |
| M6. The environment | placement, shared infrastructure, resource limits, instrumentation, or where the client runs |
| M7. Metrics | choosing what to measure, or combining several measurements into one number |
| M8. Feasibility | every design with a time or resource budget, and every proposed follow-up |

When a run has finished and a verdict is being written, a different set carries
the weight. **M2** governs which factor the numbers may be attributed to, how
far a conclusion may reach beyond the levels that were actually run, and which
explanations of a flat result remain unresolved. **M3** governs what a
throughput or latency figure means given how load was offered. **M5** governs
whether a difference between conditions is larger than the variation between
repetitions of the same one. **M7** governs which quantity is quoted, at what
scope, and whether combining several numbers into one preserves the property
being claimed; its verdict procedure applies these principles before a
conclusion is written. For another experiment, use M8's follow-up procedure.

A rejection from the validator may cite one of these identifiers as its reason.
When it does, the chapter it comes from is the one worth re-reading.

## M1. The claim

**Purpose.** Decide what the experiment asserts, and what would count as
evidence against it.

**Read this when.** Always. Every design states a claim, however implicitly.

**Questions to answer.** Is the objective description, comparison, explanation,
prediction or exploration? If it is a hypothesis, what outcome would make it
false? Is the criterion for a positive result fixed before the data exists?

**Related chapters.** M2 for what a comparison has to hold equal, M5 for the
precision the answer needs, M7 for whether the metric the claim names is one the
run will actually produce.

**Guidelines**

- **M1.1** **Application.** State an answerable objective, and say which kind it
  is: description, comparison, explanation, prediction or exploration. A
  hypothesis must name a specific, measurable outcome that would refute it. A
  hypothesis that no result can contradict — "acceptable throughput", "scales
  well", "performs adequately" — is a statement of intent, and every possible run
  confirms it; terms like these need a criterion. Descriptive and exploratory
  objectives need not assert a hypothesis, but they have to say that they are
  descriptive or exploratory.
  [NIST, §5.3.1][nist-objectives]; [Ledgerwood 2018][ledgerwood]; [Jain, §2.1][jain-book]
- **M1.2** **Application.** When the question is causal or diagnostic, name the
  rival explanations and the observations that would distinguish them. The point
  of varying a factor is that competing accounts predict different outcomes at
  its levels; a design that can only produce evidence for one account
  discriminates between nothing. A descriptive comparison can estimate a
  difference without establishing its mechanism, and has no rival to name.
  [Jain, §2.1][jain-book]; [Mytkowicz et al., causal analysis][bias]
- **M1.3** **Application.** For a confirmatory decision, fix the decision
  criterion before examining the results: which metric is compared, by which
  rule, and what difference counts as practically important. A threshold chosen
  after the numbers are in is not a test, because it can always be placed where
  the data already is. Criteria developed while exploring are legitimate, but
  they are postdictions: disclose them as such and confirm them on new runs.
  Statistical significance — evidence against a stated statistical hypothesis —
  is a different thing from practical importance.
  [Nosek et al. 2018][preregistration]; [Ledgerwood 2018][ledgerwood];
  [Kalibera and Jones, §4][repetition]; [NIST, §1.3.5][nist-testing]
- **M1.4** **Application.** Decide whether this is a *measurement* — what does
  this configuration do? — a *comparison* — does one alternative differ from
  another? — or an *explanation* — why does it differ? Say which, because the
  obligations accumulate: a measurement must disclose the envelope it was taken
  in and its uncertainty; a comparison must additionally establish parity and
  repetition; an explanation must additionally produce evidence bearing on the
  cause (M6.4). [NIST, §§5.3.1, 5.3.3][nist-objectives]; [Jain, §2.1][jain-book]
- **M1.5** **Application.** Ask a question the instrument can answer. A question
  whose answer depends on a quantity the available workloads and metrics never
  produce cannot be rescued by a clever specification: obtain the missing
  evidence or narrow the question. [NIST, §5.3.2][nist-variables];
  [Gray, ch. 1, §1.3, p. 5][gray-intro]

**Common pitfalls**

- *The unfalsifiable hypothesis*, which guarantees a successful run and a
  worthless one.
- *The moving criterion*, where the threshold for "better" is decided once the
  results are visible, turning noise into a finding.
- *Postdiction presented as prediction*: an explanation found after seeing the
  result reported as though it had been the hypothesis all along.
  [Nosek et al. 2018][preregistration]
- *Question–design mismatch*, where the hypothesis is about one thing and the
  varied factor is another, so the run cannot bear on the claim.
- *Benchmarketing*, where designs are adjusted until the desired ordering
  appears. Gray identified this as the reason formal benchmark specifications
  exist at all. [Gray, ch. 1, §1.5, p. 8][gray-intro]; [Raasveldt et al., §§1, 2.2][dbtest]

## M2. Factors and controls

**Purpose.** Decide what varies, what is held equal or accounted for, and
therefore what the result can be attributed to.

**Read this when.** The design compares alternatives, attributes an effect to a
cause, or sweeps a parameter across levels.

**Questions to answer.** If the result comes out as expected, what else could
have produced it? Which levels have to be present for the conclusion I want to
be licensed by the data? Is anything varying between the arms that I have not
declared — a version, an image, a storage class, an allocation? Can the system
actually use every level of each factor I vary, or does a setting or the load
cap its demand below them?

**Related chapters.** M5, because an effect is only visible against its noise;
M6, because the environment is a factor until it is controlled; M4, because
differences in data and cached state are the easiest confound to miss.

**Guidelines**

- **M2.1** Use a design whose effects are identifiable: one varied factor, a
  full factorial across the levels of several, or a deliberate fractional design
  whose aliasing — which effects it cannot separate from which — you can state,
  together with the assumption that makes the aliasing acceptable (usually that
  the aliased interactions are small). Changing several inputs together
  estimates their joint effect; it does not identify their individual effects.
  What is not defensible is an unplanned subset of combinations, where factors
  move together and the confounding is real but unknown.
  [NIST, §5.3.3.3][nist-factorial]; [NIST, §5.3.3.4.3, confounding][nist-confounding]; [Jain, §16.3][jain-book]
- **M2.2** Everything not named as a factor must be held equal across the things
  being compared, or deliberately accounted for: version, image, dataset,
  how the data is organized and stored, client, placement, durability settings, and the
  resource envelope. Where a nuisance factor cannot be held equal — the node an
  arm lands on, the time of day it runs — block on it, so that every alternative
  meets every level of it, and randomize what cannot be blocked. Literal
  identity is not required for a difference that is itself studied or accounted
  for in the design. [NIST, §5.3.3.2, blocking][nist-blocking];
  [Raasveldt et al., §§3.1–3.3][dbtest]
- **M2.3** **Application.** Prevent opportunistic access to shared resources from
  becoming an uncontrolled factor. Wherever an alternative may consume more than
  it is guaranteed — spare cores, unclaimed memory, an unthrottled disk or link —
  what it actually receives depends on what else is running and on its own
  demand, so the allocation varies exactly where the comparison is being made.
  Either fix the share each alternative can obtain, or measure under contention
  on purpose and treat that contention as a declared factor, or replicate across
  allocations and analyse the variation. State what is guaranteed and what can
  vary; resource limits alone do not establish isolation.
  [Leitner and Cito, §§2, 5.2][cloud]
- **M2.4** Give every alternative comparable tuning effort, and disclose that
  effort. A well-configured system measured against a default-configured one
  measures the configuration, and the incentive to under-tune the baseline is
  structural rather than malicious, which is why parity has to be a rule and not
  an intention. **Application:** a comparison of defaults is legitimate when it is
  explicitly scoped to defaults. [Raasveldt et al., §3.2][dbtest];
  [van der Kouwe et al. 2020, D3][crimes-sp]; [Manolescu and Manegold, slides 40–44][manolescu]
- **M2.5** Ensure the alternatives perform equivalent work: the same semantics,
  data types, durability and isolation guarantees, and results verified to agree.
  A faster answer that is a different answer is not a performance result.
  **Application:** where guarantees differ on purpose, the comparison is of the
  whole bundle, and the tradeoff has to be described.
  [Raasveldt et al., §§3.3, 3.8][dbtest]
- **M2.6** The factors declared as varied and the factors the specification
  actually varies must be the same set. Record the settings actually in effect.
  An undeclared varying value is a confound; a declared but constant one is a
  false statement about the design. Random variation between repetitions is not
  by itself a confound — that is M5's subject. [Hoefler and Belli, Rule 9][scientific]
- **M2.7** **Application.** Include the levels you intend to conclude about. A
  direct conclusion holds at the levels that were run, so if the claim is meant
  to cover a scale, a concurrency or a configuration, that value has to appear in
  the design — or the claim has to be narrowed to what did appear. A model may
  reach past the tested levels only when it is declared as a model, its
  assumptions are stated, and its predictions are checked against confirmatory
  runs; a model that fits well at the design points need not fit well away from
  them. [NIST, 5.5.9.9, using the model beyond the data domain][nist-prediction];
  [NIST, confirming model predictions][nist-confirm]; [Jain, §15][jain-book]
- **M2.8** Cover the part of the evaluation space where the change under test
  might do harm, not only where it should help. An evaluation that can only
  produce good news is selective by construction. Running a subset of a standard
  workload needs a stated reason, and conclusions drawn from it are limited to
  that subset. [van der Kouwe et al. 2020, A1–A3][crimes-sp]; [Heiser, A1–A2][heiser];
  [Raasveldt et al., Appendix A][dbtest]
- **M2.9** **Application.** Check whether other settings or the offered load
  could limit the benefit of a resource increase — an interaction, where one
  factor's effect depends on another. Before the run, inspect parallelism, pools
  and concurrent demand, and decide whether the question concerns changing the
  allocation with settings fixed or changing allocation and tuning together;
  changing both measures their joint effect unless the design can separate them
  (M2.1). Afterward, a flat result supports a narrow statement about the tested
  workload, levels and settings. Low average utilization alone neither proves
  the resource change was never exercised nor explains the result: bursts,
  individual cores and other limits may matter. State which explanation remains
  unresolved, use M6.4 for any mechanism claim, and choose a follow-up only if
  distinguishing the explanations would answer the question.
  [NIST, §5.3.2, model matrix and interaction term][nist-variables]; [Jain, ch. 16][jain-book]

**Common pitfalls**

- *Apples versus oranges*: the alternatives differ in what they compute, not
  only in how fast — different types, approximate results, weaker durability, or
  a stripped-down component measured against a complete system.
  [Raasveldt et al., §3.3][dbtest]
- *The elastic envelope*, where guarantees sit below limits and each arm
  silently receives a different machine.
- *Unequal effort*: one side tuned and the other left at defaults, or a baseline
  old enough that the comparison flatters the newcomer.
- *Over-specific tuning*, chosen for this benchmark alone and generalizing
  nowhere; running further, non-standard operations and inputs alongside the
  standard workload is the remedy. [Raasveldt et al., §3.4][dbtest]
- *The design that cannot lose*, covering only the conditions where the expected
  answer is the likely one.
- *The joint change read as separate effects*: two inputs moved together and the
  outcome attributed to one of them.
- *The unexplained flat result*: a resource sweep reported as general resource
  independence, or dismissed as never tested, without distinguishing what was
  observed from the mechanism that might explain it.

## M3. The load model

**Purpose.** Decide how work arrives at the system, which decides which
questions the run can answer at all.

**Read this when.** The question involves throughput, capacity, concurrency,
arrival rate, latency, or behaviour under load. For batch work, describe how jobs
are submitted and scheduled instead of assuming an external request generator.

**Questions to answer.** In the situation the question describes, does demand
arrive independently of completions, or do users wait for a response before
asking again? Is this measuring capacity, or response time at a stated demand?
Has one of my own client settings already fixed the quantity I mean to report?

**Related chapters.** M7 for which summary a latency claim needs; M5, because
tail behaviour needs many more observations than a mean does.

In a **closed** load model a fixed number of clients each wait for a response
before sending again, possibly after a delay called think time, so offered load
is a function of the system's own speed. In an **open** model, requests arrive at
a rate that does not depend on whether earlier ones completed. **Partly open**
models, where sessions arrive independently but each session waits for its own
responses, lie between the two. Schroeder, Wierman and Harchol-Balter showed that
in the systems they studied the models behave very differently — a closed
generator held response time nearly flat as load rose and largely hid the effect
of scheduling policy, both of which an open generator exposed — so a system
evaluated under the wrong model can support the wrong conclusion. [Schroeder et al.][load]

**Guidelines**

- **M3.1** Match the load model to the population and arrival behaviour the
  question describes: a fixed population that waits is closed, independent
  arrivals are open, independently arriving sessions are partly open. Separately
  decide whether the question is about *capacity* — how much work per unit time
  the system absorbs — or about *responsiveness* — how long a request takes at a
  given demand. Either can be studied under any of the models; the objective
  alone does not select one, and convenience of configuration should select
  none. [Schroeder et al., guiding principles][load]
- **M3.2** **Application.** Do not present a quantity one of your own settings has
  fixed as a property of the system. Report offered and achieved rates. If the
  client is capped at a rate the system could exceed, the measured throughput is
  the cap; report it as achieved throughput at that offered demand, not as the
  system's capacity. A constant-rate run is a legitimate measurement that simply
  does not establish a maximum. [Schroeder et al.][load]; [Tene, wrk2][wrk2]
- **M3.3** **Application.** A maximum-sustainable-throughput claim requires that
  sustainability be defined and its limit demonstrated rather than assumed.
  Declare in advance the requirements a load level must meet — completion,
  response-time bound, error rate, absence of growing backlog, observation
  duration, as applicable — raise the load until they fail, and report the
  highest tested level that met them. If load was never raised that far, the
  figure is a lower bound and has to be reported as one. A throughput plateau
  alone does not identify the limiting resource (M3.6, M6.4). Standard benchmark
  specifications illustrate explicit response-time and sustained-measurement
  requirements; their particular thresholds belong to each benchmark. [TPC-C 5.11, §§5.2.5, 5.5][tpc-c]
- **M3.4** Match the load model to the population the question describes. A
  closed model represents a fixed population that waits, and latency measured
  under it is correct *for that population*. It misleads when used to describe
  demand that arrives independently: because a closed generator's offered load
  is a function of the system's own speed, a stall makes it issue fewer
  requests, so the requests that would have met the stall are never sent and
  never counted — coordinated omission — which understates the tail. Where the
  question is about independent arrivals, drive an open model at a fixed rate
  and measure each request from its intended send time, not from when it was
  actually sent, or state that a closed-loop tail understates. **Application:**
  report work that could not be issued or completed rather than letting it drop
  out of the distribution. [Schroeder et al.][load]; [Tene, "How NOT to Measure Latency"][tene-talk];
  [Tene, wrk2 README, latency measurement note][wrk2]
- **M3.5** Report the population and think time behind every latency figure from
  a closed model, and the arrival process and rate for an open one. In a closed
  system latency is largely a function of how many requests are in flight, so
  the number means little without them. Varying concurrency is legitimate when
  it is the declared factor and its effects on throughput and waiting are read as
  consequences of the closed population. [Schroeder et al.][load]
- **M3.6** **Application.** Confirm the load generator was not itself the
  bottleneck. A saturated client produces a beautifully flat curve that describes
  the client. Compare intended with delivered work, and monitor the generator,
  before attributing a plateau to the system under test.
  [TPC-C 5.11, Clause 6, SUT, driver and communications][tpc-c]; [Erdelt 2024 (TPCTC 2023)][erdelt2023]

**Common pitfalls**

- *Throughput from a throttled run*, reported as capacity: a measurement of your
  own configuration file rather than of the system.
- *An open-arrival claim from closed-loop measurements*, where the tail is
  understated by an amount that depends on the workload and on where the stalls
  fall.
- *Latencies compared at different achieved throughputs*, where the two sides
  were doing different amounts of work.
- *Concurrency confused with offered load*: treating a change in a closed client
  population as if it were an independently imposed arrival rate, and reporting
  its consequences as though demand had been held fixed.
- *Missing submissions counted as successes*: work that was never issued or never
  completed silently disappearing from the latency distribution.

## M4. Data and state

**Purpose.** Decide how much data there is and what condition the system is in
when the measurement starts.

**Read this when.** The design involves dataset scale, caching, storage
behaviour, loading, or warm-up.

**Questions to answer.** Does the working set fit in memory at this size, and is
that the regime the question is about? What state does one measurement leave
behind for the next? Is preparation being charged to one alternative and not to
another?

**Related chapters.** M2, because unequal state is a confound; M8, because
preparation competes with measurement for the budget.

**Guidelines**

- **M4.1** **Application.** Size the dataset against the memory envelope
  deliberately and state which regime is being measured: fully cached, partly
  cached, or larger than memory. Distinguish the total input size from the
  working set — the data and state the workload actually touches — and describe
  the observed cache behaviour rather than inferring it from input size alone. A
  design that lands in a regime by accident answers a question nobody asked.
  [Raasveldt et al., §§3.5–3.6][dbtest] (the working-set framing is ours)
- **M4.2** **Application.** Match the data volume to the question. A dataset that
  fits entirely in cache does not exercise storage reads, so it cannot test a
  read-path storage claim and favours whichever side's advantage lies in avoiding
  that input and output. Durable writes still reach the device regardless of
  cache, so fitting in memory does not rule out every storage experiment; what
  matters is showing that the storage path the claim is about is actually used.
  This is a deduction from the difference between reads and durability
  obligations, not a result measured for every system. [TPC-C 5.11, §3.5][tpc-c]
- **M4.3** Declare the cache state each measurement is taken in — cold with
  caches flushed, warm after prior activity, or hot and steady — and the
  procedure used to reach it. All three are legitimate; mixing them within one
  comparison is not, and measuring one side's first run against another's tenth
  does exactly that. A truly cold run is hard to obtain: restarting the system
  under test can leave operating-system caches warm, and in a virtualized environment the
  host may cache as well. [Raasveldt et al., §§3.5–3.6, Appendix A][dbtest];
  [Manolescu and Manegold, slides 31–35][manolescu]
- **M4.4** Separate the cost of preparing the system from the cost of measuring
  it. Loading, building auxiliary structures, collecting statistics and converting
  formats
  are real costs: count them or exclude them explicitly, and treat every
  alternative the same way. Watch for preparation a system performs
  automatically, such as auxiliary structures or encodings built on first
  access. Preparation
  that happens implicitly for one and explicitly for another is a hidden
  subsidy. [Raasveldt et al., §3.7][dbtest]
- **M4.5** **Application.** Measure inside the interval the question is about. By
  default that is a steady interval: ramp-up and cache filling belong either
  outside the measured window or inside it by explicit decision, applied
  identically to every alternative. Where the question concerns start-up or
  transient behaviour, measure that instead and say so. Define the measurement
  window; for a claimed steady state, say how it was established; disclose when
  it was not reached. No automatic detector of steady state is universally
  reliable: in Kalibera and Jones's study, on-line warm-up heuristics often
  stopped too early or ran far too long. [Kalibera and Jones, §6][repetition];
  [TPC-C 5.11, §5.5][tpc-c];
  [Raasveldt et al., Appendix A][dbtest]
- **M4.6** Verify the results are correct before believing they are fast. A side
  that errors, returns less output, or silently skips work is not competing.
  **Application:** report incomplete work separately; a comparison restricted to
  the work both sides completed has to say that it is restricted.
  [Raasveldt et al., §3.8][dbtest]

**Common pitfalls**

- *The toy dataset with the production claim*: a scale chosen for convenience
  and a conclusion stated without one.
- *The selective data range*, stopping just before the point where the answer
  stops being flattering.
- *The unpriced preparation*, such as an auxiliary structure built during a phase
  nobody
  timed.
- *Ramp-up folded into the measurement*, so the result mostly reports how long
  the caches took to fill.
- *Skipped work counted as fast work.*

## M5. Repetition and noise

**Purpose.** Decide how many observations are needed before a difference can be
told apart from ordinary variation, and how precise the answer has to be.

**Read this when.** Anything is being compared, or a measurement could come out
differently on a second run — which, on shared infrastructure, is all of them.

**Questions to answer.** How large is the difference I expect, next to how much
this measurement moves between identical runs? At which level does the variation
I fear live: inside a run, between runs, or between deployments? Which
observations share conditions and are therefore not independent? If the
environment drifted during the experiment, could I tell that apart from the
effect?

**Related chapters.** M6 for where the variation comes from; M7 for how to
summarize what repetition produces.

**Guidelines**

- **M5.1** A single run yields no estimate of its own uncertainty. Any design
  that compares needs enough repetitions, at the levels where variation arises,
  that the spread can be estimated and the observed difference judged against
  it; with one run each, an effect and a fluctuation are indistinguishable by
  construction. Choose the number for the precision the question needs — a
  fixed minimum count does not by itself guarantee useful precision.
  [Kalibera and Jones, §§3, 9][repetition]
- **M5.2** Report uncertainty alongside any central value. A mean or median
  without it is uninterpretable, and published evaluations frequently omit it:
  Kalibera and Jones found no measure of variation in most execution-time papers
  they surveyed, and van der Kouwe et al. found it the most widespread flaw in
  theirs. Distinguish the spread of individual observations from the
  uncertainty of an estimate: the first describes the system, the second
  describes how well the experiment pinned down a quantity, such as the effect of
  a change. [Kalibera and Jones, §§1, 4][repetition]; [Hoefler and Belli, Rule 5][scientific];
  [van der Kouwe et al. 2020, B4][crimes-sp]; [Raasveldt et al., Appendix A][dbtest]
- **M5.3** State whether the measurements are deterministic. For
  non-deterministic data give confidence intervals and compare using a test or
  an interval rather than by eye. Non-overlapping intervals indicate a
  difference, but overlapping ones do not prove equality; where the comparison
  is the point, prefer an interval on the effect itself, such as the ratio of the
  means. **Application:** a flat-looking series does not establish practical
  equivalence, which requires showing that any difference is smaller than a
  margin declared in advance. [Kalibera and Jones, §§4, 10][repetition];
  [Hoefler and Belli, Rules 5, 7][scientific]; [NIST, §1.3.5][nist-testing]
- **M5.4** Do not assume the measurements are normally distributed; performance
  distributions are usually skewed with a long tail, so check before summarizing.
  A mean, a median and a percentile answer different questions — the expected
  cost, the typical case, the threshold below which a stated fraction of
  observations falls — so choose the summary the question asks for rather than
  treating any as inherently more honest. [Hoefler and Belli, Rules 6–8][scientific]
- **M5.5** Repeat at the level where the variation you fear actually lives.
  Consecutive iterations inside one process share caches and warm state and are
  not independent samples of a deployment; if placement is the suspected source,
  the deployment is what has to be repeated. More dependent observations are not
  more independent evidence. [Kalibera and Jones, §§3, 6–9][repetition]
- **M5.6** **Application.** On shared infrastructure, estimate both
  within-allocation and between-allocation variation rather than assuming which
  is larger, and allocate repetitions accordingly. The placement an arm draws can
  persist for its whole lifetime. In Leitner and Cito's study of four public
  clouds, variation between instances exceeded variation within an instance in
  all but one configuration, and multi-tenancy made performance markedly less
  predictable only for some providers; treat such orderings as findings about the
  studied providers to check, not a law to assume on a given cluster.
  [Leitner and Cito, §§5.2.1–5.2.2, Tables 4 and 6][cloud]
- **M5.7** Randomize or block the order in which alternatives are measured. If
  all of one runs before all of the other, drift in the environment over time is
  indistinguishable from the treatment. **Application:** a fixed alternating order
  is better than blocked execution but does not by itself remove time effects
  that follow the same rhythm. [NIST, §5.3.3.2][nist-blocking];
  [NIST, §5.1.3, process drifts][nist-steps]; [Mytkowicz et al., setup randomization][bias]

**Common pitfalls**

- *The single-run comparison*: two numbers, one from each side, and a
  conclusion.
- *Blocked execution*, all of one and then all of the other, with the
  neighbouring load changing in between.
- *Discarding inconvenient runs* without a rule fixed in advance and disclosed,
  which is cherry-picking whatever the intention was.
- *A nonsignificant difference reported as equality.*
- *Measurement bias mistaken for an effect*. Mytkowicz and colleagues showed
  that changes as innocuous as environment size or link order can shift results
  enough to reverse a conclusion, so an unexplained difference deserves suspicion
  before it deserves publication. [Mytkowicz et al.][bias]

## M6. The environment

**Purpose.** Decide where everything runs, what will be recorded about it, and
how interference will be investigated.

**Read this when.** The design touches placement, shared infrastructure,
resource limits, instrumentation, or the location of the client.

**Questions to answer.** Which parts of this machine are shared with something I
do not control? If I later want to attribute the effect to a particular
resource, will anything have recorded that resource? What would distinguish a
proposed cause from another explanation? Could someone else rebuild this setup
from what the specification records?

**Related chapters.** M2, because an uncontrolled environment is an undeclared
factor; M5, because what cannot be controlled has to be repeated instead.

**Guidelines**

- **M6.1** **Application.** Keep the load generator off the machine under test,
  unless co-location is itself the deployment being studied. Either way, say
  where it ran and show that it was not competing for the resource the
  experiment is about. [TPC-C 5.11, Clause 6, SUT, driver and communications][tpc-c];
  [Erdelt 2024 (TPCTC 2023)][erdelt2023]
- **M6.2** **Application.** Control placement. On a heterogeneous cluster the node
  is a factor, and an unpinned alternative draws a different machine than the
  one it is measured against. Pinning is one control; pairing alternatives on
  the same node, blocking on node, or randomizing placement and replicating are
  others. [NIST, §5.3.3.2][nist-blocking]; [Leitner and Cito, §§2, 5.2.1][cloud]
- **M6.3** Disclose the platform sufficiently for another investigator — or a
  later run of this same agent — to reproduce or contest the result: hardware,
  kernel, versions, images, configuration values, compilation settings, storage
  class and network path. This is not bookkeeping; a result nobody can reproduce
  cannot be checked. [Raasveldt et al., §3.1, Appendix A][dbtest];
  [van der Kouwe et al. 2020, F1–F2][crimes-sp]; [TPC-C 5.11, Clause 8, full disclosure][tpc-c];
  [Manolescu and Manegold, slides 149–160][manolescu]
- **M6.4** **Application.** Instrument the resource you may later want to blame.
  An explanation naming a mechanism that nothing measured is a story, not a
  finding. But utilization data lets a proposed mechanism be tested for
  plausibility, not confirmed as the cause: a utilization rise and a slowdown can
  share a third cause, so attribution needs a discriminating intervention or
  another identification method, not utilization correlation by itself. Label
  untested mechanisms as hypotheses. Missing telemetry is not evidence that
  interference was absent. [Mytkowicz et al., causal analysis][bias];
  [Manolescu and Manegold, slides 45–53][manolescu]
- **M6.5** Where isolation from other tenants cannot be guaranteed, treat that as
  a declared source of variation under M5.6 rather than an inconvenience to leave
  unmentioned. State what isolation is known and what remains uncontrolled.
  [Leitner and Cito, §§2, 5.2][cloud]

**Common pitfalls**

- *The invisible client*, generating load on the machine under test, unreported.
- *The missing platform specification*, which makes every number unverifiable.
- *Heterogeneous alternatives*: different nodes or storage classes, same table.
- *Monitoring switched off*, after which a failure is indistinguishable from
  slowness.
- *Correlation reported as mechanism.*

## M7. Metrics

**Purpose.** Decide what quantity is recorded, and how many numbers become one
without losing the property being claimed.

**Read this when.** Choosing what to measure, or combining measurements into a
single reported figure.

**Questions to answer.** What exactly is the unit of work behind this rate? Over
which population and interval? Does the question ask about the typical case or
about the tail? Will combining these numbers preserve the property being
claimed, or destroy it?

**Related chapters.** M3, because the load model decides which latency figures
mean anything; M5, because a summary without its uncertainty is not a result.

**Guidelines**

- **M7.1** Define the metric before reporting it: throughput of which unit of
  work, latency between which two points, cost including which phases. When
  reporting a derived quantity, record the measurements it was derived from.
  [Jain, §3.1][jain-book]; [NIST, §5.3.2, selecting responses][nist-variables]
- **M7.2** Prefer aggregating the underlying totals: an overall rate is total
  work divided by total time, and an overall cost is the sum of the costs. Where
  only the per-observation figures survive, the mean has to match how the
  observations were taken — the harmonic mean recovers the overall rate when each
  observation covers the same amount of work, the arithmetic mean when each
  covers the same span of time — so state which. Adding rates that were measured
  over different durations does not give the rate over their common interval,
  and similar durations alone do not show that the measurements overlapped.
  Prefer not to summarize ratios directly; where only normalized scores survive,
  the geometric mean is the accepted summary, but state the quantity it
  estimates rather than read it as an elapsed-time speedup.
  [Hoefler and Belli, §3.1.1, Rules 3–4][scientific]
- **M7.3** Never report a ratio without the absolute values behind it. A speedup
  without a baseline time cannot be sanity-checked and hides whether the
  quantities involved matter at all. [Hoefler and Belli, Rule 1][scientific];
  [van der Kouwe et al. 2020, F4][crimes-sp]; [NIST, §5.3.2][nist-variables]
- **M7.4** For tail-sensitive questions report named percentiles, and the
  population they describe, rather than a central value, because a mean conceals
  precisely the behaviour a responsiveness claim is about. **Application:** give
  their uncertainty where the number of observations supports it.
  [Hoefler and Belli, Rule 8][scientific]; [Tene, "How NOT to Measure Latency"][tene-talk]
- **M7.5** Report per-component results and not only an aggregate. An aggregate
  that improves while one component regresses badly is an important outcome, and
  only the breakdown shows it. Identify subsets and opposing trends before
  generalizing an aggregate. [van der Kouwe et al. 2020, A2, F3][crimes-sp]; [Heiser, A2, E2][heiser]
- **M7.6** **Application.** Do not promote a microbenchmark to a system claim
  without evidence linking the two. A probe of one component measures it under
  conditions the whole system may not reproduce; a system-level conclusion needs
  evidence that the component's behaviour carries over, not the probe alone.
  [van der Kouwe et al. 2020, B1][crimes-sp]; [Heiser, B1][heiser]
- **M7.7** Compute overheads against the baseline and state the denominator.
  Keep percentages and percentage points distinct. A throughput reduction is not
  the same quantity as an increase in cost per unit of work, and treating them as
  interchangeable understates the cost whenever the system was not already
  saturated. [van der Kouwe et al. 2020, B2–B3][crimes-sp]; [Heiser, B2–B3][heiser]

**Common pitfalls**

- *Averaged ratios*, such as the arithmetic mean of normalized scores, which
  depends on the baseline and rarely estimates the quantity intended; name the
  quantity wanted and the mean that recovers it.
- *Relative numbers only*, leaving no way to sanity-check the result.
- *The aggregate that hides a regression.*
- *The undefined metric*, such as a throughput figure whose unit of work is
  never stated, or an aggregate whose membership is unknown.
- *Failed work given a latency*, as though it had succeeded.

### Procedure before writing a verdict

**Policy.** This procedure is a local application of M1, M2 and M4–M7. It is
guidance for the agent, not a separately validated scientific method. Heiser's
discussion of benchmark subsets and missing component results
([Heiser, A2, E2][heiser]) supports limiting subset claims and inspecting the
breakdown; Hoefler and Belli's rules on reporting conditions and uncertainty
([Hoefler and Belli][scientific]) support stating the comparison's conditions and
variability. Neither source establishes that this particular sequence improves a
language model.

1. Restate the original question and the hypothesis that was actually tested.
   Do not silently strengthen a question about whether an effect changes into a
   claim that it always increases, and keep an explanation developed after
   seeing the result distinct from the original hypothesis (M1.3).
2. Identify the metric, its unit, the components it covers and the matched
   settings. A phase aggregate and an individual component timer are different
   measurements. If an aggregate's membership is unknown, do not assume that it
   represents either the full workload or the common successful subset.
3. Inspect each available component's measurements before generalizing an
   aggregate ranking. Preserve reversals between components or settings. State
   the observed repetition count, the dependencies between observations and the
   uncertainty; parallel clients or streams within one repetition do not
   create additional independent repetitions.
4. Locate failures at their observed component, configuration and load. State
   completion and speed separately. A common successful subset may support a
   limited comparison, subject to other validity checks. It cannot settle the
   missing components, and successful timings alone do not show that a restart
   or other disruption was harmless. Missing data do not automatically strengthen
   the preferred result.
5. Bound each conclusion by the tested levels and available uncertainty.
   Distinguish observations, model predictions and proposed mechanisms. A
   descriptive flat series does not establish equivalence, meaning that any
   difference is smaller than a predeclared practically important margin.
6. Write the verdict and the answer to each question at that same scope, and
   keep structured claims at the scope of the prose. Keep unresolved evidence
   visible. An automatic check that declines a comparison is not permission to
   assert that comparison in prose. Use M8's follow-up procedure before
   proposing another experiment, or finish with a limited conclusion.

For example, suppose two components have timings for both systems and a third
fails at the highest concurrency. The first system's better aggregate does not
establish that it wins both successful components. Compare those components
separately, report where the third failed, and leave its speed comparison
unresolved. Do not describe the failure as occurring at every concurrency.

## M8. Feasibility

**Purpose.** Decide whether this design can actually be run, and where to spend
the budget it has.

**Read this when.** Always. Every design competes with a time and resource
budget. Also before proposing any follow-up experiment.

**Questions to answer.** How many phases does this expand to, and how long will
they take? If the budget forces a cut, which levels can go without costing the
ability to tell an effect from noise? Is time being spent on preparation that
buys no evidence? Would another experiment change a decision or reduce relevant
uncertainty?

**Related chapters.** M1 for the objective; M2 for coverage, because levels are
usually the first thing cut; M5 for precision, because repetitions are what make
a comparison readable.

**Guidelines**

- **M8.1** **Application.** Estimate the cost of a design before committing to it —
  preparation, measurement and recovery, in phases, wall-clock time and cluster
  occupancy — and check that every planned run is feasible. Leave slack in the
  budget for runs that have to be repeated. [NIST, §5.1.3][nist-steps];
  [NIST, §5.3.3][nist-design]
- **M8.2** **Application.** Factorial designs multiply. When one is too large, cut
  first what cannot discriminate between the competing explanations — usually
  levels — and keep the effects the design must identify. There is no universal
  order for cutting levels versus repetitions: balance coverage against the
  precision the objective requires, but never cut repetitions below what is
  needed to tell the effect from noise, because without that no comparison is
  readable at all. [NIST, §5.3.3][nist-design]; [Kalibera and Jones, §9][repetition];
  [Jain, §16.3.3][jain-book]
- **M8.3** **Application.** Spend the budget on evidence. Preparation that
  establishes the intended state — a properly cold run, a loaded dataset with its
  auxiliary structures — is part of the measurement and is not wasted, even when it is slow.
  Time spent artificially slowing preparation, or preparing state the question
  does not need, buys no evidence and is subtracted directly from what could have
  been measured. [Raasveldt et al., §§3.6–3.7][dbtest]
- **M8.4** **Application.** Prefer the most economical design that can refute the
  hypothesis or meet the objective with useful precision. Where follow-up
  experiments are limited or unavailable, a decisive narrow experiment is worth
  more than a broad sweep that ends inconclusively. Small size alone does not
  establish adequacy. [NIST, §5.1.3, keep the experiment simple][nist-steps];
  [NIST, §5.3.3][nist-design]; [Jain, Box 2.1][jain-book]
- **M8.5** **Policy.** Bound every phase with a deadline appropriate to the budget
  and recovery options, so one hung component costs a run instead of the entire
  budget. Record timeouts and incomplete outcomes: silently dropping interrupted
  work would change the population being compared. No universal deadline is
  asserted. Implementation background: [Erdelt 2022 (TPCTC 2021)][erdelt2021]

**Common pitfalls**

- *The sweep that never finishes.*
- *Repetitions traded for levels*, producing a large design that cannot support
  a single claim.
- *Budget spent on preparation* the question does not need, rather than on
  measurement.
- *Essential preparation omitted to save time*, which changes the experiment.
- *Exploration where only one attempt was available.*

### Procedure for a follow-up

**Policy.** This is a local application of M1, M2, M5 and M8. The NIST/SEMATECH
handbook supports [setting explicit objectives][nist-objectives] and
[selecting a design for those objectives and available resources][nist-design].
The procedure below is our adaptation, not a demonstrated language-model result.

1. Name the unresolved question. It may concern a mechanism, precision, coverage
   or repeatability. When diagnosis is the objective, name the competing
   explanations the follow-up could distinguish, and keep a suspected mechanism
   separate from a measured one.
2. State in advance which observations would support or contradict each
   explanation, and which outcome would leave the question unresolved.
3. Choose the smallest workload and set of conditions that can answer that
   question. Justify each added component, factor level and repetition; retain
   enough repetitions to assess variability. Explain any expansion to the full
   workload.
4. State whether the goal is diagnosing the original outcome or comparing
   performance under revised settings. Applying a change equally to all
   alternatives supports a comparison under those settings; it does not by
   itself isolate the original cause. For diagnosis, identify which intervention
   and measurements distinguish the explanations.
5. Explain why the proposed change addresses the suspected constraint, estimate
   its cost, and state what decision or knowledge the result could change. If it
   cannot resolve useful uncertainty within the budget, finish with an explicit
   limited conclusion.

## Appendix L. Local agent interface

This appendix describes how this agent's implementation applies some of the
rules above. It is interface documentation and operating policy, not
methodology, and it is the only part of this handbook that names a specific
workload.

**Validator.** The current validator implements restricted checks associated
with M1.1, M2.1, M2.3, M2.6 and M5.1: a heuristic against vague adequacy
claims, separable declared resource factors, equal resource requests and limits,
agreement between declared and varied factors, and a minimum repetition count.
**Policy:** these are local interface rules. Equal requests and limits are one way
to satisfy M2.3, not a universal condition for a valid experiment, and a minimum
repetition count does not guarantee useful precision (M5.1). A joint resource
change can answer a joint-effect question (M2.1) even where the current
interface rejects it. If the interface cannot express a scientifically
appropriate design, record that limitation rather than distorting the design.

**YCSB.** The catalog's `max_execution_time` caps the benchmarking phase and
`operations_scale` sets the total operation count, which is split across the
pods. Without a cap each pod receives a fixed share and may finish at a
different time, while the report's phase throughput adds up the pods' separate
rates — which M7.2 warns against. A capped pod still stops early once its share
of operations is exhausted, so a cap needs enough operations to keep every pod
busy. Neither control excludes warm-up (M4.5). **Policy:** the validator warns,
without refusing, when a YCSB round runs several pods without a cap. The
interpretation assessor withholds a throughput shape or ranking when a phase's
summed rate exceeds its pods' work spread over the longest pod duration by more
than 20%, or when that cannot be checked. The threshold targets large
distortions; it is not a scientific boundary.

**Harness.** Before a verdict can be recorded, the harness requires the
Navigation section and M2, M3, M5 and M7 to have been read. The verdict
procedure also draws on M1, M4 and M6, which can be requested by heading in the
same way.

## Sources

Each source is tagged with its evidential type, because the entries carry
different weight:

- **[E]** peer-reviewed empirical study — can support empirical claims, within
  the systems and conditions it studied;
- **[M]** peer-reviewed methodology or position paper — supports normative
  recommendations;
- **[T]** textbook or institutional reference work;
- **[S]** standard specification — authoritative for what that benchmark
  requires; its thresholds are not general findings;
- **[C]** expert commentary, tutorial or practitioner material — credible, but not
  peer-reviewed; never the sole support for a rule here;
- **[O]** the author's own work — describes this infrastructure; not independent
  support for a general rule.

Section and rule references point to the editions linked here. Where the
literature is silent, rules are labelled Application or Policy above.

Experimental design and statistics:

- **[T]** NIST/SEMATECH, *e-Handbook of Statistical Methods*. Sections 5.1.3
  (steps and practical considerations), 5.3.1 (objectives), 5.3.2 (factors and
  responses), 5.3.3 (design selection), 5.3.3.2 (randomized block designs),
  5.3.3.3 (full factorial designs), 5.3.3.4.3 (confounding), 5.5.9.9 (using a
  fitted model beyond the design points, and confirming its predictions), and
  1.3.5 (quantitative techniques, including practical versus statistical
  significance). General methodological guidance, not benchmark-specific.
- **[T]** Raj Jain, *The Art of Computer Systems Performance Analysis: Techniques
  for Experimental Design, Measurement, Simulation, and Modeling*,
  Wiley-Interscience, 1991 — evaluation methodology (ch. 2), metrics (ch. 3),
  regression and prediction beyond the measured range (ch. 15), and experimental
  and factorial designs (chs. 16–19). [Contents][jain-book].
- **[M]** Brian A. Nosek, Charles R. Ebersole, Alexander C. DeHaven and David T.
  Mellor, "The preregistration revolution", *PNAS* 115(11), 2600–2606, 2018.
  DOI: 10.1073/pnas.1708274114. [Article][preregistration]. A perspective from
  psychology; its application to benchmarking is ours.
- **[C]** Alison Ledgerwood, "The preregistration revolution needs to distinguish
  between predictions and analyses", *PNAS* 115(45), E10516–E10517, 2018 (letter).
  DOI: 10.1073/pnas.1812592115. [Letter][ledgerwood].

Database benchmarking and benchmark construction:

- **[T]** Jim Gray (ed.), *The Benchmark Handbook for Database and Transaction
  Processing Systems*, 2nd ed., Morgan Kaufmann, 1993 — chapter 1, Gray's
  introduction: the criteria of a useful benchmark (relevance, portability,
  scalability, simplicity) and the diagnosis of "benchmarketing". An expert essay
  within a reference work. Cited by section and page of the print edition
  (relevance, §1.3, p. 5; benchmarketing, §1.5, p. 8); the online edition's
  numbering may differ. [Edition contents][gray-book]; [chapter 1][gray-intro].
- **[M]** Mark Raasveldt, Pedro Holanda, Tim Gubner and Hannes Mühleisen, "Fair
  Benchmarking Considered Difficult: Common Pitfalls in Database Performance
  Testing", *DBTest '18*. DOI: 10.1145/3209950.3209955. [Paper][dbtest]. Its
  experiments are illustrative mock benchmarks, not a prevalence study.
- **[M]** Karl Huppler, "The Art of Building a Good Benchmark", TPCTC 2009 —
  [paper][huppler].
- **[C]** Ioana Manolescu and Stefan Manegold, *Performance Evaluation in Database
  Research: Principles and Experience*, tutorial, ICDE 2008 — [slides][manolescu].
  Cited by slide number (235 slides): tuning and fairness (40–44), profiling and
  monitoring to find out what happens (45–53), hot vs cold runs (31–35), hardware
  specification and repeatability (149–160). Its experiment-design section
  (55–58) reproduces Jain and is not cited separately.
- **[S]** Transaction Processing Performance Council, *TPC Benchmark C Standard
  Specification*, revision 5.11 — durability (§3.5), maximum qualified
  throughput (§5.2.5), steady state and measurement interval (§5.5), SUT,
  driver and communications definition (Clause 6), and full disclosure (Clause 8). [Specification][tpc-c].

Systems performance evaluation and reporting:

- **[M]** Torsten Hoefler and Roberto Belli, "Scientific Benchmarking of Parallel
  Computing Systems: Twelve Ways to Tell the Masses When Reporting Performance
  Results", *SC '15*. DOI: 10.1145/2807591.2807644. [Paper][scientific]. Rules
  derived from a review of published HPC papers.
- **[M]** Erik van der Kouwe, Gernot Heiser, Dennis Andriesse, Herbert Bos and
  Cristiano Giuffrida, "Benchmarking Flaws Undermine Security Research", *IEEE
  Security & Privacy* 18(3), 48–57, 2020. DOI: 10.1109/MSEC.2020.2969862.
  [Paper][crimes-sp]. Peer-reviewed; 22 flaws coded A1–F4 (its own scheme, which
  differs from Heiser's numbering) and a study of 50 systems-security papers.
  Complete results are in the authors' IEEE EuroS&P 2019 SoK paper.
  Preprint: "Benchmarking Crimes: An Emerging Threat in Systems Security",
  arXiv:1801.02381, 2018 — [preprint][crimes-arxiv].
- **[C]** Gernot Heiser, "Systems Benchmarking Crimes" — [web page][heiser]. The
  origin of the crimes list, cited by its letter identifiers (A1 not evaluating
  potential degradation, A2 subsetting, B1 microbenchmarks, B2 throughput only,
  B3 downplaying overheads, E2 missing sub-benchmark results). Heiser's IDs are
  not van der Kouwe et al.'s: Heiser E2 corresponds to their F3. Expert
  commentary; every rule citing it also cites van der Kouwe et al.

Load models, latency and noise:

- **[E]** Bianca Schroeder, Adam Wierman and Mor Harchol-Balter, "Open Versus
  Closed: A Cautionary Tale", *NSDI '06*, pp. 239–252. [Paper][load]. Its measured
  outcomes concern the systems and load models studied.
- **[C]** Gil Tene, "How NOT to Measure Latency", talk, QCon London 2013 — the
  origin of the term *coordinated omission*. [Recording][tene-talk].
- **[C]** Gil Tene, *wrk2* — [README][wrk2], in particular its closing note on
  latency measurement and coordinated omission. Tool documentation; it
  illustrates intended-send-time accounting and does not mandate this tool.
- **[E]** Todd Mytkowicz, Amer Diwan, Matthias Hauswirth and Peter F. Sweeney,
  "Producing Wrong Data Without Doing Anything Obviously Wrong!", *ASPLOS XIV*,
  2009, pp. 265–276. DOI: 10.1145/1508244.1508275. [Publisher version][bias].
  Measurement bias, with causal analysis to detect it and setup randomization to
  avoid it.
- **[E]** Tomas Kalibera and Richard Jones, "Rigorous Benchmarking in Reasonable
  Time", *ISMM '13*. DOI: 10.1145/2464157.2464160. [Author's manuscript][repetition].
  Repetition levels (§3), summarising results and effect sizes (§4), warm-up and
  independent state (§6), multi-level repetition counts (§9), speedup intervals
  (§10). The linked manuscript corrects the ISMM version.
- **[E]** Philipp Leitner and Jürgen Cito, "Patterns in the Chaos — A Study of
  Performance Variation and Predictability in Public IaaS Clouds", *ACM
  Transactions on Internet Technology* 16(3), 2016. DOI: 10.1145/2885497.
  [Preprint][cloud]. Studied EC2, GCE, Azure and Softlayer in 2014–2015; findings
  are conditional on those providers, instance types and workloads. The first
  arXiv version covered only EC2 and GCE; cite the published version.

Reproducibility and the surrounding infrastructure:

- **[C]** ACM SIGMOD Availability and Reproducibility Initiative —
  [web page][sigmod-repro]. A community norm, not evidence.
- **[O]** Patrick K. Erdelt, "A Framework for Supporting Repetition and Evaluation
  in the Process of Cloud-Based DBMS Performance Benchmarking", *Performance
  Evaluation and Benchmarking* (TPCTC 2020), 2021, pp. 75–92.
  DOI: 10.1007/978-3-030-84924-5_6. [Record][erdelt2020].
- **[O]** Patrick K. Erdelt, "Orchestrating DBMS Benchmarking in the Cloud with
  Kubernetes", *Performance Evaluation and Benchmarking* (TPCTC 2021), 2022,
  pp. 81–97. DOI: 10.1007/978-3-030-94437-7_6. [Record][erdelt2021].
- **[O]** Patrick K. Erdelt, "A Cloud-Native Adoption of Classical DBMS
  Performance Benchmarks and Tools", *Performance Evaluation and Benchmarking*
  (TPCTC 2023), 2024, pp. 124–142. DOI: 10.1007/978-3-031-68031-1_9.
  [Record][erdelt2023]. Includes monitoring of benchmark drivers.

For the three Erdelt papers, the first year is the proceedings publication year;
the TPCTC year identifies the conference.

All locators are now confirmed. Gray is cited by the print 2nd edition's
section and page (§1.3, p. 5; §1.5, p. 8).

[nist-steps]: https://itl.nist.gov/div898/handbook/pri/section1/pri13.htm
[nist-objectives]: https://itl.nist.gov/div898/handbook/pri/section3/pri31.htm
[nist-variables]: https://itl.nist.gov/div898/handbook/pri/section3/pri32.htm
[nist-design]: https://itl.nist.gov/div898/handbook/pri/section3/pri33.htm
[nist-blocking]: https://itl.nist.gov/div898/handbook/pri/section3/pri332.htm
[nist-factorial]: https://itl.nist.gov/div898/handbook/pri/section3/pri333.htm
[nist-confounding]: https://itl.nist.gov/div898/handbook/pri/section3/pri3343.htm
[nist-prediction]: https://www.itl.nist.gov/div898/handbook/pri/section5/pri5998.htm
[nist-confirm]: https://www.itl.nist.gov/div898/handbook/pri/section5/pri599b.htm
[nist-testing]: https://www.itl.nist.gov/div898/handbook/eda/section3/eda35.htm
[preregistration]: https://doi.org/10.1073/pnas.1708274114
[ledgerwood]: https://doi.org/10.1073/pnas.1812592115
[jain-book]: https://www.cs.wustl.edu/~jain/books/perf_toc.htm
[gray-book]: https://jimgray.azurewebsites.net/benchmarkhandbook/toc.htm
[gray-intro]: https://jimgray.azurewebsites.net/benchmarkhandbook/chapter1.pdf
[dbtest]: https://hannes.muehleisen.org/publications/DBTEST2018-performance-testing.pdf
[huppler]: https://www.tpc.org/tpctc/tpctc2009/tpctc2009-03.pdf
[manolescu]: https://ir.cwi.nl/pub/13810/13810B.pdf
[tpc-c]: https://www.tpc.org/tpc_documents_current_versions/pdf/tpc-c_v5.11.0.pdf
[scientific]: https://htor.inf.ethz.ch/publications/img/hoefler-scientific-benchmarking.pdf
[crimes-sp]: https://download.vusec.net/papers/benchmarking_sp20.pdf
[crimes-arxiv]: https://arxiv.org/abs/1801.02381
[heiser]: https://gernot-heiser.org/benchmarking-crimes.html
[load]: https://www.usenix.org/legacy/event/nsdi06/tech/full_papers/schroeder/schroeder.pdf
[tene-talk]: https://www.infoq.com/presentations/latency-pitfalls/
[wrk2]: https://github.com/giltene/wrk2
[bias]: https://doi.org/10.1145/1508244.1508275
[repetition]: https://kar.kent.ac.uk/33611/
[cloud]: https://arxiv.org/abs/1411.2429
[sigmod-repro]: https://reproducibility.sigmod.org/
[erdelt2020]: https://link.springer.com/chapter/10.1007/978-3-030-84924-5_6
[erdelt2021]: https://link.springer.com/chapter/10.1007/978-3-030-94437-7_6
[erdelt2023]: https://link.springer.com/chapter/10.1007/978-3-031-68031-1_9
