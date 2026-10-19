# Plan: OLTP SUTs in bexhoma - current images, settings, CLI and placement

Status: **WP1-WP9 implemented 2026-10-17, committed (`7ed91c36`, released in v0.11.5); WP10 not (later, R7).** Unit tests:
`tests/test_set_arg_styles.py` (WP2/WP3), `tests/test_tls_secret.py` (WP5),
`tests/test_cluster_sut_settings.py` (WP4/WP6/WP7/WP8/WP9). The WP8 init/check scripts were run on
PostgreSQL 18.6, MySQL 9.7.2, MariaDB 12.3.3, Citus 14.2.0 and MonetDB Dec2025-SP3 pods (MySQL: startup
values restored after every check). HammerDB images rebuilt on base 6.0 and checked (2026-10-17).
Open: the smoke runs of section 3. Deviation from the plan: the HammerDB scripts read the generic `BEXHOMA_TLS`
(set by bexhoma where the job mounts the CA) instead of `HAMMERDB_MYSQL_SSL`. cadvisor stays v0.47.0.
Revised 2026-10-16 to cover only changes to bexhoma (code, templates, config, scripts, images, tests,
docs). Running the storage study itself is out of scope.

Scope:
- SUTs: PostgreSQL, PGBouncer, Citus, MySQL, MariaDB, CockroachDB, TiDB, YugabyteDB, Redis
  (standalone, cluster), Dragonfly (standalone, cluster, replica). **CedarDB is out of scope.**
- Benchmarks touched: TPC-C (HammerDB), Benchbase, YCSB (OLTP), TPC-H and TPC-DS (init/check scripts).

Related: [plan-storage-class-sweep](plan-storage-class-sweep.md).

---

## 1. Decisions (user, 2026-10-16)

| # | Decision |
|---|---|
| D1 | Durability: keep the current settings as they are (MySQL/MariaDB `flush-log-at-trx-commit=2`, YugabyteDB `durable_wal_write=false`). |
| D2 | Replication: realistic, 3 (CockroachDB/TiDB `-nw 3 -nwr 3`, YugabyteDB RF 3). |
| D3 | Versions: LTS lines; newest release where there is no LTS. |
| D4 | CockroachDB: latest version without a license key = **v24.2.4** (unchanged). |
| D5 | MySQL **9.7** with TLS for HammerDB via a Secret created by bexhoma (WP5). |
| D6 | Dragonfly: `SAVE` on all workers (WP4) and settings via environment variables (WP3). |
| D7 | Worker placement via a new option (WP6); per-component sizing (WP7). |
| D8 | YugabyteDB volumes per tserver: chart default 2 or 1 - left open, made a parameter (WP9). |
| D9 | Redis and Dragonfly are included. |
| D10 | MySQL init scripts: keep the import-speed settings, but only for the load phase (WP8). |
| D11 | TPC-H/TPC-DS get always-included check scripts, like TPC-C/YCSB/Benchbase (WP8). |
| D12 | `CHECKPOINT` always in the PostgreSQL check scripts. |
| - | The probe/PID-1 fix (PostgreSQL, PgDuckDB, Citus) is already committed. |

---

## 2. Work packages

Order and dependencies: WP1 first (plain template/image changes). WP2 and WP3 are independent code
changes to `--set`. WP5 needs WP1 (MySQL 9.7). WP8 can go in parallel. WP4, WP6, WP7 touch
`configurations/lifecycle.py` / `loading.py` and should be done one after another. WP9 is script-only
plus a small metrics change. WP10 is optional and last.

### WP1. Templates: current images and required setting fixes

Files: `k8s/deploymenttemplate-*.yml`, image tags in `cluster.config` / `k8s-cluster.config` where
pinned.

