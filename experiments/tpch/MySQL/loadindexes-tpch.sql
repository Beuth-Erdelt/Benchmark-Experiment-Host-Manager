-- Benchmark-Experiment-Host-Manager | experiments/tpch/MySQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Verify that indexes created by initindexes-tpch.sql are actually
--          used by forcing index scans, then count all rows in each table.
--          Note: FORCE INDEX(s_n) references supplier(s_nationkey) which is
--          not created in initindexes-tpch.sql (supplier->nation FK not applied).

-- Force index scans to confirm each index is operational
SELECT COUNT(*) FROM tpch.customer  FORCE INDEX(c_n);
SELECT COUNT(*) FROM tpch.nation    FORCE INDEX(n_r);
SELECT COUNT(*) FROM tpch.supplier  FORCE INDEX(s_n);
SELECT COUNT(*) FROM tpch.partsupp  FORCE INDEX(ps_s);
SELECT COUNT(*) FROM tpch.partsupp  FORCE INDEX(ps_p);
SELECT COUNT(*) FROM tpch.orders    FORCE INDEX(o_c);
SELECT COUNT(*) FROM tpch.lineitem  FORCE INDEX(l_o);
SELECT COUNT(*) FROM tpch.lineitem  FORCE INDEX(l_ps);

-- Verify row counts for all tables
SELECT COUNT(*) FROM tpch.customer;
SELECT COUNT(*) FROM tpch.lineitem;
SELECT COUNT(*) FROM tpch.nation;
SELECT COUNT(*) FROM tpch.supplier;
SELECT COUNT(*) FROM tpch.partsupp;
SELECT COUNT(*) FROM tpch.orders;
SELECT COUNT(*) FROM tpch.region;
SELECT COUNT(*) FROM tpch.part;
