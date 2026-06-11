-- Benchmark-Experiment-Host-Manager | experiments/tpch/OmniSci
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2020 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: Load TPC-H data at scale factor 1 (SF1 ~ 1 GB) into OmniSci.
--          OmniSci COPY uses its own options: delimiter sets the field separator,
--          header='false' skips header-row detection, quoted='false' disables
--          quote handling (dbgen output is unquoted).

COPY customer FROM '/data/tpch/SF1/customer.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY lineitem FROM '/data/tpch/SF1/lineitem.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY nation FROM '/data/tpch/SF1/nation.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY orders FROM '/data/tpch/SF1/orders.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY part FROM '/data/tpch/SF1/part.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY partsupp FROM '/data/tpch/SF1/partsupp.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY region FROM '/data/tpch/SF1/region.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
COPY supplier FROM '/data/tpch/SF1/supplier.tbl'
    WITH (delimiter = '|', header = 'false', quoted = 'false');
