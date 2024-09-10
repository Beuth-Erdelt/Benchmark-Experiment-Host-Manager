#!/bin/bash


BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR


### YCSB Loader Test for Scaling the Driver (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
    -sf 1 \
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
    run </dev/null &>$LOG_DIR/test_ycsb_testcase_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_1.log


#### Wait so that experiments receive different codes
sleep 1200



#### Delete persistent storage
kubectl delete pvc bexhoma-storage-postgresql-ycsb-1
sleep 10

### YCSB Loader Test for Persistency (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
    -sf 1 \
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
    run </dev/null &>$LOG_DIR/test_ycsb_testcase_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_2.log


#### Wait so that experiments receive different codes
sleep 900



### YCSB Execution for Scaling and Repetition (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
    -sf 1 \
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
    run </dev/null &>$LOG_DIR/test_ycsb_testcase_3.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_3.log


#### Wait so that experiments receive different codes
sleep 900



### YCSB Execution Different Workload (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
    -sf 1 \
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
    run </dev/null &>$LOG_DIR/test_ycsb_testcase_4.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_4.log


#### Wait so that experiments receive different codes
sleep 900



#### YCSB Execution Monitoring (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
    -sf 1 \
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
    run </dev/null &>$LOG_DIR/test_ycsb_testcase_5.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_5.log


#### Wait so that experiments receive different codes
sleep 900



















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
    run </dev/null &>$LOG_DIR/test_benchbase_testcase_1.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_1.log


#### Wait so that experiments receive different codes
sleep 900


#### Delete persistent storage
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
    run </dev/null &>$LOG_DIR/test_benchbase_testcase_2.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_1.log


#### Wait so that experiments receive different codes
sleep 900


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
    run </dev/null &>$LOG_DIR/test_benchbase_testcase_3.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_3.log


#### Wait so that experiments receive different codes
sleep 900


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
    run </dev/null &>$LOG_DIR/test_benchbase_testcase_4.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_4.log


#### Wait so that experiments receive different codes
#sleep 5






#### TPC-H Power Test - only PostgreSQL (TestCases.md)
nohup python tpch.py -ms 1 -tr \
    -sf 1 \
    -dt \
    -t 1200 \
    -dbms PostgreSQL \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -ii -ic -is \
    -nlp 8 \
    -nbp 1 \
    -ne 1 \
    -nc 1 \
    run </dev/null &>$LOG_DIR/test_tpch_testcase_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_1.log


#### Wait so that experiments receive different codes
sleep 600


### TPC-H Monitoring (TestCases.md)
nohup python tpch.py -ms 1 -tr \
    -sf 3 \
    -dt \
    -t 1200 \
    -dbms PostgreSQL \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -ii -ic -is \
    -nlp 8 \
    -nbp 1 \
    -ne 1 \
    -nc 1 \
    -m -mc \
    run </dev/null &>$LOG_DIR/test_tpch_testcase_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_2.log


#### Wait so that experiments receive different codes
sleep 1800

#### Delete persistent storage
kubectl delete pvc bexhoma-storage-postgresql-tpch-1
sleep 10


### TPC-H Throughput Test (TestCases.md)
nohup python tpch.py -ms 1 -tr \
    -sf 1 \
    -dt \
    -t 1200 \
    -dbms PostgreSQL \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -ii -ic -is \
    -nlp 8 \
    -nbp 1 \
    -ne 1,2 \
    -nc 2 \
    -m -mc \
    -rst shared -rss 100Gi \
    run </dev/null &>$LOG_DIR/test_tpch_testcase_3.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_3.log


#### Wait so that experiments receive different codes
sleep 1800






### HammerDB Simple (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
    -sf 16 \
    -dbms PostgreSQL \
    -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
    -tb 131072 \
    -nlt 8 \
    -nbp 1 \
    -nbt 16 \
    -ne 1 \
    -nc 1 \
    run </dev/null &>$LOG_DIR/test_hammerdb_testcase_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_hammerdb_testcase_1.log


#### Wait so that experiments receive different codes
sleep 1200

