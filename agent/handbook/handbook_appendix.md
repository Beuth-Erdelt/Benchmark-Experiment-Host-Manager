# Experiment Design Handbook — Appendix and Sources

    handbook_version: "0.8.4"

Companion to `handbook.md`. The method chapters M1–M8 live there; this file
holds the local agent interface and the full source list, which the method
chapters cite but do not need in order to be applied.

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
