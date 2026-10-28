# SSB Query Reference

This page documents the 13 queries of the Star Schema Benchmark (SSB) as implemented in
bexhoma, driven by the [dbmsbenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker)
Python framework. The SQL below is taken from the query files in
[`experiments/ssb/`](../experiments/ssb/), which `experiments/ssb/make_queries.py` writes.

Specification: P. O'Neil, E. O'Neil, X. Chen, S. Revilak: *Star Schema Benchmark*,
Revision 3, 2009, <https://www.cs.umb.edu/~poneil/StarSchemaB.PDF>.

---

## Query Files

| Option | Schema | File |
|---|---|---|
| `-xsv normal -xqv spec` (default) | star schema | `queries-ssb.config` |
| `-xsv normal -xqv random` | star schema | `queries-ssb-random.config` |
| `-xsv flat -xqv spec` | `lineorder_flat` | `queries-ssb-flat.config` |
| `-xsv flat -xqv random` | `lineorder_flat` | `queries-ssb-flat-random.config` |

All four files have the same 13 queries in the same order, so `-xaq 1,4,7` selects Q1.1,
Q2.1 and Q3.1 in each of them. For `-xshq` each file holds 40 fixed random permutations of
the 13 queries (SSB defines no stream orderings). The same SQL runs on PostgreSQL, MonetDB and
ClickHouse; there are no per-DBMS variants. Results are compared across DBMS with
`'compare': 'result'` on sorted result sets.

The flat queries read `lineorder_flat`, which has no date dimension: year, month and week
are predicates on `lo_orderdate` (a `DATE`), and the year in the output is
`cast(extract(year from lo_orderdate) as integer)`, named `d_year` as in the star schema.
Locally at SF 1, both variants return the same results for every query.

## Deviations from the Specification

