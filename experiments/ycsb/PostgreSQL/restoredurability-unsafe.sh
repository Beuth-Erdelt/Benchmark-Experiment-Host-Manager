# Benchmark-Experiment-Host-Manager | experiments/ycsb/PostgreSQL
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
# Purpose: Undo load durability 'unsafe', after restoredurability-unsafe.sql
#          (fsync on, CHECKPOINT). Flushes the OS cache to the volume, as the
#          PostgreSQL docs require when fsync goes from off to on.
echo "sync after fsync=off"
sync
echo "done"