| SUT / template | From | To | Required changes beyond the tag |
|---|---|---|---|
| PostgreSQL (`PostgreSQL.yml`, `PGBouncer.yml` backend) | `postgres:18.3` | `postgres:18.6` | none |
| PGBouncer variants (`PGBouncerReplica.yml`, `PGBouncerSidecar.yml`) | `postgres:16.1`, `edoburu/pgbouncer` (untagged) | `postgres:18.6`, `edoburu/pgbouncer:v1.26.0-p0` | none (release notes checked 2026-10-17: online restart removed, `search_path` tracked by default, new `client_login_count` stat; 1.26.1 fixes a `search_path` ignore regression but is not on edoburu yet) |
| PGBouncer (`PGBouncer.yml`) | `edoburu/pgbouncer:v1.25.1-p0` | `v1.26.0-p0` | as above (`POOL_MODE session`, `IGNORE_STARTUP_PARAMETERS` unaffected) |
| Citus (`Citus.yml`, coordinator + workers) | `citusdata/citus:13.2.0-alpine` (PG 17.6) | **`14.2.0` (Debian, PG 18.4), not `14.2.0-alpine`** | (a) **Not alpine:** `14.2.0-alpine` raises `ERROR: could not append to file: Not supported` in ~5 % of HammerDB New Order transactions (171-177 per minute, also on a real volume, same with HammerDB 5.0); `13.2.0-alpine` and `14.2.0` Debian run with 0 errors (checked 2026-10-17). (b) **Set `PGDATA=/var/lib/postgresql/data/pgdata` on the coordinator** (the workers have it, the coordinator does not): PG 18 images default to `/var/lib/postgresql/18/docker`, and with the PVC at `/var/lib/postgresql/data` the entrypoint refuses to start (crash loop, tested). (c) **fix preStop**: `/usr/lib/postgresql/16/bin/pg_ctl` does not exist; Debian 14.2 has `/usr/lib/postgresql/18/bin/pg_ctl` (also on `PATH`) and `/usr/local/bin/gosu`. Broken today already. |
| MySQL (`MySQL.yml`) | `mysql:8.4.0` | `mysql:9.7.2` | **remove `--mysql-native-password=ON`** (server aborts on 9.x). Add TLS volume/args (WP5). Other args unchanged (D1). |
| MariaDB (`MariaDB.yml`) | `mariadb:11.4.7` | `mariadb:12.3.3` | remove `--innodb-buffer-pool-chunk-size` (deprecated, ignored); readiness probe `timeoutSeconds: 2` -> 10 |
| CockroachDB (`CockroachDB.yml`) | `v24.2.4` | **unchanged** (D4) | none |
| TiDB (`TiDB.yml`, PD/TiKV/SQL) | `v7.1.6` | `v8.5.8` | none (TiKV accepts `--pd`; SQL pod `yum install mysql` works on Rocky Linux 9; both tested) |
| Redis (`Redis.yml`) | `redis:8.6.1` | `redis:8.10.2` | none (args accepted) |
| Redis cluster (`RedisCluster.yml`) | `redis:7.4.2` (SUT, workers), `redis:7.0` (helper) | `redis:8.10.2` | none (checked 2026-10-17: template args accepted, 3-node cluster `ok`, hostname endpoints route) |
| Dragonfly (`Dragonfly.yml`, `DragonflyCluster.yml`, `DragonflyReplica.yml`) | `v1.37.0` | `v2.0.2` | move `--maxmemory` out of the command into an env default (WP3) |
| Exporters | postgres-exporter `v0.19.1`, mysqld-exporter `v0.17.2`, `latest` tags (pgbouncer-exporter, redis_exporter) | `v0.20.1`, `v0.20.0`, pinned tags (redis_exporter `v1.94.0`, works with `--is-cluster` on 8.10) | none (checked 2026-10-17: mysqld-exporter 0.17.2/0.20.0 same names, works on MySQL 9.7 caching_sha2 with cold cache; postgres-exporter 0.20.1 only drops the unused `pg_stat_archiver_last_archive_age`). Pre-existing, not caused by the update: 15 PG names in `k8s-cluster.config` are empty in both versions (PG 17+ moved the checkpoint columns out of `pg_stat_bgwriter`; per-table stats only for the exporter's database; `pg_stat_wal_wal_bytes` absent) - separate cleanup |
| cadvisor sidecars | `v0.47.0` | `v0.60.6` | low priority (unused with `-mc`) |
| CedarDB | - | out of scope | - |
| YugabyteDB | Helm chart in the test scripts | see WP9 | - |

Memory sizes in the templates (e.g. MySQL/MariaDB buffer pool 96G) stay as they are, so other studies
are unaffected; runs with smaller limits set them via `--set` (WP2).

Acceptance: every updated SUT starts with its template and a smoke run (`-sf 1`, short duration) of its
usual benchmark completes (see section 3).

### WP2. `--set` for MySQL/MariaDB-style arguments

Today `--set` only patches PostgreSQL-style `-c key=value` pairs (`configurations/manifest.py:36-63`
`ensure_arg_pairs`, `:66` `patch_container`). A MySQL `--set` would append `-c ...` to `mysqld`.

Changes:
1. `manifest.py`: a second argument style `--key=value` (one list element), as used by the MySQL and
   MariaDB templates. Style per container: declared in the template (annotation, e.g.
   `bexhoma/arg-style: flag` on the Deployment) with detection from the existing args as fallback
   (`-c` pairs -> pg style; `--x=y` elements -> flag style).
2. Name matching treats `-` and `_` as equal (MySQL does; templates use hyphens; the selector regex
   `experiments/base.py:75-80` allows only `[A-Za-z0-9_]`). Replace in place if present, append
   otherwise. Valueless flags (`--skip-log-bin`) are out of scope.
3. `spec.py`: arg style `mysql-flag` next to `pg-guc`/`env-var` (`spec.py:102-121`), so catalog
   `derive:` formulas (e.g. buffer pool = `0.6 * memory_limit`) work for MySQL/MariaDB.
4. Tests next to `tests/test_pgduckdb_knobs.py`: replace, append, hyphen/underscore, `@CONFIG` scope,
   PostgreSQL-style args unaffected.
5. Docs: `--set` help text and the parameters docs page (which template uses which style).

Example after WP2: `--set deployment[bexhoma-deployment-mysql].container[dbms].innodb_buffer_pool_size=10G`.

Not covered: CockroachDB/TiDB flags inside `bash -c` strings, YugabyteDB (Helm gflags).

### WP3. `--set` for environment variables; Dragonfly settings via ENV

1. `manifest.py` `patch_container`: if `param` starts with `env.`, set or replace the entry in the
   container's `env` list (args untouched). The selector regex already accepts `env.NAME`
   (`param` = name + one `.ext`). Works for Deployments and StatefulSets and with `@CONFIG`.
   Example: `--set statefulset[bexhoma-worker].container[dbms].env.DFLY_snapshot_cron="* * * * *"`.
2. `spec.py`: wire the existing `env-var` arg style (`spec.py:120`) to this mechanism.
3. Dragonfly templates (all three): move `--maxmemory` from the `sh -c "exec dragonfly ..."` command into
   an `env` default `DFLY_maxmemory`, because **the command line wins over the env var** (tested). Keep
   the value; sizing per run via `--set ...env.DFLY_maxmemory`.
4. Tests: set/replace/append, Deployment and StatefulSet, `@CONFIG`, args unchanged.

Tested (Dragonfly 2.0.2): `DFLY_proactor_threads`, `DFLY_snapshot_cron` from env take effect
(`* * * * *` wrote a snapshot every minute); `--maxmemory=2GiB` on the command line beat
`DFLY_maxmemory=1GiB`.

### WP4. Reset and check scripts on all workers

Today reset scripts (`exec_reset_script`, `configurations/loading.py:890-989`) and the `Checks`/index
scripts run only in the first SUT pod (`execute_command_in_pod_sut`, `loading.py:932-934`). For
`DragonflyCluster` that pod is a placeholder; the data is on the workers, which never get the `SAVE` of
`experiments/ycsb/Dragonfly/save-snapshot.sh`.

Changes:
1. Per-configuration script target, e.g. `config.set_script_target('workers')`, default `'sut'`.
2. For `'workers'`: run each script in every pod of `get_worker_pods(only_stateful=True)`
   (`configurations/base.py:793`), container `dbms`, in parallel threads; logs per pod
   (`...-<pod>.stdout.log`); returned time = maximum over the pods.
3. Set `'workers'` in `ycsb.py` for `DragonflyCluster` and `RedisCluster`. `DragonflyReplica`: also
   `'workers'` (corrected 2026-10-19, #667): its SUT Deployment is a dummy, the master is `bexhoma-worker-0`,
   and `SAVE` (`CO::ADMIN`, not journaled) does not reach the replicas.
4. Tests: target selection, per-pod logs, timing = max.

### WP5. TLS Secret for MySQL and HammerDB (D5)

Why: MySQL 9.x has no `mysql_native_password`; `root@'%'` then uses `caching_sha2_password`, whose
first login needs TLS or the server's RSA key. HammerDB can only do TLS, and only with a readable CA file.

Changes:
1. **Config:** a flag in the MySQL docker entry of `cluster.config` and `k8s-cluster.config`, e.g.
   `'tls': {'secret': True}` (reusable later for MariaDB, PostgreSQL, CockroachDB secure mode).
2. **Secret creation in `start_sut()`** (`configurations/lifecycle.py:490`), before the SUT manifests are
   applied: self-signed CA + server certificate generated with Python `cryptography` (add to
   `requirements.txt`; 48.0.0 is installed in the env). SANs: SUT service name, `.namespace`, `.svc`,
   `.svc.cluster.local`, `localhost`. Keys `ca.pem`, `server-cert.pem`, `server-key.pem`. Name
   `bexhoma-tls-<configuration>-<experiment>`, labels `app`, `experiment`, `configuration`,
   `component=tls`. New module, e.g. `bexhoma/tls.py`, with a pure function that returns the Secret
   document (unit-testable).
3. **Cleanup:** experiment cleanup uses `kubectl delete all -l experiment=...`
   (`experiments/base.py:1393`); `all` does **not** include Secrets. Add `delete secret -l
   experiment=...,component=tls` there and in `stop_sut` (`lifecycle.py:1384`).
4. **MySQL template:** volume from the Secret at `/etc/mysql/certs` (read-only) and args
   `--ssl-ca=/etc/mysql/certs/ca.pem --ssl-cert=/etc/mysql/certs/server-cert.pem
   --ssl-key=/etc/mysql/certs/server-key.pem`. bexhoma fills in the Secret name (as for the PVC
   `claimName`) and removes volume and args when TLS is off.
5. **HammerDB job templates** (generator, benchmarker): the same Secret, only `ca.pem` mapped to
   `/etc/mysql/certs/ca-cert.pem` (`items:`), env `HAMMERDB_MYSQL_SSL=true` for MySQL.
   `images/hammerdb/{generator,benchmarker}/*.sh`: `diset connection mysql_ssl true` when that env is
   set (the lines exist, commented out). **Move the HammerDB images to 6.0** (R8, user decision
   2026-10-17): base `tpcorg/hammerdb:v6.0` (or the per-DBMS tags such as `v6.0-mysql`, `v6.0-postgres`,
   `v6.0-maria`) in `images/hammerdb/{generator,benchmarker}/Dockerfile`, then rebuild. Tested with
   MySQL 9.7 over TLS (build + timed run). Checked 2026-10-17 with the generic `tpcorg/hammerdb:v6.0`
   and bexhoma's `diset` lines for PostgreSQL 18.6, Citus, MariaDB 12.3.3 and MySQL 9.7.2 (TLS): all
   keys accepted, build + 1-min timed run with time profile OK, 0 errors; bexhoma's collector
   (`tpcc.py:132-158`) parses `TEST RESULT`, `Active` (first match, via `zip`) and the
   `/tmp/hdbxtprofile.log` block (`SUMMARY OF`, `>>>>> PROC: NEWORD`, separator, `CALLS/MIN/AVG/P99...`)
   unchanged. The generic base image is enough; no per-DBMS tags needed.
6. **Init script:** `experiments/tpcc/MySQL/initschema-tpcc.sql:14` -> `IDENTIFIED BY 'root'`.
7. JDBC clients (YCSB, Benchbase, dbmsbenchmarker): no change (tested: YCSB over TLS, Benchbase via RSA key).
8. Tests: unit test of the Secret document (keys, SANs, labels, name); template patch with TLS on/off.

### WP6. Worker placement `-rnw` (D7)

Today `-rnn` sets a `kubernetes.io/hostname` nodeSelector only on the SUT Deployment
(`lifecycle.py:1295-1364`); StatefulSet workers are placed freely (verified).

Changes:
1. `cli_args.py`: `-rnw/--request-node-worker`, nodes joined with `+` (e.g.
   `cl-worker37+cl-worker38+cl-worker39`); special value `sut` = the `-rnn` node. Commas keep their
   sweep meaning: `-rnw` becomes one more list in the resource cells (`cli_args.py:77-94`), paired by
   position like `-rst`.
2. `lifecycle.py`, StatefulSet branch (`:853-1044`): for every StatefulSet of the SUT add
   `nodeAffinity` (`kubernetes.io/hostname In [nodes]`) and a `topologySpreadConstraint`
   (`maxSkew: 1`, `topologyKey: kubernetes.io/hostname`, `whenUnsatisfiable: DoNotSchedule`, label
   selector per component). Existing template anti-affinity stays.
3. Not given: unchanged behavior.
4. Workload info text ("Workers are fixed to ...") and the summary.
5. Tests: manifest patch for one and several StatefulSets, `sut`, sweep pairing.
6. YugabyteDB: same node list as Helm values in `Install-YugabyteDB` (WP9).

Tested (TiDB v8.5.8 prototype): one PD and one TiKV per listed node; 4 TiKV on 3 nodes -> 2/1/1; no
conflict with the template's soft anti-affinity.

### WP7. Per-component sizing (D7)

Today `-rc/-rr/-lc/-lr` overwrite the `dbms` container of **every** StatefulSet (`lifecycle.py:947-974`)
and `-rss` every `volumeClaimTemplates[0]` (`:1037-1044`); `-rc 4` / `-rr 16Gi` are defaults, so
template values never survive. TiDB's PD (template 0.25-1 CPU, 0.5-2 Gi, 10Gi) gets the TiKV size.

Design (R4, detailed 2026-10-17):

1. **Two attributes on `SutConfiguration`** (`configurations/base.py`), with setters:
   - `data_components: Optional[list[str]] = None` - StatefulSet components (their `component` label)
     that receive the experiment's resources and volume size. `None` = all StatefulSets (today's
     behavior, backward compatible). `set_data_components(['tikv'])`.
   - `sut_role: str = 'data'` - `'placeholder'` marks a SUT Deployment that holds no data (entry point,
     client or helper pod). `set_sut_role('placeholder')`.
   `monitoring_sut = False` is **not** usable as the marker: `DragonflyReplica` sets it too, but its
   SUT pod is the master and holds data; DatabaseService sets it because the DBMS is outside Kubernetes.
2. **StatefulSet branch** (`lifecycle.py:947-974` resources, `:1037-1044` volume size): a helper
   `cfg.receives_experiment_resources(component)` = `data_components is None or component in
   data_components`.
   - True: as today, `-rc/-rr/-lc/-lr` and `-rss`.
   - False: keep the template's `resources` and `volumeClaimTemplates[0]...storage`. The storage
     **class** still comes from `-rst` (all volumes of a configuration in one class).
   - Per-component overrides win in both cases, mirroring the existing `replicas_<component>`
     (`get_num_worker()`, `base.py:777-791`): `cfg.resources['requests_<component>']`,
     `['limits_<component>']` (dicts with `cpu`/`memory`), `['storage_<component>']` (size), set via
     `set_resources(requests_pd={'cpu': '500m', 'memory': '1Gi'}, ...)`.
3. **Deployment branch** (`lifecycle.py:1287-1364`): for `sut_role == 'placeholder'` skip the
   `-rc/-rr/-lc/-lr` override and keep the template's resources; node pinning (`-rnn`) still applies.
   The template values become the single source for the placeholder size (visible in the YAML),
   instead of constants in code. Template fixes needed for that:
   - `RedisCluster.yml`, `DragonflyCluster.yml` SUT Deployment: today `requests 1 CPU / 1Gi`, `limits
     16 CPU / 16-128Gi` -> e.g. `requests 250m / 512Mi`, `limits 1 CPU / 1Gi`.
   - `CockroachDB.yml` SUT Deployment (client pod): today `requests 100m / 16Gi`, `limits 100m / 1Gi` -
     request above limit, only valid because bexhoma overwrites it -> `requests 250m / 512Mi`,
     `limits 1 CPU / 1Gi`.
   - `YugabyteDB.yml` helper pod: same small size.
4. **Where it is set** (experiment scripts `benchbase.py`, `ycsb.py`, `tpch.py`, `hammerdb.py` where the
   DBMS is configured):

   | Configuration | `data_components` | `sut_role` |
   |---|---|---|
   | TiDB | `['tikv']` (PD keeps template: 0.25-1 CPU, 0.5-2Gi, 10Gi) | data (SQL pod: `-rc/-rr`, compute) |
   | CockroachDB | all (`worker`) | placeholder (client pod) |
   | Citus | all (`worker`) | data (coordinator holds metadata, plans queries) |
   | Redis cluster, Dragonfly cluster | all (`worker`) | placeholder |
   | Dragonfly replica | all (`worker`) | placeholder (master = `bexhoma-worker-0`; corrected 2026-10-19) |
   | YugabyteDB | - (Helm) | placeholder (helper pod) |
   | DatabaseService | - | placeholder (DBMS outside Kubernetes; pod is a client) |
   | PostgreSQL, MySQL, MariaDB, Redis, Dragonfly standalone | - | data |
5. **Reporting:** at manifest creation sum the requested CPU/RAM of the SUT Deployment and every
   StatefulSet (x replicas) and store it with the connection info (e.g. `resources_total`); the
   summary shows it per configuration.
6. **Tests:** manifests from the TiDB template with `data_components=['tikv']` (PD keeps template
   resources and 10Gi, TiKV gets `-rc/-rr` and `-rss`); per-component override; placeholder Deployment
   keeps template resources but gets `-rnn`; `None` reproduces today's manifests exactly.

Tested (TiDB v8.5.8 prototype): PD with template resources, TiKV and SQL with 8 CPU / 16 Gi: all Ready,
4 stores Up, `max-replicas` 3, data region on 3 stores.

### WP8. Init and check scripts: import settings scoped to the load phase (D10, D11, D12)

**8a. Post-load runs always.** TPC-C/YCSB/Benchbase use `Checks` (on by default, set in
`experiments/{tpcc,ycsb,benchbase}.py`). TPC-H/TPC-DS select their post-load list from
`-xii/-xic/-xis` (`benchmarks/tpch.py:20-50`, `benchmarks/tpcds.py:128-134`); without flags it is empty,
so today's load relaxations stay active for the queries (MySQL `autocommit=0`, `foreign_key_checks=0`,
`unique_checks=0`, `flush_log_at_trx_commit=2`; PostgreSQL `synchronous_commit=off` via `ALTER SYSTEM`).
Changes:
1. New key `Checks` for the "no flag" combination instead of `""` (`_INDEXING_KEYS`; the catalog
   translator shares `resolve_indexing_key`), and in `tpcds.py`.
