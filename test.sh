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
sleep 600



kubectl delete pvc bexhoma-storage-postgresql-ycsb-1
sleep 10

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
sleep 600



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
sleep 900



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
sleep 600



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
sleep 600








#### Benchbase Simple
nohup python benchbase.py -ms 1 -tr \
    -sf 16 \
    -sd 5 \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -dbms PostgreSQL \
    -tb 1024 \
    -nbp 1 \
    -nbt 16 \
    -nbf 8 \
    -ne 1 \
    -nc 1 \
    run </dev/null &>logs/test_benchbase_testcase_1.log &

# watch -n 30 tail -n 50 logs/test_benchbase_testcase_1.log


#### Wait so that experiments receive different codes
sleep 600


kubectl delete pvc bexhoma-storage-postgresql-benchbase-16
sleep 10

#### Benchbase Persistency
nohup python benchbase.py -ms 1 -tr \
    -sf 16 \
    -sd 1 \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -dbms PostgreSQL \
    -tb 1024 \
    -nbp 1 \
    -nbt 16 \
    -nbf 8 \
    -ne 1 \
    -nc 2 \
	-rst shared -rss 50Gi \
    run </dev/null &>logs/test_benchbase_testcase_2.log &

# watch -n 30 tail -n 50 logs/test_benchbase_testcase_1.log


#### Wait so that experiments receive different codes
sleep 600


#### Benchbase Monitoring
nohup python benchbase.py -ms 1 -tr \
    -sf 16 \
    -sd 5 \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -dbms PostgreSQL \
    -tb 1024 \
    -nbp 1 \
    -nbt 16 \
    -nbf 8 \
    -ne 1 \
    -nc 1 \
    -m -mc \
    run </dev/null &>logs/test_benchbase_testcase_3.log &

# watch -n 30 tail -n 50 logs/test_benchbase_testcase_3.log


#### Wait so that experiments receive different codes
sleep 600


#### Benchbase Complex
nohup python benchbase.py -ms 1 -tr \
    -sf 16 \
    -sd 2 \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -dbms PostgreSQL \
    -tb 1024 \
    -nbp 1,2 \
    -nbt 8 \
    -nbf 8 \
    -ne 1,2 \
    -nc 2 \
    -m -mc \
	-rst shared -rss 50Gi \
    run </dev/null &>logs/test_benchbase_testcase_4.log &

# watch -n 30 tail -n 50 logs/test_benchbase_testcase_4.log


#### Wait so that experiments receive different codes
#sleep 5
