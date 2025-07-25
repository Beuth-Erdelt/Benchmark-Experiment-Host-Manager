#!/bin/bash
######################################################################################
# Bash Script for Bexhoma Test Runs - More Tests to cover more cases like more DBMS 
######################################################################################
#
# This scripts starts a sequence of experiments with varying parameters.
# Each experiment waits until previous tests have been completed.
# Logs are written to a log folder.
# At the end, logs are cleaned and the summaries are extracted and stored in separate files.
#
# Author: Patrick K. Erdelt
# Email: patrick.erdelt@bht-berlin.de
# Date: 2024-10-01
# Version: 1.0
######################################################################################


BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

mkdir -p $LOG_DIR

# Define the wait_process function
wait_process() {
    local process_name=$1

    # Wait until the process with the name passed as an argument has terminated
    while ps aux | grep "[p]ython $process_name.py" > /dev/null; do
        # Process is still running, wait for 5 seconds
        echo "$(date +"%Y-%m-%d %H:%M:%S"): Waiting for process python $process_name.py to terminate..."
        sleep 60
    done

    echo "$(date +"%Y-%m-%d %H:%M:%S"): Process python $process_name.py has terminated."
}

# Example usage
#wait_process "tpch"


# Wait for all previous jobs to complete
wait_process "tpch"
wait_process "tpcds"
wait_process "hammerdb"
wait_process "benchbase"
wait_process "ycsb"














###########################################
############### TPC-H MySQL ###############
###########################################



### TPC-H Power Test - only MySQL (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mysql_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mysql_1.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"


### TPC-H Monitoring (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 10 \
  -dt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mysql_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mysql_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"

#### Delete persistent storage
kubectl delete pvc bexhoma-storage-mysql-tpch-1
sleep 30


### TPC-H Throughput Test (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 10 \
  -dt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mysql_3.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mysql_3.log


#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "tpch"




###########################################
############ TPC-H PostgreSQL #############
###########################################



### TPC-H Power Test - only PostgreSQL (TestCases.md)
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
  run </dev/null &>$LOG_DIR/test_tpch_testcase_postgresql_1.log &


#### Wait so that next experiment receives a different code
wait_process "tpch"


### TPC-H Monitoring (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 10 \
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
  run </dev/null &>$LOG_DIR/test_tpch_testcase_postgresql_2.log &


#### Wait so that next experiment receives a different code
wait_process "tpch"

#### Delete persistent storage
kubectl delete pvc bexhoma-storage-postgresql-tpch-1
sleep 30


### TPC-H Throughput Test (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 10 \
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
  run </dev/null &>$LOG_DIR/test_tpch_testcase_postgresql_3.log &


#### Wait so that next experiment receives a different code
wait_process "tpch"









###########################################
############## TPC-H MariaDB ##############
###########################################



### TPC-H Power Test - only MariaDB (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mariadb_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mariadb_1.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"


### TPC-H Monitoring (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mariadb_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mariadb_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"


#### Delete persistent storage
kubectl delete pvc bexhoma-storage-mariadb-tpch-1
sleep 30


### TPC-H Throughput Test (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mariadb_3.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mariadb_3.log


#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "tpch"










###########################################
############### TPC-DS MySQL ##############
###########################################



### TPC-H Power Test - only MySQL (TestCases.md)
nohup python tpcds.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_tpcds_testcase_mysql_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mysql_1.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"


### TPC-H Monitoring (TestCases.md)
nohup python tpcds.py -ms 1 -tr \
  -sf 10 \
  -dt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_tpcds_testcase_mysql_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mysql_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"

#### Delete persistent storage
kubectl delete pvc bexhoma-storage-mysql-tpcds-1
sleep 30


### TPC-H Throughput Test (TestCases.md)
nohup python tpcds.py -ms 1 -tr \
  -sf 10 \
  -dt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/test_tpcds_testcase_mysql_3.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mysql_3.log


#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "tpcds"




###########################################
############ TPC-DS PostgreSQL ############
###########################################



### TPC-H Power Test - only PostgreSQL (TestCases.md)
nohup python tpcds.py -ms 1 -tr \
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
  run </dev/null &>$LOG_DIR/test_tpcds_testcase_postgresql_1.log &


#### Wait so that next experiment receives a different code
wait_process "tpcds"


