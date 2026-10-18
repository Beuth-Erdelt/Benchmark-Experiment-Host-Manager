"""Tests for the reduced cluster-call overhead (dev/plan-fewer-kubectl-calls.md).

Each test checks that a merged, cached or rerouted call gives the same result
as before and keeps its fallback: token refresh throttling (M14), call
counting (M0), pod reads through the API (M9), exec through the API (M7),
host probes (M7, M8), uploads (M1, M13), Redis (M2), volume labels (M3),
stored job pods (M10) and the follow-up waits of the main loop (M11).

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

from kubernetes import client as k8s
from kubernetes.client.rest import ApiException

from bexhoma import clusters
from bexhoma.cluster_calls import (
    CallStats, ThrottledTokenRefresh, TOKEN_EXPIRY_MARGIN_SECONDS, TOKEN_REFRESH_SECONDS,
    stored_pods, token_expiry,
)
from bexhoma.clusters import Kubernetes, POD_NOT_READ
from bexhoma.configurations.host import HostProbe, STATIC_HOST_INFO, _field
from bexhoma.experiments.base import ExperimentBase, MAX_FOLLOW_UP_WAITS_IN_A_ROW

__all__ = []

_SH_CANDIDATES = [shutil.which('sh'), r'C:\Program Files\SmartGit\git\usr\bin\sh.exe',
                  r'C:\Program Files\Git\usr\bin\sh.exe']
_SH = next((c for c in _SH_CANDIDATES if c and os.path.isfile(c)), None)


def _bare_cluster() -> Kubernetes:
    """Build a cluster object without reading a config or contacting a cluster."""
    cluster = Kubernetes.__new__(Kubernetes)
    cluster.context = 'test'
    cluster.namespace = 'benchmarks'
    cluster.appname = 'bexhoma'
    cluster.logger = mock.Mock()
    cluster.wait = mock.Mock()
    return cluster


def _jwt(exp: float) -> str:
    """An unsigned JWT with an ``exp`` claim."""
    def part(data: dict) -> str:
        return base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip('=')
    return 'Bearer ' + '.'.join([part({'alg': 'none'}), part({'exp': exp}), 'signature'])


def _pod(name='sut-0', app='bexhoma', phase='Running', uid='uid-1', node='cl-worker1',
         containers=('dbms', 'monitor'), init_containers=(), restarts=(0, 2), waiting=(None, None),
         init_waiting=()):
    """A V1Pod as the API returns it."""
    statuses = [
        k8s.V1ContainerStatus(
            name=container, image='i', image_id='i', ready=True, restart_count=count,
            state=k8s.V1ContainerState(waiting=k8s.V1ContainerStateWaiting(reason=reason) if reason else None))
        for container, count, reason in zip(containers, restarts, waiting)]
    init_statuses = [
        k8s.V1ContainerStatus(
            name=container, image='i', image_id='i', ready=False, restart_count=0,
            state=k8s.V1ContainerState(waiting=k8s.V1ContainerStateWaiting(reason=reason) if reason else None))
        for container, reason in zip(init_containers, init_waiting)]
    return k8s.V1Pod(
        metadata=k8s.V1ObjectMeta(name=name, uid=uid, labels={'app': app}),
        spec=k8s.V1PodSpec(
            node_name=node,
            containers=[k8s.V1Container(name=container) for container in containers],
            init_containers=[k8s.V1Container(name=container) for container in init_containers] or None),
        status=k8s.V1PodStatus(phase=phase, container_statuses=statuses,
                               init_container_statuses=init_statuses or None))


class TokenRefreshTest(unittest.TestCase):
    """M14: the client's refresh hook runs about once a minute, not per request."""

    def setUp(self) -> None:
        self.now = [1000.0]
        self.hook = mock.Mock()
        self.refresh = ThrottledTokenRefresh(self.hook, clock=lambda: self.now[0])
        self.configuration = SimpleNamespace(api_key={'authorization': _jwt(1000.0 + 300)})

    def test_passes_the_hook_on_once_for_many_requests(self) -> None:
        for _ in range(5):
            self.refresh(self.configuration)
        self.assertEqual(self.hook.call_count, 1)

    def test_passes_it_on_again_after_the_refresh_interval(self) -> None:
        self.refresh(self.configuration)
        self.now[0] += TOKEN_REFRESH_SECONDS - 1
        self.refresh(self.configuration)
        self.assertEqual(self.hook.call_count, 1)
        self.now[0] += 1
        self.refresh(self.configuration)
        self.assertEqual(self.hook.call_count, 2)

    def test_passes_it_on_when_the_token_is_about_to_expire(self) -> None:
        self.refresh(self.configuration)
        self.configuration.api_key['authorization'] = _jwt(self.now[0] + TOKEN_EXPIRY_MARGIN_SECONDS - 1)
        self.refresh(self.configuration)
        self.assertEqual(self.hook.call_count, 2)

    def test_stays_in_front_when_the_client_registers_its_hook_again(self) -> None:
        configuration = SimpleNamespace(api_key={'authorization': _jwt(1000.0 + 300)})
        calls = []

        def client_hook(conf):
            # as kube_config._set_config(): reload and register a new hook
            calls.append(1)
            conf.refresh_api_key_hook = client_hook

        refresh = ThrottledTokenRefresh(client_hook, clock=lambda: self.now[0])
        configuration.refresh_api_key_hook = refresh
        for _ in range(3):
            configuration.refresh_api_key_hook(configuration)
        self.assertIs(configuration.refresh_api_key_hook, refresh)
        self.assertEqual(len(calls), 1)

    def test_reads_the_expiry_of_a_jwt_only(self) -> None:
        self.assertEqual(token_expiry(_jwt(1234.0)), 1234.0)
        self.assertIsNone(token_expiry('Bearer opaque-token'))
        self.assertIsNone(token_expiry(None))
        self.assertIsNone(token_expiry('Bearer a.!!!.c'))

    def test_api_clients_get_the_throttled_hook(self) -> None:
        def load(context=None, client_configuration=None):
            client_configuration.host = 'http://127.0.0.1:1'
            client_configuration.refresh_api_key_hook = mock.Mock()

        cluster = _bare_cluster()
        with mock.patch.object(clusters.kubernetes_config, 'load_kube_config', side_effect=load):
            api_client = cluster._new_api_client()
        self.assertIsInstance(api_client.configuration.refresh_api_key_hook, ThrottledTokenRefresh)


