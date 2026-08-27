# Benchmark-Experiment-Host-Manager — package conventions
Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

Tradeoff: These guidelines bias toward caution over speed. For trivial tasks, use judgment.

1. Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:
State your assumptions explicitly. If uncertain, ask.
If multiple interpretations exist, present them - don't pick silently.
If a simpler approach exists, say so. Push back when warranted.
If something is unclear, stop. Name what's confusing. Ask.

2. Simplicity First

Minimum code that solves the problem. Nothing speculative.

No features beyond what was asked.
No abstractions for single-use code.
No "flexibility" or "configurability" that wasn't requested.
No error handling for impossible scenarios.
If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

3. Surgical Changes

Touch only what you must. Clean up only your own mess.

When editing existing code:
Don't "improve" adjacent code, comments, or formatting.
Don't refactor things that aren't broken.
Match existing style, even if you'd do it differently.
If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
Remove imports/variables/functions that YOUR changes made unused.
Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

4. Goal-Driven Execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:
"Add validation" → "Write tests for invalid inputs, then make them pass"
"Fix the bug" → "Write a test that reproduces it, then make it pass"
"Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

5. Don't Reinvent the Wheel
if what we are trying to do is similar to settled science or industry practice, let me know. We don't have to reinvent the wheel.
If you see a clearly better approach, say so before implementing. Explain the tradeoff in 2-4 bullets. If the current request is still reasonable, proceed unless the alternative avoids serious risk or wasted work.

6. Write in Full Sentences, No Unexplained Jargon

**Technical terms are fine — but explain each one once, in the same breath. And explanations
are prose, not notes to yourself.**

Applies everywhere the user reads: chat replies, reports, docs, artifacts, commit messages.

Gloss every term on first use: "the story's centroid (the average fingerprint of its member articles)". After that, use it freely — the user reads ML papers.
Don't invent shorthand labels (story A/B/C, phase 2, …) without restating what they refer to when they reappear.
Explain in complete sentences: what was wrong, why the fix works, what it changes for the
  user. Not fragments, not clauses stacked behind em-dashes.
Bullets are for parallel items. Anything with a because or a but is an argument and
  belongs in prose.
Explanations are code-free. When the user asks to have something explained —
  a concept, an architecture, what was built — explain the idea in plain sentences
  without file paths, function names, table names, or identifiers. Those belong in
  docs and commit messages, where they can be looked up; in an explanation they are
  noise to a reader who doesn't live in the code. Mention code locations only when
  the user explicitly asks where something is implemented.
Brevity is not a goal in itself. Guidelines 2 and 3 are about code and never license
  terse prose — nor does the note-style of a /compact summary.

7. Document Every Implementation Request

docs/FEATURES.md is the traceability record. Keep it current in the same change.

Every implementation request gets a dated entry in the Part-2 request log
  (what was asked, in short) and — once shipped — a Part-1 inventory entry
  (what was built, where it lives, status).
Feature removals or replacements are logged there too, with what replaced
  them. Nothing disappears silently.
This is not optional polish: the user follows progress and traces past
  decisions through this file.


## Scope
The bexhoma package itself is off limits. Active work happens in the agent
implementation only — `agent/` and its tests. Do not modify `bexhoma/`, the
top-level experiment drivers, `k8s/`, or `contracts/` to make agent work
easier; treat them as a fixed external dependency the agent is written
against. If a bexhoma bug or limitation blocks the agent, report it and
propose a change — do not apply one unless explicitly asked.

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

## Comments
- Comment when the WHY is non-obvious: a hidden constraint, a workaround,
  a subtle invariant.
- Add a short WHAT comment to introduce important sections whose purpose is
  not immediately obvious from the surrounding code structure.
- Do not comment self-explanatory code — names should be sufficient.
