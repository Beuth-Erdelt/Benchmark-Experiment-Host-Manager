# Plan: failed loads are detected, MySQL/MariaDB sizing fits the container

Status: **parked 2026-10-22.** P1 implemented as option A3 and committed (`8a530999`); cluster
check done 2026-10-22 (section 3, "Pending test runs": passed). P2-P6 open.

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
- bexhoma overwrites the request with `-rr` (default 16Gi) and the limit with `-lr` (default 0 =
  bexhoma removes the limit, `lifecycle.py:1457`). The namespace then sets the limit equal to the
  request, so the effective limit is `-lr`, else `-rr`. The buffer pool is not touched. Every run
  without `--set ...innodb_buffer_pool_size` therefore has a pool 6x the limit. It survived so far
  because the data did not fill it (SF 1, small OLTP) or only just (SF 10 before `daed9c02`).
- Affects every benchmark on these templates: TPC-H, TPC-DS, HammerDB TPC-C, YCSB, Benchbase. The
  test scripts work around it with ~90 `--set ...innodb_buffer_pool_size=32G` lines.
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

### P1. Buffer pool fits the container (A)

Options (2026-10-22):

| | Idea | For | Against |
|---|---|---|---|
| A1 | bexhoma sets the pool to a share of the effective limit (`-lr`, else `-rr`), e.g. 60 %, unless `--set` gives one | always fits, follows `-rr` sweeps | bexhoma decides a DBMS setting; must be reported |
| A2 | template placeholder `--innodb-buffer-pool-size={buffer_pool}`, filled by A1's rule | visible in the template that it is computed | more template machinery |
| A3 | small static default in the template (8G); larger pools only via `--set` | simple, no hidden logic | wastes memory with large `-rr`; scripts keep their `--set` |
| A4 | start check: pool (template or `--set`) > ~80 % of the effective limit -> warning or stop | cheap guard, works for every DBMS setting | fixes nothing alone |
| A5 | MySQL sizes itself: `--container-aware=ON` + `--innodb-dedicated-server=ON` | native | MySQL only; behaviour on 9.7.2 to check |

**Decision (user, 2026-10-22): A3.** Implemented 2026-10-22:
- MySQL: `--innodb-buffer-pool-size=8G`, `--innodb-buffer-pool-instances=8`, no
  `--innodb-buffer-pool-chunk-size` (default 128M). With 2G chunks x 16 instances MySQL rounds a
  pool up to a multiple of 32G (unless the pool is smaller than that, then it shrinks the chunk);
  with 128M x 8 a `--set` value is rounded to at most the next 1G.
- MariaDB: `--innodb-buffer-pool-size=8G` (no instances/chunk setting in 12.x).
- 8G = half of the default `-rr 16Gi`: the 10G runs peaked at 13.4 GiB working set (page cache,
  16 loader connections), so 8G leaves room. Runs with more memory set the pool with `--set`.
- Comments in the test scripts ("template: 96G") and docs/DBMS.md updated; recorded outputs
  (docs/TestCases.md, docs/Example-*.md) unchanged.
- Results of runs without `--set` change compared with earlier ones (pool 96G -> 8G); for SF 1 and
  small OLTP the old pool never filled, so the difference is the smaller cache only.
- A4 remains useful as a guard later (also for PostgreSQL `shared_buffers`).

### P2. tmpdir inside the budget (A)
- Option a (T1): `/mysqltmp` as plain `emptyDir` (disk). Safe for any SF; sort files go to node disk.
- Option b (T2): keep `medium: Memory`, size it inside the budget (pool + tmpfs <= ~80 % of limit).
- Proposal: a (simpler, no hidden memory use). The MariaDB template has no RAM-backed tmpdir.
- Not part of A3; open.

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

### Pending test runs (P1/A3, parked 2026-10-22, to be run by the user)

TPC-H SF 10, load only, nvme, no `--set` (template 8G), one after the other:

```powershell
foreach ($dbms in @('MySQL','MariaDB')) {
  bexhoma tpch -dbms $dbms -sf 10 -nc 1 -nlp 16 -xii -xic -xis -rst nvme -rss 100Gi -rsr -ks no -ms 10 `
    -rnn <SUT node> -rnl <loader node> -rnb <loader node> `
    load 2>&1 | Out-File "logs_tests\testcase_tpch_$($dbms.ToLower())_bp8g_default.log" -Encoding utf8
}
```

Check per run: config dump `innodb_buffer_pool_size` = 8589934592; no SUT restart; peak working set
< 16Gi (Prometheus `container_memory_working_set_bytes`, `dbms`); lineitem 59,986,052, 8 PK / 9 FK;
no `ERROR` in the `*.stderr.log` of the postload scripts.

First attempt 1792662245 (MySQL, SUT cl-worker37, loaders cl-worker39) was stopped after 83 min and
cleaned up: 15 of 16 loader pods waited for the 16th, which stayed `Pending` with "Too many pods" -
cl-worker39 was at its pod limit. Pick a loader node with free pod slots (cl-worker38 took 16
loaders before), or lower `-nlp`. This hang is the loader barrier (all pods of a job must run) - no
timeout fails it; candidate for P4.
- The volume `bexhoma-storage-mysql-nvme-tpch-10` holds a partial load from 1792662245; `-rsr`
  removes it.

**Result (2026-10-22, SUT cl-worker36, loaders cl-worker38): passed.**

| | MySQL 1792675567 | MariaDB 1792677130 |
|---|---|---|
| Buffer pool (config dump) | 8589934592 (8G) | 8589934592 (8G) |
| SUT restarts | 0 | 0 |
| Peak RSS / cache / working set | 9.2 / 7.3 / 10.5 GiB | 8.6 / 1.0 / 8.6 GiB |
| lineitem, orders | 59,986,052 / 15,000,000 | 59,986,052 / 15,000,000 |
| Keys | 8 PK / 9 FK | 8 PK / 9 FK |
| Errors (postload stderr, loader logs) | none | none |
| Load (ingest / postload) | 970 s (134 / 762) | 1359 s (169 / 1114) |

MySQL with 8G vs. the 10G run 1792540834 (same nodes, `-xld relaxed`): 970 s vs. 928 s; postload
762 vs. 687 s. Postload dominates at a pool smaller than lineitem (8.7 GB data + 3.5 GB index).

## 4. Open decisions (user)

1. P1: decided A3 (static 8G) on 2026-10-22; A1/A2/A4/A5 kept as later options.
2. P2: tmpdir on disk (a) or sized tmpfs (b)?
3. P4: on a failed load, delete the PVC always, or only with `-xld unsafe` / `-rsr`?
4. P5: implement `-nlt` for MySQL/MariaDB or drop it?
5. Order: proposal P4 + P3 first (wrong results are worse than slow ones), then P1/P2, then P5/P6.