class CallStatsTest(unittest.TestCase):
    """M0: calls are counted and described."""

    def test_describes_the_calls_since_a_snapshot(self) -> None:
        stats = CallStats()
        stats.record_kubectl(1.0)
        before = stats.snapshot()
        stats.record_kubectl(1.5)
        stats.record_kubectl(1.5)
        stats.record_api(0.25)
        self.assertEqual(stats.since(before), "2 kubectl calls 3.0s, 1 API requests 0.2s")


class ReadPodTest(unittest.TestCase):
    """M9: one pod read instead of kubectl jsonpath calls or listing all pods."""

    def setUp(self) -> None:
        self.cluster = _bare_cluster()
        self.cluster.v1core = mock.Mock()
        self.cluster.kubectl = mock.Mock(side_effect=AssertionError('no kubectl expected'))

    def test_status_of_a_pod(self) -> None:
        self.cluster.v1core.read_namespaced_pod.return_value = _pod(phase='Succeeded')
        self.assertEqual(self.cluster.get_pod_status('sut-0'), 'Succeeded')
        self.cluster.v1core.list_namespaced_pod.assert_not_called()

    def test_pod_of_another_app_or_gone_counts_as_not_found(self) -> None:
        self.cluster.v1core.read_namespaced_pod.return_value = _pod(app='other')
        self.assertEqual(self.cluster.get_pod_status('sut-0'), '')
        self.cluster.v1core.read_namespaced_pod.side_effect = ApiException(status=404)
        self.assertEqual(self.cluster.get_pod_status('sut-0'), '')
        self.assertEqual(self.cluster.get_pod_containers('sut-0'), [])
        self.assertEqual(self.cluster.get_pod_restart_counts('sut-0'), {})
        self.assertEqual(self.cluster.get_pod_waiting_reasons('sut-0'), [])

    def test_containers_restarts_and_waiting_reasons(self) -> None:
        self.cluster.v1core.read_namespaced_pod.return_value = _pod(
            init_containers=('init',), init_waiting=('PodInitializing',),
            waiting=(None, 'ImagePullBackOff'))
        self.assertEqual(self.cluster.get_pod_containers('sut-0'), ['dbms', 'monitor', 'init'])
        self.assertEqual(self.cluster.get_pod_restart_counts('sut-0'), {'dbms': 0, 'monitor': 2})
        self.assertEqual(self.cluster.get_pod_waiting_reasons('sut-0'), ['PodInitializing', 'ImagePullBackOff'])

    def test_falls_back_to_kubectl_when_the_api_keeps_failing(self) -> None:
        self.cluster.v1core.read_namespaced_pod.side_effect = ApiException(status=500)
        self.cluster.cluster_access = mock.Mock()
        self.cluster.kubectl = mock.Mock(side_effect=['dbms', ''])
        with mock.patch('builtins.print'):
            self.assertEqual(self.cluster.get_pod_containers('sut-0'), ['dbms'])
        self.assertEqual(self.cluster.v1core.read_namespaced_pod.call_count, 3)

    def test_without_api_client_nothing_is_read(self) -> None:
        cluster = _bare_cluster()
        self.assertIs(cluster._read_pod('sut-0'), POD_NOT_READ)


