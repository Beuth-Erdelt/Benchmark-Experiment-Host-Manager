# Plan: software quality: lint, docs checks, shared argument checks, CI

Status: written 2026-11-22. **S1, S3, S5, S7 done 2026-11-23** on branch `software-quality-p2` (one branch
for all four, by request; not pushed). Open: S2, S4, S6. Deviations from the text below:
- S1: E501, UP032 and F401 are not selected yet (1,268 findings, fixed in bulk by S2 and then enabled);
  the other 204 findings carry `# noqa`. Ruff runs in its own CI job `lint`.
- S3: the page check is "reachable from the toctree, directly or by links" instead of an exclusion list
  (only `docs/README.md` is exempt); check 3 covers every function the docs name in code style
  (`name()`, `obj.name(args)`) against all definitions in the repository, with a list of SQL/PromQL/library
  names, because names next to source links were only 2. It found 69 `.html` links (broken on GitHub),
  one dead link and two stale names (`get_inspector()`, `_effective_post_load()`), all fixed.
- S5: no CI run yet. Checked locally: ruff with target py310 finds no newer syntax, no 3.11+ standard
  library feature is used, every direct requirement has a 3.10 wheel (`dash-renderer`, a dbmsbenchmarker
  dependency without wheel, prevents an offline resolution of the whole tree).
- S7: reported in the job summary, `continue-on-error` until S2 is done; this branch has 72% diff coverage
  because of the noqa lines. Only on pull requests into `dev`.

