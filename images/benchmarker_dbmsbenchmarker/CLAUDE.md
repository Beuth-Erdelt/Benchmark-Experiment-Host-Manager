# images/benchmarker_dbmsbenchmarker — development notes

## Overview

The `images/benchmarker_dbmsbenchmarker/` directory contains the Docker image template
for running DBMSBenchmarker query workloads within the Bexhoma framework.

## Directory layout

```
images/benchmarker_dbmsbenchmarker/
├── Dockerfile_template    — image template; {version} replaced by create_Dockerfiles.py
├── create_Dockerfiles.py  — generates the versioned Dockerfile from Dockerfile_template
├── benchmarker.sh         — entrypoint: runs the timed DBMSBenchmarker workload
├── connections.config     — default DBMS connection config (used in TESTRUN mode)
├── queries.config         — default query config (used in TESTRUN mode)
└── README.md              — environment variable reference
```

`Dockerfile_template` is the canonical source. Do not edit generated `Dockerfile` files directly.

---

## Execution flow (`benchmarker.sh`)

1. Capture script start time.
2. Optionally sleep until `BEXHOMA_TIME_START` (synchronized start across pods).
3. Create `/results/$BEXHOMA_EXPERIMENT/` if it does not exist.
4. Pop the pod's child index from the Redis queue
   `bexhoma-benchmarker-<CONNECTION>-<EXPERIMENT>`.
5. **Multi-tenant adjustment**: if `BEXHOMA_TENANT_BY` is `schema` or `database`,
   divide `BEXHOMA_NUM_PODS` by `BEXHOMA_TENANT_NUM` and compute the per-tenant
   child index; override `BEXHOMA_SCHEMA` or `BEXHOMA_DATABASE` accordingly.
   Original values are saved so pod-count synchronisation uses the full count.
6. Increment and poll the Redis counter
   `bexhoma-benchmarker-podcount-<CONNECTION>-<EXPERIMENT>` until all
   `BEXHOMA_NUM_PODS` pods (full count) are ready.
7. If `BEXHOMA_TENANT_BY=container`, additionally wait on the cross-tenant counter
   `bexhoma-benchmarker-podcount-<EXPERIMENT>` until `BEXHOMA_NUM_PODS_TOTAL` pods
   are ready.
8. Restore per-tenant `BEXHOMA_CHILD` and `BEXHOMA_NUM_PODS`.
9. Convert `DBMSBENCHMARKER_SHUFFLE_QUERIES` and `DBMSBENCHMARKER_RECREATE_PARAMETER`
   from Python boolean strings (`True`/`False`) to integers (`1`/`0`).
10. Run `python benchmark.py run` with the full flag set.  Verbose mode adds
    `-d -vq -vr -vp -vs`.
11. Extract the precise benchmark duration from DBMSBenchmarker's log line
    `DBMSBenchmarker duration...: N [s]` and compute `bexhoma_end_epoch_computed`.
12. Emit `BEXHOMA_DURATION`, `BEXHOMA_START`, `BEXHOMA_END` to stdout.

---

## Multi-tenant modes

| `BEXHOMA_TENANT_BY` | Effect on `BEXHOMA_NUM_PODS` | Effect on `BEXHOMA_CHILD` | Override |
|---|---|---|---|
| `schema` | Divided by `BEXHOMA_TENANT_NUM` | `BEXHOMA_CHILD % BEXHOMA_TENANT_NUM + 1` | `BEXHOMA_SCHEMA=tenant_<N>` |
| `database` | Divided by `BEXHOMA_TENANT_NUM` | `BEXHOMA_CHILD % BEXHOMA_TENANT_NUM + 1` | `BEXHOMA_DATABASE=tenant_<N>` |
| `container` | Unchanged | Unchanged | Separate pod-count barrier on `BEXHOMA_NUM_PODS_TOTAL` |
| *(empty)* | Unchanged | Unchanged | None |

Pod-count synchronisation always uses the full `BEXHOMA_NUM_PODS` (restored before
the wait loop).

---

## Key design decisions

| Decision | Reason |
|---|---|
| `DBMSBENCHMARKER_CODE` has no Docker ENV default | The value is used in a `RUN mkdir` build step; giving it an ENV default would cause Docker to create a mis-named directory at image build time |
| Timing uses wall-clock epoch, then refined | DBMSBenchmarker reports its internal duration; the script computes `END = START + duration` for higher precision than a post-run `date` call |
| Python boolean conversion before flag expansion | DBMSBenchmarker's environment variables use Python `True`/`False` strings; shell needs integers for arithmetic tests |
| Disabled `-sl` and `-st` flags | Timing is handled by the shell (`BEXHOMA_TIME_START` sleep); passing them again to DBMSBenchmarker would double-count the wait |
| Verbose and non-verbose paths are two explicit branches | Makes the non-verbose case self-contained and easy to read; no conditional flag assembly needed |

---

## DBMSBenchmarker CLI flags

| Flag | Argument | Meaning |
|---|---|---|
| `-f` / `-r` | `DBMSBENCHMARKER_CODE` | Config and result base folder |
| `-cs -sf` | `DBMSBENCHMARKER_CONNECTION` | Create sub-folder per DBMS connection |
| `-ms` | `DBMSBENCHMARKER_CLIENT` | Maximum number of connection sub-folders |
| `-c` | `DBMSBENCHMARKER_CONNECTION` | DBMS connection name to benchmark |
| `-ca` | `DBMSBENCHMARKER_ALIAS` | Alias for the DBMS connection |
| `-cf` | `<CONNECTION>.config` | Per-connection config file |
| `-rcp` | `0` or `1` | Recreate query parameters per stream |
| `-sid` | `BEXHOMA_CHILD` | Stream ID for parallel execution |
| `-ssh` | `0` or `1` | Shuffle query order by stream ID |
| `-mps` | *(flag)* | Monitor per stream, not per query |
| `-fixdb` | `BEXHOMA_DATABASE` | Override the database name |
| `-fixs` | `BEXHOMA_SCHEMA` | Override the schema name |
| `-d -vq -vr -vp -vs` | *(flags)* | Verbose output (verbose mode only) |
| `-db` | *(flag)* | Debug mode (dev mode only) |

---

## Dockerfile template

`Dockerfile_template` contains the placeholder `{version}` which `create_Dockerfiles.py`
replaces with the target DBMSBenchmarker Git tag (e.g. `v0.14.6`).  Both the pip
install step and the `git clone` step use the same tag to ensure consistency.

---

## Style conventions

- **Dockerfile_template**: `ENV` declarations use `KEY=value` form; grouped by concern
  under section headers.  The `{version}` placeholder appears only in the two
  DBMSBenchmarker install/clone steps.
- **Shell scripts**: Section banners use `#### Title ####`.  No commented-out dead
  code; no debug write-only commands.
- **READMEs**: One entry per ENV, grouped by concern, with clear descriptions of
  units and defaults.