class StatefulSetPodsTest(unittest.TestCase):
    """get_stateful_set_pods() finds the pods of a StatefulSet bexhoma did not create."""

    def setUp(self) -> None:
        self.cluster = _bare_cluster()
        self.cluster.v1apps = mock.Mock()
        self.cluster.v1core = mock.Mock()
        self.cluster.v1apps.read_namespaced_stateful_set.return_value = k8s.V1StatefulSet(
            spec=k8s.V1StatefulSetSpec(
                selector=k8s.V1LabelSelector(match_labels={'app': 'yb-tserver', 'release': 'yb'}),
                service_name='yb-tservers', template=k8s.V1PodTemplateSpec()))
        self.cluster.v1core.list_namespaced_pod.return_value = k8s.V1PodList(items=[
            _pod(name=name) for name in ('yb-tserver-10', 'yb-tserver-2', 'yb-tserver-0', 'yb-tserver-x')])

    def test_pods_by_the_stateful_sets_selector_in_ordinal_order(self) -> None:
        self.assertEqual(self.cluster.get_stateful_set_pods('yb-tserver'),
                         ['yb-tserver-0', 'yb-tserver-2', 'yb-tserver-10'])
        self.assertEqual(self.cluster.v1core.list_namespaced_pod.call_args.kwargs['label_selector'],
                         'app=yb-tserver,release=yb')

    def test_missing_stateful_set_gives_no_pods(self) -> None:
        self.cluster.v1apps.read_namespaced_stateful_set.side_effect = ApiException(status=404)
        self.assertEqual(self.cluster.get_stateful_set_pods('yb-tserver'), [])
        self.assertEqual(self.cluster.get_stateful_set_pods(''), [])

    def test_worker_pods_use_the_components_own_stateful_set(self) -> None:
        from bexhoma.configurations.base import SutConfiguration
        cluster = mock.Mock()
        cluster.get_stateful_set_pods.side_effect = lambda name: [f'{name}-0']
        config = SimpleNamespace(
            statefulset_name='yb-tserver', experiment=SimpleNamespace(cluster=cluster),
            deployment_infos={'statefulset': {'yb-tserver': {'name': 'yb-tserver'},
                                              'yb-master': {'name': 'yb-master'}}})
        self.assertEqual(SutConfiguration.get_worker_pods(config, component='yb-master'), ['yb-master-0'])
        self.assertEqual(SutConfiguration.get_worker_pods(config, component='yb-tserver'), ['yb-tserver-0'])
        self.assertEqual(SutConfiguration.get_worker_pods(config), ['yb-tserver-0'])


