# Handbook source map — handbook v0.8.3

One primary source per guideline (M1.1–M8.5, 50 guidelines), for citing each
entry. Regenerated against `experiment_design_handbook_v0.8.3.md`; supersedes the
v0.4.0–v0.6.1 maps. For all sources per guideline see
`handbook_source_map_multi.md`; for locators, anchor quotes and verification
status see `handbook_source_quotes.md`.

**Columns**
- **Label** — as in the handbook: blank = summarizes the source; **A** =
  Application (our deduction; the source supports the principle, not
  necessarily the exact wording); **P** = Policy (operating choice, not a
  literature finding).
- **Type** — evidential type of the primary: [E] empirical study, [M]
  peer-reviewed methodology/position paper, [T] textbook or reference work,
  [S] standard, [C] commentary/practitioner, [O] author's own work.
- **Primary** — the first source the handbook cites for the rule; the one to
  cite if you cite only one.

Tally: 26 unmarked, 23 Application, 1 Policy. Primaries by type: 18 [M],
14 [T], 13 [E], 4 [S], 1 [O] (the Policy rule M8.5). No primary is a [C]
source. Per-source counts are in the usage section of the multi map.

---

## M1 — The claim
| ID | Label | Rule (short) | Primary (locator) | Type | key |
|----|----|----|----|----|----|
| M1.1 | A | Answerable objective; refutable hypothesis | NIST §5.3.1 | T | `nist_ehandbook` |
| M1.2 | A | Rival explanations for causal questions | Jain §2.1 | T | `jain1991art` |
| M1.3 | A | Confirmatory criterion fixed in advance | Nosek et al. 2018 | M | `nosek2018preregistration` |
| M1.4 | A | Measurement / comparison / explanation | NIST §§5.3.1, 5.3.3 | T | `nist_ehandbook` |
| M1.5 | A | Question the instrument can answer | NIST §5.3.2 | T | `nist_ehandbook` |

## M2 — Factors and controls
| ID | Label | Rule (short) | Primary (locator) | Type | key |
|----|----|----|----|----|----|
| M2.1 | | Identifiable design; state aliasing | NIST §§5.3.3.3, 5.3.3.4.3 | T | `nist_ehandbook` |
| M2.2 | | Hold equal or block/randomize | NIST §5.3.3.2 | T | `nist_ehandbook` |
| M2.3 | A | Opportunistic shared resources | Leitner & Cito §§2, 5.2 | E | `leitnercito2016` |
| M2.4 | | Comparable, disclosed tuning | Raasveldt §3.2 | M | `raasveldt2018fair` |
| M2.5 | | Equivalent work, verified results | Raasveldt §§3.3, 3.8 | M | `raasveldt2018fair` |
| M2.6 | | Declared factors = varied factors | Hoefler & Belli Rule 9 | M | `hoefler2015scientific` |
| M2.7 | A | Conclude only at tested levels / declared model | NIST 5.5.9.9 (beyond the data domain) | T | `nist_ehandbook` |
| M2.8 | | Cover where the change might harm | van der Kouwe et al. 2020, A1–A3 | M | `vanderkouwe2020flaws` |
| M2.9 | A | Interactions limiting a resource increase | NIST §5.3.2 (interaction term) | T | `nist_ehandbook` |

## M3 — The load model
| ID | Label | Rule (short) | Primary (locator) | Type | key |
|----|----|----|----|----|----|
| M3.1 | | Load model follows the population | Schroeder et al. (guiding principles) | E | `schroeder2006open` |
| M3.2 | A | Offered vs achieved; cap ≠ capacity | Schroeder et al. | E | `schroeder2006open` |
| M3.3 | A | Sustainability criteria; highest passing level | TPC-C 5.11 §§5.2.5, 5.5 | S | `tpc` |
| M3.4 | | Coordinated omission; intended send time | Schroeder et al. | E | `schroeder2006open` |
| M3.5 | | Population/think time or arrival process | Schroeder et al. | E | `schroeder2006open` |
| M3.6 | A | Generator not the bottleneck | TPC-C 5.11, Clause 6 | S | `tpc` |

## M4 — Data and state
| ID | Label | Rule (short) | Primary (locator) | Type | key |
|----|----|----|----|----|----|
| M4.1 | A | Memory regime; working set | Raasveldt §§3.5–3.6 | M | `raasveldt2018fair` |
| M4.2 | A | Storage path actually exercised | TPC-C 5.11 §3.5 | S | `tpc` |
| M4.3 | | Declared cache state and procedure | Raasveldt §§3.5–3.6, App. A | M | `raasveldt2018fair` |
| M4.4 | | Preparation cost, incl. automatic | Raasveldt §3.7 | M | `raasveldt2018fair` |
| M4.5 | A | Measure the interval the question is about | Kalibera & Jones §6 | E | `kalibera2013rigorous` |
| M4.6 | | Correctness before speed; incomplete work | Raasveldt §3.8 | M | `raasveldt2018fair` |

