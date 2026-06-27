"""SUT and auxiliary component lifecycle management for bexhoma configurations."""
from __future__ import annotations

import copy
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from .base import SutConfiguration

__all__ = ['LifecycleManager']


class LifecycleManager:
    """Manages SUT, monitoring, maintaining, loading start/stop and port forwarding.

    :param config: The parent configuration this manager belongs to.
    :type config: SutConfiguration
    """

    def __init__(self, config: SutConfiguration) -> None:
        """Initialise with a back-reference to the parent configuration.

        :param config: Parent :class:`SutConfiguration` instance.
        :type config: SutConfiguration
        """
        self._config = config

    def start_maintaining(
        self,
        app: str = '',
        component: str = 'maintaining',
        experiment: str = '',
        configuration: str = '',
        parallelism: int = 1,
        num_pods: int = 1,
    ) -> None:
        """Start a maintaining job.

        :param app: App label.
        :param component: Component label (default ``'maintaining'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        :param parallelism: Number of parallel pods in the job.
        :param num_pods: Total pods that must complete.
        """
        cfg = self._config
        if len(app) == 0:
            app = cfg.appname
        if len(configuration) == 0:
            configuration = cfg.configuration
        if len(experiment) == 0:
            experiment = cfg.code
        job = cfg.manifest.create_manifest_maintaining(
            app=app, component='maintaining', experiment=experiment,
            configuration=configuration, parallelism=parallelism, num_pods=num_pods)
        cfg.logger.debug("Deploy " + job)
        cfg.experiment.cluster.create_object_from_file(job)

    def create_monitoring(
        self,
        app: str = '',
        component: str = 'monitoring',
        experiment: str = '',
        configuration: str = '',
    ) -> str:
        """Generate the monitoring component name.

        :param app: App label.
        :param component: Component label (default ``'monitoring'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        :return: Generated component name string.
        :rtype: str
        """
        cfg = self._config
        name = cfg.generate_component_name(
            app=app, component=component,
            experiment=experiment, configuration=configuration)
        cfg.logger.debug("LifecycleManager.create_monitoring({})".format(name))
        return name

    def get_deployment_component(self, container: str) -> str:
        """Find the first deployment/statefulset that contains a container with the given name.

        :param container: Container name to search for.
        :return: Component name that owns the container, or empty string if not found.
        :rtype: str
        """
        cfg = self._config
        for name, deployment in cfg.deployment_infos['deployment'].items():
            if 'containers' in deployment and container in deployment['containers']:
                return name
        for name, statefulset in cfg.deployment_infos['statefulset'].items():
            if 'containers' in statefulset and container in statefulset['containers']:
                return name
        return ""

    def start_monitoring(
        self,
        app: str = '',
        component: str = 'monitoring',
        experiment: str = '',
        configuration: str = '',
    ) -> None:
        """Start a Prometheus monitoring deployment for this configuration.

        :param app: App label.
        :param component: Component label (default ``'monitoring'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        """
        cfg = self._config
        if not cfg.experiment.monitoring_active or (
                cfg.experiment.cluster.monitor_cluster_active
                and cfg.experiment.cluster.monitor_cluster_exists
                and not cfg.monitor_app_active):
            return
        if len(app) == 0:
            app = cfg.appname
        if len(configuration) == 0:
            configuration = cfg.configuration
        if len(experiment) == 0:
            experiment = cfg.code
        deployment_template = 'deploymenttemplate-bexhoma-prometheus.yml'
        name = self.create_monitoring(app, component, experiment, configuration)
        name_sut = self.create_monitoring(app, 'sut', experiment, configuration)
        name_pool = self.create_monitoring(app, 'pool', experiment, configuration)
        if 'monitor' in cfg.dockertemplate and 'component' in cfg.dockertemplate['monitor']:
            name_monitor_application_component = cfg.dockertemplate['monitor']['component']
        else:
            name_monitor_application_component = 'sut'
        name_monitor_application = self.create_monitoring(
            app, name_monitor_application_component, experiment, configuration)
        name_service = cfg.generate_component_name(
            app=app, component='sut',
            experiment=cfg.get_experiment_name(), configuration=configuration)
        name_worker = cfg.get_worker_name()
        name_service_headless = name_worker
        if cfg.experiment.cluster.monitor_cluster_active:
            print("{:30s}: wants to monitor all components in cluster".format(configuration))
        if not cfg.experiment.cluster.monitor_cluster_exists:
            print("{:30s}: cannot rely on preinstalled monitoring".format(configuration))
        print("{:30s}: starts monitoring with prometheus pod".format(configuration))
        deployment_experiment = cfg.experiment.path + '/{name}.yml'.format(name=name)
        with open(cfg.experiment.cluster.yamlfolder + deployment_template) as stream:
            try:
                result = yaml.safe_load_all(stream)
                result = [data for data in result]
                for dep in result:
                    if dep['kind'] == 'Service':
                        dep['metadata']['name'] = name
                        dep['metadata']['labels']['app'] = app
                        dep['metadata']['labels']['component'] = component
                        dep['metadata']['labels']['configuration'] = configuration
                        dep['metadata']['labels']['dbms'] = cfg.docker
                        dep['metadata']['labels']['experiment'] = experiment
                        dep['metadata']['labels']['volume'] = cfg.volume
                        dep['spec']['selector'] = dep['metadata']['labels'].copy()
                    if dep['kind'] == 'Deployment':
                        dep['metadata']['name'] = name
                        dep['metadata']['labels']['app'] = app
                        dep['metadata']['labels']['component'] = component
                        dep['metadata']['labels']['configuration'] = configuration
                        dep['metadata']['labels']['dbms'] = cfg.docker
                        dep['metadata']['labels']['experiment'] = str(experiment)
                        dep['metadata']['labels']['volume'] = cfg.volume
                        dep['spec']['template']['metadata']['labels'] = dep['metadata']['labels'].copy()
                        dep['spec']['selector']['matchLabels'] = dep['metadata']['labels'].copy()
                        envs = dep['spec']['template']['spec']['containers'][0]['env']
                        prometheus_config = """global:
  scrape_interval: 15s

scrape_configs:
  - job_name: '{master}'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_timeout}
    static_configs:
      - targets: ['{master}:9300']
  - job_name: 'monitor-gpu'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_timeout}
    static_configs:
      - targets: ['{master}:9400']""".format(
                            master=name_sut,
                            prometheus_interval=cfg.prometheus_interval,
                            prometheus_timeout=cfg.prometheus_timeout)
                        if cfg.monitor_app_active:
                            if 'monitor' in cfg.dockertemplate:
                                for monitor_component, application_monitoring in cfg.dockertemplate['monitor'].items():
                                    print("{:30s}: need application monitoring for {}".format(
                                        configuration, monitor_component))
                                    if ('discovery' in application_monitoring
                                            and application_monitoring['discovery']
                                            and 'discovery_config' in application_monitoring
                                            and len(application_monitoring['discovery_config']) > 0):
                                        prometheus_config += application_monitoring[
                                            'discovery_config'].format(
                                            namespace=cfg.experiment.namespace,
                                            master=name_sut,
                                            prometheus_interval=cfg.prometheus_interval,
                                            prometheus_timeout=cfg.prometheus_timeout)
                                    elif ('blackbox' in application_monitoring
                                          and application_monitoring['blackbox']):
                                        app_monitor_targets = (
                                            "\n          - postgres@localhost:5432/postgres?sslmode=disable\n")
                                        if cfg.tenant_per == 'database' and cfg.num_tenants > 0:
                                            connections = [
                                                f"          - postgres@localhost:5432/tenant_{i}?sslmode=disable"
                                                for i in range(cfg.num_tenants)
                                            ]
                                            app_monitor_targets += "\n".join(connections)
                                        prometheus_config += """
  - job_name: 'monitor-app'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_timeout}
    metrics_path: /probe
    static_configs:
      - targets: {app_monitor_targets}
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        regex: .*@([^:/]+:\\d+)/.*
        replacement: ${{1}}
        target_label: instance
      - target_label: __address__
        replacement: {master}:9500""".format(
                                            master=name_monitor_application,
                                            prometheus_interval=cfg.prometheus_interval,
                                            prometheus_timeout=cfg.prometheus_timeout,
                                            app_monitor_targets=app_monitor_targets)
                                    elif ('headless' in application_monitoring
                                          and application_monitoring['headless']):
                                        endpoints_cluster = []
                                        endpoints_worker = cfg.get_worker_endpoints()
                                        worker_idx = 0
                                        for endpoint in endpoints_worker:
                                            if endpoint in endpoints_cluster:
                                                print("{:30s}: found worker endpoint (cAdvisor) for application monitoring {} (already monitored by cluster)".format(
                                                    configuration, endpoint))
                                                continue
                                            print("{:30s}: found worker endpoint (cAdvisor) for application monitoring {} (added to Prometheus) of sidecar container".format(
                                                configuration, endpoint))
                                            prometheus_config += """
  - job_name: 'monitor-app-{endpoint}'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_timeout}
    metrics_path: /_status/vars
    static_configs:
      - targets: ['{endpoint}:8080']""".format(
                                                endpoint=endpoint,
                                                client=worker_idx,
                                                prometheus_interval=cfg.prometheus_interval,
                                                prometheus_timeout=cfg.prometheus_timeout)
                                            worker_idx += 1
                                    else:
                                        prometheus_config += """
  - job_name: 'monitor-app'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_timeout}
    static_configs:
      - targets:
          - {master}:9500
        labels:
          app: mysql-app""".format(
                                            master=name_sut,
                                            prometheus_interval=cfg.prometheus_interval,
                                            prometheus_timeout=cfg.prometheus_timeout)
                        endpoints_cluster = cfg.experiment.cluster.get_service_endpoints(
                            service_name="bexhoma-service-monitoring-default")
                        ep_idx = 0
                        for endpoint in endpoints_cluster:
                            print("{:30s}: found monitoring endpoint (cAdvisor) for monitoring {} (added to Prometheus) of daemonset".format(
                                configuration, endpoint))
                            prometheus_config += """
  - job_name: 'monitor-gpu-{endpoint}'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_timeout}
    static_configs:
      - targets: ['{endpoint}:9300']""".format(
                                endpoint=endpoint,
                                client=ep_idx,
                                prometheus_interval=cfg.prometheus_interval,
                                prometheus_timeout=cfg.prometheus_timeout)
                            ep_idx += 1
                        if len(endpoints_cluster) == 0:
                            endpoints_worker = cfg.get_worker_endpoints()
                            worker_ep_idx = 0
                            for endpoint in endpoints_worker:
                                if endpoint in endpoints_cluster:
                                    print("{:30s}: found worker endpoint (cAdvisor) for monitoring GPUs of {} (already monitored by cluster)".format(
                                        configuration, endpoint))
                                    continue
                                print("{:30s}: found worker endpoint (cAdvisor) for monitoring GPUs of {} (added to Prometheus) of sidecar container".format(
                                    configuration, endpoint))
                                prometheus_config += """
  - job_name: 'monitor-gpu-{endpoint}'
    scrape_interval: {prometheus_interval}
    scrape_timeout: {prometheus_timeout}
    static_configs:
      - targets: ['{endpoint}:9300']""".format(
                                    endpoint=endpoint,
                                    client=worker_ep_idx,
                                    prometheus_interval=cfg.prometheus_interval,
                                    prometheus_timeout=cfg.prometheus_timeout)
                                worker_ep_idx += 1
                        for env_idx, env_item in enumerate(envs):
                            if env_item['name'] == 'BEXHOMA_SERVICE':
                                dep['spec']['template']['spec']['containers'][0]['env'][env_idx]['value'] = name_sut
                            if env_item['name'] == 'DBMSBENCHMARKER_CONFIGURATION':
                                dep['spec']['template']['spec']['containers'][0]['env'][env_idx]['value'] = configuration
                            if env_item['name'] == 'BEXHOMA_WORKERS':
                                dep['spec']['template']['spec']['containers'][0]['env'][env_idx]['value'] = prometheus_config
                            cfg.logger.debug('LifecycleManager.start_monitoring({})'.format(str(env_item)))
                        if 'monitoring' in cfg.nodes:
                            if 'nodeSelector' not in dep['spec']['template']['spec']:
                                dep['spec']['template']['spec']['nodeSelector'] = dict()
                            if dep['spec']['template']['spec']['nodeSelector'] is None:
                                dep['spec']['template']['spec']['nodeSelector'] = dict()
                            dep['spec']['template']['spec']['nodeSelector']['type'] = cfg.nodes['monitoring']
            except yaml.YAMLError as exc:
                print(exc)
        with open(deployment_experiment, "w+") as stream:
            try:
                stream.write(yaml.dump_all(result))
            except yaml.YAMLError as exc:
                print(exc)
        cfg.logger.debug("Deploy " + deployment_template)
        cfg.experiment.cluster.create_object_from_file(deployment_experiment)

    def stop_monitoring(
        self,
        app: str = '',
        component: str = 'monitoring',
        experiment: str = '',
        configuration: str = '',
    ) -> None:
        """Stop a monitoring deployment and remove its service.

        :param app: App label.
        :param component: Component label (default ``'monitoring'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        """
        cfg = self._config
        if len(app) == 0:
            app = cfg.appname
        if len(configuration) == 0:
            configuration = cfg.configuration
        if len(experiment) == 0:
            experiment = cfg.code
        deployments = cfg.experiment.cluster.get_deployments(
            app=app, component=component, experiment=experiment, configuration=configuration)
        for deployment in deployments:
            cfg.experiment.cluster.delete_deployment(deployment)
        services = cfg.experiment.cluster.get_services(
            app=app, component=component, experiment=experiment, configuration=configuration)
        for service in services:
            cfg.experiment.cluster.delete_service(service)

    def stop_maintaining(
        self,
        app: str = '',
        component: str = 'maintaining',
        experiment: str = '',
        configuration: str = '',
    ) -> None:
        """Stop a maintaining job and remove all its pods.

        :param app: App label.
        :param component: Component label (default ``'maintaining'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        """
        cfg = self._config
        if len(app) == 0:
            app = cfg.appname
        if len(configuration) == 0:
            configuration = cfg.configuration
        if len(experiment) == 0:
            experiment = cfg.code
        jobs = cfg.experiment.cluster.get_jobs(app, component, experiment, configuration)
        for job in jobs:
            success = cfg.experiment.cluster.get_job_status(job)
            print(job, success)
            cfg.experiment.cluster.delete_job(job)
        pods = cfg.experiment.cluster.get_job_pods(app, component, experiment, configuration)
        for pod in pods:
            status = cfg.experiment.cluster.get_pod_status(pod)
            print(pod, status)
            containers = cfg.experiment.cluster.get_pod_containers(pod)
            for container in containers:
                stdout = cfg.experiment.cluster.pod_log(pod=pod, container=container)
                filename_log = cfg.path + '/' + pod + '.' + container + '.log'
                with open(filename_log, "w") as log_file:
                    log_file.write(stdout)
            cfg.experiment.cluster.delete_pod(pod)

    def stop_loading(
        self,
        app: str = '',
        component: str = 'loading',
        experiment: str = '',
        configuration: str = '',
    ) -> None:
        """Stop a loading job and remove all its pods.

        :param app: App label.
        :param component: Component label (default ``'loading'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        """
        cfg = self._config
        if len(app) == 0:
            app = cfg.appname
        if len(configuration) == 0:
            configuration = cfg.configuration
        if len(experiment) == 0:
            experiment = cfg.code
        jobs = cfg.experiment.cluster.get_jobs(app, component, experiment, configuration)
        for job in jobs:
            success = cfg.experiment.cluster.get_job_status(job)
            print(job, success)
            cfg.experiment.cluster.delete_job(job)
        pods = cfg.experiment.cluster.get_job_pods(app, component, experiment, configuration)
        for pod in pods:
            status = cfg.experiment.cluster.get_pod_status(pod)
            print(pod, status)
            cfg.experiment.cluster.delete_pod(pod)

    def generate_port_forward(self) -> str:
        """Generate a kubectl port-forward command string for this SUT.

        :return: Ready-to-run ``kubectl port-forward`` command.
        :rtype: str
        """
        cfg = self._config
        context = cfg.experiment.cluster.context
        app = cfg.appname
        component = 'sut'
        experiment = cfg.get_experiment_name()
        configuration = cfg.configuration
        name = cfg.generate_component_name(
            app=app, component=component,
            experiment=experiment, configuration=configuration)
        ports = cfg.experiment.cluster.get_ports_of_service(
            app=app, component=component,
            experiment=experiment, configuration=configuration)
        forward = ['kubectl', '--context {context}'.format(context=context),
                   'port-forward', 'service/' + name]
        forward.extend(ports)
        return " ".join(forward)

    def start_sut(
        self,
        app: str = '',
        component: str = 'sut',
        experiment: str = '',
        configuration: str = '',
    ):
        """Start the system-under-test (DBMS).

        Controls optional worker and storage resources.  Resources are set
        according to the configuration's ``resources`` dict.

        :param app: App label.
        :param component: Component label (default ``'sut'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        :return: True if the SUT was started; False if it was already running.
        :rtype: bool or None
        """
        cfg = self._config
        use_storage = cfg.use_storage()
        use_data = cfg.use_distributed_datasource
        if len(app) == 0:
            app = cfg.appname
        if len(configuration) == 0:
            configuration = cfg.configuration
        if len(experiment) == 0:
            experiment = cfg.code
        if cfg.storage['storageConfiguration']:
            storageConfiguration = cfg.storage['storageConfiguration']
        else:
            storageConfiguration = configuration
        use_ramdisk = cfg.use_ramdisk()
        cfg.volume_per_tenant = cfg.experiment.multi_tenant_volume

        def extract_component_labels(file_path):
            deployments = []
            statefulsets = []
            pvcs = []
            with open(file_path, 'r') as yaml_file:
                docs = yaml.safe_load_all(yaml_file)
                for doc in docs:
                    if not isinstance(doc, dict):
                        continue
                    kind = doc.get('kind')
                    metadata = doc.get('metadata', {})
                    labels = metadata.get('labels', {})
                    label_component = labels.get('component')
                    if label_component:
                        if kind == 'Deployment':
                            deployments.append(label_component)
                        elif kind == 'StatefulSet':
                            statefulsets.append(label_component)
                        elif kind == 'PersistentVolumeClaim':
                            pvcs.append(label_component)
            return deployments, statefulsets, pvcs

        def set_component_labels(dep):
            dep['metadata']['labels']['app'] = app
            dep['metadata']['labels']['component'] = 'storage'
            dep['metadata']['labels']['configuration'] = storageConfiguration
            dep['metadata']['labels']['experiment'] = cfg.storage_label
            dep['metadata']['labels']['dbms'] = cfg.docker
            dep['metadata']['labels']['volume'] = cfg.volume
            for label_key, label_value in cfg.additional_labels.items():
                dep['metadata']['labels'][label_key] = str(label_value)
            return dep

        def should_we_remove_pvcs():
            return (not cfg.loading_finished
                    and cfg.experiment.args_dict['request_storage_remove']
                    and cfg.num_experiment_to_apply_done == 0)

        def reset_and_remove_pvc(pvc):
            if should_we_remove_pvcs:
                print("{:30s}: storage {} should be removed".format(configuration, pvc))
                cfg.experiment.cluster.delete_pvc(pvc)
                cfg.wait(10)
                pvcs_remaining = cfg.experiment.cluster.get_pvc(pvc=pvc)
                while len(pvcs_remaining) > 0:
                    print("{:30s}: storage {} still exists".format(configuration, pvc))
                    cfg.wait(10)
                    pvcs_remaining = cfg.experiment.cluster.get_pvc(pvc=pvc)
                print("{:30s}: storage {} is gone".format(configuration, pvc))

        def get_labels_from_loaded_pvc():
            if use_storage and not use_ramdisk and not should_we_remove_pvcs():
                list_of_pvc = cfg.get_list_of_pvc()
                print("{:30s}: list of pvcs {}".format(cfg.configuration, list_of_pvc))
                volume = list_of_pvc[0]
                pvcs_labels = cfg.experiment.cluster.get_pvc_labels(pvc=volume)
                cfg.logger.debug(pvcs_labels)
                if len(pvcs_labels) > 0:
                    print("{:30s}: storage {} exists".format(configuration, volume))
                    pvc_labels = pvcs_labels[0]
                    copy_labels = [
                        'loaded', 'timeLoading', 'timeLoadingStart', 'timeLoadingEnd',
                        'indexed', 'time_generated', 'time_indexed', 'time_ingested',
                        'time_initconstraints', 'time_initindexes', 'time_initschema',
                        'time_initstatistics', 'time_loaded',
                    ]
                    return {label: value for label, value in pvc_labels.items()
                            if label in copy_labels}
            return []

        def set_labels_from_loaded_pvc():
            if len(labels_on_existing_pvc) > 0:
                dep['spec']['template']['metadata']['labels']['storage_exists'] = "True"
                for label in labels_on_existing_pvc:
                    print("{:30s}: copied label {} = {}".format(
                        configuration, label, labels_on_existing_pvc[label]))
                    dep['spec']['template']['metadata']['labels'][label] = (
                        labels_on_existing_pvc[label])
                print("{:30s}: loading is set to finished".format(configuration))
                cfg.loading_active = False
                cfg.monitor_loading = False

        name = cfg.generate_component_name(
            app=app, component=component,
            experiment=cfg.get_experiment_name(), configuration=configuration)
        template = cfg.sut_template
        deployment_experiment = cfg.experiment.path + '/{name}.yml'.format(name=name)
        sut_manifest_file = cfg.experiment.cluster.yamlfolder + template
        deploys, ssets, pvcs = extract_component_labels(sut_manifest_file)
        print("{:30s}: deployments {}".format(configuration, deploys))
        print("{:30s}: stateful sets {}".format(configuration, ssets))
        print("{:30s}: pvcs {}".format(configuration, pvcs))
        if 'deployment' not in cfg.deployment_infos:
            cfg.deployment_infos['deployment'] = {}
        for deployment in deploys:
            cfg.deployment_infos['deployment'][deployment] = {}
            cfg.deployment_infos['deployment'][deployment]['name'] = cfg.generate_component_name(
                app=app, component=deployment,
                experiment=cfg.get_experiment_name(), configuration=configuration)
            cfg.deployment_infos['deployment'][deployment]['name_service'] = (
                cfg.generate_component_name(
                    app=app, component=deployment,
                    experiment=cfg.get_experiment_name(), configuration=configuration))
            cfg.deployment_infos['deployment'][deployment]['pods'] = []
            cfg.deployment_infos['deployment'][deployment]['containers'] = []
            if len(pvcs):
                if use_storage and not use_ramdisk:
                    cfg.deployment_infos['deployment'][deployment]['name_pvc'] = (
                        cfg.generate_component_name(
                            app=app, component='storage',
                            experiment=cfg.storage_label, configuration=storageConfiguration))
                    cfg.deployment_infos['deployment'][deployment]['pvc'] = [
                        cfg.generate_component_name(
                            app=app, component='storage',
                            experiment=cfg.storage_label, configuration=storageConfiguration)]
        if 'statefulset' not in cfg.deployment_infos:
            cfg.deployment_infos['statefulset'] = {}
        for stateful_set in ssets:
            cfg.deployment_infos['statefulset'][stateful_set] = {}
            worker_name = cfg.get_worker_name(component=stateful_set)
            cfg.deployment_infos['statefulset'][stateful_set]['name'] = worker_name
            cfg.deployment_infos['statefulset'][stateful_set]['name_service'] = (
                cfg.get_worker_name(component=stateful_set))
            cfg.deployment_infos['statefulset'][stateful_set]['pods'] = [
                f"{worker_name}-{i}" for i in range(cfg.num_worker)]
            cfg.deployment_infos['statefulset'][stateful_set]['containers'] = []
            if use_storage and not use_ramdisk:
                list_of_workers_pvcs = []
                for worker in range(cfg.num_worker):
                    worker_full_name = "bxw-{name_worker}-{worker_number}".format(
                        name_worker=worker_name, worker_number=worker)
                    list_of_workers_pvcs.append(worker_full_name)
                cfg.deployment_infos['statefulset'][stateful_set]['pvc'] = list_of_workers_pvcs
        cfg.logger.debug(cfg.deployment_infos)
        labels_on_existing_pvc = get_labels_from_loaded_pvc()
        if use_storage and not use_ramdisk:
            print("{:30s}: found labels on pvc = {}".format(
                configuration, labels_on_existing_pvc))
        cfg.service = name
        name_worker = cfg.get_worker_name(component='worker')
        name_service_headless = name_worker
        name_pvc = cfg.generate_component_name(
            app=app, component='storage',
            experiment=cfg.storage_label, configuration=storageConfiguration)
        name_pool = cfg.generate_component_name(
            app=app, component='pool',
            experiment=cfg.get_experiment_name(), configuration=configuration)
        name_store = cfg.get_worker_name(component='store')
        cfg.logger.debug('LifecycleManager.start_sut(name={})'.format(name))
        deployments = cfg.experiment.cluster.get_deployments(
            app=app, component=component,
            experiment=cfg.get_experiment_name(), configuration=configuration)
        if len(deployments) > 0:
            return False
        print("{:30s}: name of SUT pods = {}".format(configuration, name))
        print("{:30s}: name of SUT service = {}".format(configuration, name))
        if use_storage:
            if use_ramdisk:
                print("{:30s}: uses RAM disk".format(configuration))
            else:
                print("{:30s}: name of SUT PVC name = {}".format(configuration, name_pvc))
        if cfg.num_worker > 0:
            print("{:30s}: name of worker pods = {}".format(configuration, name_worker))
            print("{:30s}: name of worker service headless = {}".format(
                configuration, name_worker))
        env = cfg.sut_parameters
        store_args = cfg.dockertemplate['store_args'] if 'store_args' in cfg.dockertemplate else True
        worker_port = (":" + str(cfg.dockertemplate['worker_port'])
                       if 'worker_port' in cfg.dockertemplate else "")
        list_of_workers = []
        for worker in range(cfg.num_worker):
            worker_full_name = "{name_worker}-{worker_number}.{worker_service}{worker_port}".format(
                name_worker=name_worker, worker_number=worker,
                worker_service=name_service_headless, worker_port=worker_port)
            list_of_workers.append(worker_full_name)
        list_of_workers_as_string = ",".join(list_of_workers)
        env['BEXHOMA_WORKER_LIST'] = list_of_workers_as_string
        list_of_workers_as_string_space = " ".join(list_of_workers)
        env['BEXHOMA_WORKER_LIST_SPACE'] = list_of_workers_as_string_space
        env['BEXHOMA_WORKER_NAME'] = "{name_worker}".format(name_worker=name_worker)
        env['BEXHOMA_WORKER_SERVICE'] = "{worker_service}".format(
            worker_service=name_service_headless)
        env['BEXHOMA_SUT_NAME'] = name
        if cfg.num_worker > 0:
            worker_full_name = "{name_worker}-{worker_number}.{worker_service}".format(
                name_worker=name_worker, worker_number=0,
                worker_service=name_service_headless)
            env['BEXHOMA_WORKER_FIRST'] = worker_full_name
            env['STATEFULSET_NAME'] = name_worker
            env['BEXHOMA_STORE_NAME'] = "{name_store}".format(
                name_store=name_store, worker_service=name_store)
            env['BEXHOMA_STORE_SERVICE'] = "{worker_service}".format(
                name_store=name_store, worker_service=name_store)
            list_of_stores = []
            for worker in range(cfg.num_worker):
                store_full_name = "{name_store}-{worker_number}.{worker_service}{worker_port}".format(
                    name_store=name_store, worker_number=worker,
                    worker_service=name_store, worker_port=worker_port)
                list_of_stores.append(store_full_name)
            list_of_stores_as_string = ",".join(list_of_stores)
            if cfg.num_worker > 0:
                store_full_name = "{name_store}-{worker_number}.{worker_service}".format(
                    name_store=name_store, worker_number=0, worker_service=name_store)
                env['BEXHOMA_STORE_FIRST'] = store_full_name
            env['BEXHOMA_STORE_LIST'] = list_of_stores_as_string
            if cfg.docker == "TiDB":
                name_worker = cfg.get_worker_name(component='pd')
                name_service_headless = name_worker
                list_initial_cluster = []
                for worker in range(cfg.num_worker):
                    clusternode_full_name = (
                        "{name_worker}-{worker_number}=http://{name_worker}-{worker_number}"
                        ".{worker_service}:2380".format(
                            name_worker=name_worker, worker_number=worker,
                            worker_service=name_service_headless))
                    list_initial_cluster.append(clusternode_full_name)
                list_initial_cluster_as_string = ",".join(list_initial_cluster)
                env['BEXHOMA_INITIAL_CLUSTER'] = list_initial_cluster_as_string
        for statefulset_name, statefulset in cfg.deployment_infos['statefulset'].items():
            name_worker = statefulset['name']
            name_service_headless = name_worker
            list_of_workers = []
            for worker in range(cfg.num_worker):
                worker_full_name = "{name_worker}-{worker_number}.{worker_service}{worker_port}".format(
                    name_worker=name_worker, worker_number=worker,
                    worker_service=name_service_headless, worker_port=worker_port)
                list_of_workers.append(worker_full_name)
            list_of_workers_as_string = ",".join(list_of_workers)
            env['BEXHOMA_{}_LIST'.format(statefulset_name.upper())] = list_of_workers_as_string
            list_of_workers_as_string_space = " ".join(list_of_workers)
            env['BEXHOMA_{}_LIST_SPACE'.format(statefulset_name.upper())] = (
                list_of_workers_as_string_space)
            env['BEXHOMA_{}_NAME'.format(statefulset_name.upper())] = (
                "{name_worker}".format(name_worker=name_worker))
            env['BEXHOMA_{}_SERVICE'.format(statefulset_name.upper())] = (
                "{worker_service}".format(worker_service=name_service_headless))
        with open(sut_manifest_file) as stream:
            try:
                result = yaml.safe_load_all(stream)
                result = [data for data in result]
                result = cfg.manifest.patch_dbms_args(result, cfg.experiment.dbms_args)
            except yaml.YAMLError as exc:
                print(exc)
        for key in reversed(range(len(result))):
            dep = result[key]
            ########################################
            # Kind=PersistentVolumeClaim
            ########################################
            if dep['kind'] == 'PersistentVolumeClaim':
                pvc = dep['metadata']['name']
                if not use_storage:
                    del result[key]
                elif use_ramdisk:
                    del result[key]
                else:
                    cfg.logger.debug('LifecycleManager.start_sut(PVC={},{})'.format(
                        pvc, name_pvc))
                    dep['metadata']['name'] = name_pvc
                    dep['metadata']['labels']['loaded'] = "False"
                    dep['metadata']['labels']['app'] = app
                    dep['metadata']['labels']['component'] = 'storage'
                    dep['metadata']['labels']['configuration'] = storageConfiguration
                    dep['metadata']['labels']['experiment'] = cfg.storage_label
                    dep['metadata']['labels']['dbms'] = cfg.docker
                    dep['metadata']['labels']['volume'] = cfg.volume
                    for label_key, label_value in cfg.additional_labels.items():
                        dep['metadata']['labels'][label_key] = str(label_value)
                    if (cfg.storage['storageClassName'] is not None
                            and len(cfg.storage['storageClassName']) > 0):
                        dep['spec']['storageClassName'] = cfg.storage['storageClassName']
                    else:
                        del result[key]['spec']['storageClassName']
                    if len(cfg.storage['storageSize']) > 0:
                        dep['spec']['resources']['requests']['storage'] = cfg.storage['storageSize']
                    pvcs = cfg.experiment.cluster.get_pvc(
                        app=app, component='storage',
                        experiment=cfg.storage_label, configuration=storageConfiguration)
                    if len(pvcs) > 0:
                        if (not cfg.loading_finished
                                and cfg.experiment.args_dict['request_storage_remove']
                                and cfg.num_experiment_to_apply_done == 0):
                            reset_and_remove_pvc(name_pvc)
                        else:
                            del result[key]
                if cfg.volume_per_tenant:
                    print(f"I need {cfg.num_tenants} copies of PVC")
                    for i in range(cfg.num_tenants):
                        dep_tenant = copy.deepcopy(dep)
                        dep_tenant['metadata']['name'] = (
                            dep_tenant['metadata']['name'] + "-" + str(i))
                        result.append(dep_tenant)
                        tenant_pvc_name = dep_tenant['metadata']['name']
                        if (not cfg.loading_finished
                                and cfg.experiment.args_dict['request_storage_remove']
                                and cfg.num_experiment_to_apply_done == 0):
                            reset_and_remove_pvc(tenant_pvc_name)
            ########################################
            # Kind=StatefulSet
            ########################################
            if dep['kind'] == 'StatefulSet':
                if dep['metadata']['labels']['component'] in cfg.deployment_infos['statefulset']:
                    statefulset = cfg.deployment_infos['statefulset'][
                        dep['metadata']['labels']['component']]
                else:
                    continue
                if cfg.num_worker == 0:
                    del result[key]
                    continue
                statefulset_type = dep['metadata']['labels']['component']
                dep['metadata']['name'] = statefulset['name']
                dep['metadata']['labels']['app'] = app
                dep['spec']['serviceName'] = statefulset['name']
                dep['metadata']['labels']['configuration'] = configuration
                dep['metadata']['labels']['experiment'] = experiment
                dep['metadata']['labels']['dbms'] = cfg.docker
                dep['metadata']['labels']['volume'] = cfg.volume
                for label_key, label_value in cfg.additional_labels.items():
                    dep['metadata']['labels'][label_key] = str(label_value)
                dep['spec']['replicas'] = cfg.num_worker
                dep['spec']['selector']['matchLabels'] = dep['metadata']['labels'].copy()
                dep['spec']['template']['metadata']['labels'] = dep['metadata']['labels'].copy()
                if 'initContainers' in dep['spec']['template']['spec']:
                    for i_container, container in enumerate(
                            dep['spec']['template']['spec']['initContainers']):
                        cfg.logger.debug('LifecycleManager.start_sut(create_manifest_statefulset({}))'.format(env))
                        if ('env' not in dep['spec']['template']['spec']['initContainers'][i_container]
                                or dep['spec']['template']['spec']['containers'][i_container]['env'] is None):
                            dep['spec']['template']['spec']['initContainers'][i_container]['env'] = []
                        for i_env, e in env.items():
                            index_of_env = next(
                                (i for i, d in enumerate(
                                    dep['spec']['template']['spec']['initContainers'][i_container]['env'])
                                 if d.get('name') == i_env), -1)
                            if index_of_env >= 0:
                                dep['spec']['template']['spec']['initContainers'][i_container]['env'][index_of_env]['value'] = str(e)
                            else:
                                dep['spec']['template']['spec']['initContainers'][i_container]['env'].append(
                                    {'name': i_env, 'value': str(e)})
                for i_container, container in enumerate(
                        dep['spec']['template']['spec']['containers']):
                    cfg.deployment_infos['statefulset'][statefulset_type]['containers'].append(
                        container['name'])
                    cfg.logger.debug('LifecycleManager.start_sut(create_manifest_statefulset({}))'.format(env))
                    if ('env' not in dep['spec']['template']['spec']['containers'][i_container]
                            or dep['spec']['template']['spec']['containers'][i_container]['env'] is None):
                        dep['spec']['template']['spec']['containers'][i_container]['env'] = []
                    for i_env, e in env.items():
                        index_of_env = next(
                            (i for i, d in enumerate(
                                dep['spec']['template']['spec']['containers'][i_container]['env'])
                             if d.get('name') == i_env), -1)
                        if index_of_env >= 0:
                            dep['spec']['template']['spec']['containers'][i_container]['env'][index_of_env]['value'] = str(e)
                        else:
                            dep['spec']['template']['spec']['containers'][i_container]['env'].append(
                                {'name': i_env, 'value': str(e)})
                    if container['name'] == 'dbms':
                        if 'args' in container and store_args:
                            cfg.deployment_infos['statefulset'][statefulset_type]['args'] = (
                                container['args'])
                            cfg.worker_startup_args = container['args']
                            cfg.logger.debug("{:30s}: worker args = {}".format(
                                configuration, container['args']))
                        else:
                            cfg.deployment_infos['statefulset'][statefulset_type]['args'] = []
                        if 'volumeMounts' in container:
                            for j, vol in enumerate(container['volumeMounts']):
                                if vol['name'] == 'bxw':
                                    if not use_storage:
                                        del result[key]['spec']['template']['spec']['containers'][i_container]['volumeMounts'][j]
                        if cfg.use_ephemeral_storage():
                            ephemeral_size = cfg.storage['storageSize']
                            c = dep['spec']['template']['spec']['containers'][i_container]
                            c.setdefault('resources', {})
                            c['resources'].setdefault('requests', {})
                            c['resources'].setdefault('limits', {})
                            c['resources']['requests']['ephemeral-storage'] = ephemeral_size
                            c['resources']['limits']['ephemeral-storage'] = ephemeral_size
                        req_cpu_w = 0
                        limit_cpu_w = 0
                        req_mem_w = 0
                        limit_mem_w = 0
                        if 'requests' in cfg.resources and 'cpu' in cfg.resources['requests']:
                            req_cpu_w = cfg.resources['requests']['cpu']
                        if 'requests' in cfg.resources and 'memory' in cfg.resources['requests']:
                            req_mem_w = cfg.resources['requests']['memory']
                        if 'limits' in cfg.resources and 'cpu' in cfg.resources['limits']:
                            limit_cpu_w = cfg.resources['limits']['cpu']
                        if 'limits' in cfg.resources and 'memory' in cfg.resources['limits']:
                            limit_mem_w = cfg.resources['limits']['memory']
                        c = dep['spec']['template']['spec']['containers'][i_container]
                        c.setdefault('resources', {})
                        c['resources'].setdefault('requests', {})
                        c['resources'].setdefault('limits', {})
                        c['resources']['requests']['cpu'] = req_cpu_w
                        c['resources']['limits']['cpu'] = limit_cpu_w
                        c['resources']['requests']['memory'] = req_mem_w
                        c['resources']['limits']['memory'] = limit_mem_w
                        if limit_cpu_w == "0":
                            del c['resources']['limits']['cpu']
                        if limit_mem_w == "0":
                            del c['resources']['limits']['memory']
                        if req_cpu_w == "0":
                            del c['resources']['requests']['cpu']
                        if req_mem_w == "0":
                            del c['resources']['requests']['memory']
                    elif (not cfg.monitoring_active
                          or cfg.experiment.cluster.monitor_cluster_active
                          or cfg.experiment.cluster.monitor_cluster_exists):
                        if container['name'] == 'cadvisor':
                            del result[key]['spec']['template']['spec']['containers'][i_container]
                            cfg.deployment_infos['statefulset'][statefulset_type]['containers'].pop()
                        if container['name'] == 'dcgm-exporter':
                            del result[key]['spec']['template']['spec']['containers'][i_container]
                            cfg.deployment_infos['statefulset'][statefulset_type]['containers'].pop()
                if 'volumes' in dep['spec']['template']['spec']:
                    for j, vol in enumerate(dep['spec']['template']['spec']['volumes']):
                        if vol['name'] == 'bxw':
                            if not use_storage:
                                del result[key]['spec']['template']['spec']['volumes'][j]
                            elif use_ramdisk:
                                del result[key]['spec']['template']['spec']['volumes'][j]['persistentVolumeClaim']
                                result[key]['spec']['template']['spec']['volumes'][j]['emptyDir'] = {
                                    'sizeLimit': cfg.storage['storageSize'], 'medium': 'Memory'}
                if 'volumeClaimTemplates' in result[key]['spec']:
                    name_worker_stateful_set = cfg.get_worker_name(component=statefulset_type)
                    if not use_storage or use_ramdisk:
                        del result[key]['spec']['volumeClaimTemplates']
                    else:
                        list_of_workers_pvcs = []
                        for worker in range(cfg.num_worker):
                            worker_full_name = "bxw-{name_worker}-{worker_number}".format(
                                name_worker=name_worker_stateful_set, worker_number=worker)
                            list_of_workers_pvcs.append(worker_full_name)
                        cfg.deployment_infos['statefulset'][statefulset_type]['pvc'] = (
                            list_of_workers_pvcs)
                        remove_old_pvcs = (
                            not cfg.loading_finished
                            and cfg.experiment.args_dict['request_storage_remove']
                            and cfg.num_experiment_to_apply_done == 0)
                        old_pvc_exist = False
                        for statefulset_name_pvc in list_of_workers_pvcs:
                            pvc_exists = cfg.experiment.cluster.pvc_exists(statefulset_name_pvc)
                            if pvc_exists > 0:
                                print("{:30s}: storage {} exists".format(
                                    configuration, statefulset_name_pvc))
                                old_pvc_exist = True
                                if remove_old_pvcs:
                                    print("{:30s}: storage {} should be removed".format(
                                        configuration, statefulset_name_pvc))
                                    cfg.experiment.cluster.delete_pvc(statefulset_name_pvc)
                        if old_pvc_exist and remove_old_pvcs:
                            cfg.wait(10)
                            for statefulset_name_pvc in list_of_workers_pvcs:
                                pvc_exists = cfg.experiment.cluster.pvc_exists(statefulset_name_pvc)
                                while pvc_exists:
                                    print("{:30s}: storage {} still exists".format(
                                        configuration, statefulset_name_pvc))
                                    cfg.wait(10)
                                    pvc_exists = cfg.experiment.cluster.pvc_exists(
                                        statefulset_name_pvc)
                                print("{:30s}: storage {} is gone".format(
                                    configuration, statefulset_name_pvc))
                        result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels']['app'] = app
                        result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels']['component'] = statefulset_type
                        result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels']['configuration'] = storageConfiguration
                        result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels']['experiment'] = cfg.storage_label
                        result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels']['dbms'] = cfg.docker
                        result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels']['volume'] = cfg.volume
                        for label_key, label_value in cfg.additional_labels.items():
                            result[key]['spec']['volumeClaimTemplates'][0]['metadata']['labels'][label_key] = str(label_value)
                        if (cfg.storage['storageClassName'] is not None
                                and len(cfg.storage['storageClassName']) > 0):
                            dep['spec']['volumeClaimTemplates'][0]['spec']['storageClassName'] = (
                                cfg.storage['storageClassName'])
                        else:
                            del result[key]['spec']['storageClassName']
                        if len(cfg.storage['storageSize']) > 0:
                            dep['spec']['volumeClaimTemplates'][0]['spec']['resources']['requests']['storage'] = cfg.storage['storageSize']
            ########################################
            # Kind=Job
            ########################################
            if dep['kind'] == 'Job':
                dep['metadata']['name'] = name_worker
                dep['metadata']['labels']['app'] = app
                dep['metadata']['labels']['configuration'] = configuration
                dep['metadata']['labels']['experiment'] = experiment
                dep['metadata']['labels']['dbms'] = cfg.docker
                dep['metadata']['labels']['volume'] = cfg.volume
                for label_key, label_value in cfg.additional_labels.items():
                    dep['metadata']['labels'][label_key] = str(label_value)
                dep['spec']['template']['metadata']['labels'] = dep['metadata']['labels'].copy()
                for i_container, container in enumerate(
                        dep['spec']['template']['spec']['containers']):
                    cfg.logger.debug('LifecycleManager.start_sut(add_env({}))'.format(env))
                    if ('env' not in dep['spec']['template']['spec']['containers'][i_container]
                            or dep['spec']['template']['spec']['containers'][i_container]['env'] is None):
                        dep['spec']['template']['spec']['containers'][i_container]['env'] = list()
                    for i_env, e in env.items():
                        index_of_env = next(
                            (i for i, d in enumerate(
                                dep['spec']['template']['spec']['containers'][i_container]['env'])
                             if d.get('name') == i_env), -1)
                        if index_of_env >= 0:
                            dep['spec']['template']['spec']['containers'][i_container]['env'][index_of_env]['value'] = str(e)
                        else:
                            dep['spec']['template']['spec']['containers'][i_container]['env'].append(
                                {'name': i_env, 'value': str(e)})
            ########################################
            # Kind=Service
            ########################################
            if dep['kind'] == 'Service':
                if dep['metadata']['labels']['component'] in cfg.deployment_infos['statefulset']:
                    statefulset = cfg.deployment_infos['statefulset'][
                        dep['metadata']['labels']['component']]
                    data = statefulset
                    if cfg.num_worker == 0:
                        del result[key]
                        continue
                else:
                    if dep['metadata']['labels']['component'] in cfg.deployment_infos['deployment']:
                        deployment = cfg.deployment_infos['deployment'][
                            dep['metadata']['labels']['component']]
                        data = deployment
                    else:
                        continue
                dep['metadata']['name'] = data['name_service']
                dep['metadata']['labels']['app'] = app
                dep['metadata']['labels']['configuration'] = configuration
                dep['metadata']['labels']['experiment'] = experiment
                dep['metadata']['labels']['dbms'] = cfg.docker
                dep['metadata']['labels']['volume'] = cfg.volume
                for label_key, label_value in cfg.additional_labels.items():
                    dep['metadata']['labels'][label_key] = str(label_value)
                if 'statefulset.kubernetes.io/pod-name' in dep['spec']['selector']:
                    dep['spec']['selector']['statefulset.kubernetes.io/pod-name'] = (
                        env['BEXHOMA_WORKER_NAME'] + '-0')
                else:
                    dep['spec']['selector']['configuration'] = configuration
                    dep['spec']['selector']['experiment'] = experiment
                    dep['spec']['selector']['dbms'] = cfg.docker
                    dep['spec']['selector']['volume'] = cfg.volume
                if not cfg.monitoring_active or (
                        cfg.experiment.cluster.monitor_cluster_exists
                        and not cfg.monitor_app_active):
                    for i, ports in reversed(list(enumerate(dep['spec']['ports']))):
                        if ('name' in ports
                                and ports['name'] != 'port-dbms'
                                and ports['name'] != 'port-bus'
                                and ports['name'] != 'port-web'):
                            del result[key]['spec']['ports'][i]
                if not cfg.monitoring_active or (
                        cfg.experiment.cluster.monitor_cluster_exists
                        and not cfg.monitor_app_active):
                    for i, ports in reversed(list(enumerate(dep['spec']['ports']))):
                        if ('name' in ports
                                and ports['name'] != 'port-dbms'
                                and ports['name'] != 'port-bus'
                                and ports['name'] != 'port-web'):
                            del result[key]['spec']['ports'][i]
            ########################################
            # Kind=Deployment
            ########################################
            if dep['kind'] == 'Deployment':
                if dep['metadata']['labels']['component'] in cfg.deployment_infos['deployment']:
                    deployment = cfg.deployment_infos['deployment'][
                        dep['metadata']['labels']['component']]
                else:
                    continue
                deployment_type = dep['metadata']['labels']['component']
                dep['metadata']['name'] = deployment['name']
                dep['metadata']['labels']['app'] = app
                dep['metadata']['labels']['configuration'] = configuration
                dep['metadata']['labels']['experiment'] = experiment
                dep['metadata']['labels']['dbms'] = cfg.docker
                dep['metadata']['labels']['volume'] = cfg.volume
                dep['metadata']['labels']['sut'] = name
                dep['metadata']['labels']['pool'] = name_pool
                for label_key, label_value in cfg.additional_labels.items():
                    dep['metadata']['labels'][label_key] = str(label_value)
                dep['metadata']['labels']['experimentRun'] = str(
                    cfg.num_experiment_to_apply_done + 1)
                dep['spec']['selector']['matchLabels'] = dep['metadata']['labels'].copy()
                dep['spec']['template']['metadata']['labels'] = dep['metadata']['labels'].copy()
                set_labels_from_loaded_pvc()
                for i_container, container in reversed(list(enumerate(
                        dep['spec']['template']['spec']['containers']))):
                    cfg.deployment_infos['deployment'][deployment_type]['containers'].append(
                        container['name'])
                    cfg.logger.debug('LifecycleManager.start_sut(create_manifest_deployment({}))'.format(env))
                    if ('env' not in dep['spec']['template']['spec']['containers'][i_container]
                            or dep['spec']['template']['spec']['containers'][i_container]['env'] is None):
                        dep['spec']['template']['spec']['containers'][i_container]['env'] = []
                    for i_env, e in env.items():
                        index_of_env = next(
                            (i for i, d in enumerate(
                                dep['spec']['template']['spec']['containers'][i_container]['env'])
                             if d.get('name') == i_env), -1)
                        if index_of_env >= 0:
                            dep['spec']['template']['spec']['containers'][i_container]['env'][index_of_env]['value'] = str(e)
                        else:
                            dep['spec']['template']['spec']['containers'][i_container]['env'].append(
                                {'name': i_env, 'value': str(e)})
                    if container['name'] == 'dbms':
                        if 'args' in container and store_args:
                            cfg.sut_startup_args = container['args']
                            cfg.logger.debug("{:30s}: server args = {}".format(
                                configuration, container['args']))
                        if 'volumeMounts' in container and len(container['volumeMounts']) > 0:
                            for j, vol in reversed(list(enumerate(container['volumeMounts']))):
                                if vol['name'] == 'benchmark-storage-volume':
                                    if not use_storage:
                                        del result[key]['spec']['template']['spec']['containers'][i_container]['volumeMounts'][j]
                                    elif cfg.volume_per_tenant:
                                        print(f"I need {cfg.num_tenants} copies of volumeMounts")
                                        for i in range(cfg.num_tenants):
                                            vol_tenant = copy.deepcopy(vol)
                                            vol_tenant['mountPath'] = f"/tenant_{i}"
                                            vol_tenant['name'] = vol_tenant['name'] + "-" + str(i)
                                            dep['spec']['template']['spec']['containers'][i_container]['volumeMounts'].append(vol_tenant)
                                if vol['name'] == 'benchmark-data-volume':
                                    if not use_data:
                                        del result[key]['spec']['template']['spec']['containers'][i_container]['volumeMounts'][j]
                        if deployment_type == 'sut':
                            if cfg.dockerimage:
                                result[key]['spec']['template']['spec']['containers'][i_container]['image'] = cfg.dockerimage
                            else:
                                cfg.dockerimage = result[key]['spec']['template']['spec']['containers'][i_container]['image']
                    elif (not cfg.monitoring_active
                          or cfg.experiment.cluster.monitor_cluster_active
                          or cfg.experiment.cluster.monitor_cluster_exists):
                        if container['name'] == 'cadvisor':
                            del result[key]['spec']['template']['spec']['containers'][i_container]
                            cfg.deployment_infos['deployment'][deployment_type]['containers'].pop()
                        if container['name'] == 'dcgm-exporter':
                            del result[key]['spec']['template']['spec']['containers'][i_container]
                            cfg.deployment_infos['deployment'][deployment_type]['containers'].pop()
                if ('volumes' in dep['spec']['template']['spec']
                        and dep['spec']['template']['spec']['volumes'] is not None):
                    for i, vol in reversed(list(enumerate(
                            dep['spec']['template']['spec']['volumes']))):
                        if vol['name'] == 'benchmark-storage-volume':
                            if not use_storage:
                                del result[key]['spec']['template']['spec']['volumes'][i]
                            elif use_ramdisk:
                                del result[key]['spec']['template']['spec']['volumes'][i]['persistentVolumeClaim']
                                result[key]['spec']['template']['spec']['volumes'][i]['emptyDir'] = {
                                    'sizeLimit': cfg.storage['storageSize'], 'medium': 'Memory'}
                            else:
                                vol['persistentVolumeClaim']['claimName'] = name_pvc
                                if cfg.volume_per_tenant:
                                    print(f"I need {cfg.num_tenants} copies of volumes")
                                    for i in range(cfg.num_tenants):
                                        vol_tenant = copy.deepcopy(vol)
                                        vol_tenant['name'] = vol_tenant['name'] + "-" + str(i)
                                        vol_tenant['persistentVolumeClaim']['claimName'] = (
                                            vol_tenant['persistentVolumeClaim']['claimName']
                                            + "-" + str(i))
                                        dep['spec']['template']['spec']['volumes'].append(vol_tenant)
                                cfg.deployment_infos['deployment'][deployment_type]['pvc'] = [name_pvc]
                        if vol['name'] == 'benchmark-data-volume':
                            if not use_data:
                                del result[key]['spec']['template']['spec']['volumes'][i]
                        if 'hostPath' in vol and not cfg.monitoring_active:
                            del result[key]['spec']['template']['spec']['volumes'][i]
                if 'initContainers' in result[key]['spec']['template']['spec']:
                    if not use_storage:
                        del result[key]['spec']['template']['spec']['initContainers']
                    else:
                        for i_container, container in reversed(list(enumerate(
                                dep['spec']['template']['spec']['initContainers']))):
                            if ('volumeMounts' in container
                                    and len(container['volumeMounts']) > 0):
                                for j, vol in reversed(list(enumerate(
                                        container['volumeMounts']))):
                                    if vol['name'] == 'benchmark-storage-volume':
                                        if not use_storage:
                                            del result[key]['spec']['template']['spec']['initContainers'][i_container]['volumeMounts'][j]
                                        elif cfg.volume_per_tenant:
                                            print(f"I need {cfg.num_tenants} copies of volumeMounts")
                                            for i in range(cfg.num_tenants):
                                                vol_tenant = copy.deepcopy(vol)
                                                vol_tenant['mountPath'] = f"/tenant_{i}"
                                                vol_tenant['name'] = (
                                                    vol_tenant['name'] + "-" + str(i))
                                                dep['spec']['template']['spec']['initContainers'][i_container]['volumeMounts'].append(vol_tenant)
                if deployment_type == 'pool':
                    if 'replicas_pooling' in cfg.resources:
                        num_replicas_pooling = cfg.resources['replicas_pooling']
                        result[key]['spec']['replicas'] = num_replicas_pooling
                if deployment_type == 'sut':
                    if 'replicas_sut' in cfg.resources:
                        num_replicas_sut = cfg.resources['replicas_sut']
                        result[key]['spec']['replicas'] = num_replicas_sut
                    for i_container, container in reversed(list(enumerate(
                            dep['spec']['template']['spec']['containers']))):
                        if container['name'] == 'dbms':
                            break
                    req_cpu = 0
                    limit_cpu = 0
                    req_mem = 0
                    limit_mem = 0
                    req_gpu = 0
                    node_cpu = ''
                    node_gpu = ''
                    if 'requests' in cfg.resources and 'cpu' in cfg.resources['requests']:
                        req_cpu = cfg.resources['requests']['cpu']
                    if 'requests' in cfg.resources and 'memory' in cfg.resources['requests']:
                        req_mem = cfg.resources['requests']['memory']
                    if 'limits' in cfg.resources and 'cpu' in cfg.resources['limits']:
                        limit_cpu = cfg.resources['limits']['cpu']
                    if 'limits' in cfg.resources and 'memory' in cfg.resources['limits']:
                        limit_mem = cfg.resources['limits']['memory']
                    if 'nodeSelector' in cfg.resources and 'cpu' in cfg.resources['nodeSelector']:
                        node_cpu = cfg.resources['nodeSelector']['cpu']
                    if 'nodeSelector' in cfg.resources and 'gpu' in cfg.resources['nodeSelector']:
                        node_gpu = cfg.resources['nodeSelector']['gpu']
                    if 'nodeSelector' in cfg.resources:
                        nodeSelectors = cfg.resources['nodeSelector'].copy()
                    else:
                        nodeSelectors = {}
                    num_replicas_pooling = 0
                    if 'replicas_pooling' in cfg.resources:
                        num_replicas_pooling = cfg.resources['replicas_pooling']
                    cfg.resources = {}
                    cfg.resources['requests'] = {}
                    cfg.resources['requests']['cpu'] = req_cpu
                    cfg.resources['requests']['memory'] = req_mem
                    cfg.resources['requests']['gpu'] = req_gpu
                    cfg.resources['limits'] = {}
                    cfg.resources['limits']['cpu'] = limit_cpu
                    cfg.resources['limits']['memory'] = limit_mem
                    cfg.resources['nodeSelector'] = {}
                    cfg.resources['nodeSelector']['cpu'] = node_cpu
                    cfg.resources['nodeSelector']['gpu'] = node_gpu
                    if num_replicas_pooling > 0:
                        cfg.resources['replicas_pooling'] = num_replicas_pooling
                    dep['spec']['template']['spec']['containers'][i_container]['resources']['requests']['cpu'] = req_cpu
                    dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']['cpu'] = limit_cpu
                    dep['spec']['template']['spec']['containers'][i_container]['resources']['requests']['memory'] = req_mem
                    dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']['memory'] = limit_mem
                    if limit_cpu == "0":
                        del dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']['cpu']
                    if limit_mem == "0":
                        del dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']['memory']
                    if req_cpu == "0":
                        del dep['spec']['template']['spec']['containers'][i_container]['resources']['requests']['cpu']
                    if req_mem == "0":
                        del dep['spec']['template']['spec']['containers'][i_container]['resources']['requests']['memory']
                    if cfg.use_ephemeral_storage():
                        ephemeral_size = cfg.storage['storageSize']
                        dep['spec']['template']['spec']['containers'][i_container]['resources']['requests']['ephemeral-storage'] = ephemeral_size
                        dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']['ephemeral-storage'] = ephemeral_size
                    if node_gpu:
                        if 'nodeSelector' not in dep['spec']['template']['spec']:
                            dep['spec']['template']['spec']['nodeSelector'] = {}
                        if dep['spec']['template']['spec']['nodeSelector'] is None:
                            dep['spec']['template']['spec']['nodeSelector'] = {}
                        dep['spec']['template']['spec']['nodeSelector']['gpu'] = node_gpu
                        dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']['nvidia.com/gpu'] = int(req_gpu)
                    else:
                        if 'nvidia.com/gpu' in dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']:
                            del dep['spec']['template']['spec']['containers'][i_container]['resources']['limits']['nvidia.com/gpu']
                    if 'nodeSelector' not in dep['spec']['template']['spec']:
                        dep['spec']['template']['spec']['nodeSelector'] = {}
                    if dep['spec']['template']['spec']['nodeSelector'] is None:
                        dep['spec']['template']['spec']['nodeSelector'] = {}
                    dep['spec']['template']['spec']['nodeSelector']['cpu'] = node_cpu
                    if node_cpu == '':
                        del dep['spec']['template']['spec']['nodeSelector']['cpu']
                    for nodeSelector, value in nodeSelectors.items():
                        if nodeSelector == 'cpu' or nodeSelector == 'gpu':
                            continue
                        dep['spec']['template']['spec']['nodeSelector'][nodeSelector] = value
                        cfg.resources['nodeSelector'][nodeSelector] = value
                    if 'sut' in cfg.nodes:
                        if 'nodeSelector' not in dep['spec']['template']['spec']:
                            dep['spec']['template']['spec']['nodeSelector'] = dict()
                        if dep['spec']['template']['spec']['nodeSelector'] is None:
                            dep['spec']['template']['spec']['nodeSelector'] = dict()
                        dep['spec']['template']['spec']['nodeSelector']['type'] = cfg.nodes['sut']
        with open(deployment_experiment, "w+") as stream:
            try:
                stream.write(yaml.dump_all(result))
            except yaml.YAMLError as exc:
                print(exc)
        cfg.logger.debug("Deploy " + deployment_experiment)
        cfg.experiment.cluster.create_object_from_file(deployment_experiment)
        return True

    def stop_sut(
        self,
        app: str = '',
        component: str = 'sut',
        experiment: str = '',
        configuration: str = '',
    ) -> None:
        """Stop the SUT deployment and remove services, stateful sets, and optionally storage.

        :param app: App label.
        :param component: Component label (default ``'sut'``).
        :param experiment: Experiment code.
        :param configuration: DBMS configuration name.
        """
        cfg = self._config
        if len(app) == 0:
            app = cfg.appname
        if len(configuration) == 0:
            configuration = cfg.configuration
        if len(experiment) == 0:
            experiment = cfg.code
        cfg.logger.debug(
            f"stop_sut component={component} experiment={experiment} configuration={configuration}")
        if len(cfg.storage) > 0 and 'keep' in cfg.storage and cfg.storage['keep']:
            pass
        else:
            use_storage = cfg.use_storage()
            if use_storage:
                if cfg.storage['storageConfiguration']:
                    storageConfiguration = cfg.storage['storageConfiguration']
                else:
                    storageConfiguration = configuration
                name_pvc = cfg.generate_component_name(
                    app=app, component='storage',
                    experiment=cfg.storage_label, configuration=storageConfiguration)
                cfg.experiment.cluster.delete_pvc(name_pvc)
                worker_pvcs = cfg.experiment.cluster.get_pvc(
                    app=app, component='worker',
                    experiment=experiment, configuration=storageConfiguration)
                for pvc_name in worker_pvcs:
                    cfg.experiment.cluster.delete_pvc(pvc_name)
        deployments = cfg.experiment.cluster.get_deployments(
            app=app, component=component, experiment=experiment, configuration=configuration)
        for deployment in deployments:
            cfg.experiment.cluster.delete_deployment(deployment)
        stateful_sets = cfg.experiment.cluster.get_stateful_sets(
            app=app, component=component, experiment=experiment, configuration=configuration)
        for stateful_set in stateful_sets:
            cfg.experiment.cluster.delete_stateful_set(stateful_set)
        jobs = cfg.experiment.cluster.get_jobs(
            app=app, component=component, experiment=experiment, configuration=configuration)
        for job in jobs:
            cfg.experiment.cluster.delete_job(job)
        services = cfg.experiment.cluster.get_services(
            app=app, component=component, experiment=experiment, configuration=configuration)
        for service in services:
            cfg.experiment.cluster.delete_service(service)
        if cfg.experiment.monitoring_active:
            self.stop_monitoring()
        if cfg.experiment.maintaining_active:
            self.stop_maintaining()
        if cfg.experiment.loading_active:
            self.stop_loading()
        if component == 'sut':
            if 'deployment' in cfg.deployment_infos:
                list_of_worker_components = list(cfg.deployment_infos['deployment'].keys())
                for worker_component in list_of_worker_components:
                    if worker_component != 'sut':
                        self.stop_sut(
                            app=app, component=worker_component,
                            experiment=cfg.get_experiment_name(),
                            configuration=configuration)
            if 'statefulset' in cfg.deployment_infos:
                list_of_worker_components = list(cfg.deployment_infos['statefulset'].keys())
                for worker_component in list_of_worker_components:
                    if worker_component != 'sut':
                        self.stop_sut(
                            app=app, component=worker_component,
                            experiment=experiment, configuration=configuration)
