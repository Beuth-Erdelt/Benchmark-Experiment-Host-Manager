# Contributing to Bexhoma

You would like to contribute? Great!

Some things that you can help on include:
* **New Workloads**: We are interested in adding other relevant workloads, for example more workloads from Benchbase. The `experiments/` folder includes scripts for preparing various databases for various workloads. The `k8s` folder containers YAML manifests for using components. The `images/` folder contains Dockerfiles for implementing tools for components.
* **New DBMS**: We are interested in adding other relevant DBMS. The `experiments/` folder includes scripts for preparing various databases for various workloads. The `k8s` folder containers YAML manifests for using components. This includes DBMS managed by Bexhoma.
* **Documentation**: If a point in the documentation is unclear, we look forward to receiving tips and suggestions for improvement.
* **Testing**: If the behavior is not as expected and you suspect a bug, please report it to our [issue tracker](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/issues).
* **Use Cases**: If you have had any experiences with peculiarities, mistakes, ambiguities or oddities or particularly beautiful cases etc., we are interested in hearing about them and passing them on to others.

## Non-code contributions

Even if you don’t feel ready or able to contribute code, you can still help out. There always things that can be improved on the documentation (even just proof reading, or telling us if a section isn’t clear enough).


## Code contributions

We welcome pull requests to fix bugs or add new features.

### Licensing

In your git commit and/or pull request, please explicitly state that you agree to your contributions being licensed under "GNU Affero General Public License v3".


### Git Usage

If you are planning to make a pull request, start by creating a new branch with a short but descriptive name (rather than using your master branch).


### Coding Conventions

Bexhoma tries to follow the coding conventions laid out in PEP8 and PEP257

- http://www.python.org/dev/peps/pep-0008/
- http://www.python.org/dev/peps/pep-0257/


### Testing

New features or functions will not be accepted without testing.
Likewise for any enhancement or bug fix, we require including an additional test.

The file https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/test.sh includes some demo tests.
For new or important features, we are happy to include a "TEST Passed" or "TEST failed" scenario.