"""
Benchmark class for TPC-H experiments.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from types import SimpleNamespace

from .base import DBMSBenchmarkerBenchmark

__all__ = ["TPCH"]


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
        timeout = int(args.timeout)
        if mode == 'run':
            experiment.set_queryfile('queries-tpch.config')
            experiment.set_workload(
                name='TPC-H Queries SF=' + str(SF),
                info='This experiment compares run time and resource consumption of TPC-H queries in different DBMS.',
                type='tpch',
                defaultParameters={'SF': SF},
            )
        elif mode == 'load':
            experiment.set_workload(
                name='TPC-H Data Loading SF=' + str(SF),
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
                name='TPC-H Data Dummy SF=' + str(SF),
                info='This experiment is for testing loading. It just runs a SELECT 1 query.',
                type='tpch',
                defaultParameters={'SF': SF},
            )
        else:
            experiment.set_queryfile('queries-tpch-profiling.config')
            experiment.set_workload(
                name='TPC-H Data Profiling SF=' + str(SF),
                info='This experiment compares imported TPC-H data sets in different DBMS.',
                type='tpch',
                defaultParameters={'SF': SF},
            )
        experiment.loading_active = True
        experiment.use_distributed_datasource = True
        if experiment.loading_is_active():
            experiment.workload['info'] += "\nTPC-H (SF={}) data is loaded and benchmark is executed.".format(SF)
        if experiment.benchmarking_is_active():
            if shuffle_queries:
                experiment.workload['info'] += "\nQuery ordering is as required by the TPC."
            else:
                experiment.workload['info'] += "\nQuery ordering is Q1 - Q22."
            if recreate_parameter:
                experiment.workload['info'] += "\nAll instances use different query parameters."
            else:
                experiment.workload['info'] += "\nAll instances use the same query parameters."
            experiment.workload['info'] += "\nTimeout per query is {}.".format(timeout)
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
                experiment.workload['info'] += "\nImport is limited to table {}.".format(limit_import_table)