2. `checkschema-tpch.sql` / `checkschema-tpcds.sql` appended as the **last** entry of every post-load
   list in `cluster.config` and `k8s-cluster.config` (`volumes.tpch/tpcds.initscripts`, incl. `_tenant`
   variants), so index/constraint builds still run relaxed and the restore comes afterwards.
3. `loading.py:838-850` already waits for the `index` label when post-load scripts exist; plain loads
   then report a non-zero `time_postload`.

**8b. MySQL init scripts.** Keep import-speed settings for the load only, sized to the container:

| Setting (today) | Where | New |
|---|---|---|
| `innodb_flush_log_at_trx_commit = 0` / `2` | tpcc, ycsb / tpch | keep for load, restore |
| `innodb_log_buffer_size = 16G` (4 GiB effective max) | tpcc, ycsb | load only, e.g. `1G`, restore |
| `innodb_buffer_pool_size = 32G` (40 GiB effective) | tpcc, ycsb | remove (template / `--set`) |
| `tmp_table_size`, `max_heap_table_size` (32G / 1G) | tpcc / tpcds | remove (template args if needed) |
| `sync_binlog` | tpch | remove (binlog is off) |
| `io_capacity 200/2000`, `ddl_threads 4`, `parallel_read_threads 4` | tpch `initstatistics` | replace by restore |
| `foreign_key_checks`, `unique_checks`, `autocommit` | tpch | off for load, on in the check script |
| users/grants, `local_infile`, `sql_mode` | all | keep (`IDENTIFIED BY 'root'`, WP5) |

