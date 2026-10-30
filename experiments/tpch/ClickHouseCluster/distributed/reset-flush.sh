#!/bin/sh
# Benchmark-Experiment-Host-Manager | experiments/tpch/ClickHouseCluster/distributed
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Pre-benchmark reset for ClickHouse, run before each benchmarking
#          round with -ar, in every worker pod. Steps of the reset contract (docs/DBMS.md):
#          1 statistics, 2 persist, 3 counters.

# step 1 (statistics): n/a - MergeTree keeps no optimizer statistics unless they are declared per column

# step 2 (persist): an INSERT writes its parts as files without fsync (fsync_after_insert = 0),
# so the loaded data may still be dirty in the page cache; sync writes it to disk
sync && echo "sync done"

# step 3 (counters): n/a - system.events and the Prometheus counters cannot be reset
