Summary of the designed experiment:

- Workload: YCSB workload a (50/50 single-row primary-key reads and updates) on a 1 GB dataset.
- Factor under test: concurrency, swept from 1 to 32 clients in powers of two.
- System: PostgreSQL on cl-worker36, using the analytical-ssd profile with local node storage (no PVC).
- Repetitions: 3 to assess variability.
- Hypothesis: Throughput rises roughly linearly with client count until saturation, after which throughput plateaus and response latency increases sharply. The design isolates concurrency as the only varying factor and holds everything else equal.
- Run size: 18 benchmark phases, expected to finish well within the one-hour budget.

The experiment has been submitted and is running under experiment code 1787903176.
