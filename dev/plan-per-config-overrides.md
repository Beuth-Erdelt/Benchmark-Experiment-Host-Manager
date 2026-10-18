# Plan: per-tenant overrides (placement and workload)

Status: **planned** (2026-10-16), not implemented. Split out of
[plan-tenancy-sweep.md](plan-tenancy-sweep.md), where it was M1 (`-xtnn`)
and M2 (`-xtw`) as `hardware.py`-only flags. Decided 2026-10-17: a separate
flag `--set-tenant`; `--set` stays a pure manifest patch and is not changed.

## Goal

Let the tenants of one experiment differ in **where the SUT runs** and
**what load its loader/benchmarker generates**, through one generic
mechanism that every benchmark script gets for free, instead of new flags per
script.

Uses:

- Tenancy sweep, placement C: tenants round-robin over several client nodes.
- Tenancy sweep, noisy neighbor: tenant 0 writes 1 MiB blocks, the others
  commit, all with the synchronized start.
- TPC-C tenants (`benchbase.py -mtb container`): one unthrottled tenant next
  to throttled ones.
- [plan-ycsb-sysbench-noisy-neighbor.md](plan-ycsb-sysbench-noisy-neighbor.md),
  where the configurations are tenants.

## Addressing: by tenant id

`--set-tenant` selects tenants by **tenant id**, 0…N−1.

Why not the configuration name (the `@CONFIG` scope of `--set`):

- In container mode the scripts create tenants with
  `configurations.default(...)` and no name; `name_format` is computed but
  unused (`benchbase.py:198`, `tpch.py:266`). The name falls back to docker
  name plus a **process-wide** counter (`configurations/base.py:79-84`), so
  it shifts with the DBMS list, the resource sweep
  (`expand_resource_cells`) and anything else created first. The YCSB
  catalog already ran into this (`experiments/ycsb_catalog.py:95`).
- The tenant id is 0…N−1 in every script, already names the PVC
  (`postgresql-{tenant}-{N}`, `hardware-{tenant}-{N}`), and is passed as
  `BEXHOMA_TENANT_ID` to the jobs and as `TENANT` to the evaluator.
- `-mtn 8 ... --set-tenant "0:..."` stays correct when N or the DBMS list
  changes.

`@CONFIG` on `--set` stays as it is, for heterogeneity without tenants
(resource sweep).

## Facts this plan relies on

- `--set` today: `SELECTOR_RE` (`experiments/base.py:75-80`) accepts only
  `deployment|statefulset[NAME][@CONFIG].container[C].PARAM`, and
  `patch_container()` (`configurations/manifest.py:66`) only rewrites
  `-c key=value` pairs in the container's `args`.
- `patch_dbms_args()` runs on the SUT manifest at `lifecycle.py:798`,
  **before** the resources block (`lifecycle.py:1295-1364`) writes the pod's
  `nodeSelector` from `cfg.resources['nodeSelector']`, including the
  hostname that `-rnn` sets (`experiments/base.py:693-699`). A node set by
  patching the manifest would be overwritten by `-rnn`. **Placement must go
  through `cfg.resources`**, not through manifest patching.
- `SutConfiguration.set_resources()` merges into `cfg.resources`
  (`configurations/base.py:505`).
- Job env starts from `env_default` in `create_manifest_job()`
  (`configurations/manifest.py:251ff.`) and is extended by the
  loading/benchmarking parameters of the round.
- `SutConfiguration` has `num_tenants` and `tenant_per`
  (`configurations/base.py:149-150`) but **no tenant id**; it lives only in
  each script's loop variable.
- Container tenancy exists in `benchbase.py`, `tpch.py` and `hardware.py`.
  `ycsb.py` has none. In `benchbase.py` the MySQL tenant branch sets
  `TENANT` for the evaluator but not `BEXHOMA_TENANT_ID` for the jobs, and no
  container-tenant branch calls `set_benchmark_resetscript`.

## Design

### Syntax

```
--set-tenant "IDS:TARGET=VALUE"
```

- `IDS`: one id (`0`), a range (`1-7`), or a comma list of ids and ranges
  (`0,3,6-8`). Everything before the first `:`.
- `TARGET=VALUE`: split at the first `=`, so values may contain `=` and `:`.
- Repeatable, like `--set`.

| Target | Example | Applied |
|---|---|---|
| `node` | `0,3,6:node=cl-worker21` | `cfg.resources['nodeSelector']['kubernetes.io/hostname']`, before the SUT manifest is built |
| `loading.env.NAME` | `0:loading.env.BENCHBASE_TERMINALS=64` | env of the tenant's loading job, after every other source |
| `benchmarking.env.NAME` | `0:benchmarking.env.HARDWARE_FIO_BS=1M` | env of the tenant's benchmarking jobs, after every other source |
| `deployment[NAME].container[C].PARAM` (or `statefulset[...]`) | `1-7:deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=2GB` | the `--set` manifest patch, restricted to these tenants |

