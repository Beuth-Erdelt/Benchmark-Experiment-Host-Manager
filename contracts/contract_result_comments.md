# contract_result.yml — design rationale and provenance

This file is **not** required to read a completed experiment's result
folder. `contracts/contract_result.yml` is fully self-contained on its own:
every field an agent needs — `entry_point`, `structure`, `tiers`,
`provenance`, `versions`, `key_metrics_by_benchmark_type`, `validity`,
`verdict_shape`, `answer_contract`, `known_gaps` — is encoded as actual parseable YAML data in
that file, not as comments. Nothing in `contract_result.yml` should ever
require reading this document, or any other file, to know what a result
folder contains and how to decode its filenames — the only other files an
agent needs are `contract_catalog.yml` (what you can ask for) and
`dev/catalog/environment.yml` (what cluster capacity exists).

This document exists purely for human maintainers: the *why* behind the
choices baked into the contract, its provenance, and pointers to the wider
design history that produced it.

## Status and provenance

`contracts/contract_result.yml` is an active reference, promoted alongside
`contract_catalog.yml` out of `dev/` to `contracts/` for visibility — it is
not parsed by any code (it documents `report_writer.py`'s own output shape,
it doesn't drive it). It is the third leg of a trio: `contract_catalog.yml`
(what you can ask for), `dev/catalog/environment.yml` (what cluster
capacity exists), and this file (what you'll get back once an experiment
runs). Read it before submitting an experiment (via `tpch.py`/`ycsb.py`/...
directly, or a `contract_catalog.yml` + `experiment.yml` pair resolved by
`bexhoma/spec.py`) to know what the result folder will contain and how to
decode its filenames, without needing a live cluster connection or the
bexhoma source tree.

## See also

- `docs/AgentResultContract.md` — prose version of this file, with worked
  examples and rationale.
- `docs/Design-Catalog-Contract.md` — the input-side catalog contract
  (issue #764) this complements.
- `bexhoma/report_writer.py` — implementation; `SCHEMA_VERSION` source of
  truth.
- `bexhoma/experiments/README.md` — full `show_summary()` call graph,
  per-benchmark-type detail.
- `docs/AgentReport.md` — design rationale for the tiered report.
- `contracts/contract_catalog.yml` — the input-side contract.
- `contracts/contract_result.yml` — the actual contract.
