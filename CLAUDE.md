# Benchmark-Experiment-Host-Manager — package conventions

## Scope
These rules apply to all Python code in this repository.
Do **not** change logic or public names (classes, public methods, public attributes).
When cleaning code, verify that all references (imports, call sites, attribute
accesses) still resolve correctly after the change.
Before introducing a new pattern, check how similar things are already done in
the codebase and follow the existing convention.

## PEP 8
- Remove unused imports.
- `if x is not None` — never `if not x is None`.
- No always-true guards (`if True:`); flatten the body.
- Use `_` for intentionally unused loop or tuple-unpack variables.
- Use f-strings consistently; do not mix with `%` or `.format()`.
- Delete commented-out code that is not documentation.
- When removing a commented-out code block, also remove any comment whose sole
  purpose was to describe what that dead code did.
- Triple-quoted strings used as block comments or section separators are dead
  strings, not docstrings; replace with a `# Section name` line or delete.
- No always-constant variables used to gate output (`silent = False` that is
  never changed); flatten the conditional directly.
- Deprecated methods that are kept for reference must be prefixed `OLD_`
  (e.g. `OLD_evaluate_results`), not suffixed or left with an ambiguous name.
- Never use bare `except:`; always catch specific exception types.
- Extract unexplained numeric and string literals into named constants.

## PEP 257 — docstrings
- Documentation is generated with Sphinx.
- Every public module, class, and method gets a Sphinx-style docstring.
- Format: one-line imperative summary, blank line, then `:param name:`,
  `:type name:`, `:return:`, `:rtype:` as needed.
- Private helpers (`_name`) need at minimum a one-line docstring.

## Type annotations
- Annotate method parameters and return types whenever the type can be
  confidently inferred from context, usage, or existing docstrings.
- Use built-in generics (`list[str]`, `dict[str, int]`) over `typing` aliases
  where Python version allows.

## Attributes
- Declare all instance attributes in `__init__` before first use.
- Do not create attributes dynamically outside `__init__`.
- Define `__all__` in every module to make the public API explicit.

## Naming
- No single-letter names except `i`/`j` in simple index loops and `_` for discards.
- No opaque abbreviations; `df_aggregated` is fine, `x` is not.
- Propose clearer and consistent method names when existing names are unclear,
  inconsistent, or do not follow a unified convention across the codebase.

## Comments
- Comment when the WHY is non-obvious: a hidden constraint, a workaround,
  a subtle invariant.
- Add a short WHAT comment to introduce important sections whose purpose is
  not immediately obvious from the surrounding code structure.
- Do not comment self-explanatory code — names should be sufficient.
