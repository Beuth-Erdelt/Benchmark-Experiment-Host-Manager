-- Benchmark-Experiment-Host-Manager | experiments/tpcds/ClickHouseCluster
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Pre-benchmark reset for TPC-DS on a ClickHouse cluster, run on the
--          coordinator before each benchmarking round with -ar. Steps of the
--          reset contract (docs/DBMS.md): 1 statistics, 2 persist, 3 counters.
--          The sync of the shards' page cache is reset-flush.sh, which runs
--          on every worker (script target workers).

-- step 1 (statistics): n/a - MergeTree keeps no optimizer statistics unless they are declared per column

-- step 2 (persist): rows a Distributed table still holds for the shards are sent now
SYSTEM FLUSH DISTRIBUTED dbgen_version;
SYSTEM FLUSH DISTRIBUTED customer_address;
SYSTEM FLUSH DISTRIBUTED customer_demographics;
SYSTEM FLUSH DISTRIBUTED date_dim;
SYSTEM FLUSH DISTRIBUTED warehouse;
SYSTEM FLUSH DISTRIBUTED ship_mode;
SYSTEM FLUSH DISTRIBUTED time_dim;
SYSTEM FLUSH DISTRIBUTED reason;
SYSTEM FLUSH DISTRIBUTED income_band;
SYSTEM FLUSH DISTRIBUTED item;
SYSTEM FLUSH DISTRIBUTED store;
SYSTEM FLUSH DISTRIBUTED call_center;
SYSTEM FLUSH DISTRIBUTED customer;
SYSTEM FLUSH DISTRIBUTED web_site;
SYSTEM FLUSH DISTRIBUTED store_returns;
SYSTEM FLUSH DISTRIBUTED household_demographics;
SYSTEM FLUSH DISTRIBUTED web_page;
SYSTEM FLUSH DISTRIBUTED promotion;
SYSTEM FLUSH DISTRIBUTED catalog_page;
SYSTEM FLUSH DISTRIBUTED inventory;
SYSTEM FLUSH DISTRIBUTED catalog_returns;
SYSTEM FLUSH DISTRIBUTED web_returns;
SYSTEM FLUSH DISTRIBUTED web_sales;
SYSTEM FLUSH DISTRIBUTED catalog_sales;
SYSTEM FLUSH DISTRIBUTED store_sales;

-- step 3 (counters): n/a - system.events and the Prometheus counters cannot be reset
