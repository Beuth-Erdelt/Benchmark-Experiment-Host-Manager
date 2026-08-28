# Experiment Design Handbook

    handbook_version: "0.4.0"

Guidance on how to turn a research question into a sound benchmark experiment.
Read the `## Navigation` section first; it explains what this document is and
routes you to the chapters your question needs.

## Navigation

Three documents shape an experiment here, and they do different work. The
catalog contract defines which experiments are **legal**: the workloads, systems
and parameters that exist in this deployment, and the values they may take. The
result contract defines which claims are **supportable** once a run has
finished, and how the evidence has to be read before anything is claimed. This
handbook supplies the third thing, which is neither a question of legality nor
of claiming: the methodological knowledge that separates an experiment which
answers its question from one that merely runs.

It is guidance rather than a binding interface. The two contracts are checked;
this document is knowledge you are expected to apply with judgment. It gives no
values to copy, because a benchmark experiment is not a form to fill in, and a
principle applied without its reason is as likely to spoil a design as to
improve it. Every principle below is therefore stated together with the reason
it exists, and where that reason does not hold for the question in front of you,
the reason is what governs, not the sentence.

These principles apply to reading a measurement as much as to planning one. The
mechanics of that reading belong elsewhere: which files a result folder holds,
which checks decide whether a run is valid, and how a verdict must be structured
and its evidence cited are the result contract's subject, and this handbook does
not repeat them. But what a finished number may be said to show, at what scope,
against how much variation, and how far beyond the levels actually run a
conclusion may reach, are questions the chapters below answer — and they do not
stop applying once the run is over.

It names no workload, system or setting, because anything specific enough to
copy would be a rule to follow rather than a reason to think with.

Principles carry identifiers such as `M1.1` or `M4.3` so that a design decision,
a review comment or a rejection can point at one precisely.

Each chapter below is a Markdown section that can be requested on its own by its
exact heading, so you do not have to read the handbook whole. Read this
Navigation section first, then the chapters this question actually routes to.

When designing, two chapters bear on every experiment: **M1** because every
experiment makes a claim, and **M8** because every design has to fit a budget.
**M2** and **M5** apply to anything that compares. The rest depend on the shape
of the question.

| Chapter | Read it when the question involves |
| --- | --- |
| M1. The claim | any hypothesis or decision criterion — that is, every design |
| M2. Factors and controls | any comparison between alternatives, any attribution of an effect to a cause, or any sweep over levels |
| M3. The load model | throughput, capacity, concurrency, arrival rate, or responsiveness under load |
| M4. Data and state | dataset scale, caching, storage, loading, or warm-up |
| M5. Repetition and noise | any comparison, or any measurement that could come out differently on a second run |
| M6. The environment | placement, shared infrastructure, resource limits, or where the client runs |
| M7. Metrics | choosing what to measure, or combining several measurements into one number |
| M8. Feasibility | every design with a time or resource budget — that is, every design |

When a run has finished and a verdict is being written, a different set carries
the weight. **M2** governs which factor the numbers may be attributed to, and
how far a conclusion may reach beyond the levels that were actually run. **M3**
governs what a throughput or latency figure means given how load was offered,
and what has to be stated alongside it for the figure to be interpretable.
**M5** governs whether a difference between conditions is larger than the
variation between repetitions of the same one. **M7** governs which quantity is
quoted, at what scope, and whether combining several numbers into one preserves
the property being claimed.

A rejection from the validator may cite one of these identifiers as its reason.
When it does, the chapter it comes from is the one worth re-reading.

## M1. The claim

**Purpose.** Decide what the experiment asserts, and what would count as
evidence against it.

**Read this when.** Always. Every design states a claim, however implicitly.

**Questions to answer.** What outcome would make this hypothesis false? Is this
a comparison between alternatives or a measurement of one configuration? Is the
criterion for a positive result fixed before the data exists?

**Related chapters.** M2 for what a comparison has to hold equal, M7 for whether
the metric the claim names is one the run will actually produce.

**Guidelines**

- **M1.1** State the hypothesis so that some specific, measurable outcome would
  refute it. A hypothesis that no result can contradict — "acceptable
  throughput", "scales well", "performs adequately" — is a statement of intent,
  and every possible run confirms it.
