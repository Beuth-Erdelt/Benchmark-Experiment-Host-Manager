# Benchmark-Experiment-Host-Manager | experiments/ycsb/Dragonfly
# Authors: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Pre-benchmark reset for YCSB on Dragonfly, run before each
#          benchmarking round with -ar: in the SUT pod, or on every worker
#          (cluster and replica mode). Steps of the reset contract
#          (docs/DBMS.md): 1 statistics, 2 persist, 3 counters. SAVE runs
#          twice with a 5-second delay to ensure the snapshot is written to
#          disk.
#          No curly braces in this file: bexhoma may fill it with str.format().

# step 1 (statistics): n/a - key-value store without optimizer statistics

# step 2 (persist)
echo "invoking SAVE"
/usr/bin/redis-cli SAVE

echo "sleeping 5 secs"
sleep 5

echo "invoking SAVE"
/usr/bin/redis-cli SAVE

# step 3 (counters)
echo "invoking CONFIG RESETSTAT"
/usr/bin/redis-cli CONFIG RESETSTAT
