Summary of the designed experiment:

I designed a 2×2 factorial experiment to isolate whether halving CPU cores or halving memory causes slowdowns for your analytical workload. The experiment uses the TPC-H workload (SF=1, ~1 GB) with multi-join/aggregation queries (5,7,8,9,21) to match your nightly job profile. It compares:

- Baseline: 16 CPU cores, 64 GiB RAM
- CPU-halved: 8 cores, 64 GiB RAM
- Memory-halved: 16 cores, 32 GiB RAM
- Both-halved: 8 cores, 32 GiB RAM

Each configuration runs 3 repetitions with 2 concurrent streams, ensuring statistical significance and keeping run time under an hour. The PostgreSQL system is pinned to cl-worker36 with ephemeral storage. The hypothesis will be validated by measuring query latency differences attributable to each resource factor independently, as required by the discriminates field. The experiment code is 1787928413.
