# Benchmark-Experiment-Host-Manager | experiments/ycsb/Redis
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Pre-benchmark reset for YCSB on Redis, run before each
#          benchmarking round with -ar: in the SUT pod (standalone) or on
#          every worker (cluster, script target 'workers'). Steps of the reset
#          contract (docs/DBMS.md): 1 statistics, 2 persist, 3 counters. SAVE
#          is synchronous and returns when the RDB snapshot is on disk.
#          No curly braces in this file: bexhoma may fill it with str.format().

# step 1 (statistics): n/a - key-value store without optimizer statistics

# step 2 (persist)
echo "invoking SAVE"
redis-cli SAVE

# step 3 (counters)
echo "invoking CONFIG RESETSTAT"
redis-cli CONFIG RESETSTAT
