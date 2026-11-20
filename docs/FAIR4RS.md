# FAIR4RS Self-Assessment

This page assesses Bexhoma against the [FAIR Principles for Research Software (FAIR4RS)](https://doi.org/10.15497/RDA00068) (Barker et al., *Scientific Data* 9, 622, 2022, [doi:10.1038/s41597-022-01710-x](https://doi.org/10.1038/s41597-022-01710-x)).

Assessed on 2026-11-19 for version 0.11.18.
Each principle is rated **met**, **partly met** or **not met**, with the evidence in the repository or in public services.
Open points are listed at the end.

## Findable

| Principle | Status | Evidence |
|---|---|---|
| F1. Software is assigned a globally unique and persistent identifier. | not met | Bexhoma has no DOI yet. The GitHub repository and the PyPI package `bexhoma` are not persistent identifiers. |
| F1.1. Components of the software representing levels of granularity are assigned distinct identifiers. | partly met | The catalog contract and the result contract (`contracts/`) carry version numbers of their own (`catalog_contract_version`, `result_contract_version`), independent of the Bexhoma version. Neither they nor other components (images, collectors, evaluators) have identifiers of their own. |
| F1.2. Different versions of the software are assigned distinct identifiers. | partly met | Releases are tagged `vX.Y.Z` on [GitHub](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/releases) and published with the same version number on [PyPI](https://pypi.org/project/bexhoma/); there are no version DOIs. |
| F2. Software is described with rich metadata. | met | [`CITATION.cff`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/CITATION.cff), [`codemeta.json`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/codemeta.json) and `pyproject.toml`: description, author with ORCID and affiliation, contributor, licence, keywords, related publications, repository, documentation, issue tracker, runtime requirements. |
| F3. Metadata clearly and explicitly include the identifier of the software they describe. | not met | There is no persistent identifier to include. |
| F4. Metadata are FAIR, searchable and indexable. | partly met | PyPI and GitHub index the package and the repository; the metadata are not registered with a DOI service such as DataCite. |

## Accessible

| Principle | Status | Evidence |
|---|---|---|
| A1. Software is retrievable by its identifier using a standardised communications protocol. | partly met | The source is retrievable over HTTPS from GitHub, the package with `pip install bexhoma`, but not by a persistent identifier. |
| A1.1. The protocol is open, free, and universally implementable. | met | HTTPS. |
| A1.2. The protocol allows for an authentication and authorization procedure, where necessary. | met | Not necessary: software and metadata are public without authentication. |
| A2. Metadata are accessible, even when the software is no longer available. | not met | The metadata exist only on GitHub and PyPI, together with the software. |

## Interoperable

| Principle | Status | Evidence |
|---|---|---|
| I1. Software reads, writes and exchanges data in a way that meets domain-relevant community standards. | partly met | Experiments run on Kubernetes and are described by Kubernetes manifests (`k8s/`); hardware metrics are collected with Prometheus and cAdvisor; DBMS are reached through JDBC and SQL or the drivers of the benchmark tools (HammerDB, Benchbase, YCSB). The catalog contract and the result contract (`contracts/`) are published, versioned YAML specifications ([catalog contract](AgentCatalogContract.md), [result contract](AgentResultContract.md)); reports carry their contract version. However, results of analytical workloads are stored in the result folder of DBMS-Benchmarker, which contains pickled pandas DataFrames, and the configuration files are Python literals. |
| I2. Software includes qualified references to other objects. | met | `CITATION.cff` names the article to cite and the other describing publications by DOI, `codemeta.json` lists them as reference publications; both refer to DBMS-Benchmarker, which Bexhoma requires. |

## Reusable

| Principle | Status | Evidence |
|---|---|---|
| R1. Software is described with a plurality of accurate and relevant attributes. | met | README, [documentation](https://bexhoma.readthedocs.io) of concepts, configuration, monitoring, evaluators and collectors; an example page per benchmark and per DBMS; logs of the documented example runs in `logs_tests/`. |
| R1.1. Software is given a clear and accessible license. | met | AGPL-3.0-or-later in `LICENSE`, stated as SPDX identifier in `pyproject.toml`, `CITATION.cff` and `codemeta.json`; the logo under CC BY 4.0 (`docs/logo/`). Material from others and its licences are listed in [`THIRD_PARTY.md`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/THIRD_PARTY.md); the Docker images carry the licence texts of their components in `/licenses/`. |
| R1.2. Software is associated with detailed provenance. | met | Software: git history, release notes per [release](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/releases), authors and contributors in [`AUTHORS.md`](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/AUTHORS.md) with a written authorship rule in [CONTRIBUTING](CONTRIBUTING.md#authorship). Results: the workload description records the Bexhoma version, agent reports record it with the contract versions, the result folder records the configuration and the versions of DBMS and JDBC driver, and from DBMS-Benchmarker 0.16.0 on also its version per connection. |
| R2. Software includes qualified references to other software. | met | Dependencies with version constraints in `requirements.txt`; the tools, drivers and generators built into the images with their sources and licences in `THIRD_PARTY.md`; the DBMS images in the manifests in `k8s/`. |
| R3. Software meets domain-relevant community standards. | partly met | Packaged with `pyproject.toml` and published on PyPI; a written code style (PEP 8, PEP 257), pull request workflow, versioning policy and release checklist in [CONTRIBUTING](CONTRIBUTING.md); unit tests in CI on every pull request; documented test cases run on a Kubernetes cluster ([TestCases](TestCases.md)), and a core set of ten reference experiments must pass on a cluster before every minor release, which the publish workflow checks before it uploads to PyPI; results derived from TPC workloads are marked as not comparable with official TPC results. However, CI tests one Python version (3.12), and test coverage is not measured. |

## Open points

* **F1, F1.2, F3, A2:** archive releases on Zenodo (concept DOI and version DOIs), with a DOI badge in the README.
* **F1.1:** release the contract specifications and the validator separately, with identifiers of their own.
* **R3:** measure test coverage in CI and test more Python versions.
* **I1:** see the open points of [DBMS-Benchmarker](https://dbmsbenchmarker.readthedocs.io/en/latest/FAIR4RS.html) for the formats of its result folder.
