# TPC-H Query Reference

This page documents the 22 TPC-H reading queries as implemented in bexhoma, driven by the
[dbmsbenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) Python framework.

> The query file is derived from the TPC-H benchmark and as such is **not comparable to published
> TPC-H results**, as the query file results do not comply with the TPC-H Specification.
> Official TPC-H benchmark: <http://www.tpc.org/tpch>

---

## Configuration Structure

Queries are defined in [`experiments/tpch/queries-tpch.config`](../experiments/tpch/queries-tpch.config)
as a Python dict conforming to the dbmsbenchmarker format.

### Top-level fields

| Field | Value | Meaning |
|---|---|---|
| `name` | `"The TPC-H Queries"` | Experiment name shown in reports |
| `factor` | `"mean"` | Aggregation factor for multi-run results |
| `connectionmanagement.timeout` | `1200` | Per-query timeout in seconds |
| `connectionmanagement.numProcesses` | `1` | Parallel benchmark processes |
| `connectionmanagement.runsPerConnection` | `0` | 0 = new connection per run |
| `connectionmanagement.singleConnection` | `True` | Reuse one connection per DBMS |
| `stream_ordering` | dict | TPC-H stream orderings 1–40, each a permutation of Q1–Q22 |

### Per-query fields

| Field | Meaning |
|---|---|
| `title` | Display name shown in the report |
| `query` | Default SQL, used unless the active DBMS has an entry in `DBMS` |
| `DBMS` | Dict of DBMS-name → SQL override (or list of SQL statements for multi-step queries) |
| `parameter` | Dict of substitution parameters, each with `type` and `range` |
| `active` | Whether the query runs in this experiment |
| `numWarmup` | Number of warm-up runs (not measured) |
| `numCooldown` | Number of cool-down runs (not measured) |
| `numRun` | Number of measured runs |
| `timer.datatransfer.compare` | How results are compared across DBMS (`"result"` = exact row-set match) |
| `timer.datatransfer.sorted` | Whether results are sorted before comparison |
| `timer.datatransfer.precision` | Decimal places for floating-point result comparison |

### Placeholder convention

The TPC-H specification uses `:N` positional placeholders (e.g., `:1`, `:2`).
Bexhoma uses named placeholders in curly braces (e.g., `{DATE}`, `{REGION}`).

| TPC-H spec | Bexhoma equivalent |
|---|---|
| `:1` (first parameter) | `{PARAM_NAME}` |
| `:n 100` (return 100 rows) | `limit 100` appended to query |
| `create view revenue:s …` | CTE `with revenue … as (…)` or view with `{numRun}{STREAM}` suffix |

---

## Q1 – Pricing Summary Report Query

Summary pricing report for all lineitems shipped as of a given date (60–120 days before the
greatest ship date in the database).

**Parameters:**

| bexhoma | TPC-H | Type | Range |
|---|---|---|---|
| `{DELTA}` | `:1` | integer | [60, 120] |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
l_returnflag,
l_linestatus,
sum(l_quantity) as sum_qty,
sum(l_extendedprice) as sum_base_price,
sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
lineitem
where
l_shipdate <= date '1998-12-01' - interval '[DELTA]' day (3)
group by
l_returnflag,
l_linestatus
order by
l_returnflag,
l_linestatus;
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB (adds <code>cast(sum_qty as bigint)</code>)</summary>

```sql
select
l_returnflag,
l_linestatus,
cast(sum(l_quantity) as bigint) as sum_qty,
sum(l_extendedprice) as sum_base_price,
sum(l_extendedprice*(1-l_discount)) as sum_disc_price,
sum(l_extendedprice*(1-l_discount)*(1+l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
lineitem
where
l_shipdate <= date '1998-12-01' - interval '{DELTA}' day
group by
l_returnflag,
l_linestatus
order by
l_returnflag,
l_linestatus
```

</details>

<details>
<summary>MySQL — <code>date('…')</code> syntax; <code>cast(… as unsigned int)</code>; <code>limit 10000000</code></summary>

