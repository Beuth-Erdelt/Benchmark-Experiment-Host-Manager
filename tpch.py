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
from bexhoma.cli_args import make_base_parser, resolve_scaling_factor
from bexhoma.benchmarks.base import DIMENSION_VARIANTS, dimension_folder
from bexhoma.system_descriptors import (dbms_choices, default_dockers, dimension_dockers, load_dockers,
                                        refresh_template, storage_prefix, unsupported_dimension)
from bexhoma.experiments.system_builder import (build_configuration, entry_parameters, loading_layouts,
                                                tenancy_error, tenant_ids)
from bexhoma.cli_args import storage_suffix as _storage_suffix, set_cell_storage as _set_cell_storage
# resource sweeps (-rc/-lc/-rr/-lr/-rst lists) are expanded for every DBMS by
# ExperimentBase.expand_resource_cells(); kept here under its old name
from bexhoma.cli_args import resource_cells as _resource_cells
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
import re


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)


def build_parser() -> argparse.ArgumentParser:
    """
    Build the argument parser for the TPC-H entry script.

    Extracted from ``if __name__ == '__main__':`` so it can be imported and
    fed a synthetic argv (e.g. ``build_parser().parse_args([mode])``) by
    :mod:`bexhoma.experiments.tpch_builder`, instead of re-declaring these flags by hand.

    :return: Configured argument parser.
    :rtype: argparse.ArgumentParser
    """
    description = """Run TPC-H benchmark queries against a DBMS in Kubernetes.
    Data is generated on a shared distributed filesystem and loaded in parallel.
    Supports optional index, constraint, and statistics creation; multi-stream query ordering.
    """
    parser = argparse.ArgumentParser(description=description, parents=[make_base_parser()])
    parser.add_argument('mode', help='experiment phase: profile import, run queries, start SUT only, load data, empty tables, or summarize results', choices=['profiling', 'run', 'start', 'load', 'empty', 'summary'])
    parser.add_argument('-dbms', '--dbms', help='one or more DBMS engines to test', choices=dbms_choices('tpch'), default=[], nargs='*')
    parser.add_argument('-xlit',  '--xlimit-import-table', help='import only this table (useful for partial re-loads)', default='', dest='limit_import_table')
    parser.add_argument('-xdt',   '--xdata-transfer', help='also measure data transfer volume per query', action='store_true', default=False, dest='datatransfer')
    parser.add_argument('-xqr',   '--xnum-query-runs', help='number of times to repeat each query', default=1, dest='num_run')
    parser.add_argument('-xnls',  '--xnum-loading-split', help='number of parallel loader batches (total loaders ÷ this = batch size)', default="1", dest='num_loading_split')
    parser.add_argument('-xii',   '--xinit-indexes', help='create indexes on all tables after loading', action='store_true', default=False, dest='init_indexes')
    parser.add_argument('-xic',   '--xinit-constraints', help='add primary-key and foreign-key constraints after loading', action='store_true', default=False, dest='init_constraints')
    parser.add_argument('-xis',   '--xinit-statistics', help='run ANALYZE / UPDATE STATISTICS after loading', action='store_true', default=False, dest='init_statistics')
    parser.add_argument('-xcol',  '--xinit-columns', help='use columnar storage (Citus only)', action='store_true', default=False, dest='init_columns')
    parser.add_argument('-xdim',  '--xdimensions', help='ClickHouseCluster: replicated = a full copy of part, partsupp, supplier and customer on every node, joins with orders/lineitem run locally per shard; distributed = these four spread over the shards like orders and lineitem, joined across nodes per query; nation and region are a full copy in both. Citus always uses reference tables (distributed is refused), single-node DBMS ignore it', choices=DIMENSION_VARIANTS, default='replicated', dest='dimensions')
    parser.add_argument('-xrcp',  '--xrecreate-parameter', help='regenerate random query parameters for each stream', action='store_true', default=False, dest='recreate_parameter')
    parser.add_argument('-xshq',  '--xshuffle-queries', help='shuffle query execution order independently per stream', action='store_true', default=False, dest='shuffle_queries')
    parser.add_argument('-xrs',   '--xnum-refresh-streams', help='enable a TPC-H RF1/RF2 refresh stream running in parallel with the query streams; value is the number of RF1+RF2 pairs applied per benchmarking round (set equal to the number of parallel query streams for a spec-compliant throughput test; 0 = disabled)', default=0, type=int, dest='num_refresh_streams')
    parser.add_argument('-xrso',  '--xrefresh-stream-offset', help='start the refresh stream at set OFFSET+1, so that sets 1..OFFSET are skipped (use to continue from a previous run without re-applying already-applied sets)', default=0, type=int, dest='num_refresh_stream_offset')
    parser.add_argument('-xaq',   '--xactive-queries', help='comma-separated 1-based query numbers to run, e.g. 3,5,6,7 (all other queries are set inactive in the query config uploaded to the cluster; unset = run all queries as defined in the query config file)', default='', dest='active_queries')
    parser.add_argument('-xdfe',  '--xduckdb-force-execution', help='run queries on PostgreSQL tables in pg_duckdb\'s DuckDB engine (PgDuckDB only); off by default, so they run in PostgreSQL\'s own executor', action='store_true', default=False, dest='duckdb_force_execution')
    parser.add_argument('-xve',   '--xverbose-explain', help='run and print configured EXPLAIN statements after each benchmark query (requires an \'explain\' key in the DBMS connection\'s JDBC config)', action='store_true', default=False, dest='verbose_explain')
    parser.add_argument('-xse',   '--xstore-explain', help='run configured EXPLAIN statements after the first run of each benchmark query and store the result in the protocol (requires an \'explain\' key in the DBMS connection\'s JDBC config)', action='store_true', default=False, dest='store_explain')
    return parser


