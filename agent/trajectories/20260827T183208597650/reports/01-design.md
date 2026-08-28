I designed a simple, valid YCSB experiment on PostgreSQL that satisfies the catalog and the method contract. The specification runs YCSB workload A (read/update 50/50) on PostgreSQL with a small dataset (SF=1), two concurrency levels (1 and 4 clients), and three repetitions to allow a basic estimate of variance. Resources are fixed (CPU and memory request=limit) to ensure a hard envelope. The factor under test is concurrency, and everything else is held equal across arms.

The experiment is ready to run as specified in inbox/ycsb-postgres-quick.yml.
