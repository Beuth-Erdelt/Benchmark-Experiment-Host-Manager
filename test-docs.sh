#!/bin/bash

mkdir -p ./logs/

BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"




#### YCSB Loader Test for docs
# SF = 1
# PostgreSQL 1 and 8 loader
# [1,2,3,4,5,6,7,8] times 16384 = target
# monitoring all components
# no persistent storage
nohup python ycsb.py -ms 1 -m -mc --workload a -tr \
	-dbms PostgreSQL \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	run &>logs/test_ycsb_docs_1.log &

 watch -n 30 tail -n 50 logs/test_ycsb_docs_1.log


#### Wait so that experiments receive different codes
sleep 5


#### TPC-H Power Test - compare DBMS for docs
# SF = 1
# PostgreSQL 8 loader
# MonetDB 8 loader
# MySQL 8 loader threads
# 1x(1) benchmarker
# monitoring all components
# no persistent storage
nohup python tpch.py -ms 1 -m -mc -dt -sf 1 -ii -ic -is \
	-nlp 8 -nlt 8 \
	-nc 1 -ne 1 \
	-rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
	-t 1200 \
	run &>logs/test_tpch_docs_1.log &

# watch -n 30 tail -n 50 logs/test_tpch_docs_1.log


#### Wait so that experiments receive different codes
sleep 5
