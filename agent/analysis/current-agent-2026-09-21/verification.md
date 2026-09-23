# Verification record

Reviewed commit: `66a67a58d0cd01e4ba01cfbe735b72aa1462e955` (v0.10.13). Date: 21 September 2026.

## Runtime review and safe probes

The implementation review covered the agent harness, validator, tools, model adapter, submission adapter, local lifecycle, cluster controller, serving manifests, catalog/result contracts, handbook, and maintained agent tests. Searches found no project training or adapter-loading pipeline in those components. Private model volumes and live deployment configuration were not inspected.

`audit_probes.py` was executed with Python 3.13 in a temporary environment, from the repository root:

```sh
MPLCONFIGDIR=/private/tmp/bexhoma-mpl PYTHONPATH=. \
  /private/tmp/bexhoma-audit-venv/bin/python \
  agent/analysis/current-agent-2026-09-21/audit_probes.py
```

The observed results are preserved in `audit-results.json`. All expected findings were reproduced. The process launcher was mocked, so no model request, credential renewal, Kubernetes mutation, or real benchmark was performed. The script reuses fixtures from the current test module and should be reviewed if those fixtures change.

## Maintained tests

The original repository `.venv` points at an unavailable Python 3.14 interpreter. The system Python is 3.9, below the project's supported minimum. To avoid changing the project environment, the review used a temporary Python 3.13 virtual environment with import dependencies installed separately. This was not a full locked production environment.

The focused command was:

```sh
TMPDIR=/private/tmp MPLCONFIGDIR=/private/tmp/bexhoma-mpl \
  /private/tmp/bexhoma-audit-venv/bin/python \
  -m unittest tests.test_agent_harness tests.test_agent_lifecycle
```

**183 tests ran: 177 passed, 4 failed, and 2 errored.** No runtime implementation or maintained tests were edited to make the result green.

The six non-passing tests were triaged as follows:

| Test | Observed cause |
|---|---|
| `test_benchmarker_peak_limits_must_fit_its_pinned_node` | The test expects four benchmarkers to require 512 GiB, assuming 128 GiB per pod. The current catalog/template declares 16 GiB per pod, so the proposed four pods require 64 GiB and fit the 384 GiB fixture node. |
| `test_co_located_sut_limits_are_added_to_benchmarker_limits` | The test expects two benchmarkers plus the 8 GiB SUT to require 264 GiB. With the current 16 GiB per benchmarker, they require 40 GiB and fit the fixture's 256 GiB node. |
| `test_completed_design_labels_investigation_with_scale_and_model` | The test selects the first directory from `investigations.iterdir()` without filtering for an investigation. The shared `inbox` directory can be selected, so the expected model suffix is absent. |
| `test_a_submitted_design_without_a_summary_still_succeeds` | The same unfiltered first-directory assumption can select `inbox`, causing the suffix assertion to fail. |
| `test_a_denied_directory_rename_does_not_fail_the_design_phase` | The same selection can choose `inbox`, then attempt to read its nonexistent trajectory. |
| `test_cli_interprets_an_exact_report_without_local_run_state` | The same selection can choose `inbox`, then attempt to read its nonexistent answer. |

An earlier run with macOS's default temporary-directory alias produced 8 failures and 1 error in 183 tests. Several compared `/var/...` paths with their canonical `/private/var/...` equivalents. Repeating with a canonical temporary root removed those path-alias failures but exposed the directory-order assumptions above. The failures were not presented as proof of broken production benchmark execution.

The tested temporary environment used Python 3.13.11, `dbmsbenchmarker` 0.15.1, `openai` 3.16.2, PyYAML 6.0.3, `python-dotenv` 1.2.3, Kubernetes client 36.0.3, and HiYaPyCo 0.7.0, plus transitive dependencies. The Kubernetes and HiYaPyCo versions differ from the root requirements' pins. The isolated result is useful for these mocked tests but is not certification of the production dependency combination.

## Diagram and artifact checks

All 13 DOT sources were rendered successfully by Graphviz to SVG. Raster previews of all diagrams were visually inspected. The entity relationship and failure/recovery layouts were revised to improve readability. Diagram labels and branches were checked against the implementation and the written findings. Each SVG is embedded directly in the HTML; no CDN or remote diagram renderer is required.

Static checks confirm 13 embedded diagrams, local Markdown image targets, valid SVG XML, unique HTML element identifiers, resolvable internal navigation anchors, and syntactically valid JavaScript. The HTML contains no external scripts, stylesheets, or image dependencies. External source citations are ordinary links.

A live browser was unavailable through the computer-use tool, so interactive zoom/dialog behavior and full browser page layout were not visually exercised. The controls are included, with native SVG files available as a fallback. The HTML was not converted to PDF or DOCX.

## Rebuild

Install Graphviz and Python Markdown in your chosen environment, then run:

```sh
python agent/analysis/current-agent-2026-09-21/build_report.py
```

The builder rewrites DOT, SVG, and HTML outputs from the graph definitions and `report.md`. Open `report.html` locally; no web server is necessary. The ZIP contains the editable report, graphs, builder, probes, and verification record.
