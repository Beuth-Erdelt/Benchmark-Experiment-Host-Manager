"""
Agent-consumable tiered Markdown summary report writer.

Writes ``{resultfolder}/{code}/report/`` alongside the plain-text summary that
:meth:`~bexhoma.benchmarks.base.Benchmark.show_summary` already prints to
stdout. The report is organised in three tiers so an agent (or a human) can
navigate from a headline answer to raw evidence without guessing a path:

Output contract
----------------

1. **Entry point, stop-early rule.** Always start at ``index.md``. Its Tests
   table, Health Summary, and section links usually answer "did this pass"
   and "what ran" on their own — stop there if that is the question. Only
   open a tier-2 file when an actual metric value is needed, and only follow
   a tier-2 file's Provenance link when its evidence still does not resolve
   the question.
2. **Tiered file groups, with read-when conditions.**

   - Tier 1 — Answers: ``index.md``. Read always, first.
   - Tier 2 — Evidence: ``workflow.md``, ``loading.md``, ``execution.md``,
     ``monitoring.md``, ``connections.md`` (each only written when the
     underlying phase/data is actually active). Read when a metric value is
     needed, or a Tests-table failure needs tracing to its connection/phase.
   - Tier 3 — Diagnosis: the literal, pre-existing result-folder files linked
     from every tier-2 file's ``### Provenance`` footer (``connections.config``,
     per-pod logs, rendered Kubernetes manifests, loading DDL/bash scripts and
     their stdout/stderr, SUT container logs and ``kubectl describe pod``
     output, Prometheus metric CSVs). Read only when tier 2's aggregated view
     does not resolve the question.
3. **Naming legend**, framed as a decoding algorithm — see
   :data:`_NAMING_CONVENTIONS_MD`, embedded verbatim in ``index.md``.
4. **Validity-first rule**: a failed Tests-table row scopes interpretation of
   every metric below it — see :data:`_VALIDITY_RULES_MD`, embedded verbatim
   in ``index.md``.
5. **Interpretation rules** (compare only within one experiment code, report
   variance across repetitions, cite file paths) — see
   :data:`_INTERPRETATION_RULES_MD`, embedded verbatim in ``index.md``.

Consistency guarantee
----------------------

Every cross-reference is computed at generation time from the real
filesystem/data, never hand-maintained as a separate list that could drift:
``index.md``'s ``sections`` frontmatter is built from the files this module
actually wrote; every ``### Provenance`` link is ``glob()``-derived against
the real result folder; every relative path is ``os.path.relpath()``-computed
rather than a hand-typed ``../``; connection-name links in metric tables and
``connections.md``'s anchors both come from the same
``get_connections_of_experiment()`` call, so a link can never dangle.

See ``bexhoma/experiments/README.md`` §9 and ``docs/AgentReport.md`` for the
full design rationale.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yaml

from bexhoma import evaluators
from bexhoma.benchmarks.base import Section

__all__ = ["write_markdown_report"]

#: Bump whenever the frontmatter fields, tiers, or file layout change.
SCHEMA_VERSION = "1.0.0"

_NAMING_CONVENTIONS_MD = """### Naming Conventions

Every identifier in this report is a positional concatenation. Decode any of
them by counting dash-separated segments from the right — no lookup table is
needed, just the position rule:

- `connection` = `<configuration>-<experiment_run>-<client>-<benchmark_run>-<pod>`
- `job` = `<configuration>-<experiment_run>-<client>-<benchmark_run>` (drops the trailing pod segment)
- `phase` = `<configuration>-<experiment_run>-<client>` (drops benchmark_run and pod too)

| Term | Description | Example |
|---|---|---|
| configuration | Name of the SUT instance | `PostgreSQL-1` |
| experiment_run | Repeat counter for the whole experiment | `2` |
| client | 1-based index of the benchmark phase within a run | `3` |
| phase | Benchmark phase identifier | `PostgreSQL-1-2-3` |
| benchmark_run | 1-based index of a parallel benchmark job within a phase | `4` |
| job | Benchmark job identifier | `PostgreSQL-1-2-3-4` |
| pod | 1-based index of a driver pod within a job | `5` |
| connection | Driver-pod identifier | `PostgreSQL-1-2-3-4-5` |

