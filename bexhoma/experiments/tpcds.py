"""
Experiment class for TPC-DS benchmarks.

Provides :class:`tpcds`, which extends :class:`dbmsbenchmarker` to orchestrate
TPC-DS data generation, loading, and query execution via the DBMSBenchmarker
tool inside a Kubernetes cluster.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from dbmsbenchmarker import parameter
import logging
import urllib3
from types import SimpleNamespace

from .dbmsbenchmarker import dbmsbenchmarker

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

__all__ = ["tpcds"]

# TPC-DS experiment class


class tpcds(dbmsbenchmarker):
    """
    Class for defining an TPC-DS experiment.
    This sets
    
    * the folder to the experiment - including query file and schema informations per dbms
    * name and information about the experiment
    * additional parameters - here SF (the scaling factor)
    """
    def __init__(self,
            cluster,
            code=None,
            queryfile = 'queries-tpcds.config',
            SF = '100',
            num_experiment_to_apply = 1,
            timeout = 7200,
            script=None,
            ):
        dbmsbenchmarker.__init__(self, cluster=cluster, code=code, num_experiment_to_apply=num_experiment_to_apply, timeout=timeout)
        self.SF = SF                                                    # TPC-DS scaling factor (data size in GB)
        self.use_distributed_datasource = False                         # True when loading uses a distributed in-cluster data source
        if script is None:
            script = 'SF'+str(SF)+'-index'
        self.set_experiment(volume='tpcds')
        self.cluster.set_experiments_configfolder('experiments/tpcds')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_queryfile(queryfile)
        self.set_additional_labels(SF=SF)
        self.set_workload(
            name = 'TPC-DS Queries SF='+str(SF),
            info = 'This experiment performs some TPC-DS inspired queries.',
            type = 'tpcds',
            )
        self.storage_label = 'tpcds-'+str(SF)                          # label used to match persistent storage to this experiment
    def set_queries_full(self) -> None:
        """Switch to the full TPC-DS query file covering all 99 queries."""
        self.set_queryfile('queries-tpcds.config')

    def set_queries_profiling(self) -> None:
        """Switch to the abbreviated profiling query file for import validation."""
        self.set_queryfile('queries-tpcds-profiling.config')

    def prepare_testbed(self, parameter: dict) -> None:
        """
        Configure the TPC-DS experiment from a CLI parameter dict and delegate to dbmsbenchmarker.

        Sets workload metadata and appends info lines about SF, query ordering,
        parameterisation, indexing strategy, and optional table-level import limits.

        :param parameter: Dict of CLI arguments as produced by argparse.
        """
        args = SimpleNamespace(**parameter)
        self.args = args
        self.args_dict = parameter
        mode = str(parameter['mode'])
        if mode=='load' or mode=='start':
            self.benchmarking_active = False
        if mode=='start':
            self.loading_deactivated = True
        SF = str(self.SF)
        # shuffle ordering and random parameters
        recreate_parameter = args.recreate_parameter
        shuffle_queries = args.shuffle_queries
        # limit to one table
        limit_import_table = args.limit_import_table
        # indexes
        init_indexes = args.init_indexes
        init_constraints = args.init_constraints
        init_statistics = args.init_statistics
        # columnar storage
        init_columns = args.init_columns
        # timeout of a benchmark
        timeout = int(args.timeout)
        if mode == 'run':
            # we want all TPC-H queries
            self.set_queries_full()
            self.set_workload(
                name = 'TPC-DS Queries SF='+str(SF),
                info = 'This experiment compares run time and resource consumption of TPC-DS queries in different DBMS.',
                type = 'tpcds',
                defaultParameters = {'SF': SF}
            )
        elif mode == 'load':
            self.set_workload(
                name = 'TPC-DS Data Loading SF='+str(SF),
                info = 'This imports TPC-DS data sets.',
                type = 'tpcds',
                defaultParameters = {'SF': SF}
            )
        elif mode == 'start':
            self.set_workload(
                name = 'TPC-DS Start DBMS',
                info = 'This just starts a SUT.',
                intro = 'Start DBMS and do not load data.',
                type = 'tpcds',
                defaultParameters = {'SF': SF}
            )
        elif mode == 'empty':
            # set benchmarking queries to dummy - SELECT 1
            self.set_queryfile('queries-tpcds-empty.config')
            self.set_workload(
                name = 'TPC-DS Data Dummy SF='+str(SF),
                info = 'This experiment is for testing loading. It just runs a SELECT 1 query.',
                type = 'tpcds',
                defaultParameters = {'SF': SF}
            )
        else:
            self.set_queries_profiling()
            self.set_workload(
                name = 'TPC-DS Data Profiling SF='+str(SF),
                info = 'This experiment compares imported TPC-DS data sets in different DBMS.',
                type = 'tpcds',
                defaultParameters = {'SF': SF}
            )
        # new loading in cluster
        self.loading_active = True
        self.use_distributed_datasource = True
        if self.loading_is_active():
            self.workload['info'] = self.workload['info']+"\nTPC-DS (SF={}) data is loaded and benchmark is executed.".format(SF)
        if self.benchmarking_is_active():
            if shuffle_queries:
                self.workload['info'] = self.workload['info']+"\nQuery ordering is as required by the TPC."
            else:
                self.workload['info'] = self.workload['info']+"\nQuery ordering is Q1 - Q99."
            if recreate_parameter:
                self.workload['info'] = self.workload['info']+"\nAll instances use different query parameters."
            else:
                self.workload['info'] = self.workload['info']+"\nAll instances use the same query parameters."
            if init_columns:
                self.workload['info'] = self.workload['info']+"\nStorage is set to columnar."
            self.workload['info'] = self.workload['info']+"\nTimeout per query is {}.".format(timeout)
        # optionally set some indexes and constraints after import
        self.set_experiment(script='Schema')
        if self.loading_is_active():
            if init_indexes or init_constraints or init_statistics:
                self.set_experiment(indexing='Index')
                init_scripts = " Import sets indexes after loading."
                if init_constraints:
                    self.set_experiment(indexing='Index_and_Constraints')
                    init_scripts = "\nImport sets indexes and constraints after loading."
                if init_statistics:
                    self.set_experiment(indexing='Index_and_Constraints_and_Statistics')
                    init_scripts = "\nImport sets indexes and constraints after loading and recomputes statistics."
                self.workload['info'] = self.workload['info']+init_scripts
            if len(limit_import_table):
                # import is limited to single table
                self.workload['info'] = self.workload['info']+"\nImport is limited to table {}.".format(limit_import_table)
        dbmsbenchmarker.prepare_testbed(self, parameter)