- **M1.2** When the claim is comparative or causal, name the rival explanation
  the experiment is meant to rule out. The point of varying a factor is that the
  competing accounts predict different outcomes at its different levels; a design
  that can only produce evidence for one account discriminates between nothing.
  A purely descriptive measurement has no rival to name and does not need one.
- **M1.3** Fix the decision criterion before the run: which quantity is
  compared, against what margin, to count as support. A threshold chosen after
  the numbers are in is not a test, because it can always be placed where the
  data already is.
- **M1.4** Decide whether this is a *measurement* — what does this configuration
  do? — or a *comparison* — does one alternative differ from another? Say which,
  because the obligations differ: a measurement must disclose the envelope it was
  taken in, a comparison must additionally establish parity and repetition.
- **M1.5** Ask a question the instrument can answer. A question whose answer
  depends on a quantity the available workloads and metrics never produce cannot
  be rescued by a clever specification.

**Common pitfalls**

- *The unfalsifiable hypothesis*, which guarantees a successful run and a
  worthless one.
- *The moving criterion*, where the threshold for "better" is decided once the
  results are visible, turning noise into a finding.
- *Question–design mismatch*, where the hypothesis is about one thing and the
  varied factor is another, so the run cannot bear on the claim.
- *Benchmarketing*, where designs are adjusted until the desired ordering
  appears. Gray identified this as the reason formal benchmark specifications
  exist at all.

## M2. Factors and controls

**Purpose.** Decide what varies, what is held equal, and therefore what the
result can be attributed to.

**Read this when.** The design compares alternatives, attributes an effect to a
cause, or sweeps a parameter across levels.

**Questions to answer.** If the result comes out as expected, what else could
have produced it? Which levels have to be present for the conclusion I want to
be licensed by the data? Is anything varying between the arms that I have not
declared — a version, an image, a storage class, an allocation?

**Related chapters.** M5, because an effect is only visible against its noise;
M6, because the environment is a factor until it is controlled; M4, because
differences in data and cached state are the easiest confound to miss.

**Guidelines**

- **M2.1** Use a design whose effects are identifiable: one varied factor, a
  full factorial across the levels of several, or a deliberate fractional design
  whose aliasing — which effects it cannot separate from which — you can state.
  What is not defensible is an unplanned subset of combinations, where factors
  move together and the confounding is real but unknown.
- **M2.2** Everything not named as a factor must be identical across the things
  being compared: version, image, dataset, schema, physical design, client,
  placement, durability settings, and the resource envelope.
- **M2.3** Prevent opportunistic access to shared resources from becoming an
  uncontrolled factor. Wherever an alternative may consume more than it is
  guaranteed — spare cores, unclaimed memory, an unthrottled disk or link — what
  it actually receives depends on what else is running and on its own demand, so
  the allocation varies exactly where the comparison is being made. Either fix
  the share each alternative can obtain, or measure under contention on purpose
  and treat that contention as a declared factor.
- **M2.4** Give every alternative comparable tuning effort. A well-configured
  system measured against a default-configured one measures the configuration,
  and the incentive to under-tune the baseline is structural rather than
  malicious, which is why parity has to be a rule and not an intention.
- **M2.5** Ensure the alternatives perform equivalent work: the same semantics,
  data types, durability and isolation guarantees, and results verified to agree.
  A faster answer that is a different answer is not a performance result.
- **M2.6** The factors declared as isolated and the factors the specification
  actually varies must be the same set. An undeclared varying value is a
  confound; a declared but constant one is a false statement about the design.
- **M2.7** Include the levels you intend to conclude about. A conclusion holds
  at the levels that were run, so if the claim is meant to cover a scale, a
  concurrency or a configuration, that value has to appear in the design — or the
  claim has to be narrowed to what did appear.
- **M2.8** Cover the part of the evaluation space where the change under test
  might do harm, not only where it should help. An evaluation that can only
  produce good news is selective by construction, and running a subset of a
  standard workload needs a stated reason.

**Common pitfalls**

- *Apples versus oranges*: the alternatives differ in what they compute, not
  only in how fast — different types, approximate results, weaker durability, or
  a stripped-down component measured against a complete system.
