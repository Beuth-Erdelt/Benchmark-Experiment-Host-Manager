# Handbook source provenance — handbook v0.8.3

For each source the v0.8.0 handbook cites: its evidential type, one short
verbatim anchor quote, and the guidelines it grounds with their locators and
verification status. Organized by source; for the rule-by-rule view see
`handbook_source_map_multi.md`. Supersedes the v0.4.0-based provenance file. *S3* = the locator-confirmation session.

Verbatim quoting is limited to one short anchor per source. The per-entry
**locators** do the verification work and are what you cite. The source texts
themselves are not stored here — re-check against the paper if needed.

**Status legend**
- ✅ verified against the source text (the session is noted: *S1* = the earlier
  provenance session, including your uploaded Jain and Gray; *S2* = the v0.8.0
  review session).
- ◐ source verified, but this specific locator (section/clause number) not yet
  confirmed.
- 📄 locator taken from the audit or the handbook, not checked by me.

Never cite a ◐ or 📄 locator externally until it is confirmed.

---

## NIST/SEMATECH e-Handbook `nist_ehandbook` [T]
Web reference; cite by section number and page URL. Section pages fetched S2.
**Anchor quote (§5.3.3.2):** "Block what you can, randomize what you cannot."

| Entry | Locator | Status |
|----|----|----|
| M1.1, M1.4 | §5.3.1 — objectives; comparative vs screening designs | ✅ S2 |
| M1.3, M5.3 | §1.3.5 — "Practical Versus Statistical Significance": significance depends on sample size; a large sample can reject for a difference of no engineering significance | ✅ S5 |
| M5.3, M5 pitfalls | §1.3.5 — accepting a hypothesis does not mean it is true (nonsignificant ≠ equal) | ✅ S5 |
| M1.5, M7.1, M7.3 | §5.3.2 — include all relevant responses; measure both rates, not only their ratio | ✅ S2 |
| M2.9 | §5.3.2 — model matrix with interaction term | ✅ S2 |
| M2.1 | §5.3.3.3 — full factorial designs | ✅ S2 |
| M2.1 | §5.3.3.4.3 — confounding/aliasing; sparsity-of-effects assumption | ✅ S2 |
| M2.2, M5.7, M6.2 | §5.3.3.2 — nuisance factors; blocking; randomize the rest | ✅ S2 |
| M5.7, M8.1, M8.4 | §5.1.3 — keep simple; check runs feasible; watch drifts; allow for the unexpected | ✅ S2 |
| M1.4, M8.1, M8.2, M8.4 | §5.3.3 — design depends on objectives, resources and error control; leave runs for redos | ✅ S2 |
| M2.7 | 5.5.9.9, "How do we Use the Model Beyond the Data Domain?" (page `pri5998`) | ✅ S2 — numbering differs between live site and old exports; cite title + URL |
| M2.7 | 5.5.9.9, model-validation page (`pri599b`) — predictions need confirmatory data | ✅ S2 (same numbering caveat) |

## Jain 1991 `jain1991art` [T]
Uploaded web-capture edition has no printed pages; cite by section.

| Entry | Locator | Status |
|----|----|----|
| M1.1, M1.2, M1.4 | §2.1 — goals; metrics, workloads and methodology depend on the goal | ✅ S1 |
| M7.1 | §3.1 — selecting a metric | ✅ S1 |
| M2.7 | §15 — confidence falls outside the measured range | ✅ S1 |
| M2.1 | §16.3 — interactions not estimable with one-factor-at-a-time designs | ✅ S1 |
| M2.9 | ch. 16 — experimental design, interactions | ✅ S1 (chapter level) |
| M8.2 | §16.3.3 — fractional factorials save time and expense | ✅ S1 |
| M8.4 | Box 2.1, item 10 — efficient design | ✅ S1 |

## Gray (ed.) 1993 `gray1993benchmark` [T]
Chapter 1, Gray's introduction; an expert essay within a reference work.
Cite the print 2nd edition (Morgan Kaufmann, 1993) by section and page.
**Anchor quote (from your upload):** benchmarketing highlights "the strengths of
the product and hiding its weaknesses."

| Entry | Locator | Status |
|----|----|----|
| M1.5 | ch. 1, relevance criterion — §1.3, p. 5, print 2nd ed. (your upload) | ✅ S1 — cited as ch. 1, §1.3, p. 5 |
| M1 pitfalls | ch. 1, benchmarketing — §1.5, p. 8, print 2nd ed. (your upload) | ✅ S1 — cited as ch. 1, §1.5, p. 8 |

