-- Benchmark-Experiment-Host-Manager | experiments/tpch/PostgreSQL
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Add primary key and foreign key constraints to TPC-H tables
--          in the named schema. Run after data loading.
--          Each ALTER TABLE combines all actions for that table so it is
--          locked only once. Statements are ordered by FK dependency.
--          Note: the supplier→nation FK is part of the TPC-H DDL standard
--          but is not required by any query in the TPC-H workload and is
--          therefore not applied here.
--          {BEXHOMA_SCHEMA} is substituted at runtime by the Bexhoma framework.

ALTER TABLE {BEXHOMA_SCHEMA}.region
    ADD PRIMARY KEY (r_regionkey);

ALTER TABLE {BEXHOMA_SCHEMA}.nation
    ADD PRIMARY KEY (n_nationkey),
    ADD FOREIGN KEY (n_regionkey)          REFERENCES {BEXHOMA_SCHEMA}.region(r_regionkey);

ALTER TABLE {BEXHOMA_SCHEMA}.part
    ADD PRIMARY KEY (p_partkey);

ALTER TABLE {BEXHOMA_SCHEMA}.supplier
    ADD PRIMARY KEY (s_suppkey);

ALTER TABLE {BEXHOMA_SCHEMA}.partsupp
    ADD PRIMARY KEY (ps_partkey, ps_suppkey),
    ADD FOREIGN KEY (ps_suppkey)           REFERENCES {BEXHOMA_SCHEMA}.supplier(s_suppkey),
    ADD FOREIGN KEY (ps_partkey)           REFERENCES {BEXHOMA_SCHEMA}.part(p_partkey);

ALTER TABLE {BEXHOMA_SCHEMA}.customer
    ADD PRIMARY KEY (c_custkey),
    ADD FOREIGN KEY (c_nationkey)          REFERENCES {BEXHOMA_SCHEMA}.nation(n_nationkey);

ALTER TABLE {BEXHOMA_SCHEMA}.orders
    ADD PRIMARY KEY (o_orderkey),
    ADD FOREIGN KEY (o_custkey)            REFERENCES {BEXHOMA_SCHEMA}.customer(c_custkey);

ALTER TABLE {BEXHOMA_SCHEMA}.lineitem
    ADD PRIMARY KEY (l_orderkey, l_linenumber),
    ADD FOREIGN KEY (l_orderkey)           REFERENCES {BEXHOMA_SCHEMA}.orders(o_orderkey),
    ADD FOREIGN KEY (l_partkey)            REFERENCES {BEXHOMA_SCHEMA}.part(p_partkey),
    ADD FOREIGN KEY (l_suppkey)            REFERENCES {BEXHOMA_SCHEMA}.supplier(s_suppkey),
    ADD FOREIGN KEY (l_partkey, l_suppkey) REFERENCES {BEXHOMA_SCHEMA}.partsupp(ps_partkey, ps_suppkey);