```sql
select
l_returnflag,
l_linestatus,
cast(sum(l_quantity) as unsigned int) as sum_qty,
sum(l_extendedprice) as sum_base_price,
sum(l_extendedprice*(1-l_discount)) as sum_disc_price,
sum(l_extendedprice*(1-l_discount)*(1+l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
lineitem
where
l_shipdate <= date('1998-12-01') - interval '{DELTA}' day
group by
l_returnflag,
l_linestatus
order by
l_returnflag,
l_linestatus
limit 10000000
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>dateadd(dd, -{DELTA}, …)</code></summary>

```sql
select
l_returnflag,
l_linestatus,
cast(sum(l_quantity) as bigint) as sum_qty,
sum(l_extendedprice) as sum_base_price,
sum(l_extendedprice*(1-l_discount)) as sum_disc_price,
sum(l_extendedprice*(1-l_discount)*(1+l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
lineitem
where
l_shipdate <= dateadd(dd, -{DELTA}, cast('1998-12-01' as date))
group by
l_returnflag,
l_linestatus
order by
l_returnflag,
l_linestatus
```

</details>

<details>
<summary>MonetDB — <code>cast(sum_charge as double)</code> to avoid overflow</summary>

```sql
select
l_returnflag,
l_linestatus,
cast(sum(l_quantity) as bigint) as sum_qty,
sum(l_extendedprice) as sum_base_price,
sum(l_extendedprice*(1-l_discount)) as sum_disc_price,
sum(cast(l_extendedprice*(1-l_discount)*(1+l_tax) as double)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
lineitem
where
l_shipdate <= date '1998-12-01' - interval '{DELTA}' day
group by
l_returnflag,
l_linestatus
order by
l_returnflag,
l_linestatus
```

</details>

<details>
<summary>SAP HANA — <code>add_days(to_date('1998-12-01'), -{DELTA})</code></summary>

```sql
select
l_returnflag,
l_linestatus,
cast(sum(l_quantity) as bigint) as sum_qty,
sum(l_extendedprice) as sum_base_price,
sum(l_extendedprice*(1-l_discount)) as sum_disc_price,
sum(l_extendedprice*(1-l_discount)*(1+l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
lineitem
where
l_shipdate <= add_days(to_date('1998-12-01'), -{DELTA})
group by
l_returnflag,
l_linestatus
order by
l_returnflag,
l_linestatus
```

</details>

<details>
<summary>DB2 — <code>date '…' - {DELTA} day</code> (no <code>interval</code> keyword)</summary>

```sql
select
l_returnflag,
l_linestatus,
cast(sum(l_quantity) as bigint) as sum_qty,
sum(l_extendedprice) as sum_base_price,
sum(l_extendedprice*(1-l_discount)) as sum_disc_price,
sum(l_extendedprice*(1-l_discount)*(1+l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
avg(l_extendedprice) as avg_price,
avg(l_discount) as avg_disc,
count(*) as count_order
from
lineitem
where
l_shipdate <= date '1998-12-01' - {DELTA} day
group by
l_returnflag,
l_linestatus
order by
l_returnflag,
l_linestatus
```

</details>

---

## Q2 – Minimum Cost Supplier Query

Finds which supplier should be selected to place an order for a given part in a given region.
Returns the first 100 rows.

**Parameters:**

| bexhoma | TPC-H | Type | Range / Values |
|---|---|---|---|
| `{SIZE}` | `:1` | integer | [1, 50] |
| `{TYPE3}` | `:2` (syllable 3 of type) | list | TIN, NICKEL, BRASS, STEEL, COPPER |
| `{REGION}` | `:3` | list | AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment
from
part, supplier, partsupp, nation, region
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = [SIZE]
and p_type like '%[TYPE]'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '[REGION]'
and ps_supplycost = (
select min(ps_supplycost)
from partsupp, supplier, nation, region
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '[REGION]'
)
order by s_acctbal desc, n_name, s_name, p_partkey;
-- :n 100
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MySQL, MariaDB; correlated subquery; <code>limit 100</code></summary>

```sql
select
s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment
from
part, supplier, partsupp, nation, region
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = {SIZE}
and p_type like '%{TYPE3}'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '{REGION}'
and ps_supplycost = (
select min(ps_supplycost)
from partsupp, supplier, nation, region
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '{REGION}'
)
order by s_acctbal desc, n_name, s_name, p_partkey
limit 100
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>select top 100</code></summary>

```sql
select top 100
s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment
from
part, supplier, partsupp, nation, region
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = {SIZE}
and p_type like '%{TYPE3}'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '{REGION}'
and ps_supplycost = (
select min(ps_supplycost)
from partsupp, supplier, nation, region
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '{REGION}'
)
order by s_acctbal desc, n_name, s_name, p_partkey
```

</details>

<details>
<summary>Oracle — <code>fetch next 100 rows only</code></summary>

```sql
select
s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment
from
part, supplier, partsupp, nation, region
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and p_size = {SIZE}
and p_type like '%{TYPE3}'
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '{REGION}'
and ps_supplycost = (
select min(ps_supplycost)
from partsupp, supplier, nation, region
where
p_partkey = ps_partkey
and s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '{REGION}'
)
order by s_acctbal desc, n_name, s_name, p_partkey
fetch next 100 rows only
```

</details>

<details>
<summary>OmniSci / Clickhouse / MariaDBCS — correlated subquery rewritten as CTE</summary>

```sql
with subquery as (
select
ps_partkey as subq_ps_partkey,
min(ps_supplycost) as min_ps_supplicost
from
partsupp, supplier, nation, region
where
s_suppkey = ps_suppkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '{REGION}'
group by subq_ps_partkey
)
select
s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, s_phone, s_comment
from
part join
partsupp on p_partkey = ps_partkey join
supplier on s_suppkey = ps_suppkey join
nation on s_nationkey = n_nationkey join
region on n_regionkey = r_regionkey join
subquery on subq_ps_partkey = ps_partkey
where
ps_supplycost = min_ps_supplicost
and p_size = {SIZE}
and p_type like '%{TYPE3}'
and r_name = '{REGION}'
order by s_acctbal desc, n_name, s_name, p_partkey
limit 100
```

</details>

---

## Q3 – Shipping Priority Query

Retrieves the 10 unshipped orders with the highest value. Returns the first 10 rows.

**Parameters:**

| bexhoma | TPC-H | Type | Range / Values |
|---|---|---|---|
| `{SEGMENT}` | `:1` | list | AUTOMOBILE, BUILDING, FURNITURE, MACHINERY, HOUSEHOLD |
| `{DATE}` | `:2` | date | [1995-03-01, 1995-03-31] |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
l_orderkey,
sum(l_extendedprice*(1-l_discount)) as revenue,
o_orderdate,
o_shippriority
from
customer, orders, lineitem
where
c_mktsegment = '[SEGMENT]'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '[DATE]'
and l_shipdate > date '[DATE]'
group by l_orderkey, o_orderdate, o_shippriority
order by revenue desc, o_orderdate;
-- :n 10
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB; <code>limit 10</code></summary>

```sql
select
l_orderkey,
sum(l_extendedprice*(1-l_discount)) as revenue,
o_orderdate,
o_shippriority
from
customer, orders, lineitem
where
c_mktsegment = '{SEGMENT}'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '{DATE}'
and l_shipdate > date '{DATE}'
group by l_orderkey, o_orderdate, o_shippriority
order by revenue desc, o_orderdate
limit 10
```

</details>

<details>
<summary>MySQL — <code>date('…')</code> function syntax</summary>

```sql
select
l_orderkey,
sum(l_extendedprice*(1-l_discount)) as revenue,
o_orderdate,
o_shippriority
from
customer, orders, lineitem
where
c_mktsegment = '{SEGMENT}'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date('{DATE}')
and l_shipdate > date('{DATE}')
group by l_orderkey, o_orderdate, o_shippriority
order by revenue desc, o_orderdate
limit 10
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>select top 10</code>; <code>cast('…' as date)</code></summary>

```sql
select top 10
l_orderkey,
sum(l_extendedprice*(1-l_discount)) as revenue,
o_orderdate,
o_shippriority
from
customer, orders, lineitem
where
c_mktsegment = '{SEGMENT}'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < cast('{DATE}' as date)
and l_shipdate > cast('{DATE}' as date)
group by l_orderkey, o_orderdate, o_shippriority
order by revenue desc, o_orderdate
```

</details>

<details>
<summary>Oracle — <code>fetch next 10 rows only</code></summary>

```sql
select
l_orderkey,
sum(l_extendedprice*(1-l_discount)) as revenue,
o_orderdate,
o_shippriority
from
customer, orders, lineitem
where
c_mktsegment = '{SEGMENT}'
and c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate < date '{DATE}'
and l_shipdate > date '{DATE}'
group by l_orderkey, o_orderdate, o_shippriority
order by revenue desc, o_orderdate
fetch next 10 rows only
```

</details>

---

## Q4 – Order Priority Checking Query

Counts orders in a given quarter where at least one lineitem was received later than its
committed date, to assess order priority system effectiveness.

**Parameters:**

| bexhoma | TPC-H | Type | Range |
|---|---|---|---|
| `{DATE}` | `:1` | firstofmonth | [1993-01-01, 1997-10-01] |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
o_orderpriority,
count(*) as order_count
from orders
where
o_orderdate >= date '[DATE]'
and o_orderdate < date '[DATE]' + interval '3' month
and exists (
select * from lineitem
where l_orderkey = o_orderkey and l_commitdate < l_receiptdate
)
group by o_orderpriority
order by o_orderpriority;
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB</summary>

```sql
select
o_orderpriority,
count(*) as order_count
from orders
where
o_orderdate >= date '{DATE}'
and o_orderdate < date '{DATE}' + interval '3' month
and exists (
select * from lineitem
where l_orderkey = o_orderkey and l_commitdate < l_receiptdate
)
group by o_orderpriority
order by o_orderpriority
```

</details>

<details>
<summary>MySQL — <code>date('…')</code> function syntax</summary>

```sql
select
o_orderpriority,
count(*) as order_count
from orders
where
o_orderdate >= date('{DATE}')
and o_orderdate < date('{DATE}') + interval '3' month
and exists (
select * from lineitem
where l_orderkey = o_orderkey and l_commitdate < l_receiptdate
)
group by o_orderpriority
order by o_orderpriority
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>dateadd(mm, +3, …)</code></summary>

```sql
select
o_orderpriority,
count(*) as order_count
from orders
where
o_orderdate >= cast('{DATE}' as date)
and o_orderdate < dateadd(mm, +3, cast('{DATE}' as date))
and exists (
select * from lineitem
where l_orderkey = o_orderkey and l_commitdate < l_receiptdate
)
group by o_orderpriority
order by o_orderpriority
```

</details>

<details>
<summary>SAP HANA — <code>add_months(to_date(…), 3)</code></summary>

```sql
select
o_orderpriority,
count(*) as order_count
from orders
where
o_orderdate >= date '{DATE}'
and o_orderdate < add_months(to_date('{DATE}'), 3)
and exists (
select * from lineitem
where l_orderkey = o_orderkey and l_commitdate < l_receiptdate
)
group by o_orderpriority
order by o_orderpriority
```

</details>

<details>
<summary>DB2 — <code>date '…' + 3 month</code></summary>

```sql
select
o_orderpriority,
count(*) as order_count
from orders
where
o_orderdate >= date '{DATE}'
and o_orderdate < date '{DATE}' + 3 month
and exists (
select * from lineitem
where l_orderkey = o_orderkey and l_commitdate < l_receiptdate
)
group by o_orderpriority
order by o_orderpriority
```

</details>

<details>
<summary>Citus — <code>exists</code> rewritten as plain join (Citus correlated-subquery limitation)</summary>

```sql
select
o_orderpriority,
count(*) as order_count
from orders, lineitem
where
o_orderdate >= date('{DATE}')
and o_orderdate < date('{DATE}') + interval '3' month
and l_orderkey = o_orderkey
and l_commitdate < l_receiptdate
group by o_orderpriority
order by o_orderpriority
```

</details>

---

## Q5 – Local Supplier Volume Query

Lists the revenue volume done through local suppliers where both customer and supplier are in
the same nation, for a given region and year.

**Parameters:**

| bexhoma | TPC-H | Type | Range / Values |
|---|---|---|---|
| `{REGION}` | `:1` | list | AFRICA, AMERICA, ASIA, EUROPE, MIDDLE EAST |
| `{DATE}` | `:2` | firstofyear | [1993, 1997] |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
n_name,
sum(l_extendedprice * (1 - l_discount)) as revenue
from
customer, orders, lineitem, supplier, nation, region
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '[REGION]'
and o_orderdate >= date '[DATE]'
and o_orderdate < date '[DATE]' + interval '1' year
group by n_name
order by revenue desc;
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB</summary>

```sql
select
n_name,
sum(l_extendedprice * (1 - l_discount)) as revenue
from
customer, orders, lineitem, supplier, nation, region
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '{REGION}'
and o_orderdate >= date '{DATE}'
and o_orderdate < date '{DATE}' + interval '1' year
group by n_name
order by revenue desc
```

</details>

<details>
<summary>MySQL — <code>date('…')</code> function syntax</summary>

```sql
select
n_name,
sum(l_extendedprice * (1 - l_discount)) as revenue
from
customer, orders, lineitem, supplier, nation, region
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '{REGION}'
and o_orderdate >= date('{DATE}')
and o_orderdate < date('{DATE}') + interval '1' year
group by n_name
order by revenue desc
```

</details>

<details>
<summary>MariaDBCS — adds <code>+0</code> to <code>c_nationkey</code> to disable index (ColumnStore optimizer workaround)</summary>

```sql
select
n_name,
sum(l_extendedprice * (1 - l_discount)) as revenue
from
customer, orders, lineitem, supplier, nation, region
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey+0
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '{REGION}'
and o_orderdate >= date('{DATE}')
and o_orderdate < date('{DATE}') + interval '1' year
group by n_name
order by revenue desc
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>dateadd(yy, +1, …)</code></summary>

```sql
select
n_name,
sum(l_extendedprice * (1 - l_discount)) as revenue
from
customer, orders, lineitem, supplier, nation, region
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '{REGION}'
and o_orderdate >= cast('{DATE}' as date)
and o_orderdate < dateadd(yy, +1, cast('{DATE}' as date))
group by n_name
order by revenue desc
```

</details>

<details>
<summary>SAP HANA — <code>add_years(to_date(…), 1)</code></summary>

```sql
select
n_name,
sum(l_extendedprice * (1 - l_discount)) as revenue
from
customer, orders, lineitem, supplier, nation, region
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '{REGION}'
and o_orderdate >= to_date('{DATE}')
and o_orderdate < add_years(to_date('{DATE}'),1)
group by n_name
order by revenue desc
```

</details>

<details>
<summary>DB2 — <code>date '…' + 1 year</code></summary>

```sql
select
n_name,
sum(l_extendedprice * (1 - l_discount)) as revenue
from
customer, orders, lineitem, supplier, nation, region
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = '{REGION}'
and o_orderdate >= date '{DATE}'
and o_orderdate < date '{DATE}' + 1 year
group by n_name
order by revenue desc
```

</details>

---

## Q6 – Forecasting Revenue Change Query

Quantifies the revenue increase from eliminating discounts in a given range during a given year.

**Parameters:**

| bexhoma | TPC-H | Type | Range |
|---|---|---|---|
| `{DATE}` | `:1` | firstofyear | [1993, 1997] |
| `{DISCOUNT}` | `:2` | float | [0.02, 0.09] |
| `{QUANTITY}` | `:3` | integer | [24, 25] |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
sum(l_extendedprice * l_discount) as revenue
from lineitem
where
l_shipdate >= date '[DATE]'
and l_shipdate < date '[DATE]' + interval '1' year
and l_discount between [DISCOUNT] - 0.01 and [DISCOUNT] + 0.01
and l_quantity < [QUANTITY];
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB</summary>

```sql
select
sum(l_extendedprice*l_discount) as revenue
from lineitem
where
l_shipdate >= date '{DATE}'
and l_shipdate < date '{DATE}' + interval '1' year
and l_discount between {DISCOUNT} - 0.01 and {DISCOUNT} + 0.01
and l_quantity < {QUANTITY}
```

</details>

<details>
<summary>MySQL — <code>date('…')</code> function syntax</summary>

```sql
select
sum(l_extendedprice*l_discount) as revenue
from lineitem
where
l_shipdate >= date('{DATE}')
and l_shipdate < date('{DATE}') + interval '1' year
and l_discount between {DISCOUNT} - 0.01 and {DISCOUNT} + 0.01
and l_quantity < {QUANTITY}
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>dateadd(yy, +1, …)</code></summary>

```sql
select
sum(l_extendedprice*l_discount) as revenue
from lineitem
where
l_shipdate >= cast('{DATE}' as date)
and l_shipdate < dateadd(yy, +1, cast('{DATE}' as date))
and l_discount between {DISCOUNT} - 0.01 and {DISCOUNT} + 0.01
and l_quantity < {QUANTITY}
```

</details>

<details>
<summary>SAP HANA — <code>add_years</code></summary>

```sql
select
sum(l_extendedprice*l_discount) as revenue
from lineitem
where
l_shipdate >= to_date('{DATE}')
and l_shipdate < add_years(to_date('{DATE}'),1)
and l_discount between {DISCOUNT} - 0.01 and {DISCOUNT} + 0.01
and l_quantity < {QUANTITY}
```

</details>

<details>
<summary>Clickhouse — <code>CAST(… AS Decimal(16,2))</code> for BETWEEN on discount column</summary>

```sql
select
sum(l_extendedprice*l_discount) as revenue
from lineitem
where
l_shipdate >= toDate('{DATE}')
and l_shipdate < addYears(toDate('{DATE}'),1)
and l_discount between CAST({DISCOUNT} - 0.01 AS Decimal(16, 2)) and CAST({DISCOUNT} + 0.01 AS Decimal(16, 2))
and l_quantity < {QUANTITY}
```

</details>

<details>
<summary>DB2 — <code>date '…' + 1 year</code></summary>

```sql
select
sum(l_extendedprice*l_discount) as revenue
from lineitem
where
l_shipdate >= date '{DATE}'
and l_shipdate < date '{DATE}' + 1 year
and l_discount between {DISCOUNT} - 0.01 and {DISCOUNT} + 0.01
and l_quantity < {QUANTITY}
```

</details>

---

## Q7 – Volume Shipping Query

Finds gross discounted revenues for 1995 and 1996 for goods shipped between two given nations
to support shipping contract re-negotiation.

**Parameters:**

| bexhoma | TPC-H | Type | Notes |
|---|---|---|---|
| `{NATION1}`, `{NATION2}` | `:1`, `:2` | list, size 2, drawn without replacement | 25 TPC-H nations |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
supp_nation, cust_nation, l_year, sum(volume) as revenue
from (
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract(year from l_shipdate) as l_year,
l_extendedprice * (1 - l_discount) as volume
from
supplier, lineitem, orders, customer, nation n1, nation n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = '[NATION1]' and n2.n_name = '[NATION2]')
or (n1.n_name = '[NATION2]' and n2.n_name = '[NATION1]')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) as shipping
group by supp_nation, cust_nation, l_year
order by supp_nation, cust_nation, l_year;
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB; adds <code>cast(extract(year …) as int)</code></summary>

```sql
select
supp_nation, cust_nation, l_year, sum(volume) as revenue
from (
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
cast(extract(year from l_shipdate) as int) as l_year,
l_extendedprice * (1 - l_discount) as volume
from
supplier, lineitem, orders, customer, nation n1, nation n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = '{NATION1}' and n2.n_name = '{NATION2}')
or (n1.n_name = '{NATION2}' and n2.n_name = '{NATION1}')
)
and l_shipdate between date '1995-01-01' and date '1996-12-31'
) shipping
group by supp_nation, cust_nation, l_year
order by supp_nation, cust_nation, l_year
```

</details>

<details>
<summary>MySQL — plain <code>extract</code>; <code>date('…')</code> literals; subquery needs <code>as</code> alias</summary>

```sql
select
supp_nation, cust_nation, l_year, sum(volume) as revenue
from (
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
extract(year from l_shipdate) as l_year,
l_extendedprice * (1 - l_discount) as volume
from
supplier, lineitem, orders, customer, nation n1, nation n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = '{NATION1}' and n2.n_name = '{NATION2}')
or (n1.n_name = '{NATION2}' and n2.n_name = '{NATION1}')
)
and l_shipdate between date('1995-01-01') and date('1996-12-31')
) as shipping
group by supp_nation, cust_nation, l_year
order by supp_nation, cust_nation, l_year
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>year()</code> function; <code>cast('…' as date)</code> literals</summary>

```sql
select
supp_nation, cust_nation, l_year, sum(volume) as revenue
from (
select
n1.n_name as supp_nation,
n2.n_name as cust_nation,
cast(year(l_shipdate) as int) as l_year,
l_extendedprice * (1 - l_discount) as volume
from
supplier, lineitem, orders, customer, nation n1, nation n2
where
s_suppkey = l_suppkey
and o_orderkey = l_orderkey
and c_custkey = o_custkey
and s_nationkey = n1.n_nationkey
and c_nationkey = n2.n_nationkey
and (
(n1.n_name = '{NATION1}' and n2.n_name = '{NATION2}')
or (n1.n_name = '{NATION2}' and n2.n_name = '{NATION1}')
)
and l_shipdate between cast('1995-01-01' as date) and cast('1996-12-31' as date)
) as shipping
group by supp_nation, cust_nation, l_year
order by supp_nation, cust_nation, l_year
```

</details>

---

## Q8 – National Market Share Query

Determines how the market share of a given nation within a given region has changed over 1995–1996
for a given part type.

**Parameters:**

| bexhoma | TPC-H | Type | Notes |
|---|---|---|---|
| `{NATIONREGION2}` | `:1` (NATION) | dict-derived | Nation name in the CASE WHEN |
| `{NATIONREGION1}` | `:2` (REGION) | dict-derived | Region corresponding to the chosen nation |
| `{TYPE1}{TYPE2}{TYPE3}` | `:3` (TYPE) | three lists | Concatenated to form the 3-syllable type |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
o_year,
sum(case when nation = '[NATION]' then volume else 0 end) / sum(volume) as mkt_share
from (
select
extract(year from o_orderdate) as o_year,
l_extendedprice * (1 - l_discount) as volume,
n2.n_name as nation
from
part, supplier, lineitem, orders, customer, nation n1, nation n2, region
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = '[REGION]'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = '[TYPE]'
) as all_nations
group by o_year
order by o_year;
```

</details>

<details>
<summary>Default SQL — adds <code>cast(extract … as int)</code> and <code>cast(l_extendedprice as double)</code></summary>

```sql
select
o_year,
sum(case
when nation = '{NATIONREGION2}' then volume
else 0
end) / sum(volume) as mkt_share
from (
select
cast(extract(year from o_orderdate) as int) as o_year,
cast(l_extendedprice as double) * (1-l_discount) as volume,
n2.n_name as nation
from
part, supplier, lineitem, orders, customer, nation n1, nation n2, region
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = '{NATIONREGION1}'
and s_nationkey = n2.n_nationkey
and o_orderdate between date '1995-01-01' and date '1996-12-31'
and p_type = '{TYPE1}{TYPE2}{TYPE3}'
) all_nations
group by o_year
order by o_year
```

</details>

<details>
<summary>MySQL — <code>cast(… as unsigned)</code>; <code>date('…')</code> literals; subquery needs <code>as</code></summary>

```sql
select
o_year,
sum(case
when nation = '{NATIONREGION2}' then volume
else 0
end) / sum(volume) as mkt_share
from (
select
cast(extract(year from o_orderdate) as unsigned) as o_year,
cast(l_extendedprice as double) * (1-l_discount) as volume,
n2.n_name as nation
from
part, supplier, lineitem, orders, customer, nation n1, nation n2, region
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = '{NATIONREGION1}'
and s_nationkey = n2.n_nationkey
and o_orderdate between date('1995-01-01') and date('1996-12-31')
and p_type = '{TYPE1}{TYPE2}{TYPE3}'
) as all_nations
group by o_year
order by o_year
```

</details>

<details>
<summary>PostgreSQL / Citus — <code>double precision</code> cast</summary>

```sql
select
o_year,
sum(case
when nation = '{NATIONREGION2}' then volume
else 0
end) / sum(volume) as mkt_share
from (
select
cast(extract(year from o_orderdate) as integer) as o_year,
cast(l_extendedprice as double precision) * (1-l_discount) as volume,
n2.n_name as nation
from
part, supplier, lineitem, orders, customer, nation n1, nation n2, region
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = '{NATIONREGION1}'
and s_nationkey = n2.n_nationkey
and o_orderdate between date('1995-01-01') and date('1996-12-31')
and p_type = '{TYPE1}{TYPE2}{TYPE3}'
) as all_nations
group by o_year
order by o_year
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>year()</code> function; <code>cast('…' as date)</code> literals</summary>

```sql
select
o_year,
sum(case
when nation = '{NATIONREGION2}' then volume
else 0
end) / sum(volume) as mkt_share
from (
select
cast(year(o_orderdate) as int) as o_year,
cast(l_extendedprice as float) * (1-l_discount) as volume,
n2.n_name as nation
from
part, supplier, lineitem, orders, customer, nation n1, nation n2, region
where
p_partkey = l_partkey
and s_suppkey = l_suppkey
and l_orderkey = o_orderkey
and o_custkey = c_custkey
and c_nationkey = n1.n_nationkey
and n1.n_regionkey = r_regionkey
and r_name = '{NATIONREGION1}'
and s_nationkey = n2.n_nationkey
and o_orderdate between cast('1995-01-01' as date) and cast('1996-12-31' as date)
and p_type = '{TYPE1}{TYPE2}{TYPE3}'
) as all_nations
group by o_year
order by o_year
```

</details>

---

## Q9 – Product Type Profit Measure Query

Determines how much profit is made on a given line of parts, broken out by supplier nation and year.

**Parameters:**

| bexhoma | TPC-H | Type | Range |
|---|---|---|---|
| `{COLOR}` | `:1` | list | 92 color names (e.g., `almond`, `green`, `steel`) |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
nation, o_year, sum(amount) as sum_profit
from (
select
n_name as nation,
extract(year from o_orderdate) as o_year,
l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount
from
part, supplier, lineitem, partsupp, orders, nation
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%[COLOR]%'
) as profit
group by nation, o_year
order by nation, o_year desc;
```

</details>

<details>
<summary>Default SQL — adds <code>cast(extract(year …) as int)</code></summary>

```sql
select
nation, o_year, sum(amount) as sum_profit
from (
select
n_name as nation,
cast(extract(year from o_orderdate) as int) as o_year,
l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount
from
part, supplier, lineitem, partsupp, orders, nation
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%{COLOR}%'
) profit
group by nation, o_year
order by nation, o_year desc
```

</details>

<details>
<summary>MySQL — plain <code>extract</code>; subquery needs <code>as</code> alias</summary>

```sql
select
nation, o_year, sum(amount) as sum_profit
from (
select
n_name as nation,
extract(year from o_orderdate) as o_year,
l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount
from
part, supplier, lineitem, partsupp, orders, nation
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%{COLOR}%'
) as profit
group by nation, o_year
order by nation, o_year desc
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>year()</code> function</summary>

```sql
select
nation, o_year, sum(amount) as sum_profit
from (
select
n_name as nation,
cast(year(o_orderdate) as int) as o_year,
l_extendedprice * (1 - l_discount) - ps_supplycost * l_quantity as amount
from
part, supplier, lineitem, partsupp, orders, nation
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%{COLOR}%'
) as profit
group by nation, o_year
order by nation, o_year desc
```

</details>

<details>
<summary>OmniSci — double cast to avoid precision loss in columnar format</summary>

```sql
select
nation, o_year, cast(sum(amount) as double) as sum_profit
from (
select
n_name as nation,
cast(extract(year from o_orderdate) as int) as o_year,
cast(l_extendedprice as double) * (1 - l_discount) - cast(ps_supplycost as double) * l_quantity as amount
from
part, supplier, lineitem, partsupp, orders, nation
where
s_suppkey = l_suppkey
and ps_suppkey = l_suppkey
and ps_partkey = l_partkey
and p_partkey = l_partkey
and o_orderkey = l_orderkey
and s_nationkey = n_nationkey
and p_name like '%{COLOR}%'
) profit
group by nation, o_year
order by nation, o_year desc
```

</details>

---

## Q10 – Returned Item Reporting Query

Finds the top 20 customers by lost revenue from returned parts in a given quarter.
Returns the first 20 rows.

**Parameters:**

| bexhoma | TPC-H | Type | Range |
|---|---|---|---|
| `{DATE}` | `:1` | firstofmonth | [1993-02-01, 1995-01-01] |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
c_custkey, c_name,
sum(l_extendedprice * (1 - l_discount)) as revenue,
c_acctbal, n_name, c_address, c_phone, c_comment
from customer, orders, lineitem, nation
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '[DATE]'
and o_orderdate < date '[DATE]' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by c_custkey, c_name, c_acctbal, c_phone, n_name, c_address, c_comment
order by revenue desc;
-- :n 20
```

</details>

<details>
<summary>Default SQL — adds <code>cast(… as double)</code> for revenue; <code>limit 20</code></summary>

```sql
select
c_custkey, c_name,
sum(cast(l_extendedprice * (1 - l_discount) as double)) as revenue,
c_acctbal, n_name, c_address, c_phone, c_comment
from customer, orders, lineitem, nation
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '{DATE}'
and o_orderdate < date '{DATE}' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by c_custkey, c_name, c_acctbal, c_phone, n_name, c_address, c_comment
order by revenue desc
limit 20
```

</details>

<details>
<summary>MySQL — <code>date('…')</code> syntax; no double cast</summary>

```sql
select
c_custkey, c_name,
sum(l_extendedprice * (1 - l_discount)) as revenue,
c_acctbal, n_name, c_address, c_phone, c_comment
from customer, orders, lineitem, nation
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date('{DATE}')
and o_orderdate < date('{DATE}') + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by c_custkey, c_name, c_acctbal, c_phone, n_name, c_address, c_comment
order by revenue desc
limit 20
```

</details>

<details>
<summary>PostgreSQL / Citus — <code>double precision</code> cast</summary>

```sql
select
c_custkey, c_name,
sum(cast(l_extendedprice * (1 - l_discount) as double precision)) as revenue,
c_acctbal, n_name, c_address, c_phone, c_comment
from customer, orders, lineitem, nation
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date('{DATE}')
and o_orderdate < date('{DATE}') + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by c_custkey, c_name, c_acctbal, c_phone, n_name, c_address, c_comment
order by revenue desc
limit 20
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>select top 20</code>; <code>dateadd(mm, +3, …)</code></summary>

```sql
select top 20
c_custkey, c_name,
sum(l_extendedprice * (1 - l_discount)) as revenue,
c_acctbal, n_name, c_address, c_phone, c_comment
from customer, orders, lineitem, nation
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= cast('{DATE}' as date)
and o_orderdate < dateadd(mm, +3, cast('{DATE}' as date))
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by c_custkey, c_name, c_acctbal, c_phone, n_name, c_address, c_comment
order by revenue desc
```

</details>

<details>
<summary>Oracle — <code>fetch next 20 rows only</code></summary>

```sql
select
c_custkey, c_name,
sum(l_extendedprice * (1 - l_discount)) as revenue,
c_acctbal, n_name, c_address, c_phone, c_comment
from customer, orders, lineitem, nation
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '{DATE}'
and o_orderdate < date '{DATE}' + interval '3' month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by c_custkey, c_name, c_acctbal, c_phone, n_name, c_address, c_comment
order by revenue desc
fetch next 20 rows only
```

</details>

<details>
<summary>SAP HANA — <code>add_months(to_date(…), 3)</code></summary>

```sql
select
c_custkey, c_name,
sum(cast(l_extendedprice * (1 - l_discount) as double)) as revenue,
c_acctbal, n_name, c_address, c_phone, c_comment
from customer, orders, lineitem, nation
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= to_date('{DATE}')
and o_orderdate < add_months(to_date('{DATE}'),3)
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by c_custkey, c_name, c_acctbal, c_phone, n_name, c_address, c_comment
order by revenue desc
limit 20
```

</details>

<details>
<summary>DB2 — <code>date '…' + 3 month</code></summary>

```sql
select
c_custkey, c_name,
sum(cast(l_extendedprice * (1 - l_discount) as double)) as revenue,
c_acctbal, n_name, c_address, c_phone, c_comment
from customer, orders, lineitem, nation
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and o_orderdate >= date '{DATE}'
and o_orderdate < date '{DATE}' + 3 month
and l_returnflag = 'R'
and c_nationkey = n_nationkey
group by c_custkey, c_name, c_acctbal, c_phone, n_name, c_address, c_comment
order by revenue desc
limit 20
```

</details>

---

## Q11 – Important Stock Identification Query

Identifies parts that represent a significant fraction of the total value of available parts
from suppliers in a given nation.

**Parameters:**

| bexhoma | TPC-H | Type | Notes |
|---|---|---|---|
| `{NATION}` | `:1` | list | 25 TPC-H nations |
| `{FRACTION}` | `:2` (partial) | list | [0.0001] — fixed constant |
| `{SF}` | — | list | [1] — scale factor; effective fraction = `{FRACTION} / {SF}` |

The TPC-H spec uses a single `:2` value computed as `0.0001 / SF`. Bexhoma exposes SF and
FRACTION as separate parameters and computes `{FRACTION} * (1.0 / {SF})` in the query.

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
ps_partkey,
sum(ps_supplycost * ps_availqty) as value
from partsupp, supplier, nation
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = '[NATION]'
group by ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select sum(ps_supplycost * ps_availqty) * [FRACTION]
from partsupp, supplier, nation
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = '[NATION]'
)
order by value desc;
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB; alias <code>v</code>; fraction as <code>{FRACTION} * (1.0 / {SF})</code></summary>

```sql
select
ps_partkey,
sum(ps_supplycost * ps_availqty) as v
from partsupp, supplier, nation
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = '{NATION}'
group by ps_partkey having
sum(ps_supplycost * ps_availqty) > (
select sum(ps_supplycost * ps_availqty) * {FRACTION} * (1.0 / {SF})
from partsupp, supplier, nation
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = '{NATION}'
)
order by v desc
```

</details>

<details>
<summary>Clickhouse — explicit <code>Float64</code> cast in HAVING; <code>{SF}.0</code> forces float division</summary>

```sql
select
ps_partkey,
sum(ps_supplycost * ps_availqty) as v
from partsupp, supplier, nation
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = '{NATION}'
group by ps_partkey having
cast(sum(ps_supplycost * ps_availqty) as Float64) > (
select cast(sum(ps_supplycost * ps_availqty) as Float64) * {FRACTION} * (1.0 / {SF}.0)
from partsupp, supplier, nation
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = '{NATION}'
)
order by v desc
```

</details>

<details>
<summary>DB2 — <code>double</code> cast instead of Float64</summary>

```sql
select
ps_partkey,
cast(sum(ps_supplycost * ps_availqty) as double) as v
from partsupp, supplier, nation
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = '{NATION}'
group by ps_partkey having
cast(sum(ps_supplycost * ps_availqty) as double) > (
select cast(sum(ps_supplycost * ps_availqty) as double) * {FRACTION} * (1.0 / {SF}.0)
from partsupp, supplier, nation
where
ps_suppkey = s_suppkey
and s_nationkey = n_nationkey
and n_name = '{NATION}'
)
order by v desc
```

</details>

---

## Q12 – Shipping Modes and Order Priority Query

Determines whether less expensive shipping modes negatively affect critical-priority orders.

**Parameters:**

| bexhoma | TPC-H | Type | Range / Values |
|---|---|---|---|
| `{SHIPMODE1}`, `{SHIPMODE2}` | `:1`, `:2` | list, size 2, distinct | REG AIR, AIR, RAIL, SHIP, TRUCK, MAIL, FOB |
| `{DATE}` | `:3` | firstofyear | [1993, 1997] |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
l_shipmode,
sum(case when o_orderpriority = '1-URGENT' or o_orderpriority = '2-HIGH' then 1 else 0 end) as high_line_count,
sum(case when o_orderpriority <> '1-URGENT' and o_orderpriority <> '2-HIGH' then 1 else 0 end) as low_line_count
from orders, lineitem
where
o_orderkey = l_orderkey
and l_shipmode in ('[SHIPMODE1]', '[SHIPMODE2]')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '[DATE]'
and l_receiptdate < date '[DATE]' + interval '1' year
group by l_shipmode
order by l_shipmode;
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB; CASE returns <code>1.0</code>/<code>0.0</code></summary>

```sql
select
l_shipmode,
sum(case
when o_orderpriority ='1-URGENT' or o_orderpriority ='2-HIGH' then 1.0
else 0.0
end) as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT' and o_orderpriority <> '2-HIGH' then 1.0
else 0.0
end) as low_line_count
from orders, lineitem
where
o_orderkey = l_orderkey
and l_shipmode in ('{SHIPMODE1}', '{SHIPMODE2}')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '{DATE}'
and l_receiptdate < date '{DATE}' + interval '1' year
group by l_shipmode
order by l_shipmode
```

</details>

<details>
<summary>MySQL — <code>date('…')</code> function syntax</summary>

```sql
select
l_shipmode,
sum(case
when o_orderpriority ='1-URGENT' or o_orderpriority ='2-HIGH' then 1.0
else 0.0
end) as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT' and o_orderpriority <> '2-HIGH' then 1.0
else 0.0
end) as low_line_count
from orders, lineitem
where
o_orderkey = l_orderkey
and l_shipmode in ('{SHIPMODE1}', '{SHIPMODE2}')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date('{DATE}')
and l_receiptdate < date('{DATE}') + interval '1' year
group by l_shipmode
order by l_shipmode
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>dateadd(yy, +1, …)</code></summary>

```sql
select
l_shipmode,
sum(case
when o_orderpriority ='1-URGENT' or o_orderpriority ='2-HIGH' then 1.0
else 0.0
end) as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT' and o_orderpriority <> '2-HIGH' then 1.0
else 0.0
end) as low_line_count
from orders, lineitem
where
o_orderkey = l_orderkey
and l_shipmode in ('{SHIPMODE1}', '{SHIPMODE2}')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= cast('{DATE}' as date)
and l_receiptdate < dateadd(yy, +1, cast('{DATE}' as date))
group by l_shipmode
order by l_shipmode
```

</details>

<details>
<summary>SAP HANA — <code>add_years(to_date(…), 1)</code></summary>

```sql
select
l_shipmode,
sum(case
when o_orderpriority ='1-URGENT' or o_orderpriority ='2-HIGH' then 1.0
else 0.0
end) as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT' and o_orderpriority <> '2-HIGH' then 1.0
else 0.0
end) as low_line_count
from orders, lineitem
where
o_orderkey = l_orderkey
and l_shipmode in ('{SHIPMODE1}', '{SHIPMODE2}')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= to_date('{DATE}')
and l_receiptdate < add_years(to_date('{DATE}'),1)
group by l_shipmode
order by l_shipmode
```

</details>

<details>
<summary>DB2 — <code>date '…' + 1 year</code></summary>

```sql
select
l_shipmode,
sum(case
when o_orderpriority ='1-URGENT' or o_orderpriority ='2-HIGH' then 1.0
else 0.0
end) as high_line_count,
sum(case
when o_orderpriority <> '1-URGENT' and o_orderpriority <> '2-HIGH' then 1.0
else 0.0
end) as low_line_count
from orders, lineitem
where
o_orderkey = l_orderkey
and l_shipmode in ('{SHIPMODE1}', '{SHIPMODE2}')
and l_commitdate < l_receiptdate
and l_shipdate < l_commitdate
and l_receiptdate >= date '{DATE}'
and l_receiptdate < date '{DATE}' + 1 year
group by l_shipmode
order by l_shipmode
```

</details>

---

## Q13 – Customer Distribution Query

Seeks relationships between customers and the size of their orders.

**Parameters:**

| bexhoma | TPC-H | Type | Range / Values |
|---|---|---|---|
| `{WORD1}` | `:1` | list | special, pending, unusual, express |
| `{WORD2}` | `:2` | list | packages, requests, accounts, deposits |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
c_count, count(*) as custdist
from (
select
c_custkey,
count(o_orderkey)
from customer left outer join orders on
c_custkey = o_custkey
and o_comment not like '%[WORD1]%[WORD2]%'
group by c_custkey
) as c_orders (c_custkey, c_count)
group by c_count
order by custdist desc, c_count desc;
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MySQL, MariaDB; no DBMS-specific variants</summary>

```sql
select
c_count, count(*) as custdist
from (
select
c_custkey c_custkey,
count(o_orderkey) c_count
from customer left outer join orders on
c_custkey = o_custkey
where o_comment not like '%{WORD1}%{WORD2}%'
group by c_custkey
) c_orders
group by c_count
order by custdist desc, c_count desc
```

</details>

---

## Q14 – Promotion Effect Query

Determines what percentage of revenue in a given month came from promotional parts.

**Parameters:**

| bexhoma | TPC-H | Type | Range |
|---|---|---|---|
| `{DATE}` | `:1` | firstofmonth | [1993-01-01, 1997-01-01] |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
100.00 * sum(case
when p_type like 'PROMO%' then l_extendedprice * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from lineitem, part
where
l_partkey = p_partkey
and l_shipdate >= date '[DATE]'
and l_shipdate < date '[DATE]' + interval '1' month;
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB</summary>

```sql
select
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice*(1-l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from lineitem, part
where
l_partkey = p_partkey
and l_shipdate >= date '{DATE}'
and l_shipdate < date '{DATE}' + interval '1' month
```

</details>

<details>
<summary>MySQL — <code>date('…')</code> function syntax</summary>

```sql
select
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice*(1-l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from lineitem, part
where
l_partkey = p_partkey
and l_shipdate >= date('{DATE}')
and l_shipdate < date('{DATE}') + interval '1' month
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>dateadd(mm, +1, …)</code></summary>

```sql
select
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice*(1-l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from lineitem, part
where
l_partkey = p_partkey
and l_shipdate >= cast('{DATE}' as date)
and l_shipdate < dateadd(mm, +1, cast('{DATE}' as date))
```

</details>

<details>
<summary>OmniSci — explicit <code>FLOAT</code> cast in THEN branch</summary>

```sql
select
100.00 * sum(case
when p_type like 'PROMO%'
then cast(l_extendedprice as FLOAT) * (1 - l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from lineitem, part
where
l_partkey = p_partkey
and l_shipdate >= date '{DATE}'
and l_shipdate < date '{DATE}' + interval '1' month
```

</details>

<details>
<summary>MonetDB — outer <code>CAST(… AS double)</code> to avoid integer division</summary>

```sql
select
100.00 * CAST(sum(case
when p_type like 'PROMO%'
then cast(l_extendedprice as FLOAT) * (1 - l_discount)
else 0
end) AS double) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from lineitem, part
where
l_partkey = p_partkey
and l_shipdate >= date '{DATE}'
and l_shipdate < date '{DATE}' + interval '1' month
```

</details>

<details>
<summary>SAP HANA — <code>add_months(to_date(…), 1)</code></summary>

```sql
select
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice*(1-l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from lineitem, part
where
l_partkey = p_partkey
and l_shipdate >= to_date('{DATE}')
and l_shipdate < add_months(to_date('{DATE}'),1)
```

</details>

<details>
<summary>Clickhouse — <code>Float64</code> cast on both numerator and denominator</summary>

```sql
select
100.00 * CAST(sum(case
when p_type like 'PROMO%'
then cast(l_extendedprice as Float64) * (1 - l_discount)
else 0
end) AS Float64) / CAST(sum(l_extendedprice * (1 - l_discount)) AS Float64) as promo_revenue
from lineitem, part
where
l_partkey = p_partkey
and l_shipdate >= date '{DATE}'
and l_shipdate < date '{DATE}' + interval '1' month
```

</details>

<details>
<summary>DB2 — <code>date '…' + 1 month</code></summary>

```sql
select
100.00 * sum(case
when p_type like 'PROMO%'
then l_extendedprice*(1-l_discount)
else 0
end) / sum(l_extendedprice * (1 - l_discount)) as promo_revenue
from lineitem, part
where
l_partkey = p_partkey
and l_shipdate >= date '{DATE}'
and l_shipdate < date '{DATE}' + 1 month
```

</details>

---

## Q15 – Top Supplier Query

Determines the top supplier by total revenue in a given quarter to reward or negotiate with.

**Parameters:**

| bexhoma | TPC-H | Type | Range |
|---|---|---|---|
| `{DATE}` | `:1` | firstofmonth | [1993-01-01, 1997-10-01] |
| `{STREAM}` | — | list | [1] — stream suffix for unique view name |

> Note: `datatransfer` is disabled for Q15 (`active: False`) because multi-step view execution
> does not return rows the way a single SELECT does.

<details>
<summary>TPC-H reference SQL — three-statement CREATE VIEW / SELECT / DROP VIEW pattern</summary>

```sql
create view revenue:s (supplier_no, total_revenue) as
select l_suppkey, sum(l_extendedprice * (1 - l_discount))
from lineitem
where l_shipdate >= date ':1'
and l_shipdate < date ':1' + interval '3' month
group by l_suppkey;

select s_suppkey, s_name, s_address, s_phone, total_revenue
from supplier, revenue:s
where s_suppkey = supplier_no
and total_revenue = (select max(total_revenue) from revenue:s)
order by s_suppkey;

drop view revenue:s;
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB, MonetDB; CTE avoids CREATE/DROP VIEW</summary>

```sql
with revenue (supplier_no, total_revenue) as (
select l_suppkey, sum(l_extendedprice * (1-l_discount))
from lineitem
where l_shipdate >= date('{DATE}')
and l_shipdate < date('{DATE}') + interval '3' month
group by l_suppkey)
select s_suppkey, s_name, s_address, s_phone, total_revenue
from supplier, revenue
where s_suppkey = supplier_no
and total_revenue = (select max(total_revenue) from revenue)
order by s_suppkey
```

</details>

<details>
<summary>Original_view — three-statement view; view name includes <code>{numRun}{STREAM}</code> to avoid conflicts</summary>

Statement 1:
```sql
create view revenue{numRun}{STREAM} as
select l_suppkey supplier_no, sum(l_extendedprice * (1 - l_discount)) total_revenue
from lineitem
where l_shipdate >= date '{DATE}'
and l_shipdate < date '{DATE}' + interval '3' month
group by l_suppkey
```

Statement 2:
```sql
select s_suppkey, s_name, s_address, s_phone, total_revenue
from supplier, revenue{numRun}{STREAM}
where s_suppkey = supplier_no
and total_revenue = (select max(total_revenue) from revenue{numRun}{STREAM})
order by s_suppkey
```

Statement 3:
```sql
drop view revenue{numRun}
```

</details>

<details>
<summary>MySQL_view — three-statement view; <code>date('…')</code> syntax</summary>

Statement 1:
```sql
create view revenue{numRun}{STREAM} as
select l_suppkey supplier_no, sum(l_extendedprice * (1 - l_discount)) total_revenue
from lineitem
where l_shipdate >= date('{DATE}')
and l_shipdate < date('{DATE}') + interval '3' month
group by l_suppkey
```

Statements 2 and 3 identical to Original_view.

</details>

<details>
<summary>T-SQL (SQL Server) — three-statement view; <code>dateadd(mm, +3, …)</code></summary>

Statement 1:
```sql
create view revenue{numRun}{STREAM} as
select l_suppkey supplier_no, sum(l_extendedprice * (1 - l_discount)) total_revenue
from lineitem
where l_shipdate >= cast('{DATE}' as date)
and l_shipdate < dateadd(mm, +3, cast('{DATE}' as date))
group by l_suppkey
```

Statements 2 and 3 identical to Original_view.

</details>

<details>
<summary>SAP HANA — three-statement view; <code>add_months(to_date(…), 3)</code></summary>

Statement 1:
```sql
create view revenue{numRun}{STREAM} as
select l_suppkey supplier_no, sum(l_extendedprice * (1 - l_discount)) total_revenue
from lineitem
where l_shipdate >= to_date('{DATE}')
and l_shipdate < add_months(to_date('{DATE}'),3)
group by l_suppkey
```

Statements 2 and 3 identical to Original_view.

</details>

<details>
<summary>DB2 — three-statement view; <code>date '…' + 3 month</code></summary>

Statement 1:
```sql
create view revenue{numRun} as
select l_suppkey supplier_no, sum(l_extendedprice * (1 - l_discount)) total_revenue
from lineitem
where l_shipdate >= date '{DATE}'
and l_shipdate < date '{DATE}' + 3 month
group by l_suppkey
```

Statements 2 and 3 identical to Original_view.

</details>

---

## Q16 – Parts/Supplier Relationship Query

Counts the number of suppliers who can supply parts satisfying a customer's requirements,
excluding suppliers with known complaints.

**Parameters:**

| bexhoma | TPC-H | Type | Range |
|---|---|---|---|
| `{BRAND1}{BRAND2}` | `:1` | two integers 1–5 | forms `Brand#XY` |
| `{TYPE1}{TYPE2}{TYPE3}` | `:2` | three lists | combined type prefix |
| `{SIZE1}`–`{SIZE8}` | `:3`–`:10` | 8 distinct integers | [1, 50] |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
p_brand, p_type, p_size,
count(distinct ps_suppkey) as supplier_cnt
from partsupp, part
where
p_partkey = ps_partkey
and p_brand <> '[BRAND]'
and p_type not like '[TYPE]%'
and p_size in ([SIZE1],[SIZE2],[SIZE3],[SIZE4],[SIZE5],[SIZE6],[SIZE7],[SIZE8])
and ps_suppkey not in (
select s_suppkey from supplier where s_comment like '%Customer%Complaints%'
)
group by p_brand, p_type, p_size
order by supplier_cnt desc, p_brand, p_type, p_size;
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MySQL, MariaDB; no DBMS-specific variants</summary>

```sql
select
p_brand, p_type, p_size,
count(distinct ps_suppkey) as supplier_cnt
from partsupp, part
where
p_partkey = ps_partkey
and p_brand <> 'Brand#{BRAND1}{BRAND2}'
and p_type not like '{TYPE1}{TYPE2}{TYPE3}%'
and p_size in ({SIZE1},{SIZE2},{SIZE3},{SIZE4},{SIZE5},{SIZE6},{SIZE7},{SIZE8})
and ps_suppkey not in (
select s_suppkey from supplier where s_comment like '%Customer%Complaints%'
)
group by p_brand, p_type, p_size
order by supplier_cnt desc, p_brand, p_type, p_size
```

</details>

---

## Q17 – Small-Quantity-Order Revenue Query

Determines the average yearly revenue loss if small-quantity orders for a given brand and
container type were no longer taken.

**Parameters:**

| bexhoma | TPC-H | Type | Range / Values |
|---|---|---|---|
| `{BRAND1}{BRAND2}` | `:1` | two integers 1–5 | forms `Brand#XY` |
| `{CONTAINER1} {CONTAINER2}` | `:2` | two lists (space-joined) | SM/LG/MED/JUMBO/WRAP + CASE/BOX/BAG/JAR/PKG/PACK |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
sum(l_extendedprice) / 7.0 as avg_yearly
from lineitem, part
where
p_partkey = l_partkey
and p_brand = '[BRAND]'
and p_container = '[CONTAINER]'
and l_quantity < (
select 0.2 * avg(l_quantity) from lineitem where l_partkey = p_partkey
);
```

</details>

<details>
<summary>Default SQL — PostgreSQL; correlated subquery form</summary>

```sql
select
sum(l_extendedprice) / 7.0 as avg_yearly
from lineitem, part
where
p_partkey = l_partkey
and p_brand = 'Brand#{BRAND1}{BRAND2}'
and p_container = '{CONTAINER1} {CONTAINER2}'
and l_quantity < (
select 0.2 * avg(l_quantity) from lineitem where l_partkey = p_partkey
)
```

</details>

<details>
<summary>OmniSci / MariaDBCS / Citus — correlated subquery rewritten as pre-aggregated JOIN</summary>

```sql
select
sum(li.l_extendedprice) / 7.0 as avg_yearly
from lineitem li
join part p on li.l_partkey = p.p_partkey
join (
   select l_partkey, 0.2 * avg(l_quantity) as quantity
   from lineitem group by l_partkey
) as quantities on li.l_partkey = quantities.l_partkey
and li.l_quantity < quantities.quantity
where p.p_brand = 'Brand#{BRAND1}{BRAND2}'
and p.p_container = '{CONTAINER1} {CONTAINER2}'
```

</details>

<details>
<summary>Clickhouse — JOIN rewrite; decimal cast for <code>avg_yearly</code></summary>

```sql
select
cast(sum(li.l_extendedprice) as DECIMAL(16,2)) / cast(7.00 as decimal(16,2)) as avg_yearly
from lineitem li
join part p on li.l_partkey = p.p_partkey
join (
   select l_partkey, CAST(0.2 * avg(l_quantity) AS DECIMAL(16,2)) as quantity
   from lineitem group by l_partkey
) as quantities on li.l_partkey = quantities.l_partkey
where p.p_brand = 'Brand#{BRAND1}{BRAND2}'
and li.l_quantity < quantities.quantity
and p.p_container = '{CONTAINER1} {CONTAINER2}'
```

</details>

---

## Q18 – Large Volume Customer Query

Ranks customers based on having placed large-quantity orders. Returns the first 100 rows.

**Parameters:**

| bexhoma | TPC-H | Type | Range |
|---|---|---|---|
| `{QUANTITY}` | `:1` | integer | [312, 315] |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select
c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice, sum(l_quantity)
from customer, orders, lineitem
where
o_orderkey in (
select l_orderkey from lineitem group by l_orderkey having sum(l_quantity) > [QUANTITY]
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice
order by o_totalprice desc, o_orderdate;
-- :n 100
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB; <code>cast(sum(l_quantity) as int)</code>; <code>limit 100</code></summary>

```sql
select
c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice,
cast(sum(l_quantity) as int) as sum_quant
from customer, orders, lineitem
where
o_orderkey in (
select l_orderkey from lineitem group by l_orderkey having sum(l_quantity) > {QUANTITY}
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice
order by o_totalprice desc, o_orderdate
limit 100
```

</details>

<details>
<summary>MySQL — <code>cast(… as unsigned integer)</code></summary>

```sql
select
c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice,
cast(sum(l_quantity) as unsigned integer) as sum_quant
from customer, orders, lineitem
where
o_orderkey in (
select l_orderkey from lineitem group by l_orderkey having sum(l_quantity) > {QUANTITY}
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice
order by o_totalprice desc, o_orderdate
limit 100
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>select top 100</code></summary>

```sql
select top 100
c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice,
cast(sum(l_quantity) as int) as sum_quant
from customer, orders, lineitem
where
o_orderkey in (
select l_orderkey from lineitem group by l_orderkey having sum(l_quantity) > {QUANTITY}
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice
order by o_totalprice desc, o_orderdate
```

</details>

<details>
<summary>Oracle — <code>fetch next 100 rows only</code></summary>

```sql
select
c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice,
cast(sum(l_quantity) as int) as sum_quant
from customer, orders, lineitem
where
o_orderkey in (
select l_orderkey from lineitem group by l_orderkey having sum(l_quantity) > {QUANTITY}
)
and c_custkey = o_custkey
and o_orderkey = l_orderkey
group by c_name, c_custkey, o_orderkey, o_orderdate, o_totalprice
order by o_totalprice desc, o_orderdate
fetch next 100 rows only
```

</details>

---

## Q19 – Discounted Revenue Query

Finds gross discounted revenue for orders of three types of parts shipped by air and delivered
in person.

**Parameters:**

| bexhoma | TPC-H | Type | Range |
|---|---|---|---|
| `{BRAND11}{BRAND12}` | `:1` | two integers | first part group brand |
| `{BRAND21}{BRAND22}` | `:2` | two integers | second part group brand |
| `{BRAND31}{BRAND32}` | `:3` | two integers | third part group brand |
| `{QUANTITY1}` | `:4` | integer | [1, 10] |
| `{QUANTITY2}` | `:5` | integer | [10, 20] |
| `{QUANTITY3}` | `:6` | integer | [20, 30] |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select sum(l_extendedprice * (1 - l_discount)) as revenue
from lineitem, part
where (
p_partkey = l_partkey and p_brand = '[BRAND1]'
and p_container in ('SM CASE','SM BOX','SM PACK','SM PKG')
and l_quantity >= [QUANTITY1] and l_quantity <= [QUANTITY1] + 10
and p_size between 1 and 5
and l_shipmode in ('AIR','AIR REG') and l_shipinstruct = 'DELIVER IN PERSON'
) or (
p_partkey = l_partkey and p_brand = '[BRAND2]'
and p_container in ('MED BAG','MED BOX','MED PKG','MED PACK')
and l_quantity >= [QUANTITY2] and l_quantity <= [QUANTITY2] + 10
and p_size between 1 and 10
and l_shipmode in ('AIR','AIR REG') and l_shipinstruct = 'DELIVER IN PERSON'
) or (
p_partkey = l_partkey and p_brand = '[BRAND3]'
and p_container in ('LG CASE','LG BOX','LG PACK','LG PKG')
and l_quantity >= [QUANTITY3] and l_quantity <= [QUANTITY3] + 10
and p_size between 1 and 15
and l_shipmode in ('AIR','AIR REG') and l_shipinstruct = 'DELIVER IN PERSON'
);
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MySQL, MariaDB</summary>

```sql
select
sum(l_extendedprice * (1 - l_discount)) as revenue
from lineitem, part
where (
p_partkey = l_partkey
and p_brand = 'Brand#{BRAND11}{BRAND12}'
and p_container in ('SM CASE','SM BOX','SM PACK','SM PKG')
and l_quantity >= {QUANTITY1} and l_quantity <= {QUANTITY1} + 10
and p_size between 1 and 5
and l_shipmode in ('AIR','AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
) or (
p_partkey = l_partkey
and p_brand = 'Brand#{BRAND21}{BRAND22}'
and p_container in ('MED BAG','MED BOX','MED PKG','MED PACK')
and l_quantity >= {QUANTITY2} and l_quantity <= {QUANTITY2} + 10
and p_size between 1 and 10
and l_shipmode in ('AIR','AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
) or (
p_partkey = l_partkey
and p_brand = 'Brand#{BRAND31}{BRAND32}'
and p_container in ('LG CASE','LG BOX','LG PACK','LG PKG')
and l_quantity >= {QUANTITY3} and l_quantity <= {QUANTITY3} + 10
and p_size between 1 and 15
and l_shipmode in ('AIR','AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
)
```

</details>

<details>
<summary>MariaDBCS — pulls <code>p_partkey = l_partkey</code> outside OR groups (ColumnStore pushdown requirement)</summary>

```sql
select
sum(l_extendedprice * (1 - l_discount)) as revenue
from lineitem, part
where p_partkey = l_partkey
and ((
p_brand = 'Brand#{BRAND11}{BRAND12}'
and p_container in ('SM CASE','SM BOX','SM PACK','SM PKG')
and l_quantity >= {QUANTITY1} and l_quantity <= {QUANTITY1} + 10
and p_size between 1 and 5
and l_shipmode in ('AIR','AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
) or (
p_brand = 'Brand#{BRAND21}{BRAND22}'
and p_container in ('MED BAG','MED BOX','MED PKG','MED PACK')
and l_quantity >= {QUANTITY2} and l_quantity <= {QUANTITY2} + 10
and p_size between 1 and 10
and l_shipmode in ('AIR','AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
) or (
p_brand = 'Brand#{BRAND31}{BRAND32}'
and p_container in ('LG CASE','LG BOX','LG PACK','LG PKG')
and l_quantity >= {QUANTITY3} and l_quantity <= {QUANTITY3} + 10
and p_size between 1 and 15
and l_shipmode in ('AIR','AIR REG')
and l_shipinstruct = 'DELIVER IN PERSON'
))
```

</details>

---

## Q20 – Potential Part Promotion Query

Identifies suppliers in a given nation having selected parts that may be candidates for a
promotional offer.

**Parameters:**

| bexhoma | TPC-H | Type | Range |
|---|---|---|---|
| `{COLOR}` | `:1` | list | 92 color names |
| `{DATE}` | `:2` | firstofyear | [1993, 1997] |
| `{NATION}` | `:3` | list | 25 TPC-H nations |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select s_name, s_address
from supplier, nation
where s_suppkey in (
select ps_suppkey from partsupp
where ps_partkey in (select p_partkey from part where p_name like '[COLOR]%')
and ps_availqty > (
select 0.5 * sum(l_quantity) from lineitem
where l_partkey = ps_partkey and l_suppkey = ps_suppkey
and l_shipdate >= date '[DATE]'
and l_shipdate < date '[DATE]' + interval '1' year
)
)
and s_nationkey = n_nationkey
and n_name = '[NATION]'
order by s_name;
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB</summary>

```sql
select s_name, s_address
from supplier, nation
where s_suppkey in (
select ps_suppkey from partsupp
where ps_partkey in (select p_partkey from part where p_name like '{COLOR}%')
and ps_availqty > (
select 0.5 * sum(l_quantity) from lineitem
where l_partkey = ps_partkey and l_suppkey = ps_suppkey
and l_shipdate >= date '{DATE}'
and l_shipdate < date '{DATE}' + interval '1' year
)
)
and s_nationkey = n_nationkey
and n_name = '{NATION}'
order by s_name
```

</details>

<details>
<summary>MySQL — <code>date('…')</code> function syntax</summary>

```sql
select s_name, s_address
from supplier, nation
where s_suppkey in (
select ps_suppkey from partsupp
where ps_partkey in (select p_partkey from part where p_name like '{COLOR}%')
and ps_availqty > (
select 0.5 * sum(l_quantity) from lineitem
where l_partkey = ps_partkey and l_suppkey = ps_suppkey
and l_shipdate >= date('{DATE}')
and l_shipdate < date('{DATE}') + interval '1' year
)
)
and s_nationkey = n_nationkey
and n_name = '{NATION}'
order by s_name
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>dateadd(yy, +1, …)</code></summary>

```sql
select s_name, s_address
from supplier, nation
where s_suppkey in (
select ps_suppkey from partsupp
where ps_partkey in (select p_partkey from part where p_name like '{COLOR}%')
and ps_availqty > (
select 0.5 * sum(l_quantity) from lineitem
where l_partkey = ps_partkey and l_suppkey = ps_suppkey
and l_shipdate >= cast('{DATE}' as date)
and l_shipdate < dateadd(yy, +1, cast('{DATE}' as date))
)
)
and s_nationkey = n_nationkey
and n_name = '{NATION}'
order by s_name
```

</details>

<details>
<summary>OmniSci / Citus — triple correlated subquery rewritten as CTE</summary>

```sql
with corrsq as (
select l_partkey, l_suppkey, 0.5 * sum(l_quantity) sum_subq
from lineitem
where l_shipdate >= date '{DATE}'
and l_shipdate < date '{DATE}' + interval '1' year
group by l_partkey, l_suppkey
)
select s_name, s_address
from supplier, nation
where s_suppkey in (
select distinct ps_suppkey
from partsupp join corrsq
on corrsq.l_partkey = ps_partkey and corrsq.l_suppkey = ps_suppkey
where ps_partkey in (select distinct p_partkey from part where p_name like '{COLOR}%')
and ps_availqty > corrsq.sum_subq
)
and s_nationkey = n_nationkey
and n_name = '{NATION}'
order by s_name
```

</details>

<details>
<summary>Clickhouse — CTE rewrite; <code>toDate</code> / <code>addYears</code></summary>

```sql
with corrsq as (
select l_partkey, l_suppkey, 0.5 * sum(l_quantity) sum_subq
from lineitem
where l_shipdate >= toDate('{DATE}')
and l_shipdate < addYears(toDate('{DATE}'),1)
group by l_partkey, l_suppkey
)
select s_name, s_address
from supplier, nation
where s_suppkey in (
select distinct ps_suppkey
from partsupp join corrsq
on corrsq.l_partkey = ps_partkey and corrsq.l_suppkey = ps_suppkey
where ps_partkey in (select distinct p_partkey from part where p_name like '{COLOR}%')
and ps_availqty > corrsq.sum_subq
)
and s_nationkey = n_nationkey
and n_name = '{NATION}'
order by s_name
```

</details>

<details>
<summary>SAP HANA — <code>add_years(to_date(…), 1)</code></summary>

```sql
select s_name, s_address
from supplier, nation
where s_suppkey in (
select ps_suppkey from partsupp
where ps_partkey in (select p_partkey from part where p_name like '{COLOR}%')
and ps_availqty > (
select 0.5 * sum(l_quantity) from lineitem
where l_partkey = ps_partkey and l_suppkey = ps_suppkey
and l_shipdate >= to_date('{DATE}')
and l_shipdate < add_years(to_date('{DATE}'),1)
)
)
and s_nationkey = n_nationkey
and n_name = '{NATION}'
order by s_name
```

</details>

<details>
<summary>DB2 — <code>date '…' + 1 year</code></summary>

```sql
select s_name, s_address
from supplier, nation
where s_suppkey in (
select ps_suppkey from partsupp
where ps_partkey in (select p_partkey from part where p_name like '{COLOR}%')
and ps_availqty > (
select 0.5 * sum(l_quantity) from lineitem
where l_partkey = ps_partkey and l_suppkey = ps_suppkey
and l_shipdate >= date '{DATE}'
and l_shipdate < date '{DATE}' + 1 year
)
)
and s_nationkey = n_nationkey
and n_name = '{NATION}'
order by s_name
```

</details>

---

## Q21 – Suppliers Who Kept Orders Waiting Query

Identifies suppliers who were not able to ship required parts in a timely manner.
Returns the first 100 rows.

**Parameters:**

| bexhoma | TPC-H | Type | Range / Values |
|---|---|---|---|
| `{NATION}` | `:1` | list | 25 TPC-H nations |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select s_name, count(*) as numwait
from supplier, lineitem l1, orders, nation
where s_suppkey = l1.l_suppkey
and o_orderkey = l1.l_orderkey
and o_orderstatus = 'F'
and l1.l_receiptdate > l1.l_commitdate
and exists (
select * from lineitem l2
where l2.l_orderkey = l1.l_orderkey and l2.l_suppkey <> l1.l_suppkey
)
and not exists (
select * from lineitem l3
where l3.l_orderkey = l1.l_orderkey and l3.l_suppkey <> l1.l_suppkey
and l3.l_receiptdate > l3.l_commitdate
)
and s_nationkey = n_nationkey
and n_name = '[NATION]'
group by s_name
order by numwait desc, s_name;
-- :n 100
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB; <code>limit 100</code></summary>

```sql
select s_name, count(*) as numwait
from supplier, lineitem l1, orders, nation
where s_suppkey = l1.l_suppkey
and o_orderkey = l1.l_orderkey
and o_orderstatus = 'F'
and l1.l_receiptdate > l1.l_commitdate
and exists (
select * from lineitem l2
where l2.l_orderkey = l1.l_orderkey and l2.l_suppkey <> l1.l_suppkey
)
and not exists (
select * from lineitem l3
where l3.l_orderkey = l1.l_orderkey and l3.l_suppkey <> l1.l_suppkey
and l3.l_receiptdate > l3.l_commitdate
)
and s_nationkey = n_nationkey
and n_name = '{NATION}'
group by s_name
order by numwait desc, s_name
limit 100
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>select top 100</code></summary>

```sql
select top 100 s_name, count(*) as numwait
from supplier, lineitem l1, orders, nation
where s_suppkey = l1.l_suppkey
and o_orderkey = l1.l_orderkey
and o_orderstatus = 'F'
and l1.l_receiptdate > l1.l_commitdate
and exists (
select * from lineitem l2
where l2.l_orderkey = l1.l_orderkey and l2.l_suppkey <> l1.l_suppkey
)
and not exists (
select * from lineitem l3
where l3.l_orderkey = l1.l_orderkey and l3.l_suppkey <> l1.l_suppkey
and l3.l_receiptdate > l3.l_commitdate
)
and s_nationkey = n_nationkey
and n_name = '{NATION}'
group by s_name
order by numwait desc, s_name
```

</details>

<details>
<summary>Oracle — <code>fetch next 100 rows only</code></summary>

```sql
select s_name, count(*) as numwait
from supplier, lineitem l1, orders, nation
where s_suppkey = l1.l_suppkey
and o_orderkey = l1.l_orderkey
and o_orderstatus = 'F'
and l1.l_receiptdate > l1.l_commitdate
and exists (
select * from lineitem l2
where l2.l_orderkey = l1.l_orderkey and l2.l_suppkey <> l1.l_suppkey
)
and not exists (
select * from lineitem l3
where l3.l_orderkey = l1.l_orderkey and l3.l_suppkey <> l1.l_suppkey
and l3.l_receiptdate > l3.l_commitdate
)
and s_nationkey = n_nationkey
and n_name = '{NATION}'
group by s_name
order by numwait desc, s_name
fetch next 100 rows only
```

</details>

---

## Q22 – Global Sales Opportunity Query

Counts customers by country code who have not placed orders but have above-average positive
account balances.

**Parameters:**

| bexhoma | TPC-H | Type | Range / Notes |
|---|---|---|---|
| `{I1}`–`{I7}` | `:1`–`:7` | 7 integers without replacement | [10, 34] — two-digit country code prefixes |

<details>
<summary>TPC-H reference SQL</summary>

```sql
select cntrycode, count(*) as numcust, sum(c_acctbal) as totacctbal
from (
select substring(c_phone from 1 for 2) as cntrycode, c_acctbal
from customer
where substring(c_phone from 1 for 2) in ('[I1]','[I2]','[I3]','[I4]','[I5]','[I6]','[I7]')
and c_acctbal > (
select avg(c_acctbal) from customer
where c_acctbal > 0.00
and substring(c_phone from 1 for 2) in ('[I1]','[I2]','[I3]','[I4]','[I5]','[I6]','[I7]')
)
and not exists (select * from orders where o_custkey = c_custkey)
) as custsale
group by cntrycode
order by cntrycode;
```

</details>

<details>
<summary>Default SQL — PostgreSQL, MariaDB; <code>substring(… from 1 for 2)</code></summary>

```sql
select cntrycode, count(*) as numcust, sum(c_acctbal) as totacctbal
from (
select substring(c_phone from 1 for 2) as cntrycode, c_acctbal
from customer
where substring(c_phone from 1 for 2) in ('{I1}','{I2}','{I3}','{I4}','{I5}','{I6}','{I7}')
and c_acctbal > (
select avg(c_acctbal) from customer
where c_acctbal > 0.00
and substring(c_phone from 1 for 2) in ('{I1}','{I2}','{I3}','{I4}','{I5}','{I6}','{I7}')
)
and not exists (select * from orders where o_custkey = c_custkey)
) as custsale
group by cntrycode
order by cntrycode
```

</details>

<details>
<summary>T-SQL (SQL Server) — <code>substring(c_phone, 1, 2)</code> positional syntax</summary>

```sql
select cntrycode, count(*) as numcust, sum(c_acctbal) as totacctbal
from (
select substring(c_phone, 1, 2) as cntrycode, c_acctbal
from customer
where substring(c_phone, 1, 2) in ('{I1}','{I2}','{I3}','{I4}','{I5}','{I6}','{I7}')
and c_acctbal > (
select avg(c_acctbal) from customer
where c_acctbal > 0.00
and substring(c_phone, 1, 2) in ('{I1}','{I2}','{I3}','{I4}','{I5}','{I6}','{I7}')
)
and not exists (select * from orders where o_custkey = c_custkey)
) as custsale
group by cntrycode
order by cntrycode
```

</details>

<details>
<summary>Oracle / SAP HANA — <code>substr(c_phone, 1, 2)</code>; subquery alias without <code>as</code></summary>

```sql
select cntrycode, count(*) as numcust, sum(c_acctbal) as totacctbal
from (
select substr(c_phone, 1, 2) as cntrycode, c_acctbal
from customer
where substr(c_phone, 1, 2) in ('{I1}','{I2}','{I3}','{I4}','{I5}','{I6}','{I7}')
and c_acctbal > (
select avg(c_acctbal) from customer
where c_acctbal > 0.00
and substr(c_phone, 1, 2) in ('{I1}','{I2}','{I3}','{I4}','{I5}','{I6}','{I7}')
)
and not exists (select * from orders where o_custkey = c_custkey)
) custsale
group by cntrycode
order by cntrycode
```

</details>

<details>
<summary>Citus — nested correlated subqueries rewritten as CTEs with LEFT JOIN</summary>

```sql
with avg_acctbal as (
select
substring(c_phone from 1 for 2) as cntrycode,
avg(c_acctbal) as avg_balance
from customer
where c_acctbal > 0.00
and substring(c_phone from 1 for 2) in ('{I1}', '{I2}', '{I3}', '{I4}', '{I5}', '{I6}', '{I7}')
group by substring(c_phone from 1 for 2)
),
no_orders as (
select o_custkey from orders group by o_custkey
)
select
substring(c.c_phone from 1 for 2) as cntrycode,
count(*) as numcust,
sum(c.c_acctbal) as totacctbal
from
customer c
inner join avg_acctbal a on substring(c.c_phone from 1 for 2) = a.cntrycode
left join no_orders o on c.c_custkey = o.o_custkey
where
substring(c.c_phone from 1 for 2) in ('{I1}', '{I2}', '{I3}', '{I4}', '{I5}', '{I6}', '{I7}')
and c.c_acctbal > a.avg_balance
and o.o_custkey is null
group by substring(c.c_phone from 1 for 2)
order by cntrycode
```

</details>

---

## Cross-Reference: Dialect Overrides by Query

A checkmark means that DBMS has a SQL override in the config; blank means the default SQL is used.

| Query | MySQL | T-SQL | Oracle | SAP HANA | DB2 | MonetDB | Clickhouse | OmniSci | MariaDBCS | Citus | PostgreSQL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | ✓ | ✓ | | ✓ | ✓ | ✓ | | | | | |
| Q2 | | ✓ | ✓ | | | | ✓ | ✓ | ✓ | | |
| Q3 | ✓ | ✓ | ✓ | | | | | | | | |
| Q4 | ✓ | ✓ | | ✓ | ✓ | | | | | ✓ | |
| Q5 | ✓ | ✓ | | ✓ | ✓ | | | | ✓ | | |
| Q6 | ✓ | ✓ | | ✓ | ✓ | | ✓ | | | | |
| Q7 | ✓ | ✓ | | | | | | | | | |
| Q8 | ✓ | ✓ | | | | | | | | ✓ | ✓ |
| Q9 | ✓ | ✓ | | | | | | ✓ | | | |
| Q10 | ✓ | ✓ | ✓ | ✓ | ✓ | | | | | ✓ | ✓ |
| Q11 | | | | | ✓ | | ✓ | | | | |
| Q12 | ✓ | ✓ | | ✓ | ✓ | | | | | | |
| Q13 | | | | | | | | | | | |
| Q14 | ✓ | ✓ | | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| Q15 | ✓ | ✓ | | ✓ | ✓ | ✓ | | | | | |
| Q16 | | | | | | | | | | | |
| Q17 | | | | | | | ✓ | ✓ | ✓ | ✓ | |
| Q18 | ✓ | ✓ | ✓ | | | | | | | | |
| Q19 | | | | | | | | | ✓ | | |
| Q20 | ✓ | ✓ | | ✓ | ✓ | | ✓ | ✓ | | ✓ | |
| Q21 | | ✓ | ✓ | | | | | | | | |
| Q22 | | ✓ | ✓ | ✓ | | | | | | ✓ | |

---

## Stream Ordering

The TPC-H specification defines 40 stream orderings, each a permutation of Q1–Q22, for
throughput testing. Bexhoma stores these in the `stream_ordering` dict (keys 1–40).
The power test uses a single stream; the throughput test cycles through multiple streams
in parallel.

Example (stream 1): Q21 → Q3 → Q18 → Q5 → Q11 → Q7 → Q6 → Q20 → Q17 → Q12 → Q16 →
Q15 → Q13 → Q10 → Q2 → Q8 → Q14 → Q19 → Q9 → Q22 → Q1 → Q4

The full ordering table is defined in the config file under the `stream_ordering` key.
