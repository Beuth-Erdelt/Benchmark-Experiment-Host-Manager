-- Benchmark-Experiment-Host-Manager | experiments/ycsb/YugabyteDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Verifies the YCSB usertable distribution across YugabyteDB
--          tablets and reports the current row count.

SELECT 'yb_table_properties.usertable' AS msg;
SELECT * FROM yb_table_properties('usertable'::regclass);

SELECT 'yb_servers' AS msg;
SELECT *
FROM yb_servers()
JOIN yb_local_tablets ON true;

SELECT COUNT(*) AS "Number of rows in usertable" FROM usertable;
