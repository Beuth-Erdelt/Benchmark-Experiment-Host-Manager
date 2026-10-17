# Plan: per-tenant overrides (placement and workload)

Status: **planned** (2026-10-16), not implemented. Split out of
[plan-tenancy-sweep.md](plan-tenancy-sweep.md), where it was M1 (`-xtnn`)
and M2 (`-xtw`) as `hardware.py`-only flags.

## Goal

Let the configurations of one experiment differ in **where the SUT runs**
and **what load its loader/benchmarker generates**, through one generic
mechanism that every benchmark script gets for free, instead of new flags per
script.

Uses:

- Tenancy sweep, placement C: tenants round-robin over several client nodes.
- Tenancy sweep, noisy neighbor: tenant 0 writes 1 MiB blocks, the others
  commit, all with the synchronized start.
- TPC-C tenants (`benchbase.py -mtb container`): one unthrottled tenant next
  to throttled ones.
- [plan-ycsb-sysbench-noisy-neighbor.md](plan-ycsb-sysbench-noisy-neighbor.md)
  and any other experiment with several configurations that should not be
  identical.

## Addressing: by tenant id

Overrides select configurations by **tenant id**, `@tenant:ID`, next to
the existing `@CONFIG` scope of `--set`.

Why not the configuration name:

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
- `-mtn 8 ... @tenant:0` stays correct when N or the DBMS list changes.

Syntax: `@tenant:0`, `@tenant:1-7`, `@tenant:0,3,6`. `@CONFIG` stays for
heterogeneity without tenants (resource sweep).

**Precedence:** a scoped operation beats an unscoped one, whatever the order
on the command line; between two scoped ones, the last wins. "Everyone does
X, tenant 0 does Y" is then one unscoped default plus one override.

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

### Two override targets

| Target | Selector | Applied |
|---|---|---|
| SUT node | `sut@tenant:ID.node=<hostname>` | into `cfg.resources['nodeSelector']['kubernetes.io/hostname']` before the manifest is built |
| Job env | `job[loading\|benchmarking]@tenant:ID.env[NAME]=<value>` | into the job's env in `create_manifest_job()`, after every other source |

Both accept `@CONFIG` as well as `@tenant:`, and both accept no scope at
all (applies to every configuration). The node target is deliberately not
spelled as a manifest path: it has to win over `-rnn`, which a manifest
patch cannot (see Facts).

Examples:

```
# placement C: round-robin over three client nodes
--set "sut@tenant:0,3,6,9.node=cl-worker21"
--set "sut@tenant:1,4,7,10.node=cl-worker34"
--set "sut@tenant:2,5,8,11.node=cl-worker37"

# noisy neighbor (fio): tenant 0 seqwrite, the rest the commit default
--set "job[benchmarking]@tenant:0.env[HARDWARE_FIO_BS]=1M"
--set "job[benchmarking]@tenant:0.env[HARDWARE_FIO_IODEPTH]=8"
--set "job[benchmarking]@tenant:0.env[HARDWARE_FIO_ENGINE]=libaio"
--set "job[benchmarking]@tenant:0.env[HARDWARE_FIO_FDATASYNC]=0"

# TPC-C: tenant 0 unthrottled next to throttled tenants
--set "job[benchmarking]@tenant:0.env[BENCHBASE_TARGET]=16384"
```

The fio "profiles" (commit, randwrite, seqwrite) from the tenancy plan
become documented bundles of such lines, not code.

### Rules

- `@tenant:` on an experiment without container tenancy, or an id ≥ N: refuse
  at startup with a clear message.
- `sut...node` together with `-rnn`: the scoped node replaces `-rnn`'s
  hostname for that configuration. Every other selector `-rnn` sets
  (`cpu`, `gpu`) is kept; check that the `gpu` nodes, which carry no `cpu`
  label value, still match (see Risks).
- Env overrides apply to every round of the configuration. They do not
  multiply rounds and do not interact with the sweep lists (`-nbt`,
  `-xnbf`, ...): a sweep value for the same variable is overridden.
- Every override that took effect is printed like `--set` already does
  (`manifest.py:182`) and listed in `workload['info']`.

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