- *The elastic envelope*, where guarantees sit below limits and each arm
  silently receives a different machine.
- *Unequal effort*: one side tuned and the other left at defaults, or a baseline
  old enough that the comparison flatters the newcomer.
- *Over-specific tuning*, chosen for this benchmark alone and generalizing
  nowhere.
- *The design that cannot lose*, covering only the conditions where the expected
  answer is the likely one.

## M3. The load model

**Purpose.** Decide how work arrives at the system, which decides which
questions the run can answer at all.

**Read this when.** The question involves throughput, capacity, concurrency,
arrival rate, latency, or behaviour under load.

**Questions to answer.** In the situation the question describes, does demand
arrive independently of completions, or do users wait for a response before
asking again? Is this measuring capacity, or response time at a stated demand?
Has one of my own client settings already fixed the quantity I mean to report?

**Related chapters.** M7 for which summary a latency claim needs; M5, because
tail behaviour needs many more observations than a mean does.

In a **closed** load model a fixed number of clients each wait for a response
before sending again, so offered load is a function of the system's own speed.
In an **open** model, requests arrive at a rate that does not depend on whether
earlier ones completed. Schroeder, Wierman and Harchol-Balter showed the two
behave so differently that a system evaluated under the wrong one can yield the
opposite conclusion: a closed generator holds response time nearly flat as load
rises and largely hides the effect of scheduling policy, both of which an open
generator exposes.

**Guidelines**

- **M3.1** Decide first whether the question is about *capacity* — how much work
  per unit time the system absorbs — or about *responsiveness* — how long a
  request takes at a given demand. The load model follows from that, not from
  what is convenient to configure.
- **M3.2** Never report a quantity that one of your own settings has fixed. If
  the client is capped at a rate the system could exceed, the measured
  throughput is the cap: a property of the harness, not of the system.
- **M3.3** A maximum-sustainable-throughput claim requires that saturation be
  demonstrated rather than assumed. Load is raised until throughput stops rising
  and latency turns upward; if it was never raised that far, the figure is a
  lower bound and has to be reported as one.
- **M3.4** Match the load model to the population the question describes. A
  closed model represents a fixed population that waits, and latency measured
  under it is correct *for that population*. It misleads when it is used to
  describe demand that arrives independently: as the system slows, a closed
  generator — or an open one whose schedule has slipped — stops issuing
  requests, so the requests that would have met the stall are never sent and
  never counted, and the omission is coordinated with the very stall it should
  be measuring. Where the question is about independent arrivals, measure each
  request from its intended arrival time, or say that the tail understates.
- **M3.5** Report the concurrency and think time behind every latency figure. In
  a closed system latency is largely a function of how many requests are in
  flight, so the number means little without them.
- **M3.6** Confirm the load generator was not itself the bottleneck. A saturated
  client produces a beautifully flat curve that describes the client.

**Common pitfalls**

- *Throughput from a throttled run*, the most common way to measure your own
  configuration file.
- *An open-arrival claim from closed-loop measurements*, where the tail is wrong
  by orders of magnitude rather than percentages.
- *Latencies compared at different achieved throughputs*, where the two sides
  were doing different amounts of work.
- *Concurrency used as a proxy for load*, which moves the offered demand and the
  queueing regime together and so violates M2.1.

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

- **M4.1** Size the dataset against the memory envelope deliberately and state
  which regime is being measured: fully cached, partly cached, or larger than
  memory. A design that lands in a regime by accident answers a question nobody
  asked.
- **M4.2** Match the data volume to the question. A dataset that fits entirely
  in cache cannot test a claim about storage behaviour, and it systematically
  favours whichever side's advantage lies in avoiding input and output.
- **M4.3** Declare the cache state each measurement is taken in — cold with
  caches flushed, warm after prior activity, or hot and steady. All three are
  legitimate; mixing them within one comparison is not, and measuring one side's
  first run against another's tenth does exactly that.
- **M4.4** Separate the cost of preparing the system from the cost of measuring
  it. Loading, index construction, statistics collection and format conversion
  are real costs: count them or exclude them explicitly, and treat every
  alternative the same way. Preparation that happens implicitly for one and
  explicitly for another is a hidden subsidy.
