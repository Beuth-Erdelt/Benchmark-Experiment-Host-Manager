# Plan: Star Schema Benchmark (SSB)

Status: **plan only** (2026-10-24). Nothing is implemented. Tracks issue #348
("Try SSB"). Decisions of 2026-10-24 are in "Decisions" at the end; the
sections below already follow them.

## Goal

Add SSB as a DBMSBenchmarker workload, built like TPC-H and TPC-DS:

- **Generator pods** write SSB `.tbl` files to the shared data volume if they
  are not there yet. The data can be split into chunks for parallel loaders.
- **Loader pods** for PostgreSQL, MonetDB and ClickHouse.
- **Two schema variants:** `normal` (star schema, 4 dimensions + `lineorder`)
  and `flat` (one denormalized table `lineorder_flat`).
- **Two query variants:** `spec` (the 13 queries with the constants from the
  SSB specification) and `random` (the same 13 queries as templates with
  random parameters that keep each query's selectivity).

Rule from the request: everything SSB-specific lives in SSB files
(`ssb.py` in the root and in the `bexhoma/` subfolders, `experiments/ssb/`,
`images/ssb/`, `k8s/jobtemplate-loading-ssb-*.yml`). Other files stay generic.
The section "Generic files" below lists the few places this touches and how
each stays benchmark-free.

## Sources (trustworthy, checked 2026-10-24)

| What | Source | Use |
|---|---|---|
| Specification | P. O'Neil, E. O'Neil, X. Chen, S. Revilak: *Star Schema Benchmark*, Revision 3, 2009, <https://www.cs.umb.edu/~poneil/StarSchemaB.PDF>; paper: *The Star Schema Benchmark and Augmented Fact Table Indexing*, TPCTC 2009 | Schema, scaling rules, the 13 queries, the filter factor of each query |
| Generator | <https://github.com/eyalroz/ssb-dbgen> (fork of greenlion/ssb-dbgen, which comes from the UMass code). Merges the fixes of several abandoned forks. CMake build. | `dbgen`, pinned to one commit |
| Randomized queries | T. Rabl, M. Poess, H.-A. Jacobsen, P. O'Neil, E. O'Neil: *Variations of the Star Schema Benchmark to Test the Effects of Data Skew on Query Performance*, ICPE 2013, <https://research.spec.org/icpe_proceedings/2013/p361.pdf> (= the ACM link in #348) | Section 3.2: query templates with per-query parameter tables (e.g. Q1.1: year in [1993, 1997], `lo_discount between d-1 and d+1`, `lo_quantity < q`). This is the "randomized generalization". The skew part (PDGF data generator) is out of scope here. |
| Flat variant | ClickHouse docs, *Star Schema Benchmark* (<https://clickhouse.com/docs/getting-started/example-datasets/star-schema>); Apache Doris docs, *SSB* (<https://doris.apache.org/docs/benchmark/ssb/>, `tools/ssb-tools`: `ssb-flat-queries`, `ssb-queries`); StarRocks *SSB Flat* | `lineorder_flat` = `lineorder` inner-joined with customer, supplier, part (date is folded into `lo_orderdate`). Flat versions of Q1.1 to Q4.3. |
| Reference row counts | Doris SF1000: lineorder 5,999,989,709; customer 30,000,000; part 2,000,000; supplier 2,000,000; date 2,556 | Cross-check of the generator |

Why eyalroz/ssb-dbgen and not the alternatives:
- `vadimtk/ssb-dbgen` (used by the ClickHouse docs): older, Makefile only,
  without the fixes merged later.
- Doris `tools/ssb-tools`: a wrapper that downloads a dbgen fork. It adds a
  layer but no new source.

What the eyalroz generator offers (read from `src/driver.c`):
- `-s SF` sets the scale factor.
- `-T c|p|s|d|l` generates one table.
- `-b dists.dss` sets the distributions file.
- `-C n -S k` builds step `k` of `n`. Steps > 1 skip the date table.
- `-f` overwrites existing files.
- Build options: `EOL_HANDLING` (no trailing `|`) and `YMD_DASH_DATE`.

The code itself calls the parallel path "brittle", so M1 verifies it (see below).

Scaling (spec):

| Table | Rows |
|---|---|
| customer | 30,000 × SF |
| supplier | 2,000 × SF |
| part | 200,000 × ⌊1 + log2 SF⌋ |
| date | 2,556 (1992-01-01 to 1998-12-31) |
| lineorder | ≈ 6,000,000 × SF |

## What exists today (the template to copy)

- **Entry script** `tpcds.py` (root): argparse on `make_base_parser()`, one
  `configurations.default(...)` per DBMS, loading parameters
  (`STORE_RAW_DATA`, `BEXHOMA_SYNCH_GENERATE`, `TRANSFORM_RAW_DATA`,
  `TPCDS_TABLE`, `PODS_TOTAL`, `PODS_PARALLEL`), then `experiment.process()`.
- **Benchmark class** `bexhoma/benchmarks/tpcds.py::TPCDS(DBMSBenchmarkerBenchmark)`:
  `configure_workload()` chooses the query file per mode, writes the info text
  and picks the post-load list (`Checks` / `Index` / `Index_and_Constraints` /
  `Index_and_Constraints_and_Statistics`).
- **Experiment class** `bexhoma/experiments/tpcds.py::TpcdsExperiment`:
  `set_experiment(volume='tpcds')`,
  `set_experiments_configfolder('experiments/tpcds')`, `storage_label`,
  `add_benchmark(...)`, `experiment_dict_template`.
- **Script lists** live in the cluster config: `k8s-cluster.config`
  `volumes.<name>.initscripts` (`Schema`, `Checks`, `Index`, ...). They are
  read in `experiments/base.py:1404-1413` and `configurations/base.py:93-102`.
- **Images** `images/tpch/generator` (`generator.sh`: Redis queue → chunk
  index, `/data/tpch/SF$SF[/$N/$k]`, exits early if `*tbl*` exists, writes
  `/tmp/tpch/BEXHOMA_CHILD` for the loader, `dbgen -s SF -S k -C N`, `sed`
  drops the trailing `|`) and `images/tpch/loader_{postgresql,monetdb,clickhouse}`
  (`loader.sh`: reads the chunk index, barriers, one bulk load per file,
  reference tables only by child 1).
- **Job template** `k8s/jobtemplate-loading-tpch-PostgreSQL.yml`: generator
  as initContainer, loader as main container, emptyDir `/tmp/tpch`, PVC
  `bexhoma-data` on `/data`.
- **Query parameters** (DBMSBenchmarker `parameter.py`): types `integer`,
  `float`, `list` (with `size` for n distinct values → `NAME1`, `NAME2`),
  `date`, `firstofmonth`, `firstofyear`, `hexcode`, `dict` (returns a
  correlated pair key/value → `NAME1`, `NAME2`). Values are drawn once per
  experiment. `-xrcp` draws them per stream.
- **Collectors/evaluators:** `benchmark_sequence` stores the tool name
  (`dbmsbenchmarker`), so `collectors/mixed.py` and the evaluators need no
  SSB entry.

## Design

### D1. Schema variant: `normal` | `flat`

- Option `-xsv/--xschema-variant {normal,flat}`, default `normal`. It is
  passed to the generator and the loader as env `SSB_SCHEMA_VARIANT`.
- `normal`: dbgen files, loaded into the 4 dimensions + `lineorder`.
- `flat`: **decided (2026-10-24): the generator writes flat files by
  streaming in bash (option C below)**, and the loaders load only
  `lineorder_flat`. No CTAS in the DBMS, no extra binary.
- Flat table columns: **all** columns: the 17 `lo_*` columns, then all
  customer, supplier and part columns except their keys (key = the `lo_*`
  FK already there). This is the ClickHouse `lineorder_flat` column set; the
  exact list and order are fixed in M0 and are the same in the generator
  script and in `initschema-ssb-flat.sql`.
  - `lo_orderdate` and `lo_commitdate` become a `DATE` (ISO `yyyy-mm-dd`,
    converted in awk from the `yyyymmdd` key).
  - Reason: `EXTRACT(YEAR FROM lo_orderdate)` and date ranges work the same
    in PostgreSQL, MonetDB and ClickHouse. With an integer key, ClickHouse's
    `/` returns a float.
  - `dates` is not joined: the queries need only year/month/week, which
    come from `lo_orderdate`.

#### Flat files by bash streaming (option C, decided)

dbgen cannot write a flat table, so the generator pod joins after dbgen.
Column numbers below assume the dbgen order `lo_orderkey`(1),
`lo_linenumber`(2), `lo_custkey`(3), `lo_partkey`(4), `lo_suppkey`(5),
`lo_orderdate`(6), ..., `lo_commitdate`(16), `lo_shipmode`(17); M0 checks
it against the generator.

1. Each pod `k` of `N` runs `dbgen -s SF -C N -S k -T l` → its `lineorder`
   chunk.
   - If the normal chunk for the same SF/N/k already exists on `/data`, it
     is read from there instead (same rows, saves time).
2. Each pod also generates the **full** customer, supplier and part tables
   locally (`dbgen -s SF -T c`, `-T s`, `-T p`, without chunking). dbgen
   is deterministic, so every pod gets the same rows. This avoids a barrier
   on child 1 writing the dimensions to `/data`.
3. One pipeline, only `sort` touches the disk:
   ```bash
   export LC_ALL=C
   sort -t'|' -k1,1 -S "$SSB_SORT_MEM" -T "$work" customer.tbl > customer.sorted
   sort -t'|' -k3,3 -S "$SSB_SORT_MEM" -T "$work" lineorder.tbl.$k \
     | join -t'|' --check-order -1 3 -2 1 -o "$JOIN_FIELDS" - customer.sorted \
     | awk -F'|' -v OFS='|' -f flat.awk supplier.tbl part.tbl - \
     > lineorder_flat.tbl
   ```
   - **customer** (30,000 × SF rows, the big one) by sort-merge: `sort`
     with a fixed buffer (`SSB_SORT_MEM`, default 512M) spills to `$work`;
     `join` streams over both sorted inputs. `--check-order` makes a wrong
     sort order fail instead of silently dropping rows. `-o` lists all
     `lineorder` fields, then all customer fields except the key, so the
     column order is fixed.
   - **supplier and part** (at most about 2 M rows each, even at SF1000)
     by hash lookup: `flat.awk` reads both files into arrays
     `key → rest of line` (all columns), then streams the joined lines,
     appends the supplier and part columns, converts the two dates to ISO
     and writes the final column order. A missing key → `exit 1`.
   - `flat.awk` is a file in the generator image, not inlined in
     `generator.sh`.
4. **Row order:** the output is ordered by `lo_custkey`. By default a final
   `sort -t'|' -k1,1n -k2,2n` (same buffer and temp dir) restores the
   `lineorder` order (`lo_orderkey, lo_linenumber`), so PostgreSQL gets the
   same physical order as the normal variant and query times stay
   comparable. `SSB_FLAT_RESTORE_ORDER=0` skips it (ClickHouse sorts by
   its `ORDER BY` anyway). M1 measures the cost.
5. **Check:** `wc -l lineorder_flat.tbl` = `wc -l` of the chunk. `join`
   drops unmatched lines without an error, so this count is the real check.
   The pod fails on a mismatch.
6. **Work dir** `$work` (sort temp, dimensions, chunk): an `emptyDir` on
   node disk in the SSB job templates, **not** the memory-backed `emptyDir`
   used for `/tmp/tpch` in the TPC-H template. Otherwise the sort temp
   lands in RAM. Size limit from M1 (about 2–3× the chunk). Deleted after
   success.
7. Output to `/data/ssb/SF$SF/flat[/$N/$k]/lineorder_flat.tbl`, next to
   the normal files (`/data/ssb/SF$SF[/$N/$k]`), with its own `.complete`
   marker. Normal and flat data coexist and are reused independently.
8. The loader loads only `lineorder_flat.tbl` into `lineorder_flat`, in
   parallel per pod like `lineorder`. The schema script creates only
   `lineorder_flat` (`initschema-ssb-flat.sql`).

Memory: `sort -S` (512 MB) + the awk arrays of supplier and part with all
columns (my estimate: a few 100 MB at SF100, about 1 GB at SF1000;
measured in M1). Independent of the size of `lineorder` and customer.

Why flat files and not a CTAS in the DBMS:
- measured is the ingest of the wide table, like the published
  Doris/StarRocks/ClickHouse flat runs;
- the flat table is loaded in parallel per pod;
- no join/date-conversion SQL per dialect;
- cost: extra disk on `/data` (flat ≈ 2× lineorder, measured in M1) and
  the sort temp in the work dir.

#### Other options, kept for later inspection

| Option | How | RAM | Cost | Why not now |
|---|---|---|---|---|
| A. awk lookup for all three | customer, supplier, part in awk arrays, one streaming pass over `lineorder` | grows with customer: my estimate 0.5 GB at SF100, 4 GB at SF1000 (with all columns more) | simplest, fastest, no sort, keeps `lineorder` order | RAM grows with SF |
| B. `sort` + `join` for all three | three external sorts (custkey, suppkey, partkey) with `join` after each | fixed (`sort -S`) | 3 sorts (4 with order restore), temp disk 2–3× chunk, much CPU | slowest; C needs only one sort |
| D. DuckDB CLI | `COPY (SELECT … JOIN …) TO 'lineorder_flat.tbl'` from `read_csv` (SQL file `flat.sql`), `memory_limit` + `temp_directory` to spill | limitable | extra pinned binary in the image; fast | user prefers bash without an extra dependency |
| E. CTAS in the DBMS | load normal tables, `CREATE TABLE lineorder_flat AS SELECT …` post-load | in the DBMS | per-dialect SQL, no parallel load of the flat table | measures something else than published flat runs |

M1b measures C against D (and optionally A) on the same input; switching
is limited to the generator image.

### D2. Query variant: `spec` | `random`

- Option `-xqv/--xquery-variant {spec,random}`, default `spec`.
- Together with D1 this gives four query files in `experiments/ssb/`:
  `queries-ssb.config`, `queries-ssb-random.config`,
  `queries-ssb-flat.config`, `queries-ssb-flat-random.config`. In addition:
  `queries-ssb-empty.config`, `queries-ssb-profiling.config` (row counts,
  min/max of the key columns, as for TPC-H).
- `stream_ordering`: SSB defines no stream permutations. For `-xshq` a fixed
  table of 40 random permutations of 1..13 is generated once and stored in
  the query file (like TPC-H).
- Randomization rules (Rabl et al. 2013, sec. 3.2, adapted so that each
  query keeps its spec filter factor):
  1. A predicate that picks **one member of a uniform hierarchy level**
     (year, month, week, region, nation, city, mfgr, category, brand) is
     drawn from the whole level. With uniform data the filter factor stays
     the same.
  2. A **range over a measure** (`lo_discount`, `lo_quantity`) keeps its
     width and moves its start.
  3. **Correlated values** come from one `dict` parameter (region → nation,
     nation → cities).

| Q | Spec constants | Random |
|---|---|---|
| 1.1 | year 1993; discount 1–3; quantity < 25 | year ∈ [1993,1997]; discount D..D+2, D ∈ [0,8]; quantity < 25 (kept: FF 0.48 by definition) |
| 1.2 | yearmonthnum 199401; discount 4–6; quantity 26–35 | yearmonthnum ∈ 199201..199712; D..D+2; Q..Q+9, Q ∈ [1,41] |
| 1.3 | week 6, year 1994; discount 5–7; quantity 26–35 | week ∈ [1,52], year ∈ [1992,1997]; D..D+2; Q..Q+9 |
| 2.1 | category MFGR#12; s_region AMERICA | category ∈ MFGR#11..55 (25); region ∈ 5 |
| 2.2 | brand1 MFGR#2221..2228; s_region ASIA | category ∈ 25, brand start B ∈ [10,33] → B..B+7 (≥ 10, so the string range stays lexical); region |
| 2.3 | brand1 MFGR#2239; s_region EUROPE | category ∈ 25 × brand ∈ [1,40]; region |
| 3.1 | c_region = s_region = ASIA; years 1992–1997 | region ∈ 5 (same value for c and s); years fixed (a 6-year window fits only once) |
| 3.2 | nation UNITED STATES (c and s) | nation ∈ 25 |
| 3.3 | cities UNITED KI1, UNITED KI5 (c and s) | nation → 2 distinct cities of that nation |
| 3.4 | as 3.3 + yearmonth Dec1997 | as 3.3 + yearmonth ∈ Jan1992..Dec1997 |
| 4.1 | region AMERICA (c, s); mfgr ∈ {1,2} | region; 2 distinct mfgr from 1..5 |
| 4.2 | as 4.1 + year ∈ {1997,1998} | as 4.1 + years Y, Y+1, Y ∈ [1992,1997] |
| 4.3 | c_region AMERICA, s_nation UNITED STATES, year ∈ {1997,1998}, category MFGR#14 | region → nation of it (`dict`); Y, Y+1; category ∈ 25 |

  Open details to verify in M0 against the spec PDF: the spec constants
  above, how `d_weeknuminyear` is defined (for the flat Q1.3 date range),
  whether the 1998 order dates are complete, and the brand numbering (1..40
  per category). City strings are the first 9 characters of the nation,
  padded with blanks, plus a digit 0–9 (`'CHINA    1'`, `'UNITED KI1'`).
  The `dict` for nation → cities is written out in the query file.

- **Generic DBMSBenchmarker extension** (in DBMS-Benchmarker, benchmark-free):
  `dict` with `size > 1` samples `size` distinct values from the chosen key's
  list (→ `NAME1` = key, `NAME2`.. = values). Q3.3/3.4 need it (two cities of
  the same nation). `integer` with `size` already gives distinct values (4.1
  mfgr), but not "Y and Y+1". For 4.2/4.3, write `Y+1` in SQL
  (`{YEAR} + 1`), which every dialect accepts.
- Dialects: one base SQL per query, `DBMS` variants only where needed
  (ClickHouse: string literals and `LowCardinality` are fine; flat Q1.3/Q1.2
  date ranges with `interval` differ per dialect). The goal is ANSI SQL
  without variants for `normal`.

### D3. Generator image `images/ssb/generator`

- **Dockerfile, multi-stage:** stage 1 clones eyalroz/ssb-dbgen at a
  **pinned commit**, builds with `-DEOL_HANDLING=ON` and copies the license
  file. Stage 2 = Debian slim + `redis-cli` + `dbgen` + `dists.dss` +
  `flat.awk` (coreutils `sort`/`join` and `gawk` come with the image; pin
  `gawk` if Debian slim has only `mawk`, and test with the one in the image).
  - Unlike TPC-H, no binary is checked into git and the build is
    reproducible.
  - Keep `TRANSFORM_RAW_DATA` as a fallback switch (`sed` over the files) in
    case `EOL_HANDLING` does not work for all tables.
- `generator.sh` = copy of the TPC-H script with `tpch` → `ssb` (paths
  `/data/ssb/SF$SF/$N/$k`, `/tmp/ssb/BEXHOMA_CHILD`), call
  `dbgen -b dists.dss -s $SF [-C $N -S $k] -f`. With
  `SSB_SCHEMA_VARIANT=flat` it runs the steps in "Flat files by bash
  streaming" (D1) instead.
- Data reuse: the existing logic stays ("folder contains `*tbl*` → exit 0",
  `STORE_RAW_DATA_RECREATE`).
  - Gap: a generator pod that dies halfway leaves a partial folder that the
    next run takes as complete.
  - Improvement (in the SSB script, not shared): write a marker file
    `.complete` at the end and check that instead of `*tbl*`.
- Multi-tenancy blocks of the TPC-H script are **not** copied in v1. SSB v1
  supports no `-mtn`; the entry script rejects it with a clear message.
- **Chunking:** `-C N -S k` per pod. Child 1 also writes `date.tbl`. The
  loader loads `date` only in child 1 (like `nation`/`region` in TPC-H).
  Which tables dbgen actually splits (customer/supplier/part as well, or only
  lineorder) and the file names of the parts (`lineorder.tbl.k`?) are checked
  in M1. The loader globs `*tbl*` and maps the name to the table, so both
  cases work.

### D4. Loader images `images/ssb/loader_{postgresql,monetdb,clickhouse}`

Each is a copy of the TPC-H loader without the tenancy blocks, with
`/tmp/ssb`, `SSB_TABLE` (limit to one table, `-xlit`) and `date` only by
child 1. With `SSB_SCHEMA_VARIANT=flat` it reads from
`/data/ssb/SF$SF/flat[/$N/$k]` and loads `lineorder_flat.tbl` only (every
child). The flat file has ISO dates; all three load commands accept them
for a `DATE` column.

| DBMS | Load command | Notes |
|---|---|---|
| PostgreSQL | `psql \COPY <t> FROM '<file>' delimiter '|' null ''` | Check: output `COPY <lines>` = `wc -l`. TPC-H sets `FAILED=0` regardless; SSB fails the pod on a mismatch. |
| MonetDB | `mclient COPY <n> RECORDS INTO <t> FROM STDIN USING DELIMITERS '|'` | `.monetdb` credentials, retry as in TPC-H |
| ClickHouse | `clickhouse-client --format_csv_delimiter='|' --query "INSERT INTO <t> FORMAT CSV" < file` | Like the TPC-H ClickHouse loader. `ClickHouseCluster` later. |

The table name `date` is a reserved word in PostgreSQL/MonetDB. **Decided:
`dates`** (as in Doris): no quoting in 13 × 4 queries, the loader maps
`date.tbl` → `dates`. This is a deviation from the spec and is noted in the
workload info.

### D5. Per-DBMS scripts `experiments/ssb/{PostgreSQL,MonetDB,ClickHouse}/`

Each folder has:
- `initschema-ssb.sql`, `initschemadummy-ssb.sql`
- `initschema-ssb-flat.sql`, `initschemadummy-ssb-flat.sql`
- `initindexes-ssb.sql`, `initconstraints-ssb.sql` (PK/FK),
  `initstatistics-ssb.sql`
- `initindexes-ssb-flat.sql`, `initstatistics-ssb-flat.sql` (no
  constraints for flat: there are no FKs, and `lo_orderkey, lo_linenumber`
  as PK is optional)
- `checkschema-ssb.sql`, `checkschema-ssb-flat.sql` (row counts, sizes;
  always last)
- `reset-ssb.sql` / `reset-flush.sh` (for `-ar`)
- `durability-*.sql` / `restoredurability-*.sql` (copied from TPC-H so that
  `-xld` works)

Content, following the TPC-H scripts of the same DBMS (style: header
comment with purpose, one `ALTER TABLE` per table in PostgreSQL, one action
per statement in MonetDB, `sys.` prefix for MonetDB `ANALYZE`):

| Script | PostgreSQL | MonetDB | ClickHouse |
|---|---|---|---|
| `initindexes-ssb.sql` (`-xii`) | FK columns of the fact table: `lineorder(lo_orderdate)`, `(lo_custkey)`, `(lo_suppkey)`, `(lo_partkey)`; dimension attributes the queries filter on: `customer(c_region)`, `(c_nation)`, `(c_city)`, `supplier(s_region)`, `(s_nation)`, `(s_city)`, `part(p_mfgr)`, `(p_category)`, `(p_brand1)`, `dates(d_year)`, `(d_yearmonthnum)` | same set as named indexes (MonetDB: per-column access paths, like its TPC-H script) | none (file missing = skipped, as in TPC-H) |
| `initconstraints-ssb.sql` (`-xic`) | PK `customer(c_custkey)`, `supplier(s_suppkey)`, `part(p_partkey)`, `dates(d_datekey)`, `lineorder(lo_orderkey, lo_linenumber)`; FK `lo_custkey`, `lo_suppkey`, `lo_partkey`, `lo_orderdate` → dimensions (`lo_commitdate` → `dates` only if M1 shows all values exist) | same, one statement each | none |
| `initstatistics-ssb.sql` (`-xis`) | `ANALYZE VERBOSE` per table + row counts of the small tables | `ANALYZE sys.<table>` per table | none |
| `checkschema-ssb.sql` | row counts, sizes, `CHECKPOINT` (copy of the TPC-H one) | same | row counts, sizes |
| flat: `initindexes-ssb-flat.sql` | `lineorder_flat(lo_orderdate)` and the filter columns `c_region`, `s_region`, `c_nation`, `s_nation`, `p_category`, `p_mfgr` | same | none |
| flat: `initstatistics-ssb-flat.sql` | `ANALYZE VERBOSE lineorder_flat` | `ANALYZE sys.lineorder_flat` | none |

- Index list in M4 is checked against the 13 query plans (PostgreSQL
  `EXPLAIN` via `-xse`): an index that no query uses is dropped, as the
  TPC-H script does for `l_suppkey`.
- ClickHouse: MergeTree tables; `lineorder` ordered by
  `(lo_orderdate, lo_orderkey)`, `lineorder_flat` the same, as in the
  ClickHouse docs. The sort key is set in `initschema-ssb.sql`, so the
  index/constraint/statistics scripts are not needed.
- Spec decimals: ClickHouse uses `UInt32`, PG/MonetDB `INTEGER`/`DECIMAL` as
  defined in the spec.

### D6. Script lists in the cluster config

**Decided:** a new entry `volumes.ssb` in `cluster.config`, like
`volumes.tpcds` (`cluster.config:1529`). `k8s-cluster.config` has the same
volume block (`k8s-cluster.config:1522`), so it gets the same entry to keep
both files in step. This is config, not code.

```
'ssb': {
    'id': '<next free id>',
    'initscripts': {
        'Schema':        ['durability.sql', 'initschema-ssb.sql'],
        'Schema_dummy':  ['durability.sql', 'initschemadummy-ssb.sql'],
        'Checks':        ['restoredurability.sql', 'checkschema-ssb.sql'],
        'Index':         ['initindexes-ssb.sql', 'restoredurability.sql', 'checkschema-ssb.sql'],
        'Index_and_Constraints': [...],
        'Index_and_Constraints_and_Statistics': [...],
        # flat: only lineorder_flat
        'Schema_flat':       ['durability.sql', 'initschema-ssb-flat.sql'],
        'Schema_dummy_flat': ['durability.sql', 'initschemadummy-ssb-flat.sql'],
        'Checks_flat':       ['restoredurability.sql', 'checkschema-ssb-flat.sql'],
        'Index_flat':        ['initindexes-ssb-flat.sql', 'restoredurability.sql', 'checkschema-ssb-flat.sql'],
        'Index_and_Statistics_flat': ['initindexes-ssb-flat.sql', 'initstatistics-ssb-flat.sql',
                                      'restoredurability.sql', 'checkschema-ssb-flat.sql'],
    }
},
```

- `bexhoma/benchmarks/ssb.py::configure_workload` picks the keys (base
  name from `-xii/-xic/-xis`, plus `_flat` for `-xsv flat`; `-xic` is
  ignored for flat with a note in the workload info).
- No `SF<n>` keys: they belong to the old init-script path, which SSB does
  not use (loading always goes through the loader pods).
- Choose the `id` in M2 after reading how the existing entries use theirs.

## Generic files (and how they stay generic)

| # | File | Change | Benchmark-free? |
|---|---|---|---|
| G1 | `bexhoma/benchmarks/__init__.py`, `bexhoma/experiments/__init__.py` | one import line + alias `ssb = SsbExperiment` each | Registry only, no logic. Alternative: auto-discovery via `pkgutil`, more change than benefit. **Recommendation: import lines.** |
| G2 | `bexhoma/scripts/experimentsmanager.py:204-216` | Replace the `match type` with `getattr(experiments, workload_properties['type'], experiments.base)` | Yes, and it **removes** the existing names `ycsb/tpcc/tpch/tpcds/benchbase`. Without G2, `bexhoma summary` for SSB falls back to `experiments.base` and shows no DBMSBenchmarker summary. |
| G3 | DBMS-Benchmarker `parameter.py::randomizer.dict` | `size > 1` (D2) | Yes |
| G4 | `scripts/build.sh` and `scripts/build.ps1` | add lines that name the four images (`generator_ssb`, `loader_ssb_postgresql`, `loader_ssb_monetdb`, `loader_ssb_clickhouse`), next to the TPC-DS lines | Decided: these scripts may name images |
| G5 | Docs index (`docs/`, `README.md`) | Link to the new page `docs/Example-SSB.md` | Documentation |
| G6 | `cluster.config`, `k8s-cluster.config` | entry `volumes.ssb` (D6) | Decided: config may name the benchmark |

Not touched in v1: `experiment.py` / `bexhoma/spec.py` /
`contracts/*.yml` / `agent/` (YAML and agent path; today that is TPC-H/YCSB
only), `collectors/*`, `evaluators/*` (generic via `dbmsbenchmarker`).

## Milestones

**M0 – Sources pinned.**
- Read the spec PDF; write down the 13 queries, filter factors, scaling and
  the column list in `experiments/ssb/README.md`.
- Clone eyalroz/ssb-dbgen: read the license, choose and note the commit
  hash, check the build with `EOL_HANDLING=ON`.
- Check the open details from D2 (weeks, 1998, brands).

**M1 – Generator verified locally (scratchpad, not in the repo).**
- SF1 without chunks vs `-C 4 -S 1..4`. Check:
  - Which files appear and under which names.
  - The sum of rows per table is equal.
  - No duplicate keys (`lo_orderkey, lo_linenumber`; `c_custkey`, ...).
  - `date` only in step 1.
  - Row counts match the spec formula.
  - SF10 part = 200,000 × ⌊1 + log2 10⌋ = 800,000.
- FK check: every `lo_orderdate`/`lo_commitdate` exists in `date`.
- Result decides D3 (which tables are split; is the `sed` fallback needed).
- Flat (option C): SF1 unchunked and the 4 chunks. Check: rows =
  `lineorder` rows, the union of the chunk files = the unchunked file
  (sorted), all dimension columns present, ISO dates, row order restored.
  Measure at SF1 and SF10: time (with and without order restore), peak RSS
  of awk and sort, sort temp size, flat file size. Decides the RAM limit
  and the work-dir size limit of the generator container in the job
  templates.

**M1b – Flat generation: pure bash (C) vs DuckDB (D), measured.**
- Goal: numbers for both on the same input, so the choice of C can be
  revisited with data. Does not block M2+; the production image stays bash
  only.
- Tool: `images/ssb/generator/compare-flat.sh` (dev tool, in the repo next to
  `generator.sh`). It takes one `lineorder` chunk plus the full customer,
  supplier, part files and runs
  1. C: `sort`/`join`/`flat.awk`, with and without the final order restore;
  2. D: DuckDB CLI with `flat.sql` (same column list and order, ISO dates,
     `ORDER BY lo_orderkey, lo_linenumber` in the variant with order
     restore), `memory_limit` set to the same RAM budget as C and
     `temp_directory` in the same work dir;
  3. optionally A (awk lookup for all three) as the low-effort baseline.
- Per run it records, as one CSV line: method, SF, N, k, order restore
  (yes/no), wall time, user+sys CPU, peak RSS (`/usr/bin/time -v`), peak
  temp-dir size (polled `du`), output size, row count.
- **Equal output:** both outputs, sorted with `LC_ALL=C sort`, must be
  byte-identical (`cmp`). DuckDB may format numbers differently (e.g.
  decimals, trailing zeros); `flat.sql` casts so the text matches dbgen's.
  Any remaining difference is listed, not hidden.
- Where:
  - locally (scratchpad, WSL/Linux): SF1 and SF10, N = 1 and 4;
  - on the cluster: SF100 with N = 8, one chunk, in a one-off pod on a
    worker node with the same RAM limit and disk `emptyDir` as the
    generator job (`-ks no`-style cleanup by label). DuckDB comes from a
    dev image tag `generator_ssb:<version>-duckdb` (build arg
    `INCLUDE_DUCKDB=1`, pinned DuckDB release with checksum); the normal tag
    stays without DuckDB.
- Each configuration runs 3×; report median and spread. Page cache is
  dropped between runs if the pod may do that, otherwise the first run is
  discarded as warm-up.
- Result: a table in this plan and a short section in `docs/Example-SSB.md`
  (time, CPU, RAM, temp disk per method and SF). You decide afterwards
  whether C stays; switching only changes the generator image (D1, "Other
  options").

**M2 – Python side.**
- `bexhoma/benchmarks/ssb.py` (`SSB(DBMSBenchmarkerBenchmark)`,
  `configure_workload`: modes run/load/start/empty/profiling, query file
  from `schema_variant` × `query_variant`, schema and post-load keys incl.
  `_flat`, info text).
- `volumes.ssb` in `cluster.config` and `k8s-cluster.config` (D6, G6).
- `bexhoma/experiments/ssb.py` (`SsbExperiment`, `volume='ssb'`,
  `storage_label = f'ssb-{SF}'`; plus `-flat` in the storage label for
  flat, because a loaded PVC from the normal variant does not contain
  `lineorder_flat`).
- Root `ssb.py` (copy of `tpcds.py`, DBMS PostgreSQL/MonetDB/ClickHouse,
  options `-xsv`, `-xqv`, `-xlit`, `-xii/-xic/-xis`, `-xrcp`, `-xshq`,
  `-xaq`; rejects `-mtn`).
- G1, G2.

**M3 – Images.**
- `images/ssb/generator`, `images/ssb/loader_{postgresql,monetdb,clickhouse}`,
  `images/ssb/README.md` + one README per image (style as in
  `images/tpch/README.md`).
- Job templates `k8s/jobtemplate-loading-ssb-{PostgreSQL,MonetDB,ClickHouse}.yml`
  (+ `-NIL` like TPC-H, if used).
- G4 (`build.sh` and `build.ps1`). Build and push the images.

**M4 – Schema and scripts** (D5) for the three DBMS, normal and flat.

**M5 – Query files** (D2): first `spec` normal, then flat, then the two
`random` files. G3 in DBMS-Benchmarker incl. a unit test.
- Local test: generate parameters 1000×, check that every SQL instance is
  valid (city strings exist, brand range lexical).
- Every query on SF1 returns ≥ 1 row.

**M6 – Unit tests** (`tests/test_ssb_*.py`, following
`tests/test_reset_scripts.py` and `tests/test_cluster_sut_settings.py`):
- Query file chosen per variant.
- Every key `configure_workload` can pick exists in `volumes.ssb` of both
  cluster config files, both files hold the same entry, and each referenced
  script exists for each DBMS.
- G2 dispatch for every type.

**M7 – Cluster checks** (`-ks no`, `-nc 2` if with `-rst`;
cleanup `kubectl delete all,secret -l experiment=<code>`):
1. `ssb.py -sf 1 -dbms PostgreSQL MonetDB ClickHouse -nlp 1 run`.
   The results of the 13 queries must be equal across the three DBMS (the
   DBMSBenchmarker result comparison). The spec gives no expected answers,
   so agreement across DBMS is the correctness check.
2. Same with `-nlp 4`. Row counts in `checkschema` equal to run 1, `date`
   only once.
3. `-xsv flat`: flat results = normal results per query.
4. `-xqv random` and `-xqv random -xrcp -ne 1,2`: no errors, parameters in
   the protocol vary.
5. Second run on the same SF: the generator reports "Raw folder exists".
6. SF10 with `-nlp 8` as a size check (timings for the docs).

**M8 – Test scripts.**
- `scripts/test-docs-ssb.sh` and `scripts/test-docs-ssb.ps1`, built like
  `scripts/test-docs-tpcds.sh/.ps1`:
  - `source ./scripts/testfunctions.sh`
  - one commented block per run (each option explained in the header
    comment), then `bexhoma ssb ...`, wait, log, extract the summary to
    `logs_tests/doc_ssb_*_summary.txt`
- Runs, all with `-ks no` and the node/`-ms` variables of the other scripts:

  | # | Run | Shows in the docs |
  |---|---|---|
  | 1 | `-dbms PostgreSQL -sf 1 -nlp 8 -xii -xic -xis -tr` | normal, spec, parallel load |
  | 2 | `-dbms MonetDB -sf 1 -nlp 8 -tr` | MonetDB |
  | 3 | `-dbms ClickHouse -sf 1 -nlp 8 -tr` | ClickHouse |
  | 4 | `-dbms PostgreSQL MonetDB ClickHouse -sf 1 -xsv flat -tr` | flat |
  | 5 | `-dbms PostgreSQL -sf 1 -xqv random -xrcp -ne 1,2 -tr` | random parameters, different per stream |
  | 6 | `-dbms PostgreSQL -sf 1 -nlp 8 -rst $BEXHOMA_STORAGE -rss 50Gi -nc 2 -tr` | persistent storage, repetition 2 reuses the data (-nc 2 per the storage-run rule) |
  | 7 | `load` mode / `profiling` mode, one each | modes |

- Hook into the scripts that run several docs scripts, if they list them
  (`scripts/test-docs-cases.sh/.ps1`, `scripts/test-current.sh`): check in
  M8 and add SSB where TPC-DS is listed.
- The results of M7 (cluster checks) are the first run of this script, so
  M7 and M8 can share runs.

**M9 – Docs page.**
- `docs/Example-SSB.md`, built like `docs/Example-TPC-DS.md`:
  - what SSB is, with the sources (spec, ICPE 2013, ClickHouse/Doris for
    flat, eyalroz/ssb-dbgen with commit)
  - generator and loaders: data on `/data/ssb/SF<n>[/<N>/<k>]` and
    `/data/ssb/SF<n>/flat[/<N>/<k>]`, reuse, split for `-nlp`, flat files
    joined by `sort`/`join`/`awk` streaming in the generator
  - options `-xsv`, `-xqv`, `-xlit`, `-xii/-xic/-xis`, `-xrcp`,
    `-xshq`, `-xaq`, with one example command each, taken from
    `test-docs-ssb.sh`
  - summary output of runs 1, 4 and 5 (pasted from the logs, as on the other
    Example pages)
  - deviations from the spec: table `dates`, `lo_orderdate` as `DATE` in
    flat, the randomization rules (D2 table)
  - limits of v1: no multi-tenancy, no ClickHouseCluster, no MySQL/MariaDB
- `docs/Queries-SSB.md` like `docs/Queries-TPC-H.md`: the 13 queries
  (normal and flat) and their parameter domains.
- Add both pages to `docs/Examples.md` and `docs/WorkBenchmarkList.md`
  (and to the docs index if pages are listed there, e.g. a Sphinx toctree);
  update `images/README.md` and `experiments/README.md` if they list the
  benchmarks.
- Comment on issue #348 with a link (only after you approve it).

## Risks

- **dbgen chunking is "brittle"** (comment in the code). M1 checks it before
  anything depends on it. Fallback: generate lineorder in chunks and the
  dimensions only in child 1 (`-T`).
- **Generator license:** the original comes from TPC dbgen. The TPC-H image
  carries `tpc_eula.txt`. M0 clarifies what eyalroz's repo includes, and the
  image includes it.
- **Flat streaming in the generator pod:** RAM is bounded (`sort -S` +
  supplier/part arrays), but the sort temp needs node disk (work-dir
  `emptyDir`, 2–3× the chunk). A node with little ephemeral storage evicts
  the pod; use more loader pods (smaller chunks) or move `$work` to the
  PVC. Sizes from M1 and M7.6.
- **`join` pitfalls:** both inputs must be sorted with the same `LC_ALL=C`
  key order; `--check-order` and the row count check (D1 step 5) catch
  mistakes.
- **Disk on `/data`:** flat data comes on top of the normal data. Check the
  free space of the `bexhoma-data` PVC before SF100 flat runs.
- **Randomization changes run time per draw** (e.g. a nation with fewer
  rows). With uniform data the variance is small. Compare `random` runs only
  with the same seed / the same parameter file. DBMSBenchmarker stores the
  parameters in the protocol.
- **`dates` instead of `date`:** published SSB results use both. Comparison
  across systems is not affected; the table name is in the docs.

## Decisions (2026-10-24)

1. Option names `-xsv {normal,flat}`, `-xqv {spec,random}`: **ok**.
2. Table name **`dates`**.
3. SSB script lists go into **`cluster.config`** (plus the same entry in
   `k8s-cluster.config`), not into `experiments/ssb.py` (D6, G6).
4. `scripts/build.sh` and `scripts/build.ps1` **name the SSB images** (G4).
5. Multi-tenancy (`-mtn`) **later**; `ssb.py` rejects it in v1.
6. Flat data: **flat files generated by bash streaming, option C**
   (`sort`+`join` for customer, awk lookup for supplier and part) in the
   generator pod (D1). Options A, B, D (DuckDB) and E (CTAS) stay in D1 for
   later inspection. No CTAS in the DBMS, no `-xdn`.
9. Flat table has **all dimension columns** (as ClickHouse `lineorder_flat`).
10. **Measure pure bash (C) vs DuckDB (D)** for flat generation (M1b).
7. G1: **import lines**.
8. `ClickHouseCluster` and MySQL/MariaDB: **later**.

The plan as a whole is agreed (2026-10-24). No open decisions; the
remaining unknowns are checked in M0/M1.
