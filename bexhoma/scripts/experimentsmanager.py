"""
CLI tool for managing bexhoma experiments in Kubernetes detached mode.

Provides utilities for monitoring and controlling experiment runs that
are detached from the local process, communicating with Kubernetes pods
to query status and collect results.

Authors: Patrick K. Erdelt
Copyright (C) 2021 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from bexhoma import *
from bexhoma.scripts.cli import EXPERIMENT_MODES
from dbmsbenchmarker import *
import logging
import urllib3
import logging
import argparse
import pandas as pd
from tabulate import tabulate
from datetime import datetime
from prettytable import PrettyTable, ALL
import ast

urllib3.disable_warnings()
logging.basicConfig(level=logging.ERROR)

#: ``status`` of a Kubernetes Job condition that marks it as completed.
_JOB_COMPLETE_CONDITION_TYPE = 'Complete'


def _labels(obj) -> dict:
    """Return a Kubernetes object's metadata labels, or an empty dict if unset."""
    return obj.metadata.labels or {}


def _filter_by_labels(items: list, component: str = '', experiment: str = '', configuration: str = '') -> list:
    """Filter already bulk-fetched Kubernetes objects by label, without any further API calls."""
    filtered = []
    for item in items:
        labels = _labels(item)
        if component and labels.get('component') != component:
            continue
        if experiment and labels.get('experiment') != experiment:
            continue
        if configuration and labels.get('configuration') != configuration:
            continue
        filtered.append(item)
    return filtered


def _pod_status_counts(pods: list) -> dict:
    """Count already bulk-fetched Pod objects by their status phase."""
    counts = {}
    for pod in pods:
        phase = pod.status.phase
        counts[phase] = counts.get(phase, 0) + 1
    return counts


def _job_is_complete(job) -> bool:
    """Return whether a bulk-fetched Job's completions target has been reached (mirrors ``Kubernetes.get_job_status``)."""
    status = job.status
    spec = job.spec
    if status.succeeded is not None and spec.completions is not None and spec.completions <= status.succeeded:
        return True
    if status.succeeded is not None and status.succeeded > 0 and status.conditions:
        return status.conditions[0].type == _JOB_COMPLETE_CONDITION_TYPE
    return False


