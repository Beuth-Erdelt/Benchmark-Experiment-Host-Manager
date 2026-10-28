-- Benchmark-Experiment-Host-Manager | experiments/ssb/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Create indexes after data loading (-xii): the foreign key columns of
--          lineorder for the joins, and the dimension columns the 13 SSB queries
--          filter on. Same set as for PostgreSQL; MonetDB uses them as per-column
--          access paths (it may also ignore them).
--          No curly braces in this file: bexhoma may fill it with str.format().

CREATE INDEX lo_od ON lineorder (lo_orderdate);
CREATE INDEX lo_c  ON lineorder (lo_custkey);
CREATE INDEX lo_s  ON lineorder (lo_suppkey);
CREATE INDEX lo_p  ON lineorder (lo_partkey);
CREATE INDEX c_r   ON customer  (c_region);
CREATE INDEX c_n   ON customer  (c_nation);
CREATE INDEX c_ci  ON customer  (c_city);
CREATE INDEX s_r   ON supplier  (s_region);
CREATE INDEX s_n   ON supplier  (s_nation);
CREATE INDEX s_ci  ON supplier  (s_city);
CREATE INDEX p_m   ON part      (p_mfgr);
CREATE INDEX p_ca  ON part      (p_category);
CREATE INDEX p_b   ON part      (p_brand1);
CREATE INDEX d_y   ON dates     (d_year);
CREATE INDEX d_ymn ON dates     (d_yearmonthnum);
CREATE INDEX d_ym  ON dates     (d_yearmonth);
CREATE INDEX d_w   ON dates     (d_weeknuminyear);
