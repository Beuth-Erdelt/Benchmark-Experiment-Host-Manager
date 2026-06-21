# TPC-DS Query Reference

The [TPC-DS](https://www.tpc.org/tpcds/) benchmark defines 99 decision-support queries covering three
retail channels (store, catalog, web) and associated returns. This page documents all 99 queries as
implemented in Bexhoma, including the TPC-DS reference SQL and any DBMS-specific dialect variants.

> **Reference version:** All SQL templates and parameter distributions on this page are taken from
> **TPC-DS v4.0.0** (`DSGen-software-code-4.0.0/query_templates/` and `query_variants/`).

## Configuration File

Queries are stored in [`experiments/tpcds/queries-tpcds.config`](../experiments/tpcds/queries-tpcds.config).
The format is defined by the [`dbmsbenchmarker`](https://github.com/perdelt/dbmsbenchmarker) Python
package. Each entry is a Python dict:

| Key | Description |
|-----|-------------|
| `'title'` | Label used in result tables |
| `'query'` | SQL string or list of SQL strings (multi-statement queries) |
| `'DBMS'` | Optional dict: DBMS name → dialect-specific SQL |
| `'parameter'` | Dict of runtime substitution parameters |
| `'active'` | Whether this query runs |
| `'numWarmup'` / `'numCooldown'` | Warm-up / cool-down runs |
| `'numRun'` | Number of measured runs |
| `'timer'` | Timer configuration |

## Placeholder Convention

| Notation | Used in | Meaning |
|----------|---------|---------|
| `[PARAM]` | TPC-DS template files (`.tpl`) | Substitution placeholder |
| `{PARAM}` | Bexhoma config SQL | Runtime parameter, substituted by `dbmsbenchmarker` |
| `[_LIMITA] select [_LIMITB] … [_LIMITC]` | TPC-DS template | Row-limit markers |
| `select … limit N` | Bexhoma config SQL | Concrete row limit (typically 100) |

## Parameter Types

| Config type | Meaning |
|-------------|---------|
| `"integer"` with `"range": [min, max]` | Uniform random integer in [min, max] |
| `"list"` with `"range": [v1, v2, …]` | One value chosen uniformly from the list |
| `"integer"` or `"list"` with `"size": N` | N independent draws, substituted as `{PARAM1}`, `{PARAM2}`, …, `{PARAMN}` |

## Multi-Statement Queries

Q14, Q23, Q24, and Q39 each consist of two SQL statements executed in sequence.
In the config, `'query'` is a Python list `[sql_a, sql_b]`. Both statements share the same
parameter substitution.

## DBMS Dialect Overrides

Sixteen queries carry a `'DBMS'` key with dialect-specific SQL for one or more systems:

| Query | DBMS overrides | Reason |
|-------|---------------|--------|
| Q5 | MariaDB | Nested CTE workaround (MariaDB <10.4 cannot have CTEs defined inside CTE bodies) |
| Q14a+b | MariaDB | Nested CTE workaround + `INTERSECT` substitute |
| Q18 | MariaDB, MonetDB, PostgreSQL | `GROUP BY ROLLUP` syntax differences |
| Q22 | MariaDB, MonetDB, PostgreSQL | `GROUP BY ROLLUP` syntax differences |
| Q27 | MonetDB, PostgreSQL | `GROUP BY ROLLUP` syntax differences |
| Q36 | MonetDB, PostgreSQL | `GROUP BY ROLLUP` syntax differences |
| Q51 | MySQL | `FULL OUTER JOIN` not supported; rewritten with `UNION ALL` |
| Q54 | MySQL | `CAST(… AS INT)` not supported; replaced by `CAST(… AS SIGNED)` |
| Q66 | MonetDB, PostgreSQL | String concatenation `\|\|` → `CONCAT()` |
| Q67 | MonetDB, PostgreSQL | `GROUP BY ROLLUP` syntax differences |
| Q70 | MonetDB, PostgreSQL, Exasol, MemSQL | `GROUP BY ROLLUP` syntax differences |
| Q77 | MariaDB, MonetDB, PostgreSQL | Nested CTE workaround + `GROUP BY ROLLUP` |
| Q80 | MariaDB, MonetDB, PostgreSQL, MemSQL | Nested CTE workaround + `GROUP BY ROLLUP` |
| Q84 | MonetDB, PostgreSQL | String concatenation `\|\|` → `CONCAT()` |
| Q86 | MariaDB, MonetDB, PostgreSQL, Exasol, MemSQL | `GROUP BY ROLLUP` syntax differences |
| Q97 | MySQL | `FULL OUTER JOIN` not supported; rewritten with `UNION ALL + GROUP BY` |

---

## Deviations from the TPC-DS Reference Templates

Not every query in bexhoma is a verbatim translation of the TPC-DS template.
Differences fall into two categories:

- **Syntactic** — different SQL dialect or notation, but the query returns the same result set on the same data.
- **Semantic** — the query logic or filter differs, so a different result set is expected compared to a conforming TPC-DS implementation.

### Semantic Differences (different result set expected)

| Query | What bexhoma does | What the template specifies | Effect |
|-------|-------------------|-----------------------------|--------|
| **Q2** | `d_year = {YEAR}` and `d_year = {YEAR}+1` now substituted correctly (previously hardcoded 1998/1999) | Draws `[YEAR]` and `[YEAR]+1` from a uniform distribution (1998–2001) | **Fixed** — all year pairs now exercised |
| **Q5** | Date window corrected to `interval '30' day` (previously `interval '14' day`) | `+ 30 days` | **Fixed** |
| **Q13** | `d_year = {YEAR}` now substituted (previously hardcoded 2001); `YEAR` parameter added (1998–2002) | Draws `[YEAR]` from uniform distribution | **Fixed** |
| **Q30** | `STATE` expanded to all 43 US state codes (previously only `["TN"]`) | Draws `[STATE]` from `fips_county` distribution (any US state) | **Fixed** |
| **Q49** | `d_moy` filter removed from all three channel subqueries; `MONTH` parameter removed | No month filter; the template aggregates an entire year | **Fixed** |
| **Q98** | Start date uses `{DAY}` parameter (integer 1–28) instead of hardcoded `01`; `DAY` parameter added | Start date drawn from a sales-weighted date distribution within Jan–Jul of `[YEAR]` | **Approximated** — uniform day distribution used; sales-weighted draw not expressible in dbmsbenchmarker |

### Syntactic Differences (same result set, dialect adaptation)

| Difference | Queries affected | Notes |
|------------|-----------------|-------|
| `GROUP BY … WITH ROLLUP` (MySQL/MariaDB default) vs. `GROUP BY ROLLUP(…)` (standard SQL) | Q5, Q18, Q22, Q27, Q36, Q67, Q70, Q77, Q80, Q86 | Per-DBMS overrides in the `'DBMS'` key handle each target system |
| `CONCAT('a', ',', 'b')` vs. standard `'a' \|\| ',' \|\| 'b'` | Q5, Q66, Q84 | MySQL/MariaDB default; `\|\|` used in PostgreSQL/MonetDB/Exasol overrides |
| `interval 'N' day` vs. `+ N days` date arithmetic | Q5, Q21, Q32, Q72, Q77, Q80, Q92 | Both express the same time offset; dialect normalised for portability |
| `ORDER BY col IS NOT NULL, col` (explicit NULL-last sort) vs. plain `ORDER BY col` | Q5, Q65, Q72 | Added to make NULL ordering deterministic across DBMS that differ in default NULL position |
| `FULL OUTER JOIN` rewritten as `UNION ALL + GROUP BY` for MySQL | Q51, Q97 | MySQL/MariaDB override; the rewrite is logically equivalent |
| `CAST(… AS SIGNED)` vs. `CAST(… AS INT)` | Q54 (MySQL override) | MySQL does not support `INT` as a cast target |
| `CAST(inv_after AS FLOAT) / inv_before` vs. plain division | Q21 | Forces floating-point division; semantically equivalent on non-integer inputs |
| Nested CTE workaround (outer CTE wraps everything) | Q5 (MariaDB), Q14a+b (MariaDB), Q77 (MariaDB), Q80 (MariaDB) | MariaDB <10.4 cannot reference a CTE from inside another CTE body |

---

## Q1 — Store Returns: High Return Rate Customers

Finds customers whose total returns at a given store exceed 120% of the average return for that store,
filtered to a specific state and year.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `AGG_FIELD` | list | `SR_RETURN_AMT`, `SR_FEE`, `SR_REFUNDED_CASH`, `SR_RETURN_AMT_INC_TAX`, `SR_REVERSED_CHARGE`, `SR_STORE_CREDIT`, `SR_RETURN_TAX` |
| `STATE` | list | US state abbreviations (51 values, AK–WY) |
| `YEAR` | integer | 1998–2002 |

<details>
<summary>TPC-DS Reference SQL (query1.tpl)</summary>

```sql
with customer_total_return as
(select sr_customer_sk as ctr_customer_sk
,sr_store_sk as ctr_store_sk
,sum([AGG_FIELD]) as ctr_total_return
from store_returns
,date_dim
where sr_returned_date_sk = d_date_sk
and d_year =[YEAR]
group by sr_customer_sk
,sr_store_sk)
[_LIMITA] select [_LIMITB] c_customer_id
from customer_total_return ctr1
,store
,customer
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
from customer_total_return ctr2
where ctr1.ctr_store_sk = ctr2.ctr_store_sk)
and s_store_sk = ctr1.ctr_store_sk
and s_state = '[STATE]'
and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id
[_LIMITC];
```

</details>

---

## Q2 — Weekly Sales Ratio Year-over-Year

Computes the ratio of sales per day-of-week between two consecutive years across web and catalog channels.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2001 |

<details>
<summary>TPC-DS Reference SQL (query2.tpl)</summary>

```sql
with wscs as
(select sold_date_sk
       ,sales_price
 from (select ws_sold_date_sk sold_date_sk
             ,ws_ext_sales_price sales_price
       from web_sales
       union all
       select cs_sold_date_sk sold_date_sk
             ,cs_ext_sales_price sales_price
       from catalog_sales)),
wswscs as
(select d_week_seq,
       sum(case when (d_day_name='Sunday') then sales_price else null end) sun_sales,
       sum(case when (d_day_name='Monday') then sales_price else null end) mon_sales,
       sum(case when (d_day_name='Tuesday') then sales_price else  null end) tue_sales,
       sum(case when (d_day_name='Wednesday') then sales_price else null end) wed_sales,
       sum(case when (d_day_name='Thursday') then sales_price else null end) thu_sales,
       sum(case when (d_day_name='Friday') then sales_price else null end) fri_sales,
       sum(case when (d_day_name='Saturday') then sales_price else null end) sat_sales
from wscs
    ,date_dim
where d_date_sk = sold_date_sk
group by d_week_seq)
select d_week_seq1
      ,round(sun_sales1/sun_sales2,2)
      ,round(mon_sales1/mon_sales2,2)
      ,round(tue_sales1/tue_sales2,2)
      ,round(wed_sales1/wed_sales2,2)
      ,round(thu_sales1/thu_sales2,2)
      ,round(fri_sales1/fri_sales2,2)
      ,round(sat_sales1/sat_sales2,2)
from
(select wswscs.d_week_seq d_week_seq1
       ,sun_sales sun_sales1
       ,mon_sales mon_sales1
       ,tue_sales tue_sales1
       ,wed_sales wed_sales1
       ,thu_sales thu_sales1
       ,fri_sales fri_sales1
       ,sat_sales sat_sales1
 from wswscs,date_dim
 where date_dim.d_week_seq = wswscs.d_week_seq and
       d_year = [YEAR]) y,
(select wswscs.d_week_seq d_week_seq2
       ,sun_sales sun_sales2
       ,mon_sales mon_sales2
       ,tue_sales tue_sales2
       ,wed_sales wed_sales2
       ,thu_sales thu_sales2
       ,fri_sales fri_sales2
       ,sat_sales sat_sales2
 from wswscs
     ,date_dim
 where date_dim.d_week_seq = wswscs.d_week_seq and
       d_year = [YEAR]+1) z
where d_week_seq1=d_week_seq2-53
order by d_week_seq1;
```

</details>

> **Bexhoma note:** The template uses `[YEAR]` and `[YEAR]+1` for consecutive years. Bexhoma hardcodes
> `d_year = 1998` and `d_year = 1999` in the subqueries instead of using the `{YEAR}` parameter for
> the year-plus-one case.

---

## Q3 — Brand Sales by Month

Finds the top-selling brands in the store channel for a given manufacturer and month, with selectable aggregation.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `MONTH` | integer | 11–12 |
| `MANUFACT` | integer | 1–1000 |
| `AGGC` | list | `ss_ext_sales_price`, `ss_sales_price`, `ss_ext_discount_amt`, `ss_net_profit` |

<details>
<summary>TPC-DS Reference SQL (query3.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] dt.d_year
      ,item.i_brand_id brand_id
      ,item.i_brand brand
      ,sum([AGGC]) sum_agg
from  date_dim dt
     ,store_sales
     ,item
where dt.d_date_sk = store_sales.ss_sold_date_sk
  and store_sales.ss_item_sk = item.i_item_sk
  and item.i_manufact_id = [MANUFACT]
  and dt.d_moy=[MONTH]
group by dt.d_year
     ,item.i_brand
     ,item.i_brand_id
order by dt.d_year
        ,sum_agg desc
        ,brand_id
[_LIMITC];
```

</details>

---

## Q4 — Multi-Channel Customer Year-over-Year Growth

Finds customers whose spending growth in catalog and web channels exceeds their store spending growth
between two consecutive years. Uses a selectable customer attribute in the output.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2001 |
| `SELECTONE` | list | `t_s_secyear.customer_preferred_cust_flag`, `t_s_secyear.customer_birth_country`, `t_s_secyear.customer_login`, `t_s_secyear.customer_email_address` |

<details>
<summary>TPC-DS Reference SQL (query4.tpl)</summary>

```sql
with year_total as (
 select c_customer_id customer_id
       ,c_first_name customer_first_name
       ,c_last_name customer_last_name
       ,c_preferred_cust_flag customer_preferred_cust_flag
       ,c_birth_country customer_birth_country
       ,c_login customer_login
       ,c_email_address customer_email_address
       ,d_year dyear
       ,sum(((ss_ext_list_price-ss_ext_wholesale_cost-ss_ext_discount_amt)+ss_ext_sales_price)/2) year_total
       ,'s' sale_type
 from customer, store_sales, date_dim
 where c_customer_sk = ss_customer_sk
   and ss_sold_date_sk = d_date_sk
 group by c_customer_id, c_first_name, c_last_name, c_preferred_cust_flag,
          c_birth_country, c_login, c_email_address, d_year
 union all
 select c_customer_id customer_id
       ,c_first_name customer_first_name
       ,c_last_name customer_last_name
       ,c_preferred_cust_flag customer_preferred_cust_flag
       ,c_birth_country customer_birth_country
       ,c_login customer_login
       ,c_email_address customer_email_address
       ,d_year dyear
       ,sum((((cs_ext_list_price-cs_ext_wholesale_cost-cs_ext_discount_amt)+cs_ext_sales_price)/2)) year_total
       ,'c' sale_type
 from customer, catalog_sales, date_dim
 where c_customer_sk = cs_bill_customer_sk
   and cs_sold_date_sk = d_date_sk
 group by c_customer_id, c_first_name, c_last_name, c_preferred_cust_flag,
          c_birth_country, c_login, c_email_address, d_year
 union all
 select c_customer_id customer_id
       ,c_first_name customer_first_name
       ,c_last_name customer_last_name
       ,c_preferred_cust_flag customer_preferred_cust_flag
       ,c_birth_country customer_birth_country
       ,c_login customer_login
       ,c_email_address customer_email_address
       ,d_year dyear
       ,sum((((ws_ext_list_price-ws_ext_wholesale_cost-ws_ext_discount_amt)+ws_ext_sales_price)/2)) year_total
       ,'w' sale_type
 from customer, web_sales, date_dim
 where c_customer_sk = ws_bill_customer_sk
   and ws_sold_date_sk = d_date_sk
 group by c_customer_id, c_first_name, c_last_name, c_preferred_cust_flag,
          c_birth_country, c_login, c_email_address, d_year)
[_LIMITA] select [_LIMITB]
                 t_s_secyear.customer_id
                ,t_s_secyear.customer_first_name
                ,t_s_secyear.customer_last_name
                ,[SELECTONE]
 from year_total t_s_firstyear, year_total t_s_secyear,
      year_total t_c_firstyear, year_total t_c_secyear,
      year_total t_w_firstyear, year_total t_w_secyear
 where t_s_secyear.customer_id = t_s_firstyear.customer_id
   and t_s_firstyear.customer_id = t_c_secyear.customer_id
   and t_s_firstyear.customer_id = t_c_firstyear.customer_id
   and t_s_firstyear.customer_id = t_w_firstyear.customer_id
   and t_s_firstyear.customer_id = t_w_secyear.customer_id
   and t_s_firstyear.sale_type = 's' and t_c_firstyear.sale_type = 'c'
   and t_w_firstyear.sale_type = 'w' and t_s_secyear.sale_type = 's'
   and t_c_secyear.sale_type = 'c' and t_w_secyear.sale_type = 'w'
   and t_s_firstyear.dyear = [YEAR] and t_s_secyear.dyear = [YEAR]+1
   and t_c_firstyear.dyear = [YEAR] and t_c_secyear.dyear = [YEAR]+1
   and t_w_firstyear.dyear = [YEAR] and t_w_secyear.dyear = [YEAR]+1
   and t_s_firstyear.year_total > 0 and t_c_firstyear.year_total > 0
   and t_w_firstyear.year_total > 0
   and case when t_c_firstyear.year_total > 0 then t_c_secyear.year_total / t_c_firstyear.year_total else null end
           > case when t_s_firstyear.year_total > 0 then t_s_secyear.year_total / t_s_firstyear.year_total else null end
   and case when t_c_firstyear.year_total > 0 then t_c_secyear.year_total / t_c_firstyear.year_total else null end
           > case when t_w_firstyear.year_total > 0 then t_w_secyear.year_total / t_w_firstyear.year_total else null end
 order by t_s_secyear.customer_id, t_s_secyear.customer_first_name,
          t_s_secyear.customer_last_name, [SELECTONE]
[_LIMITC];
```

</details>

---

## Q5 — Net Revenue by Sales Channel with Rollup

Reports sales, returns, and net profit for store, catalog, and web channels with subtotals using `ROLLUP`.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DAY` | integer | 1–30 |
| `MONTH` | integer | 8–8 |
| `YEAR` | integer | 1998–2002 |

<details>
<summary>TPC-DS Reference SQL (query5.tpl)</summary>

```sql
with ssr as (
 select s_store_id,
        sum(sales_price) as sales, sum(profit) as profit,
        sum(return_amt) as returns, sum(net_loss) as profit_loss
 from (
   select ss_store_sk as store_sk, ss_sold_date_sk as date_sk,
          ss_ext_sales_price as sales_price, ss_net_profit as profit,
          cast(0 as decimal(7,2)) as return_amt, cast(0 as decimal(7,2)) as net_loss
   from store_sales
   union all
   select sr_store_sk as store_sk, sr_returned_date_sk as date_sk,
          cast(0 as decimal(7,2)) as sales_price, cast(0 as decimal(7,2)) as profit,
          sr_return_amt as return_amt, sr_net_loss as net_loss
   from store_returns) salesreturns, date_dim, store
 where date_sk = d_date_sk
   and d_date between cast('[SALES_DATE]' as date)
              and (cast('[SALES_DATE]' as date) + 14 days)
   and store_sk = s_store_sk
 group by s_store_id),
csr as (... catalog channel analog ...),
wsr as (... web channel analog ...)
[_LIMITA] select [_LIMITB] channel, id,
       sum(sales) as sales, sum(returns) as returns, sum(profit) as profit
from (
  select 'store channel' as channel, 'store' || s_store_id as id,
         sales, returns, (profit - profit_loss) as profit from ssr
  union all
  select 'catalog channel' as channel, 'catalog_page' || cp_catalog_page_id as id,
         sales, returns, (profit - profit_loss) as profit from csr
  union all
  select 'web channel' as channel, 'web_site' || web_site_id as id,
         sales, returns, (profit - profit_loss) as profit from wsr
) x
group by rollup (channel, id)
order by channel, id
[_LIMITC];
```

</details>

> **Bexhoma note:** The template uses `SALES_DATE` (a generated date in month `{MONTH}`/year `{YEAR}`);
> Bexhoma exposes `{YEAR}`, `{MONTH}`, and `{DAY}` as separate integer parameters and constructs
> `cast('{YEAR}-{MONTH}-{DAY}' as date)` in the SQL. The template uses standard SQL `|| ` for
> string concatenation and `GROUP BY ROLLUP(channel, id)` syntax; the bexhoma default SQL uses
> MySQL-compatible `GROUP BY channel, id WITH ROLLUP` and `CONCAT(...)` instead.

<details>
<summary>MariaDB dialect (nested CTE workaround)</summary>

MariaDB older versions cannot reference one CTE body from another within the same `WITH` clause.
Bexhoma wraps `ssr`, `csr`, and `wsr` in a nested CTE structure using `with total as (...)`.

</details>

---

## Q6 — State-Level Customer Purchase Behavior

Counts customers per state who bought items priced above 120% of their category average in a specific year-month.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `MONTH` | integer | 1–7 |

<details>
<summary>TPC-DS Reference SQL (query6.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] a.ca_state state, count(*) cnt
from customer_address a, customer c, store_sales s, date_dim d, item i
where a.ca_address_sk = c.c_current_addr_sk
  and c.c_customer_sk = s.ss_customer_sk
  and s.ss_sold_date_sk = d.d_date_sk
  and s.ss_item_sk = i.i_item_sk
  and d.d_month_seq =
       (select distinct (d_month_seq)
        from date_dim
        where d_year = [YEAR] and d_moy = [MONTH])
  and i.i_current_price > 1.2 *
       (select avg(j.i_current_price) from item j where j.i_category = i.i_category)
group by a.ca_state
having count(*) >= 10
order by cnt, a.ca_state
[_LIMITC];
```

</details>

---

## Q7 — Store Sales by Item and Demographics

Averages quantity, list price, coupon amount, and sales price per item in the store channel,
filtered by customer gender, marital status, and education status.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `MS` | list | M, S, D, W, U |
| `GEN` | list | M, F |
| `ES` | list | Primary, Secondary, College, 2 yr Degree, 4 yr Degree, Advanced Degree, Unknown |

<details>
<summary>TPC-DS Reference SQL (query7.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] i_item_id,
       avg(ss_quantity) agg1, avg(ss_list_price) agg2,
       avg(ss_coupon_amt) agg3, avg(ss_sales_price) agg4
from store_sales, customer_demographics, date_dim, item, promotion
where ss_sold_date_sk = d_date_sk
  and ss_item_sk = i_item_sk
  and ss_cdemo_sk = cd_demo_sk
  and ss_promo_sk = p_promo_sk
  and cd_gender = '[GEN]'
  and cd_marital_status = '[MS]'
  and cd_education_status = '[ES]'
  and (p_channel_email = 'N' or p_channel_event = 'N')
  and d_year = [YEAR]
group by i_item_id
order by i_item_id
[_LIMITC];
```

</details>

---

## Q8 — Net Profit per Store by ZIP Code

Finds net profit per store for customers whose ZIP codes appear in a large IN-list of 400 codes
(intersected with preferred customers), filtered by quarter and year.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `ZIP` | integer (×400) | 10000–99999 — 400 independent draws, substituted as `{ZIP.1}`…`{ZIP.400}` |
| `YEAR` | integer | 1998–2002 |
| `QOY` | integer | 1–2 |

<details>
<summary>TPC-DS Reference SQL (query8.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] s_store_name, sum(ss_net_profit)
from store_sales, date_dim, store,
     (select ca_zip from (
       SELECT substr(ca_zip,1,5) ca_zip FROM customer_address
       WHERE substr(ca_zip,1,5) IN ('[ZIP.1]','[ZIP.2]',...,'[ZIP.400]')
       intersect
       select ca_zip from (
         SELECT substr(ca_zip,1,5) ca_zip, count(*) cnt
         FROM customer_address, customer
         WHERE ca_address_sk = c_current_addr_sk
           and c_preferred_cust_flag='Y'
         group by ca_zip having count(*) > 10) A1) A2) V1
where ss_store_sk = s_store_sk
  and ss_sold_date_sk = d_date_sk
  and d_qoy = [QOY] and d_year = [YEAR]
  and (substr(s_zip,1,2) = substr(V1.ca_zip,1,2))
group by s_store_name
order by s_store_name
[_LIMITC];
```

</details>

> **Bexhoma note:** The 400-element IN-list uses `{ZIP.1}` through `{ZIP.400}`, generated from a
> single `ZIP` parameter with `'size': 400`.

---

## Q9 — Conditional Bucket Aggregation

Computes conditional averages over store sales quantity buckets (1–20, 21–40, 41–60, 61–80, 81–100),
choosing between two aggregation columns based on a count threshold.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `RC` | integer (×5) | 1–567080 — 5 draws, substituted as `{RC.1}`…`{RC.5}` |
| `AGGCTHEN` | list | `ss_ext_discount_amt`, `ss_ext_sales_price`, `ss_ext_list_price`, `ss_ext_tax` |
| `AGGCELSE` | list | `ss_net_paid`, `ss_net_paid_inc_tax`, `ss_net_profit` |

<details>
<summary>TPC-DS Reference SQL (query9.tpl)</summary>

```sql
select
  case when (select count(*) from store_sales where ss_quantity between 1 and 20)   > [RC.1]
       then (select avg([AGGCTHEN]) from store_sales where ss_quantity between 1 and 20)
       else (select avg([AGGCELSE]) from store_sales where ss_quantity between 1 and 20) end bucket1,
  case when (select count(*) from store_sales where ss_quantity between 21 and 40)  > [RC.2]
       then (select avg([AGGCTHEN]) from store_sales where ss_quantity between 21 and 40)
       else (select avg([AGGCELSE]) from store_sales where ss_quantity between 21 and 40) end bucket2,
  case when (select count(*) from store_sales where ss_quantity between 41 and 60)  > [RC.3]
       then (select avg([AGGCTHEN]) from store_sales where ss_quantity between 41 and 60)
       else (select avg([AGGCELSE]) from store_sales where ss_quantity between 41 and 60) end bucket3,
  case when (select count(*) from store_sales where ss_quantity between 61 and 80)  > [RC.4]
       then (select avg([AGGCTHEN]) from store_sales where ss_quantity between 61 and 80)
       else (select avg([AGGCELSE]) from store_sales where ss_quantity between 61 and 80) end bucket4,
  case when (select count(*) from store_sales where ss_quantity between 81 and 100) > [RC.5]
       then (select avg([AGGCTHEN]) from store_sales where ss_quantity between 81 and 100)
       else (select avg([AGGCELSE]) from store_sales where ss_quantity between 81 and 100) end bucket5
from reason
where r_reason_sk = 1;
```

</details>

---

## Q10 — Customer Demographics Multi-Channel Analysis

Reports demographic breakdown of customers who shopped in store sales and also in web or catalog sales,
filtered by a 10-county set over a 3-month window.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1999–2002 |
| `MONTH` | integer | 1–4 |
| `COUNTY` | list (×10) | 10 random draws from US county list (1870+ values) — substituted as `{COUNTY.1}`…`{COUNTY.10}` |

<details>
<summary>TPC-DS Reference SQL (query10.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  cd_gender, cd_marital_status, cd_education_status, count(*) cnt1,
  cd_purchase_estimate, count(*) cnt2, cd_credit_rating, count(*) cnt3,
  cd_dep_count, count(*) cnt4, cd_dep_employed_count, count(*) cnt5,
  cd_dep_college_count, count(*) cnt6
from customer c, customer_address ca, customer_demographics
where c.c_current_addr_sk = ca.ca_address_sk
  and ca_county in ('[COUNTY.1]','[COUNTY.2]','[COUNTY.3]','[COUNTY.4]','[COUNTY.5]',
                    '[COUNTY.6]','[COUNTY.7]','[COUNTY.8]','[COUNTY.9]','[COUNTY.10]')
  and cd_demo_sk = c.c_current_cdemo_sk
  and exists (select * from store_sales, date_dim
              where c.c_customer_sk = ss_customer_sk
                and ss_sold_date_sk = d_date_sk
                and d_year = [YEAR]
                and d_moy between [MONTH] and [MONTH]+3)
  and (exists (select * from web_sales, date_dim
               where c.c_customer_sk = ws_bill_customer_sk
                 and ws_sold_date_sk = d_date_sk
                 and d_year = [YEAR]
                 and d_moy between [MONTH] and [MONTH]+3)
    or exists (select * from catalog_sales, date_dim
               where c.c_customer_sk = cs_ship_customer_sk
                 and cs_sold_date_sk = d_date_sk
                 and d_year = [YEAR]
                 and d_moy between [MONTH] and [MONTH]+3))
group by cd_gender, cd_marital_status, cd_education_status, cd_purchase_estimate,
         cd_credit_rating, cd_dep_count, cd_dep_employed_count, cd_dep_college_count
order by cd_gender, cd_marital_status, cd_education_status, cd_purchase_estimate,
         cd_credit_rating, cd_dep_count, cd_dep_employed_count, cd_dep_college_count
[_LIMITC];
```

</details>

---

## Q11 — Web vs. Store Year-over-Year Customer Growth

Finds customers whose web spending growth exceeds their store spending growth between two consecutive years.
Uses list price minus discount as the spending measure (vs. Q4 which uses a more complex average).

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2001 |
| `SELECTONE` | list | `t_s_secyear.customer_preferred_cust_flag`, `t_s_secyear.customer_birth_country`, `t_s_secyear.customer_login`, `t_s_secyear.customer_email_address` |

<details>
<summary>TPC-DS Reference SQL (query11.tpl)</summary>

```sql
with year_total as (
 select c_customer_id customer_id, c_first_name customer_first_name,
        c_last_name customer_last_name, c_preferred_cust_flag customer_preferred_cust_flag,
        c_birth_country customer_birth_country, c_login customer_login,
        c_email_address customer_email_address, d_year dyear,
        sum(ss_ext_list_price-ss_ext_discount_amt) year_total, 's' sale_type
 from customer, store_sales, date_dim
 where c_customer_sk = ss_customer_sk and ss_sold_date_sk = d_date_sk
 group by c_customer_id, c_first_name, c_last_name, c_preferred_cust_flag,
          c_birth_country, c_login, c_email_address, d_year
 union all
 select c_customer_id customer_id, c_first_name customer_first_name,
        c_last_name customer_last_name, c_preferred_cust_flag customer_preferred_cust_flag,
        c_birth_country customer_birth_country, c_login customer_login,
        c_email_address customer_email_address, d_year dyear,
        sum(ws_ext_list_price-ws_ext_discount_amt) year_total, 'w' sale_type
 from customer, web_sales, date_dim
 where c_customer_sk = ws_bill_customer_sk and ws_sold_date_sk = d_date_sk
 group by c_customer_id, c_first_name, c_last_name, c_preferred_cust_flag,
          c_birth_country, c_login, c_email_address, d_year)
[_LIMITA] select [_LIMITB]
       t_s_secyear.customer_id, t_s_secyear.customer_first_name,
       t_s_secyear.customer_last_name, [SELECTONE]
from year_total t_s_firstyear, year_total t_s_secyear,
     year_total t_w_firstyear, year_total t_w_secyear
where t_s_secyear.customer_id = t_s_firstyear.customer_id
  and t_s_firstyear.customer_id = t_w_secyear.customer_id
  and t_s_firstyear.customer_id = t_w_firstyear.customer_id
  and t_s_firstyear.sale_type = 's' and t_w_firstyear.sale_type = 'w'
  and t_s_secyear.sale_type = 's' and t_w_secyear.sale_type = 'w'
  and t_s_firstyear.dyear = [YEAR] and t_s_secyear.dyear = [YEAR]+1
  and t_w_firstyear.dyear = [YEAR] and t_w_secyear.dyear = [YEAR]+1
  and t_s_firstyear.year_total > 0 and t_w_firstyear.year_total > 0
  and case when t_w_firstyear.year_total > 0 then t_w_secyear.year_total / t_w_firstyear.year_total else 0.0 end
      > case when t_s_firstyear.year_total > 0 then t_s_secyear.year_total / t_s_firstyear.year_total else 0.0 end
order by t_s_secyear.customer_id, t_s_secyear.customer_first_name,
         t_s_secyear.customer_last_name, [SELECTONE]
[_LIMITC];
```

</details>

---

## Q12 — Web Sales Revenue Ratio by Item Class

Computes revenue contribution (as a percentage of class total) per item in up to 3 selected categories
for a 30-day sales window.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `CATEGORY` | list (×3) | 3 draws from: Books, Children, Electronics, Home, Jewelry, Men, Music, Shoes, Sports, Women |

<details>
<summary>TPC-DS Reference SQL (query12.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] i_item_id, i_item_desc, i_category, i_class, i_current_price,
       sum(ws_ext_sales_price) as itemrevenue,
       sum(ws_ext_sales_price)*100/sum(sum(ws_ext_sales_price)) over
           (partition by i_class) as revenueratio
from web_sales, item, date_dim
where ws_item_sk = i_item_sk
  and i_category in ('[CATEGORY.1]', '[CATEGORY.2]', '[CATEGORY.3]')
  and ws_sold_date_sk = d_date_sk
  and d_date between cast('[SDATE]' as date) and (cast('[SDATE]' as date) + 30 days)
group by i_item_id, i_item_desc, i_category, i_class, i_current_price
order by i_category, i_class, i_item_id, i_item_desc, revenueratio
[_LIMITC];
```

</details>

> **Bexhoma note:** The template uses `[SDATE]` (a random date sampled from sales data). Bexhoma
> does not include a date parameter in the config; instead the date filter is replaced with a fixed
> date range in the SQL.

---

## Q13 — Store Sales Aggregates by Demographics and Geography

Computes simple aggregates on store sales filtered by three demographic combinations paired with
three geographic regions, each with different price/profit constraints.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `STATE` | list (×9) | 9 draws from US state codes (44 values) — substituted as `{STATE.1}`…`{STATE.9}` |
| `MS` | list (×3) | 3 draws from: M, S, D, W, U — substituted as `{MS.1}`…`{MS.3}` |
| `ES` | list (×3) | 3 draws from: Primary, Secondary, College, 2 yr Degree, 4 yr Degree, Advanced Degree, Unknown |

<details>
<summary>TPC-DS Reference SQL (query13.tpl)</summary>

```sql
select avg(ss_quantity), avg(ss_ext_sales_price),
       avg(ss_ext_wholesale_cost), sum(ss_ext_wholesale_cost)
from store_sales, store, customer_demographics, household_demographics,
     customer_address, date_dim
where s_store_sk = ss_store_sk
  and ss_sold_date_sk = d_date_sk and d_year = 2001
  and ((ss_hdemo_sk=hd_demo_sk and cd_demo_sk = ss_cdemo_sk
        and cd_marital_status = '[MS.1]' and cd_education_status = '[ES.1]'
        and ss_sales_price between 100.00 and 150.00 and hd_dep_count = 3)
    or (ss_hdemo_sk=hd_demo_sk and cd_demo_sk = ss_cdemo_sk
        and cd_marital_status = '[MS.2]' and cd_education_status = '[ES.2]'
        and ss_sales_price between 50.00 and 100.00 and hd_dep_count = 1)
    or (ss_hdemo_sk=hd_demo_sk and cd_demo_sk = ss_cdemo_sk
        and cd_marital_status = '[MS.3]' and cd_education_status = '[ES.3]'
        and ss_sales_price between 150.00 and 200.00 and hd_dep_count = 1))
  and ((ss_addr_sk = ca_address_sk and ca_country = 'United States'
        and ca_state in ('[STATE.1]','[STATE.2]','[STATE.3]')
        and ss_net_profit between 100 and 200)
    or (ss_addr_sk = ca_address_sk and ca_country = 'United States'
        and ca_state in ('[STATE.4]','[STATE.5]','[STATE.6]')
        and ss_net_profit between 150 and 300)
    or (ss_addr_sk = ca_address_sk and ca_country = 'United States'
        and ca_state in ('[STATE.7]','[STATE.8]','[STATE.9]')
        and ss_net_profit between 50 and 250));
```

</details>

> **Bexhoma note:** The template hardcodes `d_year = 2001`, so date filtering uses a fixed year.

---

## Q14a+b — Cross-Channel Item Sales (Multi-Statement)

Two-statement query. **Part a** finds items sold in November across all three channels in a given year
whose cross-channel sales exceed the average, then rolls up with `UNION`. **Part b** compares store
sales in a specific December week against the prior year for the same items.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2000 |
| `DAY` | integer | 1–28 |

<details>
<summary>TPC-DS Reference SQL (query_variants/query14a.tpl — Part a)</summary>

```sql
with cross_items as (
  select i_item_sk ss_item_sk from item,
  (select iss.i_brand_id brand_id, iss.i_class_id class_id, iss.i_category_id category_id
   from store_sales, item iss, date_dim d1
   where ss_item_sk = iss.i_item_sk and ss_sold_date_sk = d1.d_date_sk
     and d1.d_year between 1999 and 1999+2
   intersect
   select ics.i_brand_id, ics.i_class_id, ics.i_category_id
   from catalog_sales, item ics, date_dim d2
   where cs_item_sk = ics.i_item_sk and cs_sold_date_sk = d2.d_date_sk
     and d2.d_year between 1999 and 1999+2
   intersect
   select iws.i_brand_id, iws.i_class_id, iws.i_category_id
   from web_sales, item iws, date_dim d3
   where ws_item_sk = iws.i_item_sk and ws_sold_date_sk = d3.d_date_sk
     and d3.d_year between 1999 and 1999+2) x
  where i_brand_id = brand_id and i_class_id = class_id and i_category_id = category_id),
avg_sales as (
  select avg(quantity*list_price) average_sales
  from (select ss_quantity quantity, ss_list_price list_price
        from store_sales, date_dim
        where ss_sold_date_sk = d_date_sk and d_year between 1999 and 2001
        union all
        select cs_quantity quantity, cs_list_price list_price
        from catalog_sales, date_dim
        where cs_sold_date_sk = d_date_sk and d_year between [YEAR] and [YEAR]+2
        union all
        select ws_quantity quantity, ws_list_price list_price
        from web_sales, date_dim
        where ws_sold_date_sk = d_date_sk and d_year between [YEAR] and [YEAR]+2) x),
results AS (...)
[_LIMITA] select [_LIMITB] channel, i_brand_id, i_class_id, i_category_id, sum_sales, number_sales
from (select channel, i_brand_id, i_class_id, i_category_id, sum_sales, number_sales from results
      union select channel, i_brand_id, i_class_id, null, sum(sum_sales), sum(number_sales)
            from results group by channel, i_brand_id, i_class_id
      union select channel, i_brand_id, null, null, sum(sum_sales), sum(number_sales)
            from results group by channel, i_brand_id
      union select channel, null, null, null, sum(sum_sales), sum(number_sales)
            from results group by channel
      union select null, null, null, null, sum(sum_sales), sum(number_sales) from results) z
order by channel, i_brand_id, i_class_id, i_category_id
[_LIMITC];
```

</details>

<details>
<summary>TPC-DS Reference SQL (query_variants/query14a.tpl — Part b)</summary>

```sql
with cross_items as (...),
avg_sales as (...)
[_LIMITA] select [_LIMITB] * from
(select 'store' channel, i_brand_id, i_class_id, i_category_id,
        sum(ss_quantity*ss_list_price) sales, count(*) number_sales
 from store_sales, item, date_dim
 where ss_item_sk in (select ss_item_sk from cross_items)
   and ss_item_sk = i_item_sk and ss_sold_date_sk = d_date_sk
   and d_week_seq = (select d_week_seq from date_dim
                     where d_year = [YEAR]+1 and d_moy = 12 and d_dom = [DAY])
 group by i_brand_id, i_class_id, i_category_id
 having sum(ss_quantity*ss_list_price) > (select average_sales from avg_sales)) this_year,
(select 'store' channel, i_brand_id, i_class_id, i_category_id,
        sum(ss_quantity*ss_list_price) sales, count(*) number_sales
 from store_sales, item, date_dim
 where ss_item_sk in (select ss_item_sk from cross_items)
   and ss_item_sk = i_item_sk and ss_sold_date_sk = d_date_sk
   and d_week_seq = (select d_week_seq from date_dim
                     where d_year = [YEAR] and d_moy = 12 and d_dom = [DAY])
 group by i_brand_id, i_class_id, i_category_id
 having sum(ss_quantity*ss_list_price) > (select average_sales from avg_sales)) last_year
where this_year.i_brand_id = last_year.i_brand_id
  and this_year.i_class_id = last_year.i_class_id
  and this_year.i_category_id = last_year.i_category_id
order by this_year.channel, this_year.i_brand_id, this_year.i_class_id, this_year.i_category_id
[_LIMITC];
```

</details>

<details>
<summary>MariaDB dialect</summary>

MariaDB cannot use `INTERSECT` and cannot reference CTEs from within sibling CTE bodies.
Bexhoma rewrites using a nested `with total as (...)` wrapper and replaces `INTERSECT` with
`EXISTS` subqueries. Additionally, the `UNION`-based rollup in Part a is replaced by
`GROUP BY ... WITH ROLLUP`.

</details>

---

## Q15 — Catalog Sales by ZIP Code

Summarizes catalog sales amounts by customer ZIP code, filtered by specific ZIP codes, states, or
high-value sales.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `QOY` | integer | 1–2 |

<details>
<summary>TPC-DS Reference SQL (query15.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] ca_zip, sum(cs_sales_price)
from catalog_sales, customer, customer_address, date_dim
where cs_bill_customer_sk = c_customer_sk
  and c_current_addr_sk = ca_address_sk
  and (substr(ca_zip,1,5) in ('85669','86197','88274','83405','86475',
                               '85392','85460','80348','81792')
    or ca_state in ('CA','WA','GA')
    or cs_sales_price > 500)
  and cs_sold_date_sk = d_date_sk
  and d_qoy = [QOY] and d_year = [YEAR]
group by ca_zip
order by ca_zip
[_LIMITC];
```

</details>

---

## Q16 — Catalog Order Count by County and State

Counts distinct catalog orders shipped to a given state over a 60-day window with cross-warehouse
fulfillment and no returns.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `COUNTY` | list (×5) | 5 random US counties — substituted as `{COUNTY.1}`…`{COUNTY.5}` |
| `MONTH` | integer | 2–5 |
| `STATE` | list | US state codes (44 values) |
| `YEAR` | integer | 1999–2002 |

<details>
<summary>TPC-DS Reference SQL (query16.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
   count(distinct cs_order_number) as "order count",
   sum(cs_ext_ship_cost) as "total shipping cost",
   sum(cs_net_profit) as "total net profit"
from catalog_sales cs1, date_dim, customer_address, call_center
where d_date between '[YEAR]-[MONTH]-01'
           and (cast('[YEAR]-[MONTH]-01' as date) + 60 days)
  and cs1.cs_ship_date_sk = d_date_sk
  and cs1.cs_ship_addr_sk = ca_address_sk
  and ca_state = '[STATE]'
  and cs1.cs_call_center_sk = cc_call_center_sk
  and cc_county in ('[COUNTY.1]','[COUNTY.2]','[COUNTY.3]','[COUNTY.4]','[COUNTY.5]')
  and exists (select * from catalog_sales cs2
              where cs1.cs_order_number = cs2.cs_order_number
                and cs1.cs_warehouse_sk <> cs2.cs_warehouse_sk)
  and not exists (select * from catalog_returns cr1
                  where cs1.cs_order_number = cr1.cr_order_number)
order by count(distinct cs_order_number)
[_LIMITC];
```

</details>

---

## Q17 — Item Return and Re-Purchase Analysis

Computes counts, averages, and coefficient of variation for quantities in store sales, store returns,
and subsequent catalog re-purchases, within the same three quarters.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |

<details>
<summary>TPC-DS Reference SQL (query17.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] i_item_id, i_item_desc, s_state,
       count(ss_quantity) as store_sales_quantitycount,
       avg(ss_quantity) as store_sales_quantityave,
       stddev_samp(ss_quantity) as store_sales_quantitystdev,
       stddev_samp(ss_quantity)/avg(ss_quantity) as store_sales_quantitycov,
       count(sr_return_quantity) as store_returns_quantitycount,
       avg(sr_return_quantity) as store_returns_quantityave,
       stddev_samp(sr_return_quantity) as store_returns_quantitystdev,
       stddev_samp(sr_return_quantity)/avg(sr_return_quantity) as store_returns_quantitycov,
       count(cs_quantity) as catalog_sales_quantitycount,
       avg(cs_quantity) as catalog_sales_quantityave,
       stddev_samp(cs_quantity) as catalog_sales_quantitystdev,
       stddev_samp(cs_quantity)/avg(cs_quantity) as catalog_sales_quantitycov
from store_sales, store_returns, catalog_sales,
     date_dim d1, date_dim d2, date_dim d3, store, item
where d1.d_quarter_name = '[YEAR]Q1'
  and d1.d_date_sk = ss_sold_date_sk
  and i_item_sk = ss_item_sk
  and s_store_sk = ss_store_sk
  and ss_customer_sk = sr_customer_sk
  and ss_item_sk = sr_item_sk
  and ss_ticket_number = sr_ticket_number
  and sr_returned_date_sk = d2.d_date_sk
  and d2.d_quarter_name in ('[YEAR]Q1','[YEAR]Q2','[YEAR]Q3')
  and sr_customer_sk = cs_bill_customer_sk
  and sr_item_sk = cs_item_sk
  and cs_sold_date_sk = d3.d_date_sk
  and d3.d_quarter_name in ('[YEAR]Q1','[YEAR]Q2','[YEAR]Q3')
group by i_item_id, i_item_desc, s_state
order by i_item_id, i_item_desc, s_state
[_LIMITC];
```

</details>

---

## Q18 — Catalog Sales Aggregates by Geography and Demographics (Rollup)

Averages catalog sales quantities, prices, and demographics by item, country, state, county
using `ROLLUP`.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `STATE` | list (×7) | 7 draws from US state codes (44 values) — substituted as `{STATE.1}`…`{STATE.7}` |
| `MONTH` | integer (×6) | 6 draws from 1–12 — substituted as `{MONTH.1}`…`{MONTH.6}` |
| `GEN` | list | M, F |
| `ES` | list | Primary, Secondary, College, 2 yr Degree, 4 yr Degree, Advanced Degree, Unknown |

<details>
<summary>TPC-DS Reference SQL (query18.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] i_item_id, ca_country, ca_state, ca_county,
       avg(cast(cs_quantity as decimal(12,2))) agg1,
       avg(cast(cs_list_price as decimal(12,2))) agg2,
       avg(cast(cs_coupon_amt as decimal(12,2))) agg3,
       avg(cast(cs_sales_price as decimal(12,2))) agg4,
       avg(cast(cs_net_profit as decimal(12,2))) agg5,
       avg(cast(c_birth_year as decimal(12,2))) agg6,
       avg(cast(cd1.cd_dep_count as decimal(12,2))) agg7
from catalog_sales, customer_demographics cd1, customer_demographics cd2,
     customer, customer_address, date_dim, item
where cs_sold_date_sk = d_date_sk
  and cs_item_sk = i_item_sk
  and cs_bill_cdemo_sk = cd1.cd_demo_sk
  and cs_bill_customer_sk = c_customer_sk
  and cd1.cd_gender = '[GEN]'
  and cd1.cd_education_status = '[ES]'
  and c_current_cdemo_sk = cd2.cd_demo_sk
  and c_current_addr_sk = ca_address_sk
  and c_birth_month in ([MONTH.1],[MONTH.2],[MONTH.3],[MONTH.4],[MONTH.5],[MONTH.6])
  and d_year = [YEAR]
  and ca_state in ('[STATE.1]','[STATE.2]','[STATE.3]',
                   '[STATE.4]','[STATE.5]','[STATE.6]','[STATE.7]')
group by rollup (i_item_id, ca_country, ca_state, ca_county)
order by ca_country, ca_state, ca_county, i_item_id
[_LIMITC];
```

</details>

<details>
<summary>MariaDB / MonetDB / PostgreSQL dialects</summary>

MariaDB uses `GROUP BY i_item_id, ca_country, ca_state, ca_county WITH ROLLUP`.
MonetDB and PostgreSQL use standard `GROUP BY ROLLUP(i_item_id, ca_country, ca_state, ca_county)`.

</details>

---

## Q19 — Store Sales by Brand and Manager

Reports total external sales price grouped by brand and manufacturer for a given store manager,
month, and year, filtering out customers who share ZIP code prefix with the store.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `MONTH` | integer | 11–12 |
| `MANAGER` | integer | 1–100 |

<details>
<summary>TPC-DS Reference SQL (query19.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] i_brand_id brand_id, i_brand brand, i_manufact_id, i_manufact,
       sum(ss_ext_sales_price) ext_price
from date_dim, store_sales, item, customer, customer_address, store
where d_date_sk = ss_sold_date_sk
  and ss_item_sk = i_item_sk
  and i_manager_id = [MANAGER]
  and d_moy = [MONTH]
  and d_year = [YEAR]
  and ss_customer_sk = c_customer_sk
  and c_current_addr_sk = ca_address_sk
  and substr(ca_zip,1,5) <> substr(s_zip,1,5)
  and ss_store_sk = s_store_sk
group by i_brand, i_brand_id, i_manufact_id, i_manufact
order by ext_price desc, i_brand, i_brand_id, i_manufact_id, i_manufact
[_LIMITC];
```

</details>

---

## Q20 — Catalog Sales Revenue Ratio by Item Class

Analogous to Q12 but for the catalog channel. Computes revenue contribution per item in selected
categories over a 30-day window.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `CATEGORY` | list (×3) | 3 draws from: Books, Children, Electronics, Home, Jewelry, Men, Music, Shoes, Sports, Women |

<details>
<summary>TPC-DS Reference SQL (query20.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] i_item_id, i_item_desc, i_category, i_class, i_current_price,
       sum(cs_ext_sales_price) as itemrevenue,
       sum(cs_ext_sales_price)*100/sum(sum(cs_ext_sales_price)) over
           (partition by i_class) as revenueratio
from catalog_sales, item, date_dim
where cs_item_sk = i_item_sk
  and i_category in ('[CATEGORY.1]', '[CATEGORY.2]', '[CATEGORY.3]')
  and cs_sold_date_sk = d_date_sk
  and d_date between cast('[SDATE]' as date) and (cast('[SDATE]' as date) + 30 days)
group by i_item_id, i_item_desc, i_category, i_class, i_current_price
order by i_category, i_class, i_item_id, i_item_desc, revenueratio
[_LIMITC];
```

</details>

> **Bexhoma note:** `[SDATE]` is replaced by a date derived from `{YEAR}` and `{MONTH}` parameters
> in the bexhoma SQL.

---

## Q21 — Inventory Levels Before and After a Sale Date

Checks whether inventory level ratios (before vs. after a key date) remain within 2/3 to 3/2,
for items priced between $0.99 and $1.49.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `MONTH` | integer | 1–12 |
| `DAY` | integer | 1–28 |
| `YEAR` | integer | 1998–2002 |

<details>
<summary>TPC-DS Reference SQL (query21.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] *
from (select w_warehouse_name, i_item_id,
             sum(case when (cast(d_date as date) < cast('[SALES_DATE]' as date))
                      then inv_quantity_on_hand else 0 end) as inv_before,
             sum(case when (cast(d_date as date) >= cast('[SALES_DATE]' as date))
                      then inv_quantity_on_hand else 0 end) as inv_after
      from inventory, warehouse, item, date_dim
      where i_current_price between 0.99 and 1.49
        and i_item_sk = inv_item_sk
        and inv_warehouse_sk = w_warehouse_sk
        and inv_date_sk = d_date_sk
        and d_date between (cast('[SALES_DATE]' as date) - 30 days)
                       and (cast('[SALES_DATE]' as date) + 30 days)
      group by w_warehouse_name, i_item_id) x
where (case when inv_before > 0 then inv_after / inv_before else null end)
      between 2.0/3.0 and 3.0/2.0
order by w_warehouse_name, i_item_id
[_LIMITC];
```

</details>

> **Bexhoma note:** `[SALES_DATE]` is replaced with a date constructed from `{YEAR}`, `{MONTH}`,
> `{DAY}` integer parameters.

---

## Q22 — Average Inventory by Product with Rollup

Averages inventory on hand per product (name, brand, class, category) over a 12-month period,
using `ROLLUP` to generate subtotals.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1224 (month sequence number) |

<details>
<summary>TPC-DS Reference SQL (query22.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] i_product_name, i_brand, i_class, i_category,
       avg(inv_quantity_on_hand) qoh
from inventory, date_dim, item
where inv_date_sk = d_date_sk
  and inv_item_sk = i_item_sk
  and d_month_seq between [DMS] and [DMS]+11
group by rollup(i_product_name, i_brand, i_class, i_category)
order by qoh, i_product_name, i_brand, i_class, i_category
[_LIMITC];
```

</details>

<details>
<summary>MariaDB / MonetDB / PostgreSQL dialects</summary>

MariaDB uses `GROUP BY i_product_name, i_brand, i_class, i_category WITH ROLLUP`.
MonetDB and PostgreSQL use standard `GROUP BY ROLLUP(...)`.

</details>

---

## Q23a+b — Frequent Store Buyers in Catalog and Web (Multi-Statement)

Two-statement query. Identifies "best store sales customers" (top 5% by spend) who also purchased
frequently-sold items via catalog or web in a given month.
**Part a** returns total sales; **Part b** returns customers with their names and totals.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2000 |
| `MONTH` | integer | 1–7 |
| `TOPPERCENT` | integer | 95–95 (fixed at 95th percentile) |

<details>
<summary>TPC-DS Reference SQL (query23.tpl — Part a)</summary>

```sql
with frequent_ss_items as (
  select substr(i_item_desc,1,30) itemdesc, i_item_sk item_sk, d_date solddate, count(*) cnt
  from store_sales, date_dim, item
  where ss_sold_date_sk = d_date_sk and ss_item_sk = i_item_sk
    and d_year in ([YEAR],[YEAR]+1,[YEAR]+2,[YEAR]+3)
  group by substr(i_item_desc,1,30), i_item_sk, d_date
  having count(*) > 4),
max_store_sales as (
  select max(csales) tpcds_cmax from (
    select c_customer_sk, sum(ss_quantity*ss_sales_price) csales
    from store_sales, customer, date_dim
    where ss_customer_sk = c_customer_sk and ss_sold_date_sk = d_date_sk
      and d_year in ([YEAR],[YEAR]+1,[YEAR]+2,[YEAR]+3)
    group by c_customer_sk)),
best_ss_customer as (
  select c_customer_sk, sum(ss_quantity*ss_sales_price) ssales
  from store_sales, customer
  where ss_customer_sk = c_customer_sk
  group by c_customer_sk
  having sum(ss_quantity*ss_sales_price) > ([TOPPERCENT]/100.0) *
         (select * from max_store_sales))
[_LIMITA] select [_LIMITB] sum(sales)
from (select cs_quantity*cs_list_price sales
      from catalog_sales, date_dim
      where d_year = [YEAR] and d_moy = [MONTH] and cs_sold_date_sk = d_date_sk
        and cs_item_sk in (select item_sk from frequent_ss_items)
        and cs_bill_customer_sk in (select c_customer_sk from best_ss_customer)
      union all
      select ws_quantity*ws_list_price sales
      from web_sales, date_dim
      where d_year = [YEAR] and d_moy = [MONTH] and ws_sold_date_sk = d_date_sk
        and ws_item_sk in (select item_sk from frequent_ss_items)
        and ws_bill_customer_sk in (select c_customer_sk from best_ss_customer))
[_LIMITC];
```

</details>

<details>
<summary>TPC-DS Reference SQL (query23.tpl — Part b)</summary>

```sql
... same CTEs ...
[_LIMITA] select [_LIMITB] c_last_name, c_first_name, sales
from (select c_last_name, c_first_name, sum(cs_quantity*cs_list_price) sales
      from catalog_sales, customer, date_dim
      where d_year = [YEAR] and d_moy = [MONTH] and cs_sold_date_sk = d_date_sk
        and cs_item_sk in (select item_sk from frequent_ss_items)
        and cs_bill_customer_sk in (select c_customer_sk from best_ss_customer)
        and cs_bill_customer_sk = c_customer_sk
      group by c_last_name, c_first_name
      union all
      select c_last_name, c_first_name, sum(ws_quantity*ws_list_price) sales
      from web_sales, customer, date_dim
      where d_year = [YEAR] and d_moy = [MONTH] and ws_sold_date_sk = d_date_sk
        and ws_item_sk in (select item_sk from frequent_ss_items)
        and ws_bill_customer_sk in (select c_customer_sk from best_ss_customer)
        and ws_bill_customer_sk = c_customer_sk
      group by c_last_name, c_first_name)
order by c_last_name, c_first_name, sales
[_LIMITC];
```

</details>

---

## Q24a+b — Store Sales Paid Amount by Color (Multi-Statement)

Two-statement query. Each part finds customers who paid more than 5% of average net paid per store
for items in a specific color (Part a uses `{COLOR.1}`, Part b uses `{COLOR.2}`), within a given
market.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `MARKET` | integer | 5–10 |
| `COLOR` | list (×2) | 2 draws from 67 color names — substituted as `{COLOR.1}`, `{COLOR.2}` |
| `AMOUNTONE` | list | `ss_net_paid`, `ss_net_paid_inc_tax`, `ss_net_profit`, `ss_sales_price`, `ss_ext_sales_price` |

<details>
<summary>TPC-DS Reference SQL (query24.tpl — Part a)</summary>

```sql
with ssales as (
  select c_last_name, c_first_name, s_store_name, ca_state, s_state,
         i_color, i_current_price, i_manager_id, i_units, i_size,
         sum([AMOUNTONE]) netpaid
  from store_sales, store_returns, store, item, customer, customer_address
  where ss_ticket_number = sr_ticket_number and ss_item_sk = sr_item_sk
    and ss_customer_sk = c_customer_sk and ss_item_sk = i_item_sk
    and ss_store_sk = s_store_sk and c_current_addr_sk = ca_address_sk
    and c_birth_country <> upper(ca_country)
    and s_zip = ca_zip and s_market_id = [MARKET]
  group by c_last_name, c_first_name, s_store_name, ca_state, s_state,
           i_color, i_current_price, i_manager_id, i_units, i_size)
select c_last_name, c_first_name, s_store_name, sum(netpaid) paid
from ssales
where i_color = '[COLOR.1]'
group by c_last_name, c_first_name, s_store_name
having sum(netpaid) > (select 0.05*avg(netpaid) from ssales)
order by c_last_name, c_first_name, s_store_name;
```

</details>

<details>
<summary>TPC-DS Reference SQL (query24.tpl — Part b)</summary>

Same structure as Part a but filtering on `i_color = '[COLOR.2]'`.

</details>

---

## Q25 — Store-Return-Catalog Profit Analysis

Reports net profit aggregation (with selectable aggregate function) for items that appear in store
sales, get returned, and are re-purchased in the catalog, all in the same year and adjacent months.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `AGG` | list | `sum`, `min`, `max`, `avg`, `stddev_samp` |

<details>
<summary>TPC-DS Reference SQL (query25.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  i_item_id, i_item_desc, s_store_id, s_store_name,
  [AGG](ss_net_profit) as store_sales_profit,
  [AGG](sr_net_loss) as store_returns_loss,
  [AGG](cs_net_profit) as catalog_sales_profit
from store_sales, store_returns, catalog_sales,
     date_dim d1, date_dim d2, date_dim d3, store, item
where d1.d_moy = 4 and d1.d_year = [YEAR]
  and d1.d_date_sk = ss_sold_date_sk
  and i_item_sk = ss_item_sk
  and s_store_sk = ss_store_sk
  and ss_customer_sk = sr_customer_sk
  and ss_item_sk = sr_item_sk
  and ss_ticket_number = sr_ticket_number
  and sr_returned_date_sk = d2.d_date_sk
  and d2.d_moy between 4 and 10 and d2.d_year = [YEAR]
  and sr_customer_sk = cs_bill_customer_sk
  and sr_item_sk = cs_item_sk
  and cs_sold_date_sk = d3.d_date_sk
  and d3.d_moy between 4 and 10 and d3.d_year = [YEAR]
group by i_item_id, i_item_desc, s_store_id, s_store_name
order by i_item_id, i_item_desc, s_store_id, s_store_name
[_LIMITC];
```

</details>

---

## Q26 — Catalog Sales Averages by Item and Demographics

Reports average quantities, list prices, coupon amounts, and sales prices for catalog sales
filtered by gender, marital status, education, year, and promotional channels.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `GEN` | list | M, F |
| `MS` | list | S, M, D, W, U |
| `ES` | list | Primary, Secondary, College, 2 yr Degree, 4 yr Degree, Advanced Degree, Unknown |
| `YEAR` | integer | 1998–2002 |

<details>
<summary>TPC-DS Reference SQL (query26.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] i_item_id,
       avg(cs_quantity) agg1, avg(cs_list_price) agg2,
       avg(cs_coupon_amt) agg3, avg(cs_sales_price) agg4
from catalog_sales, customer_demographics, date_dim, item, promotion
where cs_sold_date_sk = d_date_sk
  and cs_item_sk = i_item_sk
  and cs_bill_cdemo_sk = cd_demo_sk
  and cs_promo_sk = p_promo_sk
  and cd_gender = '[GEN]'
  and cd_marital_status = '[MS]'
  and cd_education_status = '[ES]'
  and (p_channel_email = 'N' or p_channel_event = 'N')
  and d_year = [YEAR]
group by i_item_id
order by i_item_id
[_LIMITC];
```

</details>

---

## Q27 — Store Sales Aggregates by State and Demographics (Rollup)

Similar to Q26 but for store sales, with `ROLLUP` over item and state to produce subtotals.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `GEN` | list | M, F |
| `MS` | list | S, M, D, W, U |
| `ES` | list | education distribution values |
| `STATE` | list (×6) | 6 draws from state codes — substituted as `{STATE.1}`…`{STATE.6}` |

<details>
<summary>TPC-DS Reference SQL (query27.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] i_item_id, s_state, grouping(s_state) g_state,
       avg(ss_quantity) agg1, avg(ss_list_price) agg2,
       avg(ss_coupon_amt) agg3, avg(ss_sales_price) agg4
from store_sales, customer_demographics, date_dim, store, item
where ss_sold_date_sk = d_date_sk
  and ss_item_sk = i_item_sk
  and ss_store_sk = s_store_sk
  and ss_cdemo_sk = cd_demo_sk
  and cd_gender = '[GEN]'
  and cd_marital_status = '[MS]'
  and cd_education_status = '[ES]'
  and d_year = [YEAR]
  and s_state in ('[STATE_A]','[STATE_B]','[STATE_C]','[STATE_D]','[STATE_E]','[STATE_F]')
group by rollup (i_item_id, s_state)
order by i_item_id, s_state
[_LIMITC];
```

</details>

<details>
<summary>MariaDB / MonetDB / PostgreSQL dialects</summary>

MariaDB uses `GROUP BY i_item_id, s_state WITH ROLLUP`.
MonetDB and PostgreSQL use standard `GROUP BY ROLLUP(i_item_id, s_state)`.

</details>

---

## Q28 — Multi-Band List Price and Discount Crosstab

Cross-tabulates list price averages, counts, and distinct counts across six quantity bands
(0–5, 6–10, 11–15, 16–20, 21–25, 26–30) simultaneously.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `LISTPRICE` | integer (×6) | 6 independent draws from 0–190 |
| `COUPONAMT` | integer (×6) | 6 independent draws from 0–18000 |
| `WHOLESALECOST` | integer (×6) | 6 independent draws from 0–80 |

<details>
<summary>TPC-DS Reference SQL (query28.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] *
from (select avg(ss_list_price) B1_LP, count(ss_list_price) B1_CNT,
             count(distinct ss_list_price) B1_CNTD
      from store_sales
      where ss_quantity between 0 and 5
        and (ss_list_price between [LISTPRICE.1] and [LISTPRICE.1]+10
             or ss_coupon_amt between [COUPONAMT.1] and [COUPONAMT.1]+1000
             or ss_wholesale_cost between [WHOLESALECOST.1] and [WHOLESALECOST.1]+20)) B1,
     (select avg(ss_list_price) B2_LP, count(ss_list_price) B2_CNT,
             count(distinct ss_list_price) B2_CNTD
      from store_sales
      where ss_quantity between 6 and 10
        and (ss_list_price between [LISTPRICE.2] and [LISTPRICE.2]+10
             or ss_coupon_amt between [COUPONAMT.2] and [COUPONAMT.2]+1000
             or ss_wholesale_cost between [WHOLESALECOST.2] and [WHOLESALECOST.2]+20)) B2,
     ... (bands B3-B6 analogous)
[_LIMITC];
```

</details>

---

## Q29 — Store-Return-Catalog Quantity Analysis

Similar to Q25 but computes aggregate quantities rather than profit, with a shorter
return-window (month + 3) and a wider re-purchase window (3 years).

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2000 |
| `MONTH` | integer | 4 (fixed) |
| `AGG` | list | sum, min, max, avg, stddev_samp |

<details>
<summary>TPC-DS Reference SQL (query29.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
    i_item_id, i_item_desc, s_store_id, s_store_name,
    [AGG](ss_quantity) as store_sales_quantity,
    [AGG](sr_return_quantity) as store_returns_quantity,
    [AGG](cs_quantity) as catalog_sales_quantity
from store_sales, store_returns, catalog_sales,
     date_dim d1, date_dim d2, date_dim d3, store, item
where d1.d_moy = [MONTH] and d1.d_year = [YEAR]
  and d1.d_date_sk = ss_sold_date_sk
  and i_item_sk = ss_item_sk
  and s_store_sk = ss_store_sk
  and ss_customer_sk = sr_customer_sk
  and ss_item_sk = sr_item_sk
  and ss_ticket_number = sr_ticket_number
  and sr_returned_date_sk = d2.d_date_sk
  and d2.d_moy between [MONTH] and [MONTH] + 3
  and d2.d_year = [YEAR]
  and sr_customer_sk = cs_bill_customer_sk
  and sr_item_sk = cs_item_sk
  and cs_sold_date_sk = d3.d_date_sk
  and d3.d_year in ([YEAR],[YEAR]+1,[YEAR]+2)
group by i_item_id, i_item_desc, s_store_id, s_store_name
order by i_item_id, i_item_desc, s_store_id, s_store_name
[_LIMITC];
```

</details>

---

## Q30 — Web Returns by State vs. Average

Finds customers whose total web return amount is 20% above the average for their state,
in a given year.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `STATE` | list | US state codes (44 values) |
| `YEAR` | integer | 1999–2002 |

<details>
<summary>TPC-DS Reference SQL (query30.tpl)</summary>

```sql
with customer_total_return as (
  select wr_returning_customer_sk as ctr_customer_sk,
         ca_state as ctr_state,
         sum(wr_return_amt) as ctr_total_return
  from web_returns, date_dim, customer_address
  where wr_returned_date_sk = d_date_sk
    and d_year = [YEAR]
    and wr_returning_addr_sk = ca_address_sk
  group by wr_returning_customer_sk, ca_state)
[_LIMITA] select [_LIMITB]
  c_customer_id, c_salutation, c_first_name, c_last_name, c_preferred_cust_flag,
  c_birth_day, c_birth_month, c_birth_year, c_birth_country, c_login, c_email_address,
  c_last_review_date_sk, ctr_total_return
from customer_total_return ctr1, customer_address, customer
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
                                from customer_total_return ctr2
                               where ctr1.ctr_state = ctr2.ctr_state)
  and ca_address_sk = c_current_addr_sk
  and ca_state = '[STATE]'
  and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id, c_salutation, c_first_name, c_last_name, c_preferred_cust_flag,
         c_birth_day, c_birth_month, c_birth_year, c_birth_country, c_login, c_email_address,
         c_last_review_date_sk, ctr_total_return
[_LIMITC];
```

</details>

---

## Q31 — Quarter-over-Quarter Sales Growth by County

Compares web vs. store sales growth between consecutive quarters for counties where the
web/store growth ratios are consistently positive.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `AGG` | list | one of 6 column expressions used in ORDER BY |

<details>
<summary>TPC-DS Reference SQL (query31.tpl)</summary>

```sql
with ss as (
  select ca_county, d_qoy, d_year, sum(ss_ext_sales_price) as store_sales
  from store_sales, date_dim, customer_address
  where ss_sold_date_sk = d_date_sk and ss_addr_sk = ca_address_sk
  group by ca_county, d_qoy, d_year),
ws as (
  select ca_county, d_qoy, d_year, sum(ws_ext_sales_price) as web_sales
  from web_sales, date_dim, customer_address
  where ws_sold_date_sk = d_date_sk and ws_bill_addr_sk = ca_address_sk
  group by ca_county, d_qoy, d_year)
select ss1.ca_county, ss1.d_year,
       ws2.web_sales/ws1.web_sales web_q1_q2_increase,
       ss2.store_sales/ss1.store_sales store_q1_q2_increase,
       ws3.web_sales/ws2.web_sales web_q2_q3_increase,
       ss3.store_sales/ss2.store_sales store_q2_q3_increase
from ss ss1, ss ss2, ss ss3, ws ws1, ws ws2, ws ws3
where ss1.d_qoy = 1 and ss1.d_year = [YEAR]
  and ss1.ca_county = ss2.ca_county and ss2.d_qoy = 2 and ss2.d_year = [YEAR]
  and ss2.ca_county = ss3.ca_county and ss3.d_qoy = 3 and ss3.d_year = [YEAR]
  and ss1.ca_county = ws1.ca_county and ws1.d_qoy = 1 and ws1.d_year = [YEAR]
  and ws1.ca_county = ws2.ca_county and ws2.d_qoy = 2 and ws2.d_year = [YEAR]
  and ws1.ca_county = ws3.ca_county and ws3.d_qoy = 3 and ws3.d_year = [YEAR]
  and case when ws1.web_sales > 0 then ws2.web_sales/ws1.web_sales else null end
       > case when ss1.store_sales > 0 then ss2.store_sales/ss1.store_sales else null end
  and case when ws2.web_sales > 0 then ws3.web_sales/ws2.web_sales else null end
       > case when ss2.store_sales > 0 then ss3.store_sales/ss2.store_sales else null end
order by [AGG];
```

</details>

---

## Q32 — Catalog Discount Excess Over Average

Finds total excess discount amounts in catalog sales where items from a given manufacturer
have discount amounts above 1.3× their 90-day average, during a date window.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `IMID` | integer | 1–1000 |
| `YEAR` | integer | 1998–2002 |
| `CSDATE` | date | derived: Jan 1 – Apr 1 of `{YEAR}` |

<details>
<summary>TPC-DS Reference SQL (query32.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] sum(cs_ext_discount_amt) as "excess discount amount"
from catalog_sales, item, date_dim
where i_manufact_id = [IMID]
  and i_item_sk = cs_item_sk
  and d_date between '[CSDATE]' and (cast('[CSDATE]' as date) + 90 days)
  and d_date_sk = cs_sold_date_sk
  and cs_ext_discount_amt > (
        select 1.3 * avg(cs_ext_discount_amt)
        from catalog_sales, date_dim
        where cs_item_sk = i_item_sk
          and d_date between '[CSDATE]' and (cast('[CSDATE]' as date) + 90 days)
          and d_date_sk = cs_sold_date_sk)
[_LIMITC];
```

</details>

> **Bexhoma note:** `[CSDATE]` is constructed from `{YEAR}`, `{MONTH}`, `{DAY}` integer parameters
> in the bexhoma SQL.

---

## Q33 — Cross-Channel Sales by Manufacturer in a Region

Sums external sales price across all three channels (store, catalog, web) for manufacturers
whose items belong to a specified category, in a given GMT timezone, year, and month.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `MONTH` | integer | 1–7 |
| `COUNTY` | integer | 1–N (active store counties) |
| `GMT` | list | GMT offset derived from county |
| `CATEGORY` | list | Books, Home, Electronics, Jewelry, Sports |

<details>
<summary>TPC-DS Reference SQL (query33.tpl)</summary>

```sql
with ss as (
  select i_manufact_id, sum(ss_ext_sales_price) total_sales
  from store_sales, date_dim, customer_address, item
  where i_manufact_id in (select i_manufact_id from item where i_category in ('[CATEGORY]'))
    and ss_item_sk = i_item_sk and ss_sold_date_sk = d_date_sk
    and d_year = [YEAR] and d_moy = [MONTH]
    and ss_addr_sk = ca_address_sk and ca_gmt_offset = [GMT]
  group by i_manufact_id),
cs as (... same for catalog_sales ...),
ws as (... same for web_sales ...)
[_LIMITA] select [_LIMITB] i_manufact_id, sum(total_sales) total_sales
from (select * from ss union all select * from cs union all select * from ws) tmp1
group by i_manufact_id
order by total_sales
[_LIMITC];
```

</details>

---

## Q34 — Store Customer Ticket Frequency in High-Purchase-Potential Households

Finds customers with 15–20 store purchases in high-purchase-potential households across
specific counties and years.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `BPONE` | list | `1001-5000`, `>10000`, `501-1000` |
| `BPTWO` | list | `0-500`, `Unknown`, `5001-10000` |
| `YEAR` | integer | 1998–2000 |
| `COUNTY` | list (×8) | 8 draws from active store counties — substituted as `{COUNTY.1}`…`{COUNTY.8}` |

<details>
<summary>TPC-DS Reference SQL (query34.tpl)</summary>

```sql
select c_last_name, c_first_name, c_salutation, c_preferred_cust_flag,
       ss_ticket_number, cnt
from (select ss_ticket_number, ss_customer_sk, count(*) cnt
      from store_sales, date_dim, store, household_demographics
      where store_sales.ss_sold_date_sk = date_dim.d_date_sk
        and store_sales.ss_store_sk = store.s_store_sk
        and store_sales.ss_hdemo_sk = household_demographics.hd_demo_sk
        and (date_dim.d_dom between 1 and 3 or date_dim.d_dom between 25 and 28)
        and (household_demographics.hd_buy_potential = '[BPONE]'
             or household_demographics.hd_buy_potential = '[BPTWO]')
        and household_demographics.hd_vehicle_count > 0
        and (case when household_demographics.hd_vehicle_count > 0
             then household_demographics.hd_dep_count / household_demographics.hd_vehicle_count
             else null end) > 1.2
        and date_dim.d_year in ([YEAR],[YEAR]+1,[YEAR]+2)
        and store.s_county in ('[COUNTY.1]','[COUNTY.2]','[COUNTY.3]','[COUNTY.4]',
                               '[COUNTY.5]','[COUNTY.6]','[COUNTY.7]','[COUNTY.8]')
      group by ss_ticket_number, ss_customer_sk) dn, customer
where ss_customer_sk = c_customer_sk and cnt between 15 and 20
order by c_last_name, c_first_name, c_salutation, c_preferred_cust_flag desc, ss_ticket_number;
```

</details>

---

## Q35 — Customer Demographics with Aggregate Dependency Counts

Reports demographic aggregates for customers who purchased in store (and also via web or
catalog) within a given year, using three independent aggregate functions.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1999–2002 |
| `AGGONE` | list | sum, min, max, avg, stddev_samp |
| `AGGTWO` | list | sum, min, max, avg, stddev_samp |
| `AGGTHREE` | list | sum, min, max, avg, stddev_samp |

<details>
<summary>TPC-DS Reference SQL (query35.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  ca_state, cd_gender, cd_marital_status, cd_dep_count, count(*) cnt1,
  [AGGONE](cd_dep_count) aggone1, [AGGTWO](cd_dep_count) aggtwo1, [AGGTHREE](cd_dep_count) aggthree1,
  cd_dep_employed_count, count(*) cnt2,
  [AGGONE](cd_dep_employed_count) aggone2, [AGGTWO](cd_dep_employed_count) aggtwo2, [AGGTHREE](cd_dep_employed_count) aggthree2,
  cd_dep_college_count, count(*) cnt3,
  [AGGONE](cd_dep_college_count) aggone3, [AGGTWO](cd_dep_college_count) aggtwo3, [AGGTHREE](cd_dep_college_count) aggthree3
from customer c, customer_address ca, customer_demographics
where c.c_current_addr_sk = ca.ca_address_sk
  and cd_demo_sk = c.c_current_cdemo_sk
  and exists (select * from store_sales, date_dim
              where c.c_customer_sk = ss_customer_sk
                and ss_sold_date_sk = d_date_sk and d_year = [YEAR] and d_qoy < 4)
  and (exists (select * from web_sales, date_dim
               where c.c_customer_sk = ws_bill_customer_sk
                 and ws_sold_date_sk = d_date_sk and d_year = [YEAR] and d_qoy < 4)
       or exists (select * from catalog_sales, date_dim
                  where c.c_customer_sk = cs_ship_customer_sk
                    and cs_sold_date_sk = d_date_sk and d_year = [YEAR] and d_qoy < 4))
group by ca_state, cd_gender, cd_marital_status, cd_dep_count, cd_dep_employed_count, cd_dep_college_count
order by ca_state, cd_gender, cd_marital_status, cd_dep_count, cd_dep_employed_count, cd_dep_college_count
[_LIMITC];
```

</details>

---

## Q36 — Store Gross Margin by Category with Rollup

Computes gross margin ratio (net profit / ext sales price) grouped by item category and class
using `ROLLUP`, then ranks within each hierarchical level.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `STATE` | list (×8) | 8 draws from active store states — substituted as `{STATE.1}`…`{STATE.8}` |

<details>
<summary>TPC-DS Reference SQL (query36.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
    sum(ss_net_profit)/sum(ss_ext_sales_price) as gross_margin,
    i_category, i_class,
    grouping(i_category)+grouping(i_class) as lochierarchy,
    rank() over (
        partition by grouping(i_category)+grouping(i_class),
                     case when grouping(i_class) = 0 then i_category end
        order by sum(ss_net_profit)/sum(ss_ext_sales_price) asc) as rank_within_parent
from store_sales, date_dim d1, item, store
where d1.d_year = [YEAR]
  and d1.d_date_sk = ss_sold_date_sk
  and i_item_sk = ss_item_sk
  and s_store_sk = ss_store_sk
  and s_state in ('[STATE_A]','[STATE_B]','[STATE_C]','[STATE_D]',
                  '[STATE_E]','[STATE_F]','[STATE_G]','[STATE_H]')
group by rollup(i_category, i_class)
order by lochierarchy desc, case when lochierarchy = 0 then i_category end, rank_within_parent
[_LIMITC];
```

</details>

<details>
<summary>MariaDB / MonetDB / PostgreSQL dialects</summary>

MariaDB uses `GROUP BY i_category, i_class WITH ROLLUP`.
MonetDB and PostgreSQL use standard `GROUP BY ROLLUP(i_category, i_class)`.

</details>

---

## Q37 — Catalog Items in Stock with Matching Sales

Finds items with current price in a range, manufactured by a set of 4 manufacturers,
having between 100 and 500 units on hand in inventory, and actually sold via catalog.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `INVDATE` | date | derived from `{YEAR}` (Jan 1 – Jul 24) |
| `MANUFACT_ID` | integer (×4) | 4 draws from 667–1000 |
| `PRICE` | integer | 10–70 |

<details>
<summary>TPC-DS Reference SQL (query37.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] i_item_id, i_item_desc, i_current_price
from item, inventory, date_dim, catalog_sales
where i_current_price between [PRICE] and [PRICE] + 30
  and inv_item_sk = i_item_sk
  and d_date_sk = inv_date_sk
  and d_date between cast('[INVDATE]' as date) and (cast('[INVDATE]' as date) + 60 days)
  and i_manufact_id in ([MANUFACT_ID.1],[MANUFACT_ID.2],[MANUFACT_ID.3],[MANUFACT_ID.4])
  and inv_quantity_on_hand between 100 and 500
  and cs_item_sk = i_item_sk
group by i_item_id, i_item_desc, i_current_price
order by i_item_id
[_LIMITC];
```

</details>

---

## Q38 — Customers Who Bought in All Three Channels

Counts distinct customers (by name and date) who appear in all three channels (store, catalog, web)
within the same 12-month sequence.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1224 |

<details>
<summary>TPC-DS Reference SQL (query38.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] count(*) from (
    select distinct c_last_name, c_first_name, d_date
    from store_sales, date_dim, customer
    where store_sales.ss_sold_date_sk = date_dim.d_date_sk
      and store_sales.ss_customer_sk = customer.c_customer_sk
      and d_month_seq between [DMS] and [DMS] + 11
  intersect
    select distinct c_last_name, c_first_name, d_date
    from catalog_sales, date_dim, customer
    where catalog_sales.cs_sold_date_sk = date_dim.d_date_sk
      and catalog_sales.cs_bill_customer_sk = customer.c_customer_sk
      and d_month_seq between [DMS] and [DMS] + 11
  intersect
    select distinct c_last_name, c_first_name, d_date
    from web_sales, date_dim, customer
    where web_sales.ws_sold_date_sk = date_dim.d_date_sk
      and web_sales.ws_bill_customer_sk = customer.c_customer_sk
      and d_month_seq between [DMS] and [DMS] + 11
) hot_cust
[_LIMITC];
```

</details>

---

## Q39a+b — Inventory Coefficient of Variation (Multi-Statement)

Two-statement query. Computes coefficient of variation (stddev/mean) of inventory by warehouse
and item per month, then joins adjacent months.
**Part a** returns all pairs where CoV > 1; **Part b** additionally requires CoV > 1.5.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `MONTH` | integer | 1–4 |
| `YEAR` | integer | 1998–2002 |

<details>
<summary>TPC-DS Reference SQL (query39.tpl — Part a)</summary>

```sql
with inv as (
  select w_warehouse_name, w_warehouse_sk, i_item_sk, d_moy,
         stdev, mean, case mean when 0 then null else stdev/mean end cov
  from (select w_warehouse_name, w_warehouse_sk, i_item_sk, d_moy,
               stddev_samp(inv_quantity_on_hand) stdev,
               avg(inv_quantity_on_hand) mean
        from inventory, item, warehouse, date_dim
        where inv_item_sk = i_item_sk and inv_warehouse_sk = w_warehouse_sk
          and inv_date_sk = d_date_sk and d_year = [YEAR]
        group by w_warehouse_name, w_warehouse_sk, i_item_sk, d_moy) foo
  where case mean when 0 then 0 else stdev/mean end > 1)
select inv1.w_warehouse_sk, inv1.i_item_sk, inv1.d_moy,
       inv1.mean, inv1.cov, inv2.w_warehouse_sk, inv2.i_item_sk,
       inv2.d_moy, inv2.mean, inv2.cov
from inv inv1, inv inv2
where inv1.i_item_sk = inv2.i_item_sk and inv1.w_warehouse_sk = inv2.w_warehouse_sk
  and inv1.d_moy = [MONTH] and inv2.d_moy = [MONTH]+1
order by inv1.w_warehouse_sk, inv1.i_item_sk, inv1.d_moy, inv1.mean, inv1.cov,
         inv2.d_moy, inv2.mean, inv2.cov;
```

</details>

<details>
<summary>TPC-DS Reference SQL (query39.tpl — Part b)</summary>

Same CTE structure as Part a, but the main query adds `and inv1.cov > 1.5`.

</details>

---

## Q40 — Catalog Sales Before and After a Key Date

Computes item-level net sales (price minus any refund) split by before/after a key date,
for items priced between $0.99 and $1.49 over a ±30-day window.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `SALES_DATE` | date | derived: Jan 31 – Jul 1 of `{YEAR}` |

<details>
<summary>TPC-DS Reference SQL (query40.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
   w_state, i_item_id,
   sum(case when (cast(d_date as date) < cast('[SALES_DATE]' as date))
            then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end) as sales_before,
   sum(case when (cast(d_date as date) >= cast('[SALES_DATE]' as date))
            then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end) as sales_after
from catalog_sales left outer join catalog_returns
         on (cs_order_number = cr_order_number and cs_item_sk = cr_item_sk),
     warehouse, item, date_dim
where i_current_price between 0.99 and 1.49
  and i_item_sk = cs_item_sk
  and cs_warehouse_sk = w_warehouse_sk
  and cs_sold_date_sk = d_date_sk
  and d_date between (cast('[SALES_DATE]' as date) - 30 days)
                 and (cast('[SALES_DATE]' as date) + 30 days)
group by w_state, i_item_id
order by w_state, i_item_id
[_LIMITC];
```

</details>

---

## Q41 — Items with Many Attribute Combinations

Finds distinct product names for items with a manufacturer ID in a 40-unit range,
where more than 0 items match a complex set of color/unit/size combinations across
Women's and Men's categories.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `MANUFACT` | integer | 667–1000 |
| `COLOR` | list (×16) | 16 draws from 67 color names |
| `UNIT` | list (×16) | 16 draws from unit types |
| `SIZE` | list (×6) | 6 draws from size values |

<details>
<summary>TPC-DS Reference SQL (query41.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] distinct(i_product_name)
from item i1
where i_manufact_id between [MANUFACT] and [MANUFACT]+40
  and (select count(*) as item_cnt
       from item
       where (i_manufact = i1.i_manufact and
         ((i_category = 'Women' and (i_color = '[COLOR.1]' or i_color = '[COLOR.2]') and
           (i_units = '[UNIT.1]' or i_units = '[UNIT.2]') and
           (i_size = '[SIZE.1]' or i_size = '[SIZE.2]')) or
          (i_category = 'Women' and ... ) or
          (i_category = 'Men' and ...) or
          (i_category = 'Men' and ...))) or
         (i_manufact = i1.i_manufact and
         ((i_category = 'Women' and ... ) or ... ))) > 0
order by i_product_name
[_LIMITC];
```

</details>

---

## Q42 — Store Sales by Category and Manager

Summarizes total extended sales price per year, category, and category ID for store manager
ID = 1, in a given month and year.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `MONTH` | integer | 11–12 |
| `YEAR` | integer | 1998–2002 |

<details>
<summary>TPC-DS Reference SQL (query42.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] dt.d_year, item.i_category_id, item.i_category,
       sum(ss_ext_sales_price)
from date_dim dt, store_sales, item
where dt.d_date_sk = store_sales.ss_sold_date_sk
  and store_sales.ss_item_sk = item.i_item_sk
  and item.i_manager_id = 1
  and dt.d_moy = [MONTH]
  and dt.d_year = [YEAR]
group by dt.d_year, item.i_category_id, item.i_category
order by sum(ss_ext_sales_price) desc, dt.d_year,
         item.i_category_id, item.i_category
[_LIMITC];
```

</details>

---

## Q43 — Store Sales by Day-of-Week per Store

Pivots store sales by day of the week (Sun–Sat), for stores in a given GMT offset and year.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `COUNTY` | integer | random active county |
| `GMT` | list | GMT offset derived from county |
| `YEAR` | integer | 1998–2002 |

<details>
<summary>TPC-DS Reference SQL (query43.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] s_store_name, s_store_id,
       sum(case when d_day_name='Sunday'    then ss_sales_price else null end) sun_sales,
       sum(case when d_day_name='Monday'    then ss_sales_price else null end) mon_sales,
       sum(case when d_day_name='Tuesday'   then ss_sales_price else null end) tue_sales,
       sum(case when d_day_name='Wednesday' then ss_sales_price else null end) wed_sales,
       sum(case when d_day_name='Thursday'  then ss_sales_price else null end) thu_sales,
       sum(case when d_day_name='Friday'    then ss_sales_price else null end) fri_sales,
       sum(case when d_day_name='Saturday'  then ss_sales_price else null end) sat_sales
from date_dim, store_sales, store
where d_date_sk = ss_sold_date_sk
  and s_store_sk = ss_store_sk
  and s_gmt_offset = [GMT]
  and d_year = [YEAR]
group by s_store_name, s_store_id
order by s_store_name, s_store_id, sun_sales, mon_sales, tue_sales, wed_sales,
         thu_sales, fri_sales, sat_sales
[_LIMITC];
```

</details>

---

## Q44 — Best and Worst Performing Items in a Store

Ranks items in a given store by net profit and joins the top-10 ascending with top-10 descending
to find the best-performing vs. worst-performing item pairs.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `STORE` | integer | random store ID |
| `NULLCOLSS` | list | `ss_customer_sk`, `ss_cdemo_sk`, `ss_hdemo_sk`, `ss_addr_sk`, `ss_promo_sk` |

<details>
<summary>TPC-DS Reference SQL (query44.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] asceding.rnk, i1.i_product_name best_performing, i2.i_product_name worst_performing
from (select *
      from (select item_sk, rank() over (order by rank_col asc) rnk
            from (select ss_item_sk item_sk, avg(ss_net_profit) rank_col
                  from store_sales ss1
                  where ss_store_sk = [STORE]
                  group by ss_item_sk
                  having avg(ss_net_profit) > 0.9*(select avg(ss_net_profit) rank_col
                                                   from store_sales
                                                   where ss_store_sk = [STORE]
                                                     and [NULLCOLSS] is null
                                                   group by ss_store_sk)) V1) V11
      where rnk < 11) asceding,
     (select *
      from (select item_sk, rank() over (order by rank_col desc) rnk
            from (...same avg logic...) V2) V21
      where rnk < 11) descending,
     item i1, item i2
where asceding.rnk = descending.rnk
  and i1.i_item_sk = asceding.item_sk
  and i2.i_item_sk = descending.item_sk
order by asceding.rnk
[_LIMITC];
```

</details>

---

## Q45 — Web Sales by ZIP and Geography

Sums web sales for customers in specific ZIP codes or for items with specific item IDs,
grouped by customer ZIP and a geographic breakdown column.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `GBOBC` | list | `ca_city`, `ca_county`, `ca_state` |
| `YEAR` | integer | 1998–2002 |
| `QOY` | integer | 1–2 |

<details>
<summary>TPC-DS Reference SQL (query45.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] ca_zip, [GBOBC], sum(ws_sales_price)
from web_sales, customer, customer_address, date_dim, item
where ws_bill_customer_sk = c_customer_sk
  and c_current_addr_sk = ca_address_sk
  and ws_item_sk = i_item_sk
  and (substr(ca_zip,1,5) in ('85669','86197','88274','83405','86475',
                               '85392','85460','80348','81792')
       or i_item_id in (select i_item_id from item
                        where i_item_sk in (2,3,5,7,11,13,17,19,23,29)))
  and ws_sold_date_sk = d_date_sk
  and d_qoy = [QOY] and d_year = [YEAR]
group by ca_zip, [GBOBC]
order by ca_zip, [GBOBC]
[_LIMITC];
```

</details>

---

## Q46 — Customer Coupon and Profit by City (Weekend Purchases)

Finds customers whose current city differs from the city where they bought, for weekend purchases
in high-vehicle-count or specific dependent-count households.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DEPCNT` | integer | 0–9 |
| `YEAR` | integer | 1998–2000 |
| `VEHCNT` | integer | -1–4 |
| `CITY` | list (×5) | 5 draws from active store cities — substituted as `{CITY.1}`…`{CITY.5}` |

<details>
<summary>TPC-DS Reference SQL (query46.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  c_last_name, c_first_name, ca_city, bought_city,
  ss_ticket_number, amt, profit
from (select ss_ticket_number, ss_customer_sk, ca_city bought_city,
             sum(ss_coupon_amt) amt, sum(ss_net_profit) profit
      from store_sales, date_dim, store, household_demographics, customer_address
      where store_sales.ss_sold_date_sk = date_dim.d_date_sk
        and store_sales.ss_store_sk = store.s_store_sk
        and store_sales.ss_hdemo_sk = household_demographics.hd_demo_sk
        and store_sales.ss_addr_sk = customer_address.ca_address_sk
        and (household_demographics.hd_dep_count = [DEPCNT]
             or household_demographics.hd_vehicle_count = [VEHCNT])
        and date_dim.d_dow in (6,0)
        and date_dim.d_year in ([YEAR],[YEAR]+1,[YEAR]+2)
        and store.s_city in ('[CITY_A]','[CITY_B]','[CITY_C]','[CITY_D]','[CITY_E]')
      group by ss_ticket_number, ss_customer_sk, ss_addr_sk, ca_city) dn,
     customer, customer_address current_addr
where ss_customer_sk = c_customer_sk
  and customer.c_current_addr_sk = current_addr.ca_address_sk
  and current_addr.ca_city <> bought_city
order by c_last_name, c_first_name, ca_city, bought_city, ss_ticket_number
[_LIMITC];
```

</details>

---

## Q47 — Month-over-Month Sales Volatility by Store and Brand

Computes monthly sales vs. 12-month average (within the same category, brand, store) and
selects rows where monthly deviation exceeds 10% of the annual average.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1999–2001 |
| `SELECTONE` | list | various projection column combinations |
| `SELECTTWO` | list | `,v1.d_year` or `,v1.d_year, v1.d_moy` |
| `ORDERBY` | list | `avg_monthly_sales`, `sum_sales`, `psum`, `nsum` |

<details>
<summary>TPC-DS Reference SQL (query47.tpl)</summary>

```sql
with v1 as (
  select i_category, i_brand, s_store_name, s_company_name, d_year, d_moy,
         sum(ss_sales_price) sum_sales,
         avg(sum(ss_sales_price)) over (partition by i_category, i_brand,
                                        s_store_name, s_company_name, d_year) avg_monthly_sales,
         rank() over (partition by i_category, i_brand, s_store_name, s_company_name
                      order by d_year, d_moy) rn
  from item, store_sales, date_dim, store
  where ss_item_sk = i_item_sk and ss_sold_date_sk = d_date_sk
    and ss_store_sk = s_store_sk
    and (d_year = [YEAR] or (d_year = [YEAR]-1 and d_moy = 12)
         or (d_year = [YEAR]+1 and d_moy = 1))
  group by i_category, i_brand, s_store_name, s_company_name, d_year, d_moy),
v2 as (
  select [SELECTONE][SELECTTWO], v1.avg_monthly_sales, v1.sum_sales,
         v1_lag.sum_sales psum, v1_lead.sum_sales nsum
  from v1, v1 v1_lag, v1 v1_lead
  where v1.rn = v1_lag.rn + 1 and v1.rn = v1_lead.rn - 1
    and same category/brand/store conditions)
[_LIMITA] select [_LIMITB] *
from v2
where d_year = [YEAR] and avg_monthly_sales > 0
  and abs(sum_sales - avg_monthly_sales)/avg_monthly_sales > 0.1
order by sum_sales - avg_monthly_sales, [ORDERBY]
[_LIMITC];
```

</details>

---

## Q48 — Store Sales Quantity by Demographic and State

Sums quantities from store sales combining three groups of demographic filters (marital status,
education, price range) with three groups of state and profit filters.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `MS` | list (×3) | 3 draws from marital status — substituted as `{MS.1}`…`{MS.3}` |
| `ES` | list (×3) | 3 draws from education — substituted as `{ES.1}`…`{ES.3}` |
| `STATE` | list (×9) | 9 draws from state codes — substituted as `{STATE.1}`…`{STATE.9}` |
| `YEAR` | integer | 1998–2002 |

<details>
<summary>TPC-DS Reference SQL (query48.tpl)</summary>

```sql
select sum(ss_quantity)
from store_sales, store, customer_demographics, customer_address, date_dim
where s_store_sk = ss_store_sk
  and ss_sold_date_sk = d_date_sk and d_year = [YEAR]
  and ((cd_demo_sk = ss_cdemo_sk and cd_marital_status = '[MS.1]'
        and cd_education_status = '[ES.1]' and ss_sales_price between 100.00 and 150.00)
    or (cd_demo_sk = ss_cdemo_sk and cd_marital_status = '[MS.2]'
        and cd_education_status = '[ES.2]' and ss_sales_price between 50.00 and 100.00)
    or (cd_demo_sk = ss_cdemo_sk and cd_marital_status = '[MS.3]'
        and cd_education_status = '[ES.3]' and ss_sales_price between 150.00 and 200.00))
  and ((ss_addr_sk = ca_address_sk and ca_country = 'United States'
        and ca_state in ('[STATE.1]','[STATE.2]','[STATE.3]') and ss_net_profit between 0 and 2000)
    or (ss_addr_sk = ca_address_sk and ca_country = 'United States'
        and ca_state in ('[STATE.4]','[STATE.5]','[STATE.6]') and ss_net_profit between 150 and 3000)
    or (ss_addr_sk = ca_address_sk and ca_country = 'United States'
        and ca_state in ('[STATE.7]','[STATE.8]','[STATE.9]') and ss_net_profit between 50 and 25000));
```

</details>

---

## Q49 — Top-10 High-Return-Ratio Items by Channel

Ranks items in each of three channels (web, catalog, store) by return-to-sales quantity ratio
and currency ratio, returning items in the top 10 by either metric.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `MONTH` | integer | 11–12 |

<details>
<summary>TPC-DS Reference SQL (query49.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] channel, item, return_ratio, return_rank, currency_rank
from (select 'web' as channel, web.item, web.return_ratio, web.return_rank, web.currency_rank
      from (select item, return_ratio, currency_ratio,
                   rank() over (order by return_ratio) as return_rank,
                   rank() over (order by currency_ratio) as currency_rank
            from (select ws.ws_item_sk as item,
                         (sum(coalesce(wr.wr_return_quantity,0)) /
                          sum(coalesce(ws.ws_quantity,0))) as return_ratio,
                         (sum(coalesce(wr.wr_return_amt,0)) /
                          sum(coalesce(ws.ws_net_paid,0))) as currency_ratio
                  from web_sales ws left outer join web_returns wr
                      on (ws.ws_order_number = wr.wr_order_number and ws.ws_item_sk = wr.wr_item_sk),
                       date_dim
                  where wr.wr_return_amt > 10000 and ws.ws_net_profit > 1
                    and ws_sold_date_sk = d_date_sk and d_year = [YEAR] and d_moy = [MONTH]
                  group by ws.ws_item_sk) in_web) web
      where web.return_rank <= 10 or web.currency_rank <= 10
      union ... same for catalog and store ...)
order by 1, 4, 5, 2
[_LIMITC];
```

</details>

---

## Q50 — Store Returns Aged by Return Latency

Reports counts of returns in each time bucket (≤30 days, 31-60, 61-90, 91-120, >120 days)
per store address, for returns in a given month and year.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `MONTH` | integer | 8–10 |

<details>
<summary>TPC-DS Reference SQL (query50.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  s_store_name, s_company_id, s_street_number, s_street_name, s_street_type,
  s_suite_number, s_city, s_county, s_state, s_zip,
  sum(case when (sr_returned_date_sk - ss_sold_date_sk <= 30) then 1 else 0 end) as "30 days",
  sum(case when (sr_returned_date_sk - ss_sold_date_sk > 30 and
                 sr_returned_date_sk - ss_sold_date_sk <= 60) then 1 else 0 end) as "31-60 days",
  sum(case when (sr_returned_date_sk - ss_sold_date_sk > 60 and
                 sr_returned_date_sk - ss_sold_date_sk <= 90) then 1 else 0 end) as "61-90 days",
  sum(case when (sr_returned_date_sk - ss_sold_date_sk > 90 and
                 sr_returned_date_sk - ss_sold_date_sk <= 120) then 1 else 0 end) as "91-120 days",
  sum(case when (sr_returned_date_sk - ss_sold_date_sk > 120) then 1 else 0 end) as ">120 days"
from store_sales, store_returns, store, date_dim d1, date_dim d2
where d2.d_year = [YEAR] and d2.d_moy = [MONTH]
  and ss_ticket_number = sr_ticket_number and ss_item_sk = sr_item_sk
  and ss_sold_date_sk = d1.d_date_sk and sr_returned_date_sk = d2.d_date_sk
  and ss_customer_sk = sr_customer_sk and ss_store_sk = s_store_sk
group by s_store_name, s_company_id, s_street_number, s_street_name, s_street_type,
         s_suite_number, s_city, s_county, s_state, s_zip
order by s_store_name, s_company_id, ...
[_LIMITC];
```

</details>

---

## Q51 — Web vs. Store Cumulative Sales Race

Computes running cumulative web and store sales per item (ordered by date), then finds items
where cumulative web sales ever exceed cumulative store sales.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1224 |

<details>
<summary>TPC-DS Reference SQL (query51.tpl)</summary>

```sql
with web_v1 as (
  select ws_item_sk item_sk, d_date,
         sum(sum(ws_sales_price)) over (partition by ws_item_sk
             order by d_date rows between unbounded preceding and current row) cume_sales
  from web_sales, date_dim
  where ws_sold_date_sk = d_date_sk and d_month_seq between [DMS] and [DMS]+11
    and ws_item_sk is not null
  group by ws_item_sk, d_date),
store_v1 as (... same for store_sales ...)
[_LIMITA] select [_LIMITB] *
from (select item_sk, d_date, web_sales, store_sales,
             max(web_sales)   over (partition by item_sk order by d_date
                                   rows between unbounded preceding and current row) web_cumulative,
             max(store_sales) over (partition by item_sk order by d_date
                                   rows between unbounded preceding and current row) store_cumulative
      from (select coalesce(web.item_sk, store.item_sk) item_sk,
                   coalesce(web.d_date, store.d_date) d_date,
                   web.cume_sales web_sales, store.cume_sales store_sales
            from web_v1 web full outer join store_v1 store
                on (web.item_sk = store.item_sk and web.d_date = store.d_date)) x) y
where web_cumulative > store_cumulative
order by item_sk, d_date
[_LIMITC];
```

</details>

<details>
<summary>MySQL dialect</summary>

MySQL does not support `FULL OUTER JOIN`. The bexhoma MySQL variant rewrites the join as
`UNION ALL + GROUP BY + COALESCE()` to simulate a full outer join.

</details>

---

## Q52 — Store Sales by Brand and Month (Manager 1)

Similar to Q42 but groups by brand instead of category, reporting total external sales price
for manager ID = 1 in a given month and year.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `MONTH` | integer | 11–12 |
| `YEAR` | integer | 1998–2002 |

<details>
<summary>TPC-DS Reference SQL (query52.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] dt.d_year, item.i_brand_id brand_id, item.i_brand brand,
       sum(ss_ext_sales_price) ext_price
from date_dim dt, store_sales, item
where dt.d_date_sk = store_sales.ss_sold_date_sk
  and store_sales.ss_item_sk = item.i_item_sk
  and item.i_manager_id = 1
  and dt.d_moy = [MONTH]
  and dt.d_year = [YEAR]
group by dt.d_year, item.i_brand, item.i_brand_id
order by dt.d_year, ext_price desc, brand_id
[_LIMITC];
```

</details>

---

## Q53 — Manufacturer Quarterly Sales Deviation

Computes quarterly sales sum vs. the 12-month average per manufacturer for specific category,
class, and brand combinations, finding those with > 10% deviation.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1224 |

<details>
<summary>TPC-DS Reference SQL (query53.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] *
from (select i_manufact_id,
             sum(ss_sales_price) sum_sales,
             avg(sum(ss_sales_price)) over (partition by i_manufact_id) avg_quarterly_sales
      from item, store_sales, date_dim, store
      where ss_item_sk = i_item_sk and ss_sold_date_sk = d_date_sk and ss_store_sk = s_store_sk
        and d_month_seq in ([DMS],[DMS]+1,...,[DMS]+11)
        and ((i_category in ('Books','Children','Electronics')
              and i_class in ('personal','portable','reference','self-help')
              and i_brand in ('scholaramalgamalg #14','scholaramalgamalg #7',
                              'exportiunivamalg #9','scholaramalgamalg #9'))
          or (i_category in ('Women','Music','Men')
              and i_class in ('accessories','classical','fragrances','pants')
              and i_brand in ('amalgimporto #1','edu packscholar #1',
                              'exportiimporto #1','importoamalg #1')))
      group by i_manufact_id, d_qoy) tmp1
where abs(sum_sales - avg_quarterly_sales) / avg_quarterly_sales > 0.1
order by avg_quarterly_sales, sum_sales, i_manufact_id
[_LIMITC];
```

</details>

---

## Q54 — Customer Revenue Segmentation Post-Purchase

Finds customers who purchased items in a specific category and class via catalog or web in a
given month, then segments them by their subsequent store revenue in the next 3 months.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `MONTH` | integer | 1–7 |
| `CATEGORY` | list | derived from categories distribution |
| `CLASS` | list | derived from category-specific class distribution |

<details>
<summary>TPC-DS Reference SQL (query54.tpl)</summary>

```sql
with my_customers as (
  select distinct c_customer_sk, c_current_addr_sk
  from (select cs_sold_date_sk sold_date_sk, cs_bill_customer_sk customer_sk, cs_item_sk item_sk
        from catalog_sales
        union all
        select ws_sold_date_sk, ws_bill_customer_sk, ws_item_sk from web_sales) cs_or_ws_sales,
       item, date_dim, customer
  where sold_date_sk = d_date_sk and item_sk = i_item_sk
    and i_category = '[CATEGORY]' and i_class = '[CLASS]'
    and c_customer_sk = cs_or_ws_sales.customer_sk
    and d_moy = [MONTH] and d_year = [YEAR]),
my_revenue as (
  select c_customer_sk, sum(ss_ext_sales_price) as revenue
  from my_customers, store_sales, customer_address, store, date_dim
  where c_current_addr_sk = ca_address_sk and ca_county = s_county and ca_state = s_state
    and ss_sold_date_sk = d_date_sk and c_customer_sk = ss_customer_sk
    and d_month_seq between (select distinct d_month_seq+1 from date_dim
                             where d_year = [YEAR] and d_moy = [MONTH])
                        and (select distinct d_month_seq+3 from date_dim
                             where d_year = [YEAR] and d_moy = [MONTH])
  group by c_customer_sk),
segments as (select cast((revenue/50) as int) as segment from my_revenue)
[_LIMITA] select [_LIMITB] segment, count(*) as num_customers, segment*50 as segment_base
from segments
group by segment
order by segment, num_customers
[_LIMITC];
```

</details>

<details>
<summary>MariaDB dialect</summary>

The bexhoma MariaDB variant rewrites the `with` clause because MariaDB cannot reference
one CTE from another. The CTEs are inlined as subqueries or wrapped in outer `with total as (...)`.

</details>

---

## Q55 — Store Brand Sales by Month and Manager

Reports total external sales price per brand for a given store manager, month, and year.
Similar to Q52 but with a configurable manager ID.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `MONTH` | integer | 11–12 |
| `MANAGER` | integer | 1–100 |

<details>
<summary>TPC-DS Reference SQL (query55.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] i_brand_id brand_id, i_brand brand,
       sum(ss_ext_sales_price) ext_price
from date_dim, store_sales, item
where d_date_sk = ss_sold_date_sk
  and ss_item_sk = i_item_sk
  and i_manager_id = [MANAGER]
  and d_moy = [MONTH]
  and d_year = [YEAR]
group by i_brand, i_brand_id
order by ext_price desc, i_brand_id
[_LIMITC];
```

</details>

---

## Q56 — Cross-Channel Sales by Color in a Region

Sums total external sales price across all three channels for items matching 3 specific colors,
in a given GMT offset, year, and month.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `MONTH` | integer | 1–7 |
| `GMT` | list | GMT offset derived from county |
| `COLOR` | list (×3) | 3 draws from 67 color names — substituted as `{COLOR.1}`…`{COLOR.3}` |

<details>
<summary>TPC-DS Reference SQL (query56.tpl)</summary>

```sql
with ss as (
  select i_item_id, sum(ss_ext_sales_price) total_sales
  from store_sales, date_dim, customer_address, item
  where i_item_id in (select i_item_id from item
                      where i_color in ('[COLOR.1]','[COLOR.2]','[COLOR.3]'))
    and ss_item_sk = i_item_sk and ss_sold_date_sk = d_date_sk
    and d_year = [YEAR] and d_moy = [MONTH]
    and ss_addr_sk = ca_address_sk and ca_gmt_offset = [GMT]
  group by i_item_id),
cs as (... same for catalog_sales ...),
ws as (... same for web_sales ...)
[_LIMITA] select [_LIMITB] i_item_id, sum(total_sales) total_sales
from (select * from ss union all select * from cs union all select * from ws) tmp1
group by i_item_id
order by total_sales, i_item_id
[_LIMITC];
```

</details>

---

## Q57 — Catalog Sales Monthly Volatility by Call Center

Analogous to Q47 but for catalog sales grouped by call center instead of store,
finding brands with > 10% deviation from monthly average.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1999–2001 |
| `SELECTONE` | list | projection column combinations |
| `SELECTTWO` | list | `,v1.d_year` or `,v1.d_year, v1.d_moy` |
| `ORDERBY` | list | avg_monthly_sales, sum_sales, psum, nsum |

<details>
<summary>TPC-DS Reference SQL (query57.tpl)</summary>

```sql
with v1 as (
  select i_category, i_brand, cc_name, d_year, d_moy,
         sum(cs_sales_price) sum_sales,
         avg(sum(cs_sales_price)) over (partition by i_category, i_brand, cc_name, d_year) avg_monthly_sales,
         rank() over (partition by i_category, i_brand, cc_name order by d_year, d_moy) rn
  from item, catalog_sales, date_dim, call_center
  where cs_item_sk = i_item_sk and cs_sold_date_sk = d_date_sk
    and cc_call_center_sk = cs_call_center_sk
    and (d_year = [YEAR] or (d_year = [YEAR]-1 and d_moy = 12)
         or (d_year = [YEAR]+1 and d_moy = 1))
  group by i_category, i_brand, cc_name, d_year, d_moy),
v2 as (select [SELECTONE][SELECTTWO], v1.avg_monthly_sales, v1.sum_sales,
              v1_lag.sum_sales psum, v1_lead.sum_sales nsum
       from v1, v1 v1_lag, v1 v1_lead
       where v1.rn = v1_lag.rn + 1 and v1.rn = v1_lead.rn - 1
         and same category/brand/call-center conditions)
[_LIMITA] select [_LIMITB] *
from v2
where d_year = [YEAR] and avg_monthly_sales > 0
  and abs(sum_sales - avg_monthly_sales)/avg_monthly_sales > 0.1
order by sum_sales - avg_monthly_sales, [ORDERBY]
[_LIMITC];
```

</details>

---

## Q58 — Cross-Channel Weekly Revenue Comparison

Joins store, catalog, and web revenues for the same items in the same fiscal week, then returns
items where all three channels have revenues within 10% of each other.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `SALES_DATE` | date | derived from `{YEAR}` (Jan 1 – Jul 24) |

<details>
<summary>TPC-DS Reference SQL (query58.tpl)</summary>

```sql
with ss_items as (
  select i_item_id item_id, sum(ss_ext_sales_price) ss_item_rev
  from store_sales, item, date_dim
  where ss_item_sk = i_item_sk
    and d_date in (select d_date from date_dim
                   where d_week_seq = (select d_week_seq from date_dim where d_date = '[SALES_DATE]'))
    and ss_sold_date_sk = d_date_sk
  group by i_item_id),
cs_items as (... same for catalog_sales ...),
ws_items as (... same for web_sales ...)
[_LIMITA] select [_LIMITB] ss_items.item_id, ss_item_rev,
       ss_item_rev/((ss_item_rev+cs_item_rev+ws_item_rev)/3)*100 ss_dev,
       cs_item_rev,
       cs_item_rev/((ss_item_rev+cs_item_rev+ws_item_rev)/3)*100 cs_dev,
       ws_item_rev,
       ws_item_rev/((ss_item_rev+cs_item_rev+ws_item_rev)/3)*100 ws_dev,
       (ss_item_rev+cs_item_rev+ws_item_rev)/3 average
from ss_items, cs_items, ws_items
where ss_items.item_id = cs_items.item_id and ss_items.item_id = ws_items.item_id
  and ss_item_rev between 0.9*cs_item_rev and 1.1*cs_item_rev
  and ss_item_rev between 0.9*ws_item_rev and 1.1*ws_item_rev
  and cs_item_rev between 0.9*ws_item_rev and 1.1*ws_item_rev
order by item_id, ss_item_rev
[_LIMITC];
```

</details>

---

## Q59 — Weekly Store Sales YoY Day-of-Week Ratios

Computes ratios of weekly store sales (by day of week) comparing two consecutive 12-month
periods, for stores with matching IDs.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1212 |

<details>
<summary>TPC-DS Reference SQL (query59.tpl)</summary>

```sql
with wss as (
  select d_week_seq, ss_store_sk,
         sum(case when d_day_name='Sunday'    then ss_sales_price else null end) sun_sales,
         sum(case when d_day_name='Monday'    then ss_sales_price else null end) mon_sales,
         sum(case when d_day_name='Tuesday'   then ss_sales_price else null end) tue_sales,
         sum(case when d_day_name='Wednesday' then ss_sales_price else null end) wed_sales,
         sum(case when d_day_name='Thursday'  then ss_sales_price else null end) thu_sales,
         sum(case when d_day_name='Friday'    then ss_sales_price else null end) fri_sales,
         sum(case when d_day_name='Saturday'  then ss_sales_price else null end) sat_sales
  from store_sales, date_dim where d_date_sk = ss_sold_date_sk
  group by d_week_seq, ss_store_sk)
[_LIMITA] select [_LIMITB]
  s_store_name1, s_store_id1, d_week_seq1,
  sun_sales1/sun_sales2, mon_sales1/mon_sales2, tue_sales1/tue_sales2,
  wed_sales1/wed_sales2, thu_sales1/thu_sales2, fri_sales1/fri_sales2, sat_sales1/sat_sales2
from (select s_store_name s_store_name1, wss.d_week_seq d_week_seq1, s_store_id s_store_id1,
             sun_sales sun_sales1, mon_sales mon_sales1, ... from wss, store, date_dim d
      where d.d_week_seq = wss.d_week_seq and ss_store_sk = s_store_sk
        and d_month_seq between [DMS] and [DMS]+11) y,
     (select ... from wss, store, date_dim d
      where d_month_seq between [DMS]+12 and [DMS]+23) x
where s_store_id1 = s_store_id2 and d_week_seq1 = d_week_seq2-52
order by s_store_name1, s_store_id1, d_week_seq1
[_LIMITC];
```

</details>

---

## Q60 — Cross-Channel Sales by Category in a Region

Analogous to Q33 and Q56 but filters by item category and GMT offset in months 8–10.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `MONTH` | integer | 8–10 |
| `GMT` | list | GMT offset derived from county |
| `CATEGORY` | list | Children, Men, Music, Jewelry, Shoes |

<details>
<summary>TPC-DS Reference SQL (query60.tpl)</summary>

```sql
with ss as (
  select i_item_id, sum(ss_ext_sales_price) total_sales
  from store_sales, date_dim, customer_address, item
  where i_item_id in (select i_item_id from item where i_category in ('[CATEGORY]'))
    and ss_item_sk = i_item_sk and ss_sold_date_sk = d_date_sk
    and d_year = [YEAR] and d_moy = [MONTH]
    and ss_addr_sk = ca_address_sk and ca_gmt_offset = [GMT]
  group by i_item_id),
cs as (... same for catalog_sales ...),
ws as (... same for web_sales ...)
[_LIMITA] select [_LIMITB] i_item_id, sum(total_sales) total_sales
from (select * from ss union all select * from cs union all select * from ws) tmp1
group by i_item_id
order by i_item_id, total_sales
[_LIMITC];
```

</details>

---

## Q61 — Promotional vs. Total Store Sales Ratio

Computes the percentage of store sales that came through promotional channels (email, mail, TV)
for a given category, GMT offset, month, and year.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `MONTH` | integer | 11–12 |
| `GMT` | list | -6 or -7 |
| `CATEGORY` | list | Books, Home, Electronics, Jewelry, Sports |

<details>
<summary>TPC-DS Reference SQL (query61.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  promotions, total,
  cast(promotions as decimal(15,4))/cast(total as decimal(15,4))*100
from
  (select sum(ss_ext_sales_price) promotions
   from store_sales, store, promotion, date_dim, customer, customer_address, item
   where ss_sold_date_sk = d_date_sk and ss_store_sk = s_store_sk
     and ss_promo_sk = p_promo_sk and ss_customer_sk = c_customer_sk
     and ca_address_sk = c_current_addr_sk and ss_item_sk = i_item_sk
     and ca_gmt_offset = [GMT] and i_category = '[CATEGORY]'
     and (p_channel_dmail = 'Y' or p_channel_email = 'Y' or p_channel_tv = 'Y')
     and s_gmt_offset = [GMT] and d_year = [YEAR] and d_moy = [MONTH]) promotional_sales,
  (select sum(ss_ext_sales_price) total
   from store_sales, store, date_dim, customer, customer_address, item
   where ... same without promotion filter ...) all_sales
order by promotions, total
[_LIMITC];
```

</details>

---

## Q62 — Web Order Shipping Latency Buckets

Reports counts of web orders in time buckets (≤30 days to >120 days) from sale to ship date,
per warehouse, shipping mode, and web site.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1224 |

<details>
<summary>TPC-DS Reference SQL (query62.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  substr(w_warehouse_name,1,20), sm_type, web_name,
  sum(case when ws_ship_date_sk - ws_sold_date_sk <= 30 then 1 else 0 end) as "30 days",
  sum(case when ws_ship_date_sk - ws_sold_date_sk > 30
           and ws_ship_date_sk - ws_sold_date_sk <= 60 then 1 else 0 end) as "31-60 days",
  sum(case when ws_ship_date_sk - ws_sold_date_sk > 60
           and ws_ship_date_sk - ws_sold_date_sk <= 90 then 1 else 0 end) as "61-90 days",
  sum(case when ws_ship_date_sk - ws_sold_date_sk > 90
           and ws_ship_date_sk - ws_sold_date_sk <= 120 then 1 else 0 end) as "91-120 days",
  sum(case when ws_ship_date_sk - ws_sold_date_sk > 120 then 1 else 0 end) as ">120 days"
from web_sales, warehouse, ship_mode, web_site, date_dim
where d_month_seq between [DMS] and [DMS]+11
  and ws_ship_date_sk = d_date_sk
  and ws_warehouse_sk = w_warehouse_sk
  and ws_ship_mode_sk = sm_ship_mode_sk
  and ws_web_site_sk = web_site_sk
group by substr(w_warehouse_name,1,20), sm_type, web_name
order by substr(w_warehouse_name,1,20), sm_type, web_name
[_LIMITC];
```

</details>

---

## Q63 — Manager-Level Monthly Sales Deviation

Analogous to Q53 but groups by manager instead of manufacturer, finding managers with monthly
sales deviation > 10% of their personal monthly average.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1224 |

<details>
<summary>TPC-DS Reference SQL (query63.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] *
from (select i_manager_id, sum(ss_sales_price) sum_sales,
             avg(sum(ss_sales_price)) over (partition by i_manager_id) avg_monthly_sales
      from item, store_sales, date_dim, store
      where ss_item_sk = i_item_sk and ss_sold_date_sk = d_date_sk
        and ss_store_sk = s_store_sk
        and d_month_seq in ([DMS],[DMS]+1,...,[DMS]+11)
        and ((i_category in ('Books','Children','Electronics') and ...) or
             (i_category in ('Women','Music','Men') and ...))
      group by i_manager_id, d_moy) tmp1
where abs(sum_sales - avg_monthly_sales)/avg_monthly_sales > 0.1
order by i_manager_id, avg_monthly_sales, sum_sales
[_LIMITC];
```

</details>

---

## Q64 — Cross-Year Item and Store Sales with Customer Demographics

One of the most complex TPC-DS queries. Joins store sales, returns, catalog cross-sales,
customer demographics, household demographics, addresses, income bands, and promotions to
compare two consecutive years (syear and fsyear) for items with low return ratios.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `COLOR` | list (×6) | 6 draws from 67 color names — substituted as `{COLOR.1}`…`{COLOR.6}` |
| `PRICE` | integer | 0–85 |
| `YEAR` | integer | 1999–2001 |

<details>
<summary>TPC-DS Reference SQL (query64.tpl)</summary>

```sql
with cs_ui as (
  select cs_item_sk, sum(cs_ext_list_price) as sale,
         sum(cr_refunded_cash+cr_reversed_charge+cr_store_credit) as refund
  from catalog_sales, catalog_returns
  where cs_item_sk = cr_item_sk and cs_order_number = cr_order_number
  group by cs_item_sk
  having sum(cs_ext_list_price) > 2*sum(cr_refunded_cash+cr_reversed_charge+cr_store_credit)),
cross_sales as (
  select i_product_name, i_item_sk, s_store_name, s_zip,
         ... demographics, address, date fields ...,
         count(*) cnt, sum(ss_wholesale_cost) s1, sum(ss_list_price) s2, sum(ss_coupon_amt) s3
  from store_sales, store_returns, cs_ui, date_dim d1, date_dim d2, date_dim d3,
       store, customer, customer_demographics cd1, customer_demographics cd2, promotion,
       household_demographics hd1, hd2, customer_address ad1, ad2, income_band ib1, ib2, item
  where ... complex join conditions ...
    and cd1.cd_marital_status <> cd2.cd_marital_status
    and i_color in ('[COLOR.1]',... ,'[COLOR.6]')
    and i_current_price between [PRICE] and [PRICE]+15
  group by i_product_name, i_item_sk, s_store_name, s_zip, ...)
select cs1.product_name, cs1.store_name, cs1.store_zip, ...,
       cs1.syear, cs1.cnt, cs1.s1 as s11, cs1.s2 as s21, cs1.s3 as s31,
       cs2.s1 as s12, cs2.s2 as s22, cs2.s3 as s32, cs2.syear, cs2.cnt
from cross_sales cs1, cross_sales cs2
where cs1.item_sk = cs2.item_sk
  and cs1.syear = [YEAR] and cs2.syear = [YEAR]+1
  and cs2.cnt <= cs1.cnt
  and cs1.store_name = cs2.store_name and cs1.store_zip = cs2.store_zip
order by cs1.product_name, cs1.store_name, cs2.cnt, cs1.s1, cs2.s1;
```

</details>

---

## Q65 — Items Underperforming Store Average

Finds items whose revenue in a 12-month sequence is at most 10% of the store's average
item revenue.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1224 |

<details>
<summary>TPC-DS Reference SQL (query65.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  s_store_name, i_item_desc, sc.revenue, i_current_price, i_wholesale_cost, i_brand
from store, item,
     (select ss_store_sk, avg(revenue) as ave
      from (select ss_store_sk, ss_item_sk, sum(ss_sales_price) as revenue
            from store_sales, date_dim
            where ss_sold_date_sk = d_date_sk and d_month_seq between [DMS] and [DMS]+11
            group by ss_store_sk, ss_item_sk) sa
      group by ss_store_sk) sb,
     (select ss_store_sk, ss_item_sk, sum(ss_sales_price) as revenue
      from store_sales, date_dim
      where ss_sold_date_sk = d_date_sk and d_month_seq between [DMS] and [DMS]+11
      group by ss_store_sk, ss_item_sk) sc
where sb.ss_store_sk = sc.ss_store_sk
  and sc.revenue <= 0.1 * sb.ave
  and s_store_sk = sc.ss_store_sk
  and i_item_sk = sc.ss_item_sk
order by s_store_name, i_item_desc
[_LIMITC];
```

</details>

---

## Q66 — Warehouse Monthly Sales and Net by Ship Mode (Pivot)

Pivots monthly sales amounts and net amounts for web and catalog channels across all 12 months,
per warehouse, filtered by time window and ship mode carrier.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `TIMEONE` | integer | 1–57597 (seconds from midnight) |
| `SMC` | list (×2) | 2 draws from carrier names — substituted as `{SMC.1}`, `{SMC.2}` |
| `NETONE` | list | web net price column |
| `NETTWO` | list | catalog net price column |
| `SALESONE` | list | web sales price column |
| `SALESTWO` | list | catalog sales price column |

<details>
<summary>TPC-DS Reference SQL (query66.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  w_warehouse_name, w_warehouse_sq_ft, w_city, w_county, w_state, w_country,
  ship_carriers, year,
  sum(jan_sales) as jan_sales, ..., sum(dec_sales) as dec_sales,
  sum(jan_sales/w_warehouse_sq_ft) as jan_sales_per_sq_foot, ...,
  sum(jan_net) as jan_net, ..., sum(dec_net) as dec_net
from (select w_warehouse_name, ...,
             '[SMC.1]'||','||'[SMC.2]' as ship_carriers, d_year as year,
             sum(case when d_moy=1 then [SALESONE]*ws_quantity else 0 end) as jan_sales,
             ...,
             sum(case when d_moy=1 then [NETONE]*ws_quantity else 0 end) as jan_net, ...
      from web_sales, warehouse, date_dim, time_dim, ship_mode
      where ws_warehouse_sk = w_warehouse_sk and ws_sold_date_sk = d_date_sk
        and ws_sold_time_sk = t_time_sk and ws_ship_mode_sk = sm_ship_mode_sk
        and d_year = [YEAR]
        and t_time between [TIMEONE] and [TIMEONE]+28800
        and sm_carrier in ('[SMC.1]','[SMC.2]')
      group by w_warehouse_name, ..., d_year
      union all
      select ... same for catalog_sales ...) x
group by w_warehouse_name, ..., ship_carriers, year
order by w_warehouse_name
[_LIMITC];
```

</details>

<details>
<summary>MariaDB / MonetDB / PostgreSQL dialects</summary>

The string concatenation `'[SMC.1]' || ',' || '[SMC.2]'` is standard SQL.
The bexhoma MariaDB variant may use `CONCAT()` instead.

</details>

---

## Q67 — Top-100 Items by Category, Brand, and Rollup

Ranks items within category by total sales using `ROLLUP` over multiple dimensions,
returning only those with rank ≤ 100.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1224 |

<details>
<summary>TPC-DS Reference SQL (query67.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] *
from (select i_category, i_class, i_brand, i_product_name,
             d_year, d_qoy, d_moy, s_store_id,
             sum(coalesce(ss_sales_price*ss_quantity,0)) sumsales,
             rank() over (partition by i_category order by sumsales desc) rk
      from (select i_category, i_class, i_brand, i_product_name,
                   d_year, d_qoy, d_moy, s_store_id,
                   sum(coalesce(ss_sales_price*ss_quantity,0)) sumsales
            from store_sales, date_dim, store, item
            where ss_sold_date_sk = d_date_sk and ss_item_sk = i_item_sk
              and ss_store_sk = s_store_sk
              and d_month_seq between [DMS] and [DMS]+11
            group by rollup(i_category, i_class, i_brand, i_product_name,
                            d_year, d_qoy, d_moy, s_store_id)) dw1) dw2
where rk <= 100
order by i_category, i_class, i_brand, i_product_name,
         d_year, d_qoy, d_moy, s_store_id, sumsales, rk
[_LIMITC];
```

</details>

<details>
<summary>MariaDB / MonetDB / PostgreSQL dialects</summary>

MariaDB uses `GROUP BY i_category, i_class, ... WITH ROLLUP`.
MonetDB and PostgreSQL use standard `GROUP BY ROLLUP(...)`.

</details>

---

## Q68 — Customer City vs. Purchase City Mismatch (2 Cities)

Simplified version of Q46 with only 2 store cities and purchases on days-of-month 1–2.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DEPCNT` | integer | 0–9 |
| `YEAR` | integer | 1998–2000 |
| `VEHCNT` | integer | -1–4 |
| `CITY` | list (×2) | 2 draws from active store cities — substituted as `{CITY.1}`, `{CITY.2}` |

<details>
<summary>TPC-DS Reference SQL (query68.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  c_last_name, c_first_name, ca_city, bought_city,
  ss_ticket_number, extended_price, extended_tax, list_price
from (select ss_ticket_number, ss_customer_sk, ca_city bought_city,
             sum(ss_ext_sales_price) extended_price,
             sum(ss_ext_list_price) list_price,
             sum(ss_ext_tax) extended_tax
      from store_sales, date_dim, store, household_demographics, customer_address
      where store_sales.ss_sold_date_sk = date_dim.d_date_sk
        and store_sales.ss_store_sk = store.s_store_sk
        and store_sales.ss_hdemo_sk = household_demographics.hd_demo_sk
        and store_sales.ss_addr_sk = customer_address.ca_address_sk
        and date_dim.d_dom between 1 and 2
        and (household_demographics.hd_dep_count = [DEPCNT]
             or household_demographics.hd_vehicle_count = [VEHCNT])
        and date_dim.d_year in ([YEAR],[YEAR]+1,[YEAR]+2)
        and store.s_city in ('[CITY_A]','[CITY_B]')
      group by ss_ticket_number, ss_customer_sk, ss_addr_sk, ca_city) dn,
     customer, customer_address current_addr
where ss_customer_sk = c_customer_sk
  and customer.c_current_addr_sk = current_addr.ca_address_sk
  and current_addr.ca_city <> bought_city
order by c_last_name, ss_ticket_number
[_LIMITC];
```

</details>

---

## Q69 — Store-Only Customers Not Buying Web or Catalog

Finds customers who shopped in-store in a 3-month window but NOT via web or catalog in the same
period, reporting demographic distributions.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `MONTH` | integer | 1–4 |
| `YEAR` | integer | 1999–2004 |
| `STATE` | list (×3) | 3 draws from state codes — substituted as `{STATE.1}`…`{STATE.3}` |

<details>
<summary>TPC-DS Reference SQL (query69.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  cd_gender, cd_marital_status, cd_education_status, count(*) cnt1,
  cd_purchase_estimate, count(*) cnt2, cd_credit_rating, count(*) cnt3
from customer c, customer_address ca, customer_demographics
where c.c_current_addr_sk = ca.ca_address_sk
  and ca_state in ('[STATE.1]','[STATE.2]','[STATE.3]')
  and cd_demo_sk = c.c_current_cdemo_sk
  and exists (select * from store_sales, date_dim
              where c.c_customer_sk = ss_customer_sk
                and ss_sold_date_sk = d_date_sk and d_year = [YEAR]
                and d_moy between [MONTH] and [MONTH]+2)
  and not exists (select * from web_sales, date_dim
                  where c.c_customer_sk = ws_bill_customer_sk
                    and ws_sold_date_sk = d_date_sk and d_year = [YEAR]
                    and d_moy between [MONTH] and [MONTH]+2)
  and not exists (select * from catalog_sales, date_dim
                  where c.c_customer_sk = cs_ship_customer_sk
                    and cs_sold_date_sk = d_date_sk and d_year = [YEAR]
                    and d_moy between [MONTH] and [MONTH]+2)
group by cd_gender, cd_marital_status, cd_education_status, cd_purchase_estimate, cd_credit_rating
order by cd_gender, cd_marital_status, cd_education_status, cd_purchase_estimate, cd_credit_rating
[_LIMITC];
```

</details>

---

## Q70 — Store Net Profit by State and County with Rollup

Ranks stores within the top-5 states by net profit, using `ROLLUP` to generate subtotals at state
and county level.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1224 |

<details>
<summary>TPC-DS Reference SQL (query70.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  sum(ss_net_profit) as total_sum, s_state, s_county,
  grouping(s_state)+grouping(s_county) as lochierarchy,
  rank() over (partition by grouping(s_state)+grouping(s_county),
               case when grouping(s_county) = 0 then s_state end
               order by sum(ss_net_profit) desc) as rank_within_parent
from store_sales, date_dim d1, store
where d1.d_month_seq between [DMS] and [DMS]+11
  and d1.d_date_sk = ss_sold_date_sk and s_store_sk = ss_store_sk
  and s_state in (select s_state
                  from (select s_state,
                               rank() over (partition by s_state
                                            order by sum(ss_net_profit) desc) as ranking
                        from store_sales, store, date_dim
                        where d_month_seq between [DMS] and [DMS]+11
                          and d_date_sk = ss_sold_date_sk and s_store_sk = ss_store_sk
                        group by s_state) tmp1
                  where ranking <= 5)
group by rollup(s_state, s_county)
order by lochierarchy desc, case when lochierarchy = 0 then s_state end, rank_within_parent
[_LIMITC];
```

</details>

<details>
<summary>MariaDB / MonetDB / PostgreSQL dialects</summary>

MariaDB uses `GROUP BY s_state, s_county WITH ROLLUP`.
MonetDB and PostgreSQL use standard `GROUP BY ROLLUP(s_state, s_county)`.

</details>

---

## Q71 — Cross-Channel Brand Sales by Time of Day

Sums external sales across all three channels for manager ID = 1 brands, sold during breakfast
or dinner meal times in a given month and year.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `MONTH` | integer | 11–12 |

<details>
<summary>TPC-DS Reference SQL (query71.tpl)</summary>

```sql
select i_brand_id brand_id, i_brand brand, t_hour, t_minute,
       sum(ext_price) ext_price
from item, (select ws_ext_sales_price as ext_price, ws_sold_date_sk as sold_date_sk,
                   ws_item_sk as sold_item_sk, ws_sold_time_sk as time_sk
            from web_sales, date_dim
            where d_date_sk = ws_sold_date_sk and d_moy = [MONTH] and d_year = [YEAR]
            union all
            select cs_ext_sales_price, cs_sold_date_sk, cs_item_sk, cs_sold_time_sk
            from catalog_sales, date_dim
            where d_date_sk = cs_sold_date_sk and d_moy = [MONTH] and d_year = [YEAR]
            union all
            select ss_ext_sales_price, ss_sold_date_sk, ss_item_sk, ss_sold_time_sk
            from store_sales, date_dim
            where d_date_sk = ss_sold_date_sk and d_moy = [MONTH] and d_year = [YEAR]) tmp,
            time_dim
where sold_item_sk = i_item_sk and i_manager_id = 1
  and time_sk = t_time_sk and (t_meal_time = 'breakfast' or t_meal_time = 'dinner')
group by i_brand, i_brand_id, t_hour, t_minute
order by ext_price desc, i_brand_id;
```

</details>

---

## Q72 — Catalog Orders with Inventory Shortfalls (No Promotion or Returned)

Counts and breaks out catalog orders where inventory was insufficient at sale time, shipped
after 5+ days, without promotion or with returns.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `BP` | list | `1001-5000`, `>10000`, `501-1000` |
| `MS` | list | marital status codes |

<details>
<summary>TPC-DS Reference SQL (query72.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  i_item_desc, w_warehouse_name, d1.d_week_seq,
  sum(case when p_promo_sk is null then 1 else 0 end) no_promo,
  sum(case when p_promo_sk is not null then 1 else 0 end) promo,
  count(*) total_cnt
from catalog_sales
join inventory on (cs_item_sk = inv_item_sk)
join warehouse on (w_warehouse_sk = inv_warehouse_sk)
join item on (i_item_sk = cs_item_sk)
join customer_demographics on (cs_bill_cdemo_sk = cd_demo_sk)
join household_demographics on (cs_bill_hdemo_sk = hd_demo_sk)
join date_dim d1 on (cs_sold_date_sk = d1.d_date_sk)
join date_dim d2 on (inv_date_sk = d2.d_date_sk)
join date_dim d3 on (cs_ship_date_sk = d3.d_date_sk)
left outer join promotion on (cs_promo_sk = p_promo_sk)
left outer join catalog_returns on (cr_item_sk = cs_item_sk and cr_order_number = cs_order_number)
where d1.d_week_seq = d2.d_week_seq
  and inv_quantity_on_hand < cs_quantity
  and d3.d_date > d1.d_date + 5
  and hd_buy_potential = '[BP]'
  and d1.d_year = [YEAR]
  and cd_marital_status = '[MS]'
group by i_item_desc, w_warehouse_name, d1.d_week_seq
order by total_cnt desc, i_item_desc, w_warehouse_name, d_week_seq
[_LIMITC];
```

</details>

---

## Q73 — Customer Ticket Frequency (1–5 Purchases) in Specific Counties

Finds customers with 1–5 store purchases in households with good buy potential, for early-month
(dom 1–2) purchases across 4 counties.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `BPONE` | list | `1001-5000`, `>10000`, `501-1000` |
| `BPTWO` | list | `0-500`, `Unknown`, `5001-10000` |
| `YEAR` | integer | 1998–2000 |
| `COUNTY` | list (×4) | 4 draws from active store counties — substituted as `{COUNTY.1}`…`{COUNTY.4}` |

<details>
<summary>TPC-DS Reference SQL (query73.tpl)</summary>

```sql
select c_last_name, c_first_name, c_salutation, c_preferred_cust_flag,
       ss_ticket_number, cnt
from (select ss_ticket_number, ss_customer_sk, count(*) cnt
      from store_sales, date_dim, store, household_demographics
      where store_sales.ss_sold_date_sk = date_dim.d_date_sk
        and store_sales.ss_store_sk = store.s_store_sk
        and store_sales.ss_hdemo_sk = household_demographics.hd_demo_sk
        and date_dim.d_dom between 1 and 2
        and (household_demographics.hd_buy_potential = '[BPONE]'
             or household_demographics.hd_buy_potential = '[BPTWO]')
        and household_demographics.hd_vehicle_count > 0
        and household_demographics.hd_dep_count/household_demographics.hd_vehicle_count > 1
        and date_dim.d_year in ([YEAR],[YEAR]+1,[YEAR]+2)
        and store.s_county in ('[COUNTY.1]','[COUNTY.2]','[COUNTY.3]','[COUNTY.4]')
      group by ss_ticket_number, ss_customer_sk) dj, customer
where ss_customer_sk = c_customer_sk and cnt between 1 and 5
order by cnt desc, c_last_name asc;
```

</details>

---

## Q74 — YoY Growth in Store vs. Web Net Paid

Finds customers whose web sales growth year-over-year exceeded their store sales growth,
using an aggregate function on net paid amounts.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2001 |
| `AGGONE` | list | sum, min, max, avg, stddev_samp |
| `ORDERC` | integer (×3) | 3 draws from 1–3 (column positions used in ORDER BY) |

<details>
<summary>TPC-DS Reference SQL (query74.tpl)</summary>

```sql
with year_total as (
  select c_customer_id customer_id, c_first_name, c_last_name, d_year as year,
         [AGGONE](ss_net_paid) year_total, 's' sale_type
  from customer, store_sales, date_dim
  where c_customer_sk = ss_customer_sk and ss_sold_date_sk = d_date_sk
    and d_year in ([YEAR],[YEAR]+1)
  group by c_customer_id, c_first_name, c_last_name, d_year
  union all
  select c_customer_id, c_first_name, c_last_name, d_year,
         [AGGONE](ws_net_paid), 'w' from customer, web_sales, date_dim
  where c_customer_sk = ws_bill_customer_sk and ws_sold_date_sk = d_date_sk
    and d_year in ([YEAR],[YEAR]+1)
  group by c_customer_id, c_first_name, c_last_name, d_year)
[_LIMITA] select [_LIMITB]
  t_s_secyear.customer_id, t_s_secyear.customer_first_name, t_s_secyear.customer_last_name
from year_total t_s_firstyear, year_total t_s_secyear,
     year_total t_w_firstyear, year_total t_w_secyear
where t_s_firstyear.customer_id = t_s_secyear.customer_id
  and t_s_firstyear.customer_id = t_w_firstyear.customer_id
  and t_s_firstyear.customer_id = t_w_secyear.customer_id
  and t_s_firstyear.sale_type = 's' and t_w_firstyear.sale_type = 'w'
  and t_s_secyear.sale_type = 's' and t_w_secyear.sale_type = 'w'
  and t_s_firstyear.year = [YEAR] and t_s_secyear.year = [YEAR]+1
  and t_w_firstyear.year = [YEAR] and t_w_secyear.year = [YEAR]+1
  and t_s_firstyear.year_total > 0 and t_w_firstyear.year_total > 0
  and t_w_secyear.year_total/t_w_firstyear.year_total >
      t_s_secyear.year_total/t_s_firstyear.year_total
order by [ORDERC.1], [ORDERC.2], [ORDERC.3]
[_LIMITC];
```

</details>

---

## Q75 — Cross-Channel Sales Count and Amount YoY

Computes total quantity sold and amount for each item dimension (brand, class, category,
manufacturer) across all three channels in two consecutive years, flagging items with
more than 10% drop in quantity.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `CATEGORY` | list | derived from categories distribution |
| `YEAR` | integer | 1999–2002 |

<details>
<summary>TPC-DS Reference SQL (query75.tpl)</summary>

```sql
with all_sales as (
  select d_year, i_brand_id, i_class_id, i_category_id, i_manufact_id,
         sum(sales_cnt) as sales_cnt, sum(sales_amt) as sales_amt
  from (select d_year, i_brand_id, i_class_id, i_category_id, i_manufact_id,
               cs_quantity - coalesce(cr_return_quantity,0) as sales_cnt,
               cs_ext_sales_price - coalesce(cr_return_amount,0.0) as sales_amt
        from catalog_sales join item ... join date_dim ...
             left join catalog_returns ... where i_category = '[CATEGORY]'
        union
        select ... from store_sales ... where i_category = '[CATEGORY]'
        union
        select ... from web_sales ... where i_category = '[CATEGORY]') sales_detail
  group by d_year, i_brand_id, i_class_id, i_category_id, i_manufact_id)
[_LIMITA] select [_LIMITB]
  prev_yr.d_year as prev_year, curr_yr.d_year as year,
  curr_yr.i_brand_id, curr_yr.i_class_id, curr_yr.i_category_id, curr_yr.i_manufact_id,
  prev_yr.sales_cnt as prev_yr_cnt, curr_yr.sales_cnt as curr_yr_cnt,
  curr_yr.sales_cnt - prev_yr.sales_cnt as sales_cnt_diff,
  curr_yr.sales_amt - prev_yr.sales_amt as sales_amt_diff
from all_sales curr_yr, all_sales prev_yr
where curr_yr.i_brand_id = prev_yr.i_brand_id and ...
  and curr_yr.d_year = [YEAR] and prev_yr.d_year = [YEAR]-1
  and cast(curr_yr.sales_cnt as decimal(17,2))/cast(prev_yr.sales_cnt as decimal(17,2)) < 0.9
order by sales_cnt_diff, sales_amt_diff
[_LIMITC];
```

</details>

---

## Q76 — Null-Column Sales Count by Channel

Finds sales records with a null value in a specific key column (one of many possible nullable FKs)
across all three channels, reporting counts and totals by channel, year, quarter, and category.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `NULLCOLSS` | list | nullable store sales FK column |
| `NULLCOLWS` | list | nullable web sales FK column |
| `NULLCOLCS` | list | nullable catalog sales FK column |

<details>
<summary>TPC-DS Reference SQL (query76.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  channel, col_name, d_year, d_qoy, i_category,
  count(*) sales_cnt, sum(ext_sales_price) sales_amt
from (select 'store' as channel, '[NULLCOLSS]' col_name, d_year, d_qoy, i_category,
             ss_ext_sales_price ext_sales_price
      from store_sales, item, date_dim
      where [NULLCOLSS] is null and ss_sold_date_sk = d_date_sk and ss_item_sk = i_item_sk
      union all
      select 'web', '[NULLCOLWS]', d_year, d_qoy, i_category, ws_ext_sales_price
      from web_sales, item, date_dim
      where [NULLCOLWS] is null and ws_sold_date_sk = d_date_sk and ws_item_sk = i_item_sk
      union all
      select 'catalog', '[NULLCOLCS]', d_year, d_qoy, i_category, cs_ext_sales_price
      from catalog_sales, item, date_dim
      where [NULLCOLCS] is null and cs_sold_date_sk = d_date_sk and cs_item_sk = i_item_sk) foo
group by channel, col_name, d_year, d_qoy, i_category
order by channel, col_name, d_year, d_qoy, i_category
[_LIMITC];
```

</details>

---

## Q77 — Cross-Channel Net Profit with Returns (Rollup)

Computes sales, returns, and net profit for each channel (store, catalog, web) in a 30-day
period, using `ROLLUP` to generate channel-level and grand totals.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `SALES_DATE` | date | derived: Aug 1 – Aug 30 of `{YEAR}` |

<details>
<summary>TPC-DS Reference SQL (query77.tpl)</summary>

```sql
with ss as (
  select s_store_sk, sum(ss_ext_sales_price) as sales, sum(ss_net_profit) as profit
  from store_sales, date_dim, store
  where ss_sold_date_sk = d_date_sk
    and d_date between '[SALES_DATE]' and '[SALES_DATE]'+30 days
    and ss_store_sk = s_store_sk group by s_store_sk),
sr as (... store returns in same window ...),
cs as (... catalog sales ...),
cr as (... catalog returns ...),
ws as (... web sales ...),
wr as (... web returns ...)
[_LIMITA] select [_LIMITB] channel, id,
  sum(sales) as sales, sum(returns) as returns, sum(profit) as profit
from (select 'store channel' as channel, ss.s_store_sk as id,
             sales, coalesce(returns,0), (profit-coalesce(profit_loss,0)) as profit
      from ss left join sr on ss.s_store_sk = sr.s_store_sk
      union all
      select 'catalog channel', cs_call_center_sk, sales, returns, (profit-profit_loss)
      from cs, cr
      union all
      select 'web channel', ws.wp_web_page_sk, sales, coalesce(returns,0),
             (profit-coalesce(profit_loss,0))
      from ws left join wr on ws.wp_web_page_sk = wr.wp_web_page_sk) x
group by rollup (channel, id)
order by channel, id
[_LIMITC];
```

</details>

<details>
<summary>MariaDB / MonetDB / PostgreSQL dialects</summary>

MariaDB uses `GROUP BY channel, id WITH ROLLUP`.
MonetDB and PostgreSQL use standard `GROUP BY ROLLUP(channel, id)`.

</details>

---

## Q78 — Store-Only Buyers vs. Other-Channel Ratios

Computes the ratio of store quantity/cost/price to web+catalog equivalents for customers
who did NOT have returns in the respective channel.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `SELECTONE` | list | column(s) used in SELECT and ORDER BY |

<details>
<summary>TPC-DS Reference SQL (query78.tpl)</summary>

```sql
with ws as (
  select d_year as ws_sold_year, ws_item_sk, ws_bill_customer_sk ws_customer_sk,
         sum(ws_quantity) ws_qty, sum(ws_wholesale_cost) ws_wc, sum(ws_sales_price) ws_sp
  from web_sales left join web_returns on wr_order_number = ws_order_number
                                       and ws_item_sk = wr_item_sk
               join date_dim on ws_sold_date_sk = d_date_sk
  where wr_order_number is null
  group by d_year, ws_item_sk, ws_bill_customer_sk),
cs as (... same for catalog_sales without returns ...),
ss as (... same for store_sales without returns ...)
[_LIMITA] select [_LIMITB]
  [SELECTONE],
  round(ss_qty/(coalesce(ws_qty,0)+coalesce(cs_qty,0)),2) ratio,
  ss_qty store_qty, ss_wc store_wholesale_cost, ss_sp store_sales_price,
  coalesce(ws_qty,0)+coalesce(cs_qty,0) other_chan_qty, ...
from ss
left join ws on (ws_sold_year = ss_sold_year and ws_item_sk = ss_item_sk and ws_customer_sk = ss_customer_sk)
left join cs on (cs_sold_year = ss_sold_year and cs_item_sk = ss_item_sk and cs_customer_sk = ss_customer_sk)
where (coalesce(ws_qty,0)>0 or coalesce(cs_qty,0)>0) and ss_sold_year = [YEAR]
order by [SELECTONE], ss_qty desc, ...
[_LIMITC];
```

</details>

---

## Q79 — Monday Store Purchases in Large Stores

Finds customers who bought on Mondays (`d_dow = 1`) in stores with 200–295 employees,
across multiple years, reporting coupon amount and net profit.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DEPCNT` | integer | 0–9 |
| `YEAR` | integer | 1998–2000 |
| `VEHCNT` | integer | -1–4 |

<details>
<summary>TPC-DS Reference SQL (query79.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  c_last_name, c_first_name, substr(s_city,1,30), ss_ticket_number, amt, profit
from (select ss_ticket_number, ss_customer_sk, store.s_city,
             sum(ss_coupon_amt) amt, sum(ss_net_profit) profit
      from store_sales, date_dim, store, household_demographics
      where store_sales.ss_sold_date_sk = date_dim.d_date_sk
        and store_sales.ss_store_sk = store.s_store_sk
        and store_sales.ss_hdemo_sk = household_demographics.hd_demo_sk
        and (household_demographics.hd_dep_count = [DEPCNT]
             or household_demographics.hd_vehicle_count > [VEHCNT])
        and date_dim.d_dow = 1
        and date_dim.d_year in ([YEAR],[YEAR]+1,[YEAR]+2)
        and store.s_number_employees between 200 and 295
      group by ss_ticket_number, ss_customer_sk, ss_addr_sk, store.s_city) ms, customer
where ss_customer_sk = c_customer_sk
order by c_last_name, c_first_name, substr(s_city,1,30), profit
[_LIMITC];
```

</details>

---

## Q80 — Channel Profit/Loss by Store/Catalog/Web Page (Rollup)

Computes sales, returns, and net profit for each channel (store, catalog, web), filtered
to items priced > $50 and not promoted via TV, with `ROLLUP` for totals.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `SALES_DATE` | date | derived: Aug 1 – Aug 30 of `{YEAR}` |

<details>
<summary>TPC-DS Reference SQL (query80.tpl)</summary>

```sql
with ssr as (
  select s_store_id as store_id, sum(ss_ext_sales_price) as sales,
         sum(coalesce(sr_return_amt,0)) as returns,
         sum(ss_net_profit - coalesce(sr_net_loss,0)) as profit
  from store_sales left outer join store_returns on (ss_item_sk = sr_item_sk and ss_ticket_number = sr_ticket_number),
       date_dim, store, item, promotion
  where ss_sold_date_sk = d_date_sk
    and d_date between '[SALES_DATE]' and '[SALES_DATE]'+30 days
    and ss_store_sk = s_store_sk and ss_item_sk = i_item_sk
    and i_current_price > 50 and ss_promo_sk = p_promo_sk and p_channel_tv = 'N'
  group by s_store_id),
csr as (... similar for catalog ...),
wsr as (... similar for web ...)
[_LIMITA] select [_LIMITB] channel, id,
  sum(sales) as sales, sum(returns) as returns, sum(profit) as profit
from (select 'store channel', 'store'||store_id, sales, returns, profit from ssr
      union all
      select 'catalog channel', 'catalog_page'||catalog_page_id, sales, returns, profit from csr
      union all
      select 'web channel', 'web_site'||web_site_id, sales, returns, profit from wsr) x
group by rollup (channel, id)
order by channel, id
[_LIMITC];
```

</details>

<details>
<summary>MariaDB / MonetDB / PostgreSQL dialects</summary>

MariaDB uses `GROUP BY channel, id WITH ROLLUP`.
MonetDB and PostgreSQL use standard `GROUP BY ROLLUP(channel, id)`.

</details>

---

## Q81 — Catalog Returns Above State Average

Analogous to Q30 (web returns) but for catalog returns — finds customers whose catalog return
total exceeds 120% of the state average in a given year.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `STATE` | list | US state codes |
| `YEAR` | integer | 1998–2002 |

<details>
<summary>TPC-DS Reference SQL (query81.tpl)</summary>

```sql
with customer_total_return as (
  select cr_returning_customer_sk as ctr_customer_sk,
         ca_state as ctr_state,
         sum(cr_return_amt_inc_tax) as ctr_total_return
  from catalog_returns, date_dim, customer_address
  where cr_returned_date_sk = d_date_sk and d_year = [YEAR]
    and cr_returning_addr_sk = ca_address_sk
  group by cr_returning_customer_sk, ca_state)
[_LIMITA] select [_LIMITB]
  c_customer_id, c_salutation, c_first_name, c_last_name,
  ca_street_number, ca_street_name, ca_street_type, ca_suite_number,
  ca_city, ca_county, ca_state, ca_zip, ca_country, ca_gmt_offset,
  ca_location_type, ctr_total_return
from customer_total_return ctr1, customer_address, customer
where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2
                                from customer_total_return ctr2
                               where ctr1.ctr_state = ctr2.ctr_state)
  and ca_address_sk = c_current_addr_sk
  and ca_state = '[STATE]'
  and ctr1.ctr_customer_sk = c_customer_sk
order by c_customer_id, c_salutation, ..., ctr_total_return
[_LIMITC];
```

</details>

---

## Q82 — In-Stock Items Sold in Store

Analogous to Q37 (catalog) but for store sales — finds items with given price range,
4 specific manufacturer IDs, 100–500 units in inventory, actually sold in-store.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `PRICE` | integer | 0–90 |
| `INVDATE` | date | derived: Jan 1 – Jul 24 of `{YEAR}` |
| `MANUFACT_ID` | integer (×4) | 4 draws from 1–1000 |

<details>
<summary>TPC-DS Reference SQL (query82.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] i_item_id, i_item_desc, i_current_price
from item, inventory, date_dim, store_sales
where i_current_price between [PRICE] and [PRICE]+30
  and inv_item_sk = i_item_sk
  and d_date_sk = inv_date_sk
  and d_date between cast('[INVDATE]' as date) and (cast('[INVDATE]' as date) + 60 days)
  and i_manufact_id in ([MANUFACT_ID.1],[MANUFACT_ID.2],[MANUFACT_ID.3],[MANUFACT_ID.4])
  and inv_quantity_on_hand between 100 and 500
  and ss_item_sk = i_item_sk
group by i_item_id, i_item_desc, i_current_price
order by i_item_id
[_LIMITC];
```

</details>

---

## Q83 — Cross-Channel Return Quantity Comparison

Computes return quantities per item for all three channels (store, catalog, web) in weeks that
contain any of three given return dates, then joins all three for items present in all channels.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `RETURNED_DATE_ONE` | date | derived: Jan 1 – Jul 24 of `{YEAR}` |
| `RETURNED_DATE_TWO` | date | derived: Aug 1 – Oct 24 of `{YEAR}` |
| `RETURNED_DATE_THREE` | date | derived: Nov 1 – Nov 24 of `{YEAR}` |

<details>
<summary>TPC-DS Reference SQL (query83.tpl)</summary>

```sql
with sr_items as (
  select i_item_id item_id, sum(sr_return_quantity) sr_item_qty
  from store_returns, item, date_dim
  where sr_item_sk = i_item_sk
    and d_date in (select d_date from date_dim
                   where d_week_seq in (select d_week_seq from date_dim
                                        where d_date in ('[RETURNED_DATE_ONE]',
                                                         '[RETURNED_DATE_TWO]',
                                                         '[RETURNED_DATE_THREE]')))
    and sr_returned_date_sk = d_date_sk
  group by i_item_id),
cr_items as (... same for catalog_returns ...),
wr_items as (... same for web_returns ...)
[_LIMITA] select [_LIMITB] sr_items.item_id,
  sr_item_qty, sr_item_qty/(sr_item_qty+cr_item_qty+wr_item_qty)/3.0*100 sr_dev,
  cr_item_qty, cr_item_qty/(sr_item_qty+cr_item_qty+wr_item_qty)/3.0*100 cr_dev,
  wr_item_qty, wr_item_qty/(sr_item_qty+cr_item_qty+wr_item_qty)/3.0*100 wr_dev,
  (sr_item_qty+cr_item_qty+wr_item_qty)/3.0 average
from sr_items, cr_items, wr_items
where sr_items.item_id = cr_items.item_id and sr_items.item_id = wr_items.item_id
order by sr_items.item_id, sr_item_qty
[_LIMITC];
```

</details>

---

## Q84 — Customers in a City with Store Returns and Income Band

Finds customers living in a specific city with income in a $50,000 range who have made store
returns, using concatenation for the customer name output.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `CITY` | list | from large cities distribution |
| `INCOME` | integer | 0–70000 |

<details>
<summary>TPC-DS Reference SQL (query84.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] c_customer_id as customer_id,
       coalesce(c_last_name,'')||', '||coalesce(c_first_name,'') as customername
from customer, customer_address, customer_demographics, household_demographics,
     income_band, store_returns
where ca_city = '[CITY]'
  and c_current_addr_sk = ca_address_sk
  and ib_lower_bound >= [INCOME]
  and ib_upper_bound <= [INCOME] + 50000
  and ib_income_band_sk = hd_income_band_sk
  and cd_demo_sk = c_current_cdemo_sk
  and hd_demo_sk = c_current_hdemo_sk
  and sr_cdemo_sk = cd_demo_sk
order by c_customer_id
[_LIMITC];
```

</details>

<details>
<summary>MariaDB / MonetDB / PostgreSQL dialects</summary>

The string concatenation `coalesce(c_last_name,'')||', '||coalesce(c_first_name,'')` is standard SQL.
The bexhoma MariaDB variant uses `CONCAT()` instead of `||`.

</details>

---

## Q85 — Web Return Reason Analysis by Demographics

Reports average return quantities, refund cash, and fees by return reason, filtered by
demographic groups (marital status × education × price range) and state/profit combinations.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `MS` | list (×3) | 3 draws from marital status — substituted as `{MS.1}`…`{MS.3}` |
| `ES` | list (×3) | 3 draws from education — substituted as `{ES.1}`…`{ES.3}` |
| `STATE` | list (×9) | 9 draws from state codes — substituted as `{STATE.1}`…`{STATE.9}` |
| `YEAR` | integer | 1998–2002 |

<details>
<summary>TPC-DS Reference SQL (query85.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  substr(r_reason_desc,1,20), avg(ws_quantity), avg(wr_refunded_cash), avg(wr_fee)
from web_sales, web_returns, web_page, customer_demographics cd1,
     customer_demographics cd2, customer_address, date_dim, reason
where ws_web_page_sk = wp_web_page_sk
  and ws_item_sk = wr_item_sk and ws_order_number = wr_order_number
  and ws_sold_date_sk = d_date_sk and d_year = [YEAR]
  and cd1.cd_demo_sk = wr_refunded_cdemo_sk and cd2.cd_demo_sk = wr_returning_cdemo_sk
  and ca_address_sk = wr_refunded_addr_sk
  and r_reason_sk = wr_reason_sk
  and ((cd1.cd_marital_status = '[MS.1]' and cd1.cd_marital_status = cd2.cd_marital_status
        and cd1.cd_education_status = '[ES.1]' and cd1.cd_education_status = cd2.cd_education_status
        and ws_sales_price between 100.00 and 150.00)
    or (cd1.cd_marital_status = '[MS.2]' and ... and ws_sales_price between 50.00 and 100.00)
    or (cd1.cd_marital_status = '[MS.3]' and ... and ws_sales_price between 150.00 and 200.00))
  and ((ca_country = 'United States' and ca_state in ('[STATE.1]','[STATE.2]','[STATE.3]')
        and ws_net_profit between 100 and 200)
    or (... '[STATE.4]'–'[STATE.6]' and profit between 150 and 300)
    or (... '[STATE.7]'–'[STATE.9]' and profit between 50 and 250))
group by r_reason_desc
order by substr(r_reason_desc,1,20), avg(ws_quantity), avg(wr_refunded_cash), avg(wr_fee)
[_LIMITC];
```

</details>

---

## Q86 — Web Net Paid Rollup by Category and Class

Ranks web sales net paid within each category using `ROLLUP` over category and class,
producing subtotals and grand total.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1224 |

<details>
<summary>TPC-DS Reference SQL (query86.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  sum(ws_net_paid) as total_sum, i_category, i_class,
  grouping(i_category)+grouping(i_class) as lochierarchy,
  rank() over (partition by grouping(i_category)+grouping(i_class),
               case when grouping(i_class) = 0 then i_category end
               order by sum(ws_net_paid) desc) as rank_within_parent
from web_sales, date_dim d1, item
where d1.d_month_seq between [DMS] and [DMS]+11
  and d1.d_date_sk = ws_sold_date_sk
  and i_item_sk = ws_item_sk
group by rollup(i_category, i_class)
order by lochierarchy desc,
         case when lochierarchy = 0 then i_category end,
         rank_within_parent
[_LIMITC];
```

</details>

<details>
<summary>MariaDB / MonetDB / PostgreSQL dialects</summary>

MariaDB uses `GROUP BY i_category, i_class WITH ROLLUP`.
MonetDB and PostgreSQL use standard `GROUP BY ROLLUP(i_category, i_class)`.

</details>

---

## Q87 — Store-Only Customers (EXCEPT Catalog and Web)

Counts customers who purchased in-store but not via catalog and not via web in a given
12-month period, using set difference (`EXCEPT`).

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1224 |

<details>
<summary>TPC-DS Reference SQL (query87.tpl)</summary>

```sql
select count(*)
from ((select distinct c_last_name, c_first_name, d_date
       from store_sales, date_dim, customer
       where store_sales.ss_sold_date_sk = date_dim.d_date_sk
         and store_sales.ss_customer_sk = customer.c_customer_sk
         and d_month_seq between [DMS] and [DMS]+11)
       except
      (select distinct c_last_name, c_first_name, d_date
       from catalog_sales, date_dim, customer
       where catalog_sales.cs_sold_date_sk = date_dim.d_date_sk
         and catalog_sales.cs_bill_customer_sk = customer.c_customer_sk
         and d_month_seq between [DMS] and [DMS]+11)
       except
      (select distinct c_last_name, c_first_name, d_date
       from web_sales, date_dim, customer
       where web_sales.ws_sold_date_sk = date_dim.d_date_sk
         and web_sales.ws_bill_customer_sk = customer.c_customer_sk
         and d_month_seq between [DMS] and [DMS]+11)
) cool_cust;
```

</details>

---

## Q88 — Hourly Store Purchase Counts (Pivot by 30-Min Window)

Returns 8 counts (one per 30-minute window from 8:30 AM to 12:30 PM) for customers with
specific dependent-count and vehicle-count households, all in one cross-product row.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `HOUR` | integer (×3) | 3 draws from -1–4 (used as `hd_dep_count` values) |
| `STORE` | list | from store names distribution |

<details>
<summary>TPC-DS Reference SQL (query88.tpl)</summary>

```sql
select *
from (select count(*) h8_30_to_9 from store_sales, household_demographics, time_dim, store
      where ss_sold_time_sk = time_dim.t_time_sk and ss_hdemo_sk = household_demographics.hd_demo_sk
        and ss_store_sk = s_store_sk and time_dim.t_hour = 8 and time_dim.t_minute >= 30
        and (... hd_dep_count in ({HOUR.1},{HOUR.2},{HOUR.3} with vehicle_count ...) ...)
        and store.s_store_name = 'ese') s1,
     (select count(*) h9_to_9_30 ... t_hour = 9 and t_minute < 30 ...) s2,
     (select count(*) h9_30_to_10 ... t_hour = 9 and t_minute >= 30 ...) s3,
     (select count(*) h10_to_10_30 ... t_hour = 10 and t_minute < 30 ...) s4,
     (select count(*) h10_30_to_11 ... t_hour = 10 and t_minute >= 30 ...) s5,
     (select count(*) h11_to_11_30 ... t_hour = 11 and t_minute < 30 ...) s6,
     (select count(*) h11_30_to_12 ... t_hour = 11 and t_minute >= 30 ...) s7,
     (select count(*) h12_to_12_30 ... t_hour = 12 and t_minute < 30 ...) s8;
```

</details>

---

## Q89 — Monthly Sales Deviation by Category and Brand

Finds store items where a month's sales deviate more than 10% from the brand's monthly
average, using window function `AVG(SUM(...)) OVER (PARTITION BY ...)`.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `CAT_A`…`CAT_F` | list (×6) | 6 draws of category+class pairs |
| `CLASS_A`…`CLASS_F` | list (×6) | matching class draws |

<details>
<summary>TPC-DS Reference SQL (query89.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] *
from (select i_category, i_class, i_brand, s_store_name, s_company_name, d_moy,
             sum(ss_sales_price) sum_sales,
             avg(sum(ss_sales_price)) over
               (partition by i_category, i_brand, s_store_name, s_company_name) avg_monthly_sales
      from item, store_sales, date_dim, store
      where ss_item_sk = i_item_sk and ss_sold_date_sk = d_date_sk
        and ss_store_sk = s_store_sk and d_year in ([YEAR])
        and ((i_category in ('[CAT_A]','[CAT_B]','[CAT_C]')
              and i_class in ('[CLASS_A]','[CLASS_B]','[CLASS_C]'))
          or (i_category in ('[CAT_D]','[CAT_E]','[CAT_F]')
              and i_class in ('[CLASS_D]','[CLASS_E]','[CLASS_F]')))
      group by i_category, i_class, i_brand, s_store_name, s_company_name, d_moy) tmp1
where case when (avg_monthly_sales <> 0)
           then (abs(sum_sales - avg_monthly_sales) / avg_monthly_sales)
           else null end > 0.1
order by sum_sales - avg_monthly_sales, s_store_name
[_LIMITC];
```

</details>

---

## Q90 — AM vs. PM Web Sales Ratio

Computes the ratio of web sales counts in a morning hour window to an afternoon hour window,
for customers with a specific dependent count and high-character-count web pages.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DEPCNT` | integer | 0–9 |
| `HOUR_AM` | integer | 6–12 |
| `HOUR_PM` | integer | 13–21 |

<details>
<summary>TPC-DS Reference SQL (query90.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  cast(amc as decimal(15,4))/cast(pmc as decimal(15,4)) am_pm_ratio
from (select count(*) amc
      from web_sales, household_demographics, time_dim, web_page
      where ws_sold_time_sk = time_dim.t_time_sk
        and ws_ship_hdemo_sk = household_demographics.hd_demo_sk
        and ws_web_page_sk = web_page.wp_web_page_sk
        and time_dim.t_hour between [HOUR_AM] and [HOUR_AM]+1
        and household_demographics.hd_dep_count = [DEPCNT]
        and web_page.wp_char_count between 5000 and 5200) at,
     (select count(*) pmc
      from web_sales, household_demographics, time_dim, web_page
      where ws_sold_time_sk = time_dim.t_time_sk
        and ws_ship_hdemo_sk = household_demographics.hd_demo_sk
        and ws_web_page_sk = web_page.wp_web_page_sk
        and time_dim.t_hour between [HOUR_PM] and [HOUR_PM]+1
        and household_demographics.hd_dep_count = [DEPCNT]
        and web_page.wp_char_count between 5000 and 5200) pt
order by am_pm_ratio
[_LIMITC];
```

</details>

---

## Q91 — Call Center Returns Loss by Manager

Sums catalog return net losses by call center manager, filtered by customer demographics
(marital status + education), buy potential, and GMT offset month.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `MONTH` | integer | 11–12 |
| `BUY_POTENTIAL` | list | 1001–5000, >10000, 501–1000, 0–500, Unknown, 5001–10000 |
| `GMT` | list | `-6`, `-7` |

<details>
<summary>TPC-DS Reference SQL (query91.tpl)</summary>

```sql
select cc_call_center_id call_center, cc_name call_center_name,
       cc_manager manager, sum(cr_net_loss) returns_loss
from call_center, catalog_returns, date_dim, customer,
     customer_address, customer_demographics, household_demographics
where cr_call_center_sk = cc_call_center_sk
  and cr_returned_date_sk = d_date_sk
  and cr_returning_customer_sk = c_customer_sk
  and cd_demo_sk = c_current_cdemo_sk
  and hd_demo_sk = c_current_hdemo_sk
  and ca_address_sk = c_current_addr_sk
  and d_year = [YEAR] and d_moy = [MONTH]
  and ((cd_marital_status = 'M' and cd_education_status = 'Unknown')
    or (cd_marital_status = 'W' and cd_education_status = 'Advanced Degree'))
  and hd_buy_potential like '[BUY_POTENTIAL]%'
  and ca_gmt_offset = [GMT]
group by cc_call_center_id, cc_name, cc_manager, cd_marital_status, cd_education_status
order by sum(cr_net_loss) desc;
```

</details>

---

## Q92 — Web Items with Excess Discount Amount

Finds web sales where the discount amount exceeds 1.3x the average for that item, in a
90-day window, for a specific manufacturer.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `IMID` | integer | 1–1000 (manufacturer ID) |
| `YEAR` | integer | 1998–2002 |
| `WSDATE` | date | derived: Jan 1 – Apr 1 of `{YEAR}` |

<details>
<summary>TPC-DS Reference SQL (query92.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] sum(ws_ext_discount_amt) as "Excess Discount Amount"
from web_sales, item, date_dim
where i_manufact_id = [IMID]
  and i_item_sk = ws_item_sk
  and d_date between '[WSDATE]' and (cast('[WSDATE]' as date) + 90 days)
  and d_date_sk = ws_sold_date_sk
  and ws_ext_discount_amt > (select 1.3 * avg(ws_ext_discount_amt)
                              from web_sales, date_dim
                              where ws_item_sk = i_item_sk
                                and d_date between '[WSDATE]'
                                              and (cast('[WSDATE]' as date) + 90 days)
                                and d_date_sk = ws_sold_date_sk)
order by sum(ws_ext_discount_amt)
[_LIMITC];
```

</details>

---

## Q93 — Customer Net Sales After Returns by Reason

Computes effective net sales per customer (quantity minus returns, times price), for
store returns with a specific return reason.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `REASON` | list | from return reasons distribution |

<details>
<summary>TPC-DS Reference SQL (query93.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] ss_customer_sk, sum(act_sales) sumsales
from (select ss_item_sk, ss_ticket_number, ss_customer_sk,
             case when sr_return_quantity is not null
                  then (ss_quantity - sr_return_quantity) * ss_sales_price
                  else (ss_quantity * ss_sales_price) end act_sales
      from store_sales left outer join store_returns
             on (sr_item_sk = ss_item_sk and sr_ticket_number = ss_ticket_number),
           reason
      where sr_reason_sk = r_reason_sk and r_reason_desc = '[REASON]') t
group by ss_customer_sk
order by sumsales, ss_customer_sk
[_LIMITC];
```

</details>

---

## Q94 — Multi-Warehouse Web Orders Not Returned

Counts distinct web orders that shipped from more than one warehouse and were never returned,
using `EXISTS`/`NOT EXISTS` correlated subqueries.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1999–2002 |
| `MONTH` | integer | 2–5 |
| `STATE` | list | US state codes |

<details>
<summary>TPC-DS Reference SQL (query94.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  count(distinct ws_order_number) as "order count",
  sum(ws_ext_ship_cost) as "total shipping cost",
  sum(ws_net_profit) as "total net profit"
from web_sales ws1, date_dim, customer_address, web_site
where d_date between '[YEAR]-[MONTH]-01' and (cast('[YEAR]-[MONTH]-01' as date) + 60 days)
  and ws1.ws_ship_date_sk = d_date_sk
  and ws1.ws_ship_addr_sk = ca_address_sk
  and ca_state = '[STATE]'
  and ws1.ws_web_site_sk = web_site_sk
  and web_company_name = 'pri'
  and exists (select * from web_sales ws2
              where ws1.ws_order_number = ws2.ws_order_number
                and ws1.ws_warehouse_sk <> ws2.ws_warehouse_sk)
  and not exists (select * from web_returns wr1
                  where ws1.ws_order_number = wr1.wr_order_number)
order by count(distinct ws_order_number)
[_LIMITC];
```

</details>

---

## Q95 — Multi-Warehouse Web Orders With Returns (CTE Variant)

Same as Q94 but with returns included, using a CTE to find multi-warehouse order numbers
and then joining back to filter with those order numbers.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1999–2002 |
| `MONTH` | integer | 2–5 |
| `STATE` | list | US state codes |

<details>
<summary>TPC-DS Reference SQL (query95.tpl)</summary>

```sql
with ws_wh as (
  select ws1.ws_order_number, ws1.ws_warehouse_sk wh1, ws2.ws_warehouse_sk wh2
  from web_sales ws1, web_sales ws2
  where ws1.ws_order_number = ws2.ws_order_number
    and ws1.ws_warehouse_sk <> ws2.ws_warehouse_sk)
[_LIMITA] select [_LIMITB]
  count(distinct ws_order_number) as "order count",
  sum(ws_ext_ship_cost) as "total shipping cost",
  sum(ws_net_profit) as "total net profit"
from web_sales ws1, date_dim, customer_address, web_site
where d_date between '[YEAR]-[MONTH]-01' and (cast('[YEAR]-[MONTH]-01' as date) + 60 days)
  and ws1.ws_ship_date_sk = d_date_sk
  and ws1.ws_ship_addr_sk = ca_address_sk
  and ca_state = '[STATE]'
  and ws1.ws_web_site_sk = web_site_sk
  and web_company_name = 'pri'
  and ws1.ws_order_number in (select ws_order_number from ws_wh)
  and ws1.ws_order_number in (select wr_order_number from web_returns, ws_wh
                               where wr_order_number = ws_wh.ws_order_number)
order by count(distinct ws_order_number)
[_LIMITC];
```

</details>

---

## Q96 — Store Sales Count in Late Evening Hour

Counts store sales in a specific late-hour 30-minute window (minute ≥ 30) for customers
with a given dependent count, in the store named 'ese'.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `HOUR` | list | 20, 15, 16, 8 |
| `DEPCNT` | integer | 0–9 |

<details>
<summary>TPC-DS Reference SQL (query96.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB] count(*)
from store_sales, household_demographics, time_dim, store
where ss_sold_time_sk = time_dim.t_time_sk
  and ss_hdemo_sk = household_demographics.hd_demo_sk
  and ss_store_sk = s_store_sk
  and time_dim.t_hour = [HOUR]
  and time_dim.t_minute >= 30
  and household_demographics.hd_dep_count = [DEPCNT]
  and store.s_store_name = 'ese'
order by count(*)
[_LIMITC];
```

</details>

---

## Q97 — Store vs. Catalog Overlap via Full Outer Join

Counts customers/items that appear in only store sales, only catalog sales, or both,
in a 12-month period using a `FULL OUTER JOIN` of two aggregated CTEs.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1224 |

<details>
<summary>TPC-DS Reference SQL (query97.tpl)</summary>

```sql
with ssci as (
  select ss_customer_sk customer_sk, ss_item_sk item_sk
  from store_sales, date_dim
  where ss_sold_date_sk = d_date_sk and d_month_seq between [DMS] and [DMS]+11
  group by ss_customer_sk, ss_item_sk),
csci as (
  select cs_bill_customer_sk customer_sk, cs_item_sk item_sk
  from catalog_sales, date_dim
  where cs_sold_date_sk = d_date_sk and d_month_seq between [DMS] and [DMS]+11
  group by cs_bill_customer_sk, cs_item_sk)
[_LIMITA] select [_LIMITB]
  sum(case when ssci.customer_sk is not null and csci.customer_sk is null then 1 else 0 end) store_only,
  sum(case when ssci.customer_sk is null and csci.customer_sk is not null then 1 else 0 end) catalog_only,
  sum(case when ssci.customer_sk is not null and csci.customer_sk is not null then 1 else 0 end) store_and_catalog
from ssci full outer join csci on (ssci.customer_sk = csci.customer_sk
                                   and ssci.item_sk = csci.item_sk)
[_LIMITC];
```

</details>

<details>
<summary>MySQL / MariaDB dialect</summary>

MySQL and MariaDB do not support `FULL OUTER JOIN`. The bexhoma implementation
rewrites this as a `UNION ALL` of left and right joins:

```sql
select
  sum(case when ssci.customer_sk is not null and csci.customer_sk is null then 1 else 0 end) store_only,
  sum(case when ssci.customer_sk is null and csci.customer_sk is not null then 1 else 0 end) catalog_only,
  sum(case when ssci.customer_sk is not null and csci.customer_sk is not null then 1 else 0 end) store_and_catalog
from (
  select ssci.customer_sk, ssci.item_sk, csci.customer_sk as c_customer_sk, csci.item_sk as c_item_sk
  from ssci left join csci on (ssci.customer_sk = csci.customer_sk and ssci.item_sk = csci.item_sk)
  union all
  select ssci.customer_sk, ssci.item_sk, csci.customer_sk, csci.item_sk
  from csci left join ssci on (ssci.customer_sk = csci.customer_sk and ssci.item_sk = csci.item_sk)
  where ssci.customer_sk is null) combined;
```

</details>

---

## Q98 — Item Revenue Share Within Class

Reports each item's revenue and its percentage share of the class-level total, using a
window function, for 3 item categories in a 30-day window.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `YEAR` | integer | 1998–2002 |
| `SDATE` | date | derived: Jan 1 – Jul 1 of `{YEAR}` |
| `CATEGORY` | list (×3) | 3 draws from categories |

<details>
<summary>TPC-DS Reference SQL (query98.tpl)</summary>

```sql
select i_item_id, i_item_desc, i_category, i_class, i_current_price,
       sum(ss_ext_sales_price) as itemrevenue,
       sum(ss_ext_sales_price)*100/sum(sum(ss_ext_sales_price)) over
           (partition by i_class) as revenueratio
from store_sales, item, date_dim
where ss_item_sk = i_item_sk
  and i_category in ('[CATEGORY.1]','[CATEGORY.2]','[CATEGORY.3]')
  and ss_sold_date_sk = d_date_sk
  and d_date between cast('[SDATE]' as date) and (cast('[SDATE]' as date) + 30 days)
group by i_item_id, i_item_desc, i_category, i_class, i_current_price
order by i_category, i_class, i_item_id, i_item_desc, revenueratio;
```

</details>

---

## Q99 — Catalog Shipping Latency Pivot by Warehouse, Mode, and Call Center

Pivots catalog order shipping latency into 5 buckets (≤30 days, 31–60, 61–90, 91–120, >120)
per warehouse × ship mode × call center combination.

| Parameter | Type | Range / Values |
|-----------|------|---------------|
| `DMS` | integer | 1176–1224 |

<details>
<summary>TPC-DS Reference SQL (query99.tpl)</summary>

```sql
[_LIMITA] select [_LIMITB]
  substr(w_warehouse_name,1,20), sm_type, cc_name,
  sum(case when (cs_ship_date_sk - cs_sold_date_sk <= 30) then 1 else 0 end) as "30 days",
  sum(case when (cs_ship_date_sk - cs_sold_date_sk > 30)
            and (cs_ship_date_sk - cs_sold_date_sk <= 60) then 1 else 0 end) as "31-60 days",
  sum(case when (cs_ship_date_sk - cs_sold_date_sk > 60)
            and (cs_ship_date_sk - cs_sold_date_sk <= 90) then 1 else 0 end) as "61-90 days",
  sum(case when (cs_ship_date_sk - cs_sold_date_sk > 90)
            and (cs_ship_date_sk - cs_sold_date_sk <= 120) then 1 else 0 end) as "91-120 days",
  sum(case when (cs_ship_date_sk - cs_sold_date_sk > 120) then 1 else 0 end) as ">120 days"
from catalog_sales, warehouse, ship_mode, call_center, date_dim
where d_month_seq between [DMS] and [DMS]+11
  and cs_ship_date_sk = d_date_sk
  and cs_warehouse_sk = w_warehouse_sk
  and cs_ship_mode_sk = sm_ship_mode_sk
  and cs_call_center_sk = cc_call_center_sk
group by substr(w_warehouse_name,1,20), sm_type, cc_name
order by substr(w_warehouse_name,1,20), sm_type, cc_name
[_LIMITC];
```

</details>

---