- **M4.5** Measure inside a steady interval. Ramp-up and cache filling belong
  either outside the measured window or inside it by explicit decision, applied
  identically to every alternative.
- **M4.6** Verify the results are correct before believing they are fast. A side
  that errors, returns fewer rows, or silently skips work is not competing.

**Common pitfalls**

- *The toy dataset with the production claim*: a scale chosen for convenience
  and a conclusion stated without one.
- *The selective data range*, stopping just before the point where the answer
  stops being flattering.
- *The unpriced preparation*, such as an index built during a phase nobody
  timed.
- *Ramp-up folded into the measurement*, so the result mostly reports how long
  the caches took to fill.

## M5. Repetition and noise

**Purpose.** Decide how many observations are needed before a difference can be
told apart from ordinary variation.

**Read this when.** Anything is being compared, or a measurement could come out
differently on a second run — which, on shared infrastructure, is all of them.

**Questions to answer.** How large is the difference I expect, next to how much
this measurement moves between identical runs? At which level does the variation
I fear live: inside a run, between runs, or between deployments? If the
environment drifted during the experiment, could I tell that apart from the
effect?

**Related chapters.** M6 for where the variation comes from; M7 for how to
summarize what repetition produces.

**Guidelines**

- **M5.1** A single run yields no estimate of its own uncertainty. Any design
  that compares needs enough repetitions that the spread can be estimated and
  the observed difference judged against it; with one run each, an effect and a
  fluctuation are indistinguishable by construction.
- **M5.2** Report variability alongside any central value. A mean or median
  without a spread is uninterpretable, and this is the single most common defect
  found in surveys of published systems work.
- **M5.3** State whether the measurements are deterministic. For
  non-deterministic data give confidence intervals, and compare using
  non-overlapping intervals or a test rather than by eye.
- **M5.4** Do not assume the measurements are normally distributed. Performance
  distributions are usually skewed with a long tail, so quantile-based summaries
  describe them more honestly than a mean and a standard deviation.
- **M5.5** Repeat at the level where the variation you fear actually lives.
  Consecutive iterations inside one process share caches and warm state and are
  not independent samples of a deployment; if placement is the suspected source,
  the deployment is what has to be repeated.
- **M5.6** On shared infrastructure, expect variation between allocations to
  exceed variation within one. Multi-tenancy dominates performance variation in
  public cloud studies, and the placement an arm happens to draw can persist for
  its whole lifetime.
- **M5.7** Interleave or randomize the order in which alternatives are measured.
  If all of one runs before all of the other, drift in the environment over time
  is indistinguishable from the treatment.

**Common pitfalls**

- *The single-run comparison*: two numbers, one from each side, and a
  conclusion.
- *Blocked execution*, all of one and then all of the other, with the
  neighbouring load changing in between.
- *Discarding inconvenient runs* without a rule fixed in advance, which is
  cherry-picking whatever the intention was.
- *Measurement bias mistaken for an effect*. Mytkowicz and colleagues showed
  that changes as innocuous as environment size can shift results enough to
  reverse a conclusion, so an unexplained difference deserves suspicion before
  it deserves publication.

## M6. The environment

**Purpose.** Decide where everything runs, and what will be recorded about it.

**Read this when.** The design touches placement, shared infrastructure,
resource limits, or the location of the client.

**Questions to answer.** Which parts of this machine are shared with something I
do not control? If I later want to attribute the effect to a particular
resource, will anything have recorded that resource? Could someone else rebuild
this setup from what the specification records?

**Related chapters.** M2, because an uncontrolled environment is an undeclared
factor; M5, because what cannot be controlled has to be repeated instead.

**Guidelines**

- **M6.1** Keep the load generator off the machine under test. Where
  co-location is unavoidable, say so, and show the client was not competing for
  the resource the experiment is about.
- **M6.2** Control placement. On a heterogeneous cluster the node is a factor,
  and an unpinned alternative draws a different machine than the one it is
  measured against.
- **M6.3** Disclose the platform completely: hardware, kernel, versions, images,
  configuration values, storage class and network path. This is not bookkeeping.
  It is the condition under which anyone — including a later run of this same
  agent — can reproduce or contest the result.