## Nosek et al. 2018 `nosek2018preregistration` [M]
PNAS 115(11), 2600–2606. Abstract and metadata checked S2.
**Anchor quote (abstract):** "define the research questions and analysis plan before observing the research outcomes"

| Entry | Locator | Status |
|----|----|----|
| M1.3, M1 pitfalls | abstract — prediction vs postdiction; preregistration | ✅ S2 |

## Ledgerwood 2018 `ledgerwood2018` [C]
PNAS letter, 115(45), E10516–E10517. Checked S2.
**Anchor quote:** "Preregistering analysis plans enables type I error control."

| Entry | Locator | Status |
|----|----|----|
| M1.1 | predictions → falsifiability | ✅ S2 |
| M1.3 | analysis plans → type I error control | ✅ S2 |

## Raasveldt et al. 2018 `raasveldt2018fair` [M]
DBTest '18, 6 pp. Full text fetched S2; section titles confirmed.
**Anchor quote (abstract):** "many different ways to influence benchmark results to favor one system"

| Entry | Locator | Status |
|----|----|----|
| M6.3, M2.2 | §3.1 Non-Reproducibility | ✅ S2 |
| M2.4, M2.2 | §3.2 Failure To Optimize | ✅ S2 |
| M2.5, M2.2, M2 pitfalls | §3.3 Apples vs Oranges | ✅ S2 |
| M2 pitfalls | §3.4 Overly-specific Tuning | ✅ S2 |
| M4.1, M4.3 | §3.5 Cold vs Hot Runs | ✅ S2 |
| M4.1, M4.3, M8.3 | §3.6 Cold vs Warm Runs (cold runs time-consuming; virtualization host caching) | ✅ S2 |
| M4.4, M8.3 | §3.7 Ignoring Preprocessing Time (incl. automatic indexing/encoding) | ✅ S2 |
| M2.5, M4.6 | §3.8 Incorrect Code | ✅ S2 |
| M2.8, M4.3, M4.5, M5.2, M6.3 | Appendix A checklist (justify subset; hot runs ignore initial runs; median + CI; reproducibility items) | ✅ S2 |
| M1 pitfalls | §§1, 2.2 — benchmarketing, citing Gray ch. 1 | ✅ S2 |

## Hoefler & Belli 2015 `hoefler2015scientific` [M]
SC '15; twelve numbered rules. Verified S1.
**Anchor quote (Rule 1 corollary):** "never report ratios without absolute values."

| Entry | Locator | Status |
|----|----|----|
| M7.3 | Rule 1 (§2.1.1) | ✅ S1 |
| M7.2 | §3.1.1, Rules 3–4 | ✅ S1 |
| M5.2, M5.3 | Rule 5 (§3.1.2) | ✅ S1 |
| M5.4 | Rules 6–8 | ✅ S1 |
| M5.3 | Rule 7 (§3.2) | ✅ S1 |
| M7.4 | Rule 8 (§3.2.3) | ✅ S1 |
| M2.6 | Rule 9 (§4.2) | ✅ S1 |
| Verdict procedure | background | ✅ S1 |

## van der Kouwe et al. 2020 `vanderkouwe2020flaws` [M]
IEEE Security & Privacy 18(3), 48–57, 2020; DOI 10.1109/MSEC.2020.2969862 (VU and
dblp records, S3). Full text read S3. Its own flaw codes A1–F4 (22 flaws) differ
from Heiser's: e.g. Heiser E2 = vdK F3, vdK E2 = "measuring only run-time overhead".
**Anchor quote (§1):** "Our list is based in large part on a web page by Heiser"

| Entry | Locator | Status |
|----|----|----|
| M2.8 | A1 degradation not evaluated; A2 subsetting without justification; A3 selective data sets | ✅ S3 |
| M2.4 | D3 unfair benchmarking of competitors | ✅ S3 |
| M5.2 | B4 no indication of significance (most widespread flaw: 80% of applicable papers) | ✅ S3 |
| M6.3 | F1 missing platform specification; F2 missing software versions | ✅ S3 |
| M7.3 | F4 relative numbers only | ✅ S3 |
| M7.5 | A2 subsetting; F3 subbenchmarks not listed | ✅ S3 |
| M7.6 | B1 microbenchmarks representing overall performance | ✅ S3 |
| M7.7 | B2 throughput degraded by x% ⇒ overhead x%; B3 bad math (percentage points) | ✅ S3 |

