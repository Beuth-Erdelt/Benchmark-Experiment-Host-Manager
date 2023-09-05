# Experiments for TPCTC 2023

The experiments assume we have set up a K8s cluster named `bexhoma-cluster-1` at AWS of nodegroups of size 0 with this [template](aws.bexhoma.cluster.yml).

The scripts automatically scale the nodegroups to the size needed.
Components of the experiments are attached to the corresponding nodegroup.

The following shows the results presented in [A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools](http://dx.doi.org/10.13140/RG.2.2.29866.18880) and how they are generated.


## Series 1 - YCSB

### Workload A

[Results](Series-1-1-YCSB-Workload-A.ipynb)

```
nohup python experiment-1-ycsb.py \
	-aws \
	-mc \
	-tr \
	-db \
	-m \
	-ms 1 \
	-dbms PostgreSQL \
	-sf 30 \
	-su 32 \
	-cx bexhoma-cluster-1 \
	-workload a \
	-ltf 1,2,3,4,5,6,7,8 \
	-tb 16384 \
	-nc 1 \
	-rc 32 \
	-rr 64Gi \
	run &>logs/experiment.1.a.log &
```

This runs a sequence of 8 benchmark runs, each with a clean copy.
The runs have increasing targets, starting with 1 * tb (=16384) up to 8 * tb (=131072).
The script `experiment-1-ycsb.py` automatically makes two runs of the complete experiment, one with a single process and one with the threads `su` split into 8 processes (=pods).

The parameters are
* `aws`: we have nodegroups and components should be assigned accordingly
* `mc`: run a cAdvisor daemonset on all nodes of the cluster
* `tr`: test result to be correct formally
* `db`: show debug messages
* `m`: monitor components
* `ms`: number of maximum allowed SUT's per cluster
* `dbms`: limit to single DBMS type
* `sf`: scaling factor (1,000,000 rows and operations per SF)
* `su`: scale of virtual users (threads)
* `cx`: K8s context to run the experiment at
* `workload`: YCSB workload (a-e)
* `ltf`: YCSB list of target factors
* `tb`: YCSB target base
* `nc`: number of runs per configuration
* `rc`: request vCPU per SUT
* `rr`: request RAM (Gb) per SUT


### Workload C

[Results](Series-1-2-YCSB-Workload-C.ipynb)

```
nohup python experiment-1-ycsb.py \
	-aws \
	-mc \
	-tr \
	-db \
	-m \
	-ms 1 \
	-dbms PostgreSQL \
	-sf 30 \
	-su 32 \
	-cx bexhoma-cluster-1 \
	-workload c \
	-ltf 4,5,6,7,8,9,10,11,12 \
	-tb 16384 \
	-nc 1 \
	-rc 32 \
	-rr 64Gi \
	run &>logs/experiment.1.c.log &
```

This runs almost the same experiment.
It is workload C this time.
Since it is a read-only workload, the throughput is higher.
The runs have increasing targets, now starting with 4 * tb (=65536) up to 12 * tb (=196608).

## Series 2 - TPC-C HammerDB

### Loading

[Results](Series-2-1-HammerDB-Loading.ipynb)

```
nohup python experiment-2-hammerdb.py \
	-aws \
	-mc \
	-tr \
	-db \
	-m \
	-ms 1 \
	-dbms PostgreSQL \
	-sf 320 \
	-su 1,2,4,8,10,16,20,32,40,80,160,320 \
	-nvu '1' \
	-sd 2 \
	-cx bexhoma-cluster-1 \
	-nc 1 \
	-rc 32 \
	-rr 64Gi \
	run &>logs/experiment.2.1.log &
```

This runs a sequence of 12 runs, each with a clean copy.
The runs have increasing vusers (i.e., driver threads), from 1 to 320 (the number of warehouses), for the loading phase.
Each run also runs the benchmark phase with 1 thread for 2 minutes.

The parameters are
* `aws`: we have nodegroups and components should be assigned accordingly
* `mc`: run a cAdvisor daemonset on all nodes of the cluster
* `tr`: test result to be correct formally
* `db`: show debug messages
* `m`: monitor components
* `ms`: number of maximum allowed SUT's per cluster
* `dbms`: limit to single DBMS type
* `sf`: scaling factor (number of warehouses)
* `su`: scale of virtual users (threads) for loading
* `nvu`: List of virtual users to run the workload one after the other
* `sd`: Duration of benchmarking in minutes
* `cx`: K8s context to run the experiment at
* `nc`: number of runs per configuration
* `rc`: request vCPU per SUT
* `rr`: request RAM (Gb) per SUT

### Execution

[Results](Series-2-2-HammerDB-Execution.ipynb)

```
nohup python experiment-2-hammerdb.py \
	-aws \
	-mc \
	-tr \
	-db \
	-m \
	-ms 1 \
	-dbms PostgreSQL \
	-nrt 5 \
	-sf 320 \
	-su 8 \
	-nvu '2 4 6 8 10 12 16 20' \
	-sd 15 \
	-cx bexhoma-cluster-1 \
	-nc 1 \
	-nbp 1,2 \
	-rc 32 \
	-rr 64Gi \
	run &>logs/experiment.2.2.log &
```
This runs a sequence of 8 benchmark runs, each with a clean copy, and with 8 threads for the loading phase.
The runs have increasing vusers (i.e., driver threads), from 2 to 20, for the execution phase for 15 minutes.
The script `experiment-1-hammerdb.py` automatically makes two runs of the complete experiment, splitting the threads into `nbp` processes (=pods).

The parameters are
* `aws`: we have nodegroups and components should be assigned accordingly
* `mc`: run a cAdvisor daemonset on all nodes of the cluster
* `tr`: test result to be correct formally
* `db`: show debug messages
* `m`: monitor components
* `ms`: number of maximum allowed SUT's per cluster
* `dbms`: limit to single DBMS type
* `nrt`: Rampup time in minutes
* `sf`: scaling factor (number of warehouses)
* `su`: scale of virtual users (threads) for loading
* `nvu`: List of virtual users to run the workload one after the other
* `sd`: Duration of benchmarking in minutes
* `cx`: K8s context to run the experiment at
* `nc`: number of runs per configuration
* `rc`: request vCPU per SUT
* `rr`: request RAM (Gb) per SUT

## Series 3 - TPC-C Benchbase Execution

[Results](Series-3-Benchbase.ipynb)

```
nohup python experiment-3-benchbase.py \
	-aws \
	-mc \
	-tr \
	-db \
	-m \
	-ms 1 \
	-dbms PostgreSQL \
	-sf 48 \
	-su 36 \
	-cx bexhoma-cluster-1 \
	-nti 900 \
	-ltf 16 \
	-tb 1024 \
	-nvu 32,64,96,128,160,192,224,256 \
	-nbp 1,2,4,8 \
	-nc 1 \
	-rc 32 \
	-rr 64Gi \
	run &>logs/experiment.3.log &
```

This runs a sequence of 4 benchmark runs, each with a clean copy.
The runs have target `ltf` * `tb` (=16384).
The runs also have an increasing number of threads given by `nvu`.
Node names are set for loading and benchmarking components and for the SUT.
This must be adjusted to names of nodes in the cluster.
The script `experiment-3benchbase.py` makes four runs of the complete experiment, splitting the threads into `nbp` processes (=pods).

The parameters are
* `aws`: we have nodegroups and components should be assigned accordingly
* `mc`: run a cAdvisor daemonset on all nodes of the cluster
* `tr`: test result to be correct formally
* `db`: show debug messages
* `m`: monitor components
* `ms`: number of maximum allowed SUT's per cluster
* `dbms`: limit to single DBMS type
* `sf`: scaling factor (number of warehouses)
* `su`: scale of virtual users (threads) for loading - ignored by Benchbase
* `cx`: K8s context to run the experiment at
* `nti`: TPC-C duration of execution in seconds
* `ltf`: TPC-C list of target factors
* `tb`: TPC-C target base
* `nvu`: TPC-C list of number of driver threads
* `nbp`: TPC-C list of number of driver pods
* `nc`: number of runs per configuration
* `rc`: request vCPU per SUT
* `rr`: request RAM (Gb) per SUT


## Series 4 - TPC-H

### Generating

[Results](Series-4-1-TPC-H-Datageneration.ipynb)

```
nohup python experiment-2-1-tpch-generating-filesystem.py \
	-aws \
	-mc \
	-tr \
	-db \
	-m \
	-ms 1 \
	-t 3600 \
	-sf 100 \
	-dt \
	-nlp 24,16,8,4,2,1 \
	-nr 1 \
	-nc 1 \
	-ne 1 \
	-cx bexhoma-cluster-1 \
	-rc 2 \
	-rr 8Gi \
	-syl 1 \
	run &>logs/experiment.4.1.log &
```

This runs a sequence of 6 runs, each with a clean copy.
Each run generates the TPC-H data.
The runs have an increasing number of pods given by `nlp`.
Each pod only generates a portion of the data.

The parameters are
* `aws`: we have nodegroups and components should be assigned accordingly
* `mc`: run a cAdvisor daemonset on all nodes of the cluster
* `tr`: test result to be correct formally
* `db`: show debug messages
* `m`: monitor components
* `ms`: number of maximum allowed SUT's per cluster
* `t`: timeout for query execution
* `sf`: TPC-H scaling factor (= GB of database)
* `dt`: data transfer during benchmarking (also fetch results, not only send query)
* `nlp`: list of numbers of loading (here: generating) pods
* `nr`: number of runs per benchmark query
* `ne`: number of runs per driver
* `nc`: number of runs per configuration
* `cx`: K8s context to run the experiment at
* `rc`: request vCPU per SUT
* `rr`: request RAM (Gb) per SUT
* `syl`: synchronize loading (here: generating) pods

### Loading

[Results](Series-4-2-TPC-H-Loading.ipynb)

```
nohup python experiment-2-3-tpch-loading-filesystem.py \
	-aws \
	-mc \
	-tr \
	-db \
	-m \
	-ms 1 \
	-dbms PostgreSQL \
	-t 3600 \
	-sf 100 \
	-mls 32 \
	-dt \
	-nlp 24,16,8,4,2,1 \
	-nr 1 \
	-nc 1 \
	-ne 1 \
	-cx bexhoma-cluster-1 \
	-rc 32 \
	-rr 64Gi \
	-syl 1 \
	empty &>logs/experiment.4.2.log &
```

This runs a sequence of 6 runs, each with a clean copy.
Each run loads the TPC-H data.
The runs have an increasing number of pods given by `nlp`.
Each pod only loads a portion of the data.

The parameters are
* `aws`: we have nodegroups and components should be assigned accordingly
* `mc`: run a cAdvisor daemonset on all nodes of the cluster
* `tr`: test result to be correct formally
* `db`: show debug messages
* `m`: monitor components
* `ms`: number of maximum allowed SUT's per cluster
* `dbms`: limit to single DBMS type
* `t`: timeout for query execution
* `sf`: TPC-H scaling factor (= GB of database)
* `mls`: maximum size of loader in RAM [Gb]
* `dt`: data transfer during benchmarking (also fetch results, not only send query)
* `nlp`: list of numbers of loading pods
* `nr`: number of runs per benchmark query
* `ne`: number of runs per driver
* `nc`: number of runs per configuration
* `cx`: K8s context to run the experiment at
* `rc`: request vCPU per SUT
* `rr`: request RAM (Gb) per SUT
* `syl`: synchronize loading pods


### Execution Throughput Test

[Results](Series-4-3-TPC-H-Throughput.ipynb)

```
nohup python experiment-2-4-tpch-benchmarking.py \
	-aws \
	-mc \
	-tr \
	-db \
	-m \
	-ms 1 \
	-dbms PostgreSQL \
	-t 3600 \
	-sf 30 \
	-dt \
	-nlp 4 \
	-nr 1 \
	-ne 1,2,3,4,5,6,7,8,9,10 \
	-nc 1 \
	-cx bexhoma-cluster-1 \
	-rc 32 \
	-rr 512Gi \
	-ii \
	-ic \
	-is \
	run &>logs/experiment.4.3.log &
```

This runs a sequence of 10 runs, each with a clean copy.
Each run loads the TPC-H data.
The runs have an increasing number of pods given by `ne` for the execution phase (throughput test).

The parameters are
* `aws`: we have nodegroups and components should be assigned accordingly
* `mc`: run a cAdvisor daemonset on all nodes of the cluster
* `tr`: test result to be correct formally
* `db`: show debug messages
* `m`: monitor components
* `ms`: number of maximum allowed SUT's per cluster
* `dbms`: limit to single DBMS type
* `t`: timeout for query execution
* `sf`: TPC-H scaling factor (= GB of database)
* `dt`: data transfer during benchmarking (also fetch results, not only send query)
* `nlp`: list of numbers of loading pods
* `nr`: number of runs per benchmark query
* `ne`: number of runs per driver
* `nc`: number of runs per configuration
* `cx`: K8s context to run the experiment at
* `rc`: request vCPU per SUT
* `rr`: request RAM (Gb) per SUT
* `ii`: init indexes (CREATE INDEX)
* `ic`: init constraints (ADD PRIMARY, ADD FOREIGN)
* `is`: init statistics (ANALYZE)


