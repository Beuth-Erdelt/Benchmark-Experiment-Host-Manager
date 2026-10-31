# Example: Benchmark Cassandra

This differs from the default behaviour of bexhoma, since we benchmark **a distributed NoSQL DBMS, that can be managed by bexhoma** and exists in the Kubernetes cluster in the same namespace.

<img src="https://raw.githubusercontent.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/master/docs/workflow-sketch-simple.png"/>

Apache Cassandra is a wide-column store [1].
There is a single-host and a cluster version.
In the cluster version, there are several pods deployed for the nodes using a stateful set.
Cassandra has no coordinator node, every node answers clients.
Bexhoma still deploys a main pod as a single point of contact, to run `cqlsh` for the scripts and to annotate the status of experiments.
Bexhoma also deploys a service for clients and a headless service for communication between the nodes.
See [dummy manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-Cassandra.yml) for a single-host version that is suitable for bexhoma and see [dummy manifest](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/k8s/deploymenttemplate-CassandraCluster.yml) for a multi-host version that is suitable for bexhoma.

This can be managed by bexhoma.


**The results are not official benchmark results.
Exact performance depends on a number of parameters.
You may get different results.
These examples are solely to illustrate how to use bexhoma and show the result evaluation.**

References:
1. Apache Cassandra: https://cassandra.apache.org/
1. YCSB Repository: https://github.com/brianfrankcooper/YCSB/wiki/Running-a-Workload
1. Benchmarking cloud serving systems with YCSB: https://dl.acm.org/doi/10.1145/1807128.1807152
1. Orchestrating DBMS Benchmarking in the Cloud with Kubernetes: https://doi.org/10.1007/978-3-030-94437-7_6
1. A Cloud-Native Adoption of Classical DBMS Performance Benchmarks and Tools: https://doi.org/10.1007/978-3-031-68031-1_9


## Perform YCSB Benchmark - Ingestion of Data Included

You will have to change the node selectors there (to names of nodes, that exist in your cluster - or to leave out the corresponding parameters):
```bash
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"
BEXHOMA_STORAGE_CLASS="shared"

mkdir -p $LOG_DIR
```

For performing the experiment we can run the [ycsb file](https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager/blob/master/ycsb.py).

Example:
```bash
bexhoma ycsb \
  -dbms Cassandra \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -xop 5 \
  -m \
  -ma \
  -mc \
  -tr \
  -ar \
  -lr 16Gi \
  -rr 16Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_cassandra_1.log
```

This

* starts one Cassandra node
* creates the keyspace `ycsb` and the table `usertable`
* loads 1 million rows with 8 pods and 64 threads in total
* flushes the data and waits for the compactions (`-ar` does this before each benchmarking round as well)
* runs 5 million operations of workload A with 1 pod and 128 threads
* collects hardware metrics (`-m`) and metrics of Cassandra (`-ma`)
* shows a summary and tests the result (`-tr`)


## Cluster

`-nw 3` deploys three nodes in a stateful set. They start one after the other, loading starts when the last one has joined.

`-nwr 3` sets the replication factor of the keyspace (default 1):

```bash
bexhoma ycsb \
  -dbms Cassandra \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -nwr 3 \
  -xop 5 \
  -m \
  -ma \
  -mc \
  -tr \
  -ar \
  -lr 16Gi \
  -rr 16Gi \
  -rss 50Gi \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_cassandra_3.log
```

Reads and writes use consistency level `ONE`, the default of the YCSB binding: a request is answered by one replica, the others are written in the background.


## Persistent Storage

`-rst` puts the data of each node on a volume and `-nc 2` repeats the experiment, so the second repetition runs on the data loaded by the first:

```bash
bexhoma ycsb \
  -dbms Cassandra \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -nwr 3 \
  -xop 5 \
  -m \
  -ma \
  -mc \
  -tr \
  -ar \
  -lr 16Gi \
  -rr 16Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnl $BEXHOMA_NODE_LOAD \
  -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_cassandra_5.log
```

See [Cassandra](DBMS.md#cassandra) for the configuration, the scripts and what has no effect (`-xld`, `-xsbs`).