class _FakeStream:
    """A finished ``WSClient`` with the given output."""

    def __init__(self, stdout='', stderr='', still_open=False):
        self.stdout, self.stderr, self.still_open = stdout, stderr, still_open
        self.closed = False

    def run_forever(self, timeout=None):
        pass

    def is_open(self):
        return self.still_open

    def read_stdout(self):
        return self.stdout

    def read_stderr(self):
        return self.stderr

    def close(self):
        self.closed = True


class ExecApiTest(unittest.TestCase):
    """M7: exec through the Python client, with kubectl as fallback."""

    def setUp(self) -> None:
        self.cluster = _bare_cluster()
        self.cluster.v1exec = mock.Mock()
        self.cluster.execute_command_in_pod = mock.Mock(return_value=('', 'from kubectl', ''))

    def test_runs_the_command_without_a_local_shell(self) -> None:
        stream = _FakeStream(stdout='9\t/etc\n', stderr='warning\n')
        with mock.patch.object(clusters, 'kubernetes_stream', return_value=stream) as run:
            result = self.cluster.execute_command_in_pod_api("du -Ls /etc | awk '{print $1}'", pod='p', container='dbms')
        self.assertEqual(result, ('', '9\t/etc\n', 'warning\n'))
        self.assertEqual(run.call_args.kwargs['command'], ['sh', '-c', "du -Ls /etc | awk '{print $1}'"])
        self.assertEqual(run.call_args.kwargs['container'], 'dbms')
        self.assertTrue(stream.closed)
        self.cluster.execute_command_in_pod.assert_not_called()

    def test_falls_back_to_kubectl_on_any_failure(self) -> None:
        failures = [ApiException(status=0, reason='Handshake status 404 Not Found'),
                    ConnectionResetError('reset'), _FakeStream(still_open=True)]
        for failure in failures:
            side_effect = failure if isinstance(failure, Exception) else None
            with mock.patch.object(clusters, 'kubernetes_stream', side_effect=side_effect,
                                   return_value=failure):
                self.assertEqual(self.cluster.execute_command_in_pod_api('uname -r', pod='p'),
                                 ('', 'from kubectl', ''))
        self.assertEqual(self.cluster.execute_command_in_pod.call_count, 3)

    def test_renews_a_rejected_token_once(self) -> None:
        self.cluster.cluster_access = mock.Mock()
        rejected = ApiException(status=0, reason='Handshake status 401 Unauthorized')
        with mock.patch.object(clusters, 'kubernetes_stream',
                               side_effect=[rejected, _FakeStream(stdout='ok')]), \
                mock.patch('builtins.print'):
            self.assertEqual(self.cluster.execute_command_in_pod_api('uname -r', pod='p'), ('', 'ok', ''))
        self.cluster.cluster_access.assert_called_once_with()

    def test_without_client_kubectl_runs_it(self) -> None:
        self.cluster.v1exec = None
        self.assertEqual(self.cluster.execute_command_in_pod_api('uname -r', pod='p'), ('', 'from kubectl', ''))