Restore mechanism (tested on 9.7.2): the pre-load part saves the startup values
(`bexhoma.saved_settings`, `REPLACE INTO ... @@GLOBAL.x`), the check script reads them back with
`SELECT CAST(value AS UNSIGNED) INTO @v ...; SET GLOBAL x = @v;` (`SET GLOBAL x = DEFAULT` would give
compiled defaults; without `CAST` -> ERROR 1232).

Note: before WP8, HammerDB TPC-C and YCSB benchmarks ran with `flush_log_at_trx_commit=0` (from the
init script), TPC-H queries with `1` after `-xis`; afterwards all run with the template value (D1).
MySQL benchmark results before/after are not directly comparable (release note).

**8c. Check script content** (TPC-H/TPC-DS new; OLTP scripts extended where useful):
1. Restore and print the configured settings (MySQL as above; PostgreSQL `ALTER SYSTEM RESET
   synchronous_commit; SELECT pg_reload_conf();`, the copies in `initstatistics-*.sql` can go).
2. Row counts per table, **counts only, no expected values / verdict** (R6, user decision
   2026-10-17); no `{SF}` placeholder needed. For reference when reading the logs: TPC-H counts are
   exact and deterministic per SF (verified from loader logs: region 5, nation 25, supplier
   10,000 x SF, customer 150,000 x SF, part 200,000 x SF, partsupp 800,000 x SF, orders 1,500,000 x SF;
   lineitem SF 10 = 59,986,052, SF 30 = 179,998,372).
