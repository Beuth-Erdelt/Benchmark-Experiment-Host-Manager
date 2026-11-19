## What and why

<!-- What does this change, and why? Link the issue if there is one. -->

## Checklist

- [ ] Branch from `dev`, pull request into `dev`; the title says what changes for users (it becomes the line in the release notes)
- [ ] Tests added or updated; `python -m pytest tests` passes
- [ ] If experiment execution is affected: the relevant test cases ([TestCases](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/docs/TestCases.md)) have been run on a cluster; a representative log is linked
- [ ] If measured or evaluated numbers change (units, aggregation, formulas, rounding, timers) or metrics are renamed: the affected metrics are named above
- [ ] Type of change for the next release (see [Versions and releases](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/docs/CONTRIBUTING.md#versions-and-releases)):
  - [ ] patch (evaluation, reports, docs, fixes)
  - [ ] minor (what an experiment executes or records: contracts, result format, collectors, images, manifests, command line options)
- [ ] Material from others (code, queries, data, tools or drivers in an image) is listed in `THIRD_PARTY.md` and, for an image, in its `NOTICE`
- [ ] I agree that my contribution is licensed under AGPL-3.0-or-later