def _probe(outputs: dict, pod_object=None):
    """A HostProbe whose commands answer from ``outputs`` (command prefix -> stdout)."""
    commands = []

    def run(command='', pod='', **_):
        commands.append(command)
        for prefix, stdout in outputs.items():
            if command.startswith(prefix):
                return '', stdout, ''
        return '', '', ''

    cluster = SimpleNamespace(_read_pod=lambda pod: pod_object if pod_object is not None else POD_NOT_READ,
                              kubectl=mock.Mock(return_value=''))
    config = SimpleNamespace(
        logger=mock.Mock(), pod_sut='sut-0', execute_command_in_pod_sut=run,
        experiment=SimpleNamespace(cluster=cluster), sut_startup_args=['-c', 'x'],
        deployment_infos={'deployment': {'sut': {'data_path': '/data', 'mount_path': '/data'}}},
        dockertemplate={}, use_storage=lambda: True, use_ramdisk=lambda: False)
    return HostProbe(config), commands


_HOST_OUTPUTS = {
    'grep MemTotal': '2113450364\n',
    'more /proc/cpuinfo': 'model name\t: INTEL(R) XEON(R) PLATINUM 8570\n',
    'grep -c ^processor': '224\n',
    'uname -r': '6.8.0-137-generic\n',
    'df -m /': 'Filesystem     1M-blocks   Used Available Use% Mounted on\noverlay 1800943 856817 852572  51% /\n',
    'du --block-size=1M': '1234\t/data\n',
    'df -hP /data': 'Filesystem Size Used Avail Use% Mounted on\n/dev/rbd0 100G 55G 46G 55% /data\n',
    'cat /proc/meminfo | grep HugePages_Total': 'HugePages_Total:       0\n',
    'cat /proc/meminfo | grep HugePages_Free': 'HugePages_Free:        0\n',
    'grep ^Cpus_allowed_list': '0-223\n',
}


class HostProbeTest(unittest.TestCase):
    """M7/M8: same host info, fewer calls."""

    def test_field_matches_awk(self) -> None:
        df = _HOST_OUTPUTS['df -m /']
        self.assertEqual(_field(df, 1, 2), '856817')          # awk 'NR == 2{print $3}'
        self.assertEqual(_field('9\t/etc\n', -1, 0), '9')     # awk 'END{print $1}'
        self.assertEqual(_field('', -1, 0), '')
        self.assertEqual(_field('only one line\n', 1, 2), '')

    def test_disk_values_parsed_without_awk(self) -> None:
        probe, commands = _probe(_HOST_OUTPUTS)
        self.assertEqual(probe.get_host_diskspace_used(), 856817)
        self.assertEqual(probe.get_host_diskspace_used_data('/data'), 1234)
        self.assertEqual(commands, ['df -m /', 'du --block-size=1M -Ls /data'])
        self.assertFalse(any('$' in command for command in commands))

    def test_failed_disk_probes_give_zero(self) -> None:
        probe, _ = _probe({})
        self.assertEqual(probe.get_host_diskspace_used(), 0)
        self.assertEqual(probe.get_host_diskspace_used_data('/data'), 0)

    def test_host_info_once_per_pod_uid(self) -> None:
        pod = _pod(uid='uid-1', node='cl-worker7')
        probe, commands = _probe(_HOST_OUTPUTS, pod)
        first = probe.get_host_all()
        self.assertEqual(list(first), ['RAM', 'CPU', 'GPU', 'GPUIDs', 'Cores', 'host', 'node', 'disk',
                                       'datadisk', 'volume_size', 'volume_used', 'cuda', 'hugepages_total',
                                       'hugepages_free', 'cpu_list', 'args'])
        self.assertEqual(first['node'], 'cl-worker7')
        self.assertEqual(first['datadisk'], 1234)
        self.assertEqual((first['volume_size'], first['volume_used']), ('100G', '55G'))
        self.assertEqual(sum(command.startswith("nvidia-smi | grep") for command in commands), 1, 'cuda once')
        commands.clear()
        second = probe.get_host_all()
        self.assertEqual(second, first)
        self.assertEqual(commands, ['df -m /', 'du --block-size=1M -Ls /data', 'df -hP /data',
                                    'cat /proc/meminfo | grep HugePages_Free'])
        # a recreated pod (same name, new uid) is measured again
        pod.metadata.uid = 'uid-2'
        commands.clear()
        probe.get_host_all()
        self.assertIn('uname -r', commands)
        self.assertEqual(set(STATIC_HOST_INFO) - set(first), set())

    def test_failed_first_measurement_is_not_reused(self) -> None:
        probe, commands = _probe({'df -m /': _HOST_OUTPUTS['df -m /']}, _pod(uid='uid-1'))
        probe.get_host_all()
        commands.clear()
        probe.get_host_all()
        self.assertIn('uname -r', commands)

    def test_volume_labels_reuse_the_measurement_and_skip_unchanged_values(self) -> None:
        probe, commands = _probe(_HOST_OUTPUTS)
        probe._config.configuration = 'PostgreSQL-1'
        probe._config.code = '42'
        probe._config.deployment_infos['deployment']['sut']['pvc'] = ['pvc-1']
        probe._config.experiment.cluster.get_pods = mock.Mock(return_value=['sut-0'])
        probe._config.experiment.cluster.kubectl = mock.Mock(return_value='labeled')
        with mock.patch('builtins.print'):
            probe.check_volumes(measured={'sut-0': ('100G', '55G')})
            probe.check_volumes()
        self.assertEqual(commands, ['df -hP /data'])
        probe._config.experiment.cluster.kubectl.assert_called_once_with(
            'label pvc pvc-1 --overwrite volume_size="100G" volume_used="55G"')

    def test_restarts_from_already_read_counts(self) -> None:
        probe, _ = _probe({})
        self.assertEqual(probe.get_host_restarts('sut-0', counts={'dbms': 1, 'monitor': 0}), '1 0')
        probe._config.experiment.cluster.kubectl.assert_not_called()