### M2: scope parsing

- Extend `parse_set_arg()` with the `@tenant:` scope (single, list, range)
  and the two new targets (`sut...node`, `job[...]...env[NAME]`). The
  existing `deployment|statefulset ... container[...]` form gets
  `@tenant:` too.
- A shared `scope_matches(sel, cfg)` used by all three targets, plus the
  precedence rule (scoped > unscoped, then last wins).
- Validation at startup (unknown id, no tenancy, malformed range).
- Tests: parsing, matching, precedence, refusals; existing `--set` tests
  unchanged.

### M3: node target

- Before the SUT manifest is built, apply matching `sut...node` operations
  via `cfg.set_resources(nodeSelector={... 'kubernetes.io/hostname': node})`,
  on top of what `-rnn` put there.
- Record the node actually used per tenant (from the pod) in
  `connections.config` / `connections.md`; it is the client node for fio.
- Tests: a scoped node replaces `-rnn`'s hostname for one configuration
  only; `cpu`/`gpu` selectors handled.

### M4: env target

- In `create_manifest_job()`, after all env sources are merged, apply
  matching `job[loading|benchmarking]...env[NAME]` operations.
- Echo the overridden variables in the job logs (they mostly are already,
  e.g. `HARDWARE_FIO_*` via `benchmarker.sh`) so evaluators read the values
  each tenant actually ran with.
- Tests: override wins over sweep values; only the selected tenants' jobs
  change.

### M5: use it

- Tenancy sweep placement C and the synchronized noisy neighbor
  ([plan-tenancy-sweep.md](plan-tenancy-sweep.md)).
- Docs: one section in the tenancy docs with the placement and noisy-neighbor
  examples.

## Not covered: schema and database tenancy

There all tenants share one SUT pod, so per-tenant placement does not
apply, and a per-tenant workload would mean different env **per pod inside
one loader/benchmarker job**. `@tenant:` refuses these modes. That is the
per-pod mechanism, kept here from the tenancy plan's former M2 "Case B":

- `SutConfiguration._push_pod_configs()` (`configurations/base.py:622`)
  writes `{queue}-config-{i}` to Redis from the round entry's
  `pod_parameters`; `images/hardware/benchmarker/benchmarker.sh` (lines
  75–85) exports it as `BEXHOMA_POD_<key>`. As of 2026-10-11 this is
  plumbing only: nothing fills `pod_parameters`,
  `add_benchmarking_parameters()` / `add_benchmark_list()` do not carry it,
  and no script reads `BEXHOMA_POD_*`.
- Making it work: `add_benchmarking_parameters(..., pod_parameters=None)`
  stored in the round entry and kept by `add_benchmark_list()`;
  `benchmarker.sh` exports `BEXHOMA_POD_HARDWARE_*` as `HARDWARE_*` (image
  rebuild); the hardware evaluator groups per-phase aggregation by the fio
  parameters instead of taking the first pod's; `_push_pod_configs` should
  `str()` all values (the shell parser handles only plain strings).

A separate plan if it is ever needed.

## Risks and open points

- **Selector spelling.** `sut...node` and `job[...]...env[...]` are new
  forms next to the manifest-path form. Alternative: a separate flag
  (`--set-tenant`) to keep `--set` purely a manifest patch. Decide in M2.
- **Many tenants, many lines.** 12 tenants on 3 nodes is 3 lines with id
  lists, which is fine; a positional shorthand (`-rnn a,b,c` cycled over
  tenants) only if this gets tedious.
- **`gpu` nodes as clients** (cl-worker34/37): `-rnn` also sets the `cpu`
  label selector, which these nodes do not carry; taints and Kyverno
  tolerations to check (tenancy plan, M1 notes).
- **Variable names differ per benchmark** (`HARDWARE_FIO_*`,
  `BENCHBASE_*`, `HAMMERDB_*`). The mechanism is generic, the knowledge which
  variable means what is not; document the useful ones per benchmark.
- **Evaluation of mixed tenants.** Per-tenant summaries exist
  (`get_summary_benchmark_per_phase_multitenant`); totals over tenants with
  different workloads are not meaningful and should be reported per
  workload group.
