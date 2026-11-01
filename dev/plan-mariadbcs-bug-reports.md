# Plan: report the MariaDB ColumnStore bugs to MariaDB

Status: **plan only (2026-11-01).** Nothing written, nothing filed.

Goal: every problem found in #827 that is a bug of ColumnStore goes to MariaDB as its own ticket, with a
script that runs on a plain install, so that the maintainers can reproduce it without TPC-DS or bexhoma.

Scope: MariaDB Community Server 12.3.3 with ColumnStore 25.10.6, single node.
The bexhoma side is done: the query variants work around all of this, see
[docs/DBMS.md](../docs/DBMS.md#mariadb-columnstore) and [docs/Queries-TPC-DS.md](../docs/Queries-TPC-DS.md).

Related: [plan-result-comparison](plan-result-comparison.md), issue #827.

---

## 1. Decisions (defaults unless the user decides otherwise)

| # | Decision |
|---|---|
| D1 | Tickets go to the Jira of MariaDB (https://jira.mariadb.org), project `MCOL`, type Bug. |
| D2 | One ticket per bug. A bug with an own fix should not wait for the others. |
| D3 | The user files them from their account. The plan only prepares the texts. |
| D4 | Each ticket has a standalone SQL script. No TPC-DS data, no bexhoma, no Kubernetes. |
| D5 | The expected result comes from InnoDB, same script, same server. |
| D6 | A ticket states what was observed. Where the bug lives is for the maintainers to say. |
| D7 | No timings and no benchmark results in a ticket. |

## 2. Bugs

Order: silent wrong results first, since nobody notices them; the crash next, then the rest.

| # | Report | Kind | TPC-DS | Repro today | Workaround in bexhoma |
|---|---|---|---|---|---|
| B1 | `WHERE` on a CTE reaches its window functions | Wrong result, no error | Q47, Q57 | Minimal, needs `date_dim` | `lag()`/`lead()` in the CTE, filter as `HAVING` |
| B2 | `GROUP BY ... WITH ROLLUP` on a derived table gives wrong rows | Wrong result, no error | Q18, Q22, Q27, Q36, Q67, Q70, Q86 | Only on TPC-DS | Rollup emulated |
| B3 | `LEFT JOIN` with a filter on the outer table in `WHERE` keeps rows without a match | Wrong result, no error | Q93 | Only on TPC-DS | Inner joins |
| B4 | Join on a computed key with a small derived table gives no rows | Wrong result, no error | Q72 | Reduced, on `date_dim` | CTE `date_pairs` |
| B5 | Self join of several instances of a CTE mixes them up | Wrong result, no error | Q47, Q57 | Only on TPC-DS | `lag()`/`lead()` in the CTE |
| B6 | `GROUP BY ... WITH ROLLUP` directly on a table kills `PrimProc` | Crash | Q18, Q22, Q27, Q36, Q67, Q70, Q86 | Reduced, backtrace available | Rollup emulated |
| B7 | `cpuset.cpus` empty in the cgroup means one core | Performance | all | One pod is enough | Copy of the cgroup with the cores |

Observations so far, on TPC-DS SF 1 unless stated:

- **B1:** `with v as (select d_moy, d_dom, count(*) over (partition by d_moy) c from date_dim where d_year = 2000) select count(*), max(c) from v where d_dom <= 2` gives `max(c)` 2, expected 31. `LIMIT` in the CTE, `d_year + 0` and `condition_pushdown_for_derived=off` did not help. An outer `HAVING` did.
- **B2:** Q27 shows several rows with a `NULL` state for one item, Q22 rows with only `NULL`, Q70 has 5 rows instead of 4. Q5 and Q80 have a rollup on a CTE and were correct, so the condition is narrower than "a derived table".
- **B3:** Q93 gives 90,919 groups instead of 7,164.
- **B4:** `date_dim d1 join (select -1 as k union all select 0 union all select 1) off on (1=1) join date_dim d2 on d2.d_date_sk = d1.d_date_sk + off.k and d2.d_week_seq = d1.d_week_seq where d1.d_year = 2000` counts 0, expected 994. Without the second join it is refused with `MCS-1000`.
- **B5:** with `v1, v1 v1_lag, v1 v1_lead` joined on `rn`, `nsum` equals `sum_sales`. A join of two instances is correct.
- **B6:** `select inv_item_sk, inv_warehouse_sk, count(*) from inventory where inv_item_sk <= 1 group by inv_item_sk, inv_warehouse_sk with rollup` kills `PrimProc` (1,305 rows). `SIGSEGV` in `funcexp::FuncExp::evaluate` on a thread `BPPFE2`, reached by a `FairThreadPool` thread. It does not depend on the core count or on `RowAggrThreads`. A table with 3 rows, and `item` with 18,000 rows and string keys, do not show it.
- **B7:** with `SystemConfig CGroup` set to `.`, 35 instead of 324 threads in `PrimProc`, and `FairThreadPool` starts 2 threads. Is a ticket only if the setting is meant to be used in containers, see open points.

Not to report:

- `INTERSECT`, `EXCEPT`: known, MCOL-5598.
- `MCS-1000`, `MCS-3022`, `MCS-3033`, `MCS-3016`, `MCS-3013`, `MCS-2061`, `MCS-1001`: documented or at least clear limits.
- `ERROR 1030` with concurrent `LOAD DATA` into a table: documented that loads of a table block each other. The error instead of waiting may be worth a question, see open points.
- Q33, Q56: fixed in bexhoma, the reference query and `NULLS FIRST` for PostgreSQL and ClickHouse. ColumnStore refusing `ORDER BY total_sales IS NOT NULL` was right.

## 3. Check for duplicates

Done once by text search in `MCOL`, keywords only, so each ticket gets its own search right before filing.

| Ticket | Why it matters |
|---|---|
| MCOL-4570 | Filter on a subquery with a window function gives wrong results, fixed in 6.3.1. B1 looks like the same or a regression. Link it. |
| MCOL-678 | `WITH ROLLUP` support, closed in 23.10.1. So B2 and B6 are bugs of a supported feature. |
| MCOL-5430, MCOL-6328 | Window functions with `GROUP BY`, wrong results and a crash. Compare with B1 and B5. |
| MCOL-5842 | CTE and aggregates, wrong results. Compare with B5. |
| MCOL-5581 | `LEFT OUTER JOIN` with `WHERE`, wrong result. Compare with B3. |
| MCOL-5667 | `WITH ROLLUP` for cross-engine joins, not the same. |
| MDEV-39868 | Window function over a merged derived table, a server bug. Check it for B1. |

## 4. Milestones

### M0. Environment

Local Docker, no cluster: the start script of `k8s/deploymenttemplate-MariaDBCS.yml` on `mariadb:12.3.3`.
A second container on `mariadb:11.8` gives the older version (M3).

### M1. Standalone scripts

One file per bug, in `dev/mariadbcs-bugs/b<N>.sql`:

- `CREATE TABLE`, rows by `INSERT` or `seq_` of the Sequence engine, the query, the expected result as a comment.
- The engine as the only difference: `ENGINE=ColumnStore` or `ENGINE=InnoDB`.
- As small as it goes. B2, B3 and B5 are not reduced yet, and a small table may hide them, as with B6. Then the script generates the rows.

B6: find the smallest table that crashes, and why `item` does not.

### M2. Run

Each script on both engines, three times. A bug stays in the plan only if ColumnStore differs from InnoDB every time, or crashes every time.
A script that does not reproduce goes back to M1. If it stays that way, the ticket gets the TPC-DS data generator and the query, or it is dropped.

### M3. Versions

Each script on the newest released plugin and on 11.8, so a ticket can say if 12.3 is special.
If a newer release fixes a bug, no ticket, and a note in `docs/DBMS.md` that the variant may go.

### M4. Tickets

One text per bug in `dev/mariadbcs-bugs/b<N>.md`, for review by the user:

```markdown
**Summary:** <one line>
**Version:** ColumnStore 25.10.6, MariaDB 12.3.3, Ubuntu 24.04, single node
**Steps:** attached script
**Expected (InnoDB):** ...
**Actual (ColumnStore):** ...
**Notes:** log or backtrace, workaround, related tickets
```

B6 also gets the backtrace: start `PrimProc -f` under `gdb`, attaching is refused in a pod.

### M5. File and follow up

The user files them. The ticket numbers go into the comments of `docs/DBMS.md` and issue #827.
With each fix: rerun with the plain query, and remove the variant if it is the same as MariaDB.
Add a test that lists which variant waits for which ticket.

## 5. Open points

- B7: is `SystemConfig CGroup` meant for containers? If yes, ticket. If not, a question in the forum or nothing.
- `ERROR 1030` with concurrent `LOAD DATA`: the documentation says such loads wait. Ask, or file with a script that runs two clients?
- `cpimport -m 1` from a separate container fails with `MCS-2006`. Probably not supported, so no ticket. See #302.
