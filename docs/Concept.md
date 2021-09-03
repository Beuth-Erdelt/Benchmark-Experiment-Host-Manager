# Concepts

An **experiment** is a benchmark of a DBMS in a certain **host setting** and a specific **benchmark setting**.

A **host setting** consists of
* an instance (a virtual machine)
* a DBMS (as a docker image)
* a volume (containing some data)
* an init script (telling the dbms how to store the data)

A **benchmark setting** consists of
* a number of client processes
* a number of runs per connection
* a maximum timeout
* a lot more, depending on the [benchmark tool](https://github.com/Beuth-Erdelt/DBMS-Benchmarker)

## Workflow

The **management** roughly means
* [configure](Config.html#how-to-configure-an-experiment-setup), [set up](Config.html#example-setup-different-dbms-on-same-instance) and [start](API.html#prepare-experiment) a virtual machine environment
* [start](API.html#start-experiment) a DBMS and load raw data
* [run](API.html#run-benchmarks) some benchmarks, fetch metrics and do reporting
* [shut](API.html#stop-experiment) down environment and [clean up](API.html#clean-experiment)

<p align="center">
    <img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/architecture.png" width="640">
</p>

In more detail this means
1. **Prepare Experiment**  
    1. **Start Virtual Machine**  
    AWS: Start Instance EC2  
    k8s: Create Deployment
    1. **Attach Network**  
    AWS: Attach EIP  
    k8s: Create Service, Port Forwarding  
    1. **Attach Data Storage Volume**  
    AWS: Attach and Mount EBS  
    k8s: Attach PVC  
    1. **Start Monitoring**  
    Start Prometheus Exporter Docker Container  
1. **Start Experiment**  
    1. Start DBMS Docker Container  
    Upload and run Init Scripts  
    Load Data from Data Storage Volume
1. **Run Benchmarks**  
1. **Report**  
    1. **Pull Logs**  
    From DBMS Container
    1. **Pull Metrics**  
    From Grafana Monitoring Server
1. **Stop Experiment**  
AWS: Stop DBMS Docker Container, Remove Docker Remnants
1. **Clean Experiment**  
AWS: Unmount and Detach EBS Volume, Detach EIP, Stop Instance EC2  
k8s: Stop Port Forwarding, Delete Deployment and Services

## Prerequisits

This tool relies on
* [dbms benchmarker](https://github.com/Beuth-Erdelt/DBMS-Benchmarker) for the actual benchmarks
* a [configuration file](#clusterconfig)
* [boto](http://boto.cloudhackers.com/en/latest/) for AWS management
* [paramiko](http://www.paramiko.org/) for SSH handling
* [scp](https://pypi.org/project/scp/) for SCP handling
* [kubernetes](https://github.com/kubernetes-client/python) for k8s management
* and some more [python libraries](https://github.com/perdelt/kubecluster/blob/master/requirements.txt)
