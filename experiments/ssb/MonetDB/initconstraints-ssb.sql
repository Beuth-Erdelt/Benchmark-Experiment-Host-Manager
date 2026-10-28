-- Benchmark-Experiment-Host-Manager | experiments/ssb/MonetDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add primary key and foreign key constraints after data loading (-xic).
--          Keys as in the SSB specification (lineorder: lo_orderkey, lo_linenumber).
--          MonetDB does not support multiple actions in a single ALTER TABLE
--          statement; each constraint is applied as a separate statement.
--          Dimensions come before lineorder, which references them.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER TABLE customer
    ADD PRIMARY KEY (c_custkey);

ALTER TABLE supplier
    ADD PRIMARY KEY (s_suppkey);

ALTER TABLE part
    ADD PRIMARY KEY (p_partkey);

ALTER TABLE dates
    ADD PRIMARY KEY (d_datekey);

ALTER TABLE lineorder
    ADD PRIMARY KEY (lo_orderkey, lo_linenumber);
ALTER TABLE lineorder
    ADD FOREIGN KEY (lo_custkey) REFERENCES customer(c_custkey);
ALTER TABLE lineorder
    ADD FOREIGN KEY (lo_suppkey) REFERENCES supplier(s_suppkey);
ALTER TABLE lineorder
    ADD FOREIGN KEY (lo_partkey) REFERENCES part(p_partkey);
ALTER TABLE lineorder
    ADD FOREIGN KEY (lo_orderdate) REFERENCES dates(d_datekey);
ALTER TABLE lineorder
    ADD FOREIGN KEY (lo_commitdate) REFERENCES dates(d_datekey);
