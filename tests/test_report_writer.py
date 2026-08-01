"""
Unit tests for :mod:`bexhoma.report_writer`.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from bexhoma import report_writer


class ConnectionsMdMetricProvenanceTest(unittest.TestCase):
    """The monitoring-CSV Provenance links in connections.md must appear once,
    not once per connection. The combined query_{component}_metric_{key}.csv
    files hold every connection's own column merged together, so unlike the
    per-connection benchmarker/SUT log links, they aren't connection-specific
    and don't belong inside each per-connection subsection."""

    def test_metric_links_appear_once_for_multiple_connections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            report_dir = result_dir / 'report'
            report_dir.mkdir()
            (result_dir / 'query_benchmarking_metric_total_cpu_util.csv').write_text('a,b\n1,2\n')
            (result_dir / 'query_benchmarking_metric_total_cpu_memory.csv').write_text('a,b\n1,2\n')

            df_connections = pd.DataFrame([
                {'connection': 'postgresql-1-1-1-1-1', 'configuration': 'postgresql-1'},
                {'connection': 'postgresql-1-1-1-1-2', 'configuration': 'postgresql-1'},
            ])
            lines = report_writer._build_connections_md_lines(df_connections, result_dir, report_dir, {})

        toplevel_provenance_sections = [l for l in lines if l == '### Provenance']
        metric_link_lines = [l for l in lines if 'query_benchmarking_metric_total_cpu_util.csv]' in l]
        self.assertEqual(len(toplevel_provenance_sections), 1)
        self.assertEqual(len(metric_link_lines), 1)


class GlobProvenanceExcludeTest(unittest.TestCase):
    """Input-provenance files (experiment.yml, contract_catalog.yml, ...) must
    not be swept up and mislabeled by the workflow section's broad
    *.yml/*.yaml manifest glob -- see report_writer._INPUT_PROVENANCE_FILENAMES."""

    def test_excluded_name_is_dropped_even_though_pattern_matches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            report_dir = result_dir / 'report'
            report_dir.mkdir()
            (result_dir / 'bexhoma-sut-postgresql-1-123.yml').write_text('kind: Deployment\n')
            (result_dir / 'experiment.yml').write_text('title: x\n')

            lines = report_writer._glob_provenance(
                result_dir, report_dir, ['*.yml', '*.yaml'], 'manifests',
                exclude=frozenset({'experiment.yml'}),
            )

        joined = '\n'.join(lines)
        self.assertIn('bexhoma-sut-postgresql-1-123.yml', joined)
        self.assertNotIn('experiment.yml', joined)

    def test_no_exclusion_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            report_dir = result_dir / 'report'
            report_dir.mkdir()
            (result_dir / 'experiment.yml').write_text('title: x\n')

            lines = report_writer._glob_provenance(result_dir, report_dir, ['*.yml'], 'manifests')

        self.assertIn('experiment.yml', '\n'.join(lines))


class WorkflowSectionInputProvenanceTest(unittest.TestCase):
    """The workflow.md manifest glob must exclude the known input-provenance
    filenames, and those files must instead surface under their own,
    accurately-described entry -- not be mislabeled as K8s manifests."""

    def test_input_files_excluded_from_manifest_description(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            result_dir = Path(tmp_dir)
            report_dir = result_dir / 'report'
            report_dir.mkdir()
            (result_dir / 'bexhoma-sut-postgresql-1-123.yml').write_text('kind: Deployment\n')
            (result_dir / 'experiment.yml').write_text('title: x\n')
            (result_dir / 'contract_catalog.yml').write_text('workloads: {}\n')

            manifest_lines = report_writer._glob_provenance(
                result_dir, report_dir, ["*.yml", "*.yaml"],
                "Rendered Kubernetes Job/Deployment/Service manifests actually submitted",
                exclude=report_writer._INPUT_PROVENANCE_FILENAMES,
            )
            input_lines = report_writer._glob_provenance(
                result_dir, report_dir, sorted(report_writer._INPUT_PROVENANCE_FILENAMES),
                "The experiment.yml this run was actually built from",
            )

        manifest_joined = '\n'.join(manifest_lines)
        input_joined = '\n'.join(input_lines)
        self.assertIn('bexhoma-sut-postgresql-1-123.yml', manifest_joined)
        self.assertNotIn('experiment.yml', manifest_joined)
        self.assertNotIn('contract_catalog.yml', manifest_joined)
        self.assertIn('experiment.yml', input_joined)
        self.assertIn('contract_catalog.yml', input_joined)


if __name__ == '__main__':
    unittest.main()
