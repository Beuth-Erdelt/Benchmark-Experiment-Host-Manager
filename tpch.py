"""
CLI entry point for TPC-H benchmarks in a Kubernetes cluster.

Generates TPC-H data on a distributed filesystem (Ceph), loads it into
one or more DBMS with parallel, synchronised loaders, and runs queries.
Supports monitoring, data verification, optional index and constraint
creation, and fixed node assignment.

Authors: Patrick K. Erdelt
Copyright (C) 2023 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma import *
from bexhoma.cli_args import make_base_parser
from dbmsbenchmarker import *
import logging
import urllib3
import argparse
import time
from timeit import default_timer
import datetime
import subprocess
import psutil
import math


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    description = """Performs a TPC-H experiment. Data is generated and imported into a DBMS from a distributed filesystem (shared disk)."""
    # argparse
    parser = argparse.ArgumentParser(description=description, parents=[make_base_parser()])
    parser.add_argument('mode', help='profile the import or run the TPC-H queries', choices=['profiling', 'run', 'start', 'load', 'empty', 'summary'])
    parser.add_argument('-dbms', '--dbms', help='DBMS', choices=['PostgreSQL', 'MonetDB', 'MySQL', 'MariaDB', 'DatabaseService', 'Citus', 'CedarDB'], default=[], nargs='*')
    parser.add_argument('-lit',  '--limit-import-table', help='limit import to one table, name of this table', default='')
    parser.add_argument('-dt',   '--datatransfer', help='activates transfer of data per query (not only execution)', action='store_true', default=False)
    parser.add_argument('-nr',   '--num-run', help='number of runs per query', default=1)
    parser.add_argument('-nls',  '--num-loading-split', help='portion of loaders that should run in parallel', default="1")
    parser.add_argument('-ii',   '--init-indexes', help='adds indexes to tables after ingestion', action='store_true', default=False)
    parser.add_argument('-ic',   '--init-constraints', help='adds constraints to tables after ingestion', action='store_true', default=False)
    parser.add_argument('-is',   '--init-statistics', help='recomputes statistics of tables after ingestion', action='store_true', default=False)
    parser.add_argument('-icol', '--init-columns', help='uses columnar storage (for Citus)', action='store_true', default=False)
    parser.add_argument('-rcp',  '--recreate-parameter', help='recreate parameter for randomized queries', action='store_true', default=False)
    parser.add_argument('-shq',  '--shuffle-queries', help='have different orderings per stream', action='store_true', default=False)
    # evaluate args
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    debugging = int(args.debug)
    if args.debug:
        logger_bexhoma = logging.getLogger('bexhoma')
        logger_bexhoma.setLevel(logging.DEBUG)
        logger_loader = logging.getLogger('load_data_asynch')
        logger_loader.setLevel(logging.DEBUG)
    ##############
    ### set parameters
    ##############
    command_args = vars(args)
    ##############
    ### workflow parameters
    ##############
    # start with old experiment?
    code = args.experiment
    # only create testbed or also run a benchmark?
    mode = str(args.mode)
    # scaling of data
    SF = str(args.scaling_factor)
    # timeout of a benchmark
    timeout = int(args.timeout)
    # how often to repeat experiment?
    num_experiment_to_apply = int(args.num_config)
    # should results be tested for validity?
    test_result = args.test_result
    # configure number of clients per config
    list_clients = args.num_query_executors.split(",")
    if len(list_clients) > 0:
        list_clients = [int(x) for x in list_clients if len(x) > 0]
    else:
        list_clients = []
    # do not ingest, start benchmarking immediately
    skip_loading = args.skip_loading
    # how many workers (for distributed dbms)
    num_worker = int(args.num_worker)
    num_worker_replicas = int(args.num_worker_replicas)
    num_worker_shards = int(args.num_worker_shards)
    #multi_tenant_num = int(args.multi_tenant_num)
    #multi_tenant_by = args.multi_tenant_by
    ##############
    ### specific to: dbmsbenchmarker TPC-H
    ##############
    # shuffle ordering and random parameters
    recreate_parameter = args.recreate_parameter
    shuffle_queries = args.shuffle_queries
    # limit to one table
    limit_import_table = args.limit_import_table
    # columnar storage
    init_columns = args.init_columns
    ##############
    ### set cluster
    ##############
    aws = args.aws
    if aws:
        cluster = clusters.AWS(context=args.context)
        # scale up
        node_sizes = {
            'auxiliary': 1,
            'sut-mid': 1,
            'benchmarker': 1
        }
        #cluster.scale_nodegroups(node_sizes)
    else:
        cluster = clusters.Kubernetes(context=args.context)
    cluster_name = cluster.contextdata['clustername']
    # limit number of sut
    if args.max_sut is not None:
        cluster.max_sut = int(args.max_sut)
    # set experiment
    if code is None:
        code = cluster.code
    ##############
    ### prepare and configure experiment
    ##############
    experiment = experiments.tpch(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
    experiment.prometheus_interval = "30s"
    experiment.prometheus_timeout = "30s"
    #experiment.num_tenants = multi_tenant_num
    #experiment.tenant_per = multi_tenant_by
    # remove running dbms
    #experiment.clean()
    experiment.prepare_testbed(command_args)
    num_loading_pods = experiment.get_parameter_as_list('num_loading_pods')
    num_loading_threads = experiment.get_parameter_as_list('num_loading_threads')
    num_loading_split = experiment.get_parameter_as_list('num_loading_split')
    num_benchmarking_pods = experiment.get_parameter_as_list('num_benchmarking_pods')
    num_benchmarking_threads = experiment.get_parameter_as_list('num_benchmarking_threads')
    # set node groups for components
    if aws:
        # set node labes for components
        experiment.set_nodes(
            sut = 'sut',
            loading = 'auxiliary',
            monitoring = 'auxiliary',
            benchmarking = 'auxiliary',
            )
    # add labels about the use case
    experiment.set_additional_labels(
        usecase="tpc-h",
        experiment_design="parallel-loading"
    )
    experiment.set_default_loading_parameters(
        SF = SF,
        STORE_RAW_DATA = 1,
        STORE_RAW_DATA_RECREATE = 0,
        BEXHOMA_SYNCH_LOAD = 1,
        BEXHOMA_SYNCH_GENERATE = 1,
        TRANSFORM_RAW_DATA = 1,
        TPCH_TABLE = limit_import_table,
    )
    experiment.set_default_benchmarking_parameters(
        SF = SF,
        DBMSBENCHMARKER_RECREATE_PARAMETER = recreate_parameter,
        DBMSBENCHMARKER_SHUFFLE_QUERIES = shuffle_queries,
        DBMSBENCHMARKER_DEV = debugging,
    )
    ##############
    ### add configs of dbms to be tested
    ##############
    for loading_pods_split in num_loading_split: # should be a number of splits, e.g. 4 for 1/4th of all pods
        for loading_pods_total in num_loading_pods: # number of loading pods in total
            # split number of loading pods into parallel potions
            if loading_pods_total < loading_pods_split:
                # thats not possible
                continue
            # how many in parallel?
            split_portion = int(loading_pods_total/loading_pods_split)
            if ("PostgreSQL" in args.dbms or len(args.dbms) == 0):
                # PostgreSQL
                if experiment.tenant_per == 'container':
                    for tenant in range(experiment.num_tenants):
                        name_format = 'PostgreSQL-{cluster}-{pods}-{tenant}'
                        #, configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion, tenant=tenant)
                        config = configurations.default(experiment=experiment, docker='PostgreSQL', dialect='PostgreSQL', alias='DBMS A2')
                        #config.num_tenants = multi_tenant_num
                        #config.tenant_per = multi_tenant_by
                        config.set_storage(
                            storageConfiguration = f'postgresql-{tenant}'+"-"+str(config.num_tenants)
                            )
                        if skip_loading:
                            config.loading_deactivated = True
                        config.jobtemplate_loading = "jobtemplate-loading-tpch-PostgreSQL.yml"
                        config.set_loading_parameters(
                            PODS_TOTAL = str(loading_pods_total),
                            PODS_PARALLEL = str(split_portion),
                            BEXHOMA_TENANT_BY = config.tenant_per,
                            BEXHOMA_TENANT_NUM = config.num_tenants,
                            BEXHOMA_TENANT_ID = tenant,
                            )
                        config.set_benchmarking_parameters(
                            TENANT_BY = config.tenant_per,
                            TENANT_NUM = config.num_tenants,
                            BEXHOMA_TENANT_BY = config.tenant_per,
                            BEXHOMA_TENANT_NUM = config.num_tenants,
                            BEXHOMA_TENANT_ID = tenant,
                            )
                        config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
                        config.set_eval_parameters(
                            TENANT_BY = config.tenant_per,
                            TENANT_NUM = config.num_tenants,
                            TENANT = tenant,
                            )
                else:
                    name_format = 'PostgreSQL-{cluster}-{pods}'
                    #, configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion)
                    config = configurations.default(experiment=experiment, docker='PostgreSQL', dialect='PostgreSQL', alias='DBMS A2')
                    #config.num_tenants = multi_tenant_num
                    #config.tenant_per = multi_tenant_by
                    if config.tenant_per:
                        config.set_storage(
                            storageConfiguration = 'postgresql-'+config.tenant_per+"-"+str(config.num_tenants)
                            )
                    else:
                        config.set_storage(
                            storageConfiguration = 'postgresql'
                            )
                    if skip_loading:
                        config.loading_deactivated = True
                    config.jobtemplate_loading = "jobtemplate-loading-tpch-PostgreSQL.yml"
                    config.set_loading_parameters(
                        PODS_TOTAL = str(loading_pods_total),
                        PODS_PARALLEL = str(split_portion),
                        BEXHOMA_TENANT_BY = config.tenant_per,
                        BEXHOMA_TENANT_NUM = config.num_tenants,
                        BEXHOMA_TENANT_ID = 0,
                        )
                    config.set_benchmarking_parameters(
                        TENANT_BY = config.tenant_per,
                        TENANT_NUM = config.num_tenants,
                        BEXHOMA_TENANT_BY = config.tenant_per,
                        BEXHOMA_TENANT_NUM = config.num_tenants,
                        BEXHOMA_TENANT_ID = 0,
                        )
                    config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
                    if config.tenant_per == 'schema':
                        config.set_experiment(script='Schema_tenant')
                        config.set_experiment(indexing='Index_and_Constraints_and_Statistics_tenant')
                    config.set_eval_parameters(
                        TENANT_BY = config.tenant_per,
                        TENANT_NUM = config.num_tenants,
                        )
            if ("CedarDB" in args.dbms):
                # PostgreSQL
                name_format = 'CedarDB-{cluster}-{pods}'
                #, configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion)
                config = configurations.default(experiment=experiment, docker='CedarDB', dialect='PostgreSQL', alias='DBMS A2')
                config.set_storage(
                    storageConfiguration = 'cedardb'
                    )
                if skip_loading:
                    config.loading_deactivated = True
                config.jobtemplate_loading = "jobtemplate-loading-tpch-PostgreSQL.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    )
                config.set_benchmarking_parameters()
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("MonetDB" in args.dbms or len(args.dbms) == 0):
                # MonetDB
                name_format = 'MonetDB-{cluster}-{pods}'
                #, configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion)
                config = configurations.default(experiment=experiment, docker='MonetDB', dialect='MonetDB', alias='DBMS A1')
                config.set_storage(
                    storageConfiguration = 'monetdb'
                    )
                if skip_loading:
                    config.loading_deactivated = True
                config.jobtemplate_loading = "jobtemplate-loading-tpch-MonetDB.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    )
                config.set_benchmarking_parameters()
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("MariaDB" in args.dbms or len(args.dbms) == 0):
                # MariaDB
                name_format = 'MariaDB-{cluster}-{pods}'
                #, configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion)
                config = configurations.default(experiment=experiment, docker='MariaDB', dialect='MySQL', alias='DBMS A1')
                config.set_storage(
                    storageConfiguration = 'mariadb'
                    )
                if skip_loading:
                    config.loading_deactivated = True
                config.jobtemplate_loading = "jobtemplate-loading-tpch-MariaDB.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    MYSQL_LOADING_FROM = "LOCAL",
                    )
                config.set_benchmarking_parameters()
                config.set_sut_parameters(
                    MARIADB_DATABASE = "tpch",
                    )
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("MySQL" in args.dbms or len(args.dbms) == 0):
                # MySQL
                for threads in num_loading_threads:
                    pods_times_threads=int(loading_pods_total)*int(threads)
                    name_format = 'MySQL-{cluster}-{pods_times_threads}'
                    #, configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion, threads=threads, pods_times_threads=pods_times_threads)
                    config = configurations.default(experiment=experiment, docker='MySQL', dialect='MySQL', alias='DBMS A1')
                    config.set_storage(
                        storageConfiguration = 'mysql'
                        )
                    if skip_loading:
                        config.loading_deactivated = True
                    config.jobtemplate_loading = "jobtemplate-loading-tpch-MySQL.yml"
                    config.set_loading_parameters(
                        PODS_TOTAL = str(loading_pods_total),
                        PODS_PARALLEL = str(split_portion),
                        MYSQL_LOADING_THREADS = int(threads),#int(num_loading_threads),#int(loading_pods_total),
                        MYSQL_LOADING_PARALLEL = 1, # not possible from RAM disk, only filesystem
                        )
                    config.set_benchmarking_parameters()
                    config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("DatabaseService" in args.dbms):# or len(args.dbms) == 0): # not included per default
                # DatabaseService
                name_format = 'DBS-{cluster}-{pods}'
                #, configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion)
                config = configurations.default(experiment=experiment, docker='DatabaseService', dialect='PostgreSQL', alias='DBMS A1')
                config.monitoring_sut = False # cannot be monitored since outside of K8s
                if skip_loading:
                    config.loading_deactivated = True
                config.set_storage(
                    storageConfiguration = 'dbs'
                    )
                config.jobtemplate_loading = "jobtemplate-loading-tpch-PostgreSQL.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    BEXHOMA_HOST = 'bexhoma-service',
                    )
                config.set_benchmarking_parameters()
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
            if ("Citus" in args.dbms):
                # PostgreSQL
                name_format = 'Citus-{cluster}-{pods}'
                #, configuration=name_format.format(cluster=cluster_name, pods=loading_pods_total, split=split_portion)
                config = configurations.default(experiment=experiment, docker='Citus', dialect='PostgreSQL', alias='DBMS C2', worker=num_worker)
                if skip_loading:
                    config.loading_deactivated = True
                if init_columns:
                    config.set_experiment(script='Schema-Columnar')
                    config.set_experiment(indexing='Index_and_Statistics')
                config.set_storage(
                    storageConfiguration = 'citus'
                    )
                config.set_ddl_parameters(
                    num_worker_replicas = num_worker_replicas,
                    num_worker_shards = num_worker_shards,
                    )
                config.set_sut_parameters(
                    BEXHOMA_REPLICAS = num_worker_replicas,
                    BEXHOMA_SHARDS = num_worker_shards,
                    )
                config.set_eval_parameters(
                    BEXHOMA_REPLICAS = num_worker_replicas,
                    BEXHOMA_SHARDS = num_worker_shards,
                    BEXHOMA_WORKERS = num_worker,
                    COLUMNAR = init_columns,
                    )
                config.jobtemplate_loading = "jobtemplate-loading-tpch-PostgreSQL.yml"
                config.set_loading_parameters(
                    PODS_TOTAL = str(loading_pods_total),
                    PODS_PARALLEL = str(split_portion),
                    BEXHOMA_REPLICAS = num_worker_replicas,
                    )
                config.set_benchmarking_parameters(
                    BEXHOMA_REPLICAS = num_worker_replicas,
                    )
                config.set_loading(parallel=split_portion, num_pods=loading_pods_total)
    ##############
    ### wait for necessary nodegroups to have planned size
    ##############
    if aws:
        #cluster.wait_for_nodegroups(node_sizes)
        pass
    ##############
    ### branch for workflows
    ##############
    experiment.add_benchmark_list(list_clients)
    experiment.process()
exit()
