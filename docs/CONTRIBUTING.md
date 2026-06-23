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

Bexhoma follows [PEP 8](https://peps.python.org/pep-0008/) and [PEP 257](https://peps.python.org/pep-0257/). The most important rules in practice:

**Naming**
- `snake_case` for functions, methods, and variables; `PascalCase` for classes; `UPPER_CASE` for constants.
- No single-letter local variables except trivial loop counters. Never use `l`, `O`, or `I`.
- Do not shadow built-ins (`type`, `id`, `list`, `input`).

**Formatting**
- 4-space indentation, maximum 79-character lines.
- Two blank lines between top-level definitions; one blank line between methods.

**Idioms**
- `if x is None` / `if x is not None` — not `== None`.
- `with open(...) as f:` — not bare `open()/close()`.
- `dict.get(key, default)` instead of `if key in dict` guard patterns.
- Prefer early returns over deeply nested `if` blocks.

**Docstrings (PEP 257 + Sphinx)**

Every public module, class, and method must have a docstring using Sphinx-style annotations:

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

---

## AI-assisted contributions

Using a code copilot (GitHub Copilot, Claude, etc.) to write or review code is fine and encouraged — as long as you review the output and ensure it meets the style and correctness requirements above.

---

## Testing

New features and bug fixes must include a test.

- `test.sh` — basic functional test cases; see [TestCases](TestCases.md) for the full list.
- `test-more.sh` — extended tests covering additional DBMS and longer runs.

Run the relevant test cases against a live Kubernetes cluster before submitting. Log output from `test.sh` goes to `logs_tests/`; include a representative log in your PR if the change affects experiment execution.
