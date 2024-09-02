#!/bin/bash

mkdir -p ./logs/

BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"

### YCSB Loader Test for Scaling the Driver (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
    --workload a \
    -dbms PostgreSQL \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -tb 131072 \
    -nlp 4,8 \
    -nlt 32,64 \
    -nlf 1 \
    -nbp 1 \
    -nbt 64 \
    -nbf 1 \
    -ne 1 \
    -nc 1 \
	run </dev/null &>logs/test_ycsb_testcase_1.log &

#watch -n 30 tail -n 50 logs/test_ycsb_testcase_1.log


#### Wait so that experiments receive different codes
sleep 5



### YCSB Loader Test for Persistency (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
    --workload a \
    -dbms PostgreSQL \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -tb 131072 \
    -nlp 8 \
    -nlt 64 \
    -nlf 1 \
    -nbp 1 \
    -nbt 64 \
    -nbf 1 \
    -ne 1 \
    -nc 2 \
    -rst shared -rss 100Gi \
    run </dev/null &>logs/test_ycsb_testcase_2.log &

#watch -n 30 tail -n 50 logs/test_ycsb_testcase_2.log


#### Wait so that experiments receive different codes
sleep 5



### YCSB Execution for Scaling and Repetition (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
    --workload a \
    -dbms PostgreSQL \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -tb 131072 \
    -nlp 8 \
    -nlt 64 \
    -nlf 1 \
    -nbp 1,8 \
    -nbt 64 \
    -nbf 1 \
    -ne 1,2 \
    -nc 2 \
    -rst shared -rss 100Gi \
    run </dev/null &>logs/test_ycsb_testcase_3.log &

# watch -n 30 tail -n 50 logs/test_ycsb_testcase_3.log


#### Wait so that experiments receive different codes
sleep 5



### YCSB Execution Different Workload (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
    --workload e \
    -dbms PostgreSQL \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -tb 131072 \
    -nlp 8 \
    -nlt 64 \
    -nlf 1 \
    -nbp 8 \
    -nbt 64 \
    -nbf 1 \
    -ne 1 \
    -nc 1 \
    -rst shared -rss 100Gi \
    run </dev/null &>logs/test_ycsb_testcase_4.log &

# watch -n 30 tail -n 50 logs/test_ycsb_testcase_4.log


#### Wait so that experiments receive different codes
sleep 5



#### YCSB Execution Monitoring (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
    --workload a \
    -dbms PostgreSQL \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -tb 131072 \
    -nlp 8 \
    -nlt 64 \
    -nlf 1 \
    -nbp 1,8 \
    -nbt 64 \
    -nbf 1 \
    -ne 1 \
    -nc 1 \
    -rst shared -rss 100Gi \
    -m -mc \
    -sf 10 \
    run </dev/null &>logs/test_ycsb_testcase_5.log &

# watch -n 30 tail -n 50 logs/test_ycsb_testcase_5.log


#### Wait so that experiments receive different codes
sleep 5






#### TPC-H Power Test - only PostgreSQL (TestCases.md)
# SF = 1
# PostgreSQL 8 loader, indexed
# 1x(1) benchmarker = 1 execution stream (power test)
# no persistent storage
# no monitoring
nohup python tpch.py -ms 1 -dt -sf 1 -ii -ic -is \
	-nlp 8 -nlt 8 \
	-nc 1 -ne 1 \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-t 1200 \
	-dbms PostgreSQL \
	run &>logs/test_tpch_testcase_1.log &

# watch -n 30 tail -n 50 logs/test_tpch_testcase_1.log


#### Wait so that experiments receive different codes
sleep 5


#### TPC-H Monitoring Test (TestCases.md)
# SF = 3
# PostgreSQL 8 loader, indexed
# 1x(1) benchmarker = 1 execution stream (power test)
# persistent storage of class shared
# monitoring all components
nohup python tpch.py -ms 1 -dt -sf 3 -ii -ic -is \
	-nlp 8 -nlt 8 \
	-nc 1 -ne 1 \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-t 1200 \
	-dbms PostgreSQL \
	-m -mc \
	-rst shared -rss 100Gi \
	run &>logs/test_tpch_testcase_2.log &

# watch -n 30 tail -n 50 logs/test_tpch_testcase_2.log


#### Wait so that experiments receive different codes
sleep 5


