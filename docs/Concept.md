# Concepts

An **experiment** is a benchmark of a DBMS in a certain **host setting** and a specific **benchmark setting**.

A **host setting** consists of
* a DBMS (as a docker image)
* a volume (containing some data)
* init scripts (for pre-loading and post-loading)

A **benchmark setting** consists of
* a number of client processes
* a number of runs per connection
* a maximum timeout
* a lot more, depending on the benchmark tool, e.g. [DBMSBenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker)

## Workflow

The **management** roughly means
* start a DBMS and load raw data
* run some benchmarks, fetch metrics and do reporting
* shut down environment and clean up

<p align="center">
    <img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/architecture.png" width="640">
</p>

In more detail this means
1. **Prepare Experiment**  
    1. Use Virtual Machines provided as K8s nodes - create deployment
    1. Attach Network - create service
    1. Attach Data Storage Volume - attach PVC
    1. Start Monitoring - start node exporters and Prometheus as docker containers
1. **Start Experiment**  
    1. Start DBMS Docker Container, upload and run pre-loading init scripts (e.g., create schema), load data, upload and run post-loading init scripts (e.g., create indexes)
1. **Run Benchmarks**  
1. **Report**  
    1. Pull Logs from containers
    1. Pull Metrics from Prometheus monitoring server
1. **Stop Experiment**
1. **Clean Experiment**  
    1. Delete deployment and services


## References

You can find much more details about the concepts in the following articles.
If you use Bexhoma in work contributing to a scientific publication, we kindly ask that you cite our application note [2] or [1]:

[1] [A Framework for Supporting Repetition and Evaluation in the Process of Cloud-Based DBMS Performance Benchmarking](https://doi.org/10.1007/978-3-030-84924-5_6)
> Erdelt P.K. (2021)
> A Framework for Supporting Repetition and Evaluation in the Process of Cloud-Based DBMS Performance Benchmarking.
> In: Nambiar R., Poess M. (eds) Performance Evaluation and Benchmarking. TPCTC 2020.
> Lecture Notes in Computer Science, vol 12752. Springer, Cham.
> https://doi.org/10.1007/978-3-030-84924-5_6

[2] [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://doi.org/10.1007/978-3-030-94437-7_6)
> Erdelt P.K. (2022)
> Orchestrating DBMS Benchmarking in the Cloud with Kubernetes.
> In: Nambiar R., Poess M. (eds) Performance Evaluation and Benchmarking. TPCTC 2021.
> Lecture Notes in Computer Science, vol 13169. Springer, Cham.
> https://doi.org/10.1007/978-3-030-94437-7_6

[3] [DBMS-Benchmarker: Benchmark and Evaluate DBMS in Python](https://doi.org/10.21105/joss.04628)
> Erdelt P.K., Jestel J. (2022).
> DBMS-Benchmarker: Benchmark and Evaluate DBMS in Python.
> Journal of Open Source Software, 7(79), 4628
> https://doi.org/10.21105/joss.04628

[4] [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](http://dx.doi.org/10.13140/RG.2.2.29866.18880)
> Erdelt P.K. (2023)
> http://dx.doi.org/10.13140/RG.2.2.29866.18880
