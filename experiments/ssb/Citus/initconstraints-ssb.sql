-- Benchmark-Experiment-Host-Manager | experiments/ssb/Citus
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add primary key and foreign key constraints after data loading (-xic),
--          for reference-table dimensions (-xdim replicated). Keys as in the SSB
--          specification; the primary key of lineorder includes its distribution
--          column lo_orderkey. Citus allows foreign keys from a distributed table
--          to a reference table. One ADD CONSTRAINT per ALTER TABLE: Citus rejects
--          several subcommands ("cannot execute ADD CONSTRAINT command with other
--          subcommands").
--          No curly braces in this file: bexhoma may fill it with str.format().

ALTER TABLE public.customer  ADD PRIMARY KEY (c_custkey);
ALTER TABLE public.supplier  ADD PRIMARY KEY (s_suppkey);
ALTER TABLE public.part      ADD PRIMARY KEY (p_partkey);
ALTER TABLE public.dates     ADD PRIMARY KEY (d_datekey);
ALTER TABLE public.lineorder ADD PRIMARY KEY (lo_orderkey, lo_linenumber);

ALTER TABLE public.lineorder ADD FOREIGN KEY (lo_custkey)    REFERENCES public.customer(c_custkey);
ALTER TABLE public.lineorder ADD FOREIGN KEY (lo_suppkey)    REFERENCES public.supplier(s_suppkey);
ALTER TABLE public.lineorder ADD FOREIGN KEY (lo_partkey)    REFERENCES public.part(p_partkey);
ALTER TABLE public.lineorder ADD FOREIGN KEY (lo_orderdate)  REFERENCES public.dates(d_datekey);
ALTER TABLE public.lineorder ADD FOREIGN KEY (lo_commitdate) REFERENCES public.dates(d_datekey);