## Heiser, "Systems Benchmarking Crimes" `heiser_crimes` [C]
Web page; author's own description: a work in progress. Contents list checked S2
(letter scheme A–E).
**Anchor quote (category A):** "the mother of all benchmarking crimes: using a biased set of benchmarks"

| Entry | Locator | Status |
|----|----|----|
| M2.8 | A1 not evaluating potential degradation; A2 sub-setting | ✅ S2 |
| M7.5, verdict procedure | A2 sub-setting; E2 missing sub-benchmark results | ✅ S2 |
| M7.6 | B1 microbenchmarks | ✅ S2 |
| M7.7 | B2 throughput only; B3 downplaying overheads | ✅ S2 |

## Schroeder, Wierman & Harchol-Balter 2006 `schroeder2006open` [E]
NSDI '06, pp. 239–252. Verified S1; abstract re-checked S2.
**Anchor quote (abstract):** "a vast difference in behavior between open and closed models"

| Entry | Locator | Status |
|----|----|----|
| M3 intro | closed, open and partly open models | ✅ S2 |
| M3.1 | guiding principles for choosing the model for a workload | ✅ S2 (abstract level; cite the principles section by name) |
| M3.2 | closed generators self-limit under overload; Fig. 5 | ✅ S1 |
| M3.4 | offered load depends on system speed in a closed model | ✅ S1 |
| M3.5 | response time depends on multiprogramming level | ✅ S1 |

## Tene, "How NOT to Measure Latency" `tene_latency` [C]
Talk, QCon London 2013. Verified S1 (~33:50 for coordinated omission).
Recording: infoq.com/presentations/latency-pitfalls (S3; abstract matches the QCon London 2013 programme).
**Anchor quote:** coordinated omission "can often render percentile data useless."

| Entry | Locator | Status |
|----|----|----|
| M3.4 | coordinated omission — origin of the term | ✅ S1 |
| M7.4 | measure the full distribution / high percentiles | ✅ S1 |

## wrk2 README `wrk2` [C]
Tool documentation. Checked S2 (README text via mirrors of the same repository).
**Anchor quote:** "from the point in time where a request was supposed to be sent"

| Entry | Locator | Status |
|----|----|----|
| M3.2 | constant-throughput `--rate` parameter (illustrative only) | ✅ S2 |
| M3.4 | latency measured from the planned send time; closing note on coordinated omission | ✅ S2 |

## TPC-C rev. 5.11 `tpc` [S]
Cite the named revision and clause, not the homepage. Verified S1.
**Anchor quote:** "reached a steady state prior to commencing the measurement interval."

| Entry | Locator | Status |
|----|----|----|
| M4.2 | §3.5 durability | ✅ S1 (audit counterexample) |
| M3.3 | §5.2.5 maximum qualified throughput; §5.5 steady state | ✅ S1 |
| M4.5 | §5.5 measurement interval | ✅ S1 |
| M3.6, M6.1 | Clause 6 — SUT, driver and communications definition (RTE, emulated components, driver/SUT disclosure) | ✅ S3 via TPC-C FDR tables of contents; S1's "Clause 5" was wrong. Clause 6 defines the boundary; "not the bottleneck" is our Application |
| M6.3 | Clause 8, full disclosure | ✅ S1 |

## Kalibera & Jones 2013 `kalibera2013rigorous` [E]
ISMM '13, pp. 63–74. Full manuscript read S3 (KAR version, which corrects the
ISMM version). Sections: 3 repetition levels; 4 summarising results; 6 repeating
iterations; 7 executions; 8 compilation; 9 multi-level repetition; 10 speedup.
**Anchor quote (abstract):** "repetition is most needed where most uncertainty arises."

| Entry | Locator | Status |
|----|----|----|
| M5.1 | §3 levels of repetition; §9 optimal counts for a given precision | ✅ S3 |
| M5.5 | §3 levels; §§6–9 independence, executions, compilation, multi-level | ✅ S3 |
| M5.2 | §1 most surveyed execution-time papers gave no measure of variation; §4 effect sizes | ✅ S3 |
| M5.3, M1.3 | §4 significance tests confuse sample size with practical relevance; overlap test conservative; §10 Fieller interval for ratios | ✅ S3 |
| M4.5 | §6 initialised vs independent state; §6.3 automated warm-up heuristics unreliable | ✅ S3 |
| M8.2 | §9 cost model for repetitions under a time budget | ✅ S3 |
| all | v0.7.2's §§3, 4, 6, 9, 10 | ✅ S3 — all correct |

