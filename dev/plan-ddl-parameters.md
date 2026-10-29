# Plan: DDL parameters (placeholders in init scripts)

Status: **plan only** (2026-10-29, revised the same day). Inventory of what
exists, gaps, a generic mechanism with minimal Python changes, and candidate
parameters per DBMS. Nothing implemented. Non-DDL settings (planner knobs,
isolation level, client options):
[plan-session-parameters.md](plan-session-parameters.md) (parked; today:
one experiment per value with `--set` on the same `-rst` PVC).

## How it works today

- A driver calls `config.set_ddl_parameters(**kwargs)` (or
  `experiment.set_ddl_parameters`, inherited by every configuration,
  [base.py:126](../bexhoma/configurations/base.py#L126)). Both **replace**
  the dict instead of merging.
- When `ddl_parameters` is **non-empty**, every script of the load step
  (init, index, check, durability, reset) is read, filled with
  `str.format(**ddl_parameters)`, written as `filled_<script>` **into the
  source folder** `experiments/<bench>/<dbms>/` (gitignored), uploaded to the
  SUT and copied to the result folder
  ([loading.py:604-637](../bexhoma/configurations/loading.py#L604-L637)).
- When it is empty, scripts are uploaded unchanged.
- Separate path for tenants per schema: scripts are filled with
  `str.format(BEXHOMA_SCHEMA=...)` only, **ignoring `ddl_parameters`**
  ([loading.py:545-576](../bexhoma/configurations/loading.py#L545-L576)).
- The values also go to `connection_parameter['ddl_parameters']`
  ([benchmarking.py:149](../bexhoma/configurations/benchmarking.py#L149)),
  so they are in the result's connection info.

Consequences of `str.format`:

- Any literal `{` or `}` in **any** script of a configuration with DDL
  parameters breaks the load (`test_no_curly_braces` guards only the
  `*durability-*` scripts). JSON in YugabyteDB `replica_placement`,
  ClickHouse macros `{shard}`/`{replica}`, PL/pgSQL with `format()` are all
  affected. Redis and Dragonfly also get DDL parameters, so their `.sh`
  scripts (`save-snapshot.sh`) go through `str.format` too: no braces today,
  but a later `${VAR}` would break the load.
- A placeholder the driver does not set raises `KeyError` mid-load.

## Inventory: placeholders that exist

Keys set by drivers: `num_worker_replicas` and `num_worker_shards`, from
`-nwr` / `-nws` (default **0**, [cli_args.py:352](../bexhoma/cli_args.py#L352)),
and `BEXHOMA_SCHEMA` in the tenant-per-schema path.

| Placeholder | Script | Used for | Set by | Reachable? |
|---|---|---|---|---|
| `{num_worker_shards}` | ycsb/Citus/initschema-ycsb.sql | `citus.shard_count` | ycsb.py | yes |
| `{num_worker_replicas}` | ycsb/Citus/initschema-ycsb.sql | `citus.shard_replication_factor` | ycsb.py | yes |
| `{num_worker_replicas}` | ycsb/CockroachDB/initschema-ycsb.sql | zone `num_replicas` | ycsb.py | yes |
| `{num_worker_replicas}` | ycsb/CockroachDB/checkschema-ycsb.sql | under-replication check | ycsb.py | yes |
| `{num_worker_replicas}` | ycsb/TiDB/initschema-ycsb.sql | PD `max-replicas` | ycsb.py | yes |
| `{num_worker_replicas}` | benchbase/tpcc/TiDB/initschema-benchbase.sql | PD `max-replicas` | benchbase.py | yes |
| `{BEXHOMA_SCHEMA}` | tpch/PostgreSQL/*-tpch-schema.sql, benchbase/tpcc/PostgreSQL/*-benchbase-schema.sql | tenant schema name | loading.py (tenant per schema) | yes |
| `{num_worker_shards}`, `{num_worker_replicas}` | tpcc/Citus/initschema-tpcc-tmp.sql | shard count / RF | hammerdb.py | **no**: file not in any script list; HammerDB builds the schema |
| `{shard_count}`, `{replication_count}` | tpch/Citus/initschema-tpch-template.sql | shard count / RF | nobody | **no**: tpch.py sets `num_worker_*` → `KeyError` with the `SF*-template` keys |
| `{num_replicas}` | tpch/CockroachDB/initschema-tpch(-recommended).sql | zone `num_replicas` | nobody | no (CockroachDB not in tpch.py) |
| `{engine}` | tpch/MariaDB/initschema-tpch-template.sql | storage engine | nobody | no (MariaDB gets no DDL params) |
| `{fragment_size}`, `{shard_count}` | tpch/OmniSci/*.sql | fragment size / shards | nobody | no (legacy, not in tpch.py) |

Drivers that set `num_worker_*` without any script using them: benchbase.py
Citus and CockroachDB, hammerdb.py Citus, tpch.py Citus, ycsb.py Redis and
Dragonfly. YugabyteDB gets no DDL parameters at all. tpcds.py and ssb.py set
none (SSB solves `-xdim` by folder variants).

## Gaps found

1. **`-nws` has no effect on Citus TPC-H, SSB and both TPC-C drivers.**
   TPC-H, SSB and BenchBase TPC-C call `create_distributed_table` with the
   Citus default of 32 shards; HammerDB builds its own schema. Only YCSB
   reads `-nws`. Runs that vary `-nws` for these benchmarks measured nothing.
2. **Default 0.** With `-nwr`/`-nws` left out, YCSB Citus executes
   `SET citus.shard_count = 0` and CockroachDB `num_replicas = 0`. Test
   scripts always pass both flags, so it has not been hit; to verify on the
   cluster what happens (error or silent fallback).
3. **Orphan placeholders** (Citus TPC-H template, MariaDB `{engine}`,
   CockroachDB TPC-H, OmniSci) under names no driver sets. The Citus and
   MariaDB templates are also **stale**: last changed 2026-05-26, while the
   schemas in use changed since (MariaDB PK in schema 2026-10-22; the Citus
   template differs in 37 lines).
4. **Filled files are written into the source tree**, shared by all
   configurations: two configurations of one DBMS with different values
   race on the same `filled_*` file.
5. `str.format` on all scripts (see above); tenant path ignores DDL
   parameters.

## Proposal: mechanism

Goal: generic, no per-driver code. Drivers (tpch.py, ycsb.py, ...) only
lose lines.

- **Defaults file per script folder** (decided 2026-10-29):
  `experiments/<bench>/<dbms>/ddl-parameters.config`, Python dict literal
  like `queries-*.config`. One entry per key: default, allowed values or
  range, one-line description. The file is the single source for defaults,
  `-xddl` validation, the catalog capability and the docs table. Folder
  variants (`ssb/Citus/distributed`) use the file of `path_experiment_docker`,
  falling back to the parent folder. No file = no filling = today's
  behaviour.
- **Defaults reproduce today's scripts**, so baselines stay comparable.
  Exception: where today's value is the broken 0 (gap 2), the default is the
  DBMS default (Citus 32 shards / RF 1, CockroachDB and TiDB 3 replicas).
- **Precedence**: file defaults < `-nwr`/`-nws` (only if > 0) < `-xddl` <
  per-call values (`BEXHOMA_SCHEMA` for tenant `t`).
- **Safe filling**: replace only `{name}` where `name` is a key of the merged
  dict; everything else, including ClickHouse macros and JSON, stays
  literally. One fill function for both paths (tenant and normal), so tenant
  scripts get DDL parameters too.
- **Validation before the SUT starts**: a `-xddl` key that the
  configuration's defaults file does not declare, or a value outside its
  allowed values → error. The merged (effective) dict is stored in
  `cfg.ddl_parameters`, so the connection info records effective values,
  not only the given ones.
- **Filled files go to the result folder only** (per configuration), never
  to `experiments/`.
- **Sweep inside one experiment, generic** (revised 2026-10-29): reuse the
  resource sweep. `experiment.process()` already calls
  `expand_resource_cells()`
  ([experiments/base.py:1183](../bexhoma/experiments/base.py#L1183)), which
  deep-copies every configuration once per resource cell, for all drivers.
  DDL values become part of the cell:
  - `-xddl KEY=V1,V2` (comma list); several keys → Cartesian product.
    Values are tokens without commas; where SQL needs more (e.g.
    `CODEC(Delta, ZSTD)`), the defaults file maps the token (`delta_zstd`)
    to the SQL text.
  - cells = resource cells × DDL combinations, one numbering: `{base}-{n}`
    and alias `{base}@{n}` as today, so names don't nest.
  - **Storage per cell** (`{storageConfiguration}-{n}`, as today): data
    differs per DDL value, so a cell must never reuse another cell's PVC
    (`-rst`).
  - Only configurations whose defaults file declares **all** swept keys
    are cloned; others are kept once (like a SUT bexhoma does not manage),
    e.g. `-xddl num_worker_shards=16,32` with `-dbms PostgreSQL Citus`
    clones only Citus.
  - Validation moves to `process()`, before cloning: every configuration's
    `path_experiment_docker` is known there, and nothing is started yet.
  - The mapping cell number → values is printed, written to the workload
    info and stored per configuration (`connection_parameter`).
  - Cost: one SUT and one load per cell; `-ms` limits how many run at once.
    Alternatively, separate experiments grouped in a study
    ([plan-studies.md](plan-studies.md)).
- Keep schema **variants that change many statements** (reference vs
  distributed dimensions, distribution key, columnar) as script or folder
  variants (as `-xdim` does); a key may select the variant.

### Python changes

| File | Change | Size |
|---|---|---|
| [bexhoma/configurations/loading.py](../bexhoma/configurations/loading.py) | one fill function (load defaults file, merge, safe replace, write to result folder); replaces both existing branches (tenant `str.format` and `ddl_parameters` `str.format`) | net fewer lines |
| [bexhoma/cli_args.py](../bexhoma/cli_args.py) | `-xddl KEY=V1[,V2…]`, `action='append'`; parser returns the list of DDL combinations | ~10 lines |
| [bexhoma/experiments/base.py](../bexhoma/experiments/base.py) | where `-nwr`/`-nws` are already parsed (~line 696): build the dict from `-nwr`/`-nws` (> 0) and `-xddl`, one line in the workload info; in `expand_resource_cells()`: cells = resource cells × DDL combinations, set each clone's DDL values, clone only configurations whose defaults file declares the keys; validate before cloning | ~30 lines |
| [bexhoma/configurations/base.py](../bexhoma/configurations/base.py) | `set_ddl_parameters` merges (`update`) instead of replacing | 1 line |
| tpch.py, ycsb.py (5×), benchbase.py (3×), hammerdb.py | **delete** the `set_ddl_parameters(num_worker_*)` calls: experiments/base.py sets them for all, and the driver's 0 would otherwise override the file defaults | deletions only |
| tests/test_ddl_parameters.py (new) | merge order, safe filling (braces, macros survive), no-op without file, unknown key error, tenant path, cell expansion (product, names, storage per cell, unswept DBMS kept once) | new |
| later (M3b): [bexhoma/spec.py](../bexhoma/spec.py), tpch_catalog.py, ycsb_catalog.py | `systems[].ddl` validated against the defaults file; catalogs emit `-xddl` (shared helper, not per catalog) | small |

No change: tpcds.py, ssb.py, DBMS-Benchmarker, evaluators, k8s templates,
TPCTC23/ (legacy). `test_no_curly_braces` can stay as is.

## Candidates per DBMS

Priority: **A** = cheap, large or well-known effect, belongs in the first
round; **B** = useful sweep; **C** = later or only with extra deployment.
"Default" is the current, hard-coded behaviour.

Reach: DDL keys reach TPC-C only through **BenchBase**; HammerDB creates its
own schema (bexhoma's TPC-C init scripts are empty placeholders), and so does
BenchBase on CockroachDB.

#### PostgreSQL (also PgDuckDB, DatabaseService) — TPC-H, TPC-DS, SSB, YCSB, TPC-C (BenchBase)

| Key | Values | Default | Where | Why it matters | Prio |
|---|---|---|---|---|---|
| `fillfactor` | 50–100 | 100 | `WITH (fillfactor=…)` on usertable / BenchBase TPC-C tables | free space per page enables HOT updates: fewer index writes and less bloat for YCSB a/b/f and TPC-C; check via `n_tup_hot_upd` / `n_tup_upd` | A |
| `index_method` | btree, hash, brin | btree | TPC-H/TPC-DS index scripts | hash: smaller, faster equality on join keys; brin on dates (`l_shipdate`, `o_orderdate`) tiny and cheap when data is loaded in date order | B |
| `partition_by` | none, year | none | lineitem/orders (TPC-H), store_sales (TPC-DS) | partition pruning for date-range queries; changes plans and parallelism | B |
| `cluster_on` | none, a date index | none | after load: `CLUSTER` | physical order makes BRIN and range scans effective | C |
| `toast_compression` | pglz, lz4 | pglz | `ALTER TABLE … SET COMPRESSION` | only affects values > ~2 kB: YCSB rows (10 × 100 B) and TPC-H rows stay below, so **expected no effect** for current benchmarks; list for completeness | C |
| `autovacuum_scale_factor` | e.g. 0.01–0.2 | server default | table storage parameter | earlier vacuum on hot OLTP tables keeps bloat and latency stable in long runs | B |

#### Citus — TPC-H, SSB, YCSB, TPC-C (BenchBase)

| Key | Values | Default | Where | Why | Prio |
|---|---|---|---|---|---|
| `num_worker_shards` | 1…n | 32 | `SET citus.shard_count` before `create_distributed_table` | parallelism per query vs. per-shard overhead; rule of thumb: a small multiple of worker cores. **Fixes gap 1** | A |
| `num_worker_replicas` | 1…n | 1 | `citus.shard_replication_factor` | write amplification vs. availability. **Verify**: the YCSB script says "only citus enterprise"; statement-based replication may be deprecated in our version | B |
| `dimensions` | reference, distributed | reference | TPC-H script variant (as SSB `-xdim`) | reference tables make dimension joins local; distributed + colocated saves memory and load time at large SF | A |
| `access_method` | heap, columnar | heap (`-xcol` → columnar) | `USING columnar` | scan volume for OLAP; no updates/indexes | exists |
| `columnar_compression` | none, lz4, zstd | zstd | `alter_columnar_table_set` | CPU vs. bytes read | B |
| `columnar_stripe_row_limit`, `columnar_chunk_group_row_limit` | e.g. 150000 / 10000 | Citus defaults | same | granularity of chunk skipping and compression ratio | C |
| `fillfactor` | as PostgreSQL | 100 | on shards via coordinator DDL | as PostgreSQL | B |

TPC-C (BenchBase): distribution column `w_id` is the only sensible one; keep
fixed. HammerDB: no DDL hook (would need a post-build
`alter_distributed_table(shard_count => …)`).

#### CockroachDB — YCSB only

(BenchBase TPC-C creates the CockroachDB schema itself; bexhoma's folder has
only check and reset scripts.)

| Key | Values | Default | Where | Why | Prio |
|---|---|---|---|---|---|
| `num_worker_replicas` | 1, 3, 5 | 3 (DBMS default; today `-nwr`) | zone `num_replicas` | Raft write quorum cost | exists |
| `pk_hash` | hash, none | hash | `PRIMARY KEY USING HASH` | spreads sequential inserts (`-xio ordered`) over ranges; costs scans (YCSB e) | A |
| `bucket_count` | 4…64 | cluster setting `sql.defaults.default_hash_sharded_index_bucket_count` | `USING HASH WITH (bucket_count=…)` | write spread vs. scan fan-out; vendor advises testing per workload | B |
| `range_max_bytes` | e.g. 64 MiB – 512 MiB | 512 MiB | zone config | more, smaller ranges = more leaseholders to spread load at small SF | B |
| `pre_split` | 0…n | 0 | `ALTER TABLE … SPLIT AT` | avoids the split/rebalance phase during load | B |
| `column_families` | one, per_field | one | `FAMILY` per YCSB field | a single-field update writes one KV instead of the whole row (YCSB a/f) | B |
| `gc_ttlseconds` | e.g. 600 – 14400 | zone default | zone `gc.ttlseconds` | MVCC garbage in update-heavy runs affects scan cost | C |

#### YugabyteDB — YCSB, TPC-C (BenchBase)

| Key | Values | Default | Where | Why | Prio |
|---|---|---|---|---|---|
| `pk_sharding` | hash, asc | hash | `PRIMARY KEY (ycsb_key HASH / ASC)` | hash: even load, point reads; asc: range scans (YCSB e), hot spot for ordered inserts | A |
| `num_tablets` | 0 = auto, n | auto (`ysql_num_shards_per_tserver` + auto-split) | `SPLIT INTO n TABLETS` | parallelism and leader spread from the start; vendor starts with ~8 per tserver | A |
| `colocated` | false, true | false | database created `WITH colocation = true` (TPC-C small tables) | one tablet per small table/index costs RPCs; colocation can help a lot. **Not scripts only**: the database must exist before BenchBase connects (SUT/connection setup) | B |
| `replica_placement` | RF per table | cluster RF | tablespace `replica_placement` (JSON) | per-table RF without redeploy; needs safe filling (braces) | C |

The BenchBase TPC-C schema waits 300 s for tablet splitting; with
`num_tablets` set, that wait could shrink.

#### TiDB — YCSB, TPC-C (BenchBase)

| Key | Values | Default | Where | Why | Prio |
|---|---|---|---|---|---|
| `num_worker_replicas` | 1, 3, 5 | 3 (DBMS default; today `-nwr`) | `SET CONFIG pd max-replicas` | Raft quorum | exists |
| `clustered` | clustered, nonclustered | server default | `PRIMARY KEY (…) CLUSTERED/NONCLUSTERED` | clustered saves a lookup; nonclustered is needed for `SHARD_ROW_ID_BITS` | A |
| `shard_row_id_bits` | 0…6 | 0 | table option (nonclustered only) | spreads insert hot spot; too large = more RPCs | B |
| `pre_split_regions` | 0…n (2^n regions) | 0 | table option | regions on all TiKV from the start instead of splitting during load | A |
| `split_regions` | 0…n | 0 | `SPLIT TABLE … BETWEEN … REGIONS n` | same, for VARCHAR keys | B |
| `tiflash_replica` | 0…n | 0 | `ALTER TABLE … SET TIFLASH REPLICA n` | columnar replica for analytical queries; needs TiFlash in the template | C |

#### MySQL — TPC-H, TPC-DS, SSB, YCSB, TPC-C (BenchBase)

| Key | Values | Default | Where | Why | Prio |
|---|---|---|---|---|---|
| `row_format` | DYNAMIC, COMPRESSED | DYNAMIC | table option | COMPRESSED (+`key_block_size` 8/4): less I/O, more CPU, buffer pool holds both copies | B |
| `page_compression` | none, zlib, lz4 | none | `COMPRESSION='…'` | transparent page compression via hole punching; depends on file system | C |
| `collation` | utf8mb4_0900_ai_ci, utf8mb4_bin, latin1 | utf8mb4_0900_ai_ci | YCSB/BenchBase TPC-C tables | cost of VARCHAR key comparisons (YCSB PK is VARCHAR(255)) | B |
| `stats_sample_pages` | 20…n | 20 | table option `STATS_SAMPLE_PAGES` | quality of TPC-H/TPC-DS plans | B |
| `histograms` | off, on | off (plain `ANALYZE TABLE`) | `ANALYZE TABLE … UPDATE HISTOGRAM ON …` | better selectivity for non-indexed filters in TPC-H | B |
| `partition_by` | none, year | none | lineitem/orders | pruning; not with foreign keys | C |

InnoDB indexes are always B-trees (`USING HASH` is ignored), so no
index-type parameter.

#### MariaDB — TPC-H, TPC-DS, SSB, YCSB, TPC-C (BenchBase)

| Key | Values | Default | Where | Why | Prio |
|---|---|---|---|---|---|
| `engine` | InnoDB, Aria, ColumnStore | InnoDB | `ENGINE = {engine}` in the **current** `initschema-tpch.sql` (template is stale, see gap 3) | storage engine is the largest single factor for OLAP; ColumnStore needs its plugin/image | A |
| `page_compressed` | 0/1 + `page_compression_level` | 0 | table option | as MySQL page compression | C |
| `row_format`, `collation` | as MySQL | | | as MySQL | B |
| `histograms` | off, on | **probably on**: plain `ANALYZE TABLE` in MariaDB ≥ 10.4 collects engine-independent statistics with histograms by default; **verify on the image** | `ANALYZE TABLE … PERSISTENT FOR ALL` | optimizer statistics | B |

#### ClickHouse / ClickHouseCluster — TPC-H, TPC-DS, SSB

| Key | Values | Default | Where | Why | Prio |
|---|---|---|---|---|---|
| `order_by` | key, date | current sort keys | `ORDER BY` of the large tables (e.g. lineitem by `l_shipdate` vs `l_orderkey`) | primary index pruning; the most important physical-design choice in ClickHouse | A |
| `partition_by` | none, month, year | none | `PARTITION BY toYYYYMM(…)` | partition pruning; too many parts slow inserts | B |
| `index_granularity` | 1024…16384 | 8192 | `SETTINGS index_granularity` | finer granules filter more, bigger index | B |
| `codec` | LZ4, ZSTD(1), ZSTD(3), Delta+ZSTD | LZ4 | per column `CODEC(…)` | bytes read vs. CPU | B |
| `low_cardinality` | off, on | off | `LowCardinality(String)` for flags, modes, segments | dictionary encoding speeds group-by and filters | B |
| `skip_indexes` | none, minmax, bloom | none | `INDEX … TYPE …` (as an Index variant) | skips granules for non-key filters | C |
| `sharding_key` (Cluster) | orderkey, rand() | orderkey: orders and lineitem are **already** co-located (`Distributed(…, o_orderkey / l_orderkey)`) | `Distributed(…, key)` | with `distributed_product_mode = global` (template) joins are broadcast anyway; co-location only pays off with `local`, a session setting ([plan-session-parameters.md](plan-session-parameters.md)). Sweep = sharding key × product mode | B |
| `dimensions` (Cluster) | replicated, distributed | distributed (TPC-H) / `-xdim` (SSB) | script variant | as SSB `-xdim`; extend to TPC-H/TPC-DS | A |

`ReplicatedMergeTree` paths use `{shard}`/`{replica}` macros; safe filling
leaves them untouched.

#### MonetDB — TPC-H, TPC-DS, SSB, YCSB

Little physical design to choose: PK/FK constraints (exist as Constraints
variant) and `CREATE ORDERED INDEX` on date columns (C). Check the image
version before adding index types; imprints changed between releases.

#### Others

- **CedarDB**: PostgreSQL syntax, own storage; no known DDL knobs worth a
  sweep. None proposed.
- **Redis, Dragonfly**: no DDL; everything is a server flag → `--set`.
- **SingleStore, OmniSci, Kinetica, Exasol, DB2, SAP HANA, SQL Server,
  Oracle, MemSQL, MariaDBCS**: script folders without a driver; out of scope.
  Their orphan placeholders can stay until a driver uses them.

## Further DDL options (all DBMS)

- **Data types**: TPC-H `DECIMAL(15,2)` vs `DOUBLE PRECISION`. Citus uses
  DOUBLE, PostgreSQL DECIMAL(15,2): today a hidden difference between the
  two. Key `numeric_type`, placeholder in the column definitions.
- **Extended statistics**: `CREATE STATISTICS` on correlated TPC-H columns
  (e.g. `l_shipdate`/`l_commitdate`/`l_receiptdate`); boolean key selecting
  an extra statistics script.
- **Statistics target per column**: `ALTER TABLE … ALTER COLUMN … SET
  STATISTICS n` (PostgreSQL, Citus); MySQL/MariaDB see `stats_sample_pages`
  and histograms above.

### More candidates (not yet prioritized against the above)

Each with the hypothesis a sweep would test.

| Key | DBMS | Benchmarks | Values | Hypothesis |
|---|---|---|---|---|
| `covering_indexes` | PostgreSQL/Citus (`INCLUDE`), YugabyteDB (`INCLUDE`), CockroachDB (`STORING`, YCSB only) | TPC-C (BenchBase), TPC-H | off, on | index-only scans save heap lookups; in distributed DBMS also a second remote read per row |
| `string_type` | PostgreSQL, Citus, MySQL, ClickHouse (`FixedString`) | TPC-H, SSB | spec (`CHAR(n)`), `VARCHAR(n)`, `TEXT` | CHAR padding widens rows and costs in comparisons; spec types vs. what each DBMS prefers |
| `column_order` | PostgreSQL, Citus | TPC-C (BenchBase), TPC-H | spec, aligned | PostgreSQL pads columns to alignment; reordering (8-byte first) shrinks rows (EDB does this for TPROC-C) |
| `primary_keys` | MySQL, MariaDB (InnoDB) | TPC-H, TPC-DS | on, off | InnoDB clusters by PK; without one, a hidden row id: changes load time and join locality of lineitem/orders |
| `btree_dedup` | PostgreSQL, Citus | TPC-H | on, off | `deduplicate_items` (default on) shrinks non-unique FK indexes; effect on size and scan time |
| `pk_order` | YugabyteDB, CockroachDB | YCSB d | asc, desc | workload d reads the latest inserts; desc keeps them at the start of a range. Only with `-xio ordered` (hashed keys are not adjacent), on CockroachDB only with `pk_hash = none` |
| `distribution_key` | Citus | TPC-H | orderkey, custkey | orderkey: orders⋈lineitem local; custkey: orders⋈customer local, lineitem needs repartition |
| `tpcc_item` | Citus | TPC-C (BenchBase) | reference, distributed | item is read-only and joined with stock: reference avoids remote reads |
| `hash_partitions` | PostgreSQL | TPC-C (BenchBase) | 0, n (by `w_id`) | smaller indexes and less contention per partition; partition-wise plans |
| `projections` | ClickHouse | TPC-H, SSB | none, aggregate | aggregate projections are used transparently by matching queries; cost: load time and size |
| `wide_parts` | ClickHouse | TPC-H, TPC-DS, SSB | default, compact, wide (`min_bytes_for_wide_part`) | many small inserts from parallel loaders produce compact parts; affects merge load during and after loading |
| `tablespace_index` | PostgreSQL | TPC-H, TPC-C (BenchBase) | same, separate volume | indexes on nvme, data on cephcsi (or vice versa); needs a second volume, see [plan-storage-class-sweep.md](plan-storage-class-sweep.md) |

### What each key needs beyond the scripts

All keys need M1. Beyond that:

- **Placeholder in existing scripts only**: `btree_dedup`, `wide_parts`,
  `projections` (post-load script), extended statistics, statistics target,
  `pk_order`, `tpcc_item` (today `create_reference_table('item')`),
  `covering_indexes` as index-script variant.
- **Scripts only, but results change**: `numeric_type` (rounding) and
  `string_type` (`CHAR` trailing blanks) make DBMS-Benchmarker's result
  comparison report differences between configurations; expected, needs a
  note in the evaluation.
- **Script variant, not one placeholder**: `distribution_key` (Citus PK must
  contain the distribution column; lineitem has no custkey; customer
  becomes distributed instead of reference), `primary_keys` (FKs of the
  Constraints variant need the referenced keys: forbid the combination),
  `hash_partitions` (partition loop = PL/pgSQL with braces: needs safe
  filling).
- **More than scripts**:
  - `column_order`: loaders `\COPY` positionally (no column list, e.g.
    images/ssb/loader_postgresql/loader.sh) → loader images need column
    lists and a rebuild.
  - `tablespace_index`: second volume in the deployment template and
    storage configuration.
  - YugabyteDB `colocated`: database creation before BenchBase connects.
  - `tiflash_replica` (TiFlash nodes), MariaDB `engine=ColumnStore` (image
    with the plugin).
- **Not reachable by scripts**: HammerDB TPC-C (all DBMS) and BenchBase
  TPC-C on CockroachDB. Only post-build `ALTER`s are possible, and e.g.
  `fillfactor` set after loading affects only new pages.

Companion, not DDL: BRIN and ClickHouse `order_by` only pay off if the
loader inserts in that order; the load order would be a loader parameter.

Not a placeholder: **index and constraint timing** (before vs after the
load, PK present during the load). The statements stay the same, only the
script order changes, so this is a choice of script list like the existing
`Index`/`Constraints` keys in `cluster.config`.

## Milestones

- **M0** verify gap 2 on the cluster (Citus/CockroachDB YCSB without
  `-nwr`/`-nws`), with `-ks no`.
- **M1** mechanism (Python changes table): fill function, defaults file,
  merge, validation in `process()`, files in the result folder, `-xddl`,
  driver calls removed, unit tests (no-op for all current scripts without a
  defaults file; with a file, filled output = today's script).
- **M1b** sweep: `-xddl` comma lists as cells in `expand_resource_cells()`;
  cluster check with a 2-value sweep and `-rst` (two PVCs, both loaded) and
  a mixed `-dbms` run (unswept DBMS once).
- **M2** wire existing placeholders, scripts only: defaults files for
  ycsb/Citus, ycsb/CockroachDB, ycsb/TiDB, benchbase/tpcc/TiDB; Citus
  `SET citus.shard_count = {num_worker_shards}` into TPC-H, SSB (both
  folders), BenchBase TPC-C; MariaDB `{engine}` into the current
  `initschema-tpch.sql`; delete the stale Citus and MariaDB templates and
  their `SF*-template` keys if unused; rename or delete the CockroachDB
  TPC-H placeholder.
- **M3** priority A keys: PostgreSQL `fillfactor`; CockroachDB `pk_hash`;
  YugabyteDB `pk_sharding`, `num_tablets`; TiDB `clustered`,
  `pre_split_regions`; Citus/ClickHouse `dimensions`; ClickHouse `order_by`.
  Each with a docs test run.
- **M3b** `systems[].ddl` in experiment.yml + catalog capability.
- **M4** priority B keys, one DBMS at a time, each with a docs test run.
- **M5** "More candidates" that need only placeholders or script variants;
  candidates that need images, volumes or loader changes are a separate
  decision.

## Open questions

- Summaries (checked 2026-10-29): the "Connections" section
  ([experiments/base.py:3329-3344](../bexhoma/experiments/base.py#L3329-L3344))
  prints `resources_total`, `load_durability` and `eval_parameters` per
  connection, but **not** `ddl_parameters`. Proposal (no evaluator change):
  the cell expansion also writes the effective DDL values into the clone's
  `eval_parameters`, as Citus already does with `BEXHOMA_SHARDS`; then they
  appear per connection. The result tables (loading, throughput, latency)
  have one row per connection name (`Citus-1`, `Citus-2`) and no parameter
  columns, for resource cells too; a column per swept key there would be an
  evaluator change in all benchmark types. Defer; if needed, one generic
  "cell columns" step for resource and DDL cells together.
- Rename `expand_resource_cells()` to `expand_cells()` once it covers both?
  Cosmetic, touches only experiments/base.py and its callers.

## Sources

- CockroachDB hash-sharded indexes and storage parameters:
  https://www.cockroachlabs.com/docs/v25.3/hash-sharded-indexes,
  https://www.cockroachlabs.com/docs/v26.2/with-storage-parameter
- YugabyteDB sharding and tablet splitting:
  https://docs.yugabyte.com/stable/explore/going-beyond-sql/data-sharding/,
  https://docs.yugabyte.com/stable/architecture/docdb-sharding/tablet-splitting/,
  https://www.yugabyte.com/blog/when-using-yugabytedb-how-many-shards-should-i-break-my-table-into/
- TiDB: https://docs.pingcap.com/tidb/dev/auto-random/,
  https://docs.pingcap.com/tidb/dev/tidb-rowid/,
  https://docs.pingcap.com/tidb/v5.3/high-concurrency-best-practices
- Citus: https://www.citusdata.com/blog/2021/05/03/citus-tips-for-postgres-how-to-alter-distribution-key-shard-count/,
  https://docs.citusdata.com/en/v12.0/faq/faq.html
- ClickHouse: https://clickhouse.com/docs/best-practices/use-data-skipping-indices-where-appropriate
- PostgreSQL: https://www.postgresql.org/about/featurematrix/detail/lz4-compression-for-toast-tables,
  https://www.postgresql.org/about/news/postgresql-18-released-3142/
- HammerDB/fillfactor context: https://www.enterprisedb.com/blog/postgresql-tpc-c-benchmarks-postgresql-12-vs-postgresql-13-performance