**Experiment code convention**: `code` (this experiment's result-folder name)
is a Unix epoch timestamp in seconds, generated at experiment start. It is
unique and monotonically increasing across experiments, but is **not**
evidence that two different codes ran under comparable conditions — see
Interpretation Rules below.

**Result-folder filenames** (manifests, logs, `.describe.log` — linked from
every tier-2 file's Provenance footer) follow a related but distinct
convention: `<app>-<component>-<configuration>-<code>[-<experiment_run>[-<client>[-<benchmark_run>]]]`,
optionally followed by Kubernetes' own pod-hash/random suffix on files tied to
a specific pod (e.g. `bexhoma-benchmarker-postgresql-1-1784910886-1-1-1-qp9nt.dbmsbenchmarker.log`).
The long-lived SUT Deployment is the one exception worth knowing: its
manifest is written once per configuration with **no** `experiment_run`
segment (`bexhoma-sut-postgresql-1-1784910886.yml`), but its stored
`.describe.log` and container `.log` files splice the experiment_run in
directly after `code` — same position as everywhere else — ahead of
Kubernetes' pod-hash/random suffix
(`bexhoma-sut-postgresql-1-1784910886-3-7bd45c7b95-pwzkz.dbms.log`), because
each run can restart that same long-lived pod and needs its own capture.
"""

_VALIDITY_RULES_MD = """### Validity-First Rules

If any row in the Tests table below is **failed**, treat it as a scope
restriction on every metric elsewhere in this report — check it *before*
quoting any number, not after:

| Failed test | Scopes / invalidates | Check |
|---|---|---|
| `SQL errors` | Per-query metrics for the specific queries that errored | `execution.md`'s Errors subsection |
| `SQL warnings (result mismatch)` | Correctness of results for the affected queries (timing may still be valid) | `execution.md`'s Warnings subsection |
| `Workflow as planned` | Whether pod counts matched the intended sweep — cross-configuration/cross-phase comparisons may not be apples-to-apples | `workflow.md`'s Actual vs. Planned |
| `Geo Times [s]` / `Power@Size [~Q/h]` / `Throughput@Size` contains 0 or NaN | That metric column is incomplete for at least one row | `execution.md`'s Per Phase table |
| `{component} contains 0 or NaN in CPU [CPUs]` | Monitoring data for that component/phase | `monitoring.md` |

A **skipped** test (e.g. monitoring skipped because data was pre-existing, or
a phase shorter than the Prometheus scrape interval) does not invalidate
anything — only a **failed** row does.
"""

_INTERPRETATION_RULES_MD = """### Interpretation Rules

- **Compare only within this experiment code.** Every table in this report
  describes one controlled run. Do not treat numbers from a different
  `report/` folder (a different experiment code) as directly comparable
  without independently verifying equivalent conditions — cross-code
  comparison is what the `collectors` module is built for, not this report.
- **Report variance, not just point estimates.** Metric tables are already
  aggregated across parallel pods, but a sweep normally has multiple
  experiment-run/client repetitions. Summarize the range across those
  repetitions rather than citing one row as the only data point.
- **Cite file paths.** Any number stated in an agent's own output must be
  attributed to the specific report file (and ideally row/column) it came
  from — never asserted from memory of an earlier read.
"""

_ENTRY_POINT_MD = (
    "Start here. If the Tests and Health Summary below already answer the "
    "question, no other file needs opening. Only open a tier-2 file when an "
    "actual metric value is needed, and only follow a tier-2 file's "
    "Provenance link when its evidence still does not resolve the question."
)

_TIER_TABLE_MD = """### Report Structure

| Tier | Files | Read when |
|---|---|---|
| 1 — Answers | `index.md` (this file) | Always, first |
| 2 — Evidence | linked below, one file per active phase/topic | An actual metric value is needed, or a Tests-table failure needs tracing to its connection/phase |
| 3 — Diagnosis | raw result-folder files linked from each tier-2 file's Provenance footer | Tier 2's aggregated tables do not resolve the question |
"""


def _slugify(name: str) -> str:
    """
    Build a Markdown-heading-anchor-safe slug from a connection name.

    :param name: Connection name, e.g. ``"PostgreSQL-1-1-1-2-1"``.
    :return: Lowercased slug with any non ``[a-z0-9-]`` character collapsed
             to a single hyphen.
    :rtype: str
    """
    return re.sub(r'[^a-z0-9\-]+', '-', name.lower()).strip('-')


def _relmd(target: Path, start: Path) -> str:
    """
    Build a forward-slash relative path suitable for a Markdown link.

    :param target: Absolute path being linked to.
    :param start: Directory the link is written from (``report/``).
    :return: ``os.path.relpath(target, start)``, normalised to ``/`` separators
             so links are correct on Windows too.
    :rtype: str
    """
    return Path(os.path.relpath(target, start=start)).as_posix()


def _glob_provenance(result_dir: Path, report_dir: Path, patterns: list[str], description: str) -> list[str]:
    """
    Build a described Markdown block for every real file matching any of
    ``patterns`` — one italic line explaining why/what to look for, then one
    bullet link per matched file.

    An agent should never have to open a Provenance link just to find out
    what kind of file it is; the description answers that up front.

    :param result_dir: The experiment's result folder (one level above ``report/``).
    :param report_dir: The ``report/`` directory the links are written from.
    :param patterns: ``Path.glob()`` patterns to match against ``result_dir``.
    :param description: One-line explanation of what this file kind contains
        and why it might be worth opening — rendered as an italic line above
        the links.
    :return: ``[description_line, "", *bullet_lines, ""]``, or an empty list
             when nothing matches — a link (and its description) is never
             written for a file kind that does not exist. Description lines
             are distinguished from bullet lines by not starting with ``"- ["``
             (see :func:`_write_tier2_file`, which extracts only the bullet
             lines into the frontmatter's ``provenance`` path list).
    :rtype: list[str]
    """
    matches: set[Path] = set()
    for pattern in patterns:
        matches.update(result_dir.glob(pattern))
    if not matches:
        return []
    lines = [f"*{description}*", ""]
    lines.extend(f"- [{path.name}]({_relmd(path, report_dir)})" for path in sorted(matches))
    lines.append("")
    return lines


def _linkify_index(df: pd.DataFrame, connections_index: dict[str, str]) -> pd.DataFrame:
    """
    Rewrite a DataFrame's index into links to ``connections.md`` anchors.

    Returns a copy — the original DataFrame (and the stdout renderer, which
    never sees this function) is unaffected.

    :param df: DataFrame whose index holds connection names.
    :param connections_index: Map of connection name to its ``connections.md`` anchor slug.
    :return: Copy of ``df`` with index values replaced by Markdown links,
             for names present in ``connections_index``; other index values
             are left unchanged.
    :rtype: pandas.DataFrame
    """
    if df is None or df.empty:
        return df
    df = df.copy()
    df.index = [
        f"[{name}](connections.md#{connections_index[str(name)]})" if str(name) in connections_index else name
        for name in df.index
    ]
    return df


def _render_sections(sections: list[Section], connections_index: dict[str, str]) -> list[str]:
    """
    Render a list of top-level :class:`~bexhoma.benchmarks.base.Section`
    objects into Markdown lines.

    :param sections: Top-level sections to render, in display order.
    :param connections_index: Map of connection name to ``connections.md`` anchor slug.
    :return: Markdown lines, one section (and its children) after another.
    :rtype: list[str]
    """
    lines: list[str] = []
    for section in sections:
        _render_section(section, connections_index, lines)
    return lines


def _render_section(section: Section, connections_index: dict[str, str], lines: list[str]) -> None:
    """
    Recursively append one :class:`~bexhoma.benchmarks.base.Section` (and its
    children) to ``lines``.

    :param section: Section to render.
    :param connections_index: Map of connection name to ``connections.md`` anchor slug.
    :param lines: Accumulator list, appended to in place.
    """
    lines.append("")
    lines.append("#" * section.level + " " + section.heading)
    if section.blank_after_heading:
        lines.append("")
    if section.dataframe is not None and not (section.skip_if_empty and section.dataframe.empty):
        df = section.dataframe
        if section.link_connections and connections_index:
            df = _linkify_index(df, connections_index)
        kwargs = {"index": section.index}
        if section.floatfmt is not None:
            kwargs["floatfmt"] = section.floatfmt
        lines.append(df.to_markdown(**kwargs))
    if section.lines:
        lines.extend(section.lines)
    for child in section.children:
        _render_section(child, connections_index, lines)


def _frontmatter(fields: dict) -> str:
    """
    Build a YAML frontmatter block.

    :param fields: Frontmatter key/value pairs.
    :return: ``---\\n<yaml>\\n---\\n`` block.
    :rtype: str
    """
    return "---\n" + yaml.safe_dump(fields, sort_keys=False) + "---\n"


def _count_sut_restarts(result_dir: Path) -> tuple[int, dict[str, str]]:
    """
    Parse ``bexhoma-sut-*-restarts.json`` files into a total count and a
    per-pod breakdown.

    Same source files ``show_summary_header()`` already reads (and tests via
    ``_record_test(total_restarts == 0, "No SUT container restarts")``); this
    is an independent, read-only re-parse for report purposes, not a second
    source of truth.

    :param result_dir: The experiment's result folder.
    :return: Tuple of the total restart count across all pods, and a dict
             mapping pod name to its raw per-container restart-count string.
    :rtype: tuple[int, dict[str, str]]
    """
    total = 0
    per_pod: dict[str, str] = {}
    for restarts_file in sorted(result_dir.glob("bexhoma-sut-*-restarts.json")):
        with open(restarts_file) as handle:
            pod_restarts: dict[str, str] = json.load(handle)
        for pod, counts in pod_restarts.items():
            pod_total = sum(int(x) for x in counts.split()) if counts.strip() else 0
            total += pod_total
            per_pod[pod] = counts
    return total, per_pod


def _get_metric_definitions(connections_sorted: list[dict]) -> dict[str, dict]:
    """
    Read metric metadata (title/active/type/aggregation-kind) from the first
    connection that carries a ``monitoring.metrics`` block.

    Mirrors :meth:`bexhoma.collectors.base.get_metrics`'s field selection, but
    scoped to a single experiment's already-in-memory ``connections_sorted``
    (no second read of ``connections.config``).

    :param connections_sorted: Connection dicts as read by
        ``experiment.show_summary_header()``.
    :return: Map of metric key to its ``title``/``active``/``type``/``metric`` fields.
    :rtype: dict[str, dict]
    """
    for conn in connections_sorted:
        metrics = conn.get('monitoring', {}).get('metrics')
        if metrics:
            return {
                key: {
                    'title': metric.get('title', key),
                    'active': metric.get('active', True),
                    'type': metric.get('type', 'cluster'),
                    'metric': metric.get('metric', ''),
                }
                for key, metric in metrics.items()
            }
    return {}


def _build_monitoring_sections(
    experiment, evaluator, connections_sorted: list[dict], monitoring_applications: dict,
    result_dir: Path, report_dir: Path,
) -> tuple[list[Section], list[str]]:
    """
    Build ``monitoring.md``'s content: the curated CPU/RAM tables (same data
    ``show_summary_monitoring()`` already prints), the curated Application
    Metrics tables, and a Full Metric Catalog appendix covering every
    configured metric — not just the four hardcoded hardware ones or the
    first five application metrics ``show_summary()`` caps at. See the module
    docstring's "Scope extension" rationale.

    The Full Metric Catalog's ``component`` values are internal routing keys
    (e.g. ``stream`` for "Execution phase: SUT deployment", ``loader`` for
    "Loading phase: component loader") that are not self-explanatory on their
    own — so every catalog row and every per-metric subsection heading also
    carries the matching human-readable ``component_title`` from
    ``monitoring_components``, making a metric (e.g. CPU Throttle for the SUT)
    findable by title alone, without needing to know the internal key.

    :param experiment: The owning experiment object.
    :param evaluator: The primary benchmark's evaluator.
    :param connections_sorted: Connection dicts as read by ``show_summary_header()``.
    :param monitoring_applications: Curated application-metric DataFrames,
        keyed by title, as returned by ``show_summary_header()``.
    :param result_dir: The experiment's result folder.
    :param report_dir: The ``report/`` directory.
    :return: Tuple of the sections to render into ``monitoring.md``, and
             extra Provenance bullet lines for the metric CSVs it references.
    :rtype: tuple[list[Section], list[str]]
    """
    if not (experiment.monitoring_active or experiment.cluster.monitor_cluster_active):
        return [], []
    sections: list[Section] = []
    provenance: list[str] = []
    monitoring_components = experiment.workload.get('monitoring_components', {})
    for component, title in monitoring_components.items():
        df_monitoring, _insufficient_samples = experiment.show_summary_monitoring_table(evaluator, component)
        if len(df_monitoring) > 0:
            df = pd.concat(df_monitoring, axis=1).round(2)
            df = df.reindex(index=evaluators.natural_sort(df.index))
            df.index.names = ["DBMS"]
            sections.append(Section(heading=title, level=3, dataframe=df, link_connections=True))
    if monitoring_applications:
        for title, metrics in monitoring_applications.items():
            metrics = metrics.copy()
            metrics.index.names = ["DBMS"]
            sections.append(Section(heading=f"Application Metrics: {title}", level=3, dataframe=metrics, link_connections=True))

    metric_defs = _get_metric_definitions(connections_sorted)
    catalog_rows = []
    catalog_value_sections = []
    for component, component_title in monitoring_components.items():
        for metric_key, meta in metric_defs.items():
            df = evaluator.get_monitoring_metric(metric=metric_key, component=component)
            if df.empty:
                continue
            if meta['metric'] == 'counter':
                aggregated = df.max().sort_index() - df.min().sort_index()
            elif meta['metric'] == 'ratio':
                aggregated = df.max().sort_index()
            else:
                aggregated = df.mean().sort_index()
            df_cleaned = pd.DataFrame(aggregated)
            df_cleaned.columns = [meta['title']]
            df_cleaned = df_cleaned.reindex(index=evaluators.natural_sort(df_cleaned.index))
            df_cleaned.index.names = ["DBMS"]
            catalog_rows.append({
                'metric_key': metric_key, 'title': meta['title'], 'type': meta['type'],
                'metric': meta['metric'], 'component': component, 'component_title': component_title,
            })
            catalog_value_sections.append(Section(
                heading=f"{meta['title']} (`{metric_key}`, {component} — {component_title})", level=4,
                dataframe=df_cleaned, link_connections=True,
            ))
            csv_path = result_dir / f"query_{component}_metric_{metric_key}.csv"
            if csv_path.exists():
                provenance.append(f"- [{csv_path.name}]({_relmd(csv_path, report_dir)})")
    if catalog_rows:
        sections.append(Section(
            heading="Full Metric Catalog", level=3, index=False,
            dataframe=pd.DataFrame(catalog_rows),
            children=catalog_value_sections,
        ))
    if provenance:
        provenance = [
            "*One CSV per metric per component (wide format: one column per "
            "connection, one row per Prometheus scrape) backing each catalog "
            "table above.*", "",
        ] + provenance + [""]
    return sections, provenance


def _build_monitoring_summary_lines(monitoring_sections: list[Section]) -> list[str]:
    """
    Build a brief ``### Monitoring`` block for ``index.md``: one bullet per
    curated CPU/RAM component table in ``monitoring.md``, showing its peak
    CPU/RAM across all phases.

    Not a re-fetch: aggregates the same top-level ``Section`` dataframes
    :func:`_build_monitoring_sections` already built for ``monitoring.md``.
    A section counts as a curated hardware table (as opposed to an
    Application Metrics table or the Full Metric Catalog appendix) when its
    dataframe carries both a ``Max CPU`` and a ``Max RAM [Gb]`` column.

    :param monitoring_sections: The sections built by
        :func:`_build_monitoring_sections`.
    :return: Markdown lines for the ``### Monitoring`` block, or an empty
             list when no curated hardware section is present (monitoring
             not active, or no data collected).
    :rtype: list[str]
    """
    peaks = [
        (section.heading, section.dataframe['Max CPU'].max(), section.dataframe['Max RAM [Gb]'].max())
        for section in monitoring_sections
        if section.dataframe is not None and not section.dataframe.empty
        and 'Max CPU' in section.dataframe.columns and 'Max RAM [Gb]' in section.dataframe.columns
    ]
    if not peaks:
        return []
    lines = [
        "### Monitoring", "",
        "Peak CPU/RAM per monitored component, across all phases — see "
        "[monitoring.md](monitoring.md) for per-phase detail and the full metric catalog.",
        "",
    ]
    lines.extend(
        f"- {heading}: {max_cpu:.2f} CPUs, {max_ram:.2f} Gb RAM (peak)"
        for heading, max_cpu, max_ram in peaks
    )
    return lines


def _build_workload_identity_lines(workload: dict, code: str) -> list[str]:
    """
    Build the ``### Workload`` block for ``index.md`` from the same data
    ``show_summary_header()`` already reads (minus its per-connection loop,
    which ``connections.md`` covers instead).

    :param workload: The experiment's workload dict (``queries.config``).
    :param code: Experiment code.
    :return: Markdown lines for the Workload identity block.
    :rtype: list[str]
    """
    lines = ["### Workload", "", workload.get('name', ''), "", f"* Type: {workload.get('type', '')}"]
    if 'duration' in workload:
        lines.append(f"* Duration: {workload['duration']}s")
    lines.append(f"* Code: {code}")
    if workload.get('intro'):
        lines.append(f"* {workload['intro']}")
    if workload.get('info'):
        lines.append(f"* {workload['info'].replace(chr(10), chr(10) + '  * ')}")
    if workload.get('workflow_errors'):
        for error, messages in workload['workflow_errors'].items():
            lines.append(f"* Error: {error}")
            for message in messages:
                lines.append(f"  * {message}")
    return lines


def _build_tests_lines(test_results: list[tuple]) -> list[str]:
    """
    Render ``experiment._test_results`` as a Markdown table.

    :param test_results: List of ``(passed, label)`` tuples; ``passed`` is
        ``True``/``False``/``None`` (``None`` = skipped).
    :return: Markdown lines for the ``### Tests`` table.
    :rtype: list[str]
    """
    lines = ["### Tests", "", "| status | label |", "|---|---|"]
    for passed, label in test_results:
        status = "skipped" if passed is None else ("passed" if passed else "failed")
        lines.append(f"| {status} | {label} |")
    return lines


def _build_health_summary_lines(total_restarts: int, extra_context: dict) -> list[str]:
    """
    Build the terse ``### Health Summary`` block: one status line per
    concern, "none" in the clean case, a link to the tier-2 file with the
    full detail only when non-zero. Never embeds the full detail itself.

    :param total_restarts: Total SUT container restart count across all pods.
    :param extra_context: The ``extra_context`` dict returned by
        ``_show_extra_sections()``; carries ``num_errors``/``num_warnings``
        only for DBMSBenchmarker-family benchmarks.
    :return: Markdown lines for the Health Summary block.
    :rtype: list[str]
    """
    lines = ["### Health Summary", ""]
    if total_restarts == 0:
        lines.append("- SUT container restarts: none")
    else:
        lines.append(f"- SUT container restarts: {total_restarts} — see [connections.md](connections.md) for per-pod detail")
    if 'num_errors' in extra_context:
        num_errors = extra_context['num_errors']
        num_warnings = extra_context.get('num_warnings', 0)
        if num_errors == 0:
            lines.append("- SQL errors: none")
        else:
            lines.append(f"- SQL errors: {num_errors} — see [execution.md](execution.md)'s Errors subsection for the affected queries")
        if num_warnings == 0:
            lines.append("- SQL warnings: none")
        else:
            lines.append(f"- SQL warnings: {num_warnings} — see [execution.md](execution.md)'s Warnings subsection for the affected queries")
    return lines


def _connections_index(df_connections: pd.DataFrame) -> dict[str, str]:
    """
    Build the connection-name-to-anchor-slug map shared by the linkification
    pass and ``connections.md``'s own anchors, from a single data pull.

    :param df_connections: Output of ``evaluator.get_connections_of_experiment()``.
    :return: Map of connection name (the ``connection`` column's value, not
             the code-prefixed DataFrame index) to its ``connections.md``
             anchor slug.
    :rtype: dict[str, str]
    """
    if df_connections.empty or 'connection' not in df_connections.columns:
        return {}
    return {str(name): _slugify(str(name)) for name in df_connections['connection']}


def _build_connections_md_lines(
    df_connections: pd.DataFrame, result_dir: Path, report_dir: Path, restarts_per_pod: dict[str, str],
) -> list[str]:
    """
    Build ``connections.md``'s body: one subsection per row of
    ``df_connections``, each with its own parameter columns plus glob-derived
    links to its benchmarker log, its SUT's container log, its
    ``kubectl describe pod`` output, and the monitoring CSV covering it.

    :param df_connections: Output of ``evaluator.get_connections_of_experiment()``.
    :param result_dir: The experiment's result folder.
    :param report_dir: The ``report/`` directory.
    :param restarts_per_pod: Pod name to raw restart-count string, from
        :func:`_count_sut_restarts`.
    :return: Markdown lines for the whole file body (excluding frontmatter).
    :rtype: list[str]
    """
    lines: list[str] = []
    if restarts_per_pod:
        lines.append("### SUT Container Restarts")
        lines.append("")
        for pod, counts in sorted(restarts_per_pod.items()):
            lines.append(f"* {pod}: {counts}")
        lines.append("")
    for _connection_id, row in df_connections.iterrows():
        name = str(row.get('connection', _connection_id))
        slug = _slugify(name)
        configuration = str(row.get('configuration', ''))
        lines.append(f"#### {name}")
        lines.append("")
        lines.append(f"<a id=\"{slug}\"></a>")
        for column, value in row.items():
            if column == 'connection' or value is None:
                continue
            if isinstance(value, float) and pd.isna(value):
                continue
            if str(value) == '':
                continue
            lines.append(f"* {column}: {value}")
        log_links = _glob_provenance(
            result_dir, report_dir, [f"*{name}*.log", f"*{configuration}*.dbms*.log"],
            "This connection's own benchmarker/driver pod log, and its SUT's container "
            "log (the DBMS process's own stdout) — read for the literal error text or "
            "log lines behind a failed/slow query.",
        )
        describe_links = _glob_provenance(
            result_dir, report_dir, [f"*{configuration}*.describe.log"],
            "`kubectl describe pod` output for this connection's SUT — its event "
            "history (scheduling, image pull, restarts, OOMKills), not just static spec.",
        )
        metric_links = _glob_provenance(
            result_dir, report_dir, ["query_*_metric_*.csv"],
            "Wide-format monitoring CSV (one column per connection, one row per "
            "Prometheus scrape) backing the metrics shown for this connection — find "
            "this connection's own column.",
        )
        if log_links or describe_links or metric_links:
            lines.append("")
            lines.append("##### Provenance")
            lines.append("")
            lines.extend(log_links)
            lines.extend(describe_links)
            lines.extend(metric_links)
        lines.append("")
    return lines


def write_markdown_report(
    experiment,
    benchmark,
    workflow_section: Section | None,
    loading_section: Section | None,
    execution_section: Section | None,
    extra_sections: list[Section],
    key_metrics_section: Section | None,
    connections_sorted: list[dict],
    monitoring_applications: dict,
    extra_context: dict,
    df_connections: pd.DataFrame,
) -> None:
    """
    Write the tiered Markdown report (``report/index.md`` + detail files) to
    the experiment's result folder.

    Called from :meth:`~bexhoma.benchmarks.base.Benchmark.show_summary` when
    ``write_report=True``, using the exact same :class:`~bexhoma.benchmarks.base.Section`
    trees and data that were just rendered to stdout — nothing here re-fetches
    evaluator data that the caller already has, except the Full Metric
    Catalog appendix (see :func:`_build_monitoring_sections`), which is
    genuinely new data ``show_summary()`` never computes at all.

    :param experiment: The owning experiment object.
    :param benchmark: The primary benchmark (``self`` from ``show_summary()``);
        used for ``benchmark.evaluator.path``, the same result-folder path
        every evaluator method already resolves from.
    :param workflow_section: The ``Workflow`` section, or ``None`` when
        benchmarking was not active.
    :param loading_section: The ``Loading`` section, or ``None`` when loading
        was not active or produced no data.
    :param execution_section: The ``Execution`` section, or ``None`` when
        benchmarking was not active.
    :param extra_sections: Secondary-benchmark and Latency/Errors/Warnings
        sections from ``_show_extra_sections()``.
    :param key_metrics_section: The benchmark-type-specific ``Key Metrics``
        section from ``benchmark._build_key_metrics_section()`` (e.g. Geo
        Times/Power@Size/Throughput@Size for DBMSBenchmarker, NOPM for
        HammerDB) — the same columns that benchmark's evaluator already
        tests via ``record_tests()``. Report-only: rendered into ``index.md``,
        never printed to stdout. ``None`` when this benchmark type defines no
        headline metric, or benchmarking was not active.
    :param connections_sorted: Connection dicts as read by ``show_summary_header()``.
    :param monitoring_applications: Curated application-metric DataFrames
        from ``show_summary_header()``.
    :param extra_context: Extra context dict from ``_show_extra_sections()``
        (carries ``num_errors``/``num_warnings`` for DBMSBenchmarker-family
        benchmarks).
    :param df_connections: Output of ``evaluator.get_connections_of_experiment()``,
        or an empty DataFrame when benchmarking was not active.
    """
    result_dir = Path(benchmark.evaluator.path)
    report_dir = result_dir / "report"
    report_dir.mkdir(parents=True, exist_ok=True)

    connections_index = _connections_index(df_connections)
    written_sections: list[dict] = []

    if workflow_section is not None:
        manifest_links = _glob_provenance(
            result_dir, report_dir, ["*.yml", "*.yaml"],
            "Rendered Kubernetes Job/Deployment/Service manifests actually submitted — "
            "check for the exact resource requests/limits, image tag, env vars, and "
            "replica/parallelism counts.",
        )
        pod_describe_links = _glob_provenance(
            result_dir, report_dir, ["*.describe.log"],
            "`kubectl describe pod` output for every pod in this experiment — event "
            "history (scheduling, image pulls, restarts, OOMKills) for that specific "
            "pod object, not just static spec.",
        )
        job_describe_links = _glob_provenance(
            result_dir, report_dir, ["*.describe.job.log"],
            "`kubectl describe job` output for every loading/generator Job in this "
            "experiment — unlike a single pod's describe above, this covers the Job's "
            "full pod-creation history over its whole lifetime, so a failed pod that "
            "was replaced under `backoffLimit` still shows up here even after that "
            "failed pod's own describe has aged out via garbage collection.",
        )
        _write_tier2_file(
            report_dir, "workflow.md", "workflow", "Actual vs. planned experiment workflow.",
            [workflow_section], connections_index,
            manifest_links + pod_describe_links + job_describe_links,
        )
        written_sections.append({"title": "Workflow", "file": "workflow.md", "description": "Actual vs. planned workflow (per configuration/run/client)."})

    if loading_section is not None:
        loading_script_links = _glob_provenance(
            result_dir, report_dir, ["*-loading-*.sql.log", "*-loading-*.sh.log"],
            "The exact rendered SQL/bash script that ran for each configuration's "
            "loading phase — despite the `.log` suffix, this is the script source "
            "itself, not output. Check here to see exactly what schema/DDL was applied.",
        )
        loading_stdout_links = _glob_provenance(
            result_dir, report_dir, ["*-loading-*.stdout.log"],
            "stdout of running each loading script above.",
        )
        loading_stderr_links = _glob_provenance(
            result_dir, report_dir, ["*-loading-*.stderr.log"],
            "stderr of running each loading script above — check here first if a "
            "loading phase failed silently.",
        )
        _write_tier2_file(
            report_dir, "loading.md", "loading", "Data-loading phase results.",
            [loading_section], connections_index,
            loading_script_links + loading_stdout_links + loading_stderr_links,
        )
        written_sections.append({"title": "Loading", "file": "loading.md", "description": "Per-connection and per-run loading throughput/timing."})

    if execution_section is not None or extra_sections:
        execution_all = ([execution_section] if execution_section is not None else []) + extra_sections
        execution_links = _glob_provenance(
            result_dir, report_dir,
            ["bexhoma-benchmarker-*.log", "bexhoma-benchmarker.*.all.df.pickle"],
            "Raw per-pod benchmarker logs and the cached aggregated DataFrame they "
            "were parsed into — read the logs for the literal output behind a "
            "surprising number.",
        )
        if 'num_errors' in extra_context:
            # queries.config only carries literal SQL text for DBMSBenchmarker-family
            # benchmarks (TPC-H/TPC-DS); other tools store their workload elsewhere.
            execution_links += _glob_provenance(
                result_dir, report_dir, ["queries.config"],
                "The DBMSBenchmarker query config actually run, including the literal "
                "SQL text of every query behind the titles in the Latency/Errors/"
                "Warnings tables above — follow this for the explicit queries.",
            )
        _write_tier2_file(
            report_dir, "execution.md", "execution",
            "Benchmark execution results, including any secondary (co-running) benchmarks.",
            execution_all, connections_index, execution_links,
        )
        written_sections.append({"title": "Execution", "file": "execution.md", "description": "Per-connection/per-phase execution results, secondary-benchmark sections, latency, errors, warnings."})

    monitoring_sections, monitoring_provenance = _build_monitoring_sections(
        experiment, benchmark.evaluator, connections_sorted, monitoring_applications, result_dir, report_dir,
    )
    monitoring_summary_lines = _build_monitoring_summary_lines(monitoring_sections)
    if monitoring_sections:
        _write_tier2_file(
            report_dir, "monitoring.md", "monitoring",
            "SUT CPU/RAM/application monitoring, and the full catalog of every collected metric.",
            monitoring_sections, connections_index, monitoring_provenance,
        )
        written_sections.append({"title": "Monitoring", "file": "monitoring.md", "description": "CPU/RAM/application metrics plus the full metric catalog (all configured Prometheus metrics, not just the curated few)."})

    total_restarts, restarts_per_pod = _count_sut_restarts(result_dir)
    if not df_connections.empty:
        connections_lines = _build_connections_md_lines(df_connections, result_dir, report_dir, restarts_per_pod)
        _write_file(report_dir / "connections.md", _frontmatter({
            "schema_version": SCHEMA_VERSION, "section": "connections", "parent": "index.md",
        }) + "\n".join(connections_lines))
        written_sections.append({"title": "Connections", "file": "connections.md", "description": "One subsection per connection/pod: its own parameters, logs, monitoring, and SUT container detail."})

    key_metrics_lines: list[str] = []
    if key_metrics_section is not None:
        key_metrics_lines = _render_sections([key_metrics_section], connections_index)

    _write_index_md(
        report_dir, experiment, total_restarts, extra_context, written_sections,
        key_metrics_lines, monitoring_summary_lines,
    )


def _write_tier2_file(
    report_dir: Path, filename: str, section_tag: str, description: str,
    sections: list[Section], connections_index: dict[str, str], provenance_lines: list[str],
) -> None:
    """
    Render a list of top-level sections into one tier-2 Markdown file, with
    frontmatter and a ``### Provenance`` footer.

    :param report_dir: The ``report/`` directory.
    :param filename: Output filename, e.g. ``"workflow.md"``.
    :param section_tag: Frontmatter ``section`` value.
    :param description: One-line description, unused in the file body itself
        (surfaced from ``index.md``'s section links instead) — kept as a
        parameter for callers to pass consistently.
    :param sections: Top-level sections to render.
    :param connections_index: Map of connection name to ``connections.md`` anchor slug.
    :param provenance_lines: Pre-built Markdown lines for the ``### Provenance``
        footer (glob-derived by the caller via :func:`_glob_provenance`) —
        a mix of italic description lines and ``- [name](path)`` bullet
        lines; only the bullet lines are extracted into the frontmatter's
        ``provenance`` path list.
    """
    del description  # documented for callers; not rendered into the file body itself
    body_lines = _render_sections(sections, connections_index)
    provenance_paths = [
        line.split("](", 1)[1].rstrip(")") for line in provenance_lines if line.startswith("- [")
    ]
    text = _frontmatter({
        "schema_version": SCHEMA_VERSION, "section": section_tag, "parent": "index.md",
        "provenance": provenance_paths,
    })
    text += "\n".join(body_lines).strip("\n") + "\n"
    if provenance_lines:
        text += "\n### Provenance\n\n" + "\n".join(provenance_lines).strip("\n") + "\n"
    _write_file(report_dir / filename, text)


def _write_file(path: Path, text: str) -> None:
    """
    Write ``text`` to ``path``, overwriting any previous report from an
    earlier ``-rp`` run of the same experiment.

    :param path: Destination file path.
    :param text: File content.
    """
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def _write_index_md(
    report_dir: Path, experiment, total_restarts: int, extra_context: dict, written_sections: list[dict],
    key_metrics_lines: list[str], monitoring_summary_lines: list[str],
) -> None:
    """
    Write ``index.md`` — the tier-1 entry point.

    Content, in order: frontmatter; Workload identity; entry-point
    instruction; Report Structure (tier table); Naming Conventions;
    Validity-First Rules; ``### Tests``; Key Metrics; Monitoring (brief);
    Health Summary; Interpretation Rules; links to whichever tier-2 files
    were actually written.

    :param report_dir: The ``report/`` directory.
    :param experiment: The owning experiment object.
    :param total_restarts: Total SUT container restart count, from
        :func:`_count_sut_restarts`.
    :param extra_context: Extra context dict from ``_show_extra_sections()``.
    :param written_sections: List of ``{"title", "file", "description"}``
        dicts, one per tier-2 file actually written by
        :func:`write_markdown_report` — this, not a hand-written constant,
        is what the frontmatter's ``sections`` field and the body's link list
        are both built from.
    :param key_metrics_lines: Pre-rendered Markdown lines for the benchmark's
        headline performance metric(s) (see
        ``benchmark._build_key_metrics_section()``), or empty when this
        benchmark type defines none.
    :param monitoring_summary_lines: Pre-rendered Markdown lines for the
        brief ``### Monitoring`` block (see
        :func:`_build_monitoring_summary_lines`), or empty when monitoring
        was not active or collected no data.
    """
    passed = sum(1 for p, _ in experiment._test_results if p is True)
    failed = sum(1 for p, _ in experiment._test_results if p is False)
    skipped = sum(1 for p, _ in experiment._test_results if p is None)
    frontmatter = _frontmatter({
        "schema_version": SCHEMA_VERSION,
        "experiment_code": experiment.code,
        "workload_type": experiment.workload.get('type', ''),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "benchmarking_active": experiment.benchmarking_is_active(),
        "loading_active": experiment.loading_is_active(),
        "overall_status": {"passed": passed, "failed": failed, "skipped": skipped},
        "sections": [{"title": s["title"], "file": s["file"]} for s in written_sections],
    })
    lines: list[str] = []
    lines.extend(_build_workload_identity_lines(experiment.workload, experiment.code))
    lines.append("")
    lines.append(_ENTRY_POINT_MD)
    lines.append("")
    lines.append(_TIER_TABLE_MD)
    lines.append(_NAMING_CONVENTIONS_MD)
    lines.append(_VALIDITY_RULES_MD)
    lines.extend(_build_tests_lines(experiment._test_results))
    if key_metrics_lines:
        lines.append("")
        lines.extend(key_metrics_lines)
    if monitoring_summary_lines:
        lines.append("")
        lines.extend(monitoring_summary_lines)
    lines.append("")
    lines.extend(_build_health_summary_lines(total_restarts, extra_context))
    lines.append("")
    lines.append(_INTERPRETATION_RULES_MD)
    if written_sections:
        lines.append("### Sections")
        lines.append("")
        for section in written_sections:
            lines.append(f"* [{section['title']}]({section['file']}) — {section['description']}")
    text = frontmatter + "\n".join(lines).strip("\n") + "\n"
    _write_file(report_dir / "index.md", text)