class UploadTest(unittest.TestCase):
    """M1: fewer calls per upload, same atomic rename and check."""

    def setUp(self) -> None:
        self.cluster = _bare_cluster()
        self.execs = []
        self.exec_stdout = 'UPLOAD_OK'

        def execute(command='', pod='', container=''):
            self.execs.append(command)
            return '', self.exec_stdout if 'UPLOAD_OK' in command else '', ''

        self.cluster.execute_command_in_pod = execute
        self.cluster.kubectl = mock.Mock(return_value='')
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.files = []
        for name in ('queries.config', 'c.config', 'protocol.json'):
            path = os.path.join(self.tmp.name, name)
            with open(path, 'w') as f:
                f.write(name)
            self.files.append(path)

    def test_single_file_creates_the_directory_once_and_checks_the_rename(self) -> None:
        self.cluster.upload_file('/results/42/a', self.files[0], pod='dash')
        self.cluster.upload_file('/results/42/b', self.files[1], pod='dash')
        self.assertEqual(self.execs, [
            "mkdir -p '/results/42'",
            "mv '/results/42/a.uploadtmp' '/results/42/a' && test -s '/results/42/a' && echo UPLOAD_OK",
            "mv '/results/42/b.uploadtmp' '/results/42/b' && test -s '/results/42/b' && echo UPLOAD_OK",
        ])

    def test_single_file_retry_creates_the_directory_again(self) -> None:
        self.exec_stdout = ''
        with mock.patch('builtins.print'), self.assertRaises(RuntimeError):
            self.cluster.upload_file('/results/42/a', self.files[0], pod='dash', max_retries=2)
        self.assertEqual(sum(command.startswith('mkdir') for command in self.execs), 2)

    def test_several_files_in_one_copy_and_one_exec(self) -> None:
        self.cluster.upload_files(self.files, '/results/42', pod='dash')
        self.assertEqual(self.cluster.kubectl.call_count, 1)
        copy = self.cluster.kubectl.call_args.args[0]
        self.assertIn(':/results/42/.upload-', copy)
        self.assertEqual(len(self.execs), 2)       # mkdir, then rename + check
        command = self.execs[1]
        staging = command.split("'")[1].rsplit('/', 1)[0]
        for name in ('queries.config', 'c.config', 'protocol.json'):
            self.assertIn(f"mv '{staging}/{name}' '/results/42/{name}'", command)
            self.assertIn(f"test -s '/results/42/{name}'", command)
        self.assertTrue(command.endswith("&& echo UPLOAD_OK"))
        self.assertIn(f"rmdir '{staging}'", command)

    def test_several_files_failed_attempt_is_cleaned_up_and_repeated(self) -> None:
        self.exec_stdout = ''
        with mock.patch('builtins.print'), self.assertRaises(RuntimeError):
            self.cluster.upload_files(self.files, '/results/42', pod='dash', max_retries=2)
        self.assertEqual(self.cluster.kubectl.call_count, 2)
        self.assertEqual(sum(command.startswith("rm -rf '/results/42/.upload-") for command in self.execs), 2)

    def test_missing_local_file_raises_like_upload_file(self) -> None:
        with self.assertRaises(RuntimeError):
            self.cluster.upload_files([self.files[0], os.path.join(self.tmp.name, 'missing')], '/results/42', pod='dash')


