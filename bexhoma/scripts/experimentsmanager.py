"""
    This script contains some code snippets for testing the detached mode in Kubernetes

    Copyright (C) 2021  Patrick Erdelt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from bexhoma import *
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


def manage():
    description = """This tool helps managing running Bexhoma experiments in a Kubernetes cluster.
    """
    print(description)
    # argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('mode', help='manage experiments: stop, get status, connect to dbms or connect to dashboard', choices=['stop','status','dashboard','localdashboard','localresults','jupyter','master','data','summary'])
    parser.add_argument('-db', '--debug', help='dump debug informations', action='store_true')
    parser.add_argument('-fe', '--force-evaluate', help='force a re-evaluation of the results', action='store_true')
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
        cluster = clusters.kubernetes(clusterconfig, context=args.context)
        if args.experiment is None:
            experiment = experiments.default(cluster=cluster, code=cluster.code)
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
            experiment = experiments.default(cluster=cluster, code=args.experiment)
            experiment.stop_sut()
            experiment.stop_monitoring()
            experiment.stop_maintaining()
            experiment.stop_loading()
            experiment.stop_benchmarker()
            cluster.kubectl('delete all -l experiment='+args.experiment)
    elif args.mode == 'summary':
        if not args.experiment is None:
            cluster = clusters.kubernetes(clusterconfig, context=args.context)
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
                    case 'benchbase':
                        experiment = experiments.benchbase(cluster=cluster, code=code)
                    case _:
                        experiment = experiments.default(cluster=cluster, code=code)
                # regenerate results - only for debugging
                #experiment.evaluate_results()
                #experiment.store_workflow_results()
                if args.force_evaluate:
                    experiment.evaluate_results()
                experiment.show_summary()
    elif args.mode == 'dashboard':
        cluster = clusters.kubernetes(clusterconfig, context=args.context)
        cluster.connect_dashboard()
    elif args.mode == 'localdashboard':
        cluster = clusters.kubernetes(clusterconfig, context=args.context)
        import sys
        resultfolder = cluster.config['benchmarker']['resultfolder']
        sys.argv += ['-r',resultfolder]
        sys.argv.remove('localdashboard')
        from dbmsbenchmarker.scripts import dashboardcli
        dashboardcli.startup()
    elif args.mode == 'localresults':
        cluster = clusters.kubernetes(clusterconfig, context=args.context)
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
        cluster = clusters.kubernetes(clusterconfig, context=args.context)
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
        cluster = clusters.kubernetes(clusterconfig, context=args.context)
        cluster.connect_master(experiment=args.experiment, configuration=connection)
    elif args.mode == 'status':
        cluster = clusters.kubernetes(clusterconfig, context=args.context)
        app = cluster.appname
        # check dashboard
        dashboard_name = cluster.get_dashboard_pod_name()
        if len(dashboard_name) > 0:
            status = cluster.get_pod_status(dashboard_name)
            print("Dashboard: {}".format(status))
            # get cluster monitoring Prometheus
            monitoring_running = cluster.test_if_monitoring_healthy()
            if monitoring_running:
                print("Cluster Prometheus: {}".format("Running"))
            else:
                print("Cluster Prometheus: {}".format("Not running"))
        else:
            print("Dashboard: {}".format("Not running"))
            print("Cluster Prometheus: {}".format("Unknown"))
        # check message queue
        messagequeue_name = cluster.get_pods(component='messagequeue')
        if len(messagequeue_name) > 0:
            status = cluster.get_pod_status(messagequeue_name[0])
            print("Message Queue: {}".format(status))
        else:
            print("Message Queue: Not running")
        # get data directory
        pvcs = cluster.get_pvc(app=app, component='data-source', experiment='', configuration='')
        if len(pvcs) > 0:
            print("Data directory: {}".format("Running"))
        else:
            print("Data directory: {}".format("Missing"))
        # get result directory
        pvcs = cluster.get_pvc(app=app, component='results', experiment='', configuration='')
        if len(pvcs) > 0:
            print("Result directory: {}".format("Running"))
        else:
            print("Result directory: {}".format("Missing"))
        # get all storage volumes
        pvcs = cluster.get_pvc(app=app, component='storage', experiment='', configuration='')
        #print("PVCs", pvcs)
        volumes = {}
        for pvc in pvcs:
            volumes[pvc] = {}
            pvcs_labels = cluster.get_pvc_labels(app=app, component='storage', experiment='', configuration='', pvc=pvc)
            #print("PVCsLabels", pvcs_labels)
            pvc_labels = pvcs_labels[0]
            volumes[pvc]['configuration'] = pvc_labels['configuration']
            volumes[pvc]['experiment'] = pvc_labels['experiment']
            volumes[pvc]['loaded [s]'] = pvc_labels['loaded']
            if 'timeLoading' in pvc_labels:
                volumes[pvc]['timeLoading [s]'] = pvc_labels['timeLoading']
            else:
                volumes[pvc]['timeLoading [s]'] = ""
            volumes[pvc]['dbms'] = pvc_labels['dbms']
            #volumes[pvc]['labels'] = pvcs_label
            pvcs_specs = cluster.get_pvc_specs(app=app, component='storage', experiment='', configuration='', pvc=pvc)
            pvc_specs = pvcs_specs[0]
            #print("PVCsSpecs", pvcs_specs)
            #volumes[pvc]['specs'] = pvc_specs
            volumes[pvc]['storage_class_name'] = pvc_specs.storage_class_name
            volumes[pvc]['storage'] = pvc_specs.resources.requests['storage']
            pvcs_status = cluster.get_pvc_status(app=app, component='storage', experiment='', configuration='', pvc=pvc)
            #print("PVCsStatus", pvcs_status)
            volumes[pvc]['status'] = pvcs_status[0].phase
            if 'volume_size' in pvc_labels:
                volumes[pvc]['size'] = pvc_labels['volume_size']
            else:
                volumes[pvc]['size'] = ""
            if 'volume_used' in pvc_labels:
                volumes[pvc]['used'] = pvc_labels['volume_used']
            else:
                volumes[pvc]['used'] = ""
        #print(volumes)
        if len(volumes) > 0:
            df = pd.DataFrame(volumes).T
            #print(df)
            df = df.reindex(index=evaluators.natural_sort(df.index))
            h = ['Volumes'] + list(df.columns)
            print(tabulate(df, headers=h, tablefmt="grid", floatfmt=".2f", showindex="always"))
        # get all worker volumes
        pvcs = cluster.get_pvc(app=app, component='worker', experiment='', configuration='')
        #print("PVCs", pvcs)
        volumes = {}
        for pvc in pvcs:
            volumes[pvc] = {}
            pvcs_labels = cluster.get_pvc_labels(app=app, component='worker', experiment='', configuration='', pvc=pvc)
            #print("PVCsLabels", pvcs_labels)
            pvc_labels = pvcs_labels[0]
            volumes[pvc]['configuration'] = pvc_labels['configuration']
            volumes[pvc]['experiment'] = pvc_labels['experiment']
            #volumes[pvc]['loaded [s]'] = pvc_labels['loaded']
            #if 'timeLoading' in pvc_labels:
            #    volumes[pvc]['timeLoading [s]'] = pvc_labels['timeLoading']
            #else:
            #    volumes[pvc]['timeLoading [s]'] = ""
            volumes[pvc]['dbms'] = pvc_labels['dbms']
            #volumes[pvc]['labels'] = pvcs_label
            pvcs_specs = cluster.get_pvc_specs(app=app, component='worker', experiment='', configuration='', pvc=pvc)
            pvc_specs = pvcs_specs[0]
            #print("PVCsSpecs", pvcs_specs)
            #volumes[pvc]['specs'] = pvc_specs
            volumes[pvc]['storage_class_name'] = pvc_specs.storage_class_name
            volumes[pvc]['storage'] = pvc_specs.resources.requests['storage']
            pvcs_status = cluster.get_pvc_status(app=app, component='worker', experiment='', configuration='', pvc=pvc)
            #print("PVCsStatus", pvcs_status)
            volumes[pvc]['status'] = pvcs_status[0].phase
            if 'volume_size' in pvc_labels:
                volumes[pvc]['size'] = pvc_labels['volume_size']
            else:
                volumes[pvc]['size'] = ""
            if 'volume_used' in pvc_labels:
                volumes[pvc]['used'] = pvc_labels['volume_used']
            else:
                volumes[pvc]['used'] = ""
        #print(volumes)
        if len(volumes) > 0:
            df = pd.DataFrame(volumes).T
            #print(df)
            h = ['Volumes of Workers'] + list(df.columns)
            print(tabulate(df, headers=h, tablefmt="grid", floatfmt=".2f", showindex="always"))
        # get all pods
        pod_labels = cluster.get_pods_labels(app=app)
        #print("Pod Labels", pod_labels)
        experiment_set = set()
        for pod, labels in pod_labels.items():
            if 'experiment' in labels:
                experiment_set.add(labels['experiment'])
        #print(experiment_set)
        for experiment in experiment_set:
            if args.verbose:
                print(experiment)
            apps = {}
            pod_labels = cluster.get_pods_labels(app=app, experiment=experiment)
            configurations = set()
            for pod, labels in pod_labels.items():
                if 'configuration' in labels:
                    configurations.add(labels['configuration'])
            for configuration in configurations:
                logging.debug(configuration)
                apps[configuration] = {}
                component = 'sut'
                apps[configuration][component] = ''
                apps[configuration]['loaded [s]'] = ''
                if args.verbose:
                    deployments = cluster.get_deployments(app=app, component=component, experiment=experiment, configuration=configuration)
                    print("Deployments", deployments)
                    services = cluster.get_services(app=app, component=component, experiment=experiment, configuration=configuration)
                    print("SUT Services", services)
                pods = cluster.get_pods(app=app, component=component, experiment=experiment, configuration=configuration)
                if args.verbose:
                    print("SUT Pods", pods)
                for pod in pods:
                    status = cluster.get_pod_status(pod)
                    #print(status)
                    if pod in pod_labels and 'experimentRun' in pod_labels[pod]:
                        experimentRun = '{}. '.format(pod_labels[pod]['experimentRun'])
                    else:
                        experimentRun = ''
                    apps[configuration][component] = "{pod} ({experimentRun}{status})".format(pod='', experimentRun=experimentRun, status=status)
                    if pod in pod_labels and 'loaded' in pod_labels[pod]:
                        if pod_labels[pod]['loaded'] == 'True':
                            #apps[configuration]['loaded'] += "True"
                            apps[configuration]['loaded [s]'] = pod_labels[pod]['timeLoading']#+' [s]'
                        elif 'timeLoadingStart' in pod_labels[pod]:
                            #apps[configuration]['loaded'] = 'Started at '+pod_labels[pod]['timeLoadingStart']
                            dt_object = datetime.fromtimestamp(int(pod_labels[pod]['timeLoadingStart']))
                            t = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                            apps[configuration]['loaded [s]'] = 'Started at '+t
                        #if 'timeLoadingStart' in pod_labels[pod]:
                        #    apps[configuration]['loaded'] += ' '+pod_labels[pod]['timeLoadingStart']
                        #if 'timeLoadingEnd' in pod_labels[pod]:
                        #    apps[configuration]['loaded'] += '-'+pod_labels[pod]['timeLoadingEnd']
                        #if 'timeLoading' in pod_labels[pod]:
                        #    apps[configuration]['loaded'] += '='+pod_labels[pod]['timeLoading']+'s'
                    if pod in pod_labels and 'usecase' in pod_labels[pod]:
                        apps[configuration]['use case'] = pod_labels[pod]['usecase']
                    else:
                        apps[configuration]['use case'] = ""
                ############
                component = 'worker'
                apps[configuration][component] = ''
                if args.verbose:
                    stateful_sets = cluster.get_stateful_sets(app=app, component=component, experiment=experiment, configuration=configuration)
                    print("Stateful Sets", stateful_sets)
                    services = cluster.get_services(app=app, component=component, experiment=experiment, configuration=configuration)
                    print("Worker Services", services)
                pods = cluster.get_pods(app=app, component=component, experiment=experiment, configuration=configuration)
                if args.verbose:
                    print("Worker Pods", pods)
                num_pods = {}
                for pod in pods:
                    status = cluster.get_pod_status(pod)
                    #print(status)
                    #apps[configuration][component] += "{pod} ({status})".format(pod='', status=status)
                    num_pods[status] = 1 if not status in num_pods else num_pods[status]+1
                #print(num_pods)
                for status in num_pods.keys():
                        apps[configuration][component] += "({num} {status})".format(num=num_pods[status], status=status)
                ############
                component = 'pool'
                apps[configuration][component] = ''
                if args.verbose:
                    stateful_sets = cluster.get_stateful_sets(app=app, component=component, experiment=experiment, configuration=configuration)
                    print("Stateful Sets", stateful_sets)
                    services = cluster.get_services(app=app, component=component, experiment=experiment, configuration=configuration)
                    print("Pooling Services", services)
                pods = cluster.get_pods(app=app, component=component, experiment=experiment, configuration=configuration)
                if args.verbose:
                    print("Pooling Pods", pods)
                pods_per_status = {}
                for pod in pods:
                    status = cluster.get_pod_status(pod)
                    pods_per_status[status] = pods_per_status[status]+1 if status in pods_per_status  else 1
                    #print(status)
                for status, number in pods_per_status.items():
                    apps[configuration][component] += "{pod} ({status})".format(pod=number, status=status)
                ############
                component = 'pool'
                apps[configuration][component] = ''
                if args.verbose:
                    stateful_sets = cluster.get_stateful_sets(app=app, component=component, experiment=experiment, configuration=configuration)
                    print("Stateful Sets", stateful_sets)
                    services = cluster.get_services(app=app, component=component, experiment=experiment, configuration=configuration)
                    print("Pooling Services", services)
                pods = cluster.get_pods(app=app, component=component, experiment=experiment, configuration=configuration)
                if args.verbose:
                    print("Pooling Pods", pods)
                pods_per_status = {}
                for pod in pods:
                    status = cluster.get_pod_status(pod)
                    pods_per_status[status] = pods_per_status[status]+1 if status in pods_per_status  else 1
                    #print(status)
                for status, number in pods_per_status.items():
                    apps[configuration][component] += "{pod} ({status})".format(pod=number, status=status)
                ############
                component = 'pool'
                apps[configuration][component] = ''
                if args.verbose:
                    stateful_sets = cluster.get_stateful_sets(app=app, component=component, experiment=experiment, configuration=configuration)
                    print("Stateful Sets", stateful_sets)
                    services = cluster.get_services(app=app, component=component, experiment=experiment, configuration=configuration)
                    print("Pooling Services", services)
                pods = cluster.get_pods(app=app, component=component, experiment=experiment, configuration=configuration)
                if args.verbose:
                    print("Pooling Pods", pods)
                pods_per_status = {}
                for pod in pods:
                    status = cluster.get_pod_status(pod)
                    pods_per_status[status] = pods_per_status[status]+1 if status in pods_per_status  else 1
                    #print(status)
                for status, number in pods_per_status.items():
                    apps[configuration][component] += "{pod} ({status})".format(pod=number, status=status)
                ############
                component = 'maintaining'
                apps[configuration][component] = ''
                if args.verbose:
                        stateful_sets = cluster.get_stateful_sets(app=app, component=component, experiment=experiment, configuration=configuration)
                        print("Stateful Sets", stateful_sets)
                        services = cluster.get_services(app=app, component=component, experiment=experiment, configuration=configuration)
                        print("Maintaining Services", services)
                pods = cluster.get_pods(app=app, component=component, experiment=experiment, configuration=configuration)
                if args.verbose:
                        print("Maintaining Pods", pods)
                num_pods = {}
                for pod in pods:
                        status = cluster.get_pod_status(pod)
                        #print(status)
                        #apps[configuration][component] += "{pod} ({status})".format(pod='', status=status)
                        num_pods[status] = 1 if not status in num_pods else num_pods[status]+1
                #print(num_pods)
                for status in num_pods.keys():
                        apps[configuration][component] += "({num} {status})".format(num=num_pods[status], status=status)
                ############
                component = 'loading'
                apps[configuration][component] = ''
                if args.verbose:
                        stateful_sets = cluster.get_stateful_sets(app=app, component=component, experiment=experiment, configuration=configuration)
                        print("Stateful Sets", stateful_sets)
                        services = cluster.get_services(app=app, component=component, experiment=experiment, configuration=configuration)
                        print("Loading Services", services)
                pods = cluster.get_pods(app=app, component=component, experiment=experiment, configuration=configuration)
                if args.verbose:
                        print("Loading Pods", pods)
                num_pods = {}
                for pod in pods:
                        status = cluster.get_pod_status(pod)
                        #print(status)
                        #apps[configuration][component] += "{pod} ({status})".format(pod='', status=status)
                        num_pods[status] = 1 if not status in num_pods else num_pods[status]+1
                #print(num_pods)
                for status in num_pods.keys():
                        apps[configuration][component] += "({num} {status})".format(num=num_pods[status], status=status)
                ############
                component = 'monitoring'
                apps[configuration][component] = ''
                if args.verbose:
                    stateful_sets = cluster.get_stateful_sets(app=app, component=component, experiment=experiment, configuration=configuration)
                    print("Stateful Sets", stateful_sets)
                    services = cluster.get_services(app=app, component=component, experiment=experiment, configuration=configuration)
                    print("Monitoring Services", services)
                pods = cluster.get_pods(app=app, component=component, experiment=experiment, configuration=configuration)
                if args.verbose:
                    print("Monitoring Pods", pods)
                for pod in pods:
                    status = cluster.get_pod_status(pod)
                    #print(status)
                    apps[configuration][component] += "{pod} ({status})".format(pod='', status=status)
                ############
                component = 'benchmarker'
                apps[configuration][component] = ''
                if args.verbose:
                    jobs = cluster.get_jobs(app=app, component=component, experiment=experiment, configuration=configuration)
                    # status per job
                    for job in jobs:
                        success = cluster.get_job_status(job)
                        print(job, success)
                # all pods to these jobs
                pods = cluster.get_job_pods(app=app, component=component, experiment=experiment, configuration=configuration)
                if args.verbose:
                    print("Benchmarker Pods", pods)
                num_pods = {}
                for pod in pods:
                    status = cluster.get_pod_status(pod)
                    #print(status)
                    if pod in pod_labels and 'client' in pod_labels[pod]:
                        experimentRun = '{}. '.format(pod_labels[pod]['client'])
                    else:
                        experimentRun = ''
                    status_extended = "{pod} ({experimentRun}{status})".format(pod='', experimentRun=experimentRun, status=status)
                    num_pods[status_extended] = 1 if not status_extended in num_pods else num_pods[status_extended]+1
                    #apps[configuration][component] += "{pod} ({experimentRun}{status})".format(pod='', experimentRun=experimentRun, status=status_extended)
                for status in num_pods.keys():
                        apps[configuration][component] += "{num}x{status}".format(num=num_pods[status], status=status)
            #print(apps)
            df = pd.DataFrame(apps)
            df = df.T
            df.sort_index(inplace=True)
            df.index.name = experiment
            #print(df)
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