3. Sizes: tables, indexes, database.
4. Write-ahead log of the load (PostgreSQL `pg_stat_wal.wal_bytes`; MySQL `Innodb_redo_log_*`).
5. Configuration dump (non-default settings), as in the OLTP scripts.
6. Distribution for distributed SUTs (Citus), as in the OLTP scripts.
7. PostgreSQL: `CHECKPOINT` (D12), counted in `time_postload`.
8. Not: `VACUUM`/`ANALYZE` (stays with `-xis`).
DBMS folders: PostgreSQL, MySQL, MariaDB, Citus, PgDuckDB, MonetDB (counts/sizes only where no
settings are relaxed); missing files are skipped by bexhoma.

### WP9. YugabyteDB (Helm, test scripts) and Ceph metrics by label

Files: `scripts/test-docs-yugabytedb.ps1` / `.sh`, `bexhoma/ceph_storage.py`.
1. `Install-YugabyteDB`: add parameters for storage class (default `shared`, as today), volumes per
   tserver (`storage.tserver.count`, default 2 = chart default, D8), node placement (chart
   `nodeSelector`/affinity, WP6); chart `--version 2025.2.7` (LTS). Chart keys checked 2026-10-17: 2025.2.4 -> 2025.2.7 has no
   added, removed or changed values; `storage.*` (incl. `count`), `resource.*`, `gflags.*`,
   `preflight.skipUlimit`, `enableLoadBalancer`, `nodeSelector`, `master/tserver.affinity` exist.
   **Fix:** `tserver.livenessProbe.timeoutSeconds` / `master.livenessProbe.timeoutSeconds` are not chart
   keys and are silently ignored; the chart reads the root `livenessProbe.timeoutSeconds` (default 1 s).
   The probe (disk check on the data dirs) exists only with `storage.ephemeral=false`, so this never
   mattered with today's ephemeral runs; with PVCs set `livenessProbe.timeoutSeconds=10`.
   `durable_wal_write` stays default (D1).
