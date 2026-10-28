-- Benchmark-Experiment-Host-Manager | experiments/ssb/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create indexes after data loading (-xii), as for PostgreSQL: the
--          foreign key columns of lineorder for the joins, and the dimension
--          columns the 13 SSB queries filter on.
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE INDEX lo_od ON ssb.lineorder (lo_orderdate);
CREATE INDEX lo_c  ON ssb.lineorder (lo_custkey);
CREATE INDEX lo_s  ON ssb.lineorder (lo_suppkey);
CREATE INDEX lo_p  ON ssb.lineorder (lo_partkey);
CREATE INDEX c_r   ON ssb.customer  (c_region);
CREATE INDEX c_n   ON ssb.customer  (c_nation);
CREATE INDEX c_c   ON ssb.customer  (c_city);
CREATE INDEX s_r   ON ssb.supplier  (s_region);
CREATE INDEX s_n   ON ssb.supplier  (s_nation);
CREATE INDEX s_c   ON ssb.supplier  (s_city);
CREATE INDEX p_m   ON ssb.part      (p_mfgr);
CREATE INDEX p_c   ON ssb.part      (p_category);
CREATE INDEX p_b   ON ssb.part      (p_brand1);
CREATE INDEX d_y   ON ssb.dates     (d_year);
CREATE INDEX d_ymn ON ssb.dates     (d_yearmonthnum);
CREATE INDEX d_ym  ON ssb.dates     (d_yearmonth);
CREATE INDEX d_w   ON ssb.dates     (d_weeknuminyear);

COMMIT;