class RedisTest(unittest.TestCase):
    """M2: pod configs and counters in one MSET."""

    def setUp(self) -> None:
        self.cluster = _bare_cluster()
        self.cluster.get_pods = mock.Mock(return_value=['redis-0'])
        self.cluster.execute_command_in_pod_api = mock.Mock(return_value=('', 'OK\n', ''))
        self.cluster.execute_command_in_pod = mock.Mock(return_value=('', 'OK\n', ''))
        self.values = {'q-config-1': {'SF': "1'0", 'NAME': 'a "b"'}, 'q-podcount': 2}

    def test_one_mset_for_all_keys(self) -> None:
        self.cluster.set_redis_values(self.values)
        command = self.cluster.execute_command_in_pod_api.call_args.kwargs['command']
        self.assertTrue(command.startswith('redis-cli mset q-config-1 '))
        self.assertTrue(command.endswith(" q-podcount '2'"))
        self.cluster.execute_command_in_pod.assert_not_called()

    def test_unconfirmed_mset_sets_every_key_on_its_own(self) -> None:
        self.cluster.execute_command_in_pod_api.return_value = ('', '', 'error')
        with mock.patch('builtins.print'):
            self.cluster.set_redis_values(self.values)
        commands = [call.kwargs['command'] for call in self.cluster.execute_command_in_pod.call_args_list]
        self.assertEqual(len(commands), 2)
        self.assertTrue(commands[0].startswith('redis-cli set q-config-1 '))

    @unittest.skipUnless(_SH, 'no sh found')
    def test_json_survives_the_quoting(self) -> None:
        self.cluster.set_redis_values({'k': self.values['q-config-1']})
        command = self.cluster.execute_command_in_pod_api.call_args.kwargs['command']
        argv = command.replace('redis-cli mset ', 'printf "%s\\n" ', 1)
        output = subprocess.run([_SH, '-c', argv], capture_output=True, text=True).stdout.splitlines()
        self.assertEqual(output[0], 'k')
        self.assertEqual(json.loads(output[1]), self.values['q-config-1'])

    def test_pod_configs_as_before(self) -> None:
        from bexhoma.configurations.base import SutConfiguration
        configs = SutConfiguration._pod_configs('q', 2, {'A': 1}, [{'B': 2}])
        self.assertEqual(configs, {'q-config-1': {'A': 1, 'B': 2}, 'q-config-2': {'A': 1}})


def _experiment() -> ExperimentBase:
    experiment = ExperimentBase.__new__(ExperimentBase)
    experiment.cluster = mock.Mock()
    experiment.cluster.__dict__['_stored_pods'] = set()
    return experiment