- **M6.4** Instrument the resource you may later want to blame. Utilization data
  is what lets an effect be attributed to a cause rather than merely observed,
  and an explanation naming a mechanism that nothing measured is a story, not a
  finding.
- **M6.5** Where isolation from other tenants cannot be guaranteed, treat that
  as a declared source of variation under M5.6 rather than an inconvenience to
  leave unmentioned.

**Common pitfalls**

- *The invisible client*, generating load on the machine under test, unreported.
- *The missing platform specification*, which makes every number unverifiable.
- *Heterogeneous alternatives*: different nodes or storage classes, same table.
- *Monitoring switched off*, after which a failure is indistinguishable from
  slowness.

## M7. Metrics

**Purpose.** Decide what quantity is recorded, and how many numbers become one.

**Read this when.** Choosing what to measure, or combining measurements into a
single reported figure.

**Questions to answer.** What exactly is the unit of work behind this rate? Does
the question ask about the typical case or about the tail? Will combining these
numbers preserve the property being claimed, or destroy it?

**Related chapters.** M3, because the load model decides which latency figures
mean anything; M5, because a summary without a spread is not a result.

**Guidelines**

- **M7.1** Define the metric before reporting it: throughput of which unit of
  work, latency between which two points, cost including which phases.
- **M7.2** Prefer aggregating the underlying totals: an overall rate is total
  work divided by total time, and an overall cost is the sum of the costs. Where
  only the per-observation figures survive, the mean has to match how the
  observations were taken — the harmonic mean recovers the overall rate when each
  observation covers the same amount of work, the arithmetic mean when each
  covers the same span of time — so state which. Avoid summarizing ratios at all,
  and fall back to the geometric mean only when the underlying values are
  genuinely unavailable.
- **M7.3** Never report a ratio without the absolute values behind it. A speedup
  without a baseline time cannot be sanity-checked and hides whether the
  quantities involved matter at all.
- **M7.4** For tail-sensitive questions report named percentiles rather than a
  central value, because a mean conceals precisely the behaviour a
  responsiveness claim is about.
- **M7.5** Report per-component results and not only an aggregate. An aggregate
  that improves while one component regresses badly is an important outcome, and
  only the breakdown shows it.
- **M7.6** Do not promote a microbenchmark to a system claim. A probe of one
  component measures that component under conditions the whole system never
  reproduces.
- **M7.7** Compute overheads against the baseline, and keep percentages and
  percentage points distinct. A throughput reduction is not the same quantity as
  an overhead, and treating them as interchangeable understates the cost
  whenever the system was not already saturated.

**Common pitfalls**

- *Averaged ratios*, including the arithmetic mean of normalized scores, which
  has no meaning.
- *Relative numbers only*, leaving no way to sanity-check the result.
- *The aggregate that hides a regression.*
- *The undefined metric*, most often a throughput figure whose unit of work is
  never stated.

## M8. Feasibility

**Purpose.** Decide whether this design can actually be run, and where to spend
the budget it has.

**Read this when.** Always. Every design competes with a time and resource
budget.

**Questions to answer.** How many phases does this expand to, and how long will
they take? If the budget forces a cut, which levels can go without costing the
ability to tell an effect from noise? Is time being spent on preparation that
buys no evidence?

**Related chapters.** M5, because repetitions are the last thing that should be
cut; M2, because levels are usually the first.

**Guidelines**

- **M8.1** Estimate the cost of a design before committing to it, in phases,
  wall-clock time and cluster occupancy.
- **M8.2** Factorial designs multiply. When one is too large, remove levels that
  cannot discriminate between the competing explanations before removing
  repetitions, because repetitions are what make any comparison readable at all.
- **M8.3** Spend the budget on the measured phase. Time spent artificially
  slowing preparation buys no evidence and is subtracted directly from what
  could have been measured.
- **M8.4** Prefer the smallest design that could refute the hypothesis. Where
  follow-up experiments are limited or unavailable, a decisive narrow experiment
  is worth more than a broad sweep that ends inconclusively.
- **M8.5** Bound every phase with a deadline, so one hung component costs a run
  instead of the entire budget.

**Common pitfalls**

