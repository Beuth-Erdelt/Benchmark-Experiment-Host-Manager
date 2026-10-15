"""
Tests for the 'Volumes of Workers' table of ``bexhoma status``.

StatefulSet PVCs carry the StatefulSet's type as component label (``worker``,
but also ``pd`` and ``tikv`` for TiDB). They are found by their fixed name
prefix ``bxw-``, so all of them are listed, not only ``component=worker``.
"""
import unittest
from types import SimpleNamespace

import pandas as pd

from bexhoma.scripts.experimentsmanager import _statefulset_pvcs, _worker_volumes


def _pvc(name, labels):
    return SimpleNamespace(
        metadata=SimpleNamespace(name=name, labels=labels),
        spec=SimpleNamespace(
            storage_class_name='cephcsi',
            resources=SimpleNamespace(requests={'storage': '10Gi'})),
        status=SimpleNamespace(phase='Bound'),
    )


def _labels(component):
    return {'app': 'bexhoma', 'component': component, 'configuration': 'tidb',
            'experiment': '1234', 'dbms': 'TiDB'}


class StatusWorkerVolumesTest(unittest.TestCase):

    def setUp(self):
        self.pvcs = [
            _pvc('bxw-bexhoma-worker-citus-0', _labels('worker')),
            _pvc('bxw-bexhoma-pd-tidb-0', _labels('pd')),
            _pvc('bxw-bexhoma-tikv-tidb-0', _labels('tikv')),
            _pvc('bexhoma-storage-tidb-1234', _labels('storage')),
            _pvc('bxw-bexhoma-unlabelled-0', None),
        ]

    def test_selects_all_statefulset_pvcs(self):
        names = [pvc.metadata.name for pvc in _statefulset_pvcs(self.pvcs)]
        self.assertEqual(names, [
            'bxw-bexhoma-worker-citus-0',
            'bxw-bexhoma-pd-tidb-0',
            'bxw-bexhoma-tikv-tidb-0',
            'bxw-bexhoma-unlabelled-0',
        ])

    def test_table_lists_pd_and_tikv_with_component(self):
        volumes = _worker_volumes(self.pvcs)
        self.assertEqual(volumes['bxw-bexhoma-pd-tidb-0']['component'], 'pd')
        self.assertEqual(volumes['bxw-bexhoma-tikv-tidb-0']['component'], 'tikv')
        self.assertNotIn('bexhoma-storage-tidb-1234', volumes)

    def test_missing_labels_do_not_raise(self):
        volumes = _worker_volumes(self.pvcs)
        self.assertEqual(volumes['bxw-bexhoma-unlabelled-0']['dbms'], "")
        df = pd.DataFrame(volumes).T
        self.assertEqual(len(df), 4)


if __name__ == '__main__':
    unittest.main()
