# Benchmark-Experiment-Host-Manager | experiments/ycsb/Dragonfly
# Authors: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Triggers a Dragonfly/Redis SAVE operation twice with a 5-second
#          delay to ensure the snapshot is written to disk.

echo "invoking SAVE"
/usr/bin/redis-cli SAVE

echo "sleeping 5 secs"
sleep 5

echo "invoking SAVE"
/usr/bin/redis-cli SAVE
