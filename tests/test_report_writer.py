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


if __name__ == '__main__':
    unittest.main()
