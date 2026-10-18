"""Host probe methods for SUT pods."""
from __future__ import annotations

import copy
import json
import logging
import os
from collections import Counter
from typing import TYPE_CHECKING, Optional, Tuple

from .. import sut_restarts
from ..clusters import POD_NOT_READ

if TYPE_CHECKING:
    from .base import SutConfiguration

__all__ = ['HostProbe']

#: Values of :meth:`HostProbe.get_host_all` that do not change while a pod
#: lives; measured once per pod UID. All others are measured every time.
STATIC_HOST_INFO = ('RAM', 'CPU', 'GPU', 'GPUIDs', 'Cores', 'host', 'node',
                    'cuda', 'hugepages_total', 'cpu_list')


def _field(output: str, line: int, field: int) -> str:
    """Return a whitespace-separated field of one line, as awk would print it.

    :param output: Command output.
    :param line: Line index (``-1`` for the last line, as awk's ``END``).
    :param field: 0-based field index (awk's ``$1`` is 0).
    :return: The field, or ``''`` if the line or field does not exist.
    """
    lines = (output or '').splitlines()
    try:
        return lines[line].split()[field]
    except IndexError:
        return ''


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
        #: Values of :meth:`get_host_all` that do not change while a pod lives, per pod UID.
        self._static_host_info: dict = {}

    def _run(self, command: str, pod: str = '') -> tuple:
        """Run a read-only probe command in the SUT container (or ``pod``).

        Goes through the Python client (about 0.26 s instead of 1.6 s per
        kubectl process), with kubectl as fallback.

        :param command: Shell command; must not depend on a local shell's quoting.
        :param pod: Pod name; defaults to the current SUT pod.
        :return: ``("", stdout, stderr)``.
        """
        return self._config.execute_command_in_pod_sut(command=command, pod=pod, api=True)

    def _read_pod(self):
        """Read the current SUT pod through the API, if the cluster can.

        :return: The pod object, or ``None`` if it is gone or cannot be read this way.
        """
        read_pod = getattr(self._config.experiment.cluster, '_read_pod', None)
        if read_pod is None or not self._config.pod_sut:
            return None
        pod_object = read_pod(self._config.pod_sut)
        return None if pod_object is POD_NOT_READ else pod_object

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

    def get_data_paths(self, component: str = 'sut', kind: str = 'deployment') -> Tuple:
        """Return (data path, pvc mount path) of a component, as its template mounts them.

        The data path is where the template mounts the storage volume
        (``benchmark-storage-volume`` for a Deployment, ``bxw`` for a worker
        StatefulSet), recorded whether or not a pvc is attached; the mount path
        only when it is. A template without such a mount (e.g. TiDB's SQL
        layer, a DatabaseService) falls back to the DBMS ``datadir`` of
        ``cluster.config``.

        :param component: Component name, e.g. ``sut``, ``pool``, ``tikv``.
        :param kind: ``deployment`` or ``statefulset``.
        :return: Tuple (data_path, mount_path); mount_path is '' without a pvc.
        :rtype: tuple
        """
        info = self._config.deployment_infos.get(kind, {}).get(component, {})
        data_path = info.get('data_path') or self._config.dockertemplate.get('datadir', '')
        return data_path, info.get('mount_path', '')

    def get_host_volume(self, pod: str = '', mount_path: str = '') -> Tuple:
        """Return (size, used) of the storage volume in the SUT container.

        Asks ``df`` for the filesystem holding ``mount_path``, which works for
        every provisioner (an RBD device has no "volumes" in its df line).
        Without ``mount_path``, uses the SUT's pvc mount path, then its data
        path (:meth:`get_data_paths`), then the first df line matching
        "volumes".

        :param pod: Optional pod name override; defaults to current SUT pod.
        :param mount_path: Optional mount path of the volume inside the pod.
        :return: Tuple (size, used) as human-readable strings.
        :rtype: tuple
        """
        self._config.logger.debug('HostProbe.get_host_volume()')
        if not mount_path:
            data_path, sut_mount_path = self.get_data_paths()
            mount_path = sut_mount_path or data_path
        if mount_path:
            try:
                command = "df -hP " + mount_path
                _, stdout, _ = self._run(command, pod=pod)
                lines = [x for x in stdout.split('\n') if x.strip() != '']
                parts = lines[-1].split() if len(lines) > 1 else []
                # mounted on "/" means the path is not on a volume
                if len(parts) > 5 and parts[-1] != '/':
                    return parts[1], parts[2]
            except Exception as exc:
                logging.error(exc)
        try:
            command = "df -hP | grep volumes"
            _, stdout, _ = self._run(command, pod=pod)
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
            _, stdout, _ = self._run(command)
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
            _, stdout, _ = self._run(command)
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
            _, stdout, _ = self._run(command)
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
            _, stdout, _ = self._run(command)
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
        _, stdout, _ = self._run(command)
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
            _, stdout, _ = self._run(command)
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
        _, stdout, _ = self._run(command)
        return stdout.replace('\n', '')

    def get_host_restarts(self, pod_sut: str = '', counts: Optional[dict] = None) -> str:
        """Return the container restart counts for the SUT pod via kubectl.

        :param pod_sut: Optional pod name override; defaults to current SUT pod.
        :param counts: Restart counts per container if already read
            (``cluster.get_pod_restart_counts()``); then no kubectl call is made.
        :return: Restart count string from kubectl jsonpath output.
        :rtype: str
        """
        self._config.logger.debug('HostProbe.get_host_restarts()')
        if counts:
            return sut_restarts.clean_restart_counts(" ".join(str(count) for count in counts.values()))
        if len(pod_sut) == 0:
            pod_sut = self._config.pod_sut
        result = self._config.experiment.cluster.kubectl(
            'get pods/' + pod_sut + ' -o jsonpath="{.status.containerStatuses[*].restartCount}"')
        return sut_restarts.clean_restart_counts(result)

    def get_host_node(self) -> str:
        """Return the node name the SUT pod is scheduled on.

        :return: Node name string, or empty string on failure.
        :rtype: str
        """
        self._config.logger.debug('HostProbe.get_host_node()')
        pod_object = self._read_pod()
        if pod_object is not None and pod_object.metadata.name == self._config.pod_sut:
            return pod_object.spec.node_name or ""
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
        _, stdout, _ = self._run(command)
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
        _, stdout, _ = self._run(command)
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
        _, stdout, _ = self._run(command)
        return stdout.replace('|', '').replace('\n', '').strip()

    def get_time_diff(self) -> int:
        """Return clock skew in seconds between the SUT pod and the local host.

        Runs ``date +"%s"`` inside the SUT pod and locally, then returns
        ``remote_timestamp - local_timestamp``.

        :return: Clock difference in seconds (positive means remote is ahead).
        :rtype: int
        """
        self._config.logger.debug('HostProbe.get_time_diff()')
        command = 'date +"%s"'
        _, stdout, _ = self._run(command)
        timestamp_remote = stdout
        timestamp_local = os.popen(command).read()
        return int(timestamp_remote) - int(timestamp_local)

    def get_host_diskspace_used_data(self, data_path: str = '') -> int:
        """Return disk space used for database data directory in megabytes.

        :param data_path: Directory to measure; defaults to the SUT's data
            path (:meth:`get_data_paths`).
        :return: Size in megabytes, or 0 on failure or if no data path is known.
        :rtype: int
        """
        self._config.logger.debug('HostProbe.get_host_diskspace_used_data()')
        datadir = data_path or self.get_data_paths()[0]
        if not datadir:
            return 0
        # the first field of du's last line, as awk 'END{print $1}' gave it; no
        # awk, so no '$' that a local shell (kubectl fallback) could expand
        command = "du --block-size=1M -Ls " + datadir
        try:
            _, stdout, _ = self._run(command)
            return int(_field(stdout, -1, 0) or 0)
        except Exception:
            return 0

    def get_host_diskspace_used(self) -> int:
        """Return disk space used on the root filesystem in megabytes.

        :return: Used disk space in megabytes, or 0 on failure.
        :rtype: int
        """
        self._config.logger.debug('HostProbe.get_host_diskspace_used()')
        # the third field of df's second line, as awk 'NR == 2{print $3}' gave it
        command = "df -m /"
        try:
            _, stdout, _ = self._run(command)
            return int(_field(stdout, 1, 2))
        except Exception:
            return 0

    def check_volumes(self, measured: Optional[dict] = None) -> None:
        """Write volume size/used labels to PVCs by probing mounted volumes in pods.

        Iterates over all tracked deployments and stateful sets, calls
        ``get_host_volume()`` per pod, and writes the result as labels on the
        associated PVC via ``kubectl label``. The labels are shown by
        ``bexperiments`` (status of volumes); a label is not written again
        when it already has these values.

        :param measured: ``{pod: (size, used)}`` of SUT pods measured a moment
            ago at the same path (``get_host_all()`` in ``run_pod()``); these
            are not measured again.
        """
        use_storage = self._config.use_storage()
        use_ramdisk = self._config.use_ramdisk()
        if not (use_storage and not use_ramdisk):
            return
        measured = measured or {}
        if 'deployment' in self._config.deployment_infos:
            for component, deployment in self._config.deployment_infos['deployment'].items():
                if 'pvc' not in deployment:
                    continue
                pods = self._config.experiment.cluster.get_pods(
                    component='sut',
                    configuration=self._config.configuration,
                    experiment=self._config.code)
                pvc = deployment['pvc'][0]
                for pod in pods:
                    print("{:30s}: get size via pod {} and write to pvc {}".format(
                        self._config.configuration, pod, pvc))
                    if component == 'sut' and pod in measured:
                        size, used = measured[pod]
                    else:
                        size, used = self.get_host_volume(
                            pod=pod, mount_path=deployment.get('mount_path', ''))
                    self._label_pvc(pvc, size, used)
        if 'statefulset' in self._config.deployment_infos:
            for component, statefulset in self._config.deployment_infos['statefulset'].items():
                for i, pod in enumerate(statefulset['pods']):
                    if 'pvc' not in statefulset:
                        continue
                    pvc = statefulset['pvc'][i]
                    print("{:30s}: get size via pod {} and write to pvc {}".format(
                        self._config.configuration, pod, pvc))
                    size, used = self.get_host_volume(
                        pod=pod, mount_path=statefulset.get('mount_path', ''))
                    self._label_pvc(pvc, size, used)

    def _label_pvc(self, pvc: str, size, used) -> None:
        """Write the volume labels of a PVC, unless this process already wrote these values.

        :param pvc: Name of the PVC.
        :param size: Volume size as ``df -h`` gives it.
        :param used: Used space as ``df -h`` gives it.
        """
        written = self.__dict__.setdefault('_pvc_labels_written', {})
        if written.get(pvc) == (size, used):
            return
        fullcommand = 'label pvc {} --overwrite volume_size="{}" volume_used="{}"'.format(
            pvc, size, used)
        if self._config.experiment.cluster.kubectl(fullcommand) is not None:
            written[pvc] = (size, used)

    def get_host_all(self, component: str = 'sut', kind: str = 'deployment') -> dict:
        """Call all get_host_* probes and return a consolidated dict.

        Runs in ``self._config.pod_sut``; the caller points it at the pod of
        ``component`` first. Data size and volume are taken at that
        component's own data path (:meth:`get_data_paths`), so a worker is
        measured at its own volume, not at the SUT's.

        The values in :data:`STATIC_HOST_INFO` do not change while a pod
        lives; they are measured once per pod UID and then reused. A
        StatefulSet pod keeps its name when it is recreated (possibly on
        another node), hence the UID. Values are only reused if the first
        measurement worked (RAM, CPU, cores, kernel and node found).

        :param component: Component the pod belongs to, e.g. ``sut``, ``pool``, ``tikv``.
        :param kind: ``deployment`` or ``statefulset``.
        :return: Dict of host metrics (RAM, CPU, GPU, Cores, host, node, disk, etc.).
        :rtype: dict
        """
        data_path, mount_path = self.get_data_paths(component, kind)
        pod_object = self._read_pod()
        uid = pod_object.metadata.uid if pod_object is not None else None
        cached = self._static_host_info.get(uid, {}) if uid else {}
        volume = {}

        def volume_value(key):
            if not volume:
                volume['volume_size'], volume['volume_used'] = self.get_host_volume(
                    mount_path=mount_path or data_path)
            return volume[key]

        # in the order of the keys in connections.config
        probes = (
            ('RAM', self.get_host_memory),
            ('CPU', self.get_host_cpu),
            ('GPU', self.get_host_gpus),
            ('GPUIDs', self.get_host_gpu_ids),
            ('Cores', self.get_host_cores),
            ('host', self.get_host_system),
            ('node', self.get_host_node),
            ('disk', self.get_host_diskspace_used),
            ('datadisk', lambda: self.get_host_diskspace_used_data(data_path)),
            ('volume_size', lambda: volume_value('volume_size')),
            ('volume_used', lambda: volume_value('volume_used')),
            ('cuda', self.get_host_cuda),
            ('hugepages_total', self.get_host_hugepages_total),
            ('hugepages_free', self.get_host_hugepages_free),
            ('cpu_list', self.get_host_cpulist),
        )
        server = {}
        for key, probe in probes:
            server[key] = copy.deepcopy(cached[key]) if key in cached else probe()
        server['args'] = self._config.sut_startup_args
        if uid and not cached and all(server[key] for key in ('RAM', 'CPU', 'Cores', 'host', 'node')):
            self._static_host_info[uid] = {key: copy.deepcopy(server[key]) for key in STATIC_HOST_INFO}
        return server
