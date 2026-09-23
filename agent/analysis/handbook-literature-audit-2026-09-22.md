# Literature audit of the Experiment Design Handbook

Audit date: 2026-09-22. Reviewed handbook version: 0.5.0.

Reviewed file: `agent/experiment_design_handbook.md`, including its existing
working-tree edits. Its SHA-256 content fingerprint was
`6ae5a04aca1826a45468bec2e7627c5d3d9282c4f06d466e6bfd964ca9a660cb`.
This report records a review; it does not revise the handbook or agent behaviour.

## Verdict and method

**The handbook cannot currently be described as having every claim supported
by its stated literature.** Its central advice has substantial support, but it
mixes source recommendations, the author's own deductions, local operating
policy, and assertions that are too strong or incorrect as written.

I found no evidence that a named work was fabricated. That is different from
verifying every attribution: some references lack a specific edition or passage,
some links identify different forms of the work, and some full texts were not
available. In particular, the handbook's bibliography does not provide a
claim-to-source mapping. The mappings below are the closest support I could
identify, not proof of the author's actual derivation process.

The review covers all 50 numbered guidelines, the substantive assertions in
the introductory and cross-reference prose, all common-pitfall lists, and every
bibliography entry. Repository navigation and agent policy are distinguished
from claims about research findings. Source locations use section numbers,
named rules, or slide numbers so they remain usable across PDF copies.

Four assessments are used:

- **Supported** means an inspected source supports the central recommendation
  at the scope in which the handbook uses it. This is not a guarantee that the
  source is infallible or that the recommendation applies without judgment.
- **Qualified** means relevant support exists, but wording, scope, or an
  omitted condition needs correction before the entire guideline is defensible.
- **Derived** means the recommendation is a plausible deduction or local
  policy, but I did not locate the stated rule in the inspected sources.
- **Unsupported** means the guideline includes a substantive assertion that
  is not established by the cited material and has a concrete counterexample.

The counterexamples and proposed corrections below are the auditor's reasoning.
They are not additional findings attributed to the papers. Failure to locate a
passage does not establish that no supporting literature exists.

Across the 50 numbered guidelines, the assessments are **18 supported,
20 requiring qualification, 10 derived or local-policy recommendations, and
2 containing unsupported substantive assertions**. These counts classify whole
guidelines, not individual sentences. Additional problems occur in the
unnumbered prose and are recorded separately.

## Findings that matter most

### A resource need not be fully occupied to have an effect

M2.9 correctly asks whether another setting prevents a resource increase from
helping. Its stronger claim that use below the smallest allocation means the
factor was never tested is not justified. Average use can hide short bursts or
one fully occupied processor core. Allocating more processors can also alter
placement or parallel execution even when average use stays low.

