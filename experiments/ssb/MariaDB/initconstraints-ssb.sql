-- Benchmark-Experiment-Host-Manager | experiments/ssb/MariaDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add the foreign keys of lineorder after data loading (-xic); the
--          primary keys are already in the tables (initschema-ssb.sql).
--          foreign_key_checks is off for this session, as for TPC-H: InnoDB then
--          adds a foreign key as a metadata change instead of checking every row.
--          One ALTER TABLE for all foreign keys, so lineorder is locked once.
--          No curly braces in this file: bexhoma may fill it with str.format().

SET SESSION foreign_key_checks = 0;

ALTER TABLE ssb.lineorder
    ADD FOREIGN KEY (lo_custkey)    REFERENCES ssb.customer(c_custkey),
    ADD FOREIGN KEY (lo_suppkey)    REFERENCES ssb.supplier(s_suppkey),
    ADD FOREIGN KEY (lo_partkey)    REFERENCES ssb.part(p_partkey),
    ADD FOREIGN KEY (lo_orderdate)  REFERENCES ssb.dates(d_datekey),
    ADD FOREIGN KEY (lo_commitdate) REFERENCES ssb.dates(d_datekey);

COMMIT;