### TPC-H Monitoring (TestCases.md)
nohup python tpcds.py -ms 1 -tr \
  -sf 10 \
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
  run </dev/null &>$LOG_DIR/test_tpcds_testcase_postgresql_2.log &


#### Wait so that next experiment receives a different code
wait_process "tpcds"

#### Delete persistent storage
kubectl delete pvc bexhoma-storage-postgresql-tpcds-1
sleep 30


### TPC-H Throughput Test (TestCases.md)
nohup python tpcds.py -ms 1 -tr \
  -sf 10 \
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
  run </dev/null &>$LOG_DIR/test_tpcds_testcase_postgresql_3.log &


#### Wait so that next experiment receives a different code
wait_process "tpcds"









###########################################
############## TPC-DS MariaDB #############
###########################################



### TPC-H Power Test - only MariaDB (TestCases.md)
nohup python tpcds.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_tpcds_testcase_mariadb_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mariadb_1.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"


### TPC-H Monitoring (TestCases.md)
nohup python tpcds.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_tpcds_testcase_mariadb_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mariadb_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"


#### Delete persistent storage
kubectl delete pvc bexhoma-storage-mariadb-tpcds-1
sleep 30


### TPC-H Throughput Test (TestCases.md)
nohup python tpcds.py -ms 1 -tr \
  -sf 1 \
  -dt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 100Gi \
  run </dev/null &>$LOG_DIR/test_tpcds_testcase_mariadb_3.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mariadb_3.log


#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "tpcds"




###########################################
########### Benchbase PostgreSQL ##########
###########################################



#### Benchbase Simple (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 160 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_postgresql_1.log &


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


#### Delete persistent storage
kubectl delete pvc bexhoma-storage-postgresql-benchbase-16
sleep 30


### Benchbase Persistency (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 160 \
  -nbf 8 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_postgresql_2.log &


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


### Benchbase Monitoring (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 160 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_postgresql_3.log &


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


### Benchbase Complex (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 8 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_postgresql_4.log &


#### Wait so that next experiment receives a different code
#sleep 1800
wait_process "benchbase"







###########################################
############# Benchbase MySQL #############
###########################################



#### Benchbase Simple (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MySQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 160 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mysql_1.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_mysql_1.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


#### Delete persistent storage
kubectl delete pvc bexhoma-storage-mysql-benchbase-16
sleep 30


### Benchbase Persistency (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MySQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 160 \
  -nbf 8 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mysql_2.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_mysql_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


### Benchbase Monitoring (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MySQL \
  -tb 1024 \
  -nbp 1 \
  -nbt 160 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mysql_3.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_mysql_3.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


### Benchbase Complex (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MySQL \
  -tb 1024 \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 8 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mysql_4.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_mysql_4.log


#### Wait so that next experiment receives a different code
#sleep 1800
wait_process "benchbase"









###########################################
############ Benchbase MariaDB ############
###########################################



#### Benchbase Simple (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MariaDB \
  -tb 1024 \
  -nbp 1 \
  -nbt 160 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mariadb_1.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_mariadb_1.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


#### Delete persistent storage
kubectl delete pvc bexhoma-storage-mariadb-benchbase-16
sleep 30


### Benchbase Persistency (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MariaDB \
  -tb 1024 \
  -nbp 1 \
  -nbt 160 \
  -nbf 8 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mariadb_2.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_mariadb_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


### Benchbase Monitoring (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MariaDB \
  -tb 1024 \
  -nbp 1 \
  -nbt 160 \
  -nbf 8 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mariadb_3.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_mariadb_3.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


### Benchbase Complex (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MariaDB \
  -tb 1024 \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 8 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mariadb_4.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_mariadb_4.log


#### Wait so that next experiment receives a different code
#sleep 1800
wait_process "benchbase"








###########################################
########## HammerDB PostgreSQL ############
###########################################




### HammerDB Simple (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_postgresql_1.log &


#### Wait so that next experiment receives a different code
wait_process "hammerdb"


#### Delete persistent storage
kubectl delete pvc bexhoma-storage-mysql-hammerdb-16
sleep 30


### HammerDB Monitoring (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_postgresql_2.log &


#### Wait so that next experiment receives a different code
wait_process "hammerdb"