## Leitner & Cito 2016 `leitnercito2016` [E]
ACM TOIT 16(3), 2016; arXiv 1411.2429. Full text (arXiv v2 = published version)
read S3. Four providers (EC2, GCE, Azure, Softlayer); v1 covered only EC2 and GCE.
**Anchor quote (abstract):** "multitenancy has a dramatic impact on performance and predictability."

| Entry | Locator | Status |
|----|----|----|
| M2.3, M6.5 | §2 multi-tenancy and noisy neighbours defined; §5.2 validation | ✅ S3 |
| M6.2 | §2 heterogeneity defined; §5.2.1 heterogeneity found only in Azure and small EC2 types | ✅ S3 |
| M5.6 | §5.2.1 Table 4 (between instances) vs §5.2.2 Table 6 (within instances): within < between in all but one configuration; multi-tenancy strong only for some providers | ✅ S3 — the earlier "dominates" wording overstated this; corrected in v0.8.1 |

## Mytkowicz et al. 2009 `mytkowicz2009wrong` [E]
ASPLOS XIV, pp. 265–276. Verified S1; abstract re-checked S2.
**Anchor quote (abstract):** "measurement bias is significant and commonplace."

| Entry | Locator | Status |
|----|----|----|
| M6.4, M1.2 | causal analysis (method for detecting bias) | ✅ S2 (abstract; cite the section by method name) |
| M5.7 | setup randomization (method for avoiding bias) | ✅ S1/S2 |
| M5 pitfalls | environment size and link order as bias sources | ✅ S1 |

## Manolescu & Manegold 2008 `manolescu2008performance` [C]
ICDE 2008 tutorial, 235 slides (beamer; slide = page). Read in full from your upload (S4).
**Anchor quote (slide 47):** "Research: Always question what you see!"

| Entry | Locator | Status |
|----|----|----|
| M6.4 | slides 45–53 — unexplained scan timings; standard profiling insufficient; hardware counters, profilers, system monitors, DBMS EXPLAIN | ✅ S4 |
| M2.4 | slides 40–44 — compiler flags up to 2×, tuning 2–10×; "absolutely fair" comparisons virtually impossible, so document | ✅ S4 |
| M4.3 | slides 31–35 — definitions of cold and hot runs; document the choice; user vs real time | ✅ S4 |
| M6.3 | slides 149–150 hardware specification; 155–160 making experiments repeatable | ✅ S4 |
| — | slides 55–58 experiment design and common mistakes: taken from Jain; cite Jain | ✅ S4 |

## Erdelt TPCTC papers `erdelt_tpctc20/21/23` [O]
Author's own work. DOIs/pages from the audit, consistent across both handbooks.

| Entry | Locator | Status |
|----|----|----|
| M3.6, M6.1 | TPCTC 2023 (proc. 2024, pp. 124–142) — monitoring benchmark drivers | 📄 audit — you are the authority |
| M8.5 | TPCTC 2021 (proc. 2022, pp. 81–97) — orchestration, per-phase timeouts | 📄 — you are the authority |
| (none) | TPCTC 2020 (proc. 2021, pp. 75–92) — currently cited by no guideline | — |

## Listed in Sources, cited by no guideline
- Huppler 2009 `huppler2009art` [M], SIGMOD Reproducibility
  `sigmodreproducibility` [C], Erdelt TPCTC 2020. See the usage section of the
  multi map for where each could be attached.

---

## What's verified vs. still to do

**Confirmed in S5:** NIST §1.3.5 page read directly.

**Confirmed in S4 (your upload):** Manolescu & Manegold slides 45–53, plus slides for M2.4, M4.3, M6.3.

**Confirmed in S3:** Kalibera & Jones sections; TPC-C Clause 6; van der Kouwe et al.
2020 metadata and flaw codes; Leitner & Cito sections and tables (with a content
correction to M5.6); Tene recording URL.

**Still open:** nothing. Every locator cited by the handbook is confirmed.

**Superseded:** the v0.5.0 audit tally no longer applies; v0.8.3 records status
through its labels (26 unmarked, 23 Application, 1 Policy).