2. Ceph volume metrics: bexhoma resolves `{rbd_images}` from PVCs it created; the chart's PVCs
   (`app=yb-tserver`) are unknown, so the metrics stay empty. Add a per-configuration PVC label
   selector (e.g. `pvc_selector='app=yb-tserver'`) to the resolution in `ceph_storage.py`; covers 1 or 2
   volumes per pod.
3. Known limitation (document): `volume_used`/`volume_size` come from bexhoma's helper pod, not the tservers.

### WP10 (optional, later). Import durability as a general option (all workloads, all DBMS)

Revised 2026-10-17: the user wanted a general option, not a MySQL-only redo switch. Not implemented.

**Idea.** Every DBMS can make the import cheaper on durability, with its own statements and to a
different degree. bexhoma offers one setting for it; each DBMS maps it to what it has. An unsafe fast
import is always visible in the results.

**What the DBMS offer** (only the MySQL line is tested; (?) = to be checked first):

| DBMS | Strongest lever during the load | Runtime? | Way back |
|---|---|---|---|
| MySQL 9.7 | `ALTER INSTANCE DISABLE INNODB REDO_LOG` | yes (tested) | `ENABLE` |
| PostgreSQL / PgDuckDB | `fsync=off`, `full_page_writes=off` (WAL written, never flushed) | yes, reload | `ALTER SYSTEM RESET` + reload + `CHECKPOINT` |
| PostgreSQL, alternatives | `UNLOGGED` tables + `SET LOGGED` (writes the whole table into WAL afterwards, cost moves); `wal_level=minimal` + COPY into a table created in the same transaction | yes / restart | `SET LOGGED` / restart |
| Citus | as PostgreSQL, on coordinator and workers (`run_command_on_workers`) | yes | as PostgreSQL |
| MariaDB 12 | no redo-off switch; `innodb_flush_log_at_trx_commit=0`, `innodb_doublewrite` (?) | yes | restore saved values |
| Redis | `CONFIG SET appendonly no`, `save ""` | yes | `CONFIG SET` back, `BGREWRITEAOF`/`SAVE` |
| Dragonfly | nothing to switch off (snapshots only on demand) | - | - |
| YugabyteDB | `durable_wal_write=false` already default (D1); `yb_disable_transactional_writes` for COPY (?) | session | - |
| CockroachDB | `kv.raft_log.disable_synchronization_unsafe` (?) | cluster setting | reset |
| TiDB | no WAL switch; bulk paths only (`tidb_dml_type='bulk'`, IMPORT INTO) (?) | session | - |
| MonetDB | `COPY ... LOCKED` (?) | per statement | - |

