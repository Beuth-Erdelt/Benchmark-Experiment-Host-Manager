-- Benchmark-Experiment-Host-Manager | experiments/tpch/ClickHouseCluster
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for TPC-H on a ClickHouse cluster, run on the
--          coordinator before each benchmarking round with -ar. Steps of the
--          reset contract (docs/DBMS.md): 1 statistics, 2 persist, 3 counters.
--          The sync of the shards' page cache is reset-flush.sh, which runs
--          on every worker (script target workers).

-- step 1 (statistics): n/a - MergeTree keeps no optimizer statistics unless they are declared per column

-- step 2 (persist): rows a Distributed table still holds for the shards are sent now
SYSTEM FLUSH DISTRIBUTED nation;
SYSTEM FLUSH DISTRIBUTED region;
SYSTEM FLUSH DISTRIBUTED part;
SYSTEM FLUSH DISTRIBUTED supplier;
SYSTEM FLUSH DISTRIBUTED partsupp;
SYSTEM FLUSH DISTRIBUTED customer;
SYSTEM FLUSH DISTRIBUTED orders;
SYSTEM FLUSH DISTRIBUTED lineitem;

-- step 3 (counters): n/a - system.events and the Prometheus counters cannot be reset
