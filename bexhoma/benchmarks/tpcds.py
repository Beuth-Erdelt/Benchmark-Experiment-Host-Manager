"""
Benchmark class for TPC-DS experiments.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from types import SimpleNamespace

from .base import DBMSBenchmarkerBenchmark

__all__ = ["TPCDS"]


class TPCDS(DBMSBenchmarkerBenchmark):
    """
    Benchmark class for TPC-DS experiments using the DBMSBenchmarker tool.

    :param SF: Scaling factor — data size in GB.
    """

    def __init__(self, SF: str = '100') -> None:
        """
        :param SF: Scaling factor.
        """
        super().__init__(name='tpcds', SF=SF)

    def configure_workload(self, experiment, parameter: dict) -> None:
        """
        Parse CLI args and set TPC-DS workload metadata on the experiment.

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
        timeout = int(args.timeout)
        if mode == 'run':
            experiment.set_queryfile('queries-tpcds.config')
            experiment.set_workload(
                name=f'TPC-DS Queries SF={SF}',
                info='This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.',
                type='tpcds',
                defaultParameters={'SF': SF},
            )
        elif mode == 'load':
            experiment.set_workload(
                name=f'TPC-DS Data Loading SF={SF}',
                info='This imports TPC-DS data sets.',
                type='tpcds',
                defaultParameters={'SF': SF},
            )
        elif mode == 'start':
            experiment.set_workload(
                name='TPC-DS Start DBMS',
                info='This just starts a SUT.',
                intro='Start DBMS and do not load data.',
                type='tpcds',
                defaultParameters={'SF': SF},
            )
        elif mode == 'empty':
            experiment.set_queryfile('queries-tpcds-empty.config')
            experiment.set_workload(
                name=f'TPC-DS Data Dummy SF={SF}',
                info='This experiment is for testing loading. It just runs a SELECT 1 query.',
                type='tpcds',
                defaultParameters={'SF': SF},
            )
        else:
            experiment.set_queryfile('queries-tpcds-profiling.config')
            experiment.set_workload(
                name=f'TPC-DS Data Profiling SF={SF}',
                info='This experiment compares imported TPC-DS data sets in different DBMS.',
                type='tpcds',
                defaultParameters={'SF': SF},
            )
        experiment.loading_active = True
        experiment.use_distributed_datasource = True
        if experiment.loading_is_active():
            experiment.workload['info'] += f"\nTPC-DS (SF={SF}) data is loaded and benchmark is executed."
        if experiment.benchmarking_is_active():
            if shuffle_queries:
                experiment.workload['info'] += "\nQuery ordering is as required by the TPC."
            else:
                experiment.workload['info'] += "\nQuery ordering is Q1 - Q99."
            if recreate_parameter:
                experiment.workload['info'] += "\nAll instances use different query parameters."
            else:
                experiment.workload['info'] += "\nAll instances use the same query parameters."
            if init_columns:
                experiment.workload['info'] += "\nStorage is set to columnar."
            experiment.workload['info'] += f"\nTimeout per query is {timeout}."
        experiment.set_experiment(script='Schema')
        if experiment.loading_is_active():
            if init_indexes or init_constraints or init_statistics:
                experiment.set_experiment(indexing='Index')
                init_scripts = " Import sets indexes after loading."
                if init_constraints:
                    experiment.set_experiment(indexing='Index_and_Constraints')
                    init_scripts = "\nImport sets indexes and constraints after loading."
                if init_statistics:
                    experiment.set_experiment(indexing='Index_and_Constraints_and_Statistics')
                    init_scripts = "\nImport sets indexes and constraints after loading and recomputes statistics."
                experiment.workload['info'] += init_scripts
            if len(limit_import_table):
                experiment.workload['info'] += f"\nImport is limited to table {limit_import_table}."
