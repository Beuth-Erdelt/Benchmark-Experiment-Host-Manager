"""
Benchmark class for TPC-H experiments.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from types import SimpleNamespace

from .base import DBMSBenchmarkerBenchmark

__all__ = ["TPCH", "resolve_indexing_key"]

#: Maps every (indexes, constraints, statistics) combination to the tpch
#: volume's ``initscripts`` key that applies exactly that combination (see
#: ``k8s-cluster.config``'s ``volumes.tpch.initscripts``). The three post-load
#: steps are independent DDL/DML statements with no ordering dependency on
#: each other, so all eight combinations are legal.
_INDEXING_KEYS: dict[tuple[bool, bool, bool], str] = {
    (False, False, False): "",
    (True, False, False): "Index",
    (False, True, False): "Constraints",
    (False, False, True): "Statistics",
    (True, True, False): "Index_and_Constraints",
    (True, False, True): "Index_and_Statistics",
    (False, True, True): "Constraints_and_Statistics",
    (True, True, True): "Index_and_Constraints_and_Statistics",
}


def resolve_indexing_key(indexes: bool, constraints: bool, statistics: bool) -> str:
    """Map a post_load selection to its ``initscripts`` key.

    Single source of truth shared with the catalog-contract translator
    (:func:`bexhoma.experiments.tpch_catalog.resolve_physical_design_overrides`),
    which applies the same mapping to a ``systems[].post_load`` selection —
    the key strings must match ``k8s-cluster.config``'s ``volumes.tpch.initscripts``
    literally, or the resulting
    :meth:`~bexhoma.configurations.base.SutConfiguration.set_experiment` call
    raises ``KeyError``.

    :param indexes: Create indexes on all tables after loading.
    :param constraints: Add primary-key/foreign-key constraints after loading.
    :param statistics: Run ``ANALYZE`` after loading.
    :return: The matching ``initscripts`` key, or ``""`` when none of the
        three steps were requested.
    :rtype: str
    """
    return _INDEXING_KEYS[(bool(indexes), bool(constraints), bool(statistics))]


class TPCH(DBMSBenchmarkerBenchmark):
    """
    Benchmark class for TPC-H experiments using the DBMSBenchmarker tool.

    :param SF: Scaling factor — data size in GB.
    """

    def __init__(self, SF: str = '100') -> None:
        """
        :param SF: Scaling factor.
        """
        super().__init__(name='tpch', SF=SF)

    def configure_workload(self, experiment, parameter: dict) -> None:
        """
        Parse CLI args and set TPC-H workload metadata on the experiment.

        :param experiment: The owning experiment object.
        :param parameter: Dict of CLI arguments as produced by argparse.
        """
        args = SimpleNamespace(**parameter)
        experiment.args = args
        experiment.args_dict = parameter
        mode = str(parameter['mode'])
        if mode == 'load' or mode == 'start':
            experiment.benchmarking_active = False
        if mode == 'start':
            experiment.loading_deactivated = True
        SF = str(self.SF)
        recreate_parameter = args.recreate_parameter
        shuffle_queries = args.shuffle_queries
        limit_import_table = args.limit_import_table
        init_indexes = args.init_indexes
        init_constraints = args.init_constraints
        init_statistics = args.init_statistics
        init_columns = args.init_columns
        datatransfer = args.datatransfer
        num_loading_split = args.num_loading_split
        num_refresh_streams = int(args.num_refresh_streams)
        num_refresh_stream_offset = int(args.num_refresh_stream_offset)
        duckdb_force_execution = args.duckdb_force_execution
        verbose_explain = args.verbose_explain
        store_explain = args.store_explain
        timeout = int(args.timeout)
        if mode == 'run':
            experiment.set_queryfile('queries-tpch.config')
            experiment.set_workload(
                name=f'TPC-H Queries SF={SF}',
                info='This experiment compares run time and resource consumption of TPC-H queries in different DBMS.',
                type='tpch',
                defaultParameters={'SF': SF},
            )
        elif mode == 'load':
            experiment.set_workload(
                name=f'TPC-H Data Loading SF={SF}',
                info='This imports TPC-H data sets.',
                type='tpch',
                defaultParameters={'SF': SF},
            )
        elif mode == 'start':
            experiment.set_workload(
                name='TPC-H Start DBMS',
                info='This just starts a SUT.',
                intro='Start DBMS and do not load data.',
                type='tpch',
                defaultParameters={'SF': SF},
            )
        elif mode == 'empty':
            experiment.set_queryfile('queries-tpch-empty.config')
            experiment.set_workload(
                name=f'TPC-H Data Dummy SF={SF}',
                info='This experiment is for testing loading. It just runs a SELECT 1 query.',
                type='tpch',
                defaultParameters={'SF': SF},
            )
        else:
            experiment.set_queryfile('queries-tpch-profiling.config')
            experiment.set_workload(
                name=f'TPC-H Data Profiling SF={SF}',
                info='This experiment compares imported TPC-H data sets in different DBMS.',
                type='tpch',
                defaultParameters={'SF': SF},
            )
        experiment.loading_active = True
        experiment.use_distributed_datasource = True
        if experiment.loading_is_active():
            experiment.workload['info'] += f"\nTPC-H (SF={SF}) data is loaded and benchmark is executed."
        if experiment.benchmarking_is_active():
            if shuffle_queries:
                experiment.workload['info'] += "\nQuery ordering is as required by the TPC."
            else:
                experiment.workload['info'] += "\nQuery ordering is Q1 - Q22."
            if experiment.active_queries is not None:
                query_list = ", ".join(f"Q{n}" for n in sorted(experiment.active_queries))
                experiment.workload['info'] += f"\nQuery selection is limited to {query_list}."
            if recreate_parameter:
                experiment.workload['info'] += "\nAll instances use different query parameters."
            else:
                experiment.workload['info'] += "\nAll instances use the same query parameters."
            if init_columns:
                experiment.workload['info'] += "\nStorage is set to columnar."
            experiment.workload['info'] += f"\nTimeout per query is {timeout}."
            if datatransfer:
                experiment.workload['info'] += "\nData transfer volume per query is also measured."
            if num_refresh_streams > 0:
                experiment.workload['info'] += f"\nA TPC-H refresh stream (RF1+RF2) runs in parallel, with {num_refresh_streams} pair(s) applied per round."
                if num_refresh_stream_offset > 0:
                    experiment.workload['info'] += f" Refresh sets up to {num_refresh_stream_offset} are skipped."
            if duckdb_force_execution:
                experiment.workload['info'] += "\nPgDuckDB queries are forced through the DuckDB execution engine."
            if verbose_explain:
                experiment.workload['info'] += "\nEXPLAIN statements are run and printed after each query."
            if store_explain:
                experiment.workload['info'] += "\nEXPLAIN statements are run and stored in the protocol after the first run of each query."
        experiment.set_experiment(script='Schema')
        if experiment.loading_is_active():
            if init_indexes or init_constraints or init_statistics:
                experiment.set_experiment(indexing=resolve_indexing_key(init_indexes, init_constraints, init_statistics))
                requested_steps = [name for flag, name in (
                    (init_indexes, "indexes"),
                    (init_constraints, "constraints"),
                    (init_statistics, "statistics recomputation"),
                ) if flag]
                experiment.workload['info'] += "\nImport sets " + ", ".join(requested_steps) + " after loading."
            if len(limit_import_table):
                experiment.workload['info'] += f"\nImport is limited to table {limit_import_table}."
            if str(num_loading_split) != "1":
                experiment.workload['info'] += f"\nLoader data is split into {num_loading_split} parallel batches per pod."
