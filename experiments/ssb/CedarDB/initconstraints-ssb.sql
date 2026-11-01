-- Benchmark-Experiment-Host-Manager | experiments/ssb/CedarDB
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add primary key and foreign key constraints after data loading (-xic).
--          Keys as in the SSB specification (lineorder: lo_orderkey, lo_linenumber).
--          Each ALTER TABLE combines all actions for that table so it is locked
--          only once; dimensions come before lineorder, which references them.
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER TABLE public.customer
    ADD PRIMARY KEY (c_custkey);

ALTER TABLE public.supplier
    ADD PRIMARY KEY (s_suppkey);

ALTER TABLE public.part
    ADD PRIMARY KEY (p_partkey);

ALTER TABLE public.dates
    ADD PRIMARY KEY (d_datekey);

ALTER TABLE public.lineorder
    ADD PRIMARY KEY (lo_orderkey, lo_linenumber),
    ADD FOREIGN KEY (lo_custkey)    REFERENCES public.customer(c_custkey),
    ADD FOREIGN KEY (lo_suppkey)    REFERENCES public.supplier(s_suppkey),
    ADD FOREIGN KEY (lo_partkey)    REFERENCES public.part(p_partkey),
    ADD FOREIGN KEY (lo_orderdate)  REFERENCES public.dates(d_datekey),
    ADD FOREIGN KEY (lo_commitdate) REFERENCES public.dates(d_datekey);
