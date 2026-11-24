# TPC-DS: result comparison across DBMS (record, moved from docs/Queries-TPC-DS.md)

## Result Comparison Across DBMS (SF=3)

All 99 queries were run at SF=3 on PostgreSQL, MySQL, MariaDB, MonetDB, ClickHouse and
ClickHouseCluster in one experiment (the DBMS the `tpcds` command supports; Citus and PgDuckDB have no
TPC-DS path, CedarDB and DatabaseService are not available), timeout 900 s. Query parameters are drawn
once per experiment, so only results of the same experiment are comparable. The stored result sets were
compared with numbers rounded to two decimals and rows compared as a multiset.

**First comparison: 74 of 99 queries identical on all six systems. After the changes below: 94 of 99, and 97
of 99 once the three MariaDB timeouts were fixed (Q72, Q94, Q95 were then checked in a separate experiment on
PostgreSQL, MariaDB, MySQL, MonetDB and ClickHouse, which returned identical results).**
The two that still differ:

| Query | Systems | Cause |
|-------|---------|-------|
| Q75 | ClickHouse, ClickHouseCluster | A rounded sum differs by 1 (float against decimal summation at a `.5` boundary) |
| Q56 | MySQL, MariaDB, MonetDB vs. PostgreSQL, ClickHouse | `total_sales` can be NULL and the systems sort NULL first or last. Fixed afterwards with `NULLS FIRST` for PostgreSQL and ClickHouse: Q33 and Q56 identical on all seven DBMS with 5 parameter sets at SF 1 |

Q67 differed on MonetDB in an earlier run (rows near the `LIMIT` boundary); it agreed in the final run and the
cause was not isolated.

### How the results are compared

The comparison is done by dbmsbenchmarker (`tools.py` and `benchmarker.py`), not by TPC answer sets:

- **Normalisation per run:** every cell is converted to a string and stripped. With `sorted: True` (set for all 99
  queries) numbers are rounded to the `precision` of the queries config (**0 decimals for all TPC-DS queries**) and
  the rows are sorted by all columns. Row order is therefore irrelevant; only the rows that pass the `LIMIT` count.
- **Comparison across systems:** the merge step rounds again to 2 decimals (hard-coded), sorts, and compares each
  connection with the **first** connection (the reference) by concatenating the two result tables and dropping
  duplicates. A connection is flagged if either side has rows the other lacks.
- **What this does not detect:** differences smaller than the rounding (an average of 25.4 against 25.1 is equal at
  0 decimals), the order of the rows (so a wrong `ORDER BY` is not found), and rows that appear twice on one side and
  not at all on the other.
- **What it flags without a real difference:** values at a rounding boundary (25.4999 against 25.5), a different
  column title (ClickHouse labels a qualified column `D1.D_WEEK_SEQ`), and `''` against NULL. A failed reference
  connection flags all others.

### What made the systems agree

| Cause | Queries | Change |
|-------|---------|--------|
| NULL sorts first in MySQL, MariaDB and MonetDB and last in PostgreSQL and ClickHouse, so `LIMIT` kept different rows | Q20, Q27, Q33, Q56, Q67, Q74, Q76, Q99 | `ORDER BY col is not null, col` (Q74 orders by a `CASE` over its three key columns); Q33 and Q56 `NULLS FIRST` for PostgreSQL and ClickHouse |
| ClickHouse returned `''` instead of `NULL` for subtotal keys of `ROLLUP` | Q5, Q18, Q67, Q77, Q80 | `group_by_use_nulls = 1` in the ClickHouse deployment profile |
| ClickHouse truncates `Decimal` division, MonetDB rounds `DECIMAL` division and averages to two decimals | Q7, Q12, Q18, Q20, Q26, Q31, Q36, Q44, Q58, Q66, Q98 | Numerator or average computed as `double` (`+ 0.0e0`, `toFloat64`, `cast(… as double)`), partly as MonetDB or ClickHouse overrides |
| Integer division in PostgreSQL and MonetDB | Q78 | `ss_qty*1.0/…` |
| `2.0/3.0` is a decimal in MonetDB and `FLOAT` is single precision in MySQL, so rows at the boundary of the ratio test were taken or left out (SF=1 comparison of PostgreSQL, MonetDB, MySQL and MariaDB, 2026-11-06) | Q21 | Test in integers: `3*inv_after >= 2*inv_before and 2*inv_after <= 3*inv_before` |
| MonetDB rounds `DECIMAL` division and averages to two decimals, same comparison | Q31, Q47, Q53, Q57, Q63, Q66, Q89 | `+ 0.0e0` on the numerator or inside the average (Q63 differed in the 2026-11-06 comparison; Q53, Q57, Q89 have the same shape) |
| NULL last names sort first in MySQL, MariaDB and MonetDB and last in PostgreSQL; ties at the `LIMIT` boundary, same comparison | Q68 | `c_last_name IS NOT NULL, c_last_name`, then a total order |
| `DESC` puts NULL first in PostgreSQL and last in MySQL, MariaDB and MonetDB, same comparison | Q78 | `ss_qty IS NULL, ss_qty DESC` and the same for `ss_wc`, `ss_sp` |
| Every store in the generated data is in TN, so random states gave an empty result | Q27, Q36 | `'TN'` is always part of the state list |
| `\|\|` is logical OR in MySQL and MariaDB, so the ids were 0 or 1 | Q80 | `concat()` in the MariaDB variant and a new MySQL variant |
| MariaDB has no `GROUPING()`: real NULL categories were taken for subtotals, and Q27 had no `ORDER BY` | Q27, Q36, Q86 | Sentinel for real NULLs before the rollup; wrapped rollup with an outer `ORDER BY` |
| MonetDB rollup emulation: grand-total rank NULL, subtotal ranks per state | Q70 | Rank 1 for the grand total, subtotal ranks across all states |
| MariaDB did not finish within 900 s: no decorrelation of `EXISTS` (Q94), a self join of `web_sales` (Q95), a join order starting at the 28M-row `inventory` (Q72) | Q72, Q94, Q95 | MariaDB overrides: `IN` over `GROUP BY … HAVING`, forced join order |
| PostgreSQL, MySQL and MariaDB order strings by their own locale or collation | Q65, Q99 | Bytewise collation in the deployment templates (`--locale=C`, `utf8mb4_bin`) |

The collation change applies to every benchmark that uses these deployment templates and takes effect for newly
initialised data directories.

---

