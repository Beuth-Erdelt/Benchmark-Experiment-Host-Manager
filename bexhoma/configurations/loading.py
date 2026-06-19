"""Loading coordination and async data-loading for bexhoma configurations."""
from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import time
import threading
from datetime import datetime
from math import ceil
from timeit import default_timer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import SutConfiguration

__all__ = ['LoadingCoordinator', 'load_data_asynch']


def load_data_asynch(
    app, component, experiment, configuration, pod_sut, scriptfolder,
    commands, loadData, path, volume, context, service_name,
    time_offset=0, time_start_int=0, script_type='loaded',
    namespace='', num_tenants=0, id_tenant=0, database=[],
):
    """Execute loading scripts inside the SUT pod in a background thread.

    Runs SQL and shell scripts in sequence inside the pod, labels the SUT pod
    and its PVC with timing and completion metadata, and handles multi-tenant
    ordering via a count-down label on the pod.

    :param app: App label for the SUT pod.
    :param component: Component label (``'sut'``).
    :param experiment: Experiment code.
    :param configuration: DBMS configuration name.
    :param pod_sut: Name of the SUT pod to execute commands in.
    :param scriptfolder: Remote path inside the pod where scripts reside.
    :param commands: List of script filenames to execute.
    :param loadData: Shell command template with ``{scriptname}`` placeholder.
    :param path: Local result folder path for log files.
    :param volume: PVC name to label (empty string skips PVC labelling).
    :param context: Kubernetes context string for kubectl.
    :param service_name: Service name injected into ``loadData`` as ``{service_name}``.
    :param time_offset: Previously elapsed seconds added to the total.
    :param time_start_int: Unix timestamp of when loading started (0 = compute now).
    :param script_type: Label key written to pod/PVC (e.g. ``'loaded'``, ``'indexed'``).
    :param namespace: Kubernetes namespace injected into ``loadData``.
    :param num_tenants: Total number of tenants; 0 means single-tenant mode.
    :param id_tenant: Index of this tenant (0-based).
    :param database: List of database names to iterate scripts over.
    """
    logger = logging.getLogger('load_data_asynch')

    def execute_command_in_pod_sut(command, pod, context):
        fullcommand = (
            'kubectl --context {context} exec {pod} --container=dbms -- bash -c "{command}"'
            .format(context=context, pod=pod,
                    command=command.replace('"', '\\"').replace('\n', '\\n')))
        logger.debug('execute_command_in_pod_sut({})'.format(fullcommand))
        proc = subprocess.Popen(
            fullcommand, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        logger.debug(stdout.decode('utf-8'))
        logger.debug(stderr.decode('utf-8'))
        return "", stdout.decode('utf-8'), stderr.decode('utf-8')

    def kubectl(command, context):
        fullcommand = 'kubectl --context {context} {command}'.format(
            context=context, command=command)
        logger.debug('execute_command_in_pod_sut({})'.format(fullcommand))
        proc = subprocess.Popen(
            fullcommand, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        logger.debug(stdout.decode('utf-8'))
        logger.debug(stderr.decode('utf-8'))
        return stdout.decode('utf-8')

    time_scriptgroup_start = default_timer()
    if time_start_int == 0:
        now = datetime.utcnow()
        time_now = str(datetime.now())
        timeLoadingStart = int(datetime.timestamp(
            datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S.%f')))
    else:
        timeLoadingStart = int(time_start_int)
    logger.debug("#### time_scriptgroup_start: " + str(time_scriptgroup_start))
    logger.debug("#### timeLoadingStart: " + str(timeLoadingStart))
    logger.debug("#### timeLoading before scrips: " + str(time_offset))
    # mark pod as loading started
    labels = dict()
    labels[script_type] = 'False'
    labels["num_tenants"] = num_tenants
    if (num_tenants > 0 and id_tenant == 0) or num_tenants == 0:
        logger.debug(f"#### First tenant {id_tenant} logs starting time")
        labels['timeLoadingStart'] = timeLoadingStart
        labels['num_tenants_ready'] = 0
    fullcommand = 'label pods ' + pod_sut + ' --overwrite '
    for key, value in labels.items():
        fullcommand = fullcommand + " {key}={value}".format(key=key, value=value)
    kubectl(fullcommand, context)
    if len(volume) > 0:
        fullcommand = 'label pvc ' + volume + ' --overwrite '
        for key, value in labels.items():
            fullcommand = fullcommand + " {key}={value}".format(key=key, value=value)
        kubectl(fullcommand, context)
    # execute scripts
    times_script = dict()
    shellcommand = 'if [ -f {scriptname} ]; then sh {scriptname}; else exit 0; fi'
    for db in database:
        for c in commands:
            time_scrip_start = default_timer()
            filename, file_extension = os.path.splitext(c)
            if file_extension.lower() == '.sql':
                _, stdout, stderr = execute_command_in_pod_sut(
                    loadData.format(scriptname=scriptfolder + c,
                                    service_name=service_name,
                                    namespace=namespace, database=db),
                    pod_sut, context)
                filename_log = (
                    path + '/{app}-loading-{configuration}-{filename}-{database}{extension}.log'
                    .format(app=app, configuration=configuration,
                            filename=filename, database=db,
                            extension=file_extension.lower()).lower())
                if len(stdout) > 0:
                    with open(filename_log, 'w') as file:
                        file.write(stdout)
                filename_log = (
                    path + '/{app}-loading-{configuration}-{filename}-{database}{extension}.error'
                    .format(app=app, configuration=configuration,
                            filename=filename, database=db,
                            extension=file_extension.lower()).lower())
                if len(stderr) > 0:
                    with open(filename_log, 'w') as file:
                        file.write(stderr)
            elif file_extension.lower() == '.sh':
                _, stdout, stderr = execute_command_in_pod_sut(
                    shellcommand.format(scriptname=scriptfolder + c,
                                        service_name=service_name,
                                        namespace=namespace, database=db),
                    pod_sut, context)
                filename_log = (
                    path + '/{app}-loading-{configuration}-{filename}{database}{extension}.log'
                    .format(app=app, configuration=configuration,
                            filename=filename, database=db,
                            extension=file_extension.lower()).lower())
                if len(stdout) > 0:
                    with open(filename_log, 'w') as file:
                        file.write(stdout)
                filename_log = (
                    path + '/{app}-loading-{configuration}-{filename}{database}{extension}.error'
                    .format(app=app, configuration=configuration,
                            filename=filename, database=db,
                            extension=file_extension.lower()).lower())
                if len(stderr) > 0:
                    with open(filename_log, 'w') as file:
                        file.write(stderr)
            time_scrip_end = default_timer()
            sep = filename.find("-")
            if sep > 0:
                subscript_type = filename[:sep].lower()
                times_script[subscript_type] = time_scrip_end - time_scrip_start
                logger.debug(
                    "#### script=" + str(subscript_type)
                    + " time=" + str(times_script[subscript_type]))
    # wait for all previous tenants to finish before writing final label
    num_tenants_ready = 0
    if num_tenants > 0:
        while True:
            fullcommand = 'get pod {pod_sut} -o jsonpath="{{.metadata.labels}}"'.format(
                pod_sut=pod_sut)
            labels_raw = kubectl(fullcommand, context)
            labels_pod = json.loads(labels_raw)
            logger.debug(f"#### Found labels {id_tenant}: {labels_pod}")
            if 'timeLoadingStart' in labels_pod:
                timeLoadingStart = int(labels_pod['timeLoadingStart'])
            if 'num_tenants_ready' in labels_pod:
                num_tenants_ready = int(labels_pod['num_tenants_ready'])
            logger.debug(
                f"num_tenants_ready, id_tenant: {num_tenants_ready}, {id_tenant}")
            if num_tenants_ready == id_tenant:
                break
            time.sleep(1)
    # compute and write final timing labels
    time_scriptgroup_end = default_timer()
    time_now = str(datetime.now())
    timeLoadingEnd = int(datetime.timestamp(
        datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S.%f')))
    timeLoading = timeLoadingEnd - timeLoadingStart + time_offset
    logger.debug("#### time_scriptgroup_end: " + str(time_scriptgroup_end))
    logger.debug("#### timeLoadingEnd: " + str(timeLoadingEnd))
    logger.debug("#### timeLoading after scrips: " + str(timeLoading))
    labels = dict()
    labels['num_tenants_ready'] = id_tenant + 1
    labels['time_{script_type}'.format(script_type=script_type)] = (
        timeLoadingEnd - timeLoadingStart)
    labels['timeLoadingEnd'] = timeLoadingEnd
    if (num_tenants > 0 and id_tenant == num_tenants - 1) or num_tenants == 0:
        logger.debug(f"#### Last tenant {id_tenant} marks loading as finished")
        labels[script_type] = 'True'
        labels['timeLoading'] = timeLoading
    for subscript_type, time_subscript_type in times_script.items():
        labels['time_{script_type}'.format(script_type=subscript_type)] = ceil(time_subscript_type)
    fullcommand = 'label pods {pod_sut} --overwrite '.format(pod_sut=pod_sut)
    for key, value in labels.items():
        fullcommand = fullcommand + " {key}={value}".format(key=key, value=value)
    kubectl(fullcommand, context)
    if len(volume) > 0:
        fullcommand = 'label pvc {volume} --overwrite '.format(volume=volume)
        for key, value in labels.items():
            fullcommand = fullcommand + " {key}={value}".format(key=key, value=value)
        kubectl(fullcommand, context)


class LoadingCoordinator:
    """Coordinates data loading into the SUT via in-cluster jobs and direct scripts.

    :param config: The parent configuration this coordinator belongs to.
    :type config: SutConfiguration
    """

    def __init__(self, config: SutConfiguration) -> None:
        """Initialise with a back-reference to the parent configuration.

        :param config: Parent :class:`SutConfiguration` instance.
        :type config: SutConfiguration
        """
        self._config = config

    def start_pod(
        self,
        app: str = '',
        component: str = 'loading',
        experiment: str = '',
        configuration: str = '',
        parallelism: int = 1,
        num_pods: int = 1,
    ) -> None:
        """Start a Kubernetes loading job (parallel data ingestion).

        :param app: App label.
        :param component: Component label (default ``'loading'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        :param parallelism: Number of parallel pods.
        :param num_pods: Total pods that must complete.
        """
        cfg = self._config
        if len(app) == 0:
            app = cfg.appname
        if len(configuration) == 0:
            configuration = cfg.configuration
        if len(experiment) == 0:
            experiment = cfg.code
        cfg.logger.debug("LoadingCoordinator.start_pod({})".format(configuration))
        redisQueue = '{}-{}-{}-{}'.format(app, component, cfg.configuration, cfg.code)
        for i in range(1, cfg.num_loading + 1):
            cfg.experiment.cluster.add_to_messagequeue(queue=redisQueue, data=i)
        if cfg.experiment_dict['loader']:
            loader_entry = cfg.experiment_dict['loader'][0]
            cfg._push_pod_configs(
                queue_key=redisQueue,
                num_pods=cfg.num_loading,
                parameters=loader_entry.get('parameters', {}),
                pod_parameters=loader_entry.get('pod_parameters', []),
            )
        redisQueue = '{}-{}-job-{}-{}'.format(app, 'generator-podcount', cfg.configuration, cfg.code)
        cfg.experiment.cluster.set_pod_counter(queue=redisQueue, value=num_pods)
        redisQueue = '{}-{}-job-{}-{}'.format(app, 'loader-podcount', cfg.configuration, cfg.code)
        cfg.experiment.cluster.set_pod_counter(queue=redisQueue, value=num_pods)
        job = cfg.manifest.create_manifest_loading(
            app=app, component='loading', experiment=experiment,
            configuration=configuration, parallelism=parallelism, num_pods=num_pods)
        cfg.logger.debug("Deploy " + job)
        cfg.experiment.cluster.create_object_from_file(job)

    def start_exec(self, delay: int = 0) -> bool:
        """Start data ingestion by running init scripts directly inside the SUT pod.

        :param delay: Seconds to wait after invoking scripts.
        :return: True if loading was initiated, False if SUT is not running.
        :rtype: bool
        """
        cfg = self._config
        app = cfg.appname
        component = 'sut'
        configuration = cfg.configuration
        cfg.logger.debug("LoadingCoordinator.start_exec({})".format(configuration))
        pods = cfg.experiment.cluster.get_pods(app, component, cfg.experiment.code, configuration)
        if len(pods) > 0:
            pod_sut = pods[0]
            status = cfg.experiment.cluster.get_pod_status(pod_sut)
            if status != "Running":
                return False
            cfg.logger.debug("check if {} is running".format(pod_sut))
            self.check()
            if not cfg.loading_started:
                self.load_data(scripts=cfg.initscript)
            if delay > 0:
                cfg.delay(delay)
            return True

    def get_list_of_pvc(self) -> list:
        """Return a flat list of all PVC names claimed by this configuration.

        :return: List of PVC name strings.
        :rtype: list[str]
        """
        cfg = self._config
        list_of_pvc = []
        if 'deployment' in cfg.deployment_infos:
            for _, deployment in cfg.deployment_infos['deployment'].items():
                if 'pvc' in deployment:
                    list_of_pvc.extend(deployment['pvc'])
        if 'statefulset' in cfg.deployment_infos:
            for _, statefulset in cfg.deployment_infos['statefulset'].items():
                if 'pvc' in statefulset:
                    list_of_pvc.extend(statefulset['pvc'])
        return list_of_pvc

    def get_volume_to_label(self) -> str:
        """Return the PVC name that should receive the storage timing labels.

        :return: PVC name string.
        :rtype: str
        """
        cfg = self._config
        if cfg.storage['storageConfiguration']:
            storageConfiguration = cfg.storage['storageConfiguration']
        else:
            storageConfiguration = cfg.configuration
        name_pvc = cfg.generate_component_name(
            app=cfg.appname, component='storage',
            experiment=cfg.storage_label, configuration=storageConfiguration)
        volume = name_pvc
        list_of_pvc = self.get_list_of_pvc()
        print("{:30s}: list of pvcs {}".format(cfg.configuration, list_of_pvc))
        if len(list_of_pvc) > 0:
            volume = list_of_pvc[0]
            print("{:30s}: will be labeling {}".format(cfg.configuration, volume))
        return volume

    def copyLog(self) -> None:
        """Copy the DBMS log file from the SUT pod to the result folder."""
        cfg = self._config
        print("copyLog")
        pods = cfg.experiment.cluster.get_pods(
            component='sut', configuration=cfg.configuration, experiment=cfg.code)
        cfg.pod_sut = pods[0]
        if len(cfg.dockertemplate['logfile']):
            cmd_prepare = 'mkdir /data/' + str(cfg.code)
            cfg.execute_command_in_pod_sut(command=cmd_prepare)
            cmd_save = ('cp ' + cfg.dockertemplate['logfile']
                        + ' /data/' + str(cfg.code) + '/' + cfg.configuration + '.log')
            cfg.execute_command_in_pod_sut(command=cmd_save)

    def prepare_init_dbms(self, scripts: list) -> None:
        """Copy and optionally fill DDL scripts into the SUT pod for loading.

        :param scripts: List of script filenames from the experiment's initscript list.
        """
        cfg = self._config
        cfg.logger.debug('LoadingCoordinator.prepare_init_dbms()')
        pods = cfg.experiment.cluster.get_pods(
            component='sut', configuration=cfg.configuration, experiment=cfg.code)
        cfg.pod_sut = pods[0]
        scriptfolder = '/tmp/'
        c = cfg.dockertemplate['template']
        database = c['JDBC']['database'] if 'JDBC' in c and 'database' in c['JDBC'] else cfg.experiment.volume
        schema = c['JDBC']['schema'] if 'JDBC' in c and 'schema' in c['JDBC'] else 'default'
        databases = [database]
        if cfg.num_tenants > 0 and cfg.tenant_per == 'schema':
            for tenant in range(cfg.num_tenants):
                print("{:30s}: scripts for tenant #{}".format(cfg.configuration, tenant))
                for script in scripts:
                    filename_template = cfg.path_experiment_docker + '/' + script
                    filename_source = (cfg.experiment.cluster.experiments_configfolder
                                       + '/' + filename_template)
                    filename_base, file_extension = os.path.splitext(script)
                    if os.path.isfile(filename_source):
                        with open(filename_source, "r") as initscript_template:
                            data = initscript_template.read()
                            data = data.format(BEXHOMA_SCHEMA=f"tenant_{tenant}")
                            filename_in_resultfolder = (
                                cfg.experiment.path
                                + '/{app}-loading-{configuration}-{tenant}-{filename}'
                                  '-{database}{extension}'.format(
                                    app=cfg.appname, configuration=cfg.configuration,
                                    filename=filename_base, database=database,
                                    tenant=tenant,
                                    extension=file_extension.lower()).lower())
                            filename_target = f'/{tenant}-{script}'
                            filename_in_container = scriptfolder + filename_target
                            with open(filename_in_resultfolder, "w") as initscript_filled:
                                initscript_filled.write(data)
                            cfg.experiment.cluster.upload_file(
                                filename_remote=filename_in_container,
                                filename_local=filename_in_resultfolder,
                                pod=cfg.pod_sut, container="dbms")
                            cfg.execute_command_in_pod_sut(
                                "sed -i 's/\\r$//' {to_name}".format(
                                    to_name=filename_in_container))
            return
        if cfg.num_tenants > 0 and cfg.tenant_per == 'database':
            script = 'initdatabases.sql'
            filename_base, file_extension = os.path.splitext(script)
            filename_in_resultfolder = (
                cfg.experiment.path
                + '/{app}-loading-{configuration}-{filename}-{database}{extension}'.format(
                    app=cfg.appname, configuration=cfg.configuration,
                    filename=filename_base, database=database,
                    extension=file_extension.lower()).lower())
            filename_in_container = scriptfolder + script
            script_create_database = ''
            for tenant in range(cfg.num_tenants):
                if cfg.volume_per_tenant:
                    script_create_database += (
                        f"CREATE TABLESPACE tenant_{tenant} LOCATION '/tenant_{tenant}';\n")
                    script_create_database += (
                        f"CREATE DATABASE tenant_{tenant} TABLESPACE tenant_{tenant};\n")
                else:
                    script_create_database += f'CREATE DATABASE tenant_{tenant};\n'
            with open(filename_in_resultfolder, "w") as initscript_filled:
                initscript_filled.write(script_create_database)
            cfg.experiment.cluster.upload_file(
                filename_remote=filename_in_container,
                filename_local=filename_in_resultfolder,
                pod=cfg.pod_sut, container="dbms")
            cfg.execute_command_in_pod_sut(
                "sed -i 's/\\r$//' {to_name}".format(to_name=filename_in_container))
        if len(cfg.ddl_parameters):
            for script in scripts:
                filename_template = cfg.path_experiment_docker + '/' + script
                if os.path.isfile(cfg.experiment.cluster.experiments_configfolder
                                  + '/' + filename_template):
                    with open(cfg.experiment.cluster.experiments_configfolder
                              + '/' + filename_template, "r") as initscript_template:
                        data = initscript_template.read()
                        data = data.format(**cfg.ddl_parameters)
                        filename_filled = cfg.path_experiment_docker + '/filled_' + script
                        with open(cfg.experiment.cluster.experiments_configfolder
                                  + '/' + filename_filled, "w") as initscript_filled:
                            initscript_filled.write(data)
                        filename_in_container = scriptfolder + script
                        filename_in_resultfolder = (
                            cfg.experiment.cluster.experiments_configfolder
                            + '/' + filename_filled)
                        cfg.experiment.cluster.upload_file(
                            filename_remote=filename_in_container,
                            filename_local=filename_in_resultfolder,
                            pod=cfg.pod_sut, container="dbms")
                        cfg.execute_command_in_pod_sut(
                            "sed -i 's/\\r$//' {to_name}".format(
                                to_name=filename_in_container))
                        filename_source = (cfg.experiment.cluster.experiments_configfolder
                                           + '/' + filename_filled)
                        filename_base, file_extension = os.path.splitext(script)
                        filename_in_resultfolder = (
                            cfg.experiment.path
                            + '/{app}-loading-{configuration}-{filename}-{database}{extension}'
                            .format(app=cfg.appname, configuration=cfg.configuration,
                                    filename=filename_base, database=database,
                                    extension=file_extension.lower()).lower())
                        shutil.copy(filename_source, filename_in_resultfolder)
        else:
            for script in scripts:
                filename = cfg.path_experiment_docker + '/' + script
                filename_source = (cfg.experiment.cluster.experiments_configfolder
                                   + '/' + filename)
                filename_in_container = scriptfolder + script
                filename_base, file_extension = os.path.splitext(script)
                filename_in_resultfolder = (
                    cfg.experiment.path
                    + '/{app}-loading-{configuration}-{filename}-{database}{extension}'.format(
                        app=cfg.appname, configuration=cfg.configuration,
                        filename=filename_base, database=database,
                        extension=file_extension.lower()).lower())
                if os.path.isfile(filename_source):
                    shutil.copy(filename_source, filename_in_resultfolder)
                    cfg.experiment.cluster.upload_file(
                        filename_remote=filename_in_container,
                        filename_local=filename_in_resultfolder,
                        pod=cfg.pod_sut, container="dbms")
                    cfg.execute_command_in_pod_sut(
                        "sed -i 's/\\r$//' {to_name}".format(
                            to_name=filename_in_container))

    def check(self) -> None:
        """Check loading status, update timing attributes, and clean up finished jobs.

        If a loading job has succeeded: reads timing labels from the SUT pod,
        deletes the job and its pods, triggers index loading if configured.
        Also reads pod labels to update ``loading_started`` / ``loading_finished``.
        """
        cfg = self._config
        if cfg.loading_deactivated:
            cfg.loading_started = True
            cfg.loading_finished = True
            cfg.loading_active = False
            cfg.monitor_loading = False
            return
        loading_pods_active = True
        if cfg.loading_active:
            app = cfg.experiment.cluster.appname
            component = 'loading'
            experiment = cfg.code
            configuration = cfg.configuration
            success = cfg.experiment.cluster.get_job_status(
                app=app, component=component,
                experiment=experiment, configuration=configuration)
            jobs = cfg.experiment.cluster.get_jobs(
                app, component, cfg.code, configuration)
            for job in jobs:
                cfg.experiment.cluster.logger.debug(
                    "Found running job {}".format(job))
                success = cfg.experiment.cluster.get_job_status(job)
                cfg.experiment.cluster.logger.debug(
                    'job {} has success status {}'.format(job, success))
                pods = cfg.experiment.cluster.get_job_pods(
                    app=app, component=component,
                    experiment=experiment, configuration=configuration)
                for pod in pods:
                    status = cfg.experiment.cluster.get_pod_status(pod)
                    cfg.experiment.cluster.logger.debug(
                        "Pod {} has status {}".format(pod, status))
                    if status == "Succeeded":
                        containers = cfg.experiment.cluster.get_pod_containers(pod)
                        for container in containers:
                            if len(container) > 0:
                                if not cfg.experiment.cluster.pod_log_exists(
                                        pod_name=pod, container=container):
                                    cfg.experiment.cluster.logger.debug(
                                        "Store logs of job {} pod {} container {}".format(
                                            job, pod, container))
                                    cfg.experiment.cluster.store_pod_log(
                                        pod_name=pod, container=container)
                        if not cfg.experiment.cluster.pod_description_exists(pod_name=pod):
                            cfg.experiment.cluster.logger.debug(
                                "Store description of job {} pod {}".format(job, pod))
                            cfg.experiment.cluster.store_pod_description(pod_name=pod)
                if success:
                    cfg.experiment.cluster.logger.debug(
                        'job {} will be suspended and parallel loading will be considered finished'
                        .format(job, success))
                    pod_labels = cfg.experiment.cluster.get_pods_labels(
                        app=app, component='sut',
                        experiment=experiment, configuration=configuration)
                    if len(pod_labels) > 0:
                        pod = next(iter(pod_labels.keys()))
                        if 'timeLoadingStart' in pod_labels[pod]:
                            cfg.timeLoadingStart = int(pod_labels[pod]['timeLoadingStart'])
                        if 'timeLoadingEnd' in pod_labels[pod]:
                            cfg.timeLoadingEnd = int(pod_labels[pod]['timeLoadingEnd'])
                        if 'timeLoading' in pod_labels[pod]:
                            cfg.timeLoading = float(pod_labels[pod]['timeLoading'])
                        if 'timeIndex' in pod_labels[pod]:
                            cfg.timeIndex = float(pod_labels[pod]['timeIndex'])
                        for key, value in pod_labels[pod].items():
                            if key.startswith("time_"):
                                time_type = key[len("time_"):]
                                cfg.times_scripts[time_type] = float(value)
                    for pod in pods:
                        status = cfg.experiment.cluster.get_pod_status(pod)
                        cfg.experiment.cluster.logger.debug(
                            "Pod {} has status {}".format(pod, status))
                        cfg.experiment.cluster.logger.debug(
                            "Store logs of job {} pod {}".format(job, pod))
                        containers = cfg.experiment.cluster.get_pod_containers(pod)
                        for container in containers:
                            if len(container) > 0:
                                cfg.experiment.cluster.store_pod_log(
                                    pod_name=pod, container=container)
                        if not cfg.experiment.cluster.pod_description_exists(pod_name=pod):
                            cfg.experiment.cluster.logger.debug(
                                "Store description of job {} pod {}".format(job, pod))
                            cfg.experiment.cluster.store_pod_description(pod_name=pod)
                        cfg.experiment.cluster.delete_pod(pod)
                    cfg.experiment.end_loading(job)
                    cfg.experiment.cluster.delete_job(job)
                    loading_pods_active = False
                    pods_sut = cfg.experiment.cluster.get_pods(
                        app=app, component='sut',
                        experiment=experiment, configuration=configuration)
                    if len(pods_sut) > 0:
                        pod_sut = pods_sut[0]
                        print("{:30s}: showing loader times".format(cfg.configuration))
                        timing_datagenerator, timing_sensor, timing_total = (
                            cfg.experiment.get_job_timing_loading(job))
                        print("{:30s}: generator times (start/end per pod and container) {}".format(
                            cfg.configuration, timing_datagenerator))
                        print("{:30s}: loader times (start/end per pod and container) {}".format(
                            cfg.configuration, timing_sensor))
                        print("{:30s}: total times (start/end per pod and container) {}".format(
                            cfg.configuration, timing_total))
                        generator_time = 0
                        loader_time = 0
                        total_time = 0
                        cfg.loading_timespans = {}
                        cfg.loading_timespans['datagenerator'] = timing_datagenerator
                        cfg.loading_timespans['sensor'] = timing_sensor
                        cfg.loading_timespans['total'] = timing_total
                        if len(timing_datagenerator) > 0:
                            cfg.experiment.cluster.logger.debug(
                                "Generator times (duration per pod [s]): {}".format(
                                    [end - start for (start, end) in timing_datagenerator]))
                            timing_start = min([start for (start, end) in timing_datagenerator])
                            timing_end = max([end for (start, end) in timing_datagenerator])
                            total_time = timing_end - timing_start
                            generator_time = total_time
                            print("{:30s}: generator timespan (first to last [s]) = {}".format(
                                cfg.configuration, total_time))
                        if len(timing_sensor) > 0:
                            cfg.experiment.cluster.logger.debug(
                                "Loader times (duration per pod [s]): {}".format(
                                    [end - start for (start, end) in timing_sensor]))
                            timing_start = min([start for (start, end) in timing_sensor])
                            timing_end = max([end for (start, end) in timing_sensor])
                            total_time = timing_end - timing_start
                            loader_time = total_time
                            print("{:30s}: loader timespan (first to last [s]) = {}".format(
                                cfg.configuration, total_time))
                        if len(timing_datagenerator) > 0 and len(timing_sensor) > 0:
                            timing_total = timing_datagenerator + timing_sensor
                            cfg.experiment.cluster.logger.debug(
                                "Total times (start/end per pod and container): {}".format(
                                    timing_total))
                            timing_start = min([start for (start, end) in timing_total])
                            timing_end = max([end for (start, end) in timing_total])
                            total_time = timing_end - timing_start
                            print("{:30s}: total timespan (first to last [s]) = {}".format(
                                cfg.configuration, total_time))
                        time_now = str(datetime.now())
                        time_now_int = int(datetime.timestamp(
                            datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S.%f')))
                        cfg.timeLoadingEnd = int(time_now_int)
                        cfg.timeSchema = cfg.timeLoading
                        if total_time > 0:
                            cfg.timeLoading = ceil(total_time + cfg.timeLoading)
                        else:
                            cfg.timeLoading = ceil(
                                int(cfg.timeLoadingEnd) - int(cfg.timeLoadingStart)
                                + cfg.timeLoading)
                        cfg.timeGenerating = generator_time
                        cfg.timeIngesting = loader_time
                        cfg.experiment.cluster.logger.debug("LOADING LABELS")
                        cfg.experiment.cluster.logger.debug(cfg.timeLoadingStart)
                        cfg.experiment.cluster.logger.debug(cfg.timeLoadingEnd)
                        cfg.experiment.cluster.logger.debug(cfg.timeLoading)
                        fullcommand = (
                            'label pods ' + pod_sut
                            + ' --overwrite loaded=True timeLoadingEnd="{}" timeLoadingStart="{}"'
                              ' time_ingested={} timeLoading={} time_generated={}'.format(
                                cfg.timeLoadingEnd, cfg.timeLoadingStart,
                                loader_time, cfg.timeLoading, generator_time))
                        cfg.experiment.cluster.kubectl(fullcommand)
                        use_storage = cfg.use_storage()
                        use_ramdisk = cfg.use_ramdisk()
                        if use_storage and not use_ramdisk:
                            volume = self.get_volume_to_label()
                            if volume:
                                fullcommand = (
                                    'label pvc ' + volume
                                    + ' --overwrite loaded=True timeLoadingEnd="{}"'
                                      ' timeLoadingStart="{}" time_ingested={}'
                                      ' timeLoading={} time_generated={}'.format(
                                        cfg.timeLoadingEnd, cfg.timeLoadingStart,
                                        loader_time, cfg.timeLoading, generator_time))
                                cfg.experiment.cluster.kubectl(fullcommand)
                    if len(cfg.indexscript):
                        if cfg.tenant_per == 'container' and not cfg.loading_finished:
                            cfg.tenant_ready_to_index = True
                        else:
                            self.load_data(
                                scripts=cfg.indexscript,
                                time_offset=cfg.timeLoading,
                                time_start_int=cfg.timeLoadingStart,
                                script_type='indexed')
        else:
            loading_pods_active = False
        pod_labels = cfg.experiment.cluster.get_pods_labels(
            app=cfg.appname, component='sut',
            experiment=cfg.experiment.code, configuration=cfg.configuration)
        if len(pod_labels) > 0:
            pod = next(iter(pod_labels.keys()))
            if len(cfg.indexscript):
                if 'indexed' in pod_labels[pod]:
                    cfg.loading_started = True
                    cfg.loading_finished = (pod_labels[pod]['indexed'] == 'True')
                else:
                    cfg.loading_finished = False
                if 'time_indexed' in pod_labels[pod]:
                    cfg.timeIndex = float(pod_labels[pod]['time_indexed'])
            else:
                if not loading_pods_active:
                    if 'loaded' in pod_labels[pod]:
                        cfg.loading_started = True
                        cfg.loading_finished = (pod_labels[pod]['loaded'] == 'True')
                    else:
                        cfg.loading_started = False
            if 'timeLoadingStart' in pod_labels[pod]:
                cfg.timeLoadingStart = int(pod_labels[pod]['timeLoadingStart'])
            if 'timeLoadingEnd' in pod_labels[pod]:
                cfg.timeLoadingEnd = int(pod_labels[pod]['timeLoadingEnd'])
            if 'timeLoading' in pod_labels[pod]:
                cfg.timeLoading = float(pod_labels[pod]['timeLoading'])
            if 'time_loaded' in pod_labels[pod]:
                cfg.timeSchema = float(pod_labels[pod]['time_loaded'])
            if 'time_generated' in pod_labels[pod]:
                cfg.timeGenerating = float(pod_labels[pod]['time_generated'])
            if 'time_ingested' in pod_labels[pod]:
                cfg.timeIngesting = float(pod_labels[pod]['time_ingested'])
            for key, value in pod_labels[pod].items():
                if key.startswith("time_"):
                    time_type = key[len("time_"):]
                    cfg.times_scripts[time_type] = float(value)

    def load_data(
        self,
        scripts: list,
        time_offset: int = 0,
        time_start_int: int = 0,
        script_type: str = 'loaded',
    ) -> None:
        """Start async loading of SQL/shell scripts into the SUT.

        Calls :func:`load_data_asynch` in threads — one per tenant for
        schema/database tenancy, one thread otherwise.

        :param scripts: List of script filenames to execute.
        :param time_offset: Previously elapsed seconds added to the total duration.
        :param time_start_int: Unix timestamp when loading started (0 = compute now).
        :param script_type: Label key written to pod/PVC on completion.
        """
        cfg = self._config
        cfg.logger.debug('LoadingCoordinator.load_data()')
        cfg.loading_started = True
        self.prepare_init_dbms(scripts)
        service_name = cfg.get_service_sut(configuration=cfg.configuration)
        pods = cfg.experiment.cluster.get_pods(
            component='sut', configuration=cfg.configuration, experiment=cfg.code)
        cfg.pod_sut = pods[0]
        print("{:30s}: connect to pod {} to load scripts".format(cfg.configuration, cfg.pod_sut))
        scriptfolder = '/tmp/'
        commands = scripts.copy()
        c = cfg.dockertemplate['template']
        database = (c['JDBC']['database'] if 'JDBC' in c and 'database' in c['JDBC']
                    else cfg.experiment.volume)
        databases = [database]
        use_storage = cfg.use_storage()
        use_ramdisk = cfg.use_ramdisk()
        if use_storage and not use_ramdisk:
            volume = self.get_volume_to_label()
        else:
            volume = ''
        print("{:30s}: start asynch loading scripts of type {}".format(
            cfg.configuration, script_type))
        if 'loadData' not in cfg.dockertemplate:
            print("{:30s}: no load command found in config".format(cfg.configuration))
            return
        if cfg.num_tenants > 0:
            if cfg.tenant_per == 'schema':
                for tenant in range(cfg.num_tenants):
                    commands_tenants = [f'{tenant}-{c}' for c in commands]
                    thread_args = {
                        'app': cfg.appname, 'component': 'sut',
                        'experiment': cfg.code, 'configuration': cfg.configuration,
                        'pod_sut': cfg.pod_sut, 'scriptfolder': scriptfolder,
                        'commands': commands_tenants,
                        'loadData': cfg.dockertemplate['loadData'],
                        'path': cfg.experiment.path, 'volume': volume,
                        'context': cfg.experiment.cluster.context,
                        'service_name': service_name,
                        'time_offset': time_offset, 'script_type': script_type,
                        'time_start_int': time_start_int,
                        'namespace': cfg.experiment.cluster.namespace,
                        'num_tenants': cfg.num_tenants, 'id_tenant': tenant,
                        'database': databases,
                    }
                    cfg.logger.debug(
                        "load_data_asynch - run schema-wise scripts {}".format(thread_args))
                    thread = threading.Thread(target=load_data_asynch, kwargs=thread_args)
                    thread.start()
                    time.sleep(1)
            elif cfg.tenant_per == 'database':
                if script_type == 'loaded':
                    thread_args = {
                        'app': cfg.appname, 'component': 'sut',
                        'experiment': cfg.code, 'configuration': cfg.configuration,
                        'pod_sut': cfg.pod_sut, 'scriptfolder': scriptfolder,
                        'commands': ["initdatabases.sql"],
                        'loadData': cfg.dockertemplate['loadData'],
                        'path': cfg.experiment.path, 'volume': volume,
                        'context': cfg.experiment.cluster.context,
                        'service_name': service_name,
                        'time_offset': time_offset, 'script_type': "tenants",
                        'time_start_int': time_start_int,
                        'namespace': cfg.experiment.cluster.namespace,
                        'num_tenants': 0, 'id_tenant': 0, 'database': databases,
                    }
                    cfg.logger.debug(
                        "load_data_asynch - run create database scripts {}".format(thread_args))
                    load_data_asynch(**thread_args)
                for tenant in range(cfg.num_tenants):
                    tenant_databases = [f'tenant_{tenant}']
                    thread_args = {
                        'app': cfg.appname, 'component': 'sut',
                        'experiment': cfg.code, 'configuration': cfg.configuration,
                        'pod_sut': cfg.pod_sut, 'scriptfolder': scriptfolder,
                        'commands': commands,
                        'loadData': cfg.dockertemplate['loadData'],
                        'path': cfg.experiment.path, 'volume': volume,
                        'context': cfg.experiment.cluster.context,
                        'service_name': service_name,
                        'time_offset': time_offset, 'script_type': script_type,
                        'time_start_int': time_start_int,
                        'namespace': cfg.experiment.cluster.namespace,
                        'num_tenants': cfg.num_tenants, 'id_tenant': tenant,
                        'database': tenant_databases,
                    }
                    cfg.logger.debug(
                        "load_data_asynch - run database-wise scripts {}".format(thread_args))
                    thread = threading.Thread(target=load_data_asynch, kwargs=thread_args)
                    thread.start()
                    time.sleep(1)
            elif cfg.tenant_per == 'container':
                thread_args = {
                    'app': cfg.appname, 'component': 'sut',
                    'experiment': cfg.code, 'configuration': cfg.configuration,
                    'pod_sut': cfg.pod_sut, 'scriptfolder': scriptfolder,
                    'commands': commands,
                    'loadData': cfg.dockertemplate['loadData'],
                    'path': cfg.experiment.path, 'volume': volume,
                    'context': cfg.experiment.cluster.context,
                    'service_name': service_name,
                    'time_offset': time_offset, 'script_type': script_type,
                    'time_start_int': time_start_int,
                    'namespace': cfg.experiment.cluster.namespace,
                    'num_tenants': 0, 'id_tenant': 0, 'database': databases,
                }
                cfg.logger.debug(
                    "load_data_asynch - run container-wise scripts {}".format(thread_args))
                thread = threading.Thread(target=load_data_asynch, kwargs=thread_args)
                thread.start()
            print("{:30s}: runs scripts {}".format(cfg.configuration, commands))
        else:
            thread_args = {
                'app': cfg.appname, 'component': 'sut',
                'experiment': cfg.code, 'configuration': cfg.configuration,
                'pod_sut': cfg.pod_sut, 'scriptfolder': scriptfolder,
                'commands': commands,
                'loadData': cfg.dockertemplate['loadData'],
                'path': cfg.experiment.path, 'volume': volume,
                'context': cfg.experiment.cluster.context,
                'service_name': service_name,
                'time_offset': time_offset, 'script_type': script_type,
                'time_start_int': time_start_int,
                'namespace': cfg.experiment.cluster.namespace,
                'num_tenants': 0, 'id_tenant': 0, 'database': databases,
            }
            cfg.logger.debug("load_data_asynch - run scripts {}".format(thread_args))
            thread = threading.Thread(target=load_data_asynch, kwargs=thread_args)
            thread.start()
            return
