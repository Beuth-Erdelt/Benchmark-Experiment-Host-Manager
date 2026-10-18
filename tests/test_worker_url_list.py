"""Tests for the worker host list in JDBC URLs (``BEXHOMA_URL_LIST``).

YCSB on Citus connected only to workers 0 and 1: the list
``w0,w1,w2:9091`` gave the first two the driver's default port and the last
one the SUT service port, which the headless worker service does not have.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import ast
import unittest
from pathlib import Path

from bexhoma.configurations.manifest import worker_url_list

__all__ = []

_TEMPLATE = 'jdbc:postgresql://{serverip}:9091/{database}?loadBalanceHosts=true'
_WORKERS = ['w-0.w', 'w-1.w', 'w-2.w']


class WorkerUrlListTest(unittest.TestCase):

    def test_every_host_gets_the_worker_port(self) -> None:
        self.assertEqual(worker_url_list(_TEMPLATE, _WORKERS, 5432, database='postgres'),
                         'jdbc:postgresql://w-0.w:5432,w-1.w:5432,w-2.w:5432/postgres?loadBalanceHosts=true')

    def test_without_worker_port_as_before(self) -> None:
        self.assertEqual(worker_url_list(_TEMPLATE, _WORKERS, None, database='postgres'),
                         'jdbc:postgresql://w-0.w,w-1.w,w-2.w:9091/postgres?loadBalanceHosts=true')

    def test_template_without_port(self) -> None:
        self.assertEqual(worker_url_list('jdbc:x://{serverip}/db', _WORKERS[:1], 5432), 'jdbc:x://w-0.w:5432/db')

    def test_citus_config(self) -> None:
        config = ast.literal_eval((Path(__file__).resolve().parent.parent / 'k8s-cluster.config').read_text(encoding='utf-8'))
        citus = config['dockers']['Citus']
        url = worker_url_list(citus['template']['JDBC']['url'], _WORKERS, citus.get('worker_port'))
        self.assertTrue(url.startswith('jdbc:postgresql://w-0.w:5432,w-1.w:5432,w-2.w:5432/postgres'))


if __name__ == '__main__':
    unittest.main()
