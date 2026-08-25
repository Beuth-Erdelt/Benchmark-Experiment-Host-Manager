"""
Unit tests for :mod:`bexhoma.environment`.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import unittest
from unittest import mock

from bexhoma import environment


class BuildEnvironmentVersionFieldTest(unittest.TestCase):
    """build_environment()'s output must record environment_contract_version --
    the file's own source of truth, since environment.yml is fully generated
    (no separate contract doc to drift out of sync with)."""

    def test_environment_contract_version_is_present(self) -> None:
        fake_cluster = mock.Mock(context='stub-context', namespace='bexhoma')
        with mock.patch.object(environment, 'collect_nodes', return_value=([], [])), \
             mock.patch.object(environment, 'collect_node_usage', return_value=None), \
             mock.patch.object(environment, 'collect_storage_classes', return_value=[]), \
             mock.patch.object(environment, 'collect_resource_limits', return_value={}):
            result = environment.build_environment(fake_cluster)
        self.assertEqual(result['environment_contract_version'], environment.ENVIRONMENT_CONTRACT_VERSION)


if __name__ == '__main__':
    unittest.main()
