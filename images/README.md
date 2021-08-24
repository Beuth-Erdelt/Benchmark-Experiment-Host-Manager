# Benchmark Experiment Host Manager

In this folder is a collection of useful images.

## Orchestration of Benchmarking Experiments

<p align="center">
    <img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/v0.5.6/docs/experiment-with-orchestrator.png" width="800">
</p>

For full power, use this tool as an orchestrator as in [2]. It also starts a monitoring container using [Prometheus](https://prometheus.io/) and a metrics collector container using [cAdvisor](https://github.com/google/cadvisor). It also uses the Python package [dbmsbenchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) as query executor [2] and evaluator [1].


## References

[1] [A Framework for Supporting Repetition and Evaluation in the Process of Cloud-Based DBMS Performance Benchmarking](https://doi.org/10.1007/978-3-030-84924-5_6)

> Erdelt P.K. (2021)
> A Framework for Supporting Repetition and Evaluation in the Process of Cloud-Based DBMS Performance Benchmarking.
> In: Nambiar R., Poess M. (eds) Performance Evaluation and Benchmarking. TPCTC 2020.
> Lecture Notes in Computer Science, vol 12752. Springer, Cham.
> https://doi.org/10.1007/978-3-030-84924-5_6


[2] [Orchestrating DBMS Benchmarking in the Cloud with Kubernetes](https://www.researchgate.net/publication/353236865_Orchestrating_DBMS_Benchmarking_in_the_Cloud_with_Kubernetes)

