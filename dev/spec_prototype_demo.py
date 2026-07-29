"""
Demo/verification script for bexhoma/spec.py — the catalog.yaml + experiment.yml
translator (see docs/Design-Catalog-Contract.md).

Translates dev/catalog/experiment.yml against dev/catalog/catalog.yaml,
prints the resulting tpch.py argument vector and command line, and parses that argv
through a parser mirroring tpch.py's own (shared flags via the real,
importable `make_base_parser()`; the handful of tpch-specific flags are
duplicated here, verbatim from tpch.py, purely so this script can validate
argv shape without a live cluster — tpch.py itself is not imported or run).

Run from the repo root: ``python dev/spec_prototype_demo.py``

Reads dev/catalog/catalog.yaml and dev/catalog/experiment.yml.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bexhoma import spec
from bexhoma.cli_args import make_base_parser


def _build_reference_tpch_parser() -> argparse.ArgumentParser:
    """Mirror tpch.py's own parser, for argv validation only.

    :return: A parser accepting the same flags as ``tpch.py``.
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(parents=[make_base_parser()])
    parser.add_argument('mode', choices=['profiling', 'run', 'start', 'load', 'empty', 'summary'])
    parser.add_argument('-dbms', '--dbms', choices=['PostgreSQL', 'MonetDB', 'MySQL', 'MariaDB', 'DatabaseService', 'Citus', 'CedarDB', 'PgDuckDB'], default=[], nargs='*')
    parser.add_argument('-xlit', '--xlimit-import-table', default='', dest='limit_import_table')
    parser.add_argument('-xdt', '--xdata-transfer', action='store_true', default=False, dest='datatransfer')
    parser.add_argument('-xqr', '--xnum-query-runs', default=1, dest='num_run')
    parser.add_argument('-xnls', '--xnum-loading-split', default="1", dest='num_loading_split')
    parser.add_argument('-xii', '--xinit-indexes', action='store_true', default=False, dest='init_indexes')
    parser.add_argument('-xic', '--xinit-constraints', action='store_true', default=False, dest='init_constraints')
    parser.add_argument('-xis', '--xinit-statistics', action='store_true', default=False, dest='init_statistics')
    parser.add_argument('-xcol', '--xinit-columns', action='store_true', default=False, dest='init_columns')
    parser.add_argument('-xrcp', '--xrecreate-parameter', action='store_true', default=False, dest='recreate_parameter')
    parser.add_argument('-xshq', '--xshuffle-queries', action='store_true', default=False, dest='shuffle_queries')
    parser.add_argument('-xrs', '--xnum-refresh-streams', default=0, type=int, dest='num_refresh_streams')
    parser.add_argument('-xrso', '--xrefresh-stream-offset', default=0, type=int, dest='num_refresh_stream_offset')
    parser.add_argument('-xaq', '--xactive-queries', default='', dest='active_queries')
    parser.add_argument('-xdfe', '--xduckdb-force-execution', action='store_true', default=False, dest='duckdb_force_execution')
    parser.add_argument('-xve', '--xverbose-explain', action='store_true', default=False, dest='verbose_explain')
    return parser


def main() -> None:
    """Translate experiment.yml, print the result, and validate it parses."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    catalog_dir = os.path.join(repo_root, "dev", "catalog")
    catalog_path = os.path.join(catalog_dir, "catalog.yaml")
    experiment_path = os.path.join(catalog_dir, "experiment.yml")

    catalog = spec.load_catalog(catalog_path)
    experiment = spec.load_experiment(experiment_path)
    argv = spec.build_argv(catalog, experiment)

    print("argv:")
    for token in argv:
        print(f"  {token!r}")
    print()
    print("command:")
    print(" ", spec.build_command(argv))
    print()

    parser = _build_reference_tpch_parser()
    args = parser.parse_args(argv)
    print("parsed by tpch.py's own flag shape:")
    print(" ", vars(args))


if __name__ == "__main__":
    main()
