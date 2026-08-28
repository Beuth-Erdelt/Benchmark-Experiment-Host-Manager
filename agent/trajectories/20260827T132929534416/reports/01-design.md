I've been stuck on validation errors for my YCSB experiment design. The core issue is that when I declare a single system (`PostgreSQL`), the validator expects either:

1. An explicit `discriminates: []` to indicate no factors vary, OR  
2. A non-empty list of varying factors like `[system]` if comparing multiple systems

My attempts with both approaches have failed validation. The error messages suggest there's a mismatch between what I declare in `discriminates` and what the validator detects as actually varying across my system configurations. Since I'm only running one PostgreSQL instance (no profile, no override), nothing should vary—so an empty list seems right—but it keeps rejecting this interpretation.

I've exhausted all 5 validation calls without achieving a valid specification that answers "run YCSB on PostgreSQL." The unresolved question is whether the catalog requires at least two systems to be declared for any experiment (making `discriminates: [system]` mandatory), or if there's another structural requirement I'm missing in how single-system experiments should be specified.
