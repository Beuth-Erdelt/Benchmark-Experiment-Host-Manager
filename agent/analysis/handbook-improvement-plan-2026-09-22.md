# Handbook improvements for models with approximately 20–30 billion parameters

Recorded: 2026-09-22. Status: research-backed proposal for later implementation
and evaluation. The original proposal did not implement these changes.

**Implementation update, 2026-09-22:** The subsequent
[review of the Glimmer and Gemma runs](model-run-review-2026-09-22.md) prioritizes
query-specific evidence and a verdict procedure. The first increment adds these
to the assessment tool and handbook, and corrects M2.9. The remaining proposals
are still pending. Model-level improvement requires a controlled replay; the
offline checks establish extraction and integration only.

**Follow-up procedure update, 2026-09-22:** Handbook 0.6.1 adds the short
[M8 follow-up procedure](../experiment_design_handbook.md#procedure-for-a-follow-up).
This implements the follow-up example proposed under improvement 1 and targets
the unnecessary-experiment measure in the evaluation plan. It makes explicit
the unresolved question, competing explanations, predicted outcomes, necessary
scope and cost. The three-model pilot motivated an additional clarification:
diagnosing the original failure and comparing performance under revised settings
are different experimental objectives. This increment changes documentation
only; its effect on model behavior remains to be evaluated.

## Purpose and evidence boundaries

The aim is to help the benchmark agent turn methodological guidance into valid
experiment designs and appropriately limited conclusions. The immediate user
request is to preserve the findings, background, citations, and testing ideas so
that implementation can resume without reconstructing this discussion.

Read this proposal together with the
[literature audit of handbook 0.5.0](handbook-literature-audit-2026-09-22.md).
The audit concerns whether the handbook's scientific claims are supported.
This proposal concerns how to present and operationalize corrected guidance.
Both are needed: making an incorrect rule easier to follow would amplify the
original problem.

Three kinds of statements must remain distinguishable in future documentation:

- **Research findings** describe what a cited study actually tested and found.
- **Proposed adaptations** describe how we might apply those findings to this
  benchmark agent. Their effectiveness remains to be measured here.
- **Local policy** describes an engineering or operating choice, such as a tool
  budget. A policy must have a rationale but must not be presented as a universal
  finding from the literature.

There is relevant evidence near the intended model size: the long-context study
below includes 30B models, the grammar study includes a 33B model, and the tool
training study includes a 32B model. Other studies use different sizes or model
families. None establishes that the complete proposal improves database
experiment design for every model with 20–30 billion parameters. Parameter count
alone is not a sufficient basis for transferring the reported results.

## Starting point and prerequisite corrections

The existing agent already separates design, result interpretation, and
follow-up authoring. It has phase-specific tools, catalog and environment
validation, handbook chapter reads, recorded trajectories, and deterministic
result checks. Improvements should build on these mechanisms instead of adding
a second competing workflow. This description refers to the working tree
reviewed on 2026-09-22; check it again before implementation.

The audit classified the 50 numbered guidelines as 18 supported, 20 requiring
qualification, 10 derived recommendations or local policies, and 2 containing
unsupported substantive assertions. These are whole-guideline classifications,
not counts of individual factual claims. The audit did not find evidence of
fabricated named publications, but it could not establish full support for the
handbook as written.

Before strengthening instruction or enforcement, resolve these issues using the
audit's source passages and proposed qualifications:

1. Revise M2.9 so that low average resource utilization does not prove that an
   allocation change was never tested. Separate a measured workload-specific
   result from an explanation of the mechanism.
2. Remove the categorical rejection of concurrency sweeps. Distinguish a fixed
   population of clients from an independently imposed arrival rate.
3. Distinguish achieved throughput at a prescribed demand from maximum capacity.
4. Qualify M4.2: a cached dataset can still exercise durable storage writes.
5. Revise M6.4 so that utilization evidence alone does not establish causation.
6. Correct the interpretation of overlapping confidence intervals and qualify
   generalizations from particular cloud measurements.
7. Reconcile handbook guidance with phase prompts and validation rules. In
   particular, wording that permits only one changing input must not silently
   prohibit a justified experiment that varies several factors to estimate
   their separate and interacting effects.

These corrections require their own review. This proposal does not turn the
audit's suggested wording into an already approved scientific reference.

## Proposed improvements

### 1. Translate abstract guidance into short decision procedures

**Problem to address.** A model may quote a principle correctly while omitting
the observations or choices needed to apply it to a concrete benchmark.

**Research basis.** Khot et al. decomposed tasks into prompted subproblems and
allowed specialized prompts or symbolic functions to solve the components.
Their experiments concern symbolic and language reasoning tasks, including
multi-hop question answering, rather than database experiments. This supports
testing explicit decomposition here; it does not establish the effectiveness
of a particular handbook format or a 20–30B model result. [R1]

**Proposed adaptation.** Add a small companion of procedures. Each should state
when it applies, which evidence is required, which decision that evidence can
support, when to stop or ask for more evidence, and which conclusions remain
unjustified. Link each procedure to the corrected guideline and its specific
scientific source passage. Keep procedural steps short enough to inspect as a
unit.

Candidate procedures include selecting the workload arrival model, defining a
resource comparison, checking comparable query coverage, selecting a summary
statistic from the question, and deciding whether a follow-up distinguishes
competing explanations. The procedure must allow a valid inconclusive outcome.

**Illustrative resource-comparison procedure.** This is proposed editorial
content based on the audit's analysis of M2.9, not a quotation from Khot et al.:

1. State whether the question concerns the effect of an allocation under fixed
   settings or the best performance attainable after retuning.
2. Identify the allocation being changed and the settings held fixed. If several
   settings change together, identify the joint intervention explicitly.
3. Inspect configuration limits and available workload and resource measurements.
   Record missing evidence. Do not equate low average utilization with proof of
   no resource pressure at every time or on every processor core.
4. Report the observed outcome under the tested conditions. A flat outcome is
   not evidence that the resource never matters.
5. If explanation matters, propose a comparison that could distinguish the
   suspected limit from another plausible explanation. Do not claim to have
   isolated CPU and parallelism effects when both changed together.

**Evaluation.** Compare the corrected handbook alone with the same handbook plus
procedures, using identical questions, tools, and budgets. Review whether the
design answers the intended question and whether conclusions stay within the
evidence. A longer answer is not itself an improvement.

### 2. Provide selected, verified worked examples

**Problem to address.** General instructions may leave the model uncertain about
what an acceptable complete design or a properly limited conclusion looks like.

**Research basis.** Rubin, Herzig, and Berant trained a retriever to select
demonstrations for in-context learning, where examples are supplied in the
model's input without changing its weights. Their experiments cover three
semantic parsing tasks that map language to formal representations. The results
support investigating relevant example selection, not a universal example
count or the effectiveness of negative examples for benchmark design. [R2]

**Proposed adaptation.** Build a reviewed example library. Each entry should
contain a question, necessary environment facts, a proposed design, the evidence
used to assess it, a justified conclusion, and explicit limits. Include the
reason the example is relevant. Keep illustrative data visibly marked as
synthetic; use archived runs only with their actual provenance and limitations.

Initial cases should cover achieved throughput at a client-imposed rate, unequal
successful query coverage, and a resource increase with no measured improvement.
Include an inconclusive case. A paired misleading conclusion with its correction
is worth testing, but its benefit is a separate hypothesis, not a finding of R2.

Start with manually selected examples so that editorial quality can be checked
before introducing automated retrieval. Test selection and example count as
experimental choices. Do not assume that more demonstrations are always better.

**Evaluation.** Compare relevant examples against the corrected handbook alone
and, separately, against an equal-budget selection of less relevant examples.
Use questions with different surface details and combinations of conditions.
Review whether the agent copies incidental settings or genuinely applies the
method. Keep evaluated questions out of the demonstration library.

### 3. Deliver relevant guidance at the decision where it is needed

**Problem to address.** Required guidance can be present in the conversation yet
poorly used. An expanding handbook also competes with results and tool feedback
for the model's available input space.

**Research basis.** Liu et al. found that performance on long-context tasks
depended on where relevant information appeared. Section 4.3 and Figure 10
include MPT-30B and MPT-30B-Instruct; both showed sensitivity to information
position. This is evidence about those models and tasks, not proof that every
current 30B model fails in the same way. [R3]

**Proposed adaptation.** Extend the existing chapter-selection mechanism to
offer the applicable procedure and a small selection of examples at design,
interpretation, or follow-up time. Keep the full handbook accessible. Record
which material was supplied, its version, its position, and whether it was
provided automatically or requested through a tool.

Do not treat a model's acknowledgement of a chapter as proof that it used the
chapter correctly. If automatic context delivery replaces an explicit read,
update provenance honestly rather than recording a read that did not happen.
Avoid untested rules such as always repeating the whole handbook at the end.

**Evaluation.** Hold the guidance content fixed while changing delivery and
position. Compare current selective reads, targeted automatic delivery, and
representative placements within the conversation. Include cases where an
initially unselected chapter becomes relevant and must still be discoverable.
Measure reasoning quality alongside input tokens and read-tool calls.

### 4. Constrain output structure where the provider supports it

**Problem to address.** Invalid field names, malformed tool arguments, or unknown
verdict values can consume repair attempts before scientific quality is assessed.

**Research basis.** Geng et al. studied grammar-constrained decoding, which limits
the next generated tokens to sequences permitted by a formal grammar. Their
structured extraction, entity linking, and parsing experiments include LLaMA
7B, 13B, and 33B models. Results support testing generation constraints for
structured outputs; grammatical validity does not establish factual or
scientific correctness. [R4]

**Proposed adaptation.** First inspect actual endpoint support. Where supported,
constrain tool argument structure and finite allowed values using the existing
contracts as the authority. Continue semantic and environment validation after
generation. Do not introduce a second manually maintained catalog of allowed
values, or assume that every advertised structured-output mode enforces the
same constraints.

**Evaluation.** Report malformed output frequency, successful repair rate, and
end-to-end task quality. Include outputs that are structurally valid but
scientifically wrong. Test provider behavior explicitly; record unsupported
modes instead of silently comparing different guarantees.

### 5. Make correction depend on specific external evidence

**Problem to address.** A generic request to reconsider may encourage a confident
rewrite without fixing the failed condition.

**Research basis.** Huang et al. examined intrinsic self-correction, meaning
revision without external feedback, on reasoning tasks. It was unreliable in
their tested settings and could reduce performance. The paper discusses external
feedback and limits its conclusions; it does not prove that all self-correction
is impossible or that this agent's validators are correct. [R5]

**Proposed adaptation.** Reuse current validators and computed result checks to
return the failed condition, observed values, practical consequence, and the
choice that needs reconsideration. Identify whether feedback is a hard
contract violation, a scientific limitation, or advisory guidance. Enforce only
conditions whose semantics and applicability have been reviewed.

For example: “CPU allocation and memory allocation both changed. This comparison
can estimate their joint effect under these conditions. It cannot separately
attribute the observed difference to CPU allocation. Revise the attribution or
choose a design that can separate the effects.” This is more precise than
rejecting every design with two changing factors.

**Evaluation.** Compare current feedback with evidence-specific feedback at the
same repair budget. Include valid joint interventions, unavailable monitoring,
and genuinely incomplete comparisons. Track successful correction, false
rejection, repeated failed attempts, and correct decisions to stop. The initial
prompt must already contain the same requirements; withholding requirements
until feedback would bias the comparison.

### 6. Consider training on verified tool use only after the workflow stabilizes

**Problem to address.** Some failures may persist after clearer instructions,
examples, context delivery, and useful tool feedback.

**Research basis.** Li et al. trained models to reason with a code interpreter
and evaluated mathematical reasoning. Their study includes a 32B
DeepSeek-R1-Distill-Qwen model. It reports benefits from its training procedure,
but does not establish transfer to database benchmarking. The procedure includes
multiple stages; its final results must not be attributed to the initial small
curated example set alone. [R6]

**Proposed adaptation.** Treat fine-tuning, which changes model weights through
training examples, as a later option. Preserve reviewed trajectories showing
correct tool selection, meaningful repairs, supported conclusions, inconclusive
outcomes, and justified stopping. Reject traces that merely passed a validator
while making an unsupported claim. Keep training and final evaluation examples
separate by question family and underlying scenario where possible.

**Evaluation.** Compare the trained model with its exact untrained starting
checkpoint under the same corrected workflow. Test unfamiliar task families,
retention of ordinary instruction following, tool cost, and unsupported claims.
Begin only when a stable evaluation set and enough reviewed examples exist.
No particular training method, dataset size, or improvement is promised here.

## Implementation boundaries and likely integration points

The following locations are suggestions for later work, not files added by this
proposal. Confirm current ownership and interfaces before editing.

| Location | Intended role in a future change |
|---|---|
| `agent/experiment_design_handbook.md` | Correct scientific wording and provide precise claim-to-source references. |
| Proposed `agent/experiment_design_procedures.md` | Hold short, source-linked decision procedures. |
| Proposed `agent/experiment_design_examples.md` | Hold reviewed examples and their provenance. |
| `agent/harness/prompts.py` | Explain when to consult guidance and how to bound conclusions. |
| `agent/harness/agent.py` | Deliver phase-appropriate context and record its actual provenance. |
| `agent/harness/tools.py` | Permit authorized companion reads and expose useful evidence and feedback. |
| `agent/harness/validation.py` | Enforce reviewed, decidable conditions and describe limitations accurately. |
| `agent/harness/model_client.py` | Negotiate optional generation constraints if the endpoint supports them. |
| `tests/test_agent_harness.py` | Verify affected tool, validation, phase, and provenance behavior. |
| `docs/FEATURES.md` | Record each implemented change and its verification status. |

Keep benchmark-specific knowledge in the existing authoritative materials rather
than duplicating it across prompts. No changes to `bexhoma/`, top-level experiment
drivers, `k8s/`, or `contracts/` are authorized by this proposal. If a required
capability is missing there, document the limitation and propose it separately.

## Evaluation plan

### Establish a corrected baseline and isolate changes

Keep an archived snapshot of the current behavior for diagnosis. Use a reviewed,
corrected handbook and reconciled prompts as the baseline for measuring guidance
improvements. Otherwise a change in scientific content and a change in delivery
would be inseparable explanations for any gain.

An ablation is a comparison that adds or removes one component to estimate its
contribution. Start with these comparisons rather than enabling everything at
once:

| Comparison against the corrected baseline | Main question |
|---|---|
| Add procedures only. | Does explicit decision structure improve application of the guidance? |
| Add examples only. | Do relevant demonstrations improve design and interpretation? |
| Change context delivery only. | Does the same content work better when supplied at the relevant decision? |
| Add supported output constraints only. | Do fewer structural failures improve completion without concealing scientific errors? |
| Change correction feedback only. | Does evidence-specific feedback improve repair at a fixed budget? |

Combine promising components afterward and test whether their benefits persist
together. Evaluate training last against the strongest stable untrained setup.
Where an intervention adds input tokens, report that increase and include a
comparison under a common token or cost budget when practical. Equal tool-call
limits alone do not establish equal computational cost.

### Build cases that expose both failure and overrestriction

Use archived result bundles or clearly identified synthetic fixtures for initial
offline evaluation. A fixture is a fixed set of inputs and expected properties
used to exercise a particular case. Design tasks need fixed environment and
catalog snapshots; interpretation tasks need identical result evidence across
conditions. Run live experiments later when a question genuinely requires
execution; document changes in infrastructure and workload conditions.

The case set should include valid concurrency sweeps, rate-capped throughput
measurements, cached workloads with durable writes, low average utilization with
limited monitoring, unequal query coverage, justified joint interventions, and
missing evidence that warrants an inconclusive conclusion. Include ordinary valid
cases so that more frequent refusal cannot masquerade as better reasoning.

Separate development examples from held-out evaluation cases, which are reserved
until the design is fixed. Split by substantive scenario or question family, not
only by changing numerical values in the same template. Accept multiple valid
designs; a single reference answer must not make one preferred wording the only
correct outcome.

### Judge scientific quality independently of the enforcement mechanism

Use a written rubric reviewed against the corrected handbook and source passages.
Reviewers should not see which intervention produced an answer when feasible.
Do not use the validator being improved as the sole judge of its own success.
For disputed cases, retain the evidence and document the resolution.

The primary outcome should be the proportion of assigned tasks with an
appropriate design or interpretation and a conclusion supported by the available
evidence. Define those requirements separately for each phase before scoring.
Report incomplete tasks, refusals, and execution failures explicitly.

Also report the following measures with clear denominators:

- Report the fraction of reviewed substantive claims that lack support, together
  with the fraction of tasks containing at least one such claim.
- Report inappropriate causal attribution and unjustified claims of capacity.
- Report structurally invalid outputs and repairs that actually resolve their
  original failure.
- Report false rejection of valid designs and inappropriate refusal to answer.
- Report unnecessary follow-up experiments, with a stated review criterion for
  whether the experiment could change the answer or distinguish explanations.
- Report tool calls, generation and input tokens, elapsed time, and experiment
  cost where available.

### Control model and prompt variation

Record the exact model checkpoint or served revision, numeric precision,
inference settings, context limit, prompt and handbook versions, selected
examples, tool limits, and environment snapshot. For models that activate only
part of their parameters on each token, record both total and active parameter
counts. Differences between model families must not be interpreted as a pure
parameter-count effect.

Use the same questions for paired comparisons and repeat stochastic generations
where needed. Choose repetitions and the number of cases from pilot variability
and the smallest improvement worth detecting; this proposal supplies no
literature-backed universal sample count. Report uncertainty and performance by
task family, rather than only an overall mean. Separate operational failures
from scientific failures without deleting either from the completion accounting.

Test equivalent instruction formats as a robustness check. Sclar et al. found
substantial sensitivity to meaning-preserving prompt formatting in their tested
models and tasks, including models smaller than the target range. This motivates
checking that a chosen handbook presentation is not benefiting from one fragile
format; it does not supply a guaranteed robust template for this agent. [R7]

Before final held-out evaluation, write down the required practical improvement,
acceptable cost, and tolerated regressions. Set these project criteria using the
pilot and intended use, then freeze them. Do not select success thresholds after
seeing final results.

## Recommended order and completion criteria

First correct the scientific claims and conflicting instructions. Next prototype
procedures and a small reviewed example library, measuring each independently.
Then test targeted delivery and evidence-specific feedback. Output constraints
can proceed as an independent capability check. Consider training after the
workflow and evaluation are stable.

A future implementation is ready for review when its changed guidance has
claim-level citations and applicability limits, its integration preserves honest
provenance, its affected tool behavior has focused tests, and its evaluation
reports both scientific quality and operating cost. Keep unsuccessful variants
and their results in the record so that later work does not repeat them.

Open choices for that work include which exact models to test, the task families
and budget, who reviews scientific judgments, and whether available endpoints
support generation constraints. These are implementation decisions, not missing
research findings to fill with invented numbers.

## References

The links below identify primary research. Each supports the bounded research
summary above; the repository-specific adaptations and evaluation design are
proposals. For the benchmarking science underlying the illustrative cases, use
the claim-by-claim references in the companion audit.

**[R1]** Tushar Khot, Harsh Trivedi, Matthew Finlayson, Yao Fu, Kyle Richardson,
Peter Clark, and Ashish Sabharwal. 2023. *Decomposed Prompting: A Modular Approach
for Solving Complex Tasks*. ICLR.
[Paper](https://arxiv.org/pdf/2210.02406).

**[R2]** Ohad Rubin, Jonathan Herzig, and Jonathan Berant. 2022. *Learning To
Retrieve Prompts for In-Context Learning*. NAACL, pages 2655–2671.
[Publication and paper](https://aclanthology.org/2022.naacl-main.191/).
DOI: 10.18653/v1/2022.naacl-main.191.

**[R3]** Nelson F. Liu et al. 2024. *Lost in the Middle: How Language Models Use
Long Contexts*. Transactions of the Association for Computational Linguistics.
[Paper](https://aclanthology.org/2024.tacl-1.9.pdf).
See particularly Section 4.3 and Figure 10 for MPT-30B and MPT-30B-Instruct.

**[R4]** Saibo Geng, Martin Josifoski, Maxime Peyrard, and Robert West. 2023.
*Grammar-Constrained Decoding for Structured NLP Tasks without Finetuning*.
EMNLP. [Publication](https://aclanthology.org/2023.emnlp-main.674/)
and [paper](https://aclanthology.org/2023.emnlp-main.674.pdf).
See Sections 4–5 and the task result tables for the evaluated models and tasks.

**[R5]** Jie Huang et al. 2024. *Large Language Models Cannot Self-Correct
Reasoning Yet*. ICLR. [Paper](https://arxiv.org/pdf/2310.01798).
See the definition of intrinsic self-correction, the reasoning experiments,
and Sections 6–7 for discussion and limitations.

**[R6]** Chengpeng Li, Zhengyang Tang, Ziniu Li, Mingfeng Xue, Keqin Bao,
Tian Ding, Ruoyu Sun, Benyou Wang, Xiang Wang, Junyang Lin, and Dayiheng Liu.
2025. *Teaching Language Models to Reason with Tools*. NeurIPS.
[Conference paper](https://papers.nips.cc/paper_files/paper/2025/file/6087df8ad77f2fc8025ee0d861224596-Paper-Conference.pdf).
The reported domain is mathematical reasoning with a code interpreter.

**[R7]** Melanie Sclar, Yejin Choi, Yulia Tsvetkov, and Alane Suhr. 2024.
*Quantifying Language Models’ Sensitivity to Spurious Features in Prompt Design
or: How I learned to start worrying about prompt formatting*. ICLR.
[Paper](https://arxiv.org/pdf/2310.11324).

[R1]: https://arxiv.org/pdf/2210.02406
[R2]: https://aclanthology.org/2022.naacl-main.191/
[R3]: https://aclanthology.org/2024.tacl-1.9.pdf
[R4]: https://aclanthology.org/2023.emnlp-main.674/
[R5]: https://arxiv.org/pdf/2310.01798
[R6]: https://papers.nips.cc/paper_files/paper/2025/file/6087df8ad77f2fc8025ee0d861224596-Paper-Conference.pdf
[R7]: https://arxiv.org/pdf/2310.11324