def manage():
    description = """This tool helps managing running Bexhoma experiments in a Kubernetes cluster.
    """
    print(description)
    # argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('mode', help='manage experiments: stop, get status, connect to dbms or connect to dashboard', choices=EXPERIMENT_MODES)
    parser.add_argument('action', help='for mode dashboard/messagequeue: start or shut down the component; omit to port-forward the dashboard', nargs='?', choices=['start', 'shutdown'], default=None)
    parser.add_argument('-db', '--debug', help='dump debug informations', action='store_true')
    parser.add_argument('-fe', '--force-evaluate', help='force a re-evaluation of the results', action='store_true')
    parser.add_argument('-rp', '--report', help='write a tiered Markdown summary report (report/index.md + detail files) to the result folder', action='store_true')
    parser.add_argument('-e', '--experiment', help='code of experiment', default=None)
    parser.add_argument('-c', '--connection', help='name of DBMS', default=None)
    parser.add_argument('-v', '--verbose', help='gives more details about Kubernetes objects', action='store_true')
    parser.add_argument('-cx', '--context', help='context of Kubernetes (for a multi cluster environment), default is current context', default=None)
    clusterconfig = 'cluster.config'
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
    connection = args.connection
    if args.mode == 'stop':
        cluster = clusters.Kubernetes(clusterconfig, context=args.context)
        if args.experiment is None:
            if connection is None:
                connection = ''
            cluster.stop_sut(configuration=connection)
            cluster.stop_monitoring(configuration=connection)
            cluster.stop_maintaining()
            cluster.stop_loading()
            cluster.stop_benchmarker(configuration=connection)
            #cluster.kubectl('delete all -l experiment='+cluster.code)
            # kubectl delete all -l experiment=1742207308
        else:
            experiment = experiments.base(cluster=cluster, code=args.experiment)
            experiment.stop_sut()
            experiment.stop_monitoring()
            experiment.stop_maintaining()
            experiment.stop_loading()
            experiment.stop_benchmarker()
            cluster.kubectl('delete all -l experiment='+args.experiment)
    elif args.mode == 'summary':
        if not args.experiment is None:
            # -fe re-evaluates by executing a command inside the running dashboard pod,
            # which needs a live cluster connection; a plain summary only reads local files.
            cluster = clusters.Kubernetes(clusterconfig, context=args.context, connect=args.force_evaluate)
            resultfolder = cluster.config['benchmarker']['resultfolder']
            code = args.experiment
            with open(resultfolder+"/"+code+"/queries.config",'r') as inp:
                workload_properties = ast.literal_eval(inp.read())
                match workload_properties['type']:
                    case 'ycsb':
                        experiment = experiments.ycsb(cluster=cluster, code=code)
                    case 'tpcc':
                        experiment = experiments.tpcc(cluster=cluster, code=code)
                    case 'tpch':
                        experiment = experiments.tpch(cluster=cluster, code=code)
                    case 'tpcds':
                        experiment = experiments.tpcds(cluster=cluster, code=code)
                    case 'benchbase':
                        experiment = experiments.benchbase(cluster=cluster, code=code)
                    case _:
                        experiment = experiments.base(cluster=cluster, code=code)
                experiment.num_tenants = workload_properties.get('num_tenants', 0)
                experiment.tenant_per = workload_properties.get('tenant_per', '')
                experiment.multi_tenant_volume = workload_properties.get('multi_tenant_volume', False)
                # regenerate results - only for debugging
                #experiment.evaluate_results()
                #experiment.store_workflow_results()
                if args.force_evaluate:
                    experiment.evaluate_results()
                experiment.show_summary(write_report=args.report)
    elif args.mode == 'dashboard':
        cluster = clusters.Kubernetes(clusterconfig, context=args.context)
        if args.action == 'start':
            cluster.start_dashboard()
        elif args.action == 'shutdown':
            cluster.stop_dashboard()
        else:
            cluster.forward_dashboard_ports()
    elif args.mode == 'messagequeue':
        cluster = clusters.Kubernetes(clusterconfig, context=args.context)
        if args.action == 'shutdown':
            cluster.stop_messagequeue()
        else:
            cluster.start_messagequeue()
    elif args.mode == 'localdashboard':
        cluster = clusters.Kubernetes(clusterconfig, context=args.context)
        import sys
        resultfolder = cluster.config['benchmarker']['resultfolder']
        sys.argv += ['-r',resultfolder]
        sys.argv.remove('localdashboard')
        from dbmsbenchmarker.scripts import dashboardcli
        dashboardcli.startup()
    elif args.mode == 'localresults':
        cluster = clusters.Kubernetes(clusterconfig, context=args.context)
        # path of folder containing experiment results
        resultfolder = cluster.resultfolder
        # create evaluation object for result folder
        evaluate = inspector.inspector(resultfolder)
        # dataframe of experiments
        df = evaluate.get_experiments_preview().sort_values('time')
        df = df.reset_index()
        df['info'] = df['info'].str.replace('. ', '.\n')
        # Create a PrettyTable object
        pt = PrettyTable()
        pt.field_names = df.columns
        pt.align['info'] = 'r'  # 'r' for right alignment
        pt.hrules=ALL
        # Add rows to the PrettyTable
        for _, row in df.iterrows():
            pt.add_row(row)
        # Display the PrettyTable
        print(pt)
    elif args.mode == 'data':
        cluster = clusters.Kubernetes(clusterconfig, context=args.context)
        dashboard_name = cluster.get_dashboard_pod_name()
        if len(dashboard_name) > 0:
            cmd = {}
            cmd['get_data_dir'] = 'du -h /data/'
            stdin, stdout, stderr = cluster.execute_command_in_pod(cmd['get_data_dir'], pod=dashboard_name, container='dashboard')
            print(stdout)
    elif args.mode == 'jupyter':
        import subprocess
        cmd = ["jupyter","notebook","--notebook-dir","images/evaluator_dbmsbenchmarker/notebooks","--NotebookApp.ip","0.0.0.0","--no-browser","--NotebookApp.allow_origin","*"]
        subprocess.Popen(cmd)
    elif args.mode == 'master':
        cluster = clusters.Kubernetes(clusterconfig, context=args.context)
        cluster.forward_sut_port(experiment=args.experiment, configuration=connection)
    elif args.mode == 'status':
        cluster = clusters.Kubernetes(clusterconfig, context=args.context)
        app = cluster.appname
        # single bulk fetch per resource kind: every Pod and PVC is read once
        # here and then filtered/grouped in memory below, instead of issuing
        # one Kubernetes API call per pod/pvc/component/configuration as before
        all_pods = cluster.list_pods_full(app=app)
        all_pvcs = cluster.list_pvcs_full(app=app)
        if args.verbose:
            all_deployments = cluster.list_deployments_full(app=app)
            all_stateful_sets = cluster.list_stateful_sets_full(app=app)
            all_services = cluster.list_services_full(app=app)
            all_jobs = cluster.list_jobs_full(app=app)
        # check dashboard
        dashboard_pods = _filter_by_labels(all_pods, component='dashboard')
        if dashboard_pods:
            print("Dashboard: {}".format(dashboard_pods[0].status.phase))
            # get cluster monitoring Prometheus
            monitoring_running = cluster.is_monitoring_healthy()
            if monitoring_running:
                print("Cluster Prometheus: {}".format("Running"))
            else:
                print("Cluster Prometheus: {}".format("Not running"))
        else:
            print("Dashboard: {}".format("Not running"))
            print("Cluster Prometheus: {}".format("Unknown"))
        # check message queue
        messagequeue_pods = _filter_by_labels(all_pods, component='messagequeue')
        if messagequeue_pods:
            print("Message Queue: {}".format(messagequeue_pods[0].status.phase))
        else:
            print("Message Queue: Not running")
        # get data directory
        if _filter_by_labels(all_pvcs, component='data-source'):
            print("Data directory: {}".format("Running"))
        else:
            print("Data directory: {}".format("Missing"))
        # get result directory
        if _filter_by_labels(all_pvcs, component='results'):
            print("Result directory: {}".format("Running"))
        else:
            print("Result directory: {}".format("Missing"))
        # get all storage volumes
        volumes = {}
        for pvc in _filter_by_labels(all_pvcs, component='storage'):
            pvc_labels = _labels(pvc)
            name = pvc.metadata.name
            volumes[name] = {}
            volumes[name]['configuration'] = pvc_labels['configuration']
            volumes[name]['experiment'] = pvc_labels['experiment']
            volumes[name]['loaded [s]'] = pvc_labels['loaded']
            volumes[name]['timeLoading [s]'] = pvc_labels.get('time_loading', "")
            volumes[name]['dbms'] = pvc_labels['dbms']
            volumes[name]['storage_class_name'] = pvc.spec.storage_class_name
            volumes[name]['storage'] = pvc.spec.resources.requests['storage']
            volumes[name]['status'] = pvc.status.phase
            volumes[name]['size'] = pvc_labels.get('volume_size', "")
            volumes[name]['used'] = pvc_labels.get('volume_used', "")
        if len(volumes) > 0:
            df = pd.DataFrame(volumes).T
            df = df.reindex(index=evaluators.natural_sort(df.index))
            h = ['Volumes'] + list(df.columns)
            print(tabulate(df, headers=h, tablefmt="grid", floatfmt=".2f", showindex="always"))
        # get all worker volumes
        volumes = {}
        for pvc in _filter_by_labels(all_pvcs, component='worker'):
            pvc_labels = _labels(pvc)
            name = pvc.metadata.name
            volumes[name] = {}
            volumes[name]['configuration'] = pvc_labels['configuration']
            volumes[name]['experiment'] = pvc_labels['experiment']
            volumes[name]['dbms'] = pvc_labels['dbms']
            volumes[name]['storage_class_name'] = pvc.spec.storage_class_name
            volumes[name]['storage'] = pvc.spec.resources.requests['storage']
            volumes[name]['status'] = pvc.status.phase
            volumes[name]['size'] = pvc_labels.get('volume_size', "")
            volumes[name]['used'] = pvc_labels.get('volume_used', "")
        if len(volumes) > 0:
            df = pd.DataFrame(volumes).T
            h = ['Volumes of Workers'] + list(df.columns)
            print(tabulate(df, headers=h, tablefmt="grid", floatfmt=".2f", showindex="always"))
        # group already-fetched pods by experiment and configuration
        experiment_set = {
            _labels(pod)['experiment'] for pod in all_pods if 'experiment' in _labels(pod)
        }
        for experiment in experiment_set:
            if args.verbose:
                print(experiment)
            apps = {}
            experiment_pods = _filter_by_labels(all_pods, experiment=experiment)
            pod_labels = {pod.metadata.name: _labels(pod) for pod in experiment_pods}
            configurations = {
                labels['configuration'] for labels in pod_labels.values() if 'configuration' in labels
            }
            for configuration in configurations:
                logging.debug(configuration)
                apps[configuration] = {}
                component = 'sut'
                apps[configuration][component] = ''
                apps[configuration]['loaded [s]'] = ''
                if args.verbose:
                    deployments = [d.metadata.name for d in _filter_by_labels(all_deployments, component=component, experiment=experiment, configuration=configuration)]
                    print("Deployments", deployments)
                    services = [s.metadata.name for s in _filter_by_labels(all_services, component=component, experiment=experiment, configuration=configuration)]
                    print("SUT Services", services)
                pods = _filter_by_labels(experiment_pods, component=component, configuration=configuration)
                if args.verbose:
                    print("SUT Pods", [pod.metadata.name for pod in pods])
                for pod in pods:
                    status = pod.status.phase
                    labels = pod_labels[pod.metadata.name]
                    experimentRun = '{}. '.format(labels['experimentRun']) if 'experimentRun' in labels else ''
                    apps[configuration][component] = "{pod} ({experimentRun}{status})".format(pod='', experimentRun=experimentRun, status=status)
                    if 'loaded' in labels:
                        if labels['loaded'] == 'True':
                            apps[configuration]['loaded [s]'] = labels['time_loading']
                        elif 'time_loading_start' in labels:
                            dt_object = datetime.fromtimestamp(int(labels['time_loading_start']))
                            t = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                            apps[configuration]['loaded [s]'] = 'Started at '+t
                    apps[configuration]['use case'] = labels.get('usecase', "")
                ############
                component = 'worker'
                apps[configuration][component] = ''
                if args.verbose:
                    stateful_sets = [s.metadata.name for s in _filter_by_labels(all_stateful_sets, component=component, experiment=experiment, configuration=configuration)]
                    print("Stateful Sets", stateful_sets)
                    services = [s.metadata.name for s in _filter_by_labels(all_services, component=component, experiment=experiment, configuration=configuration)]
                    print("Worker Services", services)
                pods = _filter_by_labels(experiment_pods, component=component, configuration=configuration)
                if args.verbose:
                    print("Worker Pods", [pod.metadata.name for pod in pods])
                num_pods = _pod_status_counts(pods)
                for status in num_pods.keys():
                    apps[configuration][component] += "({num} {status})".format(num=num_pods[status], status=status)
                ############
                component = 'pool'
                apps[configuration][component] = ''
                if args.verbose:
                    stateful_sets = [s.metadata.name for s in _filter_by_labels(all_stateful_sets, component=component, experiment=experiment, configuration=configuration)]
                    print("Stateful Sets", stateful_sets)
                    services = [s.metadata.name for s in _filter_by_labels(all_services, component=component, experiment=experiment, configuration=configuration)]
                    print("Pooling Services", services)
                pods = _filter_by_labels(experiment_pods, component=component, configuration=configuration)
                if args.verbose:
                    print("Pooling Pods", [pod.metadata.name for pod in pods])
                pods_per_status = _pod_status_counts(pods)
                for status, number in pods_per_status.items():
                    apps[configuration][component] += "{pod} ({status})".format(pod=number, status=status)
                ############
                component = 'maintaining'
                apps[configuration][component] = ''
                if args.verbose:
                    stateful_sets = [s.metadata.name for s in _filter_by_labels(all_stateful_sets, component=component, experiment=experiment, configuration=configuration)]
                    print("Stateful Sets", stateful_sets)
                    services = [s.metadata.name for s in _filter_by_labels(all_services, component=component, experiment=experiment, configuration=configuration)]
                    print("Maintaining Services", services)
                pods = _filter_by_labels(experiment_pods, component=component, configuration=configuration)
                if args.verbose:
                    print("Maintaining Pods", [pod.metadata.name for pod in pods])
                num_pods = _pod_status_counts(pods)
                for status in num_pods.keys():
                    apps[configuration][component] += "({num} {status})".format(num=num_pods[status], status=status)
                ############
                component = 'loading'
                apps[configuration][component] = ''
                if args.verbose:
                    stateful_sets = [s.metadata.name for s in _filter_by_labels(all_stateful_sets, component=component, experiment=experiment, configuration=configuration)]
                    print("Stateful Sets", stateful_sets)
                    services = [s.metadata.name for s in _filter_by_labels(all_services, component=component, experiment=experiment, configuration=configuration)]
                    print("Loading Services", services)
                pods = _filter_by_labels(experiment_pods, component=component, configuration=configuration)
                if args.verbose:
                    print("Loading Pods", [pod.metadata.name for pod in pods])
                num_pods = _pod_status_counts(pods)
                for status in num_pods.keys():
                    apps[configuration][component] += "({num} {status})".format(num=num_pods[status], status=status)
                ############
                component = 'monitoring'
                apps[configuration][component] = ''
                if args.verbose:
                    stateful_sets = [s.metadata.name for s in _filter_by_labels(all_stateful_sets, component=component, experiment=experiment, configuration=configuration)]
                    print("Stateful Sets", stateful_sets)
                    services = [s.metadata.name for s in _filter_by_labels(all_services, component=component, experiment=experiment, configuration=configuration)]
                    print("Monitoring Services", services)
                pods = _filter_by_labels(experiment_pods, component=component, configuration=configuration)
                if args.verbose:
                    print("Monitoring Pods", [pod.metadata.name for pod in pods])
                for pod in pods:
                    apps[configuration][component] += "{pod} ({status})".format(pod='', status=pod.status.phase)
                ############
                component = 'benchmarker'
                apps[configuration][component] = ''
                if args.verbose:
                    jobs = _filter_by_labels(all_jobs, component=component, experiment=experiment, configuration=configuration)
                    # status per job
                    for job in jobs:
                        print(job.metadata.name, _job_is_complete(job))
                pods = _filter_by_labels(experiment_pods, component=component, configuration=configuration)
                if args.verbose:
                    print("Benchmarker Pods", [pod.metadata.name for pod in pods])
                num_pods = {}
                for pod in pods:
                    status = pod.status.phase
                    labels = pod_labels[pod.metadata.name]
                    experimentRun = '{}. '.format(labels['client']) if 'client' in labels else ''
                    status_extended = "{pod} ({experimentRun}{status})".format(pod='', experimentRun=experimentRun, status=status)
                    num_pods[status_extended] = 1 if not status_extended in num_pods else num_pods[status_extended]+1
                for status in num_pods.keys():
                        apps[configuration][component] += "{num}x{status}".format(num=num_pods[status], status=status)
            df = pd.DataFrame(apps)
            df = df.T
            df.sort_index(inplace=True)
            df.index.name = experiment
            h = [df.index.name] + list(df.columns)
            if args.verbose:
                # this shows all columns even if empty
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(tabulate(df, headers=h, tablefmt="grid", floatfmt=".2f", showindex="always"))
            else:
                df_empty = df.eq('')
                df_short = df.drop(df_empty.columns[df_empty.all()].tolist(), axis=1)
                h_short = [df_short.index.name] + list(df_short.columns)
                # this shows only columns with not all empty
                df = df.reindex(index=evaluators.natural_sort(df.index))
                print(tabulate(df_short, headers=h_short, tablefmt="grid", floatfmt=".2f", showindex="always"))
    benchmarker.logger.setLevel(logging.ERROR)