**Design.**
1. **CLI, all entry scripts:** `-xld/--load-durability {default,relaxed,off}`.
   - `default`: what the init scripts do today, no change in behavior.
   - `relaxed`: commit without flushing (PostgreSQL `synchronous_commit=off`, MySQL/MariaDB
     `innodb_flush_log_at_trx_commit=2`, Redis `appendfsync no`).
   - `off`: the strongest lever of the DBMS (table above).
2. **Scripts per DBMS, not per benchmark**, in a shared folder such as `experiments/_durability/<DBMS>/`:
   - `load-durability-relaxed.*` / `load-durability-off.*`: appended by bexhoma as the last pre-load script.
   - `load-durability-restore.*`: inserted by bexhoma before the check script in every post-load list
     (WP8 'Checks' runs always), so a load never leaves the server weakened for the benchmark.
3. **Restore** as in WP8: save startup values before relaxing (MySQL `bexhoma.saved_settings`), restore
   exactly those (PostgreSQL `ALTER SYSTEM RESET` + reload). `off` ends with a `CHECKPOINT` (or the DBMS
   equivalent) in the restore, so the first benchmark round does not pay for it.
4. **Unsupported level:** no file for the level -> message ("load durability 'off' not supported by TiDB,
   using default"), no failure; the effective level is what gets reported.
5. **Reporting:** requested and effective level in the workload info and the connection parameters;
   the summary shows it next to the loading times.
6. **Safety:** with `off`, a SUT restart during the load can lose data; bexhoma already detects SUT
   restarts and then marks the load as failed.
7. **Tests:** script-list insertion per level, restore always present, unsupported level falls back,
   reporting; scripts run on the DBMS pods as for WP8.

**First step (proposal).** Mechanism (1-7); scripts for MySQL, PostgreSQL/PgDuckDB, Citus, MariaDB
(`relaxed` only); Redis later; TiDB, CockroachDB, YugabyteDB, MonetDB report "not supported".

**Decisions (user, 2026-10-20):**
- Levels: `default/relaxed/off` (all three).
- Today's init-script relaxations (PostgreSQL `synchronous_commit=off`; MySQL flush 2/0,
  `foreign_key_checks`/`unique_checks` 0, TPC-H `autocommit` 0; their save/restore in the check
  scripts) move into `relaxed`. Init scripts then only create schemas; restore moves into
  `load-durability-restore.*`.
- Consequence: `default` becomes "DBMS as configured" (fully durable). To keep results comparable
  with earlier runs, the CLI default of `-xld` is `relaxed` (confirmed).
