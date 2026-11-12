## Show Summary

### Workload
HammerDB Workload SF=1 (warehouses for TPC-C)
* Code: 1794485904
* This experiment compares run time and resource consumption of TPC-C queries in different DBMS.
  * TPC-C data is generated and loaded using several threads.
  * Scaling factor (i.e., number of warehouses) is 1. Benchmarking runs for 5 minutes. Ramp-up period is 2 minutes before measurements begin.
  * Load durability is relaxed (-xld; restored after the load).
  * Experiment uses bexhoma version 0.11.17.
  * System metrics are monitored by a cluster-wide installation.
  * Experiment is limited to DBMS ['PostgreSQL'].
  * Import is handled by 1 processes (pods).
  * Loading is fixed to cl-worker38.
  * Benchmarking is fixed to cl-worker38.
  * SUT is fixed to cl-worker36.
  * Database uses ephemeral storage of size 50Gi.
  * Loading is tested with [1] threads, split into [1] pods.
  * Benchmarking is tested with [64] threads, split into [1] pods.
  * Benchmarking is run as [1] times the number of benchmarking pods.
  * Experiment is run once.
  * Maximum DBMS across the whole cluster is 10.
  * The SUT of each configuration's last repetition is kept running after the experiment finishes, unless another configuration waits for its slot.
  * Results are validated against basic correctness requirements.
  * SUT requests 4 CPU and 64Gi RAM. RAM limit is 64Gi.
* No results: the experiment ended before its first result was written, see the tests

### Ingestion
* PostgreSQL-1: 0 of 1 units ok

### Loader Pods with Errors
* PostgreSQL-1: pod bexhoma-loading-postgresql-1-1794485904-1-1-1-pl8sg Failed: sensor exit 1 (Error)
* PostgreSQL-1: pod bexhoma-loading-postgresql-1-1794485904-1-1-1-pl8sg unit warehouses failed (expected 1, reported 0)

### Tests
* TEST failed: Loading job bexhoma-loading-postgresql-1-1794485904-1-1-1 for PostgreSQL-1 reached Kubernetes' terminal Failed condition
* TEST failed: Loader pods without errors (failed: PostgreSQL-1: 2)
