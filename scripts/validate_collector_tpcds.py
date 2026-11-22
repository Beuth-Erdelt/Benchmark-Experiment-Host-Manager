#!/usr/bin/env python
"""
Validator for DbmsBenchmarkerCollector / TPC-DS.
Checks: no exceptions, non-empty DataFrames, important columns present
(see validate_collector_dbmsbenchmarker_common.py).
Shows head() for every DataFrame and prints a bottom-line summary.
"""
from validate_collector_dbmsbenchmarker_common import validate_dbmsbenchmarker

validate_dbmsbenchmarker("tpcds", "TPC-DS")