def tenant_parameters(experiment, entry: dict, tenant, storage_prefix: str) -> dict:
    """
    What the multi-tenant variants add to a DBMS's configuration.

    :param experiment: The experiment (``tenant_per``, ``num_tenants``).
    :param entry: The DBMS's entry for the benchmark.
    :param tenant: The tenant id from :func:`tenant_ids`, ``None`` without container-tenancy.
    :param storage_prefix: The ``storage_prefix`` of the DBMS.
    :return: ``storage`` (name of the storage), ``loading``, ``benchmarking`` and ``eval`` parameters and
        ``experiment`` (scripts) as far as they apply; empty for a DBMS without ``multi_tenancy``.
    :rtype: dict
    """
    if not entry.get('multi_tenancy'):
        return {}
    by, number = experiment.tenant_per, experiment.num_tenants
    tenant_id = 0 if tenant is None else tenant
    result = {
        'loading': {'BEXHOMA_TENANT_BY': by, 'BEXHOMA_TENANT_NUM': number, 'BEXHOMA_TENANT_ID': tenant_id},
        'benchmarking': {'TENANT_BY': by, 'TENANT_NUM': number, 'BEXHOMA_TENANT_BY': by,
                         'BEXHOMA_TENANT_NUM': number, 'BEXHOMA_TENANT_ID': tenant_id},
        'eval': {'TENANT_BY': by, 'TENANT_NUM': number},
    }
    if tenant is not None:
        result['storage'] = f'{storage_prefix}-{tenant}-{number}'
        result['eval']['TENANT'] = tenant
    elif by:
        result['storage'] = f'{storage_prefix}-{by}-{number}'
        if by == 'schema':
            result['experiment'] = {'script': 'Schema_tenant', 'indexing': 'Index_and_Constraints_and_Statistics_tenant'}
    return result


