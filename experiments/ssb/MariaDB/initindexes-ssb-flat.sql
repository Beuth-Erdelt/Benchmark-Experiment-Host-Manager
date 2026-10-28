-- Benchmark-Experiment-Host-Manager | experiments/ssb/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create indexes on lineorder_flat after data loading (-xii, -xsv flat),
--          as for PostgreSQL: the order date and the dimension columns the 13
--          SSB queries filter on.
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE INDEX lf_od ON ssb.lineorder_flat (lo_orderdate);
CREATE INDEX lf_cr ON ssb.lineorder_flat (c_region);
CREATE INDEX lf_cn ON ssb.lineorder_flat (c_nation);
CREATE INDEX lf_cc ON ssb.lineorder_flat (c_city);
CREATE INDEX lf_sr ON ssb.lineorder_flat (s_region);
CREATE INDEX lf_sn ON ssb.lineorder_flat (s_nation);
CREATE INDEX lf_sc ON ssb.lineorder_flat (s_city);
CREATE INDEX lf_pm ON ssb.lineorder_flat (p_mfgr);
CREATE INDEX lf_pc ON ssb.lineorder_flat (p_category);
CREATE INDEX lf_pb ON ssb.lineorder_flat (p_brand1);

COMMIT;