- Port to TPC-DS MySQL (#709, 2026-10-20) is in the init/check scripts for now and moves with the rest.

Tested earlier on MySQL 9.7.2: redo OFF/ON works; `ENABLE` when enabled and `DISABLE` twice are no-ops;
`root@localhost` and `root@'%'` hold `INNODB_REDO_LOG_ENABLE`; MySQL logs a warning while off.

---

## 3. Verification after implementation (not the study)

Per WP the unit tests listed above, plus one short smoke run per touched SUT and benchmark
(`-sf 1`, short duration, `-nc 1`, `-rst nvme` small volume), checking:
- SUT and workers start, no restarts; loaders/benchmarkers connect (MySQL 9.7: HammerDB over TLS,
  YCSB, Benchbase).
- `--set` values (WP2/WP3) appear in the pod spec and in `SHOW VARIABLES` / server info.
- Placement and sizes (WP6/WP7) as requested (`kubectl get pods -o wide`, resources).
- Check scripts (WP8): relaxed values during load, configured values after; row counts printed.
- Dragonfly cluster: `.dfs` files on every worker after the check/reset (WP4).
- YugabyteDB: tserver PVCs with the requested class and count; Ceph volume metrics not empty (WP9).

---

## 4. Evidence from the prototype tests (2026-10-16, scratchpad only)

| Topic | Result |
|---|---|
| Image argument check | MySQL 9.7.2: all template args valid except `--mysql-native-password=ON` (aborts). MariaDB 12.3.3: only `innodb-buffer-pool-chunk-size` deprecated. CockroachDB 26.3.2, Dragonfly 2.0.2, Redis 8.10.2 flags valid. Citus alpine: `pg_ctl` in `/usr/local/bin`. TiDB 8.5.8: Rocky Linux 9 with `yum`/`curl`. |
| WP5 TLS | Generated CA + cert as Secret on MySQL 9.7.2, cold password cache per client: `mysql` VERIFY_IDENTITY OK (TLSv1.3); HammerDB 6.0 build + 1-min run 36,494 NOPM over TLS; HammerDB 5.0 31,708 NOPM over TLS; YCSB generator 0.11.5 (Java 8) load over TLS; Benchbase generator 0.11.5 TPC-C load via RSA key; TPC-C init script unchanged fails (and leaves `root@'%'` without password), with `IDENTIFIED BY 'root'` OK. |
| WP5 HammerDB without CA | HammerDB 5.0 and 6.0: no TLS -> "Authentication requires secure connection"; `mysql_ssl true` without CA file -> SSL disabled, then `can't read "mysql_ssl_options"`. |
| WP3 Dragonfly env | env vars work; command line beats env. |
| Redis/Dragonfly persistence | Redis standalone writes RDB snapshots (default rules); Redis cluster AOF + RDB; Dragonfly only on shutdown/`SAVE` (no `snapshot_cron`). |
| WP6/WP7 TiDB | placement one PD + one TiKV per node, 2/1/1 with 4 TiKV; PD template resources work; RF 3. |
| WP8 restore | save/relax/restore across sessions works with `CAST`; init-script `SET GLOBAL` values took effect beyond the container limit (pool 40 GiB, log buffer 4 GiB in 16 Gi). |
| WP8 row counts | TPC-H loader logs: all tables exact; lineitem SF 10 = 59,986,052, SF 30 = 179,998,372. |
| WP10 redo log | OFF/ON, idempotent, privileges present. |
| Start-of-WP checks (2026-10-17) | PGBouncer 1.26.0 notes: nothing affecting bexhoma. Exporters: same metric names, MySQL 9.7 OK; pre-existing empty PG metrics noted in WP1. Redis 8.10.2 cluster: args OK, exporter `v1.94.0` with `--is-cluster`. HammerDB 6.0 (generic image), 2 warehouses, 1-min timed run: PostgreSQL 5,214 NOPM, MariaDB 27,039, MySQL 9.7 (TLS) 7,241, Citus 14.2.0 Debian 2,868 / 13.2.0-alpine 3,809, all 0 errors; Citus 14.2.0-alpine ~5 % New Order errors. YugabyteDB chart 2025.2.4 -> 2025.2.7 values identical; per-component `livenessProbe` keys ignored (root key only). |

---

## 5. Readiness for implementation

Ready, with these defaults taken from this plan unless the user decides otherwise:

| # | Point | Default in this plan |
|---|---|---|
| R1 | WP2 argument style | annotation in the template, detection as fallback |
| R2 | WP4 DragonflyReplica | ~~`SAVE` on the master only~~ corrected 2026-10-19: `SAVE` on all workers (see WP4) |
| R3 | WP6 `-rnw` | `+` joins nodes, commas sweep (paired with the resource cells), `sut` = `-rnn` node |
| R4 | WP7 data components / placeholder SUT | **decided:** design in WP7 (`data_components`, `sut_role`, template sizes 250m-1 CPU / 512Mi-1Gi), confirmed by the user 2026-10-17 |
| R5 | WP8 DBMS folders for TPC-H/TPC-DS check scripts | PostgreSQL, MySQL, MariaDB, Citus, PgDuckDB, MonetDB |
| R6 | WP8 row counts | **decided:** counts only, no expected values (user 2026-10-17) |
| R7 | WP10 | later, not part of the first implementation; revised 2026-10-17 to a general import-durability option (`-xld`), two open decisions in WP10 |
| R8 | HammerDB image | **decided:** move to 6.0 (user 2026-10-17); check the other DBMS at the start of WP5 |

R1, R2, R3, R5 and R7 are the plan's defaults; the user did not object (2026-10-17).

The five start-of-WP checks were done on 2026-10-17 (section 4). They changed the plan in two
places: Citus moves to the Debian image `14.2.0` with `PGDATA` on the coordinator (WP1), and the
YugabyteDB script must use the root `livenessProbe.timeoutSeconds` (WP9). No open checks remain.