The last row reuses the `--set` selector grammar without `@CONFIG`, so a
per-tenant DBMS knob needs no new patch code.

Examples:

```
# placement C: round-robin over three client nodes
--set-tenant "0,3,6,9:node=cl-worker21"
--set-tenant "1,4,7,10:node=cl-worker34"
--set-tenant "2,5,8,11:node=cl-worker37"

# noisy neighbor (fio): tenant 0 seqwrite, the rest the commit default
--set-tenant "0:benchmarking.env.HARDWARE_FIO_BS=1M"
--set-tenant "0:benchmarking.env.HARDWARE_FIO_IODEPTH=8"
--set-tenant "0:benchmarking.env.HARDWARE_FIO_ENGINE=libaio"
--set-tenant "0:benchmarking.env.HARDWARE_FIO_FDATASYNC=0"

# TPC-C: tenant 0 unthrottled next to throttled tenants
--set-tenant "0:benchmarking.env.BENCHBASE_TARGET=16384"
```

The fio "profiles" (commit, randwrite, seqwrite) from the tenancy plan
become documented bundles of such lines, not code.

### Rules

- **Precedence.** `--set-tenant` beats `--set`, `-rnn` and the sweep values
  for the same thing; between two `--set-tenant` operations that hit the
  same tenant and target, the last one wins. "Everyone does X, tenant 0
  does Y" is then the normal experiment plus one override.
- **Refusals at startup**, with a clear message: no tenancy (`-mtn 0`); an
  id ≥ N; a malformed id list or range; an unknown target; an empty env
  name. With schema or database tenancy, `node` and manifest targets are
  refused (one shared SUT); env targets only once M6 exists.
- **`node` with `-rnn`:** the tenant's node replaces `-rnn`'s hostname for
  that tenant. The other selectors `-rnn` sets (`cpu`, `gpu`) are kept;
  check that the `gpu` nodes, which carry no `cpu` label value, still match
  (see Risks).
- **Env overrides apply to every round** of the tenant. They do not
  multiply rounds; a sweep value for the same variable is overridden.
- **Visible:** every override that took effect is printed like `--set`
  does (`manifest.py:182`), and listed in `workload['info']`.

## Implementation sketch

### M1: tenant id on the configuration

- `SutConfiguration.tenant_id = None`; set it in every container-tenant loop
  (`benchbase.py` all DBMS branches, `tpch.py`, `hardware.py`), e.g. via a
  new `configurations.default(..., tenant=tenant)` keyword so the loops can't
  forget it.
- Derive `BEXHOMA_TENANT_ID` and `TENANT` from `cfg.tenant_id` in one place
  (manifest env / eval parameters) instead of each loop; this also fixes the
  MySQL branch.
- Store `tenant_id` in `connections.config`.
- Tests: every tenant loop sets ids 0…N−1; env and eval parameter derived.

### M2: the flag and its parser

- `cli_args.py`: `--set-tenant`, `dest="set_tenants"`, `action="append"`,
  next to `--set`.
- `experiments/base.py`: `parse_set_tenant_arg(s)` returning
  `(tenant_ids, target_kind, target, value)`; the manifest target reuses
  `SELECTOR_RE` (with `@CONFIG` refused, it would mix two scopes). Parsed
  operations stored as `experiment.tenant_args`, like `dbms_args`.
- Validation (see Rules) after `-mtb`/`-mtn` are known.
- Tests: parsing of ids, ranges, lists; split at the first `:` and `=`;
  refusals; existing `--set` tests unchanged.

### M3: node target

- Before the SUT manifest is built, apply the tenant's `node` operations
  via `cfg.set_resources(nodeSelector={... 'kubernetes.io/hostname': node})`,
  on top of what `-rnn` put there.
- Record the node actually used per tenant (from the pod) in
  `connections.config` / `connections.md`; it is the client node for fio.
- Tests: a tenant's node replaces `-rnn`'s hostname for that tenant only;
  `cpu`/`gpu` selectors handled.

### M4: env and manifest targets

- In `create_manifest_job()`, after all env sources are merged, apply the
  tenant's `loading.env.*` / `benchmarking.env.*` operations to the matching
  job kind.
- In `patch_dbms_args()`, after the `--set` operations, apply the tenant's
  manifest operations, so they win.
- Echo the overridden variables in the job logs (they mostly are already,
  e.g. `HARDWARE_FIO_*` via `benchmarker.sh`) so evaluators read the values
  each tenant actually ran with.
- Tests: override wins over sweep values and over `--set`; only the
  selected tenants change.

### M5: use it

- Tenancy sweep placement C and the synchronized noisy neighbor
  ([plan-tenancy-sweep.md](plan-tenancy-sweep.md)).
