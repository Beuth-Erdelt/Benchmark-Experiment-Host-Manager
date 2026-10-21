"""Tests for the check that schema/database tenancy gets the same number of loader pods per tenant.

The TPC-H loader splits ``-nlp`` evenly across ``-mtn`` tenants; with a remainder
a tenant loads a part twice.

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
from __future__ import annotations

import unittest

from bexhoma.cli_args import check_tenant_loading_pods

__all__ = []


class CheckTenantLoadingPodsTest(unittest.TestCase):
    """-nlp must be a multiple of -mtn for schema and database tenancy only."""

    def test_multiples_pass(self):
        for tenant_by in ('schema', 'database'):
            with self.subTest(tenant_by):
                check_tenant_loading_pods([2], 2, tenant_by)
                check_tenant_loading_pods([8], 2, tenant_by)
                check_tenant_loading_pods([4, 8], 4, tenant_by)

    def test_remainder_raises(self):
        for tenant_by in ('schema', 'database'):
            with self.subTest(tenant_by):
                with self.assertRaisesRegex(ValueError, r"-nlp 3 is not a multiple of -mtn 2"):
                    check_tenant_loading_pods([3], 2, tenant_by)
                with self.assertRaisesRegex(ValueError, r"-nlp 1,6 is not a multiple of -mtn 4"):
                    check_tenant_loading_pods([1, 4, 6], 4, tenant_by)

    def test_one_pod_per_tenant_needs_one(self):
        # Benchbase: -nlp counts pods per tenant (test-docs-multitenant.ps1 uses -nlp 1 -mtn 2)
        check_tenant_loading_pods([1], 2, 'schema', one_pod_per_tenant=True)
        with self.assertRaisesRegex(ValueError, r"-nlp 2 is not 1"):
            check_tenant_loading_pods([2], 2, 'database', one_pod_per_tenant=True)
        check_tenant_loading_pods([2], 2, 'container', one_pod_per_tenant=True)

    def test_benchbase_is_one_pod_per_tenant(self):
        from bexhoma.experiments.base import ExperimentBase
        from bexhoma.experiments.benchbase import BenchbaseExperiment
        from bexhoma.experiments.tpch import TpchExperiment
        self.assertTrue(BenchbaseExperiment.tenant_loading_one_pod_per_tenant)
        self.assertFalse(TpchExperiment.tenant_loading_one_pod_per_tenant)
        self.assertFalse(ExperimentBase.tenant_loading_one_pod_per_tenant)

    def test_no_check_without_split(self):
        # container tenancy runs one loader job per tenant, no tenancy has nothing to split
        check_tenant_loading_pods([3], 2, 'container')
        check_tenant_loading_pods([3], 0, 'schema')
        check_tenant_loading_pods([3], 0, '')


if __name__ == '__main__':
    unittest.main()
