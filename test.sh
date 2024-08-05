#!/bin/bash

mkdir -p ./logs/

BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"


#### YCSB Loader Test for Persistency (TestCases.md)
# SF = 1 (1 million rows and operations)
# PostgreSQL
# Workload A
# 64 loader threads, split into 8 parallel pods
# persistent storage of class shared
# 64 execution threads, split into 8 parallel pods
# [1,2] execute (64 threads in 8 pods and 128 threads in 16 pods)
# target is 16384 ops
# run twice
nohup python ycsb.py -ms 1 -tr \
	--workload a \
	-nlp 8 \
	-dbms PostgreSQL \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-ne 1,2 \
	-nc 2 \
	-ltf 1 \
	-rst shared -rss 100Gi \
	run &>logs/test_ycsb_testcase_1.log &

#watch -n 30 tail -n 50 logs/test_ycsb_testcase_1.log


#### Wait so that experiments receive different codes
sleep 5


#### YCSB Execution Test
# SF = 1
# PostgreSQL 1 loader
# 2x(1,2) benchmarker
# persistent storage of class shared
#nohup python ycsb.py -ms 1 -m --workload a -tr \
#	-nlp 1 \
#	-dbms PostgreSQL \
#	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
#	-ne 1,2 \
#	-nc 2 \
#	-ltf 2 \
#	-rst shared -rss 100Gi \
#	run &>logs/test_ycsb_testcase_2.log &

# watch -n 30 tail -n 50 logs/test_ycsb_testcase_2.log


#### Wait so that experiments receive different codes
#sleep 5


#### YCSB Execution Test (TestCases.md)
# python ycsb.py -ltf 1 -nlp 8 -su 64 -sf 1 -dbms PostgreSQL -wl a run
# SF = 1 (1 million rows and operations)
# workload A
# 64 loader threads, split into 8 parallel pods
# 64 execution threads, split into 8 parallel pods
# target is 16384 ops
nohup python ycsb.py -ms 1 --workload a -tr \
	-nlp 8 -su 64 \
	-dbms PostgreSQL \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-ne 1 \
	-nc 1 \
	-ltf 1 \
	run &>logs/test_ycsb_testcase_3.log &

# watch -n 30 tail -n 50 logs/test_ycsb_testcase_3.log


#### Wait so that experiments receive different codes
sleep 5


#### YCSB Execution Monitoring (TestCases.md)
# python ycsb.py -ltf 1 -nlp 8 -su 64 -sf 1 -dbms PostgreSQL -wl a -m -mc run
# SF = 1 (1 million rows and operations)
# workload A
# 64 loader threads, split into 8 parallel pods
# 64 execution threads, split into 8 parallel pods
# target is 16384 ops
# monitoring of all components activated
nohup python ycsb.py -ms 1 --workload a -tr \
	-nlp 8 -su 64 \
	-dbms PostgreSQL \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-ne 1 \
	-nc 1 \
	-ltf 1 \
	-m -mc \
	run &>logs/test_ycsb_testcase_4.log &

# watch -n 30 tail -n 50 logs/test_ycsb_testcase_4.log


#### Wait so that experiments receive different codes
sleep 5


#### YCSB Execution Complex (TestCases.md)
# python ycsb.py -ltf 1 -nlp 8 -su 64 -sf 1 -dbms PostgreSQL -wl a -rst shared -rss 30Gi -m -mc -ne 1,2 -nc 2 run
# SF = 1 (1 million rows and operations)
# workload A
# 64 loader threads, split into 8 parallel pods
# 64 execution threads, split into 8 parallel pods
# target is 16384 ops
# data is stored persistently in a PV of type shared and size 30Gi
# 2x(1,2) benchmarker
# monitoring of all components activated
#nohup python ycsb.py -ms 1 --workload a -tr \
#	-nlp 8 -su 64 \
#	-dbms PostgreSQL \
#	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
#	-ne 1,2 \
#	-nc 2 \
#	-ltf 1 \
#	-m -mc \
#	-rst shared -rss 30Gi \
#	run &>logs/test_ycsb_testcase_5.log &

# watch -n 30 tail -n 50 logs/test_ycsb_testcase_5.log


#### Wait so that experiments receive different codes
#sleep 5





