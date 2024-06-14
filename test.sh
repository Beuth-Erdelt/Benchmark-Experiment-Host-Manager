#!/bin/bash

mkdir -p ./logs/

BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"




#### YCSB Loader Test for docs
# SF = 1
# PostgreSQL 1 and 8 loader
# [1,2,3,4,5,6,7,8] times 16384 = target
nohup python ycsb.py -ms 1 -m --workload a -tr \
	-dbms PostgreSQL \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	run &>logs/test_ycsb_1.log &

# watch -n 30 tail -n 50 logs/test_ycsb_1.log


#### Wait so that experiments receive different codes
sleep 5


#### YCSB Loader Test for persistency
# SF = 1
# PostgreSQL 8 loader
# 16384 = target
# run twice
# [1,2] execute
# persistent storage of class shared
nohup python ycsb.py -ms 1 -m --workload a -tr \
	-nlp 8 \
	-dbms PostgreSQL \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-ne 1,2 \
	-nc 2 \
	-ltf 1 \
	-rst shared -rss 100Gi \
	run &>logs/test_ycsb_2.log &

# watch -n 30 tail -n 50 logs/test_ycsb_2.log


#### Wait so that experiments receive different codes
sleep 5


#### YCSB Execution Test
# SF = 1
# PostgreSQL 1 loader
# 2x(1,2) benchmarker
# persistent storage of class shared
nohup python ycsb.py -ms 1 -m --workload a -tr \
	-nlp 1 \
	-dbms PostgreSQL \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-ne 1,2 \
	-nc 2 \
	-ltf 2 \
	-rst shared -rss 100Gi \
	run &>logs/test_ycsb_3.log &

# watch -n 30 tail -n 50 logs/test_ycsb_3.log


#### Wait so that experiments receive different codes
sleep 5


#### TPC-H Power Test
# SF = 1
# PostgreSQL 8 loader
# MonetDB 8 loader
# MySQL 8 loader threads
# 1x(1) benchmarker
# no persistent storage
nohup python tpch.py -ms 1 -m -dt -sf 1 -ii -ic -is \
	-nlp 8 -nlt 8 \
	-nc 1 -ne 1 \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-t 1200 \
	run &>logs/test_tpch_1.log &

# watch -n 30 tail -n 50 logs/test_tpch_1.log


#### Wait so that experiments receive different codes
sleep 5


#### TPC-H Throughput Test
# SF = 1
# PostgreSQL 8 loader
# 2x(1,2) benchmarker
# persistent storage of class shared
nohup python tpch.py -ms 1 -m -dt -sf 1 -ii -ic -is \
	-nlp 8 -nlt 8 \
	-nc 2 -ne 1,2 \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-dbms PostgreSQL -t 1200 \
	-rst shared -rss 100Gi \
	run &>logs/test_tpch_2.log &

# watch -n 30 tail -n 50 logs/test_tpch_2.log