- Docs: `--set-tenant` next to `--set` in the CLI docs, and a section in the
  tenancy docs with the placement and noisy-neighbor examples.

### M6 (optional, not scheduled): env targets for schema and database tenancy

With schema or database tenancy all tenants share **one** configuration and
one SUT pod; `node` and manifest targets cannot apply. Loading and
benchmarking are each **one job with one pod per tenant**, and each pod
derives its tenant in the shell: `BEXHOMA_TENANT_ID=$((BEXHOMA_CHILD - 1))`
(`images/benchbase/generator.sh:81-94`, `images/benchbase/benchmarker.sh:82-94`).
A per-tenant env value is therefore a **per-pod** value, which the existing
per-pod Redis config carries.

What exists (checked 2026-10-17):

- Python: `SutConfiguration._push_pod_configs()` (`configurations/base.py:645`)
  writes, for pod i = 1…num_pods, `parameters` merged with
  `pod_parameters[i-1]` as JSON to `{queue}-config-{i}`. Called for every
  benchmarking round (`configurations/benchmarking.py:224`) and every
  loading job (`configurations/loading.py:346`), from the round entry's
  `pod_parameters`.
- Images: every loader, generator and benchmarker script reads its own key
  `...-config-$BEXHOMA_CHILD` and exports each entry as `BEXHOMA_POD_<key>`
  (benchbase, hammerdb, ycsb, hardware, dbmsbenchmarker benchmarkers; tpch
  and tpcds generators/loaders; ycsb and benchbase generators).

What is missing:

1. **Nothing fills `pod_parameters`.** `add_benchmarking_parameters()` /
   `add_benchmark_list()` / the loading equivalents have no way to set it,
   so every pod gets the same merged dict.
2. **Nothing uses `BEXHOMA_POD_*`.** The workload reads the plain names
   (`BENCHBASE_TARGET`, `HARDWARE_FIO_BS`, ...) from the job manifest's
   env. Even a filled `pod_parameters` changes nothing yet.
3. **The shell parser is minimal.** It is `awk` on `"key":"value"` pairs:
   string values only, no commas or quotes in values; an unquoted JSON
   number does not match. `_push_pod_configs` must `str()` every value.

Steps:

- `--set-tenant` env operations, in schema/database mode, go into
  `pod_parameters[tenant]` of the one loading/benchmarking job (pod i ↔
  tenant i−1), for every round. In container mode they stay plain job env
  (M4).
- `pod_parameters` stored in the round entry and kept by
  `add_benchmark_list()` (and the loading counterpart).
- Each image script, right after the per-pod read: export every
  `BEXHOMA_POD_<NAME>` (except the `BEXHOMA_POD_CONFIG_*` helpers) as
  `<NAME>` and echo it, so the workload uses it and the evaluator records
  it. One generic block, the same in every script; image rebuilds.
- Evaluators that aggregate per phase and take parameters from the first
  pod (e.g. `evaluators/hardware.py:326-330`) must group by tenant or by
  the overridden columns when tenants differ.

Open points:

- **Pod ↔ tenant only holds for one pod per tenant.** The scripts set
  `BEXHOMA_NUM_PODS=1` and tenant = `BEXHOMA_CHILD − 1`, while
  `benchbase.py` starts `loading_pods × num_tenants` loader pods. With
  `-nlp > 1` (or `-nbp > 1`) the tenant ids run past N−1. This looks like an
  existing limitation of schema/database tenancy; check, and refuse
  `--set-tenant` with more than one pod per tenant until it is fixed.
- Loading done by scripts in the SUT pod (`loading.py:1035-1099`, threads
  per tenant via `kubectl exec`) is not a job and gets no per-pod config.
  Only job-based loaders and generators are covered.
- The same path also gives "several fio pods on one SUT and volume with
  different workloads" (`-nbp N`, no tenancy), the former "Case B" of the
  tenancy plan; that would need its own flag, not `--set-tenant`.

## Risks and open points

- **Many tenants, many lines.** 12 tenants on 3 nodes is 3 lines with id
  lists, which is fine; a positional shorthand (a node list cycled over
  tenants) only if this gets tedious.
- **`gpu` nodes as clients** (cl-worker34/37): `-rnn` also sets the `cpu`
  label selector, which these nodes do not carry; taints and Kyverno
  tolerations to check.
- **Variable names differ per benchmark** (`HARDWARE_FIO_*`,
  `BENCHBASE_*`, `HAMMERDB_*`). The mechanism is generic, the knowledge which
  variable means what is not; document the useful ones per benchmark.
- **Evaluation of mixed tenants.** Per-tenant summaries exist
  (`get_summary_benchmark_per_phase_multitenant`); totals over tenants with
  different workloads are not meaningful and should be reported per
  workload group.
