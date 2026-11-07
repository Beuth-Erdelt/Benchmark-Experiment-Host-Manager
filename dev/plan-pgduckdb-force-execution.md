# Plan: PgDuckDB's force execution as a server setting, not a role setting

Status: **planned, not implemented** (2026-11-07). Findings verified on the
cluster with a PgDuckDB SUT (`bexhoma tpch -dbms PgDuckDB ... start`, code
1794055373); the end-to-end effect on a reused volume (step 1 below) is
derived from those findings, not reproduced yet.

## Problem

`-xdfe` / `--xduckdb-force-execution` (dest `duckdb_force_execution`) makes
PgDuckDB run queries on PostgreSQL tables in DuckDB's engine. Today:

1. `cluster.config` `dockers.PgDuckDB.benchmarks.{tpch,ssb}.option_parameters`
   maps the SUT environment variable `DUCKDB_FORCE_EXECUTION` to the option;
   `system_builder.build_configuration` always sets it (`'true'`/`'false'`).
2. `k8s/deploymenttemplate-PgDuckDB.yml`'s `postStart` hook reads the
   variable and, **only when it is `"true"`**, runs
   `ALTER ROLE postgres SET duckdb.force_execution = true`.
3. The catalog knob `duckdb_force_execution` (`contracts/contract_catalog.yml`)
   has `arg_style: env-var`; `tpch_catalog.option_flags()` turns it into the
   flag via `option_parameters`.

The switch itself is pg_duckdb's server setting `duckdb.force_execution`;
the environment variable is only bexhoma's trigger for the hook.

Verified on the cluster:

* `--set "deployment[bexhoma-deployment-pg-duck].container[dbms].duckdb.force_execution=true"`
  alone works: the server starts with `-c duckdb.force_execution=true`,
  `SHOW duckdb.force_execution` is `on` and a query plans as
  `Custom Scan (DuckDBScan)`, although `DUCKDB_FORCE_EXECUTION` is `"false"`.
* A role setting beats `-c`: after `ALTER ROLE postgres SET duckdb.force_execution = false`
  new sessions show `off` and plan PostgreSQL's `Seq Scan`.
* The role setting is stored in `pg_db_role_setting`, i.e. in the data
  directory on the volume.

Consequences:

1. **A volume stays forced.** The hook sets the role setting to `true` but
   never resets it, and the volume name does not depend on `-xdfe`. Every
   later run on a volume that once ran with `-xdfe` is forced, while the run
   records `DUCKDB_FORCE_EXECUTION=false`.
2. **`--set` of the variable is silently lost.** `start_sut` applies `--set`
   to the raw template first (`patch_dbms_args`, `lifecycle.py` ~941) and
   writes the SUT parameters afterwards, overwriting variables of the same
   name (~1341). `--set ...env.DUCKDB_FORCE_EXECUTION=true` becomes `false`.
   (General: any `--set ...env.NAME` loses against a SUT parameter `NAME`.)

## Plan

1. **Config: an option can set a server setting.** New optional key of a
   benchmark entry, e.g.
   `'option_settings': {'duckdb.force_execution': 'duckdb_force_execution'}`
   (server setting -> boolean option). `build_configuration` passes
   `duckdb.force_execution=true|false` as a server argument of that
   configuration, through the same path as `--set`
   (`experiment.dbms_args`, scoped `@<configuration>`), so a `--set` on the
   command line still wins. Add the key to `ENTRY_KEYS`, the validator
   (setting names are strings, options are boolean dests of the script) and
   `docs/DBMS.md`'s entry table. PgDuckDB's `tpch` and `ssb` entries use it
   instead of `option_parameters`.
2. **Template.** Remove `DUCKDB_FORCE_EXECUTION` from the PgDuckDB container
   and the `ALTER ROLE ... SET` from `postStart`; add
   `ALTER ROLE postgres RESET duckdb.force_execution` there, so a role setting
   left on an older volume no longer overrides the server setting.
3. **Catalog.** Change the knob `duckdb_force_execution` from
   `arg_style: env-var` to the PostgreSQL server-setting style (like
   `duckdb.max_memory`), or keep it an option knob whose flag comes from
   `option_settings` (then `tpch_catalog.option_flags()` reads that key).
   Decide by whether the workload-info note (`notes` with
   `when: duckdb_force_execution`) must stay: it needs the option set.
4. **Results.** The value is recorded as a server parameter of the
   configuration (connections.config / report), not as an environment
   variable.
5. **`--set` vs. SUT parameters (general, optional).** Either apply the
   `env.*` part of `--set` after the SUT parameters (and record it), or refuse
   a `--set ...env.NAME` that names a SUT parameter, pointing to the option.
6. **Tests.** Unit: the option produces the `-c duckdb.force_execution=...`
   argument for PgDuckDB and nothing for other DBMS; a command-line `--set`
   wins; the snapshot goldens of tpch/ssb with `-xdfe` change accordingly
   (accepted change). Cluster: one PgDuckDB TPC-H run with `-xdfe`, then one
   without on the **same volume** (no `-rsr`): the second must show
   `SHOW duckdb.force_execution` = `off` and PostgreSQL plans.

## Not changed

The user-facing flag `-xdfe` / `--xduckdb-force-execution` and its dest stay
(decision of 2026-11-06).
