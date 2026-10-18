-- Benchmark-Experiment-Host-Manager | experiments/tpcds/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Last post-load script, always run (also without -xii/-xic/-xis).
--          Reports row counts and storage sizes. MonetDB's init scripts relax
--          no setting, so nothing is restored here.
--          No curly braces in this file: bexhoma may fill it with str.format().

-- Row counts per table (exact counts)
SELECT 'call_center' AS table_name, COUNT(*) AS row_count FROM sys.call_center
UNION ALL SELECT 'catalog_page',           COUNT(*) FROM sys.catalog_page
UNION ALL SELECT 'catalog_returns',        COUNT(*) FROM sys.catalog_returns
UNION ALL SELECT 'catalog_sales',          COUNT(*) FROM sys.catalog_sales
UNION ALL SELECT 'customer',               COUNT(*) FROM sys.customer
UNION ALL SELECT 'customer_address',       COUNT(*) FROM sys.customer_address
UNION ALL SELECT 'customer_demographics',  COUNT(*) FROM sys.customer_demographics
UNION ALL SELECT 'date_dim',               COUNT(*) FROM sys.date_dim
UNION ALL SELECT 'dbgen_version',          COUNT(*) FROM sys.dbgen_version
UNION ALL SELECT 'household_demographics', COUNT(*) FROM sys.household_demographics
UNION ALL SELECT 'income_band',            COUNT(*) FROM sys.income_band
UNION ALL SELECT 'inventory',              COUNT(*) FROM sys.inventory
UNION ALL SELECT 'item',                   COUNT(*) FROM sys.item
UNION ALL SELECT 'promotion',              COUNT(*) FROM sys.promotion
UNION ALL SELECT 'reason',                 COUNT(*) FROM sys.reason
UNION ALL SELECT 'ship_mode',              COUNT(*) FROM sys.ship_mode
UNION ALL SELECT 'store',                  COUNT(*) FROM sys.store
UNION ALL SELECT 'store_returns',          COUNT(*) FROM sys.store_returns
UNION ALL SELECT 'store_sales',            COUNT(*) FROM sys.store_sales
UNION ALL SELECT 'time_dim',               COUNT(*) FROM sys.time_dim
UNION ALL SELECT 'warehouse',              COUNT(*) FROM sys.warehouse
UNION ALL SELECT 'web_page',               COUNT(*) FROM sys.web_page
UNION ALL SELECT 'web_returns',            COUNT(*) FROM sys.web_returns
UNION ALL SELECT 'web_sales',              COUNT(*) FROM sys.web_sales
UNION ALL SELECT 'web_site',               COUNT(*) FROM sys.web_site;

-- Storage per table (columns, heaps and auxiliary structures)
SELECT s."table",
       CAST(SUM(s.columnsize + s.heapsize + s.hashes + s.imprints + s.orderidx) / 1024 / 1024 AS BIGINT) AS size_mib
FROM sys."storage" s
JOIN sys.tables t ON t.name = s."table" AND t.system = false
WHERE s."schema" = 'sys'
GROUP BY s."table"
ORDER BY size_mib DESC;
