# Adding a DBMS

A DBMS is added by configuration alone: an entry in the `dockers` section of `cluster.config`, a deployment manifest in `k8s/` and DDL scripts in `experiments/`. No Python file changes.
The [DBMS](DBMS.md) page is the reference for the entry and the deployment template.

To add a DBMS called `NewDBMS`:

1. **Add a configuration entry** in the `dockers` section of `cluster.config` following the [Configuration Reference](DBMS.md#configuration-reference).

2. **Create a deployment manifest** at `k8s/deploymenttemplate-NewDBMS.yml`.  
   Copy `k8s/deploymenttemplate-Dummy.yml` as a starting point and adjust the image, port, and resource defaults.

3. **Add DDL scripts** in a subfolder of `experiments/`, e.g., `experiments/tpch/NewDBMS/` for TPC-H.

4. **Declare the benchmarks** it can run in `benchmarks` of the entry, with `storage_prefix` and `template.alias`, see [Benchmarks of a DBMS](DBMS.md#benchmarks-of-a-dbms).
   No entry script has to be changed: `-dbms` offers every DBMS that has an entry for the benchmark, and the configuration is built from the entry.
   The key of the entry must match the YAML filename of the deployment template (`docker='NewDBMS'`).

If you need a JDBC driver that is not yet included, please raise an issue at https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/issues.

5. **Add an example page** `docs/Example-NewDBMS.md` with a test script `scripts/test-docs-newdbms.sh` and `.ps1`, whose runs are in the order of the page.
   All example pages of a DBMS have the same structure:

   * a short introduction and references (as links), including the test script
   * the main use case (`Perform <Benchmark> Benchmark`): a quick run without monitoring, with subsections Status, Cleanup and Evaluate Results
   * Monitoring: a run of at least one minute of benchmarking with `-m -mc`, and Application Metrics (`-ma`) where the DBMS has an exporter
   * Persistent Storage: a run with `-rst` and `-nc 2`, so the second repetition uses the loaded volume
   * Variants, where the DBMS has them (cluster, replication, components, ...), one subsection with an example result each
   * Technical Details: configuration of bexhoma, deployment, schema and scripts, DDL parameters, load durability and reset scripts
   * one section per further use case (benchmark)

   Logs are named `docs_<benchmark>_<dbms>[_<role>].log`, e.g. `_monitoring`, `_appmetrics`, `_storage`, `_cluster`; [TestCases](TestCases.md) lists all test scripts.
   Add the page to `docs/index.rst` and a short section with a link to [DBMS](DBMS.md).
