
class yugabytedb(default):
    """
    :Date: 2022-10-01
    :Version: 0.6.0
    :Authors: Patrick K. Erdelt

        Class for managing an DBMS configuation.
        This is plugged into an experiment object.
        This class contains specific settings for a YugabyteDB installation.
        This is handled outside of bexhoma with the official helm chart.
        The service name is fixed to be "yb-tserver-service"

        :param experiment: Unique identifier of the experiment
        :param docker: Name of the Docker image
        :param configuration: Name of the configuration
        :param script: Unique identifier of the experiment
        :param alias: Unique identifier of the experiment

        Copyright (C) 2020  Patrick K. Erdelt

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
    def get_service_sut(self, configuration):
        """
        Returns the same of the service where to connect to the SUT.
        This in general is the name of the service of the deployed component.
        For SUT, that require a component that is not controlled by bexhoma, this may be overwritten.
        Here, always "yb-tserver-service" is returned.

        :param configuration: name of the configuration
        :return: name of the configuration's sut's service
        """
        return "yb-tserver-service"




class kinetica(default):
    """
    :Date: 2022-10-01
    :Version: 0.6.0
    :Authors: Patrick K. Erdelt

        Class for managing an DBMS configuation.
        This is plugged into an experiment object.
        This class contains specific settings for a Kinetica installation.
        This is handled outside of bexhoma with the official KAgent.
        The service name is fixed to be "bexhoma-service-kinetica"

        :param experiment: Unique identifier of the experiment
        :param docker: Name of the Docker image
        :param configuration: Name of the configuration
        :param script: Unique identifier of the experiment
        :param alias: Unique identifier of the experiment

        Copyright (C) 2020  Patrick K. Erdelt

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
    def get_service_sut(self, configuration):
        """
        Returns the same of the service where to connect to the SUT.
        This in general is the name of the service of the deployed component.
        For SUT, that require a component that is not controlled by bexhoma, this may be overwritten.
        Here, always "bexhoma-service-kinetica" is returned.

        :param configuration: name of the configuration
        :return: name of the configuration's sut's service
        """
        return "bexhoma-service-kinetica"
    def create_monitoring(self, app='', component='monitoring', experiment='', configuration=''):
        """
        Generate a name for the monitoring component.
        Basically this is `{app}-{component}-{configuration}-{experiment}-{client}`.
        For Kinetica, the service to be monitored is named 'bexhoma-service-kinetica'.

        :param app: app the component belongs to
        :param component: Component, for example sut or monitoring
        :param experiment: Unique identifier of the experiment
        :param configuration: Name of the dbms configuration
        """
        if component == 'sut':
            name = 'bexhoma-service-kinetica'
        else:
            name = self.generate_component_name(app=app, component=component, experiment=experiment, configuration=configuration)
        self.logger.debug("kinetica.create_monitoring({})".format(name))
        return name
    def set_metric_of_config(self, metric, host, gpuid):
        """
        Returns a promql query.
        Parameters in this query are substituted, so that prometheus finds the correct metric.
        Example: In 'sum(irate(container_cpu_usage_seconds_total{{container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_pod_name=~"(.*){configuration}-{experiment}(.*)", container_label_io_kubernetes_container_name="dbms"}}[1m]))'
        configuration and experiment are placeholders and will be replaced by concrete values.
        Here: We do not have a SUT that is specific to the experiment or configuration.

        :param metric: Parametrized promql query
        :param host: Name of the host the metrics should be collected from
        :param gpuid: GPU that the metrics should watch
        :return: promql query without parameters
        """
        return metric.format(host=host, gpuid=gpuid, configuration='kinetica', experiment='worker')
    def get_worker_endpoints(self):
        """
        Returns all endpoints of a headless service that monitors nodes of a distributed DBMS.
        These are IPs of cAdvisor instances.
        The endpoint list is to be filled in a config of an instance of Prometheus.
        For Kinetica the service is fixed to be 'bexhoma-service-monitoring-default' and does not depend on the experiment.

        :return: list of endpoints
        """
        endpoints = self.experiment.cluster.get_service_endpoints(service_name="bexhoma-service-monitoring-default")
        self.logger.debug("kinetica.get_worker_endpoints({})".format(endpoints))
        return endpoints