* The date dimension is the table `dates` (`date` is a reserved word).
* Q1.3 uses `lo_quantity between 26 and 35` (the specification's SQL; its text says 36-40).
* Q2.3 uses `p_brand1 = 'MFGR#2239'`: the specification's text says `MFGR#2339`, its SQL
  `MFGR#2221` (which overlaps Q2.2); ClickHouse and Doris use `MFGR#2239`.

## Random Parameters

`-xqv random` turns each query into a template (after Rabl et al., ICPE 2013, section 3.2).
Each predicate keeps the filter factor of the specification: a member of a uniform hierarchy
level is drawn from the whole level, a range over a measure keeps its width and moves, and
correlated values (a nation and its region, two cities of one nation, the first and last day of
a week) come from one `dict` parameter. Parameters are drawn once per experiment; with `-xrcp`
each stream draws its own. See [experiments/ssb/README.md](../experiments/ssb/README.md) for the
rules per query.

---

## Query Flight 1: one dimension (date) plus restrictions on the fact table

### Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)

Star schema, constants of the specification:

```sql
select sum(lo_extendedprice*lo_discount) as revenue
from lineorder, dates
where lo_orderdate = d_datekey
and d_year = 1993
and lo_discount between 1 and 3
and lo_quantity < 25
```

Flat table:

```sql
select sum(lo_extendedprice*lo_discount) as revenue
from lineorder_flat
where lo_orderdate >= date '1993-01-01' and lo_orderdate < date '1994-01-01'
and lo_discount between 1 and 3
and lo_quantity < 25
```

Random parameters, star schema: `YEAR` integer in [1993, 1997]; `DISCOUNT` integer in [2, 9]; `QUANTITY` integer in [24, 25].

```sql
select sum(lo_extendedprice*lo_discount) as revenue
from lineorder, dates
where lo_orderdate = d_datekey
and d_year = {YEAR}
and lo_discount between {DISCOUNT} - 1 and {DISCOUNT} + 1
and lo_quantity < {QUANTITY}
```

Random parameters, flat table: `YEAR1`/`YEAR2` correlated pair from a table of 5 keys (e.g. `1993` -> one of ['1994']); `DISCOUNT` integer in [2, 9]; `QUANTITY` integer in [24, 25].

```sql
select sum(lo_extendedprice*lo_discount) as revenue
from lineorder_flat
where lo_orderdate >= date '{YEAR1}-01-01' and lo_orderdate < date '{YEAR2}-01-01'
and lo_discount between {DISCOUNT} - 1 and {DISCOUNT} + 1
and lo_quantity < {QUANTITY}
```

---

### Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)

Star schema, constants of the specification:

```sql
select sum(lo_extendedprice*lo_discount) as revenue
from lineorder, dates
where lo_orderdate = d_datekey
and d_yearmonthnum = 199401
and lo_discount between 4 and 6
and lo_quantity between 26 and 35
```

Flat table:

```sql
select sum(lo_extendedprice*lo_discount) as revenue
from lineorder_flat
where lo_orderdate >= date '1994-01-01' and lo_orderdate < date '1994-02-01'
and lo_discount between 4 and 6
and lo_quantity between 26 and 35
```

Random parameters, star schema: `YEARMONTHNUM` one of 72 values (199201, 199202, 199203, ..., 199712); `DISCOUNT` integer in [2, 9]; `QUANTITY` integer in [1, 41].

```sql
select sum(lo_extendedprice*lo_discount) as revenue
from lineorder, dates
where lo_orderdate = d_datekey
and d_yearmonthnum = {YEARMONTHNUM}
and lo_discount between {DISCOUNT} - 1 and {DISCOUNT} + 1
and lo_quantity between {QUANTITY} and {QUANTITY} + 9
```

Random parameters, flat table: `MONTH1`/`MONTH2` correlated pair from a table of 72 keys (e.g. `1992-01-01` -> one of ['1992-02-01']); `DISCOUNT` integer in [2, 9]; `QUANTITY` integer in [1, 41].

```sql
select sum(lo_extendedprice*lo_discount) as revenue
from lineorder_flat
where lo_orderdate >= date '{MONTH1}' and lo_orderdate < date '{MONTH2}'
and lo_discount between {DISCOUNT} - 1 and {DISCOUNT} + 1
and lo_quantity between {QUANTITY} and {QUANTITY} + 9
```

---

### Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)

Star schema, constants of the specification:

```sql
select sum(lo_extendedprice*lo_discount) as revenue
from lineorder, dates
where lo_orderdate = d_datekey
and d_weeknuminyear = 6
and d_year = 1994
and lo_discount between 5 and 7
and lo_quantity between 26 and 35
```

Flat table:

```sql
select sum(lo_extendedprice*lo_discount) as revenue
from lineorder_flat
where lo_orderdate between date '1994-02-04' and date '1994-02-10'
and lo_discount between 5 and 7
and lo_quantity between 26 and 35
```

Random parameters, star schema: `WEEK1`/`WEEK2` correlated pair from a table of 6 keys (e.g. `1992` -> one of [2, 3, 4]...); `DISCOUNT` integer in [2, 9]; `QUANTITY` integer in [1, 41].

```sql
select sum(lo_extendedprice*lo_discount) as revenue
from lineorder, dates
where lo_orderdate = d_datekey
and d_weeknuminyear = {WEEK2}
and d_year = {WEEK1}
and lo_discount between {DISCOUNT} - 1 and {DISCOUNT} + 1
and lo_quantity between {QUANTITY} and {QUANTITY} + 9
```

Random parameters, flat table: `WEEK1`/`WEEK2` correlated pair from a table of 306 keys (e.g. `1992-01-07` -> one of ['1992-01-13']); `DISCOUNT` integer in [2, 9]; `QUANTITY` integer in [1, 41].

```sql
select sum(lo_extendedprice*lo_discount) as revenue
from lineorder_flat
where lo_orderdate between date '{WEEK1}' and date '{WEEK2}'
and lo_discount between {DISCOUNT} - 1 and {DISCOUNT} + 1
and lo_quantity between {QUANTITY} and {QUANTITY} + 9
```

---

## Query Flight 2: two dimensions (part, supplier)

### Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)

Star schema, constants of the specification:

```sql
select sum(lo_revenue) as revenue, d_year, p_brand1
from lineorder, dates, part, supplier
where lo_orderdate = d_datekey
and lo_partkey = p_partkey
and lo_suppkey = s_suppkey
and p_category = 'MFGR#12'
and s_region = 'AMERICA'
group by d_year, p_brand1
order by d_year, p_brand1
```

Flat table:

```sql
select sum(lo_revenue) as revenue, cast(extract(year from lo_orderdate) as integer) as d_year, p_brand1
from lineorder_flat
where p_category = 'MFGR#12'
and s_region = 'AMERICA'
group by cast(extract(year from lo_orderdate) as integer), p_brand1
order by d_year, p_brand1
```

Random parameters, star schema: `CATEGORY` one of 25 values (11, 12, 13, ..., 55); `REGION` one of AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST.

```sql
select sum(lo_revenue) as revenue, d_year, p_brand1
from lineorder, dates, part, supplier
where lo_orderdate = d_datekey
and lo_partkey = p_partkey
and lo_suppkey = s_suppkey
and p_category = 'MFGR#{CATEGORY}'
and s_region = '{REGION}'
group by d_year, p_brand1
order by d_year, p_brand1
```

Random parameters, flat table: `CATEGORY` one of 25 values (11, 12, 13, ..., 55); `REGION` one of AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST.

```sql
select sum(lo_revenue) as revenue, cast(extract(year from lo_orderdate) as integer) as d_year, p_brand1
from lineorder_flat
where p_category = 'MFGR#{CATEGORY}'
and s_region = '{REGION}'
group by cast(extract(year from lo_orderdate) as integer), p_brand1
order by d_year, p_brand1
```

---

### Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)

Star schema, constants of the specification:

```sql
select sum(lo_revenue) as revenue, d_year, p_brand1
from lineorder, dates, part, supplier
where lo_orderdate = d_datekey
and lo_partkey = p_partkey
and lo_suppkey = s_suppkey
and p_brand1 between 'MFGR#2221' and 'MFGR#2228'
and s_region = 'ASIA'
group by d_year, p_brand1
order by d_year, p_brand1
```

Flat table:

```sql
select sum(lo_revenue) as revenue, cast(extract(year from lo_orderdate) as integer) as d_year, p_brand1
from lineorder_flat
where p_brand1 between 'MFGR#2221' and 'MFGR#2228'
and s_region = 'ASIA'
group by cast(extract(year from lo_orderdate) as integer), p_brand1
order by d_year, p_brand1
```

Random parameters, star schema: `CATEGORY` one of 25 values (11, 12, 13, ..., 55); `BRAND1`/`BRAND2` correlated pair from a table of 9 keys (e.g. `10` -> one of ['17']); `REGION` one of AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST.

```sql
select sum(lo_revenue) as revenue, d_year, p_brand1
from lineorder, dates, part, supplier
where lo_orderdate = d_datekey
and lo_partkey = p_partkey
and lo_suppkey = s_suppkey
and p_brand1 between 'MFGR#{CATEGORY}{BRAND1}' and 'MFGR#{CATEGORY}{BRAND2}'
and s_region = '{REGION}'
group by d_year, p_brand1
order by d_year, p_brand1
```

Random parameters, flat table: `CATEGORY` one of 25 values (11, 12, 13, ..., 55); `BRAND1`/`BRAND2` correlated pair from a table of 9 keys (e.g. `10` -> one of ['17']); `REGION` one of AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST.

```sql
select sum(lo_revenue) as revenue, cast(extract(year from lo_orderdate) as integer) as d_year, p_brand1
from lineorder_flat
where p_brand1 between 'MFGR#{CATEGORY}{BRAND1}' and 'MFGR#{CATEGORY}{BRAND2}'
and s_region = '{REGION}'
group by cast(extract(year from lo_orderdate) as integer), p_brand1
order by d_year, p_brand1
```

---

### Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)

Star schema, constants of the specification:

```sql
select sum(lo_revenue) as revenue, d_year, p_brand1
from lineorder, dates, part, supplier
where lo_orderdate = d_datekey
and lo_partkey = p_partkey
and lo_suppkey = s_suppkey
and p_brand1 = 'MFGR#2239'
and s_region = 'EUROPE'
group by d_year, p_brand1
order by d_year, p_brand1
```

Flat table:

```sql
select sum(lo_revenue) as revenue, cast(extract(year from lo_orderdate) as integer) as d_year, p_brand1
from lineorder_flat
where p_brand1 = 'MFGR#2239'
and s_region = 'EUROPE'
group by cast(extract(year from lo_orderdate) as integer), p_brand1
order by d_year, p_brand1
```

Random parameters, star schema: `CATEGORY` one of 25 values (11, 12, 13, ..., 55); `BRAND` integer in [1, 40]; `REGION` one of AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST.

```sql
select sum(lo_revenue) as revenue, d_year, p_brand1
from lineorder, dates, part, supplier
where lo_orderdate = d_datekey
and lo_partkey = p_partkey
and lo_suppkey = s_suppkey
and p_brand1 = 'MFGR#{CATEGORY}{BRAND}'
and s_region = '{REGION}'
group by d_year, p_brand1
order by d_year, p_brand1
```

Random parameters, flat table: `CATEGORY` one of 25 values (11, 12, 13, ..., 55); `BRAND` integer in [1, 40]; `REGION` one of AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST.

```sql
select sum(lo_revenue) as revenue, cast(extract(year from lo_orderdate) as integer) as d_year, p_brand1
from lineorder_flat
where p_brand1 = 'MFGR#{CATEGORY}{BRAND}'
and s_region = '{REGION}'
group by cast(extract(year from lo_orderdate) as integer), p_brand1
order by d_year, p_brand1
```

---

## Query Flight 3: three dimensions (customer, supplier, date)

### Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)

Star schema, constants of the specification:

```sql
select c_nation, s_nation, d_year, sum(lo_revenue) as revenue
from customer, lineorder, supplier, dates
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_orderdate = d_datekey
and c_region = 'ASIA'
and s_region = 'ASIA'
and d_year >= 1992 and d_year <= 1997
group by c_nation, s_nation, d_year
order by d_year asc, revenue desc
```

Flat table:

```sql
select c_nation, s_nation, cast(extract(year from lo_orderdate) as integer) as d_year, sum(lo_revenue) as revenue
from lineorder_flat
where c_region = 'ASIA'
and s_region = 'ASIA'
and lo_orderdate >= date '1992-01-01' and lo_orderdate < date '1998-01-01'
group by c_nation, s_nation, cast(extract(year from lo_orderdate) as integer)
order by d_year asc, revenue desc
```

Random parameters, star schema: `REGION` one of AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST.

```sql
select c_nation, s_nation, d_year, sum(lo_revenue) as revenue
from customer, lineorder, supplier, dates
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_orderdate = d_datekey
and c_region = '{REGION}'
and s_region = '{REGION}'
and d_year >= 1992 and d_year <= 1997
group by c_nation, s_nation, d_year
order by d_year asc, revenue desc
```

Random parameters, flat table: `REGION` one of AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST.

```sql
select c_nation, s_nation, cast(extract(year from lo_orderdate) as integer) as d_year, sum(lo_revenue) as revenue
from lineorder_flat
where c_region = '{REGION}'
and s_region = '{REGION}'
and lo_orderdate >= date '1992-01-01' and lo_orderdate < date '1998-01-01'
group by c_nation, s_nation, cast(extract(year from lo_orderdate) as integer)
order by d_year asc, revenue desc
```

---

### Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)

Star schema, constants of the specification:

```sql
select c_city, s_city, d_year, sum(lo_revenue) as revenue
from customer, lineorder, supplier, dates
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_orderdate = d_datekey
and c_nation = 'UNITED STATES'
and s_nation = 'UNITED STATES'
and d_year >= 1992 and d_year <= 1997
group by c_city, s_city, d_year
order by d_year asc, revenue desc
```

Flat table:

```sql
select c_city, s_city, cast(extract(year from lo_orderdate) as integer) as d_year, sum(lo_revenue) as revenue
from lineorder_flat
where c_nation = 'UNITED STATES'
and s_nation = 'UNITED STATES'
and lo_orderdate >= date '1992-01-01' and lo_orderdate < date '1998-01-01'
group by c_city, s_city, cast(extract(year from lo_orderdate) as integer)
order by d_year asc, revenue desc
```

Random parameters, star schema: `NATION` one of 25 values (ALGERIA, ARGENTINA, BRAZIL, ..., VIETNAM).

```sql
select c_city, s_city, d_year, sum(lo_revenue) as revenue
from customer, lineorder, supplier, dates
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_orderdate = d_datekey
and c_nation = '{NATION}'
and s_nation = '{NATION}'
and d_year >= 1992 and d_year <= 1997
group by c_city, s_city, d_year
order by d_year asc, revenue desc
```

Random parameters, flat table: `NATION` one of 25 values (ALGERIA, ARGENTINA, BRAZIL, ..., VIETNAM).

```sql
select c_city, s_city, cast(extract(year from lo_orderdate) as integer) as d_year, sum(lo_revenue) as revenue
from lineorder_flat
where c_nation = '{NATION}'
and s_nation = '{NATION}'
and lo_orderdate >= date '1992-01-01' and lo_orderdate < date '1998-01-01'
group by c_city, s_city, cast(extract(year from lo_orderdate) as integer)
order by d_year asc, revenue desc
```

---

### Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)

Star schema, constants of the specification:

```sql
select c_city, s_city, d_year, sum(lo_revenue) as revenue
from customer, lineorder, supplier, dates
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_orderdate = d_datekey
and (c_city = 'UNITED KI1' or c_city = 'UNITED KI5')
and (s_city = 'UNITED KI1' or s_city = 'UNITED KI5')
and d_year >= 1992 and d_year <= 1997
group by c_city, s_city, d_year
order by d_year asc, revenue desc
```

Flat table:

```sql
select c_city, s_city, cast(extract(year from lo_orderdate) as integer) as d_year, sum(lo_revenue) as revenue
from lineorder_flat
where (c_city = 'UNITED KI1' or c_city = 'UNITED KI5')
and (s_city = 'UNITED KI1' or s_city = 'UNITED KI5')
and lo_orderdate >= date '1992-01-01' and lo_orderdate < date '1998-01-01'
group by c_city, s_city, cast(extract(year from lo_orderdate) as integer)
order by d_year asc, revenue desc
```

Random parameters, star schema: `CITY1`/`CITY2` correlated pair from a table of 250 keys (e.g. `ALGERIA  0` -> one of ['ALGERIA  1', 'ALGERIA  2', 'ALGERIA  3']...).

```sql
select c_city, s_city, d_year, sum(lo_revenue) as revenue
from customer, lineorder, supplier, dates
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_orderdate = d_datekey
and (c_city = '{CITY1}' or c_city = '{CITY2}')
and (s_city = '{CITY1}' or s_city = '{CITY2}')
and d_year >= 1992 and d_year <= 1997
group by c_city, s_city, d_year
order by d_year asc, revenue desc
```

Random parameters, flat table: `CITY1`/`CITY2` correlated pair from a table of 250 keys (e.g. `ALGERIA  0` -> one of ['ALGERIA  1', 'ALGERIA  2', 'ALGERIA  3']...).

```sql
select c_city, s_city, cast(extract(year from lo_orderdate) as integer) as d_year, sum(lo_revenue) as revenue
from lineorder_flat
where (c_city = '{CITY1}' or c_city = '{CITY2}')
and (s_city = '{CITY1}' or s_city = '{CITY2}')
and lo_orderdate >= date '1992-01-01' and lo_orderdate < date '1998-01-01'
group by c_city, s_city, cast(extract(year from lo_orderdate) as integer)
order by d_year asc, revenue desc
```

---

### Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)

Star schema, constants of the specification:

```sql
select c_city, s_city, d_year, sum(lo_revenue) as revenue
from customer, lineorder, supplier, dates
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_orderdate = d_datekey
and (c_city = 'UNITED KI1' or c_city = 'UNITED KI5')
and (s_city = 'UNITED KI1' or s_city = 'UNITED KI5')
and d_yearmonth = 'Dec1997'
group by c_city, s_city, d_year
order by d_year asc, revenue desc
```

Flat table:

```sql
select c_city, s_city, cast(extract(year from lo_orderdate) as integer) as d_year, sum(lo_revenue) as revenue
from lineorder_flat
where (c_city = 'UNITED KI1' or c_city = 'UNITED KI5')
and (s_city = 'UNITED KI1' or s_city = 'UNITED KI5')
and lo_orderdate >= date '1997-12-01' and lo_orderdate < date '1998-01-01'
group by c_city, s_city, cast(extract(year from lo_orderdate) as integer)
order by d_year asc, revenue desc
```

Random parameters, star schema: `CITY1`/`CITY2` correlated pair from a table of 250 keys (e.g. `ALGERIA  0` -> one of ['ALGERIA  1', 'ALGERIA  2', 'ALGERIA  3']...); `YEARMONTH` one of 72 values (Jan1992, Feb1992, Mar1992, ..., Dec1997).

```sql
select c_city, s_city, d_year, sum(lo_revenue) as revenue
from customer, lineorder, supplier, dates
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_orderdate = d_datekey
and (c_city = '{CITY1}' or c_city = '{CITY2}')
and (s_city = '{CITY1}' or s_city = '{CITY2}')
and d_yearmonth = '{YEARMONTH}'
group by c_city, s_city, d_year
order by d_year asc, revenue desc
```

Random parameters, flat table: `CITY1`/`CITY2` correlated pair from a table of 250 keys (e.g. `ALGERIA  0` -> one of ['ALGERIA  1', 'ALGERIA  2', 'ALGERIA  3']...); `MONTH1`/`MONTH2` correlated pair from a table of 72 keys (e.g. `1992-01-01` -> one of ['1992-02-01']).

```sql
select c_city, s_city, cast(extract(year from lo_orderdate) as integer) as d_year, sum(lo_revenue) as revenue
from lineorder_flat
where (c_city = '{CITY1}' or c_city = '{CITY2}')
and (s_city = '{CITY1}' or s_city = '{CITY2}')
and lo_orderdate >= date '{MONTH1}' and lo_orderdate < date '{MONTH2}'
group by c_city, s_city, cast(extract(year from lo_orderdate) as integer)
order by d_year asc, revenue desc
```

---

## Query Flight 4: four dimensions, profit (what-if)

### Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)

Star schema, constants of the specification:

```sql
select d_year, c_nation, sum(lo_revenue - lo_supplycost) as profit
from dates, customer, supplier, part, lineorder
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_partkey = p_partkey
and lo_orderdate = d_datekey
and c_region = 'AMERICA'
and s_region = 'AMERICA'
and (p_mfgr = 'MFGR#1' or p_mfgr = 'MFGR#2')
group by d_year, c_nation
order by d_year, c_nation
```

Flat table:

```sql
select cast(extract(year from lo_orderdate) as integer) as d_year, c_nation, sum(lo_revenue - lo_supplycost) as profit
from lineorder_flat
where c_region = 'AMERICA'
and s_region = 'AMERICA'
and (p_mfgr = 'MFGR#1' or p_mfgr = 'MFGR#2')
group by cast(extract(year from lo_orderdate) as integer), c_nation
order by d_year, c_nation
```

Random parameters, star schema: `REGION` one of AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST; `MFGR` integer in [1, 5], 2 distinct values (`MFGR1`, `MFGR2`).

```sql
select d_year, c_nation, sum(lo_revenue - lo_supplycost) as profit
from dates, customer, supplier, part, lineorder
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_partkey = p_partkey
and lo_orderdate = d_datekey
and c_region = '{REGION}'
and s_region = '{REGION}'
and (p_mfgr = 'MFGR#{MFGR1}' or p_mfgr = 'MFGR#{MFGR2}')
group by d_year, c_nation
order by d_year, c_nation
```

Random parameters, flat table: `REGION` one of AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST; `MFGR` integer in [1, 5], 2 distinct values (`MFGR1`, `MFGR2`).

```sql
select cast(extract(year from lo_orderdate) as integer) as d_year, c_nation, sum(lo_revenue - lo_supplycost) as profit
from lineorder_flat
where c_region = '{REGION}'
and s_region = '{REGION}'
and (p_mfgr = 'MFGR#{MFGR1}' or p_mfgr = 'MFGR#{MFGR2}')
group by cast(extract(year from lo_orderdate) as integer), c_nation
order by d_year, c_nation
```

---

### Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)

Star schema, constants of the specification:

```sql
select d_year, s_nation, p_category, sum(lo_revenue - lo_supplycost) as profit
from dates, customer, supplier, part, lineorder
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_partkey = p_partkey
and lo_orderdate = d_datekey
and c_region = 'AMERICA'
and s_region = 'AMERICA'
and (p_mfgr = 'MFGR#1' or p_mfgr = 'MFGR#2')
and (d_year = 1997 or d_year = 1998)
group by d_year, s_nation, p_category
order by d_year, s_nation, p_category
```

Flat table:

```sql
select cast(extract(year from lo_orderdate) as integer) as d_year, s_nation, p_category, sum(lo_revenue - lo_supplycost) as profit
from lineorder_flat
where c_region = 'AMERICA'
and s_region = 'AMERICA'
and (p_mfgr = 'MFGR#1' or p_mfgr = 'MFGR#2')
and lo_orderdate >= date '1997-01-01' and lo_orderdate < date '1999-01-01'
group by cast(extract(year from lo_orderdate) as integer), s_nation, p_category
order by d_year, s_nation, p_category
```

Random parameters, star schema: `REGION` one of AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST; `MFGR` integer in [1, 5], 2 distinct values (`MFGR1`, `MFGR2`); `YEAR` integer in [1992, 1997].

```sql
select d_year, s_nation, p_category, sum(lo_revenue - lo_supplycost) as profit
from dates, customer, supplier, part, lineorder
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_partkey = p_partkey
and lo_orderdate = d_datekey
and c_region = '{REGION}'
and s_region = '{REGION}'
and (p_mfgr = 'MFGR#{MFGR1}' or p_mfgr = 'MFGR#{MFGR2}')
and (d_year = {YEAR} or d_year = {YEAR} + 1)
group by d_year, s_nation, p_category
order by d_year, s_nation, p_category
```

Random parameters, flat table: `REGION` one of AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST; `MFGR` integer in [1, 5], 2 distinct values (`MFGR1`, `MFGR2`); `YEAR1`/`YEAR2` correlated pair from a table of 6 keys (e.g. `1992` -> one of ['1994']).

```sql
select cast(extract(year from lo_orderdate) as integer) as d_year, s_nation, p_category, sum(lo_revenue - lo_supplycost) as profit
from lineorder_flat
where c_region = '{REGION}'
and s_region = '{REGION}'
and (p_mfgr = 'MFGR#{MFGR1}' or p_mfgr = 'MFGR#{MFGR2}')
and lo_orderdate >= date '{YEAR1}-01-01' and lo_orderdate < date '{YEAR2}-01-01'
group by cast(extract(year from lo_orderdate) as integer), s_nation, p_category
order by d_year, s_nation, p_category
```

---

### Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)

Star schema, constants of the specification:

```sql
select d_year, s_city, p_brand1, sum(lo_revenue - lo_supplycost) as profit
from dates, customer, supplier, part, lineorder
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_partkey = p_partkey
and lo_orderdate = d_datekey
and c_region = 'AMERICA'
and s_nation = 'UNITED STATES'
and p_category = 'MFGR#14'
and (d_year = 1997 or d_year = 1998)
group by d_year, s_city, p_brand1
order by d_year, s_city, p_brand1
```

Flat table:

```sql
select cast(extract(year from lo_orderdate) as integer) as d_year, s_city, p_brand1, sum(lo_revenue - lo_supplycost) as profit
from lineorder_flat
where c_region = 'AMERICA'
and s_nation = 'UNITED STATES'
and p_category = 'MFGR#14'
and lo_orderdate >= date '1997-01-01' and lo_orderdate < date '1999-01-01'
group by cast(extract(year from lo_orderdate) as integer), s_city, p_brand1
order by d_year, s_city, p_brand1
```

Random parameters, star schema: `NATION1`/`NATION2` correlated pair from a table of 5 keys (e.g. `AFRICA` -> one of ['ALGERIA', 'ETHIOPIA', 'KENYA']...); `CATEGORY` one of 25 values (11, 12, 13, ..., 55); `YEAR` integer in [1992, 1997].

```sql
select d_year, s_city, p_brand1, sum(lo_revenue - lo_supplycost) as profit
from dates, customer, supplier, part, lineorder
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_partkey = p_partkey
and lo_orderdate = d_datekey
and c_region = '{NATION1}'
and s_nation = '{NATION2}'
and p_category = 'MFGR#{CATEGORY}'
and (d_year = {YEAR} or d_year = {YEAR} + 1)
group by d_year, s_city, p_brand1
order by d_year, s_city, p_brand1
```

Random parameters, flat table: `NATION1`/`NATION2` correlated pair from a table of 5 keys (e.g. `AFRICA` -> one of ['ALGERIA', 'ETHIOPIA', 'KENYA']...); `CATEGORY` one of 25 values (11, 12, 13, ..., 55); `YEAR1`/`YEAR2` correlated pair from a table of 6 keys (e.g. `1992` -> one of ['1994']).

```sql
select cast(extract(year from lo_orderdate) as integer) as d_year, s_city, p_brand1, sum(lo_revenue - lo_supplycost) as profit
from lineorder_flat
where c_region = '{NATION1}'
and s_nation = '{NATION2}'
and p_category = 'MFGR#{CATEGORY}'
and lo_orderdate >= date '{YEAR1}-01-01' and lo_orderdate < date '{YEAR2}-01-01'
group by cast(extract(year from lo_orderdate) as integer), s_city, p_brand1
order by d_year, s_city, p_brand1
```

---