The measured result can still support a narrow statement: increasing the
allocation did not improve the measured outcome under this workload and these
settings. It cannot establish that the resource is ineffective in general.
Changing both the allocation and a parallelism limit measures their joint
effect; declaring that coupling does not separate their individual effects.
The relevant background is experimental control and interactions in
[Jain's design material][jain-design] and [fractional-design material][jain-fractional].
The handbook's particular utilization rule is an additional inference.

### Several categorical prohibitions exclude valid experiments

The M3 concurrency pitfall says varying concurrency violates M2.1. This does
not follow: concurrency can be the one deliberately varied input, with changes
in throughput and waiting as its consequences. The error is treating a fixed
client population as equivalent to an independently imposed arrival rate.
[Schroeder et al., §§2 and 5–7][schroeder], distinguish those models; they do
not prohibit concurrency experiments.

M4.2 says a cached dataset cannot test storage behaviour. A counterexample is a
small database whose commits must wait for durable writes. A cached read test
may fail to exercise storage reads; that is the narrower defensible statement.
TPC-C explicitly includes durability and measurement requirements for persistent
writes in [revision 5.11, §§3.5 and 5.5.2.2][tpc-c]. The additional assertion
about which alternative is systematically favoured has no general justification.

M3.2 prohibits reporting a rate fixed by the client. Such a measurement can be
useful when reporting achieved throughput and latency at a specified demand.
It simply does not establish maximum system capacity. Gil Tene's own
[wrk2 documentation][wrk2] illustrates a legitimate constant-rate experiment.

### Monitoring does not by itself establish causation

M6.4 overstates what utilization data proves. A utilization increase and a
slowdown may share another cause. Monitoring can test whether a proposed
mechanism is plausible, but causal attribution also needs a discriminating
intervention or another justified identification method. The monitoring advice
in [Manolescu–Manegold, slides 45–53][tutorial] does not supply that missing step.
[Mytkowicz et al., §§1 and 7][mytkowicz], provide a relevant warning about
measurement bias and methods for investigating it.

### The cloud study's scope was broadened

M5.6 turns results for particular public cloud providers and workloads into a
general expectation for shared infrastructure. [Leitner–Cito, abstract,
§§5.2.1–5.2.2 and Table VI][cloud], explicitly distinguish providers. Their
comparison of variation within and between instances also has an exception.
The appropriate rule is to measure both kinds of variation and allocate
repetitions accordingly, not assume their ordering in a university cluster.

### Statistical advice needs its original qualifications

M5.3 is traceable to [Hoefler–Belli, Rules 5 and 7][hoefler]; it is not an
invented recommendation. However, non-overlap of separate confidence intervals
is not a complete decision procedure. Overlap does not establish equality.
[Kalibera–Jones, §4 and §10][kalibera], discuss this limitation and recommend
intervals for the effect itself, such as the ratio of mean execution times.
An effect interval describes uncertainty about the size of a difference, not
the spread of individual requests.

M5.4 should retain its warning against assuming a normal distribution, the
familiar symmetric bell-shaped distribution. It should not imply that a
percentile is always preferable to a mean. They answer different questions.
The same dataset may need a mean to estimate expected cost and percentiles to
describe slow requests. This distinction matters even when the observations
are skewed.

### The sources disagree about combining ratios

M7.2 follows [Hoefler–Belli, Rule 4][hoefler], in treating a geometric mean as a
fallback. [Heiser, incorrect-use item 5][heiser], and [van der Kouwe et al.,
§II.B, crime B5][crimes], recommend it for normalized benchmark scores. The
handbook should identify which recommendation it adopts and why.

An arithmetic mean of ratios is not literally meaningless: it estimates the
average ratio under a specified weighting. It may nevertheless answer the
wrong question, depend on the chosen baseline, and differ from total-work
speedup. Likewise, a geometric mean describes a multiplicative summary; it
does not automatically measure overall elapsed-time improvement. These are
different quantities, so the blanket M7 pitfall should be narrowed.

### Practical defaults are presented as literature requirements

The exact deadline rule in M8.5 and the budget priorities in M8.2–M8.4 were
not established by the inspected sources. They can be useful local policy.
However, preparation can be the scientific subject, and spending time on
initialization or independent deployments can be necessary for valid evidence.
The source-backed principle is to plan an informative experiment within its
budget, not to maximize time inside an arbitrarily labelled measured phase.

## Audit of all numbered guidelines

Each row assesses the complete numbered guideline, including its explanation.
When only the central recommendation is supported, the qualification is stated.

### M1. The claim

| Guideline | Assessment | Evidence and required action |
| --- | --- | --- |
| M1.1 | Derived | [Jain, slides 2-3 and 2-9][jain-mistakes], supports clear, unbiased goals. The exact falsifiability prescription needs a direct methodological citation or a local-policy label. An untestable statement is not confirmed by every result; it has no specified test. Replace that explanation. |
| M1.2 | Derived | Ruling out competing mechanisms is sensible for causal questions. Requiring a named rival explanation for every comparative measurement is stronger than the inspected sources. Measuring a difference need not identify its mechanism. Limit the obligation accordingly. |
| M1.3 | Derived | None of the inspected passages establishes this exact advance-decision rule. Add a direct source for confirmatory analysis or label it policy. A criterion selected after inspection can support explicitly exploratory work, but should not be represented as an independent confirmation. |
| M1.4 | Qualified | [Jain's systematic approach][jain-mistakes] motivates declaring the goal; [Kalibera–Jones, §3][kalibera], addresses measurement uncertainty. Descriptive measurements can also need independent repetitions. The distinction must not exempt them from uncertainty assessment. |
| M1.5 | Derived | This is a reasonable application of matching goals, metrics, and evaluation methods in [Jain, slides 2-3, 2-6 and 2-9][jain-mistakes]. Identify it as an application to this agent's available instruments. |

### M2. Factors and controls

| Guideline | Assessment | Evidence and required action |
| --- | --- | --- |
| M2.1 | Supported | [Jain, slides 16-9–16-11][jain-design] and [19-11–19-20][jain-fractional], support explicit designs and known confounding, meaning effects that the design cannot separate. A single-factor experiment estimates that effect at its fixed background settings; it does not resolve interactions with unvaried settings. |
| M2.2 | Qualified | [Hoefler–Belli, §4.1.1][hoefler], permits randomization when control is infeasible. Literal identity of all other conditions is neither achievable nor required. Describe relevant controls and remaining variation. Different systems may require different images, versions, and physical designs. |
| M2.3 | Qualified | Shared-resource interference is grounded in [Leitner–Cito, §§2 and 5.2][cloud]. The exact choice between fixed shares and deliberate contention is too restrictive. Replication with randomized assignment is another possible design. Resource guarantees and limits are also an implementation-specific application, not a general theorem of fair comparison. |
| M2.4 | Supported | [Raasveldt et al., §3.2][dbtest], directly supports fair tuning effort. Interpret the explanation as warning that tuning differences can account for a result, not proving that they always explain the whole difference. State explicitly if default configurations are themselves the comparison of interest. |
| M2.5 | Supported | [Raasveldt et al., §§3.3 and 3.8][dbtest], supports equivalent functionality and verified answers. If semantics or guarantees are intentionally different, report that tradeoff rather than calling the experiment an equivalent-work speed comparison. |
| M2.6 | Qualified | [Hoefler–Belli, Rule 9][hoefler], supports documenting factors. Not every undeclared fluctuation is a confound: random fluctuations can contribute uncertainty without systematically favouring an alternative. Exact correspondence between declared and expanded factors is a useful agent validation policy. |
| M2.7 | Qualified | [Huppler's slide 9][huppler-slides] limits claims to the benchmark's scope. Requiring every concluded-about value to be directly tested excludes justified interpolation and predictive models. Distinguish observations at tested settings from model-based predictions at other settings. |
| M2.8 | Supported | [Van der Kouwe et al., §II.A, A1–A2][crimes], supports evaluating potential degradation and explaining subsets. [Raasveldt et al., Appendix A][dbtest], is also relevant. |
| M2.9 | Qualified | The reachability check is a useful deduction from factor control, but the utilization test and obligatory follow-up are not established source rules. Retain the narrow workload-specific result, check bursts and individual resources, and distinguish joint changes from isolated effects. See the first finding above. |

### M3. The load model

| Guideline | Assessment | Evidence and required action |
| --- | --- | --- |
| M3.1 | Qualified | [Schroeder et al., §7][schroeder], supports choosing a representative arrival model. The choice cannot be inferred from capacity versus responsiveness alone: either question may concern a waiting population or independent arrivals. |
| M3.2 | Qualified | The capacity warning is sensible, but the prohibition on reporting achieved throughput is false. [Tene's wrk2 documentation][wrk2] provides a concrete counterexample. Report the client limit and distinguish measured throughput from capacity. |
| M3.3 | Qualified | [TPC-C §§5.2.5 and 5.5][tpc-c] illustrates that sustainability has response and steady-state conditions. A throughput plateau alone does not establish sustainability or identify the bottleneck. Declare acceptable latency, failures, backlog growth, and duration; report only successful qualifying rates as demonstrated lower bounds. |
| M3.4 | Supported | [Schroeder et al., §§2 and 7][schroeder], supports matching population models. [Tene's intended-arrival measurement description][wrk2] supports the timing remedy. That remedy is for delayed scheduling of modelled requests; it does not magically recover observations from requests dropped without accounting. |
| M3.5 | Qualified | [Schroeder et al., §5 and Figure 7][schroeder], supports the role of population and think time. For open arrivals, disclose arrival rate and distribution, queueing and admission policy, and observed concurrency. Think time is not a universal explanatory parameter for every latency figure. |
| M3.6 | Derived | The diagnostic follows from checking measurement bottlenecks. [Erdelt's TPCTC 2023 abstract][erdelt2023] specifically includes monitoring drivers. The exact categorical rule is an application; client saturation also need not produce a flat curve. |

### M4. Data and state

| Guideline | Assessment | Evidence and required action |
| --- | --- | --- |
| M4.1 | Derived | [Raasveldt et al., §§3.5–3.6][dbtest], supports distinguishing cache states. Dataset volume relative to memory is only a clue: accessed data, indexes, compression, and query workspace determine the effective working set. An accidental choice narrows the claim; it does not make the measurement worthless. |
| M4.2 | Unsupported | The cached-data prohibition has the durable-write counterexample described above. No inspected source establishes the claimed universal direction of bias. Replace it with a requirement to demonstrate that the relevant storage path is exercised. |
| M4.3 | Supported | [Raasveldt et al., §§3.5–3.6 and Appendix A][dbtest], directly addresses cold, warm, and hot runs. Define an actual preparation protocol; hot caches alone do not prove that every relevant aspect of performance is steady. |
| M4.4 | Supported | [Raasveldt et al., §3.7][dbtest], directly addresses preprocessing and automatic indexing. Make clear that comparable accounting does not require identical physical preparation across different architectures. |
| M4.5 | Supported | [TPC-C §§5.5.1–5.5.2][tpc-c] supports steady-state measurement for its stated purpose. The handbook already allows deliberate transient measurement. Preserve that exception and make the measured regime explicit. |
| M4.6 | Supported | [Raasveldt et al., §3.8][dbtest], directly supports correctness checks. Error rates may themselves be a legitimate result, but failed work cannot silently count as successful completed work. |

### M5. Repetition and noise

| Guideline | Assessment | Evidence and required action |
| --- | --- | --- |
| M5.1 | Qualified | [Kalibera–Jones, §3][kalibera], supports repeating at relevant sources of randomness. One aggregate observation cannot estimate between-run variation. One long run can contain observations of within-run uncertainty, and deterministic quantities are an exception. Define the independent experimental unit instead of equating every run with one indivisible sample. |
| M5.2 | Qualified | [Van der Kouwe et al., §IV.A][crimes], reports missing significance information in 80% of applicable papers in its sample. That supports a scoped survey claim, not an unqualified ranking across all systems literature. Distinguish spread of observations from uncertainty in a mean. |
| M5.3 | Qualified | [Hoefler–Belli, Rules 5 and 7, §3.2][hoefler], is a direct source. Restore the warning that overlap is inconclusive; specify interval method and confidence level. Prefer an interval for the actual comparison where appropriate, as discussed by [Kalibera–Jones, §§4 and 10][kalibera]. |
| M5.4 | Qualified | [Hoefler–Belli, Rule 6 and §§3.1.3 and 3.2][hoefler], supports distribution checking. The explanation should not rank quantiles as inherently more honest. Select summaries for the quantity the question asks about, and justify their uncertainty estimates. |
| M5.5 | Supported | [Kalibera–Jones, §3 and §§6–10][kalibera], directly supports choosing the repetition level. The deployment example is a reasonable application to this infrastructure. |
| M5.6 | Qualified | [Leitner–Cito, §§5.2.1–5.2.2][cloud], supports investigating both within-allocation and between-allocation variation. Its provider-specific findings do not establish the stated universal expectation or dominance claim. |
| M5.7 | Supported | [Hoefler–Belli, §4.1.1][hoefler], directly supports randomized execution order. Fixed alternation alone can still align with periodic interference. Randomize within appropriate time or allocation groups and account for dependencies. |

### M6. The environment

| Guideline | Assessment | Evidence and required action |
| --- | --- | --- |
| M6.1 | Derived | Avoiding client interference is reasonable engineering policy. [Erdelt's TPCTC 2023 abstract][erdelt2023] supports observing driver resources, but I did not verify a universal separate-machine requirement. Preserve the permitted co-location case and explain how competition is assessed. |
| M6.2 | Qualified | [Hoefler–Belli, §4.1.1][hoefler], supports accounting for placement. An unpinned alternative does not necessarily receive a different machine. Fixed placement, pairing, or randomized replicated placement can support different scopes of inference. |
| M6.3 | Supported | [Raasveldt et al., §3.1 and Appendix A][dbtest], supports setup disclosure. [SIGMOD's initiative][sigmod] also concerns sharing research artifacts. Disclosure makes evaluation inspectable; it cannot guarantee access to an identical platform. |
| M6.4 | Unsupported | [Manolescu–Manegold, slides 45–53][tutorial], supports investigation with monitoring. Utilization alone is not sufficient evidence of causation. Replace the causal guarantee with a requirement to test mechanisms and distinguish observations from explanations. |
| M6.5 | Supported | [Leitner–Cito, §§2 and 5.2][cloud], supports treating tenant interference as a possible source of variation. Keep this recommendation, but correct the overgeneralized M5.6 to which it refers. |

### M7. Metrics

| Guideline | Assessment | Evidence and required action |
| --- | --- | --- |
| M7.1 | Supported | [Jain, slides 2-9 and 2-11][jain-mistakes], and [Manolescu–Manegold, slide 22][tutorial], support defining the measured quantity. |
| M7.2 | Qualified | [Hoefler–Belli, §3.1.1 and Rules 3–4][hoefler], supports its main approach, but the geometric-mean policy differs from [Heiser, item 5][heiser], and [van der Kouwe et al., B5][crimes]. State the target quantity and weighting. Total work divided by total time applies to a defined common observation window or sequential work; summing durations of overlapping jobs does not give wall-clock throughput. |
| M7.3 | Supported | [Hoefler–Belli, Rule 1][hoefler], directly supports reporting the absolute baseline. |
| M7.4 | Supported | [Hoefler–Belli, Rule 8][hoefler], supports percentiles for questions about slow requests. Retain the opening restriction to tail-sensitive questions; not every responsiveness question is exclusively about a tail. |
| M7.5 | Supported | [Heiser, omission-of-subbenchmarks item][heiser], supports component results. The recommendation is appropriate for detecting regressions hidden by an aggregate. |
| M7.6 | Qualified | [Manolescu–Manegold, slides 10–12][tutorial], and [Heiser, microbenchmarks item][heiser], support limited generalization. The claim that the whole system *never* reproduces the component conditions is too strong. Require evidence connecting component behaviour to whole-system performance. |
| M7.7 | Qualified | [Heiser, throughput/overhead and percentage items][heiser], supports careful denominators and accounting. Replace “whenever” with a conditional statement. Throughput loss does not uniquely determine processing-cost overhead; CPU load and workload semantics matter. Even under full utilization, a 20% throughput drop corresponds to 25% greater time per unit of work, not 20%. |

### M8. Feasibility

| Guideline | Assessment | Evidence and required action |
| --- | --- | --- |
| M8.1 | Supported | [Huppler, slide 16][huppler-slides], and [Jain, slide 2-7][jain-mistakes], support economical, efficient evaluation. Counting phases and cluster occupancy is an appropriate local implementation of that principle. |
| M8.2 | Qualified | [Jain, slides 16-7 and 16-10–16-11][jain-design], supports the multiplication of combinations and reduced designs. It does not establish a universal order for cutting levels before repetitions. Preserve the combinations needed to identify the effect and enough repetition to estimate relevant uncertainty. |
| M8.3 | Derived | Avoidable delay wastes budget, but a general preference for the measured phase is not a source-established allocation rule. Preparation, stable initialization, and fresh deployments can buy essential evidence. If preparation is the research subject, it must be measured. |
| M8.4 | Derived | [Jain, slide 16-13][jain-design], supports informative economical design. “Smallest” alone does not ensure useful precision or sufficient opportunity to detect a real effect. Define what decisive means before minimizing the design. The one-attempt preference is local policy. |
| M8.5 | Derived | No inspected source establishes a deadline for every phase. Keep it as an operational safeguard. Also define how unfinished runs are reported; silently dropping slower timed-out runs would bias the result. |

## Unnumbered prose and common pitfalls

These passages also make claims. Repetition of a guideline in a pitfall does
not supply additional evidence for it.

| Passage | Assessment and action |
| --- | --- |
| Navigation, purposes, and “read this when” routing | These are local document and workflow choices, not literature findings. Section-based reading and handbook identifiers exist in the agent. The description “guidance rather than a binding interface” needs qualification because the validator enforces selected handbook principles. |
| Navigation claim that every principle is accompanied by its reason | Reasons are present, but an explanation is not a citation. Several reasons introduce stronger claims than the recommendation itself. Add source locations and identify deductions. |
| M1: unfalsifiable hypothesis, moving criterion, and question–design mismatch | These inherit the M1.1–M1.5 limitations. An untestable hypothesis does not guarantee experimental success, and choosing a threshold afterwards can create an apparent finding rather than inevitably doing so. Exploratory results remain useful when labelled. |
| M1: Gray and benchmarketing | [Gray, introduction §6][gray], supports the historical connection between misleading comparisons and standardization. “The reason ... exist at all” is unnecessarily exclusive. Say it was a motivation. |
| M2: apples versus oranges, unequal effort, and over-specific tuning | These are grounded in [Raasveldt et al., §§3.2–3.4][dbtest]. Keep them as warnings about interpretation, with an exception for intentionally studied tradeoffs. |
| M2: elastic envelope | This is a local application of resource-interference concerns. Different permissions to consume resources do not prove that the alternatives actually received different resources. Disclose allocations and assess interference. |
| M2: the design that cannot lose | This follows the evaluation-space warning in [van der Kouwe et al., A1–A2][crimes]. Replace literal impossibility of a negative result with inadequate coverage of potential disadvantages. |
| M2: unreachable level | This repeats M2.9's unsupported inference. A flat result is still evidence about the tested configuration; it is insufficient evidence about all possible resource demand. |
| M3 introduction: closed models hold latency nearly flat and hide scheduling benefits | [Schroeder et al., Figures 2, 5 and 6; §5][schroeder], supports differences under specified populations and load manipulations. It does not establish a universal flat curve. State the conditions and distinguish changing population from changing think time. |
| M3 cross-reference: tails always need many more observations than means | Estimating rare percentiles often requires many observations, but the comparison depends on the distribution, percentile and required precision. The unqualified claim is not established. Replace it with a requirement to assess uncertainty for the chosen percentile. |
| M3: throttled throughput is the “most common” error | The capacity concern is valid; the frequency ranking has no identified evidence. Remove the ranking. |
| M3: closed measurements produce tails wrong by orders of magnitude | Severe errors are possible, not inevitable. The source distinguishes workload models; it does not license a numerical claim for every mismatch. State that the error can be large and depends on workload and stalls. |
| M3: latency at different achieved throughputs | Such a comparison may be valid if the experimental question fixes the client population and compares resulting performance. Specify whether demand, population, or achieved throughput is held comparable. |
| M3: concurrency as a proxy violates M2.1 | Incorrect as a general prohibition. The distinction between a manipulated factor and its consequences resolves this. See the detailed finding above. |
| M4: toy dataset and production claim; selective data range | These are reasonable applications of scope and subset-selection warnings. The problem is unsupported generalization or selective reporting, not a small dataset by itself. See [Huppler, slide 9][huppler-slides]. |
| M4: unpriced preparation | Supported by [Raasveldt et al., §3.7][dbtest]. Make accounting scope explicit. |
| M4: ramp-up in the measurement | It is a problem for an intended steady-state claim, not for an explicit startup study. This pitfall should preserve M4.5's exception. |
| M5 introduction: every shared-infrastructure measurement can vary | Reasonable as a conservative expectation for timing measurements. Literal universality does not apply to every recorded quantity, such as a deterministic row count. |
| M5: single-run comparison | Inherits the distinction between one aggregate observation and one run containing many observations. State which source of variation was not replicated. |
| M5: “blocked execution” | The example means running all measurements of one alternative first. In experimental design, blocking normally means grouping comparable experimental units to control variation. Rename the pitfall “grouped-by-alternative execution” and explain it in full. |
| M5: discarding inconvenient runs | A sound warning. Exclusions discovered after a run, such as a verified harness failure, can be justified if disclosed. Requiring advance enumeration of every possible invalidity is too strong. |
| M5: Mytkowicz and environment size | Directly supported by [Mytkowicz et al., abstract, §1 and §§4–5][mytkowicz]. Keep the claim and add a link to the paper. |
| M6: invisible client, missing platform, and heterogeneous alternatives | These are reasonable applications of disclosure and control. They need the same scope qualifications as M6.1–M6.3; heterogeneous environments can be the declared subject of a comparison. |
| M6: no monitoring makes failure indistinguishable from slowness | False literally. Exit status, errors, request failures and logs may distinguish them. Say missing resource observations can prevent explaining a slowdown or failure. |
| M7 cross-reference: a summary without spread is not a result | Too categorical. It remains an observation, but generally cannot support an uncertainty-sensitive comparison without more information. Deterministic quantities are another exception. |
| M7: averaged ratios have no meaning | This has identifiable source ancestry, but is mathematically too broad. Explain which aggregate is wanted and why a particular mean does not estimate it. See the ratio finding above. |
| M7: relative-only numbers and hidden component regressions | Supported by [Heiser's incomplete-evaluation items][heiser]. |
| M7: undefined metric is “most often” throughput without a unit | Defining units is sound; the frequency claim has no identified supporting evidence. Remove “most often.” |
| M8 cross-reference: repetitions last, levels first | An unsupported universal priority. It must depend on the claim, variation, costs, and the combinations required to separate effects. |
| M8: unfinished sweep, levels replacing repetitions, preparation budget, and one-attempt exploration | These are design risks, not categorical invalidities. Preserve sufficient uncertainty estimation and question coverage. Preparation and exploration may themselves be informative. Label the one-attempt constraint as local operating context. |

## Source verification and citation repairs

| Listed source | What was verified | Citation repair or limitation |
| --- | --- | --- |
| Gray, *The Benchmark Handbook*, 1993 | The author's available introduction contains the four criteria and the benchmarketing discussion, especially §§3 and 6. | Cite the edition and chapter/page explicitly. The available chapter alone does not authenticate its association with the particular 1993 edition. No fabricated-work indication was found. |
| Huppler, *The Art of Building a Good Benchmark*, TPCTC 2009 | The publisher verifies the paper, pp. 18–30. The exact handbook PDF was downloaded and read; it is a 19-page presentation. | Label [the linked document as slides][huppler-slides] and separately cite [the published paper][huppler-paper]. Do not imply the paper's full text was inspected. |
| Manolescu and Manegold, ICDE 2008 tutorial | The linked 238-slide presentation was inspected. | Its displayed title is *Performance Evaluation in Database Research: Principles and Experiences*, with plural “Experiences.” Cite relevant slides. |
| Raasveldt et al., DBTest 2018 | The six-page paper and Appendix A were inspected. | This is a strong source for several specific guidelines; cite §§3.1–3.8 individually rather than just listing the paper. |
| TPC specifications | [TPC-C revision 5.11][tpc-c] was inspected for steady state, timing, durability and disclosure. | The homepage is not a sufficient passage citation. Use a named benchmark, revision, and clauses; do not universalize its workload-specific requirements. |
| Jain, 1991 book | The author's course identifies the book and chapter mapping. His design, mistakes, and fractional-design slides were inspected, as was the tutorial's explicit reuse of Jain's material. | This is verification through the author's teaching material, not a full-text check of the 1991 book. Add exact book chapters/pages if claiming direct book derivation. |
| Hoefler and Belli, SC 2015 | The linked 12-page paper was inspected, including the numbered rules. | The available author PDF includes a 2017 clarification. Record the consulted revision. Cite rules plus nearby qualifications, not rules alone. |
| Heiser, *Systems Benchmarking Crimes* | The author's page was inspected. | This is expert guidance on a changing webpage, not itself a peer-reviewed study. Add an access date and distinguish it from the empirical survey. |
| Van der Kouwe et al., 2018 | The arXiv record and 17-page manuscript were inspected. | The listed 2018 preprint is real. Identify the consulted version and its population when quoting survey conclusions. |
| Schroeder, Wierman and Harchol-Balter, NSDI 2006 | The 14-page paper was inspected for model definitions, experiments and principles. | Preserve population, load and scheduling conditions when paraphrasing results. The paper also discusses partly open models. |
| Gil Tene and HdrHistogram | A [QCon 2012 slide deck][tene], the talk listing, [HdrHistogram's repository][hdr], and Tene's wrk2 explanation were inspected. | Name a dated talk and link it. The material supports coordinated omission; it does not establish historical priority for the phrase “original statement.” wrk2 is additional primary material used for clarification, not an originally listed separate citation. |
| Mytkowicz et al., ASPLOS 2009 | The paper's full text and IBM's publication record were inspected. | Add a direct paper link and §§2, 4–5 for the examples. |
| Kalibera and Jones, ISMM 2013 | Kent's exact download failed during access. A complete copy bearing the Kent repository cover and manuscript was read from a university course mirror. | Record that copy and the DOI. The paper supports repetition-level analysis and examines warm-up detection; it does not supply a universally reliable automatic detector. |
| Leitner and Cito, ACM TOIT 2016 | The linked arXiv manuscript, version 2 dated 19 January 2016, was inspected. | Preserve its provider/workload scope and exceptions. Do not silently transfer its empirical ordering to a different cluster. |
| ACM SIGMOD initiative | The official initiative and process description were inspected. | This is community artifact guidance. It supports reproducibility practices, not the full collection of experimental or statistical rules. |
| Erdelt, TPCTC 2020 | [Publisher metadata and abstract][erdelt2020] verify the work and its repetition, metrics and evaluation subject. | Proceedings publication is 2021, pp. 75–92. Conference year 2020 is correct when labelled. Full paper not inspected; no precise universal rule is validated from the abstract alone. |
| Erdelt, TPCTC 2021 | [Publisher metadata and abstract][erdelt2021] verify the work and its orchestration subject. | Proceedings publication is 2022, pp. 81–97. Full paper not inspected. Add its DOI. |
| Erdelt, TPCTC 2023 | [Publisher metadata and abstract][erdelt2023] verify the work and explicitly mention monitoring drivers and finding performance peaks. | Proceedings publication is 2024, pp. 124–142. An attempted institutional PDF fetch was denied; full paper not inspected. Add its DOI. |

The bibliography therefore mixes research papers, a textbook, slides, standards,
software documentation, expert commentary and community policy. Those are all
potentially useful sources, but their evidential roles should be visible.

## Required revision before claiming full literature support

1. Correct the substantive overclaims identified above, including those in
   pitfalls and chapter introductions rather than only numbered rules.
2. Give every guideline a specific source passage or label it as a deduction
   or local policy. A bibliography entry alone is insufficient traceability.
3. Preserve the conditions and limitations of empirical studies. Give survey
   populations when describing frequency, and remove unsupported superlatives.
4. Explain source disagreement about statistical summaries. A local choice can
   be justified without presenting it as universal agreement.
5. Complete the edition/version and full-text gaps before relying on any
   uninspected source for a precise claim. Add a direct methodology source for
   the stronger confirmation rules in M1 if those rules remain literature claims.

This audit supplies evidence and proposed corrections. **It does not certify
the current handbook as fully supported, and its findings are not yet applied
to the handbook.**

[gray]: https://jimgray.azurewebsites.net/benchmarkhandbook/chapter1.pdf
[huppler-slides]: https://www.tpc.org/tpctc/tpctc2009/tpctc2009-03.pdf
[huppler-paper]: https://link.springer.com/chapter/10.1007/978-3-642-10424-4_3
[tutorial]: https://ir.cwi.nl/pub/13810/13810B.pdf
[dbtest]: https://hannes.muehleisen.org/publications/DBTEST2018-performance-testing.pdf
[tpc-c]: https://www.tpc.org/tpc_documents_current_versions/pdf/tpc-c_v5.11.0.pdf
[jain-mistakes]: https://www.cse.wustl.edu/~jain/iucee/ftp/k_02mst.pdf
[jain-design]: https://www.cse.wustl.edu/~jain/iucee/ftp/k_16ied.pdf
[jain-fractional]: https://www.cse.wustl.edu/~jain/iucee/ftp/k_19ffd.pdf
[hoefler]: https://htor.inf.ethz.ch/publications/img/hoefler-scientific-benchmarking.pdf
[heiser]: https://gernot-heiser.org/benchmarking-crimes.html
[crimes]: https://arxiv.org/pdf/1801.02381
[schroeder]: https://www.usenix.org/legacy/event/nsdi06/tech/full_papers/schroeder/schroeder.pdf
[tene]: https://qconsf.com/sf2012/dl/qcon-sanfran-2012/slides/GilTene_HowNotToMeasureLatency.pdf
[hdr]: https://github.com/HdrHistogram/HdrHistogram
[wrk2]: https://github.com/giltene/wrk2
[mytkowicz]: https://eecs481.org/readings/producing-wrong-data.pdf
[kalibera]: https://petertsehsun.github.io/soen691/current/papers/reasonable_benchmarking.pdf
[cloud]: https://arxiv.org/pdf/1411.2429
[sigmod]: https://reproducibility.sigmod.org/
[erdelt2020]: https://link.springer.com/chapter/10.1007/978-3-030-84924-5_6
[erdelt2021]: https://link.springer.com/chapter/10.1007/978-3-030-94437-7_6
[erdelt2023]: https://link.springer.com/chapter/10.1007/978-3-031-68031-1_9
