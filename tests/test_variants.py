"""
Tests for option-dependent variants of a DBMS entry: ``variants`` in ``cluster.config``.

A variant is ``{'when': <expression>, <entry keys>}``; every variant whose expression holds for
the command line is applied in order (:func:`bexhoma.system_descriptors.effective_entry`). The key-value
systems of YCSB use them for their cluster and replica modes.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import unittest

from bexhoma import system_descriptors as sd

from .test_reset_scripts import _run_script


class EvaluateTest(unittest.TestCase):

    context = {'num_worker': 2, 'num_worker_replicas': 0, 'name': 'x'}

    def test_comparisons_and_logic(self) -> None:
        self.assertTrue(sd.evaluate('num_worker > 0', self.context))
        self.assertFalse(sd.evaluate('num_worker > 0 and num_worker_replicas > 0', self.context))
        self.assertTrue(sd.evaluate('num_worker > 0 or num_worker_replicas > 0', self.context))
        self.assertTrue(sd.evaluate('not num_worker_replicas', self.context))
        self.assertTrue(sd.evaluate("name == 'x' and 0 < num_worker <= 2", self.context))

    def test_arithmetic(self) -> None:
        self.assertEqual(sd.evaluate('num_worker * (1 + num_worker_replicas)', {'num_worker': 3, 'num_worker_replicas': 2}), 9)
        self.assertEqual(sd.evaluate('7 // 2 - 1', {}), 2)

    def test_nothing_else_is_allowed(self) -> None:
        for expression in ('__import__("os")', 'open("x")', '[1]', 'num_worker.real', 'lambda: 1', 'num_worker ** 2'):
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError):
                    sd.evaluate(expression, self.context)

    def test_unknown_name(self) -> None:
        with self.assertRaises(KeyError):
            sd.evaluate('missing > 0', self.context)


class EffectiveEntryTest(unittest.TestCase):

    entry = {
        'reset_scripts': ['a.sh'],
        'loading_parameters': {'TYPE': 'one', 'KEEP': 1},
        'variants': [
            {'when': 'n > 0', 'docker': 'Cluster', 'loading_parameters': {'TYPE': 'cluster'},
             'sut_attributes': {'role': 'placeholder'}},
            {'when': 'n > 0 and r > 0', 'storage_prefix': 'rep', 'loading_parameters': {'TYPE': 'replica'}},
        ],
    }

    def test_no_variant_matches(self) -> None:
        result = sd.effective_entry(self.entry, {'n': 0, 'r': 0})
        self.assertEqual(result, {'reset_scripts': ['a.sh'], 'loading_parameters': {'TYPE': 'one', 'KEEP': 1}})

    def test_one_variant_merges_dicts_and_replaces_the_rest(self) -> None:
        result = sd.effective_entry(self.entry, {'n': 2, 'r': 0})
        self.assertEqual(result['docker'], 'Cluster')
        self.assertEqual(result['loading_parameters'], {'TYPE': 'cluster', 'KEEP': 1})
        self.assertEqual(result['sut_attributes'], {'role': 'placeholder'})
        self.assertNotIn('storage_prefix', result)

    def test_later_variants_win(self) -> None:
        result = sd.effective_entry(self.entry, {'n': 2, 'r': 1})
        self.assertEqual(result['loading_parameters'], {'TYPE': 'replica', 'KEEP': 1})
        self.assertEqual((result['docker'], result['storage_prefix']), ('Cluster', 'rep'))

    def test_the_entry_itself_is_untouched(self) -> None:
        sd.effective_entry(self.entry, {'n': 2, 'r': 1})
        self.assertEqual(self.entry['loading_parameters'], {'TYPE': 'one', 'KEEP': 1})
        self.assertIn('variants', self.entry)

    def test_validation(self) -> None:
        def problems(variants):
            dockers = {'A': {'storage_prefix': 'a', 'template': {'alias': 'a'},
                             'benchmarks': {'x': {'variants': variants}}}}
            return sd.validate_descriptors(dockers, {'x'})
        self.assertEqual(problems([{'when': 'n > 0', 'docker': 'B'}]), [])
        self.assertIn("needs a 'when' expression", problems([{'docker': 'B'}])[0])
        self.assertIn('not allowed in an expression', problems([{'when': 'f(1)'}])[0])
        self.assertIn("unknown key 'colour'", problems([{'when': 'n > 0', 'colour': 'red'}])[0])
        self.assertIn("unknown key 'variants'", problems([{'when': 'n > 0', 'variants': []}])[0])


class KeyValueModesTest(unittest.TestCase):
    """What the key-value systems of YCSB build for the single node, cluster and replica modes."""

    def configs(self, *argv):
        _, configurations = _run_script('ycsb.py', *argv)
        return {c.docker if c.docker in ('Cassandra', 'CassandraCluster') else c.configuration.split('-')[0]: c
                for c in configurations}

    def one(self, dbms, *argv):
        _, configurations = _run_script('ycsb.py', '-dbms', dbms, *argv)
        self.assertEqual(len(configurations), 1)
        return configurations[0]

    def test_single_node(self) -> None:
        for dbms, storage in (('Dragonfly', 'dragonfly'), ('Redis', 'redis'), ('Valkey', 'valkey'), ('Garnet', 'garnet')):
            with self.subTest(dbms=dbms):
                config = self.one(dbms)
                self.assertEqual((config.docker, config.num_worker, config.storage['storageConfiguration']), (dbms, 0, storage))
                self.assertEqual(config.loading_parameters['BEXHOMA_DBMS_TYPE'], 'redis')
                self.assertTrue(config.monitoring_sut)
                self.assertEqual(config.sut_role, 'data')   # the SUT holds the data itself (a cluster has a placeholder)

    def test_cluster_mode(self) -> None:
        for dbms, docker in (('Dragonfly', 'DragonflyCluster'), ('Redis', 'Redis'), ('Valkey', 'Valkey'), ('Garnet', 'Garnet')):
            with self.subTest(dbms=dbms):
                config = self.one(dbms, '-nw', '3')
                self.assertEqual((config.docker, config.num_worker), (docker, 3))
                self.assertEqual(config.loading_parameters['BEXHOMA_DBMS_TYPE'], 'redis-cluster')
                self.assertFalse(config.monitoring_sut)
                self.assertEqual((config.sut_role, config.script_target), ('placeholder', 'workers'))
        self.assertEqual(self.one('Redis', '-nw', '3').sut_template, 'deploymenttemplate-RedisCluster.yml')

    def test_replicas_multiply_the_pods_of_redis_like_systems_only(self) -> None:
        self.assertEqual(self.one('Redis', '-nw', '3', '-nwr', '2').num_worker, 9)
        self.assertEqual(self.one('Valkey', '-nw', '3', '-nwr', '2').num_worker, 9)
        self.assertEqual(self.one('Dragonfly', '-nw', '3', '-nwr', '2').num_worker, 3)

    def test_dragonfly_replica_mode(self) -> None:
        config = self.one('Dragonfly', '-nw', '3', '-nwr', '1')
        self.assertEqual(config.docker, 'DragonflyCluster')
        self.assertEqual(config.sut_template, 'deploymenttemplate-DragonflyReplica.yml')
        self.assertEqual(config.storage['storageConfiguration'], 'dfr')
        # worker-0 is the master: a plain client, not the cluster aware one
        self.assertEqual(config.loading_parameters['BEXHOMA_DBMS_TYPE'], 'redis')
        cluster = self.one('Dragonfly', '-nw', '3')
        self.assertEqual(cluster.storage['storageConfiguration'], 'dragonfly')
        self.assertEqual(cluster.loading_parameters['BEXHOMA_DBMS_TYPE'], 'redis-cluster')

    def test_the_scripts_stay_in_the_folder_of_the_dbms(self) -> None:
        self.assertEqual(self.one('Dragonfly', '-nw', '2').path_experiment_docker, 'Dragonfly')
        self.assertEqual(self.one('Cassandra', '-nw', '2').path_experiment_docker, 'Cassandra')
        self.assertEqual(self.one('Cassandra', '-nw', '2').docker, 'CassandraCluster')
        self.assertEqual(self.one('Cassandra').docker, 'Cassandra')

    def test_benchmarking_rounds_carry_the_client_type_of_the_mode(self) -> None:
        for argv, expected in (((), 'redis'), (('-nw', '2'), 'redis-cluster')):
            with self.subTest(argv=argv):
                config = self.one('Redis', *argv)
                rounds = [entry for client_round in config.experiment_dict['benchmarker'] for entry in client_round]
                self.assertTrue(rounds)
                for entry in rounds:
                    self.assertEqual(entry['parameters']['BEXHOMA_DBMS_TYPE'], expected)


if __name__ == '__main__':
    unittest.main()
