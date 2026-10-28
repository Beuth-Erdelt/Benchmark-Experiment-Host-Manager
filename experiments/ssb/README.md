# SSB Experiments

This folder contains the query files and the DDL scripts of the Star Schema Benchmark (SSB)
for PostgreSQL, MonetDB, ClickHouse, ClickHouseCluster, Citus, MySQL and MariaDB (PgDuckDB uses
the PostgreSQL scripts). The entry script is `ssb.py`
(`bexhoma ssb run ...`), the images are in `images/ssb/`.

## Sources

| What | Source |
|---|---|
| Specification | P. O'Neil, E. O'Neil, X. Chen, S. Revilak: *Star Schema Benchmark*, Revision 3, June 5, 2009, <https://www.cs.umb.edu/~poneil/StarSchemaB.PDF> |
| Data generator | <https://github.com/eyalroz/ssb-dbgen>, commit `ae1e254aa4d603d8ef1f44078e5abed011634b23`, plus `images/ssb/generator/dbgen-chunk-seeds.patch` |
| Random query parameters | T. Rabl, M. Poess, H.-A. Jacobsen, P. O'Neil, E. O'Neil: *Variations of the Star Schema Benchmark to Test the Effects of Data Skew on Query Performance*, ICPE 2013, section 3.2 |
| Flat table | ClickHouse docs, *Star Schema Benchmark*; Apache Doris docs, *SSB* |

## Schema and scaling

| Table | Rows | Note |
|---|---|---|
| `customer` | 30,000 x SF | |
| `supplier` | 2,000 x SF | |
| `part` | 200,000 x floor(1 + log2 SF) | SF 10: 800,000 |
| `dates` | 2,557 | 1992-01-01 to 1998-12-31; `date` in the specification (reserved word) |
| `lineorder` | about 6,000,000 x SF | SF 1: 6,001,215; SF 10: 59,986,052; orders until 1998-08-02 |
| `lineorder_flat` | = lineorder | flat variant: lineorder + all customer, supplier, part columns without keys; `lo_orderdate` and `lo_commitdate` as `DATE` |

`d_weeknuminyear` is `d_daynuminyear / 7 + 1` in dbgen: week 1 has 6 days, weeks 2-52 have 7,
week 53 one or two. Week 6 of 1994 is 1994-02-04 to 1994-02-10.

## Files

| File | Purpose |
|---|---|
| `queries-ssb.config` | 13 queries, star schema, constants of the specification (`-xsv normal -xqv spec`) |
| `queries-ssb-random.config` | 13 queries, star schema, random parameters (`-xqv random`) |
| `queries-ssb-flat.config` | 13 queries on `lineorder_flat`, constants of the specification (`-xsv flat`) |
| `queries-ssb-flat-random.config` | 13 queries on `lineorder_flat`, random parameters |
| `queries-ssb-empty.config` | `select 1` (mode `empty`) |
| `queries-ssb-profiling.config` | count, count distinct, min, max of the key and date columns (mode `profiling`, star schema) |
| `queries-ssb-flat-profiling.config` | the same for `lineorder_flat` (mode `profiling`, `-xsv flat`) |
| `make_queries.py` | Writes the seven query files above |
| `<DBMS>/initschema-ssb.sql`, `initschema-ssb-flat.sql` | Create the tables of the variant |
| `<DBMS>/initindexes-ssb*.sql` | `-xii`: foreign key columns of lineorder and the filtered dimension columns |
| `<DBMS>/initconstraints-ssb.sql` | `-xic`: primary keys and foreign keys (star schema only; MySQL and MariaDB: foreign keys, the primary keys are in the schema) |
| `<DBMS>/initstatistics-ssb*.sql` | `-xis`: `ANALYZE` |
| `<DBMS>/checkschema-ssb*.sql` | Last post-load script: row counts and sizes |
| `<DBMS>/reset-ssb*.sql`, `reset-flush.sh` | `-ar`: reset before each benchmarking round (`-flat` where the tables differ) |
| `<DBMS>/durability-*`, `restoredurability-*` | `-xld`: durability during the load (PostgreSQL, Citus, MySQL, MariaDB) |
| `<DBMS>/distributed/` | `-xdim distributed` (ClickHouseCluster, Citus): the scripts of the star schema with the dimensions spread over the nodes; the files that do not depend on the placement are copies |

