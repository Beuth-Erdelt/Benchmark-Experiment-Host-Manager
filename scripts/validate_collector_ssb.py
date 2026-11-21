#!/usr/bin/env python
"""
Validator for DbmsBenchmarkerCollector / SSB (star schema and flat schema).
Checks: no exceptions, non-empty DataFrames, important columns present
(see validate_collector_dbmsbenchmarker_common.py).
Shows head() for every DataFrame and prints a bottom-line summary.
"""
from validate_collector_dbmsbenchmarker_common import validate_dbmsbenchmarker

validate_dbmsbenchmarker("ssb", "SSB")