- *The sweep that never finishes.*
- *Repetitions traded for levels*, producing a large design that cannot support
  a single claim.
- *Budget spent on preparation* rather than on measurement.
- *Exploration where only one attempt was available.*

## Sources

This handbook distills existing literature; the method is not original to it.

Database benchmarking and benchmark construction:

- Jim Gray (ed.), *The Benchmark Handbook for Database and Transaction
  Processing Systems*, 1993 — the four criteria of a useful benchmark
  (relevance, portability, scalability, simplicity) and the diagnosis of
  "benchmarketing".
- Karl Huppler, *The Art of Building a Good Benchmark*, TPCTC 2009 —
  <https://www.tpc.org/tpctc/tpctc2009/tpctc2009-03.pdf>
- Ioana Manolescu and Stefan Manegold, *Performance Evaluation in Database
  Research: Principles and Experience*, tutorial, ICDE 2008, Cancún —
  <https://ir.cwi.nl/pub/13810/13810B.pdf>
- Mark Raasveldt, Pedro Holanda, Tim Gubner and Hannes Mühleisen, *Fair
  Benchmarking Considered Difficult: Common Pitfalls in Database Performance
  Testing*, DBTest 2018, with its fair-benchmark checklist —
  <https://hannes.muehleisen.org/publications/DBTEST2018-performance-testing.pdf>
- TPC benchmark specifications, for steady state, the measurement interval and
  the full-disclosure requirement — <https://www.tpc.org/>

Systems performance evaluation, experimental design and reporting:

- Raj Jain, *The Art of Computer Systems Performance Analysis*, 1991 — the
  distinction between inadvertent mistakes and deliberate games, and the
  treatment of factorial and fractional factorial designs behind M2.1.
- Torsten Hoefler and Roberto Belli, *Scientific Benchmarking of Parallel
  Computing Systems: Twelve Ways to Tell the Masses When Reporting Performance
  Results*, SC 2015 — the rules on means, ratios, confidence intervals,
  normality and factor documentation —
  <https://htor.inf.ethz.ch/publications/img/hoefler-scientific-benchmarking.pdf>
- Gernot Heiser, *Systems Benchmarking Crimes* —
  <https://gernot-heiser.org/benchmarking-crimes.html>
- Erik van der Kouwe et al., *Benchmarking Crimes: An Emerging Threat in Systems
  Security*, 2018 — <https://arxiv.org/abs/1801.02381>

Load models, latency and noise:

- Bianca Schroeder, Adam Wierman and Mor Harchol-Balter, *Open Versus Closed: A
  Cautionary Tale*, NSDI 2006 —
  <https://www.usenix.org/legacy/event/nsdi06/tech/full_papers/schroeder/schroeder.pdf>
- Gil Tene, *How NOT to Measure Latency*, and the HdrHistogram project — the
  original statement of coordinated omission behind M3.4.
- Todd Mytkowicz, Amer Diwan, Matthias Hauswirth and Peter F. Sweeney,
  *Producing Wrong Data Without Doing Anything Obviously Wrong!*, ASPLOS 2009 —
  measurement bias.
- Tomas Kalibera and Richard Jones, *Rigorous Benchmarking in Reasonable Time*,
  ISMM 2013 — how many repetitions, at which level, and how to detect the end of
  warm-up — <https://kar.kent.ac.uk/33611/45/p63-kaliber.pdf>
- Philipp Leitner and Jürgen Cito, *Patterns in the Chaos — A Study of
  Performance Variation and Predictability in Public IaaS Clouds*, ACM TOIT
  2016 — <https://arxiv.org/abs/1411.2429>

Reproducibility and the surrounding infrastructure:

- ACM SIGMOD Availability and Reproducibility Initiative —
  <https://reproducibility.sigmod.org/>
- Patrick K. Erdelt, *A Framework for Supporting Repetition and Evaluation in
  the Process of Cloud-Based DBMS Performance Benchmarking*, TPCTC 2020;
  *Orchestrating DBMS Benchmarking in the Cloud with Kubernetes*, TPCTC 2021;
  *A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools*,
  TPCTC 2023 — the repetition, monitoring and evaluation model this
  infrastructure implements.
