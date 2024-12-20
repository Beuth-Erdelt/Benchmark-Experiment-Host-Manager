"""
:Date: 2023-08-04
:Version: 1.0
:Authors: Patrick K. Erdelt

Performs experiment by running custom SQL queries.
"""
from bexhoma import *
from dbmsbenchmarker import *
import logging
import urllib3
import logging
import argparse
import time
from timeit import default_timer
import datetime
import subprocess
import psutil

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    description = """Performs experiment by running custom SQL queries."""
    # argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('mode', help='profile the import or run the TPC-H queries', choices=['run'])
    parser.add_argument('-aws', '--aws', help='fix components to node groups at AWS', action='store_true', default=False)
    parser.add_argument('-dbms', help='DBMS to run the experiment on', choices=['Dummy'])
    parser.add_argument('-db', '--debug', help='dump debug informations', action='store_true')
    parser.add_argument('-cx', '--context', help='context of Kubernetes (for a multi cluster environment), default is current context', default=None)
    parser.add_argument('-e', '--experiment', help='sets experiment code for continuing started experiment', default=None)
    parser.add_argument('-m', '--monitoring', help='activates monitoring', action='store_true')
    parser.add_argument('-mc', '--monitoring-cluster', help='activates monitoring for all nodes of cluster', action='store_true', default=False)
    parser.add_argument('-ms', '--max-sut', help='maximum number of parallel DBMS configurations, default is no limit', default=None)
    parser.add_argument('-dt', '--datatransfer', help='activates datatransfer', action='store_true', default=False)
    parser.add_argument('-md', '--monitoring-delay', help='time to wait [s] before execution of the runs of a query', default=10)
    parser.add_argument('-nr', '--num-run', help='number of runs per query', default=1)
    parser.add_argument('-nc', '--num-config', help='number of runs per configuration', default=1)
    parser.add_argument('-ne', '--num-query-executors', help='comma separated list of number of parallel clients', default="1")
    parser.add_argument('-t', '--timeout', help='timeout for a run of a query', default=180)
    parser.add_argument('-rr', '--request-ram', help='request ram', default='16Gi')
    parser.add_argument('-rc', '--request-cpu', help='request cpus', default='4')
    parser.add_argument('-rct', '--request-cpu-type', help='request node having node label cpu=', default='')
    parser.add_argument('-rg', '--request-gpu', help='request number of gpus', default=1)
    parser.add_argument('-rgt', '--request-gpu-type', help='request node having node label gpu=', default='a100')
    parser.add_argument('-rst', '--request-storage-type', help='request persistent storage of certain type', default=None, choices=[None, '', 'local-hdd', 'shared'])
    parser.add_argument('-rss', '--request-storage-size', help='request persistent storage of certain size', default='10Gi')
    parser.add_argument('-rnn', '--request-node-name', help='request a specific node', default=None)
    parser.add_argument('-tr', '--test-result', help='test if result fulfills some basic requirements', action='store_true', default=False)
    parser.add_argument('-rcp', '--recreate-parameter', help='recreate parameter for randomized queries', default=None)
    # evaluate args
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.DEBUG)
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
    ##############
    ### specific to: dbmsbenchmarker
    ##############
    recreate_parameter = args.recreate_parameter
    ##############
    ### set cluster
    ##############
    aws = args.aws
    if aws:
        cluster = clusters.aws(context=args.context)
        # scale up
        node_sizes = {
            'auxiliary': 1,
            'sut-mid': 1,
            'benchmarker': 1
        }
        #cluster.scale_nodegroups(node_sizes)
    else:
        cluster = clusters.kubernetes(context=args.context)
    cluster_name = cluster.contextdata['clustername']
    if args.max_sut is not None:
        cluster.max_sut = int(args.max_sut)
    # set experiment
    if code is None:
        code = cluster.code
    ##############
    ### prepare and configure experiment
    ##############
    experiment = experiments.example(cluster=cluster, timeout=timeout, code=code, num_experiment_to_apply=num_experiment_to_apply, queryfile='queries.config')
    #cluster.set_experiments_configfolder('experiments/example')
    experiment.prometheus_interval = "10s"
    experiment.prometheus_timeout = "10s"
    # remove running dbms
    #experiment.clean()
    experiment.prepare_testbed(command_args)
    num_loading_pods = experiment.get_parameter_as_list('num_loading_pods')
    num_loading_threads = experiment.get_parameter_as_list('num_loading_threads')
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
    cluster.max_sut = 1 # can only run 1 in same cluster because of fixed service
    ##############
    ### add configs of dbms to be tested
    ##############
    if args.dbms == "Dummy":
        # Dummy DBMS
        name_format = 'Dummy-{cluster}'
        config = configurations.default(experiment=experiment, docker='Dummy', configuration=name_format.format(cluster=cluster_name), dialect='PostgreSQL', alias='DBMS A1')
        config.loading_finished = True
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
    # total time of experiment
    start = default_timer()
    start_datetime = str(datetime.datetime.now())
    print("{:30s}: has code {}".format("Experiment",experiment.code))
    print("{:30s}: starts at {} ({})".format("Experiment",start_datetime, start))
    print("{:30s}: {}".format("Experiment",experiment.workload['info']))
    # run workflow
    experiment.work_benchmark_list()
    # total time of experiment
    end = default_timer()
    end_datetime = str(datetime.datetime.now())
    duration_experiment = end - start
    print("{:30s}: ends at {} ({}) - {:.2f}s total".format("Experiment",end_datetime, end, duration_experiment))
    ##################
    experiment.evaluate_results()
    experiment.stop_benchmarker()
    experiment.stop_sut()
    #experiment.zip() # OOM? exit code 137
    if test_result:
        test_result_code = experiment.test_results()
        if test_result_code == 0:
            print("Test successful!")
    cluster.restart_dashboard()
    experiment.show_summary()
exit()
