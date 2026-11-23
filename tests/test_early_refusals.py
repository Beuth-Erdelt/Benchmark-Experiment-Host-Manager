"""Phase 0 of dev/plan-dbms-generic-verification.md, as unit tests: the command line alone decides.

0.1 ``-dbms`` offers exactly the DBMS whose cluster configuration has an entry for the benchmark.
0.2 A selection a benchmark cannot run is refused as a usage error right after parsing, before
    any Kubernetes object exists: tenancy a DBMS does not declare, ``-xdim distributed`` for a
    DBMS without that variant, ``-xrs`` for DBMS that need different refresh jobs.
"""
import contextlib
import io
import os
import re
import runpy
import sys
import unittest
from unittest import mock

from bexhoma import system_descriptors as sd

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _run_main(script: str, *argv: str) -> tuple:
    """Run an entry script's ``__main__``; a Kubernetes object fails the test.

    :return: Exit code (None if it did not exit), stdout, stderr.
    """
    stdout, stderr = io.StringIO(), io.StringIO()
    reached = AssertionError(f'{script} {" ".join(argv)} reached the cluster before refusing')
    with (
        mock.patch.object(sys, 'argv', [script, *argv]),
        mock.patch('bexhoma.clusters.Kubernetes', side_effect=reached),
        mock.patch('bexhoma.clusters.AWS', side_effect=reached),
        contextlib.redirect_stdout(stdout),
        contextlib.redirect_stderr(stderr),
    ):
        try:
            runpy.run_path(os.path.join(_REPO, script), run_name='__main__')
        except SystemExit as exit_:
            return exit_.code, stdout.getvalue(), stderr.getvalue()
    return None, stdout.getvalue(), stderr.getvalue()


class DbmsChoicesTest(unittest.TestCase):
    """0.1: the help lists the DBMS of the configuration, in its order."""

    def test_choices_follow_the_cluster_configuration(self) -> None:
        dockers = sd.load_dockers()
        for script, benchmark in (('hammerdb.py', 'hammerdb'), ('ycsb.py', 'ycsb')):
            with self.subTest(script=script):
                code, stdout, _ = _run_main(script, '-h')
                self.assertEqual(code, 0)
                listed = re.search(r'-dbms \[\{([^}]*)\}', stdout)
                self.assertIsNotNone(listed, stdout[:500])
                self.assertEqual(listed.group(1).split(','), sd.compatible_dockers(dockers, benchmark))


class RefusedBeforeTheClusterTest(unittest.TestCase):
    """0.2: each refusal is exit code 2 with the reason, and no cluster object was made."""

    def assert_refused(self, script: str, argv: list, reason: str) -> None:
        code, _, stderr = _run_main(script, 'run', *argv)
        self.assertEqual(code, 2, stderr)
        self.assertIn(reason, stderr)

    def test_tenancy_by_database_for_mysql_in_tpch(self) -> None:
        self.assert_refused('tpch.py', ['-dbms', 'MySQL', '-mtn', '2', '-mtb', 'database'],
                            'MySQL does not support this tenancy in tpch')

    def test_tenancy_by_schema_for_mysql_in_benchbase(self) -> None:
        self.assert_refused('benchbase.py', ['-dbms', 'MySQL', '-mtn', '2', '-mtb', 'schema'],
                            'MySQL does not support this tenancy in benchbase')

    def test_distributed_dimensions_for_citus(self) -> None:
        self.assert_refused('tpch.py', ['-dbms', 'Citus', '-xdim', 'distributed'],
                            '-xdim distributed is not supported for Citus')

    def test_refresh_stream_for_dbms_with_different_refresh_jobs(self) -> None:
        for other in ('ClickHouse', 'MySQL'):
            with self.subTest(other=other):
                self.assert_refused('tpch.py', ['-dbms', 'PostgreSQL', other, '-xrs', '1'],
                                    'they need different ones')

    def test_refresh_stream_for_dbms_sharing_a_refresh_job_is_not_refused_early(self) -> None:
        """The check lets a valid selection through to run(), which here meets the patched cluster."""
        with self.assertRaisesRegex(AssertionError, 'reached the cluster'):
            _run_main('tpch.py', 'run', '-dbms', 'PostgreSQL', 'PgDuckDB', '-xrs', '1')


if __name__ == '__main__':
    unittest.main()
