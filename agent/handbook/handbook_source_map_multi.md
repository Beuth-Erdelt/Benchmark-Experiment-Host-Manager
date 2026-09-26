# Handbook source map — multi-source — handbook v0.8.3

Companion to `handbook_source_map.md`. Lists **every** source the v0.8.3 handbook
cites for each guideline, primary first, exactly as cited inline. Supersedes the
v0.6.1 multi map.

**Legend**
- Evidence type after each key: [E] empirical, [M] peer-reviewed methodology,
  [T] textbook/reference, [S] standard, [C] commentary/practitioner, [O] own work.
- Label: blank = summarizes source; A = Application; P = Policy.
- Every guideline citing a [C] source also cites a non-[C] source.

---

## M1 — The claim
| ID | Label | Sources (primary first) |
|----|----|----|
| M1.1 | A | `nist_ehandbook` §5.3.1 [T], `ledgerwood2018` [C], `jain1991art` §2.1 [T] |
| M1.2 | A | `jain1991art` §2.1 [T], `mytkowicz2009wrong` causal analysis [E] |
| M1.3 | A | `nosek2018preregistration` [M], `ledgerwood2018` [C], `kalibera2013rigorous` §4 [E], `nist_ehandbook` §1.3.5 [T] |
| M1.4 | A | `nist_ehandbook` §§5.3.1, 5.3.3 [T], `jain1991art` §2.1 [T] |
| M1.5 | A | `nist_ehandbook` §5.3.2 [T], `gray1993benchmark` ch. 1 §1.3, p. 5 [T] |
| M1 pitfalls | | `nosek2018preregistration` [M]; `gray1993benchmark` ch. 1 §1.5, p. 8 [T], `raasveldt2018fair` §§1, 2.2 [M] (benchmarketing) |

## M2 — Factors and controls
| ID | Label | Sources (primary first) |
|----|----|----|
| M2.1 | | `nist_ehandbook` §§5.3.3.3, 5.3.3.4.3 [T], `jain1991art` §16.3 [T] |
| M2.2 | | `nist_ehandbook` §5.3.3.2 [T], `raasveldt2018fair` §§3.1–3.3 [M] |
| M2.3 | A | `leitnercito2016` §§2, 5.2 [E] |
| M2.4 | | `raasveldt2018fair` §3.2 [M], `vanderkouwe2020flaws` D3 [M], `manolescu2008performance` sl. 40–44 [C] |
| M2.5 | | `raasveldt2018fair` §§3.3, 3.8 [M] |
| M2.6 | | `hoefler2015scientific` Rule 9 [M] |
| M2.7 | A | `nist_ehandbook` 5.5.9.9 (beyond data domain; confirmation) [T], `jain1991art` §15 [T] |
| M2.8 | | `vanderkouwe2020flaws` A1–A3 [M], `heiser_crimes` A1–A2 [C], `raasveldt2018fair` App. A [M] |
| M2.9 | A | `nist_ehandbook` §5.3.2 interaction term [T], `jain1991art` ch. 16 [T] |
| M2 pitfalls | | `raasveldt2018fair` §3.3 (apples vs oranges), §3.4 (over-specific tuning) [M] |

## M3 — The load model
| ID | Label | Sources (primary first) |
|----|----|----|
| M3 intro | | `schroeder2006open` [E] |
| M3.1 | | `schroeder2006open` guiding principles [E] |
| M3.2 | A | `schroeder2006open` [E], `wrk2` [C] |
| M3.3 | A | `tpc` §§5.2.5, 5.5 [S] |
| M3.4 | | `schroeder2006open` [E], `tene_latency` [C], `wrk2` latency note [C] |
| M3.5 | | `schroeder2006open` [E] |
| M3.6 | A | `tpc` Clause 6 [S], `erdelt_tpctc23` [O] |

## M4 — Data and state
| ID | Label | Sources (primary first) |
|----|----|----|
| M4.1 | A | `raasveldt2018fair` §§3.5–3.6 [M] (working-set framing is ours) |
| M4.2 | A | `tpc` §3.5 [S] |
| M4.3 | | `raasveldt2018fair` §§3.5–3.6, App. A [M], `manolescu2008performance` sl. 31–35 [C] |
| M4.4 | | `raasveldt2018fair` §3.7 [M] |
| M4.5 | A | `kalibera2013rigorous` §6 [E], `tpc` §5.5 [S], `raasveldt2018fair` App. A [M] |
| M4.6 | | `raasveldt2018fair` §3.8 [M] |

