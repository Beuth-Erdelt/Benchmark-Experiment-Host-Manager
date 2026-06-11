-- Benchmark-Experiment-Host-Manager | experiments/tpch/OmniSci
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 10 (SF10 ~ 10 GB) into OmniSci.
--          See initdata-tpch-SF1.sql for option descriptions.

COPY customer FROM '/data/tpch/SF10/customer.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY lineitem FROM '/data/tpch/SF10/lineitem.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY nation FROM '/data/tpch/SF10/nation.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY orders FROM '/data/tpch/SF10/orders.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY part FROM '/data/tpch/SF10/part.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY partsupp FROM '/data/tpch/SF10/partsupp.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY region FROM '/data/tpch/SF10/region.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY supplier FROM '/data/tpch/SF10/supplier.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
