# Plan: research software (FAIR4RS, citability, release gate)

Status: **mostly done.** Planned 2026-11-12, consolidated 2026-11-18, written down here 2026-11-25. DBMS-Benchmarker
is complete (v0.16.0, Zenodo 10.5281/zenodo.24354090). Bexhoma: steps 1, 3-17, 19 done (released in v0.12.0 and
v0.12.1). Open: **2, 2a, 20** (Zenodo, deliberately last), **18** (deferred), and two FAIR4RS points (R3 Python
versions, I1 result formats). The self-assessment with its open points is [docs/FAIR4RS.md](../docs/FAIR4RS.md).

Goal: the "Research software" section of the DFG proposal is true for Bexhoma and DBMS-Benchmarker: CI and
coverage, Zenodo DOIs, CITATION.cff, a release gate, contract, validator and result format released separately,
third-party licences documented, written authorship rules.

## Decisions (user)

- Licence: AGPL-3.0 for both tools, including the validator. The specifications (contract schemas, result
  format, their docs, the handbook except quotations) are CC BY 4.0, so other tools can adopt them. Consent of
  contributor Leonhard Liu obtained 2026-11-21; he is co-author of the handbook and a contributor of Bexhoma.
- Release gate, two levels. Performance numbers vary strongly: reported, never a gate.
  - Every PR and release: unit tests and the collector validations on the zipped results in `tests/validations/`
    (no exceptions, non-empty DataFrames, important columns present).
  - Minor releases (x.y.0) only: the reference set (about 10 runs, `scripts/test-reference-experiments.sh`) is
    rerun on the cluster, every log `passed` and recorded with that version. Patch releases skip it.
- No value-level comparison of evaluation output as a gate: the output changes often and on purpose, an
  unplanned change cannot be told apart. How to detect unplanned value changes stays open; the proposal does
  not promise it.
- No Zenodo archive of raw results for the gate. Publishing results is optional and follows
  [docs/Publishing-Results.md](../docs/Publishing-Results.md) (systems whose licence forbids it get the
  specification only).
- No CHANGELOG: plain GitHub generated release notes. A PR that changes numbers (units, aggregation, formulas,
  rounding, timers, renamed metrics) names the metrics in its description.
- Versioning: minor = what an experiment executes changes (contracts, result format, collectors, images);
  patch = everything else, including evaluation bug fixes (docs/CONTRIBUTING.md).
- Models: the software accepts every model and records its provenance; the project itself uses open-weight
  models only (a sentence in the proposal, not a check in the code).

## Steps

| # | Step | State |
|---|---|---|
| 1 | `CITATION.cff` (ORCID, preferred citation TPCTC 2021) | done |
| 2 | Zenodo: `.zenodo.json`, GitHub integration, concept DOI badge in README | **open, last** |
| 2a | `.gitattributes`: `export-ignore` for `dev/`, `TPCTC23/`, `notebooks/` (release zip ~175 MB -> ~70 MB; images/ and logs_tests/ stay); check on the first archived release that Zenodo's zip honours it | **open, with 2** |
| 2b | `dev/validations/` -> `tests/validations/` (before 2a, else the archive loses the test inputs) | done |
| 3 | `codemeta.json`, SPDX `AGPL-3.0-or-later` and docs URL in `pyproject.toml` | done |
| 4 | release notes instead of a CHANGELOG (decision above) | done |
| 5 | versioning policy | done |
| 6 | protect `master` (PR + green tests), PR template, CODEOWNERS | done |
| 7 | CONTRIBUTING, AUTHORS, authorship and rights policy | done |
| 8 | `THIRD_PARTY.md`; images carry `/licenses/` and the TPC EULA legend; SQL Server tools installed at start, not redistributed | done |
| 9 | coverage in CI with a floor (`fail_under` in `pyproject.toml`) | done |
| 10 | DBMS-Benchmarker test suite and workflow | done |
| 11 | FAIR4RS self-assessment, [docs/FAIR4RS.md](../docs/FAIR4RS.md) | done |
| 12 | reference set of about 10 runs (publishable DBMS only) | done |
| 13 | collector validations as pytest in CI, from `tests/validations/` (TPC-DS, SSB, hardware added in #900) | done |
| 14 | publish workflow depends on the tests | done |
| 15 | release gate job: tag equals `v<__version__>`; for x.y.0 `demo-runs.py --release-gate` | done |
| 16 | release checklist in docs | done |
| 17 | performance table of the reference set for release notes (`demo-runs.py --performance-table`), no thresholds | done |
| 18 | contract specifications, validator, result format as separately versioned packages with their own DOIs | **deferred** |
| 19 | model provenance in trajectories, reports and `agent_summary.yml` | done |
| 20 | experiment specifications in a Zenodo community; the rule part is done (Publishing-Results.md) | **open, with 2** |

## Open

### Zenodo (2, 2a, 20)

Done last, by the user's choice. Order: 2a first (it shrinks every later archive), then `.zenodo.json`
(creators, contributors, licence, keywords; DBMS-Benchmarker's file is the template), the GitHub integration,
the first archived release, the DOI badge, then the DOI in `CITATION.cff` and `codemeta.json`. Closes FAIR4RS
F1, F1.2, F3 and A2. Step 20: a Zenodo community for experiment specifications, after the first DOI.

### Step 18: separate specifications (deferred)

Recommended earlier, not decided: **option B**, a Zenodo upload per contract version from the release
workflow, plus JSON Schemas for `experiment.yaml` and the result folder (closes FAIR4RS I1 on the Bexhoma side)
and one `bexhoma validate` command.

There are three validators today:
1. `validate_experiment.py` (root): thin CLI over `bexhoma/spec.py`, contract level.
2. `agent/harness/validation.py`: a superset that adds handbook principles and a JSON verdict, already
   `bexhoma validate`.
3. `bexhoma/benchmarks/tpch/loader.validate_experiment_yaml`: an older partial check, not catalog-based.

Proposal: `bexhoma validate --contract-only` and full; fold (3) into the contract level; the method level
belongs with the handbook.

Decisions needed:
- option A, B or C;
- split the generic specification (concepts, experiment schema, result structure and validity) from Bexhoma's
  catalog instance (workloads, systems), or not;
- one DOI or two;
- how the proposal describes the validator.

### FAIR4RS points without a step

- R3: CI tests Python 3.10 and 3.12; add more versions.
- I1: the result folder's formats (pickle files, configuration as Python literals) come from DBMS-Benchmarker;
  see its FAIR4RS page.