## M5 — Repetition and noise
| ID | Label | Sources (primary first) |
|----|----|----|
| M5.1 | | `kalibera2013rigorous` §§3, 9 [E] |
| M5.2 | | `kalibera2013rigorous` §§1, 4 [E], `hoefler2015scientific` Rule 5 [M], `vanderkouwe2020flaws` B4 [M], `raasveldt2018fair` App. A [M] |
| M5.3 | | `kalibera2013rigorous` §§4, 10 [E], `hoefler2015scientific` Rules 5, 7 [M], `nist_ehandbook` §1.3.5 [T] |
| M5.4 | | `hoefler2015scientific` Rules 6–8 [M] |
| M5.5 | | `kalibera2013rigorous` §§3, 6–9 [E] |
| M5.6 | A | `leitnercito2016` §§5.2.1–5.2.2, Tables 4, 6 [E] |
| M5.7 | | `nist_ehandbook` §§5.3.3.2, 5.1.3 [T], `mytkowicz2009wrong` setup randomization [E] |
| M5 pitfalls | | `mytkowicz2009wrong` [E] |

## M6 — The environment
| ID | Label | Sources (primary first) |
|----|----|----|
| M6.1 | A | `tpc` Clause 6 [S], `erdelt_tpctc23` [O] |
| M6.2 | A | `nist_ehandbook` §5.3.3.2 [T], `leitnercito2016` §§2, 5.2.1 [E] |
| M6.3 | | `raasveldt2018fair` §3.1, App. A [M], `vanderkouwe2020flaws` F1–F2 [M], `tpc` Clause 8 [S], `manolescu2008performance` sl. 149–160 [C] |
| M6.4 | A | `mytkowicz2009wrong` causal analysis [E], `manolescu2008performance` sl. 45–53 [C] |
| M6.5 | | `leitnercito2016` §§2, 5.2 [E] |

## M7 — Metrics
| ID | Label | Sources (primary first) |
|----|----|----|
| M7.1 | | `jain1991art` §3.1 [T], `nist_ehandbook` §5.3.2 [T] |
| M7.2 | | `hoefler2015scientific` §3.1.1, Rules 3–4 [M] |
| M7.3 | | `hoefler2015scientific` Rule 1 [M], `vanderkouwe2020flaws` F4 [M], `nist_ehandbook` §5.3.2 [T] |
| M7.4 | | `hoefler2015scientific` Rule 8 [M], `tene_latency` [C] |
| M7.5 | | `vanderkouwe2020flaws` A2, F3 [M], `heiser_crimes` A2, E2 [C] |
| M7.6 | A | `vanderkouwe2020flaws` B1 [M], `heiser_crimes` B1 [C] |
| M7.7 | | `vanderkouwe2020flaws` B2–B3 [M], `heiser_crimes` B2–B3 [C] |
| Verdict procedure | P | `heiser_crimes` A2, E2 [C], `hoefler2015scientific` [M] (background only) |

## M8 — Feasibility
| ID | Label | Sources (primary first) |
|----|----|----|
| M8.1 | A | `nist_ehandbook` §§5.1.3, 5.3.3 [T] |
| M8.2 | A | `nist_ehandbook` §5.3.3 [T], `kalibera2013rigorous` §9 [E], `jain1991art` §16.3.3 [T] |
| M8.3 | A | `raasveldt2018fair` §§3.6–3.7 [M] |
| M8.4 | A | `nist_ehandbook` §§5.1.3, 5.3.3 [T], `jain1991art` Box 2.1 [T] |
| M8.5 | P | `erdelt_tpctc21` [O] (implementation background) |
| Follow-up procedure | P | `nist_ehandbook` §§5.3.1, 5.3.3 [T] (background only) |

---

## Source usage — primary vs. secondary-only

**Primary for ≥1 guideline** (count of guidelines):
- `nist_ehandbook` [T] — 12: M1.1, M1.4, M1.5, M2.1, M2.2, M2.7, M2.9, M5.7, M6.2, M8.1, M8.2, M8.4
- `raasveldt2018fair` [M] — 8: M2.4, M2.5, M4.1, M4.3, M4.4, M4.6, M6.3, M8.3
- `hoefler2015scientific` [M] — 5: M2.6, M5.4, M7.2, M7.3, M7.4
- `kalibera2013rigorous` [E] — 5: M4.5, M5.1, M5.2, M5.3, M5.5
- `schroeder2006open` [E] — 4: M3.1, M3.2, M3.4, M3.5
- `tpc` [S] — 4: M3.3, M3.6, M4.2, M6.1
- `vanderkouwe2020flaws` [M] — 4: M2.8, M7.5, M7.6, M7.7
- `leitnercito2016` [E] — 3: M2.3, M5.6, M6.5
- `jain1991art` [T] — 2: M1.2, M7.1
- `nosek2018preregistration` [M] — 1: M1.3
- `mytkowicz2009wrong` [E] — 1: M6.4
- `erdelt_tpctc21` [O] — 1: M8.5 (Policy)

