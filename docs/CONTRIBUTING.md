# Contributing to Bexhoma

Contributions are welcome. Areas where help is most useful:

- **New workloads** — a benchmark is one folder `bexhoma/benchmarks/<name>/`, plus its scripts in `experiments/`, job templates in `k8s/` and Docker images in `images/`, see [Adding a Benchmark](Adding-a-Benchmark.md).
- **New DBMS** — a DBMS is added by configuration: an entry in the `dockers` section of the cluster configuration, a deployment manifest in `k8s/` and DDL scripts in `experiments/`, see [Adding a DBMS](Adding-a-DBMS.md).
- **Bug fixes and testing** — report bugs via the [issue tracker](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/issues) or open a pull request.
- **Documentation** — corrections, clarifications, and new examples are all welcome.

[Architecture](Architecture.md) shows how the code is organised and where a change belongs.

---

## Pull requests

- `master` is always the latest stable release; nobody pushes to it directly. `dev` tracks ongoing development.
- Branch off from `dev` with a short descriptive name (`feature/ycsb-redis`, `fix/loader-encoding`).
- Open your pull request against `dev`, not `master`.
- Keep each PR focused on one change. Unrelated fixes belong in a separate PR.
- Reference the relevant issue number in the PR description where applicable.
- The description starts from the [pull request template](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/.github/PULL_REQUEST_TEMPLATE.md); its checklist asks for tests, cluster runs, changed metrics, the type of change for the next release and third-party material.
- Every pull request requests a review from the maintainer (`.github/CODEOWNERS`).
- Make sure all checks pass (see [Testing](#testing)) and review feedback is resolved before merging.
- PRs are merged into `dev` via **squash merge**.
- By submitting a PR you agree to license your contribution under the **GNU Affero General Public License v3.0 or later** (AGPL-3.0-or-later).
- Changes are recorded in the notes of the [GitHub releases](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/releases), which are generated from the pull requests. So give each pull request a title that says what changes for users.
- If a change alters measured or evaluated numbers, the pull request names the affected metrics: units, aggregation, formulas, rounding, what a timer measures, renamed metrics or columns.

---

## Versions and releases

Versions have the form `MAJOR.MINOR.PATCH`; git tags have the form `vMAJOR.MINOR.PATCH`, and the Docker images of a release are tagged `MAJOR.MINOR.PATCH` and `latest`.
While the major version is 0, a minor release may contain incompatible changes; they are named in their pull requests.

- **Minor release** (`X.Y.0`): changes what an experiment executes or records. This includes the catalog and result contracts, the result format, collectors, the Docker images and Kubernetes manifests, and the meaning of command line options.
- **Patch release** (`X.Y.Z`): everything else, including bug fixes in evaluations and reports, and documentation. If a fix changes evaluated numbers, its pull request names the affected metrics.

### Release checklist

1. Set the version with `python bump_version.py X.Y.Z`; it writes `bexhoma/__version__.py`, `CITATION.cff` and `codemeta.json`, and the tests check that they agree.
2. If the release needs a newer DBMS-Benchmarker, raise its minimum version in `requirements.txt`.
3. For a minor release only: run the reference experiments with the release candidate installed, `scripts/test-reference-experiments.sh` (or `.ps1`). They are one experiment per benchmark on PostgreSQL, plus monitoring, application monitoring and persistent storage, taken from the `test-docs-*` scripts; `BEXHOMA_PARALLEL` sets how many run at the same time (default 4). The script checks every log for passed and no failed tests and for the release version, and ends with `all passed with bexhoma X.Y.Z`. Their logs replace those of the documentation in `logs_tests/` and are committed with the release. `python scripts/demo-runs.py --performance-table` prints the key metrics of their benchmarking phases as a Markdown table; add it to the release notes. The numbers are reported for comparison with earlier releases, not checked: performance varies between runs.
4. Merge `dev` into `master` by a pull request and create a GitHub release with the tag `vX.Y.Z`. Use *Generate release notes*. Publishing uploads the package to PyPI, but only if the tests pass, the tag equals the package version and, for `X.Y.0`, every reference log in `logs_tests/` passed with that version (`python scripts/demo-runs.py --release-gate X.Y.Z`). The pull request into `master` runs the same check as an informational job (`release-gate`, it never blocks the merge), so it shows before the merge whether the release would publish. Run that check again before creating the release; a release whose upload was refused stays published on GitHub without package.
5. Build and push the images with `scripts/build.sh` (or `scripts/build.ps1`) in an environment where the release is installed (`pip install -e .`): they are tagged with the installed Bexhoma version and `latest`, and the DBMS-Benchmarker images get the installed DBMS-Benchmarker version. The licence texts of their components must be up to date (see [images/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/images/README.md)).

---

## Code style

Bexhoma follows [PEP 8](https://peps.python.org/pep-0008/) and [PEP 257](https://peps.python.org/pep-0257/). These rules apply to the Python code you write or change. [Ruff](https://docs.astral.sh/ruff/) checks part of them in CI (rules and version in `pyproject.toml` and `.github/workflows/tests.yml`); run it before a pull request:

```bash
pip install ruff==0.17.6
ruff check bexhoma agent experiment.py
```

Existing findings carry a `# noqa: <rule>` comment so that only new code fails; do not add such comments to new code, fix it instead. Line length (120) is not checked yet. Older code does not follow all of the rules (line length, f-strings, `__all__`, type annotations); do not reformat code you do not otherwise touch, and put clean-ups in their own pull request. When cleaning up existing code: do not change logic or public names (classes, public methods, public attributes), verify that all references (imports, call sites, attribute accesses) still resolve correctly after the change, and check how similar things are already done elsewhere in the codebase before introducing a new pattern.

**Naming**
- `snake_case` for functions, methods, and variables; `PascalCase` for classes; `UPPER_CASE` for constants.
- No single-letter names except `i`/`j` in simple index loops and `_` for discards. Never use `l`, `O`, or `I`.
- No opaque abbreviations; `df_aggregated` is fine, `x` is not.
- Do not shadow built-ins (`type`, `id`, `list`, `input`).
- Propose clearer and consistent method names when existing names are unclear, inconsistent, or do not follow a unified convention across the codebase.

**Formatting**
- 4-space indentation, maximum 79-character lines.
- Two blank lines between top-level definitions; one blank line between methods.

**Idioms**
- `if x is None` / `if x is not None` — not `== None`, never `if not x is None`.
- `with open(...) as f:` — not bare `open()/close()`.
- `dict.get(key, default)` instead of `if key in dict` guard patterns.
- Prefer early returns over deeply nested `if` blocks.
- Remove unused imports.
- No always-true guards (`if True:`); flatten the body.
- Use f-strings consistently; do not mix with `%` or `.format()`.
- Delete commented-out code that is not documentation; when removing a
  commented-out code block, also remove any comment whose sole purpose was
  to describe what that dead code did.
- Triple-quoted strings used as block comments or section separators are
  dead strings, not docstrings; replace with a `# Section name` line or
  delete.
- No always-constant variables used to gate output (`silent = False` that
  is never changed); flatten the conditional directly.
- Deprecated methods that are kept for reference must be prefixed `OLD_`
  (e.g. `OLD_evaluate_results`), not suffixed or left with an ambiguous
  name.
- Never use bare `except:`; always catch specific exception types.
- Extract unexplained numeric and string literals into named constants.

**Docstrings (PEP 257 + Sphinx)**

Documentation is generated with Sphinx. Every public module, class, and method must have a docstring using Sphinx-style annotations; private helpers (`_name`) need at minimum a one-line docstring.

```python
def my_method(self, param='default'):
    """
    One-line summary.

    :param param: What this controls.
    :type param: str
    :return: What is returned.
    :rtype: pandas.DataFrame
    """
```

**Type annotations**
- Annotate method parameters and return types whenever the type can be
  confidently inferred from context, usage, or existing docstrings.
- Use built-in generics (`list[str]`, `dict[str, int]`) over `typing`
  aliases where Python version allows.

**Attributes**
- Declare all instance attributes in `__init__` before first use.
- Do not create attributes dynamically outside `__init__`.
- Define `__all__` in every module to make the public API explicit.

**Comments**
- Comment when the WHY is non-obvious: a hidden constraint, a workaround,
  a subtle invariant.
- Add a short WHAT comment to introduce important sections whose purpose
  is not immediately obvious from the surrounding code structure.
- Do not comment self-explanatory code — names should be sufficient.

---

## Brand assets

The logo, icons and brand colours are in `docs/logo/`, licensed under CC BY 4.0, separately from the code; see the [logo README](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/docs/logo/README.md), which also says where they are referenced.

---

## AI-assisted contributions

Using a code copilot (GitHub Copilot, Claude, etc.) to write or review code is fine and encouraged — as long as you review the output and ensure it meets the style and correctness requirements above.

---

## Testing

New features and bug fixes must include a test.

### Running the tests locally

Install the requirements, pytest and the `agent` extra (the agent tests import its packages), then run the suite from any directory:

```bash
pip install -r requirements.txt pytest "coverage[toml]>=7.10" -e ".[agent]"
python -m pytest tests
```

No Kubernetes cluster is needed. On Windows, a few tests that need a POSIX shell are skipped; CI runs them on Linux.

### Checks of a pull request

Every pull request runs two workflows; neither needs a Kubernetes cluster.

- `tests.yml`: ruff (see Code style), and the unit tests in `tests/` on Python 3.10 (the oldest that `pyproject.toml` allows) and 3.12, `python -m pytest tests` (one file: `python -m pytest tests/test_cli.py`). They build experiments against a stub cluster (`tests/stubs.py`) and include the collector validations on the archived results in `tests/validations/` (`scripts/validate_collector_*.py --zips`, see [scripts/README.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/scripts/README.md)). The workflow also measures the test coverage of `bexhoma` and `agent`, which must not fall below the floor in `pyproject.toml` (`python -m coverage run -m pytest tests`, then `python -m coverage combine` and `python -m coverage report`), on 3.12. On a pull request into `dev` it also reports the coverage of the changed lines (`diff-cover`, 80%); this does not fail the build yet.
- `demo-runs.yml`: `logs_tests/SUMMARY.md` and the badge file match the committed logs. After committing logs, run `python scripts/demo-runs.py` and commit both files.

A pull request into `master` also runs the job `release-gate` of `tests.yml`. It shows whether the merge would qualify for a release, see the [release checklist](#release-checklist), and never blocks the merge.

### When a test fails

Some tests compare the code with recorded data. A deliberate change is accepted by updating that data in the same pull request:

| Test | Fails when | Deliberate change |
|---|---|---|
| `test_dbms_snapshots.py` | an entry script builds a different experiment than recorded in `tests/snapshots/` | `BEXHOMA_UPDATE_SNAPSHOTS=1 python -m pytest tests/test_dbms_snapshots.py`, then review the diff of `tests/snapshots/` |
| `test_no_dbms_in_python.py`, `test_no_benchmark_in_generic.py` | a file names a DBMS or a benchmark more (or less) often than its baseline in `tests/` allows | more: move the detail to `cluster.config`'s `dockers:` section or the benchmark's folder `bexhoma/benchmarks/<name>/`; less: shrink the baseline with `BEXHOMA_UPDATE_SNAPSHOTS=1` and the same test |
| `test_benchmark_contract.py` | a benchmark folder lacks something generic code relies on: classes, asset folder, job templates, summary tables, entry script shim | complete the folder, see [Adding a Benchmark](Adding-a-Benchmark.md#tests) |
| `test_system_descriptors.py` | an entry in `dockers` of `k8s-cluster.config` is invalid, its job template is missing, or a local `cluster.config` declares other `benchmarks`, `base_system` or aliases | fix the entry; add a new DBMS to both files |
| `test_reset_scripts.py` | a DBMS that an entry script offers has no reset scripts for `-ar` | add them, or list the DBMS in `NO_RESET` |
| `test_naming_conformance.py` | `contracts/contract_result.yml` or `contract_catalog.yml` and the code disagree, e.g. on the contract version or the naming of result folders | change both together; a new contract version also goes into `report_writer.SCHEMA_VERSION` or `spec.CATALOG_CONTRACT_VERSION` |
| `test_collector_validations.py` | a collector gives other results for an archived run | after a new run of `test-docs-collector`, commit the new zips of `tests/validations/` |
| `test_reference_experiments.py` | a command of a `test-docs-*` script differs from its copy in `scripts/test-reference-experiments.sh` / `.ps1` | copy the changed command |
| `test_unpublished_results.py` | `logs_tests/` contains results of a DBMS that must not be published | keep them in the git-ignored `logs_tests/local/`, see [Publishing Results](Publishing-Results.md) |
| `test_metadata.py` | the version differs between `bexhoma/__version__.py`, `CITATION.cff` and `codemeta.json` | `python bump_version.py X.Y.Z` |

### On a cluster

The examples of the documentation are produced by the `scripts/test-docs-*.sh` / `.ps1` scripts, listed in [TestCases](TestCases.md); `scripts/test-reference-experiments.sh` / `.ps1` runs one experiment per benchmark for a release. If a change affects experiment execution, run the relevant scripts against a live Kubernetes cluster before submitting. They write their logs to `logs_tests/`; link a representative log in your PR.

---

## Third-party material

If your contribution includes material from others (code, images, queries, data, JDBC drivers or tools built into an image), add it to [THIRD_PARTY.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/THIRD_PARTY.md) with its source and licence.

---

## Publishing results

Results of some DBMS must not be published, and result folders contain credentials and names of the infrastructure. Follow [Publishing Results](Publishing-Results.md) before committing logs or publishing results, and when adding a DBMS.

---

## Authorship

Bexhoma distinguishes authors from contributors, see [AUTHORS.md](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/AUTHORS.md).

- **Authors** made a scientific contribution: the concept or method, the design of benchmark experiments, measurements or evaluations. They are named in the citation metadata.
- **Contributors** made other contributions, such as implementation, maintenance, bug fixes, documentation or tests. They are acknowledged in `AUTHORS.md`.

For work done within a funded project, authorship and rights are agreed in writing at the start of the project.