### HammerDB Complex (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 16 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_postgresql_3.log &


#### Wait so that next experiment receives a different code
wait_process "hammerdb"






###########################################
############# HammerDB MySQL ##############
###########################################




### HammerDB Simple (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mysql_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_hammerdb_testcase_mysql_1.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "hammerdb"


#### Delete persistent storage
kubectl delete pvc bexhoma-storage-mysql-hammerdb-16
sleep 30


### HammerDB Monitoring (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mysql_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_hammerdb_testcase_mysql_2.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "hammerdb"


### HammerDB Complex (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 16 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mysql_3.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_hammerdb_testcase_mysql_3.log


#### Wait so that next experiment receives a different code
#sleep 3000
wait_process "hammerdb"








###########################################
############ HammerDB MariaDB #############
###########################################




### HammerDB Simple (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mariadb_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_hammerdb_testcase_mariadb_1.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "hammerdb"


#### Delete persistent storage
kubectl delete pvc bexhoma-storage-mariadb-hammerdb-16
sleep 30


### HammerDB Monitoring (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mariadb_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_hammerdb_testcase_mariadb_2.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "hammerdb"


### HammerDB Complex (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -sd 2 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 16 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mariadb_3.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_hammerdb_testcase_mariadb_3.log


#### Wait so that next experiment receives a different code
#sleep 3000
wait_process "hammerdb"















###########################################
############ YCSB PostgreSQL ##############
###########################################


### YCSB Loader Test for Scaling the Driver (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 4,8 \
  -nlt 32,64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_1.log &


#### Wait so that next experiment receives a different code
wait_process "ycsb"



#### Delete persistent storage
kubectl delete pvc bexhoma-storage-postgresql-ycsb-1
sleep 30


### YCSB Loader Test for Persistency (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_2.log &


#### Wait so that next experiment receives a different code
wait_process "ycsb"



### YCSB Execution for Scaling and Repetition (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1,2 \
  -nc 2 \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_3.log &


#### Wait so that next experiment receives a different code
wait_process "ycsb"



### YCSB Execution Different Workload (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload e \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_4.log &


#### Wait so that next experiment receives a different code
wait_process "ycsb"



#### YCSB Execution Monitoring (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -rst shared -rss 50Gi \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_5.log &


#### Wait so that next experiment receives a different code
wait_process "ycsb"










###########################################
############### YCSB MySQL ################
###########################################


### YCSB Loader Test for Scaling the Driver (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 4,8 \
  -nlt 32,64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_mysql_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_mysql_1.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"



#### Delete persistent storage
kubectl delete pvc bexhoma-storage-mysql-ycsb-1
sleep 30


### YCSB Loader Test for Persistency (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_mysql_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_mysql_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "ycsb"



### YCSB Execution for Scaling and Repetition (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1,2 \
  -nc 2 \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_mysql_3.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_mysql_3.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"



### YCSB Execution Different Workload (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload e \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -rst shared -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_mysql_4.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_mysql_4.log


#### Wait so that next experiment receives a different code
#sleep 300
wait_process "ycsb"



#### YCSB Execution Monitoring (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -rst shared -rss 50Gi \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_mysql_5.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_mysql_5.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"













###########################################
############## YCSB MariaDB ###############
###########################################



### YCSB Loader Test for Scaling the Driver (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 4,8 \
  -nlt 32,64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_mariadb_1.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_mariadb_1.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"



#### Delete persistent storage
kubectl delete pvc bexhoma-storage-mariadb-ycsb-1
sleep 30


### YCSB Loader Test for Persistency (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_mariadb_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_mariadb_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "ycsb"


### YCSB Execution for Scaling and Repetition (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1,2 \
  -nc 2 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_mariadb_3.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_mariadb_3.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"


### YCSB Execution Different Workload (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload e \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_mariadb_4.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_mariadb_4.log


#### Wait so that next experiment receives a different code
#sleep 300
wait_process "ycsb"


#### YCSB Execution Monitoring (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 1024 \
  -nlp 8 \
  -nlt 64 \
  -nlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -rst shared -rss 30Gi \
  -m -mc \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_mariadb_5.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_ycsb_testcase_mariadb_5.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "ycsb"
















###########################################
############## Clean Folder ###############
###########################################


clean_logs








