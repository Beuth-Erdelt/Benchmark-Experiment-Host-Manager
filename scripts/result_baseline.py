"""
Result baseline: check that a refactoring does not change what bexhoma makes of finished experiments.

The configuration snapshots (``tests/test_dbms_snapshots.py``) cover what an entry script
*builds*. This tool covers the other half, what comes *out*: for a selection of finished
runs it re-runs ``bexhoma summary -e <code> -rp`` on a copy of the result folder and keeps

* the printed summary (``summary.txt``),
* the Markdown report (``report/``),
* the DataFrames the evaluators derive from the logs (``frames/*.csv``, full precision),
* the table behind every section of the summary, before it is formatted for printing
  (``tables/*.csv``, full precision).

Everything but the tables is taken from stdout and from files, nothing from bexhoma's
classes, so the tool keeps working while the classes are moved and renamed. The tables
are taken where the sections are rendered (``_render_section_stdout`` of
:mod:`bexhoma.benchmarks.base`, and the sections handed to the report writer); if that
function is ever moved, the tool says so instead of silently recording no tables.

A run is summarized twice:

``cached``
    The result folder as it is. Exercises the summary, the tests and the report.
``recompute``
    Without the ``*.df.pickle`` files, so the evaluators parse the logs again. Exercises
    the log parsers; the DataFrames are dumped only in this mode.

The runs are the ones recorded in ``logs_tests/`` (:data:`RUNS`); the experiment code is
read from the *committed* log, so a rerun in progress does not change the selection.
Result folders are looked up in the result folder of ``cluster.config`` and, where they
are missing, fetched from ``/results`` of the dashboard pod (a compressed archive is
streamed out of the pod; nothing is written there, and an existing local folder is never
overwritten).

Usage (from the repository root)::

    python scripts/result_baseline.py list              # the selection, and where each result folder is
    python scripts/result_baseline.py fetch             # download the missing result folders from the pod
    python scripts/result_baseline.py record            # write the baseline (before the refactoring)
    python scripts/result_baseline.py compare           # compare the current code with the baseline

``record`` and ``compare`` take ``-k <text>`` to restrict the runs by name. The baseline
lives in ``logs_tests/local/result_baseline/`` (git-ignored): it is derived from result
folders that are not part of the repository.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BASELINE = os.path.join(_REPO, 'logs_tests', 'local', 'result_baseline')
MODES = ('cached', 'recompute')

#: The selected runs (names of ``logs_tests/<name>.log``), by group. The selection covers,
#: per benchmark, the phases (run/load/start), monitoring, storage, scale-out, tenants,
#: several DBMS, the reset and durability cases and the variants only that benchmark has.
RUNS = {
    'benchbase': [
        'docs_benchbase_postgresql_run', 'docs_benchbase_postgresql_load',
        'docs_benchbase_postgresql_start',
        'docs_benchbase_postgresql_monitoring', 'docs_benchbase_postgresql_scale', 'docs_benchbase_postgresql_storage',
        'docs_benchbase_postgresql_appmetrics', 'docs_benchbase_postgresql_keytime',
        'docs_benchbase_postgresql_tenants_container', 'docs_benchbase_postgresql_tenants_database',
        'docs_benchbase_postgresql_tenants_schema', 'docs_benchbase_postgresql_twitter_simple',
        'docs_benchbase_postgresql_chbenchmark_simple', 'docs_benchbase_postgresql_ycsb_a',
        'docs_benchbase_postgresql_collector_1', 'docs_benchbase_cockroachdb', 'docs_benchbase_citus',
        'docs_benchbase_pgbouncer_appmetrics', 'docs_reset_benchbase_postgresql',
        'docs_durability_benchbase_postgresql_relaxed',
    ],
    'hammerdb': [
        'docs_hammerdb_postgresql_load',
        'docs_hammerdb_postgresql_run', 'docs_hammerdb_postgresql_start',
        'docs_hammerdb_postgresql_monitoring', 'docs_hammerdb_postgresql_scale', 'docs_hammerdb_postgresql_storage',
        'docs_hammerdb_postgresql_appmetrics', 'docs_hammerdb_postgresql_keytime', 'docs_hammerdb_postgresql_timeseries',
        'docs_hammerdb_mariadb', 'docs_hammerdb_citus', 'docs_reset_hammerdb_postgresql',
        'docs_durability_hammerdb_postgresql_relaxed',
    ],
    'tpch': [
        'docs_tpch_postgresql', 'docs_tpch_postgresql_run', 'docs_tpch_postgresql_load', 'docs_tpch_postgresql_start',
        'docs_tpch_postgresql_monitoring', 'docs_tpch_postgresql_storage', 'docs_tpch_postgresql_appmetrics',
        'docs_tpch_postgresql_refresh', 'docs_tpch_postgresql_throughput', 'docs_tpch_postgresql_tenants_container',
        'docs_tpch_postgresql_tenants_database', 'docs_tpch_postgresql_tenants_schema',
        'docs_tpch_postgresql_tenants_database_multiload', 'docs_tpch_postgresql_subset',
        'docs_tpch_postgresql_fractional', 'docs_tpch_pgduckdb', 'docs_tpch_clickhouse_cluster',
        'docs_tpch_monetdb_refresh', 'docs_tpch_monetdb_sf100_repeated', 'docs_tpch_mariadbcs',
        'docs_reset_tpch_postgresql', 'docs_reset_tpch_refresh_postgresql', 'docs_durability_tpch_postgresql_relaxed',
    ],
    'tpcds': [
        'docs_tpcds_postgresql', 'docs_tpcds_postgresql_run', 'docs_tpcds_postgresql_load', 'docs_tpcds_postgresql_start',
        'docs_tpcds_postgresql_monitoring', 'docs_tpcds_postgresql_storage', 'docs_tpcds_postgresql_throughput',
        'docs_tpcds_postgresql_profiling', 'docs_tpcds_compare', 'docs_tpcds_mariadb', 'docs_reset_tpcds_postgresql',
        'docs_durability_tpcds_postgresql_relaxed',
    ],
    'ssb': [
        'docs_ssb_postgresql', 'docs_ssb_flat', 'docs_ssb_load', 'docs_ssb_monitoring', 'docs_ssb_storage',
        'docs_ssb_profiling', 'docs_ssb_random', 'docs_ssb_clickhousecluster_distributed', 'docs_ssb_monetdb',
    ],
    'ycsb': [
        'docs_ycsb_postgresql_run',
        'docs_ycsb_postgresql_load', 'docs_ycsb_postgresql_start',
        'docs_ycsb_postgresql_monitoring', 'docs_ycsb_postgresql_storage', 'docs_ycsb_postgresql_appmetrics',
        'docs_ycsb_postgresql_loading', 'docs_ycsb_postgresql_benchmarking', 'docs_ycsb_postgresql_reset',
        'docs_ycsb_postgresql_wl_a', 'docs_ycsb_postgresql_wl_e', 'docs_ycsb_redis', 'docs_ycsb_redis_cluster',
        'docs_ycsb_valkey_replica', 'docs_ycsb_cassandra', 'docs_ycsb_mysql_scale', 'docs_ycsb_pgbouncer',
        'docs_ycsb_tidb', 'docs_reset_ycsb_postgresql', 'docs_durability_ycsb_postgresql_relaxed',
    ],
    'hardware': [
        'docs_hardware_fio_blocksize_sweep', 'docs_hardware_fio_depth_sweep', 'docs_hardware_fio_random_page_cost',
        'docs_hardware_fio_wal_sync_fsync', 'docs_hardware_sysbench_cpu_quota_calibration',
        'docs_hardware_sysbench_nbp_overhead_sweep', 'docs_hardware_sysbench_noisy_neighbor',
        'docs_hardware_sockperf_pod_scaling_sweep', 'docs_hardware_sockperf_postgresql_query_latency',
        'docs_hardware_netperf_postgresql_pod_scaling_sweep', 'docs_hardware_netperf_postgresql_query_latency',
    ],
}


# ---------------------------------------------------------------------------- selection

def result_folder() -> str:
    """The result folder of ``cluster.config``."""
    with open(os.path.join(_REPO, 'cluster.config'), encoding='utf-8') as file:
        return ast.literal_eval(file.read())['benchmarker']['resultfolder']


def code_of(name: str) -> str | None:
    """The experiment code in the committed ``logs_tests/<name>.log``, ``None`` if there is none."""
    shown = subprocess.run(['git', 'show', f'HEAD:logs_tests/{name}.log'], cwd=_REPO, capture_output=True)
    if shown.returncode != 0:
        return None
    match = re.search(r'has code (\d+)', shown.stdout.decode('utf-8', errors='replace'))
    return match.group(1) if match else None


def selection(keyword: str = '') -> list:
    """``[(group, name, code)]`` of the selected runs whose name contains ``keyword``."""
    return [(group, name, code_of(name)) for group, names in RUNS.items() for name in names if keyword in name]


# ---------------------------------------------------------------------------- pod

def dashboard_pod() -> str:
    """Name of the running dashboard pod."""
    names = subprocess.run(['kubectl', 'get', 'pods', '-o', 'name'], capture_output=True, text=True, check=True).stdout
    pods = [line.split('/', 1)[1] for line in names.splitlines() if 'bexhoma-dashboard' in line]
    if not pods:
        raise SystemExit('no bexhoma-dashboard pod found in the current context')
    return pods[0]


def _kubectl_exec(pod: str, command: str, **kwargs) -> subprocess.CompletedProcess:
    # MSYS_NO_PATHCONV: Git Bash would rewrite /results into a Windows path
    environment = dict(os.environ, MSYS_NO_PATHCONV='1')
    return subprocess.run(['kubectl', 'exec', pod, '-c', 'dashboard', '--', 'sh', '-c', command], env=environment, **kwargs)


def pod_sizes(pod: str, codes: list) -> dict:
    """``{code: size in kB}`` of the result folders that exist in the pod."""
    listing = _kubectl_exec(pod, 'cd /results && du -sk ' + ' '.join(codes) + ' 2>/dev/null; true',
                            capture_output=True, text=True).stdout
    return {line.split()[1]: int(line.split()[0]) for line in listing.splitlines() if len(line.split()) == 2}


def fetch(code: str, pod: str, target_root: str) -> None:
    """Stream ``/results/<code>`` out of the pod as a compressed archive and unpack it into ``target_root``."""
    target = os.path.join(target_root, code)
    if os.path.exists(target):
        raise FileExistsError(target)
    with tempfile.TemporaryDirectory() as tmp_dir:
        archive = os.path.join(tmp_dir, code + '.tar.gz')
        with open(archive, 'wb') as file:
            done = _kubectl_exec(pod, f'tar czf - -C /results {code}', stdout=file, stderr=subprocess.PIPE)
        if done.returncode != 0:
            raise RuntimeError(done.stderr.decode('utf-8', errors='replace')[:500])
        unpacked = os.path.join(tmp_dir, 'unpacked')
        with tarfile.open(archive) as tar:
            tar.extractall(unpacked, filter='data')
        # moved in one step, so an interrupted download leaves no half result folder
        shutil.move(os.path.join(unpacked, code), target)


# ---------------------------------------------------------------------------- one summary

#: Runs inside the subprocess: the result folder of cluster.config is replaced by the copy.
_RUNNER = r'''
import sys
from bexhoma import clusters
copy_root = sys.argv.pop(1)
original = clusters.Kubernetes.__init__
def init(self, *args, **kwargs):
    original(self, *args, **kwargs)
    self.config['benchmarker']['resultfolder'] = copy_root
    self.resultfolder = copy_root.replace("\\", "/").replace("C:", "")
clusters.Kubernetes.__init__ = init

# the table of every summary section, as data: dumped where a section is rendered
import os, re
from bexhoma.benchmarks import base as benchmark_base
from bexhoma import report_writer
tables_folder = os.environ['BEXHOMA_BASELINE_TABLES']
os.makedirs(tables_folder, exist_ok=True)
counter = [0]
def dump(section, origin):
    frame = getattr(section, 'dataframe', None)
    if frame is None:
        return
    counter[0] += 1
    slug = re.sub(r'[^a-z0-9]+', '-', str(section.heading).lower()).strip('-')[:60]
    frame.to_csv(os.path.join(tables_folder, f'{counter[0]:03d}-{origin}-{slug}.csv'),
                 lineterminator='\n', float_format='%.12g')
render_section = benchmark_base._render_section_stdout
def render_and_dump(section):
    dump(section, 'summary')
    render_section(section)
benchmark_base._render_section_stdout = render_and_dump
write_report = report_writer.write_markdown_report
def walk(section):
    if section is not None:
        dump(section, 'report')
        for child in section.children:
            walk(child)
def write_report_and_dump(*args, **kwargs):
    # the sections that only the report shows; the others were dumped when printed
    for name in ('key_metrics_section', 'explain_section'):
        walk(kwargs.get(name))
    return write_report(*args, **kwargs)
report_writer.write_markdown_report = write_report_and_dump

from bexhoma.scripts.experimentsmanager import manage
manage()
'''


def _normalize(text: str, copy_root: str) -> str:
    """Mask what differs between two summaries of the same result folder: the place of the copy and the time."""
    for form in {copy_root, copy_root.replace('\\', '/'), copy_root.replace('\\', '\\\\'),
                 copy_root.replace('\\', '/').replace('C:', '')}:
        text = text.replace(form, '<RESULTS>')
    # the report states when it was written
    text = re.sub(r"(generated_at: )'[^']*'", r"\1'<NOW>'", text)
    return text.replace('\r\n', '\n')


#: Workload types that were renamed since the result folders were written. bexhoma itself keeps
#: no alias for an old name; the copy that is summarized gets the new one.
_RENAMED_WORKLOAD_TYPES = {'tpcc': 'hammerdb'}


def _rename_workload_types(folder: str) -> None:
    """Replace renamed workload types in the ``queries.config`` of a copied result folder."""
    path = os.path.join(folder, 'queries.config')
    if not os.path.isfile(path):
        return
    with open(path, encoding='utf-8', newline='') as file:
        text = file.read()
    changed = text
    for old, new in _RENAMED_WORKLOAD_TYPES.items():
        changed = changed.replace(f"'type': '{old}'", f"'type': '{new}'")
    if changed != text:
        with open(path, 'w', encoding='utf-8', newline='') as file:
            file.write(changed)


def summarize(code: str, mode: str, source_root: str, target: str) -> dict:
    """Summarize a copy of the result folder of ``code`` and write what comes out to ``target``.

    :return: ``{'returncode': ..., 'seconds': ...}``.
    """
    import pandas as pd
    shutil.rmtree(target, ignore_errors=True)
    os.makedirs(target)
    with tempfile.TemporaryDirectory() as copy_root:
        folder = os.path.join(copy_root, code)
        shutil.copytree(os.path.join(source_root, code), folder)
        # a report of an earlier summary is output, not input
        shutil.rmtree(os.path.join(folder, 'report'), ignore_errors=True)
        _rename_workload_types(folder)
        if mode == 'recompute':
            for name in os.listdir(folder):
                if name.endswith('.df.pickle'):
                    os.remove(os.path.join(folder, name))
        start = time.time()
        done = subprocess.run([sys.executable, '-c', _RUNNER, copy_root, 'summary', '-e', code, '-rp'],
                              cwd=_REPO, capture_output=True,
                              env=dict(os.environ, PYTHONIOENCODING='utf-8',
                                       BEXHOMA_BASELINE_TABLES=os.path.join(target, 'tables')))
        seconds = round(time.time() - start, 1)
        output = done.stdout.decode('utf-8', errors='replace')
        errors = done.stderr.decode('utf-8', errors='replace')
        with open(os.path.join(target, 'summary.txt'), 'w', encoding='utf-8', newline='\n') as file:
            file.write(_normalize(output, copy_root))
        if done.returncode != 0:
            with open(os.path.join(target, 'error.txt'), 'w', encoding='utf-8', newline='\n') as file:
                file.write(_normalize(errors, copy_root))
        report = os.path.join(folder, 'report')
        if os.path.isdir(report):
            for directory, _, names in os.walk(report):
                for name in names:
                    source = os.path.join(directory, name)
                    destination = os.path.join(target, 'report', os.path.relpath(source, report))
                    os.makedirs(os.path.dirname(destination), exist_ok=True)
                    if name.endswith(('.md', '.json', '.yml', '.txt', '.csv')):
                        with open(source, encoding='utf-8', errors='replace') as file:
                            text = _normalize(file.read(), copy_root)
                        with open(destination, 'w', encoding='utf-8', newline='\n') as file:
                            file.write(text)
                    else:
                        shutil.copyfile(source, destination)
        if mode == 'recompute':
            os.makedirs(os.path.join(target, 'frames'))
            for name in sorted(os.listdir(folder)):
                if name.endswith('.all.df.pickle'):
                    try:
                        frame = pd.read_pickle(os.path.join(folder, name))
                    except Exception as error:  # the baseline then records that it cannot be read
                        frame = pd.DataFrame({'unreadable': [type(error).__name__]})
                    frame.to_csv(os.path.join(target, 'frames', name[:-len('.pickle')] + '.csv'),
                                 lineterminator='\n', float_format='%.12g')
    return {'returncode': done.returncode, 'seconds': seconds}


# ---------------------------------------------------------------------------- compare

def _files(root: str) -> list:
    return sorted(os.path.relpath(os.path.join(directory, name), root).replace('\\', '/')
                  for directory, _, names in os.walk(root) for name in names)


def _frame_difference(before: str, after: str) -> str | None:
    """What differs between two dumped DataFrames, ``None`` if nothing does (floats within 1e-9)."""
    import pandas as pd
    old, new = pd.read_csv(before, index_col=0), pd.read_csv(after, index_col=0)
    notes = []
    if list(old.columns) != list(new.columns):
        removed, added = sorted(set(old.columns) - set(new.columns)), sorted(set(new.columns) - set(old.columns))
        if removed or added:
            notes.append(f'columns removed {removed}, added {added}')
        else:
            notes.append('column order')
    if old.shape[0] != new.shape[0]:
        notes.append(f'rows {old.shape[0]} -> {new.shape[0]}')
        return '; '.join(notes)
    common = [column for column in old.columns if column in new.columns]
    try:
        pd.testing.assert_frame_equal(old[common], new[common], check_exact=False, rtol=1e-9, check_dtype=False)
    except AssertionError as error:
        notes.append(' '.join(str(error).split())[:300])
    return '; '.join(notes) or None


def differences(before: str, after: str) -> list:
    """Differences between two outputs of :func:`summarize`, as readable lines."""
    found = []
    old_files, new_files = _files(before), _files(after)
    for name in sorted(set(old_files) - set(new_files)):
        found.append(f'missing: {name}')
    for name in sorted(set(new_files) - set(old_files)):
        found.append(f'new: {name}')
    for name in sorted(set(old_files) & set(new_files)):
        old_path, new_path = os.path.join(before, name), os.path.join(after, name)
        if name.startswith(('frames/', 'tables/')):
            difference = _frame_difference(old_path, new_path)
            if difference:
                found.append(f'{name}: {difference}')
            continue
        with open(old_path, 'rb') as file:
            old = file.read()
        with open(new_path, 'rb') as file:
            new = file.read()
        if old != new:
            old_lines = old.decode('utf-8', errors='replace').splitlines()
            new_lines = new.decode('utf-8', errors='replace').splitlines()
            changed = [(a, b) for a, b in zip(old_lines, new_lines) if a != b]
            first = f' first: {changed[0][0][:110]!r} -> {changed[0][1][:110]!r}' if changed else ''
            found.append(f'{name}: {len(changed)} lines differ, {len(old_lines)} -> {len(new_lines)} lines.{first}')
    return found


# ---------------------------------------------------------------------------- commands

def command_list(args) -> int:
    root = result_folder()
    runs = selection(args.keyword)
    missing = [code for _, _, code in runs if code and not os.path.isdir(os.path.join(root, code))]
    sizes = pod_sizes(dashboard_pod(), missing) if missing and not args.offline else {}
    total = 0
    for group, name, code in runs:
        if code is None:
            where = 'NO CODE in the committed log'
        elif os.path.isdir(os.path.join(root, code)):
            where = 'local'
        elif code in sizes:
            where = f'pod, {sizes[code] / 1024:.1f} MB'
            total += sizes[code]
        else:
            where = 'missing locally' if args.offline else 'NOT FOUND (neither local nor in the pod)'
        print(f'{group:10s} {name:55s} {code or "-":12s} {where}')
    print(f'{len(runs)} runs, {len(missing)} not local, {total / 1024:.0f} MB to fetch')
    return 0


def command_fetch(args) -> int:
    root = result_folder()
    pod = dashboard_pod()
    todo = [(name, code) for _, name, code in selection(args.keyword)
            if code and not os.path.isdir(os.path.join(root, code))]
    failed = 0
    for position, (name, code) in enumerate(todo, 1):
        try:
            fetch(code, pod, root)
            print(f'[{position}/{len(todo)}] {code} {name}', flush=True)
        except Exception as error:
            failed += 1
            print(f'[{position}/{len(todo)}] {code} {name} FAILED: {error}', flush=True)
    print(f'{len(todo) - failed} fetched, {failed} failed')
    return 1 if failed else 0


def _run_all(args, into: str) -> dict:
    root = result_folder()
    results = {}
    runs = [(group, name, code) for group, name, code in selection(args.keyword)
            if code and os.path.isdir(os.path.join(root, code))]
    for position, (group, name, code) in enumerate(runs, 1):
        for mode in MODES:
            outcome = summarize(code, mode, root, os.path.join(into, name, mode))
            results[f'{name}/{mode}'] = dict(outcome, code=code, group=group)
            print(f'[{position}/{len(runs)}] {name} {mode}: exit {outcome["returncode"]}, {outcome["seconds"]}s', flush=True)
    return results


def command_record(args) -> int:
    os.makedirs(_BASELINE, exist_ok=True)
    manifest_path = os.path.join(_BASELINE, 'manifest.json')
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, encoding='utf-8') as file:
            manifest = json.load(file)
    manifest.update(_run_all(args, _BASELINE))
    with open(manifest_path, 'w', encoding='utf-8', newline='\n') as file:
        json.dump(manifest, file, indent=1, sort_keys=True)
    failed = sorted(key for key, value in manifest.items() if value['returncode'] != 0)
    print(f'{len(manifest)} summaries in the baseline, {len(failed)} of them end with an error (recorded as such)')
    for key in failed:
        print('  error: ' + key)
    return 0


def command_compare(args) -> int:
    manifest_path = os.path.join(_BASELINE, 'manifest.json')
    if not os.path.exists(manifest_path):
        raise SystemExit('no baseline; run "record" first')
    with open(manifest_path, encoding='utf-8') as file:
        manifest = json.load(file)
    changed, stale = 0, 0
    with tempfile.TemporaryDirectory() as current:
        with contextlib.redirect_stdout(io.StringIO()) if args.quiet else contextlib.nullcontext():
            results = _run_all(args, current)
        for key in sorted(results):
            if key not in manifest:
                print(f'NOT IN BASELINE {key}')
                continue
            if manifest[key]['code'] != results[key]['code']:
                # the test was run again and its log committed: another experiment, nothing to compare
                stale += 1
                print(f'STALE {key}: baseline is of experiment {manifest[key]["code"]}, the log now names '
                      f'{results[key]["code"]}; record it again')
                continue
            found = differences(os.path.join(_BASELINE, key), os.path.join(current, key))
            if results[key]['returncode'] != manifest[key]['returncode']:
                found.insert(0, f'exit code {manifest[key]["returncode"]} -> {results[key]["returncode"]}')
            if found:
                changed += 1
                print(f'CHANGED {key}')
                for line in found:
                    print('    ' + line)
                if args.keep:
                    shutil.copytree(os.path.join(current, key), os.path.join(args.keep, key), dirs_exist_ok=True)
    print(f'{len(results)} summaries compared, {changed} changed, {stale} stale')
    return 1 if changed or stale else 0


def main() -> int:
    parser = argparse.ArgumentParser(description='Record and compare what bexhoma makes of finished experiments.')
    parser.add_argument('command', choices=['list', 'fetch', 'record', 'compare'])
    parser.add_argument('-k', '--keyword', default='', help='only the runs whose name contains this text')
    parser.add_argument('--offline', action='store_true', help='list: do not ask the pod')
    parser.add_argument('--quiet', action='store_true', help='compare: print only the differences')
    parser.add_argument('--keep', default=None, help='compare: copy the output of the changed runs to this folder')
    args = parser.parse_args()
    return {'list': command_list, 'fetch': command_fetch, 'record': command_record, 'compare': command_compare}[args.command](args)


if __name__ == '__main__':
    sys.exit(main())
