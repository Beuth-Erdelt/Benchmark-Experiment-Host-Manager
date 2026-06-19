"""Host probe methods for SUT pods."""
from __future__ import annotations

import json
import logging
import os
from collections import Counter
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from .base import SutConfiguration

__all__ = ['HostProbe']


class HostProbe:
    """Runs shell commands inside the SUT pod to collect host-level metrics.

    :param config: The parent configuration this probe belongs to.
    :type config: SutConfiguration
    """

    def __init__(self, config: SutConfiguration) -> None:
        """Initialise with a back-reference to the parent configuration.

        :param config: Parent :class:`SutConfiguration` instance.
        :type config: SutConfiguration
        """
        self._config = config

    def check_dbms_connection(self, ip: str, port: int) -> bool:
        """Check if DBMS is open for connections by opening a socket to ip:port.

        :param ip: IP of the host to connect to.
        :param port: Port of the server on the host to connect to.
        :return: True iff connecting is possible.
        :rtype: bool
        """
        import socket
        self._config.logger.debug('HostProbe.check_dbms_connection()')
        found = False
        s = socket.socket()
        s.settimeout(10)
        try:
            s.connect((ip, port))
            found = True
            print("Somebody is answering at %s:%d" % (ip, port))
        except Exception:
            print("Nobody is answering yet at %s:%d" % (ip, port))
        finally:
            s.close()
        return found

    def get_host_volume(self, pod: str = '') -> Tuple:
        """Return (size, used) of mounted volumes in the SUT container.

        :param pod: Optional pod name override; defaults to current SUT pod.
        :return: Tuple (size, used) as human-readable strings.
        :rtype: tuple
        """
        self._config.logger.debug('HostProbe.get_host_volume()')
        try:
            command = "df -hP | grep volumes"
            _, stdout, _ = self._config.execute_command_in_pod_sut(command=command, pod=pod)
            parts = stdout.split(" ")
            parts = [x for x in parts if x != '']
            if len(parts) > 2:
                size = parts[1]
                used = parts[2]
                return size, used
            else:
                return 0, 0
        except Exception as exc:
            logging.error(exc)
            return "", ""

    def get_host_hugepages_total(self) -> int:
        """Return the HugePages_Total value from /proc/meminfo.

        :return: Total huge pages count, or 0 on failure.
        :rtype: int
        """
        self._config.logger.debug('HostProbe.get_host_hugepages_total()')
        try:
            command = "cat /proc/meminfo | grep HugePages_Total"
            _, stdout, _ = self._config.execute_command_in_pod_sut(command=command)
            mem = int(stdout.replace(" ", "").replace("HugePages_Total:", ""))
            return mem
        except Exception as exc:
            logging.error(exc)
            return 0

    def get_host_hugepages_free(self) -> int:
        """Return the HugePages_Free value from /proc/meminfo.

        :return: Free huge pages count, or 0 on failure.
        :rtype: int
        """
        self._config.logger.debug('HostProbe.get_host_hugepages_free()')
        try:
            command = "cat /proc/meminfo | grep HugePages_Free"
            _, stdout, _ = self._config.execute_command_in_pod_sut(command=command)
            mem = int(stdout.replace(" ", "").replace("HugePages_Free:", ""))
            return mem
        except Exception as exc:
            logging.error(exc)
            return 0

    def get_host_cpulist(self) -> str:
        """Return the allowed CPU list from /proc/self/status.

        :return: CPU list string, or empty string on failure.
        :rtype: str
        """
        self._config.logger.debug('HostProbe.get_host_cpulist()')
        try:
            command = "grep ^Cpus_allowed_list /proc/self/status | awk '{print $2}'"
            _, stdout, _ = self._config.execute_command_in_pod_sut(command=command)
            result = stdout.replace('Cpus_allowed_list:\t', '').replace('\n', '')
            return result
        except Exception as exc:
            logging.error(exc)
            return ""

    def get_host_memory(self) -> int:
        """Return total RAM in bytes from /proc/meminfo.

        :return: Total RAM in bytes, or 0 on failure.
        :rtype: int
        """
        self._config.logger.debug('HostProbe.get_host_memory()')
        try:
            command = "grep MemTotal /proc/meminfo | awk '{print $2}'"
            _, stdout, _ = self._config.execute_command_in_pod_sut(command=command)
            mem = int(stdout.replace(" ", "").replace("MemTotal:", "").replace("kB", "")) * 1024
            return mem
        except Exception as exc:
            logging.error(exc)
            return 0

    def get_host_cpu(self) -> str:
        """Return CPU model name from /proc/cpuinfo.

        :return: CPU model name string.
        :rtype: str
        """
        self._config.logger.debug('HostProbe.get_host_cpu()')
        command = "more /proc/cpuinfo | grep 'model name' | head -n 1"
        _, stdout, _ = self._config.execute_command_in_pod_sut(command=command)
        cpu = stdout
        cpu = cpu.replace('model name\t: ', '')
        return cpu.replace('\n', '')

    def get_host_cores(self) -> int:
        """Return the number of CPU cores from /proc/cpuinfo.

        :return: Core count, or 0 on failure.
        :rtype: int
        """
        self._config.logger.debug('HostProbe.get_host_cores()')
        command = 'grep -c ^processor /proc/cpuinfo'
        try:
            _, stdout, _ = self._config.execute_command_in_pod_sut(command=command)
            if len(stdout) > 0:
                return int(stdout)
            else:
                return 0
        except Exception as exc:
            logging.error(exc)
            return 0

    def get_host_system(self) -> str:
        """Return the OS kernel version via uname -r.

        :return: Kernel version string.
        :rtype: str
        """
        self._config.logger.debug('HostProbe.get_host_system()')
        command = 'uname -r'
        _, stdout, _ = self._config.execute_command_in_pod_sut(command=command)
        return stdout.replace('\n', '')

    def get_host_restarts(self, pod_sut: str = '') -> str:
        """Return the container restart counts for the SUT pod via kubectl.

        :param pod_sut: Optional pod name override; defaults to current SUT pod.
        :return: Restart count string from kubectl jsonpath output.
        :rtype: str
        """
        self._config.logger.debug('HostProbe.get_host_restarts()')
        if len(pod_sut) == 0:
            pod_sut = self._config.pod_sut
        result = self._config.experiment.cluster.kubectl(
            'get pods/' + pod_sut + ' -o jsonpath="{.status.containerStatuses[*].restartCount}"')
        try:
            return result
        except Exception:
            return ""

    def get_host_node(self) -> str:
        """Return the node name the SUT pod is scheduled on.

        :return: Node name string, or empty string on failure.
        :rtype: str
        """
        self._config.logger.debug('HostProbe.get_host_node()')
        result = self._config.experiment.cluster.kubectl(
            'get pods/' + self._config.pod_sut + ' -o=json')
        try:
            datastore = json.loads(result)
            if self._config.pod_sut == datastore['metadata']['name']:
                node = datastore['spec']['nodeName']
                return node
        except Exception:
            return ""
        return ""

    def get_host_gpus(self) -> str:
        """Return GPU model summary string from nvidia-smi -L.

        :return: Formatted string like "2 x Tesla V100-SXM2-32GB".
        :rtype: str
        """
        self._config.logger.debug('HostProbe.get_host_gpus()')
        command = 'nvidia-smi -L'
        _, stdout, _ = self._config.execute_command_in_pod_sut(command=command)
        gpus = stdout
        gpu_lines = gpus.split("\n")
        gpu_count = Counter(
            [x[x.find(":")+2:x.find("(")-1] for x in gpu_lines if len(x) > 0])
        result = ""
        for model, count in gpu_count.items():
            result += str(count) + " x " + model
        return result

    def get_host_gpu_ids(self) -> list:
        """Return list of GPU UUIDs from nvidia-smi -L.

        :return: List of GPU UUID strings.
        :rtype: list[str]
        """
        self._config.logger.debug('HostProbe.get_host_gpu_ids()')
        command = 'nvidia-smi -L'
        _, stdout, _ = self._config.execute_command_in_pod_sut(command=command)
        gpus = stdout
        gpu_lines = gpus.split("\n")
        result = []
        for _, gpu in enumerate(gpu_lines):
            gpu_id = gpu[gpu.find('UUID: ') + 6:gpu.find(')', gpu.find('UUID: '))]
            if len(gpu_id) > 0:
                result.append(gpu_id)
        return result

    def get_host_cuda(self) -> str:
        """Return CUDA version string from nvidia-smi output.

        :return: CUDA version string, stripped of surrounding whitespace and pipes.
        :rtype: str
        """
        self._config.logger.debug('HostProbe.get_host_cuda()')
        command = "nvidia-smi | grep 'CUDA'"
        _, stdout, _ = self._config.execute_command_in_pod_sut(command=command)
        return stdout.replace('|', '').replace('\n', '').strip()

    def getTimediff(self) -> int:
        """Return clock skew in seconds between the SUT pod and the local host.

        Runs ``date +"%s"`` inside the SUT pod and locally, then returns
        ``remote_timestamp - local_timestamp``.

        :return: Clock difference in seconds (positive means remote is ahead).
        :rtype: int
        """
        self._config.logger.debug('HostProbe.getTimediff()')
        command = 'date +"%s"'
        _, stdout, _ = self._config.execute_command_in_pod_sut(command=command)
        timestamp_remote = stdout
        timestamp_local = os.popen(command).read()
        return int(timestamp_remote) - int(timestamp_local)

    def get_host_diskspace_used_data(self) -> int:
        """Return disk space used for database data directory in megabytes.

        :return: Size in megabytes, or 0 on failure or if no datadir configured.
        :rtype: int
        """
        self._config.logger.debug('HostProbe.get_host_diskspace_used_data()')
        if 'datadir' not in self._config.dockertemplate:
            return 0
        datadir = self._config.dockertemplate['datadir']
        try:
            command = "du --block-size=1M -Ls " + datadir + " | awk 'END{print \\$1}'"
            _, stdout, _ = self._config.execute_command_in_pod_sut(command)
            if len(stdout) > 0:
                return int(stdout.replace('\n', ''))
            else:
                return 0
        except Exception:
            command = "du --block-size=1M -Ls " + datadir + " | awk 'END{print $1}'"
            try:
                _, stdout, _ = self._config.execute_command_in_pod_sut(command)
                if len(stdout) > 0:
                    size_str = stdout.replace('\n', '')
                    if len(size_str) > 0:
                        return int(size_str)
            except Exception:
                return 0
        return 0

    def get_host_diskspace_used(self) -> int:
        """Return disk space used on the root filesystem in megabytes.

        :return: Used disk space in megabytes, or 0 on failure.
        :rtype: int
        """
        self._config.logger.debug('HostProbe.get_host_diskspace_used()')
        try:
            command = "df -m / | awk 'NR == 2{print \\$3}'"
            _, stdout, _ = self._config.execute_command_in_pod_sut(command=command)
            return int(stdout.replace('\n', ''))
        except Exception:
            command = "df -m / | awk 'NR == 2{print $3}'"
            try:
                _, stdout, _ = self._config.execute_command_in_pod_sut(command=command)
                if len(stdout) > 0:
                    return int(stdout.replace('\n', ''))
            except Exception:
                return 0
        return 0

    def check_volumes(self) -> None:
        """Write volume size/used labels to PVCs by probing mounted volumes in pods.

        Iterates over all tracked deployments and stateful sets, calls
        ``get_host_volume()`` per pod, and writes the result as labels on the
        associated PVC via ``kubectl label``.
        """
        use_storage = self._config.use_storage()
        use_ramdisk = self._config.use_ramdisk()
        if not (use_storage and not use_ramdisk):
            return
        if 'deployment' in self._config.deployment_infos:
            for component, deployment in self._config.deployment_infos['deployment'].items():
                for _, pod in enumerate(deployment['pods']):
                    pvc = deployment['pvc']
                    print("{:30s}: get size via pod {} and write to pvc {}".format(
                        self._config.configuration, pod, pvc))
                    size, used = self.get_host_volume(pod=pod)
                    fullcommand = 'label pvc {} --overwrite volume_size="{}" volume_used="{}"'.format(
                        pvc, size, used)
                    self._config.experiment.cluster.kubectl(fullcommand)
        if 'statefulset' in self._config.deployment_infos:
            for component, statefulset in self._config.deployment_infos['statefulset'].items():
                for i, pod in enumerate(statefulset['pods']):
                    if 'pvc' not in statefulset:
                        continue
                    pvc = statefulset['pvc'][i]
                    print("{:30s}: get size via pod {} and write to pvc {}".format(
                        self._config.configuration, pod, pvc))
                    size, used = self.get_host_volume(pod=pod)
                    fullcommand = 'label pvc {} --overwrite volume_size="{}" volume_used="{}"'.format(
                        pvc, size, used)
                    self._config.experiment.cluster.kubectl(fullcommand)

    def get_host_all(self) -> dict:
        """Call all get_host_* probes and return a consolidated dict.

        :return: Dict of host metrics (RAM, CPU, GPU, Cores, host, node, disk, etc.).
        :rtype: dict
        """
        server = {}
        server['RAM'] = self.get_host_memory()
        server['CPU'] = self.get_host_cpu()
        server['GPU'] = self.get_host_gpus()
        server['GPUIDs'] = self.get_host_gpu_ids()
        server['Cores'] = self.get_host_cores()
        server['host'] = self.get_host_system()
        server['node'] = self.get_host_node()
        server['disk'] = self.get_host_diskspace_used()
        server['datadisk'] = self.get_host_diskspace_used_data()
        size, used = self.get_host_volume()
        server['volume_size'] = size
        server['volume_used'] = used
        server['cuda'] = self.get_host_cuda()
        server['hugepages_total'] = self.get_host_hugepages_total()
        server['hugepages_free'] = self.get_host_hugepages_free()
        server['cpu_list'] = self.get_host_cpulist()
        server['cuda'] = self.get_host_cuda()
        server['args'] = self._config.sut_startup_args
        return server
