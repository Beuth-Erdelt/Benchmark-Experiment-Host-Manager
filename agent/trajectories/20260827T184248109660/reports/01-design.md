I designed a minimal YCSB experiment on PostgreSQL to satisfy the request for a quick and simple example. The specification varied client concurrency (rounds: [1, 2]) to isolate a factor, set fixed resource envelopes (cpu/limit and memory/limit equal), and pinned all pods to a single capable node (cl-worker21). The hypothesis stated that throughput/latency change with concurrency under a small configuration.

The last validation failed on M5.1: repetitions must be at least 2 for a comparison, but I only had 1. I would fix this by changing repetitions from 1 to 2, then re-validate and submit.