Follows the review of CONTRIBUTING and the design docs. The doc fixes, the
TPC-DS/SSB/Hardware collector runs and the threads-per-pod check have been
merged (#898, #900, #899).

Each step is its own branch from `dev` (`--no-track`) and its own PR into `dev`.
None of the steps builds on another, except that S6 is easier after S1.

| Step | What | Size | Risk |
|---|---|---|---|
| S1 | ruff in CI, only new violations fail | small | none, no code change |
| S2 | ruff clean-ups: real bugs first, then mechanical fixes | medium, several PRs | low |
| S3 | docs consistency test | small | none |
| S4 | one argument check for `main()` and the catalog path | small | low |
| S5 | Python 3.10 in CI | small | may find 3.11+ syntax |
| S6 | split `work_benchmark_list()` | large | medium, needs cluster runs |
| S7 | diff coverage | small | none |

## S1: ruff in CI

CONTRIBUTING states style rules in prose and says "No tool checks them yet".
Ruff would check them.

### Measured (ruff 0.17.6, `bexhoma/`, `agent/`, `experiment.py`, 43,555 lines)

Rules that map to CONTRIBUTING, line length 120:

| Rule | Meaning | Count | Auto-fix |
|---|---|---|---|
| E722 | bare `except:` | 0 | |
| E711 | `== None` | 0 | |
| F821 | undefined name | 0 | |
| E741 | ambiguous name `l`, `O`, `I` | 0 | |
| E712 | `== True` / `== False` | 2 | |
| A001 / A002 | shadowed built-in | 1 / 7 | |
| F811 | redefined unused name | 4 | partly |
| UP031 | `%` formatting | 4 | |
| B006 | mutable default argument | 13 | |
| F841 | unused variable | 37 | unsafe |
| F401 | unused import (1 of them in an `__init__`) | 139 | yes |
| UP032 | `.format()` instead of f-string | 389 | yes |
| E501 | line > 120 | 741 | |

E501 at other lengths: 1,783 at 100, 361 at 140. Most long lines are in
`experiments/base.py` (205), `configurations/base.py` (103),
`hardware/cli.py`, `configurations/lifecycle.py` (39 each).

### Plan

1. `[tool.ruff]` in `pyproject.toml`: `line-length = 120`,
   `target-version = "py310"`, `extend-exclude = ["TPCTC23", "docs/_build", "dev"]`.
2. `[tool.ruff.lint] select` = the rules in the table above, plus the defaults
   `E4`, `E7`, `E9`, `F`. Leave out the extended set ruff 0.17 shows with
   `--isolated` (I001, UP045, BLE001, ...); revisit once the code is clean.
3. Enable the four zero-violation rules (E722, E711, F821, E741) right away,
   with no baseline: they guard what is already clean.
4. For the rest, have CI fail only on new violations. Write the current
   violations once as `# noqa` comments (`ruff check --add-noqa`, about 1,340
   comments) or check only the lines a PR changes. Recommended: `--add-noqa`.
   It needs no extra tool and the comments mark exactly what is left to clean,
   and S2 removes them. Weigh this against the noise in `experiments/base.py`.
   If that is too much, use per-file ignores for E501 in the 4 files above
   instead.
5. CI: one more step in `tests.yml`, `pip install ruff==0.17.6`, then
   `ruff check bexhoma agent experiment.py`. Pin the version so a ruff
   release cannot fail a PR.
6. CONTRIBUTING: replace "No tool checks them yet" with how to run ruff
   locally.

Formatter (`ruff format`): not now. It would rewrite almost every file and
make `git blame` useless; maybe later, module by module.

## S2: ruff clean-ups

Separate PRs, purely mechanical, no logic changes mixed in. Each removes the
matching `# noqa` comments from S1.

1. **Real bugs first** (one PR):
   - `experiments/base.py:61-64`: `__all__` names `IotExperiment`,
     `TsbsExperiment`, `TpcxaiExperiment`, which do not exist there (F822).
     `from bexhoma.experiments.base import *` raises.
   - `experiments/base.py:643, 662, 679`: a local `parameter` shadows the
     imported module `parameter` (F811).
   - `experiments/base.py:3718`: a useless expression (B018), probably a
     forgotten assignment or call.
   - `configurations/lifecycle.py:351, 383, 404, 895, 897` and
     `loading.py:790`: `.format()` with unused arguments (F522/F523). Check
     whether the template lost a placeholder.
   - `environment.py:149`: class `EnvironmentError` shadows the built-in
     (A001). Renaming it is an API change; check the callers first.
   - 18 × `datetime.utcnow()` (DTZ003): deprecated since 3.12. Replace with
     `datetime.now(timezone.utc)` only where the naive/aware difference
     cannot reach a comparison or a stored timestamp. Otherwise keep the
     behaviour and only document it.
2. **Unused imports** (F401, 139): `ruff check --select F401 --fix`. Keep
   re-exports in `__init__.py` with `__all__`.
3. **f-strings** (UP032, 389): `--fix`, one subpackage per PR. Review the
   diff: a `.format()` on a template that is read from a file must stay.
4. **Unused variables** (F841, 37) and **mutable defaults** (B006, 13): by
   hand.
5. **Long lines**: last, and only in modules that are being changed anyway.

## S3: docs consistency test

Stale method names in `WorkBenchmarkList.md` and five orphaned pages were found
only by reading. A test, `tests/test_docs_consistency.py`, runs offline:

1. Every `docs/*.md` is in a toctree of `docs/index.rst` or on an explicit
   exclusion list.
2. Every relative link in `docs/*.md` and `README.md` points to an existing
   file, and `#anchor` links point to an existing heading.
3. Every `` `name()` `` that a doc puts next to a link to a source file
   exists in that file. A grep is enough; a full parser is not needed.

Optional, as a separate CI job: `sphinx-build -W -b html docs docs/_build`,
so warnings fail the build. Needs `docs/requirements.txt` installed in CI.
Read the Docs builds without `-W` today.

## S4: one argument check for `main()` and the catalog path

`tenancy_error()` and `threads_per_pod_error()` run only in the entry scripts'
`main()`. The catalog path builds `argv`, parses it and calls `run()` directly,
in two places that duplicate each other:

- `experiment.py:169` (`run_experiment_yaml`)
- `agent/harness/submit.py:95`

So a catalog experiment with an invalid tenancy or a 0-thread split is not
refused. Today the catalog covers only `tpch` and `ycsb`.

Plan:

1. `bexhoma/experiments/system_builder.py`: `argument_error(benchmark, args) -> str`,
   which calls `tenancy_error()` and, for benchmarks with split threads,
   `threads_per_pod_error()` for `-nlt/-nlp` and `-nbt/-nbp` (not for
   hardware `sockperf`). Which benchmarks split threads comes from the
   `BenchmarkDescriptor` (a new field), not from a name list, so
   `test_no_benchmark_in_generic` stays green.
2. Each `main()` calls `argument_error()` instead of its own loop and calls
   `parser.error(reason)`.
3. Each `run()` calls it too and raises `SystemExit(reason)`. Then both
   catalog paths are covered, and so is any other caller.
4. Optional: move the shared argv building of `experiment.py` and `submit.py`
   (`physical_design_overrides`, `apply_sut_resources`) into one function in
   `catalog_spec`, so the two paths cannot drift.
5. Tests: the catalog path with an uneven split and with an invalid tenancy is
   refused; `tests/test_threads_per_pod.py` and `test_tenancy.py` still pass.

## S5: Python 3.10 in CI

`pyproject.toml` says `requires-python = ">=3.10.2"`, and CI tests only 3.12.

1. `tests.yml`: a matrix over `3.10` and `3.12`, with coverage reported only
   for 3.12.
2. If 3.10 fails on 3.11+ syntax or modules (`tomllib`, `ExceptionGroup`,
   `typing.Self`), choose between fixing the code and raising `requires-python`
   to 3.12. The images and the cluster runner use 3.12, so raising it is
   acceptable, but it is a user decision and changes the PyPI metadata.

## S6: split `work_benchmark_list()`

`experiments/base.py` has 3,801 lines. `work_benchmark_list()` starts at line
2728 and is about 500 lines long, although 19 helpers were already moved out
(`_start_sut_or_abort`, `_prepare_next_repetition`, `_submit_round`, ...).

1. One handler per phase of a configuration in a pass: not started → start
   SUT; started, not loaded → loading; loaded → benchmark round; round done →
   end jobs and next repetition; done → stop. The loop only dispatches.
2. Remove the legacy `benchmark_list` path (`_submit_legacy_round`,
   `add_benchmark_list`). All entry scripts already use `experiment_dict`;
   check first that no script in `scripts/` or `dev/` still uses it.
3. Update `docs/WorkBenchmarkList.md` in the same PR (S3 checks it).
4. Verification: unit tests with a stubbed cluster for each handler, then
   `test-docs-*` runs on the cluster: TPC-H, YCSB, one tenancy run and one
   with repetitions. Run them only after the user agrees.

Do it after S1 and S2, so the diff shows logic, not style.

## S7: diff coverage

The coverage floor of 69% (`[tool.coverage.report] fail_under`) only stops
the total from falling. A PR that adds untested code still passes as long as
the total stays above 69%.

1. `tests.yml`: after `coverage combine`, `coverage xml`, then
   `diff-cover coverage.xml --compare-branch=origin/dev --fail-under=80`
   on pull requests (checkout with `fetch-depth: 0`).
2. Raise `fail_under` whenever the total rises, one step at a time.

## Not in this plan

- Type checks (mypy/pyright): later, after S6, starting with `cli_args.py`,
  `system_builder.py`, `benchmarks/registry.py`.
- Class renames in `clusters.py` (excluded by earlier decision).

## Known structural debt (moved from docs/Architecture.md)

- `experiments/base.py` (about 4,000 lines) and `clusters.py` (about 3,700 lines) are the largest modules. `work_benchmark_list()` alone is several hundred lines; splitting it into one handler per phase would make the phases testable on their own.
- The legacy `benchmark_list` path of the main loop is still there for configurations without benchmarker entries in `experiment_dict`. The entry scripts call `add_benchmark_list()`, which also fills `experiment_dict`, so they take the `experiment_dict` path.