#### TPC-H Throughput Test
# SF = 1
# PostgreSQL 8 loader, indexed
# 2x(1,2) benchmarker = 1 and 2 execution streams (run twice)
# persistent storage of class shared
# monitoring all components
nohup python tpch.py -ms 1 -dt -sf 1 -ii -ic -is \
	-nlp 8 -nlt 8 \
	-nc 2 -ne 1,2 \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-t 1200 \
	-dbms PostgreSQL \
	-m -mc \
	-rst shared -rss 100Gi \
	run &>logs/test_tpch_testcase_3.log &

# watch -n 30 tail -n 50 logs/test_tpch_testcase_3.log


#### Wait so that experiments receive different codes
sleep 5






#### Benchbase Simple
# 16 warehouses
# 16 terminals in 1 pod at execution
# target is 16384 ops
# no persistent storage
nohup python benchbase.py -ms 1 -tr \
	-sf 16 \
	-ltf 16 \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-dbms PostgreSQL \
	-nvu 16 \
	-nbp 1 \
	run &>logs/test_benchbase_testcase_1.log &

# watch -n 30 tail -n 50 logs/test_benchbase_testcase_1.log


#### Wait so that experiments receive different codes
sleep 5


#### Benchbase Monitoring
# 16 warehouses
# 16 terminals in 1 pod
# target is 16384 ops
# monitoring of all components activated
# data is stored persistently in a PV of type shared and size 50Gi
nohup python benchbase.py -ms 1 -tr \
	-sf 16 \
	-ltf 16 \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-dbms PostgreSQL \
	-nvu 16 \
	-nbp 1 \
	-m -mc \
	-rst shared -rss 50Gi \
	run &>logs/test_benchbase_testcase_2.log &

# watch -n 30 tail -n 50 logs/test_benchbase_testcase_2.log


#### Wait so that experiments receive different codes
sleep 5


#### Benchbase Complex
# 16 warehouses
# 16 terminals in 1 pod and 16 terminals in 2 pods (8 each)
# target is 16384 ops
# data is stored persistently in a PV of type shared and size 50Gi
# monitoring of all components activated
# run twice
nohup python benchbase.py -ms 1 -tr \
	-sf 16 \
	-ltf 16 \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-dbms PostgreSQL \
	-nvu 16 \
	-nbp 1,2 \
	-m -mc \
	-rst shared -rss 50Gi \
	-nc 2 \
	run &>logs/test_benchbase_testcase_3.log &

# watch -n 30 tail -n 50 logs/test_benchbase_testcase_3.log


#### Wait so that experiments receive different codes
sleep 5




#### HammerDB Simple
# 16 warehouses
# 16 threads used for loading
# 8 terminals in 1 pod
# no persistent storage
nohup python hammerdb.py \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-dbms PostgreSQL \
	-nvu '8' \
	-su 16 \
	-sf 16 \
	-nbp 1 \
	run &>logs/test_hammerdb_testcase_1.log &

# watch -n 30 tail -n 50 logs/test_hammerdb_testcase_1.log


#### Wait so that experiments receive different codes
sleep 5


#### HammerDB Monitoring
# 16 warehouses
# 16 threads used for loading
# 8 terminals in 1 pod
# data is stored persistently in a PV of type shared and size 30Gi
# monitoring of all components activated
nohup python hammerdb.py \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-dbms PostgreSQL \
	-nvu '8' \
	-su 16 \
	-sf 16 \
	-nbp 1 \
	-m -mc \
	-rst shared -rss 30Gi \
	run &>logs/test_hammerdb_testcase_2.log &

# watch -n 30 tail -n 50 logs/test_hammerdb_testcase_2.log


#### Wait so that experiments receive different codes
sleep 5


#### HammerDB Complex
# 16 warehouses
# 16 threads used for loading
# 8 terminals in 1 pod and in 2 pods (4 terminals each)
# data is stored persistently in a PV of type shared and size 30Gi
# monitoring of all components activated
nohup python hammerdb.py \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-dbms PostgreSQL \
	-nvu '8' \
	-su 16 \
	-sf 16 \
	-nbp 1,2 \
	-m -mc \
	-rst shared -rss 30Gi \
	run &>logs/test_hammerdb_testcase_3.log &

# watch -n 30 tail -n 50 logs/test_hammerdb_testcase_3.log
