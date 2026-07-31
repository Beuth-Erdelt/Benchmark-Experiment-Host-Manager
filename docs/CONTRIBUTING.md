# Contributing to Bexhoma

Contributions are welcome. Areas where help is most useful:

- **New workloads** — add benchmark scripts in `experiments/`, YAML manifests in `k8s/`, and Docker images in `images/`.
- **New DBMS** — add deployment manifests in `k8s/` and a configuration block in `experiments/`.
- **Bug fixes and testing** — report bugs via the [issue tracker](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/issues) or open a pull request.
- **Documentation** — corrections, clarifications, and new examples are all welcome.

---

## Pull requests

- Branch off from `master` with a short descriptive name (`feature/ycsb-redis`, `fix/loader-encoding`).
- Keep each PR focused on one change. Unrelated fixes belong in a separate PR.
- Reference the relevant issue number in the PR description where applicable.
- By submitting a PR you agree to license your contribution under the **GNU Affero General Public License v3**.

---

## Code style

Bexhoma follows [PEP 8](https://peps.python.org/pep-0008/) and [PEP 257](https://peps.python.org/pep-0257/). These rules apply to all Python code in the repository. When cleaning up existing code: do not change logic or public names (classes, public methods, public attributes), verify that all references (imports, call sites, attribute accesses) still resolve correctly after the change, and check how similar things are already done elsewhere in the codebase before introducing a new pattern.

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

- Logo/icon files live in `docs/logo/` (`bexhoma-banner.png` for light mode,
  `bexhoma-logo-1-lockup-dark.svg` for dark mode, plus icon/favicon variants).
- Brand colors: `#326CE5` (blue, icon/accent), `#F5A623` (orange, accent),
  `#1B2A4A` (dark navy, light-mode wordmark text).
- Referenced from `README.md` via a `<picture>` element with
  `prefers-color-scheme` sources so the logo adapts to GitHub's dark mode.
  PyPI's README renderer strips `<picture>` and doesn't resolve relative
  paths, so the fallback `<img>` inside it must use an absolute
  `raw.githubusercontent.com` URL — that fallback is what PyPI ends up
  showing.
- Referenced from `docs/conf.py` (`html_logo`, `html_favicon`) for the
  Sphinx/Read the Docs build.
- Licensed separately from the AGPL v3 code, under CC BY 4.0 — see
  `docs/logo/README.md`.

---

## AI-assisted contributions

Using a code copilot (GitHub Copilot, Claude, etc.) to write or review code is fine and encouraged — as long as you review the output and ensure it meets the style and correctness requirements above.

---

## Testing

New features and bug fixes must include a test.

- `test.sh` — basic functional test cases; see [TestCases](TestCases.md) for the full list.
- `test-more.sh` — extended tests covering additional DBMS and longer runs.

Run the relevant test cases against a live Kubernetes cluster before submitting. Log output from `test.sh` goes to `logs_tests/`; include a representative log in your PR if the change affects experiment execution.
