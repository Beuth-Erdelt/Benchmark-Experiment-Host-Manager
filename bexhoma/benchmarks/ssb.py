"""
Benchmark class for Star Schema Benchmark (SSB) experiments.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from types import SimpleNamespace

from .base import DBMSBenchmarkerBenchmark

__all__ = ["SSB", "SCHEMA_VARIANTS", "QUERY_VARIANTS", "resolve_indexing_key", "resolve_queryfile"]

#: ``-xsv``: star schema (4 dimensions + lineorder) or the denormalized lineorder_flat.
SCHEMA_VARIANTS = ('normal', 'flat')

#: ``-xqv``: constants of the SSB specification or random parameters (Rabl et al., ICPE 2013).
QUERY_VARIANTS = ('spec', 'random')

#: Maps every (indexes, constraints, statistics) combination to the ssb volume's
#: ``initscripts`` key in the cluster config (``volumes.ssb.initscripts``). Every
#: list ends with ``checkschema-ssb.sql``; without any step the list is ``Checks``.
_INDEXING_KEYS: dict[tuple[bool, bool, bool], str] = {
    (False, False, False): "Checks",
    (True, False, False): "Index",
    (False, True, False): "Constraints",
    (False, False, True): "Statistics",
    (True, True, False): "Index_and_Constraints",
    (True, False, True): "Index_and_Statistics",
    (False, True, True): "Constraints_and_Statistics",
    (True, True, True): "Index_and_Constraints_and_Statistics",
}

#: lineorder_flat has no keys to constrain, so the flat lists only cover indexes and statistics.
_INDEXING_KEYS_FLAT: dict[tuple[bool, bool], str] = {
    (False, False): "Checks_flat",
    (True, False): "Index_flat",
    (False, True): "Statistics_flat",
    (True, True): "Index_and_Statistics_flat",
}


def resolve_indexing_key(indexes: bool, constraints: bool, statistics: bool, schema_variant: str = 'normal') -> str:
    """Map a post-load selection to its ``initscripts`` key.

    :param indexes: Create indexes after loading.
    :param constraints: Add primary-key/foreign-key constraints after loading (normal schema only).
    :param statistics: Collect statistics after loading.
    :param schema_variant: One of :data:`SCHEMA_VARIANTS`.
    :return: The matching ``initscripts`` key.
    :rtype: str
    """
    if schema_variant == 'flat':
        return _INDEXING_KEYS_FLAT[(bool(indexes), bool(statistics))]
    return _INDEXING_KEYS[(bool(indexes), bool(constraints), bool(statistics))]


def resolve_queryfile(schema_variant: str, query_variant: str) -> str:
    """Query file of a schema and query variant.

    :param schema_variant: One of :data:`SCHEMA_VARIANTS`.
    :param query_variant: One of :data:`QUERY_VARIANTS`.
    :return: File name in ``experiments/ssb``, e.g. ``queries-ssb-flat-random.config``.
    :rtype: str
    """
    name = 'queries-ssb'
    if schema_variant == 'flat':
        name += '-flat'
    if query_variant == 'random':
        name += '-random'
    return name + '.config'


class SSB(DBMSBenchmarkerBenchmark):
    """
    Benchmark class for SSB experiments using the DBMSBenchmarker tool.

    :param SF: Scaling factor — data size in GB (lineorder has about 6,000,000 x SF rows).
    """

    def __init__(self, SF: str = '1') -> None:
        """
        :param SF: Scaling factor.
        """
        super().__init__(name='ssb', SF=SF)

    def configure_workload(self, experiment, parameter: dict) -> None:
        """
        Parse CLI args and set SSB workload metadata on the experiment.

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
        schema_variant = args.schema_variant
        query_variant = args.query_variant
        recreate_parameter = args.recreate_parameter
        shuffle_queries = args.shuffle_queries
        limit_import_table = args.limit_import_table
        init_indexes = args.init_indexes
        init_constraints = args.init_constraints
        init_statistics = args.init_statistics
        datatransfer = args.datatransfer
        verbose_explain = args.verbose_explain
        store_explain = args.store_explain
        timeout = int(args.timeout)
        schema_name = 'star schema' if schema_variant == 'normal' else 'flat table lineorder_flat'
        # a volume loaded with one schema variant must not be reused by the other
        experiment.storage_label = f'ssb-{SF}' if schema_variant == 'normal' else f'ssb-flat-{SF}'
        if mode == 'run':
            experiment.set_queryfile(resolve_queryfile(schema_variant, query_variant))
            experiment.set_workload(
                name=f'SSB Queries SF={SF}',
                info='This experiment compares run time and resource consumption of SSB queries in different DBMS.',
                type='ssb',
                defaultParameters={'SF': SF},
            )
        elif mode == 'load':
            experiment.set_workload(
                name=f'SSB Data Loading SF={SF}',
                info='This imports SSB data sets.',
                intro='Load data and do not run a benchmark.',
                type='ssb',
                defaultParameters={'SF': SF},
            )
        elif mode == 'start':
            experiment.set_workload(
                name='SSB Start DBMS',
                info='This just starts a SUT.',
                intro='Start DBMS and do not load data.',
                type='ssb',
                defaultParameters={'SF': SF},
            )
        elif mode == 'empty':
            experiment.set_queryfile('queries-ssb-empty.config')
            experiment.set_workload(
                name=f'SSB Data Dummy SF={SF}',
                info='This experiment is for testing loading. It just runs a SELECT 1 query.',
                type='ssb',
                defaultParameters={'SF': SF},
            )
        else:
            experiment.set_queryfile('queries-ssb-profiling.config')
            experiment.set_workload(
                name=f'SSB Data Profiling SF={SF}',
                info='This experiment compares imported SSB data sets in different DBMS.',
                type='ssb',
                defaultParameters={'SF': SF},
            )
        experiment.loading_active = True
        experiment.use_distributed_datasource = True
        experiment.workload['info'] += f"\nSchema is the {schema_name} (-xsv {schema_variant})."
        if experiment.loading_is_active():
            if experiment.benchmarking_is_active():
                experiment.workload['info'] += f"\nSSB (SF={SF}) data is loaded and benchmark is executed."
            else:
                experiment.workload['info'] += f"\nSSB (SF={SF}) data is loaded."
        if experiment.benchmarking_is_active():
            if mode == 'run':
                if query_variant == 'random':
                    experiment.workload['info'] += "\nQueries use random parameters that keep the filter factor of the specification (-xqv random)."
                else:
                    experiment.workload['info'] += "\nQueries use the constants of the specification (-xqv spec)."
            if shuffle_queries:
                experiment.workload['info'] += "\nQuery ordering is shuffled per stream."
            else:
                experiment.workload['info'] += "\nQuery ordering is Q1.1 - Q4.3."
            if experiment.active_queries is not None:
                query_list = ", ".join(f"Q{n}" for n in sorted(experiment.active_queries))
                experiment.workload['info'] += f"\nQuery selection is limited to {query_list}."
            if query_variant == 'random':
                if recreate_parameter:
                    experiment.workload['info'] += "\nAll instances use different query parameters."
                else:
                    experiment.workload['info'] += "\nAll instances use the same query parameters."
            experiment.workload['info'] += f"\nTimeout per query is {timeout}."
            if getattr(args, 'activate_reset', False):
                experiment.workload['info'] += " A reset script (e.g. CHECKPOINT/VACUUM) runs before each benchmarking round."
            if datatransfer:
                experiment.workload['info'] += "\nData transfer volume per query is also measured."
            if verbose_explain:
                experiment.workload['info'] += "\nEXPLAIN statements are run and printed after each query."
            if store_explain:
                experiment.workload['info'] += "\nEXPLAIN statements are run and stored in the protocol after the first run of each query."
        experiment.set_experiment(script='Schema' if schema_variant == 'normal' else 'Schema_flat')
        if experiment.loading_is_active():
            # always a post-load list: its last script reports row counts and sizes
            experiment.set_experiment(indexing=resolve_indexing_key(
                init_indexes, init_constraints, init_statistics, schema_variant))
            requested_steps = [name for flag, name in (
                (init_indexes, "indexes"),
                (init_constraints and schema_variant == 'normal', "constraints"),
                (init_statistics, "statistics recomputation"),
            ) if flag]
            if requested_steps:
                experiment.workload['info'] += "\nImport sets " + ", ".join(requested_steps) + " after loading."
            if init_constraints and schema_variant == 'flat':
                experiment.workload['info'] += "\nConstraints (-xic) are ignored: lineorder_flat has no keys to constrain."
            if len(limit_import_table):
                experiment.workload['info'] += f"\nImport is limited to table {limit_import_table}."