def run(args: argparse.Namespace, on_experiment_built=None) -> None:
    """
    Build and run a TPC-H experiment from an already-parsed argparse Namespace.

    Pure extraction of ``tpch.py``'s own dispatch/build logic (everything that
    used to live directly under ``if __name__ == '__main__':``), so it can be
    invoked in-process — e.g. by ``experiment.py`` for a catalog-driven
    ``experiment.yml`` whose argv is generated by
    :func:`bexhoma.spec.build_argv` — without spawning a subprocess or
    re-parsing anything through this module's own CLI a second time.

    :param args: Parsed CLI arguments, as returned by ``build_parser().parse_args(...)``.
    :param on_experiment_built: Optional callback, invoked with the built
        experiment right after its result folder is created (``experiment.path``
        already exists on disk) but before ``prepare_testbed()``/``process()``
        run. Lets a caller drop provenance files (the ``experiment.yml`` that
        was run, the contracts that governed it) into the result folder even
        if the run itself later fails. Never called for a plain
        ``python tpch.py ...`` invocation.
    """
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
    # placement of the dimensions on multi-node DBMS
    dimensions = args.dimensions
    #multi_tenant_num = int(args.multi_tenant_num)
    #multi_tenant_by = args.multi_tenant_by
    ##############
    ### specific to: dbmsbenchmarker TPC-H
    ##############
    # shuffle ordering and random parameters
    recreate_parameter = args.recreate_parameter
    shuffle_queries = args.shuffle_queries
    # run and print configured EXPLAIN statements after each query
    verbose_explain = args.verbose_explain
    # run and store configured EXPLAIN statements in the protocol
    store_explain = args.store_explain
    # limit to one table
    limit_import_table = args.limit_import_table
    # refresh stream
    num_refresh_streams = args.num_refresh_streams
    num_refresh_stream_offset = args.num_refresh_stream_offset
    # restrict to a subset of queries by 1-based query number
    active_queries = [int(x) for x in args.active_queries.split(",") if len(x) > 0] or None
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
    # the DBMS -xdim applies to
    dimension_dbms = dimension_dockers(cluster.dockers, 'tpch')
    # limit number of sut
    if args.max_sut is not None:
        cluster.max_sut = int(args.max_sut)
    # set experiment
    if code is None:
        code = cluster.code
    # summary mode resumes an existing experiment: use its own persisted SF
    # instead of the -sf CLI default (see resolve_scaling_factor docstring)
    SF = resolve_scaling_factor(cluster, code, mode, args.scaling_factor)
    ##############
    ### prepare and configure experiment
    ##############
    experiment = experiments.TpchExperiment(cluster=cluster, SF=SF, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply)
    if on_experiment_built is not None:
        on_experiment_built(experiment)
    if args.max_sut_experiment is not None:
        experiment.max_sut = int(args.max_sut_experiment)
    experiment.prometheus_interval = "30s"
    experiment.prometheus_timeout = "30s"
    experiment.set_active_queries(active_queries)
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
    # resource sweep: -rc/-lc/-rr/-lr/-rst may each carry a comma-separated
    # list; experiment.process() then clones every configuration built below
    # once per cell, e.g. -rr 32Gi,64Gi -lr 32Gi,64Gi gives PostgreSQL-1 and
    # PostgreSQL-2 (see ExperimentBase.expand_resource_cells)
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
        DBMSBENCHMARKER_VERBOSE_EXPLAIN = verbose_explain,
        DBMSBENCHMARKER_STORE_EXPLAIN = store_explain,
    )
    if num_refresh_streams > 0:
        experiment.set_default_benchmarking_parameters(
            TPCH_REFRESH_STREAMS = num_refresh_streams,
            TPCH_REFRESH_STREAM_OFFSET = num_refresh_stream_offset,
            TRANSFORM_RAW_DATA = 1,
            STORE_RAW_DATA = 1,
        )
        # one refresh job for all DBMS of the run (the default set without -dbms)
        dbms_list = args.dbms if args.dbms else default_dockers(cluster.dockers, 'tpch')
        experiment.enable_refresh_stream(template=refresh_template(cluster.dockers, dbms_list, 'tpch'))
    ##############
    ### add configs of dbms to be tested
    ##############
    # every DBMS that can run TPC-H (or the ones named by -dbms), as declared in cluster.config,
    # once per way to load it (-nls, -nlp, -nlt)
    for docker, entry, pods_total, pods_parallel, loading_parameters in loading_layouts(
            cluster.dockers, 'tpch', args, num_loading_split, num_loading_pods, num_loading_threads):
        # a DBMS in the multi-tenant variants gets one configuration per tenant (container-tenancy)
        for tenant in tenant_ids(experiment, entry):
            tenants = tenant_parameters(experiment, entry, tenant, storage_prefix(cluster.dockers, docker))
            config = build_configuration(
                experiment, docker, 'tpch', args, reset_name='tpch',
                loading_parameters={**loading_parameters, **tenants.get('loading', {})},
                storage_configuration=tenants.get('storage'))
            config.set_benchmarking_parameters(
                **entry_parameters(cluster.dockers, docker, 'tpch', 'benchmarking_parameters', args),
                **tenants.get('benchmarking', {}))
            config.set_loading(parallel=pods_parallel, num_pods=pods_total)
            if tenants.get('eval'):
                config.set_eval_parameters(**tenants['eval'])
            if tenants.get('experiment'):
                config.set_experiment(**tenants['experiment'])
            # -xdim distributed: scripts in <DBMS>/distributed, and a volume of its own
            if docker in dimension_dbms:
                config.path_experiment_docker = dimension_folder(docker, dimensions, dimension_dbms)
                if config.path_experiment_docker != docker:
                    config.storage_label = f'tpch-distributed-{SF}'

    ##############
    ### per-system physical-design overrides (yaml-governed runs only; see
    ### bexhoma.spec.resolve_physical_design_overrides -- never set by tpch.py's
    ### own CLI, so hand-typed invocations are unaffected)
    ##############
    physical_design_overrides = getattr(args, 'physical_design_overrides', {})
    for config in experiment.configurations:
        indexing_key = physical_design_overrides.get(config.docker)
        if indexing_key:
            config.set_experiment(indexing=indexing_key)
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


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    reason = tenancy_error('tpch', args)
    if reason:
        parser.error(reason)
    dockers = load_dockers()
    for docker in args.dbms:
        reason = unsupported_dimension(dockers, docker, 'tpch', args.dimensions)
        if reason:
            parser.error(f'-xdim {args.dimensions} is not supported for {docker} in TPC-H: {reason}')
    run(args)
    exit()