Total 50.

**Secondary-only** (supporting, never primary):
- `vanderkouwe2020flaws` also secondary on M2.4 (D3), M5.2 (B4), M6.3 (F1–F2), M7.3 (F4)
- `kalibera2013rigorous` also secondary on M1.3 (§4), M8.2 (§9)
- `jain1991art` also secondary on M1.1, M1.4, M2.1, M2.7, M2.9, M8.2, M8.4
- `gray1993benchmark` [T] — M1.5, M1 pitfalls
- `heiser_crimes` [C] — M2.8, M7.5, M7.6, M7.7, verdict procedure (origin of the crimes list)
- `ledgerwood2018` [C] — M1.1, M1.3
- `tene_latency` [C] — M3.4, M7.4 (origin of "coordinated omission")
- `wrk2` [C] — M3.2, M3.4
- `manolescu2008performance` [C] — M2.4, M4.3, M6.3, M6.4
- `erdelt_tpctc23` [O] — M3.6, M6.1

**Listed in Sources but cited by no guideline** — decide to cite or drop:
- `huppler2009art` [M] — candidate secondary for M1.5 (benchmark relevance) or M2.8.
- `sigmodreproducibility` [C] — candidate secondary for M6.3.
- `erdelt_tpctc20` [O] — candidate implementation background for M5.1/M5.5
  (repetition and evaluation framework), labelled as such.

**Dropped since v0.6.1:** `kounev2020systems`, `kistowski2015benchmark` (never in
either handbook's Sources); `vanderkouwe2018crimes` now only as the preprint of
`vanderkouwe2020flaws`.

## Observations
- NIST is now the most-used primary. That is appropriate for design-of-experiments
  rules (blocking, factorial design, confounding, objectives), but 9 of its 12
  primaries are Application rules: NIST supports the statistical principle, and
  the benchmarking-specific wording is ours. Where a benchmarking source makes
  the same point, it is listed as secondary.
- Every [C] source is paired with a peer-reviewed or reference source; no
  guideline rests on commentary alone.
- Empirical primaries ([E]) keep their original scope: Leitner & Cito (studied
  providers), Schroeder (studied systems), Mytkowicz (studied architectures and
  compilers).

## BibTeX stubs for new keys

All metadata verified against publisher or repository records.

```bibtex
@misc{nist_ehandbook,
  author       = {{NIST/SEMATECH}},
  title        = {e-Handbook of Statistical Methods},
  howpublished = {\url{https://www.itl.nist.gov/div898/handbook/}},
  note         = {Sections 1.3.5, 5.1.3, 5.3.1--5.3.3.4.3, 5.5.9.9}
}

@article{nosek2018preregistration,
  author  = {Nosek, Brian A. and Ebersole, Charles R. and DeHaven, Alexander C. and Mellor, David T.},
  title   = {The preregistration revolution},
  journal = {Proceedings of the National Academy of Sciences},
  volume  = {115},
  number  = {11},
  pages   = {2600--2606},
  year    = {2018},
  doi     = {10.1073/pnas.1708274114}
}

@article{ledgerwood2018,
  author  = {Ledgerwood, Alison},
  title   = {The preregistration revolution needs to distinguish between predictions and analyses},
  journal = {Proceedings of the National Academy of Sciences},
  volume  = {115},
  number  = {45},
  pages   = {E10516--E10517},
  year    = {2018},
  doi     = {10.1073/pnas.1812592115}
}

@article{vanderkouwe2020flaws,
  author  = {van der Kouwe, Erik and Heiser, Gernot and Andriesse, Dennis and Bos, Herbert and Giuffrida, Cristiano},
  title   = {Benchmarking Flaws Undermine Security Research},
  journal = {IEEE Security \& Privacy},
  volume  = {18},
  number  = {3},
  pages   = {48--57},
  year    = {2020},
  doi     = {10.1109/MSEC.2020.2969862},
  note    = {Preprint: arXiv:1801.02381}
}

@misc{wrk2,
  author       = {Tene, Gil},
  title        = {wrk2: A constant throughput, correct latency recording variant of wrk},
  howpublished = {\url{https://github.com/giltene/wrk2}},
  note         = {README, note on latency measurement and coordinated omission}
}
```
