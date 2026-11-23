"""Tests for scripts/_reorder_flags.py and scripts/_sync_ps.py: they must never change what a call does.

Cases that broke before: a second value of ``-dbms A B`` was dropped, a repeated ``--set`` was
dropped as a duplicate, flags missing from the canonical order moved to the end of the call, a
call without flags (``bexhoma experiment <yaml>``) was rewritten into ``bexhoma experiment run``,
and the PS mode was always ``run``.
"""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


reorder = _load('_reorder_flags')
sync_ps = _load('_sync_ps')

SH_MULTI = """# -dbms PostgreSQL PgDuckDB      DBMS to test
# -sf 1                         scaling factor
# --set a=1                     first setting
# --set b=2                     second setting
# -ar                           reset before each round
bexhoma tpch \\
  -sf 1 \\
  --set a=1 \\
  -dbms PostgreSQL PgDuckDB \\
  -ar \\
  --set b=2 \\
  load &>$LOG_DIR/docs_x.log
"""

SH_ONE_LINE = "bexhoma experiment tests/yaml_experiments/x.yaml &>$LOG_DIR/docs_yaml.log\n"


class ReorderFlagsTest(unittest.TestCase):

    def run_on(self, text: str, suffix: str = '.sh') -> str:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / f'test-docs-x{suffix}'
            path.write_text(text, encoding='utf-8', newline='\n')
            process = reorder.process_sh_file if suffix == '.sh' else reorder.process_ps1_file
            process(path)
            return path.read_text(encoding='utf-8')

    def test_values_and_repeated_flags_are_kept(self) -> None:
        out = self.run_on(SH_MULTI)
        self.assertIn('  -dbms PostgreSQL PgDuckDB \\\n', out)
        self.assertIn('  --set a=1 \\\n', out)
        self.assertIn('  --set b=2 \\\n', out)
        self.assertIn('  load &>$LOG_DIR/docs_x.log\n', out)
        self.assertLess(out.index('  -dbms'), out.index('  -sf'))

    def test_repeated_flags_keep_their_own_descriptions(self) -> None:
        out = self.run_on(SH_MULTI)
        self.assertRegex(out, r'# --set a=1 +first setting\n')
        self.assertRegex(out, r'# --set b=2 +second setting\n')

    def test_unknown_flag_stays_after_its_predecessor(self) -> None:
        commands = [line.strip() for line in self.run_on(SH_MULTI).splitlines() if line.startswith('  -')]
        # -ar followed -dbms; it must not move to the end
        self.assertEqual(commands[commands.index('-dbms PostgreSQL PgDuckDB \\') + 1], '-ar \\')

    def test_a_second_run_changes_nothing(self) -> None:
        """A flag without comment gets '# -flag value'; reading that back must not make it a description."""
        text = SH_MULTI.replace('# -sf 1                         scaling factor\n', '')
        once = self.run_on(text)
        self.assertIn('# -sf 1\n', once)
        self.assertEqual(self.run_on(once), once)

    def test_a_comment_of_a_flag_with_several_values_keeps_them_once(self) -> None:
        once = self.run_on(SH_MULTI)
        self.assertRegex(once, r'# -dbms PostgreSQL PgDuckDB +DBMS to test\n')
        self.assertEqual(self.run_on(once), once)

    def test_one_line_call_is_left_alone(self) -> None:
        text = "# comment\n" + SH_ONE_LINE
        self.assertEqual(self.run_on(text), text)

    def test_ps1_repeated_flags_are_kept(self) -> None:
        text = ("bexhoma tpch `\n"
                "  --set a=1                     <# first #> `\n"
                "  -dbms A B                     <# DBMS #> `\n"
                "  --set b=2                     <# second #> `\n"
                "  run 2>&1 | Out-File \"$LOG_DIR\\docs_x.log\" -Encoding utf8\n")
        out = self.run_on(text, '.ps1')
        self.assertIn('-dbms A B', out)
        self.assertEqual(out.count('--set'), 2)


class SyncPsTest(unittest.TestCase):

    def sh_info(self, text: str, logfile: str) -> dict:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'test-docs-x.sh'
            path.write_text(text, encoding='utf-8', newline='\n')
            return sync_ps.extract_sh_commands(path)[logfile]

    def test_multi_value_repeated_flags_and_mode(self) -> None:
        block = sync_ps.sh_to_ps_block(self.sh_info(SH_MULTI, 'docs_x.log'), 'docs_x.log')
        self.assertEqual(block[0], 'bexhoma tpch `')
        self.assertTrue(any(line.startswith('  -dbms PostgreSQL PgDuckDB ') for line in block))
        self.assertEqual(sum(line.startswith('  --set ') for line in block), 2)
        self.assertTrue(any('--set b=2' in line and '<# second setting #>' in line for line in block))
        self.assertEqual(block[-1], '  load 2>&1 | Out-File "$LOG_DIR\\docs_x.log" -Encoding utf8')

    def test_one_line_call_stays_one_line(self) -> None:
        block = sync_ps.sh_to_ps_block(self.sh_info(SH_ONE_LINE, 'docs_yaml.log'), 'docs_yaml.log')
        self.assertEqual(block, ['bexhoma experiment tests/yaml_experiments/x.yaml '
                                 '2>&1 | Out-File "$LOG_DIR\\docs_yaml.log" -Encoding utf8'])

    def test_generated_block_compares_equal_to_its_source(self) -> None:
        for text, logfile in ((SH_MULTI, 'docs_x.log'), (SH_ONE_LINE, 'docs_yaml.log')):
            info = self.sh_info(text, logfile)
            block = sync_ps.sh_to_ps_block(info, logfile)
            self.assertEqual(sync_ps._comparable(sync_ps.call_from_ps_block(block)),
                             sync_ps._comparable(sync_ps.call_from_sh(info)))

    def test_ps_quotes_do_not_count_as_a_difference(self) -> None:
        sh = sync_ps.parse_call(['bexhoma', 'tpch', '-ne', '1,2', 'run'])
        ps = sync_ps.call_from_ps_block(['bexhoma tpch `', '  -ne "1,2"   <# x #> `',
                                         '  run 2>&1 | Out-File "$LOG_DIR\\a.log" -Encoding utf8'])
        self.assertEqual(sync_ps._comparable(sh), sync_ps._comparable(ps))

    def test_lost_second_dbms_is_a_difference(self) -> None:
        sh = sync_ps.parse_call(['bexhoma', 'tpch', '-dbms', 'A', 'B', 'run'])
        ps = sync_ps.parse_call(['bexhoma', 'tpch', '-dbms', 'A', 'run'])
        self.assertNotEqual(sync_ps._comparable(sh), sync_ps._comparable(ps))


if __name__ == '__main__':
    unittest.main()
