# Plan: failed loads are detected, MySQL/MariaDB sizing fits the container

Status: plan only (2026-10-21). Nothing implemented.

Origin: #709 follow-up. The `-xld relaxed` vs `-xld unsafe` comparison (TPC-H MySQL SF 10, nvme,
`-nlp 16`, SUT cl-worker36) failed twice by OOM kill, and bexhoma did not notice. The rerun with a
10G buffer pool worked:

| Run | Code | Result |
|---|---|---|
| relaxed, template pool 96G | 1792538012 | OOMKilled at end of ingest; postload scripts could not connect; summary says loading passed, postload 14 s |
| unsafe, template pool 96G | 1792538799 | OOMKilled; MySQL does not start again with redo off (CrashLoop); bexhoma stops with a traceback, SUT left running despite `-ks no` |
| relaxed, `innodb_buffer_pool_size=10G` | 1792540834 | load 928 s (ingest 170, postload 687), redo 19.7 GB |
| unsafe, `innodb_buffer_pool_size=10G` | 1792542350 | load 617 s (ingest 122, postload 422), redo 89 KB; redo OFF + doublewrite DETECT_ONLY during the load, both ON after |

Memory peaks (Prometheus, `dbms` container, limit 16Gi): 96G pool runs RSS 14.0 / 12.5 GiB before the
kill; 10G pool runs working set 13.4 / 12.5 GiB (page cache up to 6.6 GiB, mostly redo log writes).

---

## 1. What is open

### A. Sizing: the MySQL/MariaDB templates do not fit the default container

- `k8s/deploymenttemplate-MySQL.yml:68` and `deploymenttemplate-MariaDB.yml:59`:
  `--innodb-buffer-pool-size=96G`, written for the templates' own limit of 128Gi (lines 130 / 95).
- bexhoma overwrites the limit with `-rr/-lr` (default 16Gi), but not the buffer pool. Every run
  without `--set ...innodb_buffer_pool_size` therefore has a pool 6x the limit. It survived so far
  because the data did not fill it (SF 1) or only just (SF 10 before `daed9c02`).
- `deploymenttemplate-MySQL.yml:174-177`: `/mysqltmp` (`--tmpdir`) is an `emptyDir` with
  `medium: Memory`, `sizeLimit: 32Gi`. Files there count against the container limit. Index builds
  (`initindexes`) write sort files there. Not the cause this time (cache 0.03 GiB in 1792538799), but
  at SF 30+ it can be.
- Test scripts work around it by hand (`--set ...innodb_buffer_pool_size=32G`, e.g.
  `scripts/test-docs-appmetrics.ps1:198`).

### B. A failed load is reported as a successful one

1. **Loader pods skip tables silently.** `images/tpch/loader_mysql/loader.sh:205-240` retries only
   on `ROLLBACK`; any other error (`ERROR 2013 Lost connection`, `ERROR 2002 Can't connect`) ends
   with `FAILED=0`, i.e. "done". In 1792538012 one pod logged 7 such errors and finished normally.
   The same pattern is in the MariaDB and TPC-DS loaders.
2. **Script errors are only written to a file.** `load_data_asynch` (`bexhoma/configurations/loading.py:131-178`)
   writes stderr to `*.stderr.log` and goes on. Nobody reads it: in 1792538012 every postload script
   failed with `ERROR 2002`, the phase was labelled done, `time_postload` = 14 s.
3. **The volume is labelled as loaded anyway.** The PVC gets `data=True` / `index=True`
   (`loading.py:848-868`, `load_data_asynch` end). A later run without `-rsr` would reuse the broken
   volume as a finished load (`loading_inherited`).
4. **The tests do not cover it.** `TEST passed: Loading measured` only checks that times exist;
   `No SUT container restarts` fails, but loading still counts as passed and the times are reported.
   WP10 (`dev/plan-oltp-storage-dbms.md:373`) assumed "bexhoma already detects SUT restarts and then
   marks the load as failed" - it does not.

### C. bexhoma crashes when the SUT container is gone

- `prepare_init_dbms` -> `upload_file` (`bexhoma/clusters.py:1999`) raises `RuntimeError` after 3
  attempts; nothing catches it (`loading.py:836` -> `experiments/base.py:2373` -> `process`).
- Consequence: no results upload, no evaluation, `-ks no` ignored (SUT stays in CrashLoop until
  deleted by hand).

### D. `-xld unsafe` after a crash

- A MySQL crash with redo disabled leaves an instance that will not start (by design, MySQL docs).
  The volume is lost. bexhoma should say so and remove the PVC (or at least never label it loaded).