class LoopTest(unittest.TestCase):
    """M10/M11/M13: fewer inspections, short waits only after own steps, one upload."""

    def test_finished_pod_is_remembered_only_when_all_files_exist(self) -> None:
        experiment = _experiment()
        cluster = experiment.cluster
        cluster.get_pod_containers.return_value = ['dbmsbenchmarker', '']
        cluster.pod_log_exists.return_value = False
        cluster.pod_description_exists.return_value = False
        experiment._store_finished_job_pod('job', 'pod-1')
        self.assertNotIn('pod-1', stored_pods(cluster))
        cluster.pod_log_exists.return_value = True
        cluster.pod_description_exists.return_value = True
        experiment._store_finished_job_pod('job', 'pod-1')
        self.assertIn('pod-1', stored_pods(cluster))
        cluster.get_pod_containers.reset_mock()
        experiment._store_finished_job_pod('job', 'pod-1')
        cluster.get_pod_containers.assert_not_called()
        cluster.store_pod_log.assert_called_with('pod-1', 'dbmsbenchmarker')

    def test_follow_up_waits_are_capped(self) -> None:
        experiment = _experiment()
        self.assertEqual(experiment._follow_up_wait(30, 'job ended'), 0)
        experiment._follow_up_waits_in_a_row = MAX_FOLLOW_UP_WAITS_IN_A_ROW
        self.assertEqual(experiment._follow_up_wait(30, 'job ended'), 30)

    def test_ended_jobs_are_remembered(self) -> None:
        experiment = _experiment()
        experiment._ended_jobs().add('job-1')
        self.assertIn('job-1', experiment._ended_jobs())

    def test_files_of_ended_jobs_in_one_upload(self) -> None:
        experiment = _experiment()
        experiment.upload_experiment_files = mock.Mock()
        experiment.upload_experiment_file = mock.Mock()
        experiment._upload_ended_job_files(['a.config', 'connections.config', 'b.config', 'connections.config'])
        experiment.upload_experiment_files.assert_called_once_with(['a.config', 'connections.config', 'b.config'])
        experiment.upload_experiment_file.assert_not_called()

    def test_failed_joint_upload_goes_file_by_file(self) -> None:
        experiment = _experiment()
        experiment.upload_experiment_files = mock.Mock(side_effect=RuntimeError('cp failed'))
        experiment.upload_experiment_file = mock.Mock(side_effect=[RuntimeError('a'), ''])
        with mock.patch('builtins.print'):
            experiment._upload_ended_job_files(['a.config', 'connections.config'])
        self.assertEqual(experiment.upload_experiment_file.call_count, 2)
        experiment.upload_experiment_file = mock.Mock(side_effect=RuntimeError('connections'))
        with mock.patch('builtins.print'), self.assertRaises(RuntimeError):
            experiment._upload_ended_job_files(['connections.config'])

    def test_end_benchmarking_collects_its_uploads(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        job = 'bexhoma-benchmarker-postgresql-1-42-1-1'
        with open(os.path.join(tmp.name, f'{job}-pod.dbmsbenchmarker.log'), 'w') as f:
            f.write('BEXHOMA_START:100\nBEXHOMA_END:200\n')
        with open(os.path.join(tmp.name, 'conn.config'), 'w') as f:
            f.write(str([{'name': 'conn', 'hostsystem': {}}]))
        experiment = _experiment()
        experiment.path = tmp.name
        experiment.code = '42'
        experiment.monitoring_active = False
        experiment.benchmarks = []
        experiment.evaluator = mock.Mock()
        experiment.upload_experiment_file = mock.Mock()
        experiment.cluster.get_jobs_labels.return_value = {job: {'start_time': '90', 'connection': 'conn'}}
        experiment.cluster.get_pods.return_value = ['dashboard-pod']
        config = SimpleNamespace(benchmarking_timespans=None, benchmark=None)
        pending = []
        with mock.patch('builtins.print'):
            experiment.end_benchmarking(job, config, pending_uploads=pending)
        self.assertEqual(pending, ['conn.config'])
        experiment.upload_experiment_file.assert_not_called()
        self.assertEqual(config.benchmarking_timespans, {'benchmarker': [(100, 200)]})


if __name__ == '__main__':
    unittest.main()