ClickHouse and ClickHouseCluster have no index, constraint or statistics scripts (the sorting
key is set in the schema). The script lists are `volumes.ssb` in the cluster config; a DBMS
folder without a listed script skips it.

The flat queries have a MySQL variant (`'DBMS': {'MySQL': ...}`, also used by MariaDB, whose
dialect is MySQL): `extract(year from lo_orderdate)` without `CAST(... AS INTEGER)`.

## Queries and filter factors (specification)

| Query | Restriction | FF on lineorder |
|---|---|---|
| Q1.1 | year 1993, discount 1-3, quantity < 25 | 0.019 |
| Q1.2 | yearmonthnum 199401, discount 4-6, quantity 26-35 | 0.00065 |
| Q1.3 | week 6 of 1994, discount 5-7, quantity 26-35 | 0.000075 |
| Q2.1 | category MFGR#12, supplier region AMERICA | 1/125 |
| Q2.2 | brands MFGR#2221-2228, supplier region ASIA | 1/625 |
| Q2.3 | brand MFGR#2239, supplier region EUROPE | 1/5000 |
| Q3.1 | customer and supplier region ASIA, years 1992-1997 | 6/175 |
| Q3.2 | customer and supplier nation UNITED STATES, years 1992-1997 | 6/4375 |
| Q3.3 | cities UNITED KI1, UNITED KI5 (customer and supplier), years 1992-1997 | 6/109375 |
| Q3.4 | same cities, December 1997 | 1/1312500 |
| Q4.1 | customer and supplier region AMERICA, mfgr 1 or 2 | 2/125 |
| Q4.2 | as Q4.1, years 1997-1998 | 4/875 |
| Q4.3 | customer region AMERICA, supplier nation UNITED STATES, category MFGR#14, years 1997-1998 | 2/21875 |

Deviations from the specification text: Q1.3 uses quantity 26-35 (the specification's SQL;
its text says 36-40), Q2.3 uses brand `MFGR#2239` (the specification's text says `MFGR#2339`,
its SQL `MFGR#2221`, which overlaps Q2.2; ClickHouse and Doris use `MFGR#2239`).

## Random parameters (`-xqv random`)

Each query keeps its specification's filter factor:

1. A predicate that picks one member of a uniform hierarchy level (year, month, week, region,
   nation, city, mfgr, category, brand) draws from the whole level.
2. A range over a measure keeps its width and moves its start (discount: D-1..D+1 with
   D in [2,9] as in the specification's Q1 template; quantity: Q..Q+9 with Q in [1,41]).
3. Correlated values come from one `dict` parameter.

| Query | Parameters |
|---|---|
| Q1.1 | year in [1993,1997]; discount D in [2,9]; quantity < Q, Q in [24,25] (the specification's ranges) |
| Q1.2 | yearmonthnum in 199201..199712; D; Q..Q+9 |
| Q1.3 | year in [1992,1997], week in [2,52]; D; Q..Q+9 |
| Q2.1 | category in MFGR#11..55; region |
| Q2.2 | category; 8 consecutive brands within one decade (start in 10, 11, 12, 20, 21, 22, 30, 31, 32: brands are not zero-padded, so `MFGR#2215`..`MFGR#2222` would also catch brand 2, `MFGR#222`); region |
| Q2.3 | category, brand in [1,40]; region |
| Q3.1 | region (same for customer and supplier); years 1992-1997 fixed |
| Q3.2 | nation |
| Q3.3 | two distinct cities of one nation (dict: city -> the other 9 cities of its nation) |
| Q3.4 | as Q3.3, month in Jan1992..Dec1997 |
| Q4.1 | region; two distinct mfgr |
| Q4.2 | as Q4.1, years Y and Y+1, Y in [1992,1997] |
| Q4.3 | region -> one of its nations (dict); years Y, Y+1; category |

The flat files take year, month and week as date ranges on `lo_orderdate` (dicts from the
first to the last or next date), so no date arithmetic is needed in SQL. With `-xrcp` every
stream draws its own parameters.

The query files are generated by `make_queries.py` (run it from the repository root after a
change), not written by hand; they were checked locally against
PostgreSQL 18.6, MonetDB Dec2025-SP3 and ClickHouse 26.8 at SF 1: all three DBMS return the
same results for every query of all four files, and the flat queries return the same results
as the star schema queries.
