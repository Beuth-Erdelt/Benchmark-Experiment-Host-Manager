"""
Experiment class for TPC-H benchmarks.

Provides :class:`tpch`, which extends :class:`dbmsbenchmarker` to orchestrate
TPC-H data generation, loading, and query execution via the DBMSBenchmarker
tool inside a Kubernetes cluster.

Authors: Patrick K. Erdelt
Copyright (C) 2020 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from dbmsbenchmarker import parameter, inspector
import logging
import urllib3
from os import makedirs, path
import time
from timeit import default_timer
#import datetime
import os
from datetime import datetime, timedelta
import re
import pandas as pd
import json
import ast
from types import SimpleNamespace
from importlib.metadata import version
from pathlib import Path
import platform
import math
from typing import List, Tuple, Optional

from bexhoma import evaluators
from .dbmsbenchmarker import dbmsbenchmarker

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)



"""
############################################################################
TPC-H
############################################################################
"""

class tpch(dbmsbenchmarker):
    """
    Class for defining an TPC-H experiment.
    This sets

    * the folder to the experiment - including query file and schema informations per dbms
    * name and information about the experiment
    * additional parameters - here SF (the scaling factor)
    """
    def __init__(self,
            cluster,
            code=None,
            queryfile = 'queries-tpch.config',
            SF = '100',
            num_experiment_to_apply = 1,
            timeout = 7200,
            script=None
            #detached=False
            ):
        dbmsbenchmarker.__init__(self, cluster=cluster, code=code, num_experiment_to_apply=num_experiment_to_apply, timeout=timeout)#, detached)
        self.SF = SF
        if script is None:
            script = 'SF'+str(SF)+'-index'
        self.set_experiment(volume='tpch')
        #self.set_experiment(script=script)
        self.cluster.set_experiments_configfolder('experiments/tpch')
        parameter.defaultParameters = {'SF': str(SF)}
        self.set_additional_labels(SF=SF)
        self.set_queryfile(queryfile)
        self.set_workload(
            name = 'TPC-H Queries SF='+str(SF),
            info = 'This experiment performs some TPC-H inspired queries.',
            type = 'tpch',
            )
        self.storage_label = 'tpch-'+str(SF)
    def set_queries_full(self):
        self.set_queryfile('queries-tpch.config')
    def set_queries_profiling(self):
        self.set_queryfile('queries-tpch-profiling.config')
    def prepare_testbed(self, parameter):
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
        # timeout of a benchmark
        timeout = int(args.timeout)
        if mode == 'run':
            # we want all TPC-H queries
            self.set_queries_full()
            self.set_workload(
                name = 'TPC-H Queries SF='+str(SF),
                info = 'This experiment compares run time and resource consumption of TPC-H queries in different DBMS.',
                type = 'tpch',
                defaultParameters = {'SF': SF}
            )
        elif mode == 'load':
            # we want to profile the import
            #self.set_queries_profiling()
            self.set_workload(
                name = 'TPC-H Data Loading SF='+str(SF),
                info = 'This imports TPC-H data sets.',
                type = 'tpch',
                defaultParameters = {'SF': SF}
            )
        elif mode == 'start':
            # we want to profile the import
            #self.set_queries_profiling()
            self.set_workload(
                name = 'TPC-H Start DBMS',
                info = 'This just starts a SUT.',
                intro = 'Start DBMS and do not load data.',
                type = 'tpch',
                defaultParameters = {'SF': SF}
            )
        elif mode == 'empty':
            # set benchmarking queries to dummy - SELECT 1
            self.set_queryfile('queries-tpch-empty.config')
            self.set_workload(
                name = 'TPC-H Data Dummy SF='+str(SF),
                info = 'This experiment is for testing loading. It just runs a SELECT 1 query.',
                type = 'tpch',
                defaultParameters = {'SF': SF}
            )
        else:
            # we want to profile the import
            self.set_queries_profiling()
            self.set_workload(
                name = 'TPC-H Data Profiling SF='+str(SF),
                info = 'This experiment compares imported TPC-H data sets in different DBMS.',
                type = 'tpch',
                defaultParameters = {'SF': SF}
            )
            # patch: use short profiling (only keys)
            #self.set_queryfile('queries-tpch-profiling-keys.config')
        # new loading in cluster
        self.loading_active = True
        self.use_distributed_datasource = True
        if self.loading_is_active():
            self.workload['info'] = self.workload['info']+"\nTPC-H (SF={}) data is loaded and benchmark is executed.".format(SF)
        if self.benchmarking_is_active():
            if shuffle_queries:
                self.workload['info'] = self.workload['info']+"\nQuery ordering is as required by the TPC."
            else:
                self.workload['info'] = self.workload['info']+"\nQuery ordering is Q1 - Q22."
            if recreate_parameter:
                self.workload['info'] = self.workload['info']+"\nAll instances use different query parameters."
            else:
                self.workload['info'] = self.workload['info']+"\nAll instances use the same query parameters."
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
            #self.set_experiment(script='Schema', indexing='Index')
            if len(limit_import_table):
                # import is limited to single table
                self.workload['info'] = self.workload['info']+"\nImport is limited to table {}.".format(limit_import_table)
        dbmsbenchmarker.prepare_testbed(self, parameter)

