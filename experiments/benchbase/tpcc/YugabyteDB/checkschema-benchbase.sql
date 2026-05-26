-- Benchmark-Experiment-Host-Manager | experiments/benchbase/tpcc/YugabyteDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Verify tablet distribution and cluster status for the benchbase
--          TPC-C tables on YugabyteDB after loading.

SELECT 'yb_table_properties.warehouse' AS msg;
SELECT * FROM yb_table_properties('warehouse'::regclass);

SELECT 'yb_table_properties.item' AS msg;
SELECT * FROM yb_table_properties('item'::regclass);

SELECT 'yb_table_properties.stock' AS msg;
SELECT * FROM yb_table_properties('stock'::regclass);

SELECT 'yb_table_properties.district' AS msg;
SELECT * FROM yb_table_properties('district'::regclass);

SELECT 'yb_table_properties.customer' AS msg;
SELECT * FROM yb_table_properties('customer'::regclass);

SELECT 'yb_table_properties.history' AS msg;
SELECT * FROM yb_table_properties('history'::regclass);

SELECT 'yb_table_properties.oorder' AS msg;
SELECT * FROM yb_table_properties('oorder'::regclass);

SELECT 'yb_table_properties.new_order' AS msg;
SELECT * FROM yb_table_properties('new_order'::regclass);

SELECT 'yb_table_properties.order_line' AS msg;
SELECT * FROM yb_table_properties('order_line'::regclass);

SELECT 'yb_servers' AS msg;
SELECT *
FROM yb_servers()
JOIN yb_local_tablets ON true;

-- Check the actual max allowed connections
SHOW max_connections;

-- Optional: How many connections are currently in use
SELECT count(*) AS active_connections FROM pg_stat_activity;