- PostgreSQL `unsafe` (`fsync=off`) has the same risk, less visibly (may start with corrupt data).

### E. Smaller items

- `-nlt` / `MYSQL_LOADING_THREADS` is ignored by the active `loader.sh` (TPC-H MySQL).
- #709: closing comment with the numbers above (no code).

---

## 2. Proposed work packages

### P1. Buffer pool follows the memory limit (A)
- In bexhoma, where `-rr/-lr` are written into the SUT container (lifecycle, see WP7/M10 of
  `plan-oltp-storage-dbms.md`): for MySQL and MariaDB, if no `--set ...innodb_buffer_pool_size` is
  given, set it to a share of the memory limit (proposal 60 %, rounded down to whole GiB; >= 1G).
- The share is a config value per DBMS in `k8s-cluster.config` (e.g. `'buffer_pool_share': 0.6`),
  so other DBMS can follow (PostgreSQL `shared_buffers`, later).
- Template comment changes from "ca 75% of 128Gi" to "replaced by bexhoma from the limit".
- `--set` keeps priority; the effective value is printed and reported in the connection info.
- Tests: manifest patch with/without `--set`, limit 16Gi -> 9G, 128Gi -> 76G, MariaDB same.

### P2. tmpdir inside the budget (A)
- Option a: `/mysqltmp` as plain `emptyDir` (disk). Safe for any SF; sort files go to node disk.
- Option b: keep `medium: Memory`, size it with P1 (pool share + tmpfs share <= ~80 % of limit).
- Proposal: a (simpler, no hidden memory use); MariaDB template checked for the same pattern.

### P3. Loaders fail loudly (B1)
- `loader.sh` (TPC-H/TPC-DS, MySQL/MariaDB): unknown error -> retry a few times, then `exit 1`
  (job pod fails, Kubernetes counts it). Connection errors (2002/2013) retry with backoff.
- Check the same pattern in the PostgreSQL/MonetDB loaders.
- bexhoma: a loader job with failed pods marks the load as failed (P4).

### P4. Load status (B2-B4, C, D)
- Script runner (`load_data_asynch`, `run_scripts_on_workers`, reset path): return code of the
  `kubectl exec` plus error patterns in stderr (`ERROR \d+`, `FATAL`, `psql: error`) -> script failed.
  Known harmless stderr (password warning, psql NOTICE) stays allowed (list per DBMS).
- SUT restart between start of loading and end of postload -> load failed (restart counts are
  already read at `experiments/base.py:2650`; read them also after each phase).
- A failed load:
  - writes `loading_failed=<reason>` on pod and PVC, never `data=True` / `index=True`;
  - stops further phases (no postload after a failed ingest);
  - in the summary: `TEST failed: Loading completed (<reason>)`, times shown as not valid;
  - with `-xld unsafe` or `-rsr`: the PVC is deleted, the message says why.
- `upload_file` errors in the loading path are caught: configuration marked failed, experiment
  continues with cleanup (`-ks` respected), results uploaded.
- Plan text WP10 point 6 corrected.

### P5. `-nlt` (E)
- Either implement threads in `loader.sh` (split file, N `mysql` processes) or drop `-nlt` for
  MySQL/MariaDB from the docs. Measurements (1792484612) say more pods give the same; proposal: drop.

### P6. #709 closing comment (E)
- Draft for the user, with the 10G numbers; no code.

---

## 3. Verification (after implementation)

- Unit tests per package (manifest patch, stderr classification, label logic, upload error path).
- Cluster:
  - P1/P2: TPC-H MySQL and MariaDB SF 10, nvme, no `--set`: no restart, pool = 60 % of limit in the
    config dump.
  - P3/P4: forced failure - kill the SUT container during ingest (`kubectl exec ... kill 1`) and
    during postload; expect `loading_failed`, no `data=True`, `TEST failed`, `-ks no` honoured,
    results uploaded. Same with `-xld unsafe` (PVC removed).
- Re-run the relaxed/unsafe comparison without `--set` once P1 is in.

## 4. Open decisions (user)

1. P1 share of the memory limit: 60 %? Configurable per DBMS?
2. P2: tmpdir on disk (a) or sized tmpfs (b)?
3. P4: on a failed load, delete the PVC always, or only with `-xld unsafe` / `-rsr`?
4. P5: implement `-nlt` for MySQL/MariaDB or drop it?
5. Order: proposal P4 + P3 first (wrong results are worse than slow ones), then P1/P2, then P5/P6.
