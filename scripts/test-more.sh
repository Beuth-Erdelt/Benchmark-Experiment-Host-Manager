#!/bin/bash
# Extended test runs covering additional DBMS and parameter combinations.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


# Import functions from testfunctions.sh
source ./scripts/testfunctions.sh

# Config nodes and paths
BEXHOMA_NODE_SUT="cl-worker14"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

# Check for file
if [[ ! -f "cluster.config" ]]; then
    echo "Error: cluster.config not found."
    exit 1
fi
echo "Passed: ./cluster.config found."

# Check for directories
for dir in "experiments" "k8s"; do
    if [[ ! -d "$dir" ]]; then
        echo "Error: Directory '$dir' missing."
        exit 1
    fi
done
echo "Passed: ./experiments/ found."
echo "Passed: ./k8s/ found."


if ! prepare_logs; then
    echo "Error: prepare_logs failed with code $?"
    exit 1
fi
echo "Passed: $LOG_DIR/ found."

echo "Checks passed. Proceeding..."

# Wait for all previous jobs to complete
wait_process "tpch"
wait_process "tpcds"
wait_process "hammerdb"
wait_process "benchbase"
wait_process "ycsb"




###########################################
################# TPC-H ###################
###########################################


#### TCP-H Compare (TestCases.md)
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpch \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpch_testcase_compare.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H compare  sf=1"


###########################################
################# TPC-DS ##################
###########################################


#### TCP-DS Compare (TestCases.md)
# -sf 1                         scaling factor (controls database size in GB)
# -nlp 8                        number of data loader pods
# -nlt 8                        threads per loader pod
# -xii                          create indexes after data load
# -xic                          enforce constraints after data load
# -xis                          run ANALYZE after data load
# -xdt                          disable result type checking
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -t 1200                       query timeout in seconds
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma tpcds \
  -sf 1 \
  -nlp 8 \
  -nlt 8 \
  -xii -xic -xis \
  -xdt \
  -ms $BEXHOMA_MS \
  -t 1200 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/test_tpcds_testcase_compare.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS compare  sf=1"













###########################################
############### TPC-H MySQL ###############
###########################################



### TPC-H Power Test - only MySQL (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -xdt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
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
  -rr 128Gi -lr 128Gi \
  -xdt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
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
  -rr 128Gi -lr 128Gi \
  -xdt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst cephcsi -rss 50Gi -rsr \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mysql_3.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mysql_3.log


#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "tpch"

nohup python tpch.py -ms 1 -xdt -tr \
  -dbms MySQL \
  -rr 128Gi -lr 128Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 10 \
  -t 1200 \
  -xii -xic -xis \
  -m -mc -ma \
  -rnn "$BEXHOMA_NODE_SUT" \
  -rnl "$BEXHOMA_NODE_LOAD" \
  -rnb "$BEXHOMA_NODE_BENCHMARK" \
  -rst ramdisk -rss 50Gi \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_mysql_ramdisk.log &

wait_process "tpch"


###########################################
############ TPC-H PostgreSQL #############
###########################################



### TPC-H Power Test - only PostgreSQL (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -xdt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
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
  -rr 128Gi -lr 128Gi \
  -xdt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
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
  -rr 128Gi -lr 128Gi \
  -xdt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst cephcsi -rss 50Gi -rsr \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_postgresql_3.log &


#### Wait so that next experiment receives a different code
wait_process "tpch"









###########################################
############## TPC-H MariaDB ##############
###########################################



### TPC-H Power Test - only MariaDB (TestCases.md)
nohup python tpch.py -ms 1 -tr \
  -sf 1 \
  -xdt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
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
  -xdt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
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
  -xdt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst cephcsi -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_tpch_testcase_mariadb_3.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_tpch_testcase_mariadb_3.log



#### Wait so that next experiment receives a different code
#sleep 1200
wait_process "tpch"

nohup python tpch.py -ms 1 -xdt -tr -lr 64Gi \
  -dbms MariaDB \
  -rr 128Gi -lr 128Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 10 \
  -t 1200 \
  -xii -xic -xis \
  -m -mc -ma \
  -rnn "$BEXHOMA_NODE_SUT" \
  -rnl "$BEXHOMA_NODE_LOAD" \
  -rnb "$BEXHOMA_NODE_BENCHMARK" \
  -rst ramdisk -rss 50Gi \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_mariadb_ramdisk.log &

wait_process "tpch"










###########################################
############### TPC-DS MySQL ##############
###########################################



### TPC-H Power Test - only MySQL (TestCases.md)
nohup python tpcds.py -ms 1 -tr \
  -sf 1 \
  -xdt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
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
  -xdt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
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
  -xdt \
  -t 1200 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst cephcsi -rss 100Gi \
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
  -xdt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
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
  -xdt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
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
  -xdt \
  -t 1200 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst cephcsi -rss 100Gi \
  run </dev/null &>$LOG_DIR/test_tpcds_testcase_postgresql_3.log &


#### Wait so that next experiment receives a different code
wait_process "tpcds"









