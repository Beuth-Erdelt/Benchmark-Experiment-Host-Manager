#!/bin/bash

 
BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"

nohup python ycsb.py -ms 1 -m -dbms PostgreSQL -workload a -tr -rnn BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb BEXHOMA_NODE_BENCHMARK -ne 1,2 -nlp 8 -ltf 4 run &>logs/test_ycsb_1.log &

nohup python ycsb.py -ms 1 -m -dbms PostgreSQL -workload a -tr -rnn BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb BEXHOMA_NODE_BENCHMARK -ne 1,2 -nlp 1 -ltf 4,5 -nc 2 -rst local-hdd -rss 50Gi run &>logs/test_ycsb_2.log &

nohup python tpch.py -ms 1 -m -dt -nlp 8 -nc 2 -nlt 8 -sf 1 -ii -ic -is -ne 1,2 -rnn BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb BEXHOMA_NODE_BENCHMARK -dbms PostgreSQL -t 1200 -rst shared -rss 50Gi run &>logs/test_tpch_1.log &

nohup python tpch.py -ms 1 -m -dt -nlp 8 -nc 1 -nlt 8 -sf 1 -ii -ic -is -ne 1 -rnn BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb BEXHOMA_NODE_BENCHMARK -t 1200 run &>logs/test_tpch_2.log &

