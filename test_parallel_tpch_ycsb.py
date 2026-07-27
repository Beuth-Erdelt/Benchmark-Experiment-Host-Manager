"""
TEST-ONLY entry point demonstrating multiple parallel loading jobs and
multiple parallel benchmarking jobs of DIFFERENT tools against one SUT.

Loads TPC-H and YCSB data into the SAME PostgreSQL database at the same time
(two concurrent Kubernetes loading Jobs, coordinated via the loader round
counter — see bexhoma/CLAUDE.md "Pod synchronization counters"), then runs
the TPC-H query stream and a YCSB workload at the same time (two concurrent
benchmarking Jobs in one client round, using the same mechanism that already
powers the TPC-H refresh stream).

This is a demonstration/test script, not a production experiment type: it is
not wired into bexhoma.experiments. Its combined "Show Summary" prints both
TPC-H's full result tables (as the primary benchmark) and a "### ycsb" section
with YCSB's own Per Connection / Per Phase / Reset results, via
Benchmark.show_summary_section().

Usage:
    python test_parallel_tpch_ycsb.py run -sf 1

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma import *
from bexhoma import benchmarks
from bexhoma.cli_args import make_base_parser
from bexhoma.experiments.tpch import TpchExperiment
from dbmsbenchmarker import *
import logging
import urllib3
import argparse


urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)


class TpchYcsbParallelTestExperiment(TpchExperiment):
    """
    TEST-ONLY experiment: TPC-H as the primary benchmark (benchmark_index=1,
    full DBMSBenchmarker evaluation), YCSB registered alongside it
    (benchmark_index=2) purely so its loading/benchmarking Jobs run and its
    logs get collected; see the module docstring for what is and isn't shown
    in the printed summary.

    Extends the template built by :class:`TpchExperiment` with a second
    loader entry and a second entry in benchmarker round 1, both targeting
    YCSB against the same PostgreSQL SUT.

    :param ycsb_rows: Number of YCSB rows to load (kept small; this is a demo).
    """

    def __init__(self, cluster, code=None, queryfile='queries-tpch.config',
                 SF='1', num_experiment_to_apply=1, timeout=600, script=None,
                 ycsb_rows=10000):
        TpchExperiment.__init__(
            self, cluster=cluster, code=code, queryfile=queryfile, SF=SF,
            num_experiment_to_apply=num_experiment_to_apply, timeout=timeout,
            script=script)
        self.ycsb_rows = ycsb_rows
        self.add_benchmark(benchmarks.YCSB(SF=str(ycsb_rows // 1000000 or 1)))
        # The second parallel loading job (YCSB) is added later, per-config, via
        # SutConfiguration.add_loading_parameters() in the __main__ block below —
        # NOT here. Adding it to experiment_dict_template as well would double it
        # up (add_configuration() deep-copies this template into every config's
        # own experiment_dict, so the config-level add_loading_parameters() call
        # would then append a *third* loader entry on top of these two).
        # Second parallel benchmarking job in round 1: runs the YCSB workload
        # while the "tpch" entry (already in the template) runs the query
        # stream — both start together (round counter), same as the existing
        # TPC-H refresh-stream mechanism.
        self.experiment_dict_template["benchmarker"][0].append({
            "name":              "ycsb",
            "benchmarker":       "ycsb",
            "template":          "jobtemplate-benchmarking-ycsb.yml",
            "parallelism":       1,
            "num_pods":          1,
            "fixed_parallelism": True,
            "target":            "sut",
            # Overrides the shared, config-wide SF broadcast from
            # experiment.set_default_benchmarking_parameters(), which carries
            # TPC-H's (possibly fractional, e.g. "0.1") SF. YCSB's own
            # evaluator casts SF to int, so this entry needs its own
            # integer-safe value instead of inheriting TPC-H's.
            "parameters":        {"SF": str(ycsb_rows // 1000000 or 1)},
        })


if __name__ == '__main__':
    description = """TEST ONLY: load TPC-H and YCSB into the same PostgreSQL database in
    parallel, then run the TPC-H query stream and a YCSB workload in parallel.
    Demonstrates the parallel-loading-jobs mechanism; not a production experiment type.
    """
    parser = argparse.ArgumentParser(description=description, parents=[make_base_parser()])
    parser.add_argument('mode', help='experiment phase', choices=['run', 'start', 'load', 'summary'], default='run')
    parser.add_argument('-dbms', '--dbms', help='fixed to PostgreSQL for this demo; present only because ExperimentBase.prepare_testbed() reads args.dbms', default=[], nargs='*')
    parser.add_argument('-yr', '--ycsb-rows', help='number of YCSB rows/operations to load and run (kept small; this is a demo)', default=10000, type=int, dest='ycsb_rows')
    # TPC-H-specific args read by benchmarks.TPCH.configure_workload()
    parser.add_argument('-xlit', '--xlimit-import-table', help='import only this table', default='', dest='limit_import_table')
    parser.add_argument('-xrcp', '--xrecreate-parameter', help='regenerate random query parameters for each stream', action='store_true', default=False, dest='recreate_parameter')
    parser.add_argument('-xshq', '--xshuffle-queries', help='shuffle query execution order independently per stream', action='store_true', default=False, dest='shuffle_queries')
    parser.add_argument('-xii',  '--xinit-indexes', help='create indexes on all tables after loading', action='store_true', default=False, dest='init_indexes')
    parser.add_argument('-xic',  '--xinit-constraints', help='add primary-key and foreign-key constraints after loading', action='store_true', default=False, dest='init_constraints')
    parser.add_argument('-xis',  '--xinit-statistics', help='run ANALYZE after loading', action='store_true', default=False, dest='init_statistics')
    # YCSB-specific args read by benchmarks.YCSB.configure_workload()
    parser.add_argument('-xwl',  '--xworkload', help='YCSB workload letter', choices=['a', 'b', 'c', 'd', 'e', 'f'], default='a', dest='workload')
    parser.add_argument('-xop',  '--xnum-operations', help='override YCSB operation count in millions (default: derive from --ycsb-rows)', default=None, dest='scaling_factor_operations')
    parser.add_argument('-xtb',  '--xtarget-base', help='YCSB base ops-per-second target', default="16384", dest='target_base')
    parser.add_argument('-xsbs', '--xscaling-batchsize', help='YCSB insert batch size', default="", dest='scaling_batchsize')
    parser.add_argument('-xio',  '--extra-insert-order', help='YCSB key insertion order', default='hashed', choices=['hashed', 'ordered'])
    parser.add_argument('-xnlf', '--xnum-loading-target-factors', help='comma-separated multipliers for the YCSB loading ops target', default="1", dest='num_loading_target_factors')
    parser.add_argument('-xnbf', '--xnum-benchmarking-target-factors', help='comma-separated multipliers for the YCSB benchmarking ops target', default="1", dest='num_benchmarking_target_factors')
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logger_bexhoma = logging.getLogger('bexhoma')
        logger_bexhoma.setLevel(logging.DEBUG)
        logger_loader = logging.getLogger('load_data_asynch')
        logger_loader.setLevel(logging.DEBUG)
    command_args = vars(args)
    code = args.experiment
    SF = str(args.scaling_factor)
    timeout = int(args.timeout)
    num_experiment_to_apply = int(args.num_config)
    ycsb_rows = int(args.ycsb_rows)
    ycsb_operations = ycsb_rows
    ##############
    ### set cluster
    ##############
    cluster = clusters.Kubernetes(context=args.context)
    if args.max_sut is not None:
        cluster.max_sut = int(args.max_sut)
    if code is None:
        code = cluster.code
    ##############
    ### prepare and configure experiment
    ##############
    experiment = TpchYcsbParallelTestExperiment(
        cluster=cluster, SF=SF, timeout=timeout, code=code,
        num_experiment_to_apply=num_experiment_to_apply, ycsb_rows=ycsb_rows)
    if args.max_sut_experiment is not None:
        experiment.max_sut = int(args.max_sut_experiment)
    experiment.prometheus_interval = "30s"
    experiment.prometheus_timeout = "30s"
    experiment.set_additional_labels(
        usecase="tpch-ycsb-parallel-test",
        experiment_design="parallel-loading-and-benchmarking",
    )
    experiment.prepare_testbed(command_args)
    # MixedExperiment.prepare_testbed() calls configure_workload() on every
    # registered benchmark in order (TPCH then YCSB); both call set_workload()
    # with the same keys (name/info/type/defaultParameters), so YCSB's call
    # — running second — silently overwrites TPCH's. Restore a combined,
    # accurate description now that both have run.
    experiment.set_workload(
        name=f"TPC-H + YCSB parallel loading/benchmarking test SF={SF}",
        info=(
            "TEST ONLY: loads TPC-H and YCSB into the same PostgreSQL database in "
            "parallel, then runs the TPC-H query stream and a YCSB workload in "
            "parallel. " + experiment.workload.get('info', '')
        ),
        type='tpch',
    )
    # Combined defaults, broadcast to every loading/benchmarking Job for this
    # config (TPC-H's loader/benchmarker ignore the YCSB_* keys and vice versa
    # — same cross-tool broadcast pattern the TPC-H refresh stream already
    # relies on for its own TPCH_REFRESH_STREAMS/TPCH_REFRESH_STREAM_OFFSET).
    experiment.set_default_loading_parameters(
        SF=SF,
        STORE_RAW_DATA=1,
        STORE_RAW_DATA_RECREATE=0,
        BEXHOMA_SYNCH_LOAD=1,
        BEXHOMA_SYNCH_GENERATE=1,
        TRANSFORM_RAW_DATA=1,
        TPCH_TABLE=args.limit_import_table,
        # ycsb/generator/generator.sh (acting as the YCSB loader) needs these;
        # YCSB_ROWS is used directly, not just as an SF-derived fallback, and
        # YCSB_STATUS is compared with `test $YCSB_STATUS -ne 0` with no
        # default, so it must always be set or the script errors out.
        YCSB_STATUS=1,
        YCSB_WORKLOAD=args.workload,
        YCSB_ROWS=ycsb_rows,
        YCSB_BATCHSIZE=args.scaling_batchsize,
        YCSB_STATUS_INTERVAL=10,
        YCSB_INSERTORDER=args.extra_insert_order,
        YCSB_MAX_EXECUTION=0,
    )
    experiment.set_default_benchmarking_parameters(
        SF=SF,
        DBMSBENCHMARKER_RECREATE_PARAMETER=args.recreate_parameter,
        DBMSBENCHMARKER_SHUFFLE_QUERIES=args.shuffle_queries,
        DBMSBENCHMARKER_DEV=int(args.debug),
        BEXHOMA_SYNCH_LOAD=1,
        YCSB_STATUS=1,
        YCSB_WORKLOAD=args.workload,
        YCSB_ROWS=ycsb_rows,
        YCSB_OPERATIONS=ycsb_operations,
        YCSB_BATCHSIZE=args.scaling_batchsize,
        YCSB_STATUS_INTERVAL=10,
        YCSB_INSERTORDER=args.extra_insert_order,
        YCSB_MAX_EXECUTION=0,
        PARALLEL="1",
        YCSB_THREADCOUNT=4,
        YCSB_TARGET=int(args.target_base),
        BEXHOMA_DBMS_TYPE="jdbc",
        YCSB_MEASUREMENT_TYPE="hdrhistogram",
    )
    ##############
    ### one PostgreSQL configuration
    ##############
    config = configurations.default(experiment=experiment, docker='PostgreSQL', dialect='PostgreSQL', alias='DBMS A2')
    config.set_storage(storageConfiguration='postgresql')
    # TPC-H's own schema ('initschema-tpch.sql', resolved via experiment.script
    # set to 'Schema' by TPCH.configure_workload()) plus the YCSB usertable
    # schema, copied alongside it — both tools load into the same database,
    # so both schemas must exist before either loader starts.
    config.initscript = config.initscript + ['initschema-ycsb-demo.sql']
    config.jobtemplate_loading = "jobtemplate-loading-tpch-PostgreSQL.yml"
    config.set_loading_parameters(
        PODS_TOTAL="1",
        PODS_PARALLEL="1",
        BEXHOMA_TENANT_BY=config.tenant_per,
        BEXHOMA_TENANT_NUM=config.num_tenants,
        BEXHOMA_TENANT_ID=0,
    )
    config.set_loading(parallel=1, num_pods=1)
    # Second, independent loading Job: YCSB, into the same database, at the
    # same time as the TPC-H loader above (this is the feature under test).
    config.add_loading_parameters(
        name="ycsb-loader",
        template="jobtemplate-loading-ycsb.yml",
        benchmarker="ycsb",
        parallelism=1,
        num_pods=1,
        target="sut",
        PARALLEL="1",
        YCSB_THREADCOUNT=4,
        YCSB_TARGET=int(args.target_base),
        YCSB_OPERATIONS=ycsb_rows,
        BEXHOMA_DBMS_TYPE="jdbc",
        YCSB_MEASUREMENT_TYPE="hdrhistogram",
        # Overrides the shared, config-wide SF broadcast from
        # experiment.set_default_loading_parameters(), which carries TPC-H's
        # (possibly fractional, e.g. "0.1") SF -- same reasoning as the SF
        # override on the "ycsb" benchmarker entry above. Without this, the
        # YCSB loader would silently load using TPC-H's SF/row count instead
        # of its own, and evaluators.ycsb's per-connection SF (parsed from
        # this loader's own log header) would misreport YCSB's loading
        # Throughput [SF/h].
        SF=str(ycsb_rows // 1000000 or 1),
    )
    config.set_benchmarking_parameters(
        TENANT_BY=config.tenant_per,
        TENANT_NUM=config.num_tenants,
        BEXHOMA_TENANT_BY=config.tenant_per,
        BEXHOMA_TENANT_NUM=config.num_tenants,
        BEXHOMA_TENANT_ID=0,
    )
    ##############
    ### single client round, single pod each — this is a demo, not a sweep
    ##############
    experiment.add_benchmark_list([1])
    experiment.process()
exit()
