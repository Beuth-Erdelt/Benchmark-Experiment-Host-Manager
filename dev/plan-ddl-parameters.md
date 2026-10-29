# Plan: DDL parameters (placeholders in init scripts)

Status (2026-10-30): **M1, M1b, M2 committed (04a57300); M2b, M2c and the
data-defining parameters committed (8616163b); M3 and `requires` committed
(b730977a); test `Init scripts without errors` committed (21a877b7)**, the
init script fixes it found committed afterwards. Rollout done (reinstall,
115 old volumes deleted), cluster checks A–R OK. Open: `dimensions` (item 14),
M3b, M4, M5, research (item 9). Non-DDL
settings (planner knobs, isolation level, client options):
[plan-session-parameters.md](plan-session-parameters.md) (parked; today:
one experiment per value with `--set` on the same `-rst` PVC).

## Open items

| # | Item | Kind | Section |
|---|---|---|---|
| 14 | `dimensions` for Citus and ClickHouseCluster TPC-H: a DDL key that selects a script folder variant | design open | [Milestones](#milestones) |
| M3b | `systems[].ddl` in experiment.yml + catalog | open | [Milestones](#milestones) |
| M4, M5 | Priority B keys, more candidates | open | [Milestones](#milestones) |
| 9 | Verify: Citus `shard_replication_factor` > 1 in our version; MariaDB histograms by default; CockroachDB `bucket_count` default in v24.2.4 | research | [Candidates](#candidates-per-dbms) |
| 11 | ~30 scripts still say "No curly braces: bexhoma may fill it with str.format()"; obsolete, harmless (durability copies are compared byte by byte) | optional | – |
| 13b | Optional: refuse a post-load step a DBMS has no script for (ClickHouse/ClickHouseCluster constraints, indexes, statistics in TPC-H, TPC-DS, SSB); decide whether missing `.sql` and `.sh` scripts are reported alike (options A/B/C, see below); missing check scripts: `checkschema-tpch` for CedarDB, DatabaseService, PgDuckDB, `checkschema-ycsb` for CedarDB, DatabaseService | open | [Init scripts](#init-scripts-without-errors-item-13) |
| – | Separate: Python client calls (`get_pods` etc. in clusters.py) do not wait for a cluster outage (`MaxRetryError`), crashed check P | open, outside this plan | – |
| – | Volumes with the old names (`bexhoma-storage-citus-nvme-tpch-*`, `bexhoma-storage-monetdb-nvme-tpch-*`, `bxw-bexhoma-worker-…`) created 2026-10-29 by runs with an older bexhoma from another machine; the new version does not find them | that machine needs the new version | [Short names](#short-volume-and-worker-names-decided-2026-10-29) |

Done (details in the sections): items 1–4b (decision B, volume labels and
reuse reporting, token rules, short names, shape and load labels), rollout,
cluster checks A–R, M3 + `requires`, item 13 (test `Init scripts without
errors` and the script fixes it found). Rejected: item 10 (summary columns
per swept key).

## Init scripts without errors (item 13)

Implemented 2026-10-29 (21a877b7): the summary judges the loading logs (SUT
and worker pods) with `script_failed`; PVC labels `errors_<phase>` carry the
count to a reuse (no label: skipped); listed scripts not in the folder are
skipped for loading and reset (missing SQL scripts in `loading_skipped`,
info section "Init Scripts Not in Folder"; missing shell scripts silent);
MariaDB `checkschema` for YCSB, BenchBase TPC-C, HammerDB TPC-C. Re-evaluation
of 433 old results: 312 passed, 75 failed. Cluster checks L (1793306726), M
(1793307081), N (1793301798), O (1793302352) passed, P (1793303111) failed on
CockroachDB `checkschema` as expected.

Fixed 2026-10-30: CockroachDB `DO $$` in `checkschema-ycsb.sql` (v24.2.4 has
no DO, PL/pgSQL needs an enterprise license) → wait loop in
`waitreplicas-ycsb.sh` (YCSB Checks list before `restoredurability.sql`;
check Q 1793311326 OK); MonetDB TPC-DS `initconstraints` one subcommand per
ALTER TABLE (check R 1793311944 OK). Citus TPC-H `initconstraints` was
already fixed in f17ce3a0.

Reporting of missing scripts, open: A) report `.sql` and `.sh` alike and move
`save-snapshot.sh` (Redis, Dragonfly) and `waitreplicas-ycsb.sh`
(CockroachDB) out of the shared YCSB list; B) record every skip, no summary
section; C) mark optional list entries. Recommended: B.

## Mechanism (implemented)

Generic, no per-driver code: the drivers only lost lines.

- **Declarations per script folder**: `experiments/<bench>/<dbms>/ddl-parameters.config`,
  Python dict literal like `queries-*.config`; per key `default`, optional
  `values` (allowed tokens), optional `sql` (token → SQL text),
  `description`. A folder variant (`ssb/Citus/distributed`) without its own
  file uses the parent's. No file = no filling = scripts uploaded unchanged.
- **Defaults reproduce the scripts as they were**, so baselines stay
  comparable. Exception: where the old value was the broken 0 (`-nwr`/`-nws`
  not given), the default is the DBMS default (Citus 32 shards / RF 1,
  CockroachDB and TiDB 3 replicas).
- **Values**: `-xddl KEY=VALUE` (repeatable; a comma list sweeps) and
  `-nwr`/`-nws` > 0 (`num_worker_replicas`/`num_worker_shards`); 0 means
  "not given". Precedence: folder default < `-nwr`/`-nws` < `-xddl`; per-call
  values (`BEXHOMA_SCHEMA` per tenant) on top. With decision B (item 2), a
  reused volume's labels override all of these.
- **Resolution in `process()`** before anything starts
  (`resolve_ddl_parameters()`): per configuration, effective values = folder
  defaults + the given values for the keys the folder declares; a value not
  in `values` or an `-xddl` key no DBMS of the experiment declares → error.
  Keys given by `-xddl` are added as `ddl_<key>` to the evaluation
  parameters (shown per connection in the summary).
- **Safe filling**: only `{key}` of the effective values is replaced; other
  braces (JSON, ClickHouse macros) stay. One fill path for normal and
  tenant-per-schema scripts (tenant scripts get DDL parameters too). Filled
  scripts go to the result folder only
  (`<app>-loading-<configuration>-<script>-...`), never to `experiments/`.
- **Sweep** in `expand_resource_cells()`: configurations are cloned per
  resource cell × combination of the swept keys **their folder declares**
  (one numbering `{base}-{n}`, alias `{base}@{n}`); a DBMS without the keys
  runs once. With decision B, a DDL sweep with `-rst` is refused (item 1).
- Keep schema **variants that change many statements** (reference vs
  distributed dimensions, distribution key, columnar) as script or folder
  variants (as `-xdim` does); a key may select the variant.

### Python changes (as implemented)

| File | Change |
|---|---|
| [bexhoma/ddl_parameters.py](../bexhoma/ddl_parameters.py) (new) | declarations, `-xddl` parsing, combinations, validation, resolution, `sql` mapping, safe fill; `storage_suffix()` to be removed (item 1) |
| [bexhoma/configurations/loading.py](../bexhoma/configurations/loading.py) | `ddl_fill_values()`, `upload_script()`; `prepare_init_dbms()` uses them for normal and tenant scripts (both `str.format` branches gone) |
| [bexhoma/cli_args.py](../bexhoma/cli_args.py) | `-xddl`, `action='append'` |
| [bexhoma/experiments/base.py](../bexhoma/experiments/base.py) | parsing next to `-nwr`/`-nws`, workload info line, `resolve_ddl_parameters()`, DDL combinations in `expand_resource_cells()` |
| [bexhoma/configurations/base.py](../bexhoma/configurations/base.py) | `set_ddl_parameters` merges; `ddl_storage_suffix` in `get_storage_configuration()` (to be removed, item 1) |
| tpch.py, ycsb.py (5×), benchbase.py (3×), hammerdb.py | `set_ddl_parameters(num_worker_*)` calls deleted |
| tests/test_ddl_parameters.py (new, 25), tests/test_ssb.py | unit tests; SSB brace test allows declared keys |

No change: tpcds.py, ssb.py, DBMS-Benchmarker, evaluators, k8s templates,
TPCTC23/ (legacy).

### Folders with declarations (M2)

| Folder | Keys | Script change |
|---|---|---|
| ycsb/Citus | `num_worker_shards`, `num_worker_replicas` | existed |
| tpch/Citus, ssb/Citus (+ `distributed/`), benchbase/tpcc/Citus | `num_worker_shards` | `SET citus.shard_count = {num_worker_shards};` before the first distribution (TPC-H row and columnar, 3 SSB schemas, BenchBase TPC-C) |
| ycsb/CockroachDB, ycsb/TiDB, benchbase/tpcc/TiDB | `num_worker_replicas` | existed |
| tpch/CockroachDB | `num_worker_replicas` | `{num_replicas}` renamed |
| tpch/MariaDB | `engine` (InnoDB, Aria, MyISAM) | `ENGINE = {engine}` per table in the current schema |

Stale templates deleted: tpch/Citus and tpch/MariaDB
`initschema-tpch-template.sql` (the `SF*-template` keys stay for OmniSci).
experiments/README.md has a section "DDL parameters" (to be fixed, item 1).

## Decisions 2026-10-29

### Volume names: B) no DDL values in the name (not implemented, item 1)

Each DBMS keeps one persistent volume per class (and resource cell).

- A DDL sweep with `-rst` is refused (all cells would get the same volume
  name); without `-rst` (ephemeral, no PVC) it works. Persisted variants:
  one value per experiment.
- A reused volume brings its DDL values along (labels, below); `-rsr`
  reloads it with the requested values, which replaces the variant it held.
- Reason: the name can never describe the data completely (`--set` values
  like `innodb_page_size` or MariaDB `default_storage_engine`, script
  versions such as the MariaDB PK change of 2026-10-22, generator/loader
  versions), so it should not pretend to.

**Rejected: A) DDL values in the name** (deterministic hash of the
non-default values, `-d<6 hex>`, 8 characters; implemented as `-ddl<6 hex>`
and verified in check A). What A would have given:
- several DDL variants of one DBMS loaded at the same time (InnoDB and
  Aria, 8 and 32 shards), each found again by every later experiment with
  the same values, from a sweep or a single value;
- DDL sweeps with `-rst`, each cell on its own reusable volume;
- no reload when a comparison is repeated (matters at large SF, where
  loading takes hours);
- defaults add nothing, so existing volumes keep their names.

Costs: 8–10 characters in names near the 52-character limit of StatefulSet
names; incomplete as a description of the data. Revisit if keeping several
variants loaded becomes necessary.

**Also rejected:** numbered DDL cells (`-1`, `-2`) in the volume name: they
only separate cells within one experiment; a later experiment cannot know
what `-2` holds (true for resource cells today, too).

### DDL values as volume labels (not implemented, item 2)

- At load time, write `ddl_<key>: <token>` per effective value (defaults
  too) next to the existing loading labels, on the volume
  `get_volume_to_label()` returns (the SUT volume, or the first worker volume
  where the SUT has none, e.g. Redis/Dragonfly). Existing PVC labels
  (checked 2026-10-29): no prefix, snake_case keys ≤ 22 characters, none
  starting with `ddl_`.
- Visible outside bexhoma: `kubectl get pvc -L ddl_engine`, selectors
  `-l ddl_engine=Aria`.
- Later, data-defining `--set` values the same way, but as one annotation
  (JSON; key like a label key, value free, all annotations ≤ 256 KiB),
  since their values (paths, `256MB`) do not fit label rules.

### Reuse: the volume's values win, differences are reported (item 2)

No stop. When a configuration finds its volume loaded (`storage_reused`,
existing mechanism in lifecycle.py), it reads the `ddl_*` labels before
anything is filled.

- Effective values = the volume's values. They fill every script that still
  runs on the reused data (post-load and reset scripts per round) and are
  what the connection info and the `ddl_<key>` evaluation parameters record.
  A rerun on an old volume needs no `-xddl`: the values are implicit in the
  volume.
- Per key, compared with what was requested:

  | Requested | Volume label | Effective | Reported |
  |---|---|---|---|
  | not given (folder default) | present | volume's value | info line "taken from the volume" |
  | given, same value | present | same | test passed |
  | given, other value | present | **volume's value** | **test failed**, names requested and volume value, hint `-rsr` |
  | any | missing (loaded before labels or before the key existed) | folder default, marked *assumed* | **test skipped** "unknown, default assumed" |
  | – | label of a key the folder no longer declares | ignored | info line "unknown key on the volume" |

- "Given" = from `-xddl`, `-nwr`/`-nws` > 0 or `systems[].ddl` in
  experiment.yml (kept apart already: `ddl_assignments`, `ddl_keys_given`).
- Printed at start, e.g. `Citus-1 : volume loaded with num_worker_shards=8
  (requested 64): the run uses the volume's values; -rsr reloads`.
- **Summary**: section "Reused Storage" (`_show_loading_provenance`) gets
  one line per configuration with the values taken from the volume, the
  differences (requested → volume) and the assumed keys. New test, one per
  experiment like `Loading measured in this experiment`:
  `DDL parameters as requested` — passed when all match, failed with the
  differing configurations and keys, skipped when only assumed values remain
  (or nothing was given and nothing reused).
- **Connection**: `ddl_parameters` (effective), `ddl_requested`,
  `ddl_source` (`loaded` | `volume` | `assumed` per key).
- **Agent report**: lists every test already
  ([docs/AgentReport.md](../docs/AgentReport.md)); add a validity rule:
  with `DDL parameters as requested` failed, results describe the volume's
  DDL values; compare configurations only by their effective values.

### Tokens and declarations: label-compatible, exact round trip (item 3)

Kubernetes rules ("Labels and Selectors") and what follows:

- **Label key** (no prefix): ≤ 63 characters, `[A-Za-z0-9_.-]`, first and
  last alphanumeric. With `ddl_` and the placeholder syntax, a declared key
  must match `^[A-Za-z]([A-Za-z0-9_]{0,57}[A-Za-z0-9])?$` (≤ 59 characters,
  no trailing `_`).
- **Label value**: ≤ 63 characters, `[A-Za-z0-9_.-]`, first and last
  alphanumeric. Tokens (`-xddl`, declared `default` and `values`) must match
  `^[A-Za-z0-9]([A-Za-z0-9_.-]{0,61}[A-Za-z0-9])?$`; today's `-xddl` rule
  (`[A-Za-z0-9_.+-]+`) is too loose. Negative numbers are not valid values:
  a token with an `sql` mapping (`unlimited` → `-1`). Only the token is
  stored, never SQL text.
- **Round trip without type conflicts** (labels are strings): values are
  canonical strings everywhere (fill, `sql` mapping and comparison already
  use `str()`).
  - `load_declarations()` turns `default` and `values` into strings; the
    file may hold only strings and ints (no bool, no float).
  - Optional `'type': 'int'`: tokens normalised on parsing
    (`str(int(token))`), so `032`, `+32` give `32`.
  - Bools as tokens with `values` (`['on', 'off']`) and an `sql` mapping;
    floats only as tokens with `values`.
  - Keys with `values` accept only the exact spelling (label values are
    case-sensitive): `engine=innodb` is refused at the start.
  - Label name ↔ key: `ddl_` + key, case-sensitive, one-to-one.
- `load_declarations()` checks keys, defaults and `values` of every file
  against these rules, so a bad entry fails at the start, not when the
  volume is labelled after the load. Unit test over all files in
  `experiments/`: value → label → value is the identity and every label is
  valid.

## Short volume and worker names (decided 2026-10-29)

**Decided**: do it; deleting all bexhoma volumes is accepted (each is loaded
once more under its new name). Abbreviations confirmed, SUT prefix kept,
deletion scope confirmed (2026-10-29). Details:

- **Rule** (corrected): the abbreviation is chosen by the **storage name**,
  not by the configuration's DBMS: the longest `dockers` name
  (case-insensitive) that the storage name starts with, followed by `-` or
  the end, is replaced by that DBMS's abbreviation. Reason: PGBouncer uses
  PostgreSQL's volume (`storageConfiguration = 'postgresql'`); longest match
  first so `clickhousecluster` wins over `clickhouse`.
- **Abbreviations** (confirmed; same 17 DBMS in both config files):
  PostgreSQL `pg`, PgDuckDB `pgd`, Citus `ci`, CockroachDB `cr`, YugabyteDB
  `yb`, TiDB `ti`, MySQL `my`, MariaDB `ma`, MonetDB `mo`, ClickHouse `ch`,
  ClickHouseCluster `chc`, Redis `rd`, Dragonfly `df`, Hardware `hw`; none
  for PGBouncer (uses `pg`), DatabaseService (no volume) and
  DragonflyCluster: its configurations use the storage name `dragonfly`
  ([ycsb.py:713](../ycsb.py#L713)), so their worker volumes become `df`
  (`bxw-bx-w-df-…`); the SUT has no volume. CedarDB has no `dockers` entry
  and keeps `cedardb`.
- **Found, independent of abbreviations**: Dragonfly's cluster mode
  (`-nw > 0`, sharded) and replica mode (`-nwr > 0`, DragonflyReplica, all
  data on worker-0) use the same storage name and therefore the same worker
  volume names, so a replica run can reuse a cluster run's volumes with
  another data layout. Fix: storage name `dfr` for the replica mode, one
  line in ycsb.py; part of M2c. More such cases: see
  [Data-defining parameters beyond DDL](#data-defining-parameters-beyond-ddl-proposal-2026-10-29-accepted-in-principle).
- Workers: `bx-w-…` for `worker`, `bx-<component>-…` otherwise (`bx-pd`,
  `bx-tikv`, `bx-store`); hash guard above 52 characters.
- SUT volumes keep the prefix `bexhoma-storage-…` (far from the 253 limit;
  `experimentsmanager.py` and others recognise the prefixes).
- **Deletion at rollout**: only PVCs with `app=bexhoma`, `component=storage`
  and the `bxw-…` worker volumes; **not** `bexhoma-data`, `bexhoma-results`
  or other PVCs of the namespace (one with `role: model-server` exists).
  List first, delete only when no experiment runs.

Background:

Worker StatefulSet names `bexhoma-<component>-<volume name>-<storage_label>`
must stay ≤ 52 characters (Kubernetes adds `-<10 hex>` for the pod label
`controller-revision-hash`, ≤ 63); over 63 the headless Service is refused
too. Already over 52 without DDL: CockroachDB BenchBase tpcc-1600 on cephcsi
(54), ClickHouseCluster SSB-flat SF100 on cephcsi (53). Redis/Dragonfly use
`bx-w-…` (set in ycsb.py since 156a2333, 2025-03-20, because Redis limits
hostname length); the others do not. Worker volumes are named by the
`volumeClaimTemplate` `bxw`: `bxw-<StatefulSet>-<ordinal>` (≤ 253, no issue).

Proposal (generic):
- Abbreviation per DBMS in `cluster.config` and `k8s-cluster.config`
  (`dockers.<DBMS>.abbreviation`: `pg`, `my`, `ma`, `mo`, `ci`, `cr`, `yb`,
  `ti`, `ch`, `chc`, `rd`, `df`, `cd`, `pgd`, ...), applied in
  `get_storage_configuration()` to the start of the storage name
  (`postgresql-schema-16` → `pg-schema-16`), so SUT and worker volumes change
  together (a renamed worker volume next to a loaded coordinator volume
  would skip loading into empty workers). Without an abbreviation: as today.
- Workers always `bx-<w|component>-…` (TiDB keeps `pd`/`tikv` apart); the
  Redis/Dragonfly special case in ycsb.py goes.
- Hash-shortening in `get_worker_name()` only above 52 characters, as a
  last line of defence (names that work keep theirs).
- Worst case afterwards: `bx-w-` + `chc` + cell + `-cephcsi` +
  `-benchbase-tpcc-1600` = 39 (49 with the rejected DDL part).
- Not possible: ClickHouseCluster with ClickHouse's name, since volumes are
  found by name alone and the coordinator volume (only Distributed tables)
  would be found by a single-node ClickHouse run.
- Cost: every volume name changes (2026-10-29: 120 PVCs, ~76 volume sets):
  each is loaded once more; old PVCs stay until deleted (list to be
  generated, not deleted automatically).

## Data-defining parameters beyond DDL (proposal 2026-10-29, accepted in principle)

On reuse, bexhoma checks only the storage class
([lifecycle.py:656](../bexhoma/configurations/lifecycle.py#L656)); it copies
the loading labels (`loaded`, `index`, times) but compares nothing else.
Cases with two variants under one volume name:

| Case | Differs | Reuse today |
|---|---|---|
| Dragonfly cluster (`-nw > 0`) vs replica (`-nwr > 0`) | layout over the workers | same worker volumes |
| Number of workers `-nw` (Citus, CockroachDB, YugabyteDB, TiDB, ClickHouseCluster, Redis/Dragonfly cluster) | not in the name | `-nw 2` → `4`: SUT volume "loaded", workers 0–1 reused, 2–3 new and empty (Citus/ClickHouseCluster: data only on old workers; Redis: slots wrong; CockroachDB/TiDB: rebalance during the measurement) |
| Citus TPC-H heap vs columnar (`-xcol`) | table format | both `citus` + `tpch-<SF>` |
| Post-load variants `-xii/-xic/-xis` (all DBMS) | indexes, constraints, statistics | run with `-xii` on a volume loaded without: loading (and the index script) skipped, runs without indexes; label `index` exists but is not compared |
| YCSB `-xio hashed/ordered` | physical key order | same volume |
| `-nwr`/`-nws` | shards, replicas | covered by DDL labels (M2b) |

Already handled: SSB schema/dimension variants via `storage_label`
(`ssb-flat-<SF>`, `ssb-distributed-<SF>`); tenancy via the storage name.

Three classes:

| Class | Examples | Where | Reuse with a difference |
|---|---|---|---|
| Template / mode, fixed for the life of a deployment | Dragonfly replica vs cluster | **name**: storage name `dfr` for the replica mode (not mapped by the abbreviation rule, as it starts with no DBMS name) | separate volumes |
| Shape, may change during a run in a future feature | `num_worker` | **label** `shape_num_worker` (+ `shape_state`) | **refused** (the run cannot take the volume's shape); `-rsr` reloads |
| Content, the run can take the volume's values | DDL values, script variant (`Schema-Columnar`), post-load variant (`Index_and_Constraints`, …), `-xio` | **labels** `ddl_*`, `load_*` | volume's values win, reported; the test becomes `Data parameters as requested` (DDL included) |

**Worker count not in the name** (first idea `ci-w4-…`, revised): a
StatefulSet scales in place under its name, creating `bxw-<StatefulSet>-3`
from the same `volumeClaimTemplate`, and cannot be renamed, so a count in
the name would be wrong after the first scaling step, and a later run with
the old count would mount workers 0–2 and miss data moved to worker 3.

**Future: shape changes during an experiment** (e.g. 3 → 4 workers while
observing the benchmark):
- After every scaling step, update `shape_num_worker` on the volume
  `get_volume_to_label()` returns; `shape_state: changing` while data is
  redistributed (Citus rebalance, Redis slot migration, CockroachDB/TiDB
  rebalancing), `stable` afterwards. A volume left `changing` (run aborted
  mid-rebalance) is never reused.
- Scale-in: delete the released worker volume, or set
  `persistentVolumeClaimRetentionPolicy: whenScaled: Delete` on the
  StatefulSets; otherwise Kubernetes keeps `bxw-…-3`, and the next
  scale-out mounts it again with stale data.
- Names, pod patterns of the monitoring and worker volumes follow the
  StatefulSet, so nothing else needs to change for the new pod
  `<StatefulSet>-3`.
- A reuse with another shape could later adapt instead of being refused:
  start with the volume's shape, then scale to the requested one; that is
  the scaling feature itself.

## Background: before this plan

- Drivers called `config.set_ddl_parameters(**kwargs)`, which replaced the
  dict. Only `num_worker_replicas`/`num_worker_shards` (`-nwr`/`-nws`,
  default 0) were set, for Citus, CockroachDB, TiDB, Redis, Dragonfly.
- With a non-empty dict, every load-step script (init, index, check,
  durability, reset) was filled with `str.format(**ddl_parameters)`, written
  as `filled_<script>` into `experiments/<bench>/<dbms>/` and uploaded.
  Tenant-per-schema scripts were filled with `BEXHOMA_SCHEMA` only, ignoring
  DDL parameters.

Placeholders found (2026-10-29):

| Placeholder | Script | Used for | Set by | Reachable? |
|---|---|---|---|---|
| `{num_worker_shards}`, `{num_worker_replicas}` | ycsb/Citus/initschema-ycsb.sql | shard count, RF | ycsb.py | yes |
| `{num_worker_replicas}` | ycsb/CockroachDB/initschema-ycsb.sql, checkschema-ycsb.sql | zone `num_replicas`, check | ycsb.py | yes |
| `{num_worker_replicas}` | ycsb/TiDB, benchbase/tpcc/TiDB initschema | PD `max-replicas` | ycsb.py, benchbase.py | yes |
| `{BEXHOMA_SCHEMA}` | tpch/PostgreSQL/*-tpch-schema.sql, benchbase/tpcc/PostgreSQL/*-benchbase-schema.sql | tenant schema | loading.py | yes |
| `{num_worker_shards}`, `{num_worker_replicas}` | tpcc/Citus/initschema-tpcc-tmp.sql | shard count, RF | hammerdb.py | no: not in any script list |
| `{shard_count}`, `{replication_count}` | tpch/Citus/initschema-tpch-template.sql | shard count, RF | nobody | no (`KeyError`); deleted |
| `{num_replicas}` | tpch/CockroachDB | zone | nobody | no; renamed |
| `{engine}` | tpch/MariaDB/initschema-tpch-template.sql | engine | nobody | no; moved to current schema, template deleted |
| `{fragment_size}`, `{shard_count}` | tpch/OmniSci | | nobody | no (legacy) |

Gaps found, all fixed by M1/M2 except where noted:
1. `-nws` had no effect on Citus TPC-H, SSB and BenchBase TPC-C (always 32
   shards); fixed. HammerDB TPC-C still builds its own schema (no hook).
2. `-nwr`/`-nws` default 0 would have set 0 shards/replicas; now "not given".
3. Orphan, stale placeholders; deleted or wired.
4. Filled files in the source tree, shared by configurations; now per
   configuration in the result folder (36 old files deleted).
5. `str.format` broke on any literal brace and raised `KeyError` for unset
   keys; now safe filling.

## Candidates per DBMS

Priority: **A** = cheap, large or well-known effect, belongs in the first
round; **B** = useful sweep; **C** = later or only with extra deployment.
"Default" is the current, hard-coded behaviour.

Reach (corrected 2026-10-29): DDL keys reach TPC-C only where bexhoma creates
the schema: BenchBase on **Citus and YugabyteDB**. HammerDB (all DBMS) and
BenchBase on PostgreSQL, MySQL, MariaDB, TiDB and CockroachDB create the
schema themselves; bexhoma's scripts there are placeholders. "TPC-C
(BenchBase)" in the tables below applies to Citus and YugabyteDB only.

#### PostgreSQL (also PgDuckDB, DatabaseService) — TPC-H, TPC-DS, SSB, YCSB, TPC-C (BenchBase)

| Key | Values | Default | Where | Why it matters | Prio |
|---|---|---|---|---|---|
| `fillfactor` | 50–100 | 100 | `WITH (fillfactor=…)` on usertable / BenchBase TPC-C tables | free space per page enables HOT updates: fewer index writes and less bloat for YCSB a/b/f and TPC-C; check via `n_tup_hot_upd` / `n_tup_upd` | A |
| `index_method` | btree, hash, brin | btree | TPC-H/TPC-DS index scripts | hash: smaller, faster equality on join keys; brin on dates (`l_shipdate`, `o_orderdate`) tiny and cheap when data is loaded in date order | B |
| `partition_by` | none, year | none | lineitem/orders (TPC-H), store_sales (TPC-DS) | partition pruning for date-range queries; changes plans and parallelism | B |
| `cluster_on` | none, a date index | none | after load: `CLUSTER` | physical order makes BRIN and range scans effective | C |
| `toast_compression` | pglz, lz4 | pglz | `ALTER TABLE … SET COMPRESSION` | only affects values > ~2 kB: YCSB rows (10 × 100 B) and TPC-H rows stay below, so **expected no effect** for current benchmarks | C |
| `autovacuum_scale_factor` | e.g. 0.01–0.2 | server default | table storage parameter | earlier vacuum on hot OLTP tables keeps bloat and latency stable in long runs | B |

#### Citus — TPC-H, SSB, YCSB, TPC-C (BenchBase)

| Key | Values | Default | Where | Why | Prio |
|---|---|---|---|---|---|
| `num_worker_shards` | 1…n | 32 | `SET citus.shard_count` | parallelism per query vs. per-shard overhead; rule of thumb: a small multiple of worker cores | **done** (M2) |
| `num_worker_replicas` | 1…n | 1 | `citus.shard_replication_factor` (YCSB) | write amplification vs. availability. **Verify** (item 9): the YCSB script says "only citus enterprise"; statement-based replication may be deprecated in our version | B |
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
| `num_worker_replicas` | 1, 3, 5 | 3 | zone `num_replicas` | Raft write quorum cost | **done** (M2) |
| `pk_hash` | hash, none | hash | `PRIMARY KEY USING HASH` | spreads sequential inserts (`-xio ordered`) over ranges; costs scans (YCSB e) | A |
| `bucket_count` | 4…64 | cluster setting `sql.defaults.default_hash_sharded_index_bucket_count` (**verify** default in v24.2.4, item 9) | `USING HASH WITH (bucket_count=…)` | write spread vs. scan fan-out; vendor advises testing per workload | B |
| `range_max_bytes` | e.g. 64 MiB – 512 MiB | 512 MiB | zone config | more, smaller ranges = more leaseholders to spread load at small SF | B |
| `pre_split` | 0…n | 0 | `ALTER TABLE … SPLIT AT` | avoids the split/rebalance phase during load | B |
| `column_families` | one, per_field | one | `FAMILY` per YCSB field | a single-field update writes one KV instead of the whole row (YCSB a/f) | B |
| `gc_ttlseconds` | e.g. 600 – 14400 | zone default | zone `gc.ttlseconds` | MVCC garbage in update-heavy runs affects scan cost | C |

#### YugabyteDB — YCSB, TPC-C (BenchBase)

| Key | Values | Default | Where | Why | Prio |
|---|---|---|---|---|---|
| `pk_sharding` | hash, asc | hash | `PRIMARY KEY (ycsb_key HASH / ASC)` | hash: even load, point reads; asc: range scans (YCSB e), hot spot for ordered inserts | A |
| `num_tablets` | 0 = auto, n | auto (`ysql_num_shards_per_tserver` + auto-split) | `SPLIT INTO n TABLETS` | parallelism and leader spread from the start; vendor starts with ~8 per tserver | A |
| `colocated` | false, true | false | database created `WITH colocation = true` (TPC-C small tables) | one tablet per small table/index costs RPCs. **Not scripts only**: the database must exist before BenchBase connects | B |
| `replica_placement` | RF per table | cluster RF | tablespace `replica_placement` (JSON; safe filling keeps the braces) | per-table RF without redeploy | C |

The BenchBase TPC-C schema waits 300 s for tablet splitting; with
`num_tablets` set, that wait could shrink.

#### TiDB — YCSB, TPC-C (BenchBase)

| Key | Values | Default | Where | Why | Prio |
|---|---|---|---|---|---|
| `num_worker_replicas` | 1, 3, 5 | 3 | `SET CONFIG pd max-replicas` | Raft quorum | **done** (M2) |
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
| `engine` | InnoDB, Aria, MyISAM | InnoDB | `ENGINE = {engine}` (TPC-H) | storage engine; check A: SF1 load Aria 106 s vs InnoDB 415 s. ColumnStore needs an image with the plugin | **done** (M2, TPC-H) |
| `page_compressed` | 0/1 + `page_compression_level` | 0 | table option | as MySQL page compression | C |
| `row_format`, `collation` | as MySQL | | | as MySQL | B |
| `histograms` | off, on | **probably on**: plain `ANALYZE TABLE` in MariaDB ≥ 10.4 collects engine-independent statistics with histograms; **verify on the image** (item 9) | `ANALYZE TABLE … PERSISTENT FOR ALL` | optimizer statistics | B |

#### ClickHouse / ClickHouseCluster — TPC-H, TPC-DS, SSB

| Key | Values | Default | Where | Why | Prio |
|---|---|---|---|---|---|
| `order_by` | key, date | current sort keys | `ORDER BY` of the large tables (e.g. lineitem by `l_shipdate` vs `l_orderkey`) | primary index pruning; the most important physical-design choice in ClickHouse | A |
| `partition_by` | none, month, year | none | `PARTITION BY toYYYYMM(…)` | partition pruning; too many parts slow inserts | B |
| `index_granularity` | 1024…16384 | 8192 | `SETTINGS index_granularity` | finer granules filter more, bigger index | B |
| `codec` | lz4, zstd1, zstd3, delta_zstd (tokens, `sql` mapping) | LZ4 | per column `CODEC(…)` | bytes read vs. CPU | B |
| `low_cardinality` | off, on | off | `LowCardinality(String)` for flags, modes, segments | dictionary encoding speeds group-by and filters | B |
| `skip_indexes` | none, minmax, bloom | none | `INDEX … TYPE …` (as an Index variant) | skips granules for non-key filters | C |
| `sharding_key` (Cluster) | orderkey, rand | orderkey: orders and lineitem are **already** co-located | `Distributed(…, key)` | with `distributed_product_mode = global` (template) joins are broadcast anyway; co-location only pays off with `local`, a session setting ([plan-session-parameters.md](plan-session-parameters.md)) | B |
| `dimensions` (Cluster) | replicated, distributed | distributed (TPC-H) / `-xdim` (SSB) | script variant | as SSB `-xdim`; extend to TPC-H/TPC-DS | A |

#### MonetDB — TPC-H, TPC-DS, SSB, YCSB

Little physical design to choose: PK/FK constraints (exist as Constraints
variant) and `CREATE ORDERED INDEX` on date columns (C). Check the image
version before adding index types; imprints changed between releases.

#### Others

- **CedarDB**: PostgreSQL syntax, own storage; no known DDL knobs worth a
  sweep.
- **Redis, Dragonfly**: no DDL; everything is a server flag → `--set`.
- **SingleStore, OmniSci, Kinetica, Exasol, DB2, SAP HANA, SQL Server,
  Oracle, MemSQL, MariaDBCS**: script folders without a driver; out of scope.

### Further DDL options (all DBMS)

- **Data types**: TPC-H `DECIMAL(15,2)` vs `DOUBLE PRECISION`. Citus uses
  DOUBLE, PostgreSQL DECIMAL(15,2): today a hidden difference between the
  two. Key `numeric_type`.
- **Extended statistics**: `CREATE STATISTICS` on correlated TPC-H columns
  (e.g. `l_shipdate`/`l_commitdate`/`l_receiptdate`); boolean key selecting
  an extra statistics script.
- **Statistics target per column**: `ALTER TABLE … ALTER COLUMN … SET
  STATISTICS n` (PostgreSQL, Citus).

### More candidates (not yet prioritized)

| Key | DBMS | Benchmarks | Values | Hypothesis |
|---|---|---|---|---|
| `covering_indexes` | PostgreSQL/Citus (`INCLUDE`), YugabyteDB (`INCLUDE`), CockroachDB (`STORING`, YCSB only) | TPC-C (BenchBase), TPC-H | off, on | index-only scans save heap lookups; in distributed DBMS also a second remote read per row |
| `string_type` | PostgreSQL, Citus, MySQL, ClickHouse (`FixedString`) | TPC-H, SSB | spec (`CHAR(n)`), `VARCHAR(n)`, `TEXT` | CHAR padding widens rows and costs in comparisons |
| `column_order` | PostgreSQL, Citus | TPC-C (BenchBase), TPC-H | spec, aligned | PostgreSQL pads columns to alignment; reordering shrinks rows (EDB does this for TPROC-C) |
| `primary_keys` | MySQL, MariaDB (InnoDB) | TPC-H, TPC-DS | on, off | InnoDB clusters by PK; without one, a hidden row id: load time and join locality |
| `btree_dedup` | PostgreSQL, Citus | TPC-H | on, off | `deduplicate_items` shrinks non-unique FK indexes |
| `pk_order` | YugabyteDB, CockroachDB | YCSB d | asc, desc | workload d reads the latest inserts; only with `-xio ordered`, on CockroachDB only with `pk_hash = none` |
| `distribution_key` | Citus | TPC-H | orderkey, custkey | orderkey: orders⋈lineitem local; custkey: orders⋈customer local, lineitem needs repartition |
| `tpcc_item` | Citus | TPC-C (BenchBase) | reference, distributed | item is read-only and joined with stock: reference avoids remote reads |
| `hash_partitions` | PostgreSQL | TPC-C (BenchBase) | 0, n (by `w_id`) | smaller indexes and less contention per partition |
| `projections` | ClickHouse | TPC-H, SSB | none, aggregate | aggregate projections used transparently; cost: load time and size |
| `wide_parts` | ClickHouse | TPC-H, TPC-DS, SSB | default, compact, wide | parallel loaders produce compact parts; merge load during and after loading |
| `tablespace_index` | PostgreSQL | TPC-H, TPC-C (BenchBase) | same, separate volume | indexes on nvme, data on cephcsi (or vice versa), see [plan-storage-class-sweep.md](plan-storage-class-sweep.md) |

What each key needs beyond a placeholder:
- **Placeholder in existing scripts only**: `btree_dedup`, `wide_parts`,
  `projections`, extended statistics, statistics target, `pk_order`,
  `tpcc_item`, `covering_indexes` (index-script variant).
- **Results change**: `numeric_type` (rounding), `string_type` (`CHAR`
  trailing blanks): DBMS-Benchmarker reports result differences between
  configurations; expected, needs a note in the evaluation.
- **Script variant**: `distribution_key` (Citus PK must contain the
  distribution column; lineitem has no custkey), `primary_keys` (forbid
  with the Constraints variant), `hash_partitions` (PL/pgSQL loop with
  braces).
- **More than scripts**: `column_order` (loaders `\COPY` positionally →
  column lists in the loader images), `tablespace_index` (second volume),
  YugabyteDB `colocated` (database before BenchBase connects),
  `tiflash_replica` (TiFlash nodes), MariaDB ColumnStore (image).
- **Not reachable by scripts**: HammerDB TPC-C (all DBMS), BenchBase TPC-C
  on CockroachDB; only post-build `ALTER`s, and e.g. `fillfactor` set after
  loading affects only new pages.

Companion, not DDL: BRIN and ClickHouse `order_by` only pay off if the
loader inserts in that order (a loader parameter). Not a placeholder: index
and constraint timing (before/after the load) is a choice of script list
like the existing `Index`/`Constraints` keys in `cluster.config`.

## Milestones

- **M0** superseded: 0 means "not given"; covered by check B.
- **M1** DONE (04a57300): mechanism, see [Python changes](#python-changes-as-implemented).
- **M1b** DONE (04a57300): sweep in `expand_resource_cells()`.
- **M2** DONE (04a57300): see [Folders with declarations](#folders-with-declarations-m2).
- **M2b** DONE (8616163b): volume names without DDL values,
  `ddl_*` volume labels, reuse semantics and reporting, token rules;
  checks C–G.
- **M2c** DONE (8616163b): short volume and worker names, Dragonfly
  replica storage name; old bexhoma volumes deleted at rollout.
- **M3** priority A keys. **DONE (b730977a)** except `dimensions` (830
  unit tests OK, defaults reproduce the old scripts):
  - ycsb/PostgreSQL `fillfactor` (int, default 100);
  - ycsb/CockroachDB `pk_hash` (hash | none);
  - ycsb/YugabyteDB `pk_sharding` (hash | asc), `num_tablets` (auto | 4 … 128,
    `SPLIT INTO n TABLETS`, only with hash);
  - ycsb/TiDB `clustered` (default | clustered | nonclustered),
    `split_regions` (none | 4 … 128, `SPLIT TABLE … BETWEEN ('user0') AND
    ('user9') REGIONS n`);
  - tpch/ClickHouse and tpch/ClickHouseCluster `order_orders`,
    `order_lineitem` (key | date).

  Corrections found while implementing: BenchBase creates the TPC-C schema
  itself for PostgreSQL, MySQL, MariaDB, TiDB and CockroachDB (bexhoma's
  scripts are placeholders); only Citus and YugabyteDB TPC-C schemas are
  bexhoma's. So `fillfactor` is YCSB only. TiDB `PRE_SPLIT_REGIONS` needs
  `SHARD_ROW_ID_BITS` or `AUTO_RANDOM` and does nothing for YCSB's VARCHAR
  key; `split_regions` replaces it.

  Cluster checks (2026-10-29, ephemeral, sweeps, `-ks no`):
  - H (1793286796) PostgreSQL `fillfactor=100,80`: `WITH (fillfactor = 100)`
    / `80` filled; all tests passed, no script errors.
  - I (1793287309) CockroachDB `pk_hash=hash,none`: `PRIMARY KEY USING HASH`
    / `PRIMARY KEY ,`; all tests passed, no script errors.
  - J (1793288481) TiDB `clustered=nonclustered`, `split_regions=16`:
    `NONCLUSTERED` filled, but `SPLIT TABLE … BETWEEN ('user0') AND
    ('user9')` failed: `ERROR 1265 … Incorrect value: 'user0' for column
    '_tidb_rowid'` (nonclustered rows are keyed by the integer rowid). The
    run went on without the split and all tests passed. Fix: generic
    `requires` in declarations (`split_regions` requires `clustered` in
    default/clustered; YugabyteDB `num_tablets` requires `pk_sharding=hash`),
    checked in `resolve_ddl_parameters()` for every combination before
    anything starts.
  - J2 (1793289753) TiDB `clustered=clustered`, `split_regions=16`:
    `PRIMARY KEY CLUSTERED`, `TOTAL_SPLIT_REGION 15`,
    `SCATTER_FINISH_RATIO 1`, no SQL errors: the key works. But
    `bx-tikv-ti-ycsb-1-0` restarted after ~8 min and then crash-looped:
    `FATAL … duplicated store address … already registered by id:13`.
    Without `-rst`, TiKV keeps its data in the container filesystem; after a
    container restart it comes back without its store ID and PD refuses the
    new registration (not caused by the renaming: worker names were
    storage-label based before too). Cause of the first restart unknown
    (only the last termination is in the describe log); run J (same
    settings, no effective split) had none.
  - J3 (1793290378) = J2 with `-m`: split again 16 regions, scatter 1, **no
    restarts**, all tests passed; TiKV peak 8.6 GB RAM in loading (limit
    16Gi). The J2 restart did not reproduce; an ephemeral TiKV cannot
    survive a container restart either way (`-rst` for long runs).
  - K (1793289099) ClickHouse `order_lineitem=key,date` ×
    `order_orders=key,date`: 4 configurations, the four sort-key
    combinations filled; all tests passed, no script errors.
  - YugabyteDB not checked (deployed by its own Helm script, not by bexhoma).

  **Found**: an error in an init script (stderr of the loading scripts) does
  not fail the run or any test; it is only in
  `bexhoma-loading-<configuration>-<script>-*.stderr.log`. Proposal: a test
  `Init scripts without errors` like `Reset scripts ran without errors`
  (open item 13).

  Open: Citus/ClickHouseCluster `dimensions` (a key that selects a script
  folder variant, like SSB `-xdim`; ClickHouseCluster replicated dimensions
  also need the dimension data on every shard).
- **M3b** `systems[].ddl` in experiment.yml + catalog capability
  ([bexhoma/spec.py](../bexhoma/spec.py), tpch_catalog.py, ycsb_catalog.py
  emit `-xddl` through a shared helper).
- **M4** priority B keys, one DBMS at a time, each with a docs test run.
- **M5** "More candidates" that need only placeholders or script variants;
  those needing images, volumes or loader changes are a separate decision.

## Cluster checks

All with `-ks no`.

- **A** (2026-10-29, code 1793273857): TPC-H `-dbms Citus MariaDB -xddl
  num_worker_shards=8,32 -xddl engine=InnoDB,Aria -rst cephcsi -rss 10Gi`
  SF1. **OK**: filled scripts in the result folder (`SET citus.shard_count =
  8` / `32`, `ENGINE = InnoDB` / `Aria`, no braces left); check script shows
  8 and 32 shards for orders/lineitem; row counts right; `ddl_*` per
  connection in the summary; no result mismatch. MariaDB Q20/Q22 hit the
  1200 s timeout under both engines (run without `-xii -xic -xis`, no
  indexes; not a DDL effect). Volumes left on cephcsi: `mariadb-cephcsi`,
  `citus-cephcsi` (+ workers), and `mariadb-ddl9703dc-cephcsi`,
  `citus-ddle10c17-cephcsi` (+ workers), whose names decision B drops
  (item 7).
- **B** (2026-10-29, code 1793273894): YCSB `-dbms PostgreSQL Citus`
  without `-nwr`/`-nws`. **OK**: filled script `SET citus.shard_count = 32`,
  `shard_replication_factor = 1`; 32 shards of usertable in the check
  output; all tests passed. Citus waited ~2 h for experiment 1793222643
  (one Citus SUT per cluster).
- **Reuse checks after M2b/M2c** (2026-10-29, after reinstall and deleting
  the 115 old volumes; TPC-H SF1, `-rst cephcsi`), all **OK**:
  - C (1793286512) MariaDB `-xddl engine=Aria -xii -xic -xis`: new volume
    `bexhoma-storage-ma-cephcsi-tpch-1` with labels `ddl_engine=Aria`,
    `load_script=Schema`, `load_indexing=Index_and_Constraints_and_Statistics`,
    `shape_num_worker=0`, `shape_state=stable`; test passed.
  - D (1793287556) same without `-xddl`: reused, "DDL values taken from the
    volume: engine=Aria", section "Data Parameters of Reused Volumes", test
    passed.
  - E (1793288096) `-xddl engine=InnoDB`: reused, ran with Aria, message
    "volume loaded with engine=Aria (requested InnoDB) … -rsr reloads",
    `TEST failed: Data parameters as requested (volume differs: MariaDB-1
    engine: requested InnoDB, volume Aria)`.
  - F1 (1793288637) Citus `-nw 2`: volumes `bexhoma-storage-ci-cephcsi-tpch-1`,
    `bxw-bx-w-ci-cephcsi-tpch-1-0/1`, StatefulSet and headless Service
    `bx-w-ci-cephcsi-tpch-1`; labels `ddl_num_worker_shards=32`,
    `shape_num_worker=2`.
  - F2 Citus `-nw 3`: refused at start, "existing storage
    bexhoma-storage-ci-cephcsi-tpch-1 was loaded with 2 workers, but 3 are
    requested".
  - G MariaDB `-xddl engine=InnoDB,Aria -rst`: refused at start
    (persistent storage).
  - Not yet seen on the cluster: a reused volume without labels (assumed,
    test skipped): no old volume left; covered by unit tests.
  - `kubectl get pvc -L ddl_engine,load_indexing,shape_num_worker` shows
    the values as columns.

## Open questions

- Result tables (loading, throughput, latency) have one row per connection
  name (`Citus-1`, `Citus-2`) and no parameter columns, for resource cells
  too. The values are in the summary's connection section (`ddl_<key>`
  evaluation parameters) and, after M2b, in `ddl_parameters` per
  connection. A column per swept key would be an evaluator change in all
  benchmark types; if needed, one generic "cell columns" step for resource
  and DDL cells together (item 10).
- Rename `expand_resource_cells()` to `expand_cells()`? Cosmetic.

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
- Kubernetes label syntax: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#syntax-and-character-set