#### TPC-H Power Test - only PostgreSQL (TestCases.md)
# python tpch.py -dt -nlp 8 -nlt 8 -sf 1 -ii -ic -is -dbms PostgreSQL run
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
# python tpch.py -dt -nlp 8 -nlt 8 -sf 1 -ii -ic -is -dbms PostgreSQL -m -mc run
# SF = 1
# PostgreSQL 8 loader, indexed
# 1x(1) benchmarker = 1 execution stream (power test)
# no persistent storage
# monitoring all components
nohup python tpch.py -ms 1 -dt -sf 1 -ii -ic -is \
	-nlp 8 -nlt 8 \
	-nc 1 -ne 1 \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-t 1200 \
	-dbms PostgreSQL \
	-m -mc \
	run &>logs/test_tpch_testcase_2.log &

# watch -n 30 tail -n 50 logs/test_tpch_testcase_2.log


#### Wait so that experiments receive different codes
sleep 5


#### TPC-H Throughput Test
# python tpch.py -dt -nlp 8 -nlt 8 -sf 1 -ii -ic -is -dbms PostgreSQL -m -mc -rst shared -rss 100Gi run
# SF = 1
# PostgreSQL 8 loader, indexed
# 2x(1,2) benchmarker = 1 and 2 execution streams
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
# python benchbase.py -ltf 16 -dbms PostgreSQL -nvu 16 -sf 16 -nbp 1 run
# 16 warehouses
# 16 terminals in 1 pod
# target is 16384 ops
# no persistent storage
nohup python benchbase.py \
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
# python benchbase.py -ltf 16 -dbms PostgreSQL -nvu 16 -sf 16 -nbp 1 -m -mc run
# 16 warehouses
# 16 terminals in 1 pod
# target is 16384 ops
# monitoring of all components activated
# no persistent storage
nohup python benchbase.py \
	-sf 16 \
	-ltf 16 \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-dbms PostgreSQL \
	-nvu 16 \
	-nbp 1 \
	-m -mc \
	run &>logs/test_benchbase_testcase_2.log &

# watch -n 30 tail -n 50 logs/test_benchbase_testcase_2.log


#### Wait so that experiments receive different codes
sleep 5


#### Benchbase Complex
# python benchbase.py -ltf 16 -dbms PostgreSQL -nvu 16 -sf 16 -nbp 1,2 -rst shared -rss 30Gi -m -mc run
# 16 warehouses
# 16 terminals in 1 pod and 16 terminals in 2 pods (8 each)
# target is 16384 ops
# data is stored persistently in a PV of type shared and size 30Gi
# monitoring of all components activated
# run twice
nohup python benchbase.py \
	-sf 16 \
	-ltf 16 \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-dbms PostgreSQL \
	-nvu 16 \
	-nbp 1,2 \
	-m -mc \
	-rst shared -rss 30Gi \
	-nc 2 \
	run &>logs/test_benchbase_testcase_3.log &

# watch -n 30 tail -n 50 logs/test_benchbase_testcase_3.log


#### Wait so that experiments receive different codes
sleep 5




#### HammerDB Simple
# python hammerdb.py -tr -dbms PostgreSQL -nvu '8' -su 16 -sf 16 -nbp 1 run
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
# python hammerdb.py -tr -dbms PostgreSQL -nvu '8' -su 16 -sf 16 -nbp 1 -m -mc run
# 16 warehouses
# 16 threads used for loading
# 8 terminals in 1 pod
# monitoring of all components activated
# no persistent storage
nohup python hammerdb.py \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-dbms PostgreSQL \
	-nvu '8' \
	-su 16 \
	-sf 16 \
	-nbp 1 \
	-m -mc \
	run &>logs/test_hammerdb_testcase_2.log &

# watch -n 30 tail -n 50 logs/test_hammerdb_testcase_2.log


#### Wait so that experiments receive different codes
sleep 5


#### HammerDB Complex
# python hammerdb.py -tr -dbms PostgreSQL -nvu '8' -su 16 -sf 16 -nbp 1,2 -rst shared -rss 30Gi -m -mc run
# 16 warehouses
# 16 threads used for loading
# 8 terminals in 1 pod and in 2 pods (4 each)
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
	run &>logs/test_hammerdb_testcase_3.log &

# watch -n 30 tail -n 50 logs/test_hammerdb_testcase_3.log