###########################################
############## TPC-DS MariaDB #############
###########################################



### TPC-H Power Test - only MariaDB (TestCases.md)
nohup python tpcds.py -ms 1 -tr \
  -sf 1 \
  -xdt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
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
  -xdt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
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
  -xdt \
  -t 1200 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xii -xic -xis \
  -nlp 8 \
  -nbp 1 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst cephcsi -rss 100Gi \
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
  -xsd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -xtb 1024 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
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
  -xsd 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -xtb 1024 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ne 1 \
  -nc 2 \
  -rst cephcsi -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_postgresql_2.log &


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


### Benchbase Monitoring (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -xsd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -xtb 1024 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
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
  -xsd 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -xtb 1024 \
  -nbp 1,2 \
  -nbt 160 \
  -xnbf 8 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst cephcsi -rss 30Gi \
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
  -xsd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MySQL \
  -xtb 1024 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
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
  -xsd 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MySQL \
  -xtb 1024 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ne 1 \
  -nc 2 \
  -rst cephcsi -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mysql_2.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_mysql_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


### Benchbase Monitoring (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -xsd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MySQL \
  -xtb 1024 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
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
  -xsd 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MySQL \
  -xtb 1024 \
  -nbp 1,2 \
  -nbt 160 \
  -xnbf 8 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst cephcsi -rss 30Gi \
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
  -xsd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MariaDB \
  -xtb 1024 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
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
  -xsd 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MariaDB \
  -xtb 1024 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
  -ne 1 \
  -nc 2 \
  -rst cephcsi -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_benchbase_testcase_mariadb_2.log &

# watch -n 30 tail -n 50 $LOG_DIR/test_benchbase_testcase_mariadb_2.log


#### Wait so that next experiment receives a different code
#sleep 600
wait_process "benchbase"


### Benchbase Monitoring (TestCases.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -xsd 5 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MariaDB \
  -xtb 1024 \
  -nbp 1 \
  -nbt 160 \
  -xnbf 8 \
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
  -xsd 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MariaDB \
  -xtb 1024 \
  -nbp 1,2 \
  -nbt 160 \
  -xnbf 8 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst cephcsi -rss 30Gi \
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
  -rst cephcsi -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_postgresql_2.log &


#### Wait so that next experiment receives a different code
wait_process "hammerdb"


### HammerDB Complex (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xsd 2 \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 16 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst cephcsi -rss 30Gi \
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
  -rst cephcsi -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mysql_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_hammerdb_testcase_mysql_2.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "hammerdb"


### HammerDB Complex (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xsd 2 \
  -dbms MySQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 16 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst cephcsi -rss 30Gi \
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
  -rst cephcsi -rss 30Gi \
  run </dev/null &>$LOG_DIR/test_hammerdb_testcase_mariadb_2.log &

#watch -n 30 tail -n 50 $LOG_DIR/test_hammerdb_testcase_mariadb_2.log


#### Wait so that next experiment receives a different code
#sleep 900
wait_process "hammerdb"


### HammerDB Complex (TestCases.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xsd 2 \
  -dbms MariaDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 16 \
  -ne 1,2 \
  -nc 2 \
  -m -mc \
  -rst cephcsi -rss 30Gi \
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
  -xtb 1024 \
  -nlp 4,8 \
  -nlt 32,64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
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
  -xtb 1024 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 2 \
  -rst cephcsi -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_2.log &


#### Wait so that next experiment receives a different code
wait_process "ycsb"



### YCSB Execution for Scaling and Repetition (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 1024 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1,2 \
  -nc 2 \
  -rst cephcsi -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_3.log &


#### Wait so that next experiment receives a different code
wait_process "ycsb"



### YCSB Execution Different Workload (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload e \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 1024 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -rst cephcsi -rss 50Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_testcase_postgresql_4.log &


#### Wait so that next experiment receives a different code
wait_process "ycsb"



#### YCSB Execution Monitoring (TestCases.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  --workload a \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 1024 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -rst cephcsi -rss 50Gi \
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
  -xtb 1024 \
  -nlp 4,8 \
  -nlt 32,64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
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
  -xtb 1024 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 2 \
  -rst cephcsi -rss 50Gi \
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
  -xtb 1024 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1,2 \
  -nc 2 \
  -rst cephcsi -rss 50Gi \
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
  -xtb 1024 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -rst cephcsi -rss 50Gi \
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
  -xtb 1024 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -rst cephcsi -rss 50Gi \
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
  -xtb 1024 \
  -nlp 4,8 \
  -nlt 32,64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
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
  -xtb 1024 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 2 \
  -rst cephcsi -rss 30Gi \
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
  -xtb 1024 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1,2 \
  -nc 2 \
  -rst cephcsi -rss 30Gi \
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
  -xtb 1024 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -rst cephcsi -rss 30Gi \
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
  -xtb 1024 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 1 \
  -nbp 1,8 \
  -nbt 64 \
  -xnbf 1 \
  -ne 1 \
  -nc 1 \
  -rst cephcsi -rss 30Gi \
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








