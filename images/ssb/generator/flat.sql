-- Benchmark-Experiment-Host-Manager | images/ssb/generator
-- Authors: Patrick K. Erdelt
-- Copyright (C) 2026 Patrick K. Erdelt
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- See LICENSE for details.
-- Purpose: DuckDB variant of the lineorder_flat join, for compare-flat.sh only
--          (dev image with INCLUDE_DUCKDB=1; generator.sh uses sort/join/gawk).
--          Same output as the bash pipeline: the 17 lineorder columns with
--          lo_orderdate and lo_commitdate as YYYY-MM-DD, then all customer,
--          supplier and part columns without their keys, '|'-separated.
--          All columns are read as text, so values are written back unchanged.
--          compare-flat.sh replaces the __PLACEHOLDERS__.

SET memory_limit = '__MEMORY_LIMIT__';
SET temp_directory = '__TEMP_DIRECTORY__';
SET preserve_insertion_order = false;

COPY (
    SELECT
        l.lo_orderkey, l.lo_linenumber, l.lo_custkey, l.lo_partkey, l.lo_suppkey,
        substr(l.lo_orderdate, 1, 4) || '-' || substr(l.lo_orderdate, 5, 2) || '-' || substr(l.lo_orderdate, 7, 2),
        l.lo_orderpriority, l.lo_shippriority, l.lo_quantity, l.lo_extendedprice, l.lo_ordtotalprice,
        l.lo_discount, l.lo_revenue, l.lo_supplycost, l.lo_tax,
        substr(l.lo_commitdate, 1, 4) || '-' || substr(l.lo_commitdate, 5, 2) || '-' || substr(l.lo_commitdate, 7, 2),
        l.lo_shipmode,
        c.c_name, c.c_address, c.c_city, c.c_nation, c.c_region, c.c_phone, c.c_mktsegment,
        s.s_name, s.s_address, s.s_city, s.s_nation, s.s_region, s.s_phone,
        p.p_name, p.p_mfgr, p.p_category, p.p_brand1, p.p_color, p.p_type, p.p_size, p.p_container
    FROM read_csv('__LINEORDER__', delim = '|', header = false, quote = '', escape = '', all_varchar = true,
                  names = ['lo_orderkey', 'lo_linenumber', 'lo_custkey', 'lo_partkey', 'lo_suppkey',
                           'lo_orderdate', 'lo_orderpriority', 'lo_shippriority', 'lo_quantity',
                           'lo_extendedprice', 'lo_ordtotalprice', 'lo_discount', 'lo_revenue',
                           'lo_supplycost', 'lo_tax', 'lo_commitdate', 'lo_shipmode']) l
    JOIN read_csv('__CUSTOMER__', delim = '|', header = false, quote = '', escape = '', all_varchar = true,
                  names = ['c_custkey', 'c_name', 'c_address', 'c_city', 'c_nation', 'c_region',
                           'c_phone', 'c_mktsegment']) c ON l.lo_custkey = c.c_custkey
    JOIN read_csv('__SUPPLIER__', delim = '|', header = false, quote = '', escape = '', all_varchar = true,
                  names = ['s_suppkey', 's_name', 's_address', 's_city', 's_nation', 's_region',
                           's_phone']) s ON l.lo_suppkey = s.s_suppkey
    JOIN read_csv('__PART__', delim = '|', header = false, quote = '', escape = '', all_varchar = true,
                  names = ['p_partkey', 'p_name', 'p_mfgr', 'p_category', 'p_brand1', 'p_color',
                           'p_type', 'p_size', 'p_container']) p ON l.lo_partkey = p.p_partkey
    __ORDER_BY__
) TO '__OUTPUT__' (FORMAT csv, DELIMITER '|', HEADER false, QUOTE '', ESCAPE '');