## M5 — Repetition and noise
| ID | Label | Rule (short) | Primary (locator) | Type | key |
|----|----|----|----|----|----|
| M5.1 | | Repeat at relevant levels for precision | Kalibera & Jones §§3, 9 | E | `kalibera2013rigorous` |
| M5.2 | | Uncertainty; observation spread vs estimate | Kalibera & Jones §§1, 4 | E | `kalibera2013rigorous` |
| M5.3 | | Intervals on the effect; equivalence margin | Kalibera & Jones §§4, 10 | E | `kalibera2013rigorous` |
| M5.4 | | No normality assumption; summary by question | Hoefler & Belli Rules 6–8 | M | `hoefler2015scientific` |
| M5.5 | | Repeat where variation lives; dependence | Kalibera & Jones §§3, 6–9 | E | `kalibera2013rigorous` |
| M5.6 | A | Within vs between allocation, not assumed | Leitner & Cito §§5.2.1–5.2.2, Tables 4, 6 | E | `leitnercito2016` |
| M5.7 | | Randomize or block measurement order | NIST §5.3.3.2 | T | `nist_ehandbook` |

## M6 — The environment
| ID | Label | Rule (short) | Primary (locator) | Type | key |
|----|----|----|----|----|----|
| M6.1 | A | Generator placement disclosed/checked | TPC-C 5.11, Clause 6 | S | `tpc` |
| M6.2 | A | Control placement (pin, pair, block, randomize) | NIST §5.3.3.2 | T | `nist_ehandbook` |
| M6.3 | | Disclose sufficiently to reproduce | Raasveldt §3.1, App. A | M | `raasveldt2018fair` |
| M6.4 | A | Monitoring tests plausibility, not cause | Mytkowicz et al. (causal analysis) | E | `mytkowicz2009wrong` |
| M6.5 | | Declared tenancy as variation | Leitner & Cito §§2, 5.2 | E | `leitnercito2016` |

## M7 — Metrics
| ID | Label | Rule (short) | Primary (locator) | Type | key |
|----|----|----|----|----|----|
| M7.1 | | Define metric; record constituents | Jain §3.1 | T | `jain1991art` |
| M7.2 | | Aggregate totals; correct mean type | Hoefler & Belli §3.1.1, Rules 3–4 | M | `hoefler2015scientific` |
| M7.3 | | Absolutes behind every ratio | Hoefler & Belli Rule 1 | M | `hoefler2015scientific` |
| M7.4 | | Named percentiles for tail questions | Hoefler & Belli Rule 8 | M | `hoefler2015scientific` |
| M7.5 | | Per-component results; opposing trends | van der Kouwe et al. 2020, A2, F3 | M | `vanderkouwe2020flaws` |
| M7.6 | A | Microbenchmark ≠ system claim | van der Kouwe et al. 2020, B1 | M | `vanderkouwe2020flaws` |
| M7.7 | | Denominators; % vs percentage points | van der Kouwe et al. 2020, B2–B3 | M | `vanderkouwe2020flaws` |

## M8 — Feasibility
| ID | Label | Rule (short) | Primary (locator) | Type | key |
|----|----|----|----|----|----|
| M8.1 | A | Estimate cost; check feasibility; slack | NIST §5.1.3 | T | `nist_ehandbook` |
| M8.2 | A | Balance levels vs repetitions by precision | NIST §5.3.3 | T | `nist_ehandbook` |
| M8.3 | A | Spend budget on evidence; needed prep isn't waste | Raasveldt §§3.6–3.7 | M | `raasveldt2018fair` |
| M8.4 | A | Most economical design that can refute | NIST §5.1.3 | T | `nist_ehandbook` |
| M8.5 | P | Deadlines; record timeouts | Erdelt TPCTC 2021 (implementation) | O | `erdelt_tpctc21` |

---

## Keys to add to `references.bib`
New in v0.8.0: `nist_ehandbook`, `nosek2018preregistration`, `ledgerwood2018`,
`vanderkouwe2020flaws`, `wrk2`. Carried over and still needed if not yet present:
`tpc`, `leitnercito2016`, `tene_latency`, `heiser_crimes`,
`manolescu2008performance`, `huppler2009art`, `sigmodreproducibility`, and the
Erdelt TPCTC keys (placeholders `erdelt_tpctc20/21/23` — rename to your existing
Bexhoma keys). BibTeX stubs are at the end of `handbook_source_map_multi.md`.

**No longer cited by the handbook:** `kounev2020systems`,
`kistowski2015benchmark`. `vanderkouwe2018crimes` survives only as the preprint
of `vanderkouwe2020flaws`.
