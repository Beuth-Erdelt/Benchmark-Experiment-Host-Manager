#!/bin/bash
######################################################################################
# Bash Script for Bexhoma Test Runs - Test scripts for database services
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














###############################################################
################## TPC-DS Persistent Storage ##################
###############################################################




#### TCP-DS Persistent Storage (Example-TPC-DS.md)
nohup python tpcds.py -ms 4 -dt -tr \
  -dbms MySQL \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_mysql_storage.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"




#### TCP-DS Persistent Storage (Example-TPC-DS.md)
nohup python tpcds.py -ms 4 -dt -tr \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_postgresql_storage.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"




#### TCP-DS Persistent Storage (Example-TPC-DS.md)
nohup python tpcds.py -ms 4 -dt -tr \
  -dbms MariaDB \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_mariadb_storage.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"




#### TCP-DS Persistent Storage (Example-TPC-DS.md)
nohup python tpcds.py -ms 4 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_monetdb_storage.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"
















################################################
################## YugaByteDB ##################
################################################


#### YCSB Ingestion (Example-YugaByteDB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_yugabytedb_1.log &


#### YCSB Execution (Example-YugaByteDB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -sl \
  --workload a \
  -dbms YugabyteDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_yugabytedb_2.log &


#### YCSB Dummy Persistent Storage (Example-YugaByteDB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 1Gi \
  run </dev/null &>$LOG_DIR/doc_ycsb_yugabytedb_3.log &


#### Benchbase Simple (Example-YugaByteDB.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms YugabyteDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_yugabytedb_1.log &


#### Benchbase More Complex (Example-YugaByteDB.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 60 \
  -dbms YugabyteDB \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_yugabytedb_2.log &





#################################################
################## CockroachDB ##################
#################################################


#### YCSB Ingestion (Example-CockroachDB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms CockroachDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_cockroachdb_1.log &


#### YCSB Execution (Example-CockroachDB.md)
nohup python ycsb.py -ms 1 -tr \
  -sl \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms CockroachDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_cockroachdb_2.log &


#### Benchbase Simple (Example-CockroachDB.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms CockroachDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_cockroachdb_1.log &


#### Benchbase Complex (Example-CockroachDB.md)
nohup python benchbase.py -ms 1 -tr \
  -sf 128 \
  -sd 60 \
  -dbms CockroachDB \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_cockroachdb_2.log &







nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_yugabytedb_tmp1.log &

wait_process "ycsb"

nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -db \
  run </dev/null &>$LOG_DIR/doc_ycsb_yugabytedb_tmp2.log &

wait_process "ycsb"



nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 1 \
  --workload a \
  -dbms YugabyteDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run </dev/null &>$LOG_DIR/doc_ycsb_yugabytedb_tmp3.log &


wait_process "ycsb"



nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms CockroachDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/doc_ycsb_cockroachdb_tmp.log &


wait_process "ycsb"



nohup python tpcds.py -ms 4 -dt -tr \
  -t 3600 \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_compare_tmp.log &


wait_process "tpcds"





nohup python ycsb.py -ms 5 -tr \
  -sf 1 \
  -sfo 1 \
  --workload a \
  -dbms DatabaseService \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -sl \
  run </dev/null &>$LOG_DIR/test_database_service.log &


wait_process "ycsb"





















###########################################
################# TPC-DS ##################
###########################################


#### TCP-DS Compare (Example-TPC-DS.md)
nohup python tpcds.py -ms 4 -dt -tr \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 3600 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 30Gi \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_compare_storage.log &


#### Wait so that next experiment receives a different code
#sleep 7200
wait_process "tpcds"


#### TCP-DS Compare (Example-TPC-DS.md)
nohup python tpcds.py -ms 6 -dt -tr \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 3600 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_compare.log &


#### Wait so that next experiment receives a different code
#sleep 7200
wait_process "tpcds"

#### TCP-DS Compare (Example-TPC-DS.md)
nohup python tpcds.py -ms 6 -dt -tr \
  -nlp 8 \
  -nlt 8 \
  -sf 10 \
  -t 3600 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_compare_10.log &


#### Wait so that next experiment receives a different code
#sleep 7200
wait_process "tpcds"


#### TCP-DS Monitoring (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_monitoring.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"


#### TCP-DS Throughput (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -nc 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_throughput.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-1
sleep 30


#### TCP-DS Persistent Storage (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpcds_testcase_storage.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpcds"



###########################################
############# TPC-DS MonetDB ##############
###########################################


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-100
sleep 30


#### TCP-DS Power 100 (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 7200 -dt \
  -rst shared -rss 500Gi \
  run &>$LOG_DIR/doc_tpcds_monetdb_1.log &


#### Wait so that next experiment receives a different code
#sleep 1800
wait_process "tpcds"


#### TCP-DS Power 100 (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 2 -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 7200 -dt \
  -rst shared -rss 500Gi \
  run &>$LOG_DIR/doc_tpcds_monetdb_2.log &


#### Wait so that next experiment receives a different code
#sleep 4800
wait_process "tpcds"


#### TCP-DS Throughput 100 (Example-TPC-DS.md)
nohup python tpcds.py -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1,1,3 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -t 7200 -dt \
  -rst shared -rss 500Gi \
  run &>$LOG_DIR/doc_tpcds_monetdb_3.log &

#### Wait so that next experiment receives a different code
#sleep 4800
wait_process "tpcds"























#PostgreSQL
##################################### sidecar
nohup python ycsb.py -ms 1 -tr   -sf 1   -sfo 1   --workload a   -dbms PostgreSQL   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -tb 16384   -nlp 8   -nlt 64   -nlf 4   -nbp 1   -nbt 64   -nbf 4   -ne 1   -nc 1   -m  run </dev/null &>$LOG_DIR/test_ycsb_postgresql_sidecar.log &
#-) ok

##################################### daemonset
nohup python ycsb.py -ms 1 -tr   -sf 1   -sfo 1   --workload a   -dbms PostgreSQL   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -tb 16384   -nlp 8   -nlt 64   -nlf 4   -nbp 1   -nbt 64   -nbf 4   -ne 1   -nc 1   -m  -mc -db run </dev/null &>$LOG_DIR/test_ycsb_postgresql_daemonset.log &
#-) ok

##################################### cluster preinstalled
nohup python ycsb.py -ms 1 -tr   -sf 1   -sfo 1   --workload a   -dbms PostgreSQL   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -tb 16384   -nlp 8   -nlt 64   -nlf 4   -nbp 1   -nbt 64   -nbf 4   -ne 1   -nc 1   -m  -mc -db run </dev/null &>$LOG_DIR/test_ycsb_postgresql_cluster.log &
#-) ok




#DatabaseService
##################################### cluster preinstalled

#########################  With loading
nohup python ycsb.py -ms 5 -tr   -sf 1   -sfo 1   --workload a   -dbms DatabaseService   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -tb 16384   -nlp 8   -nlt 64   -nlf 4   -nbp 1   -nbt 64   -nbf 4   -ne 1   -nc 1   -m -mc     run </dev/null &>$LOG_DIR/test_ycsb_databaseservice_tmp1.log &
#-) k8s: Dummy deployment - für loading z.B. PostgreSQL kompatibel: PostgreSQL Container wegen psql
#-) Metrics
#--) Execution quatsch (?)

#########################  No loading
nohup python ycsb.py -ms 5 -tr   -sf 1   -sfo 1   --workload a   -dbms DatabaseService   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -tb 16384   -nlp 8   -nlt 64   -nlf 4   -nbp 1   -nbt 64   -nbf 4   -ne 1   -nc 1   -m -mc   -sl   run </dev/null &>$LOG_DIR/test_ycsb_databaseservice_tmp2.log &
#-) cluster.config: Infos und JDBC Verbindungsdaten
#-) OK

nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 1 \
  --workload a \
  -dbms DatabaseService \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 1Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_databaseservice_tmp3.log &

  nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 1 \
  --workload a \
  -dbms DatabaseService \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 1Gi \
  run </dev/null &>$LOG_DIR/test_ycsb_databaseservice_tmp4.log &



  nohup python ycsb.py -ms 1 -tr \
  -sf 1 \
  -sfo 100 \
  --workload a \
  -dbms DatabaseService \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -sl \
  run </dev/null &>$LOG_DIR/test_ycsb_databaseservice_tmp5.log &




#YugabyteDB
##################################### daemonset
#########################  With loading
nohup python ycsb.py -ms 1 -tr   -sf 1   -sfo 1   --workload a   -dbms YugabyteDB   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -tb 16384   -nlp 8   -nlt 64   -nlf 4   -nbp 1   -nbt 64   -nbf 4   -ne 1   -nc 1   -m -mc  run </dev/null &>$LOG_DIR/test_ycsb_yugabytedb_tmp1.log &
#-) OK, after retries (usertable, host name)

#########################  No loading
nohup python ycsb.py -ms 1 -tr   -sf 1   -sfo 1   --workload a   -dbms YugabyteDB   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -tb 16384   -nlp 8   -nlt 64   -nlf 4   -nbp 1   -nbt 64   -nbf 4   -ne 1   -nc 1   -m -mc -sl  run </dev/null &>$LOG_DIR/test_ycsb_yugabytedb_tmp2.log &
#-) OK

#########################  No loading, with debug
nohup python ycsb.py -ms 1 -tr   -sf 1   -sfo 1   --workload a   -dbms YugabyteDB   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -tb 16384   -nlp 8   -nlt 64   -nlf 4   -nbp 1   -nbt 64   -nbf 4   -ne 1   -nc 1   -m -mc -sl -db run </dev/null &>$LOG_DIR/test_ycsb_yugabytedb_tmp2db.log &
#-) without loading: ok


##################################### cluster preinstalled
#########################  With loading
nohup python ycsb.py -ms 1 -tr   -sf 1   -sfo 1   --workload a   -dbms YugabyteDB   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -tb 16384   -nlp 8   -nlt 64   -nlf 4   -nbp 1   -nbt 64   -nbf 4   -ne 1   -nc 1   -m -mc  run </dev/null &>$LOG_DIR/test_ycsb_yugabytedb_tmp3.log &

#########################  No loading
nohup python ycsb.py -ms 1 -tr   -sf 1   -sfo 1   --workload a   -dbms YugabyteDB   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -tb 16384   -nlp 8   -nlt 64   -nlf 4   -nbp 1   -nbt 64   -nbf 4   -ne 1   -nc 1   -m -mc -sl  run </dev/null &>$LOG_DIR/test_ycsb_yugabytedb_tmp4.log &
#-) OK

#########################  No loading, with debug
nohup python ycsb.py -ms 1 -tr   -sf 1   -sfo 1   --workload a   -dbms YugabyteDB   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -tb 16384   -nlp 8   -nlt 64   -nlf 4   -nbp 1   -nbt 64   -nbf 4   -ne 1   -nc 1   -m -mc -sl -db run </dev/null &>$LOG_DIR/test_ycsb_yugabytedb_tmp4db.log &
#-) OK


##################################### sidecar

#########################  No loading
nohup python ycsb.py -ms 1 -tr   -sf 1   -sfo 1   --workload a   -dbms YugabyteDB   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -tb 16384   -nlp 8   -nlt 64   -nlf 4   -nbp 1   -nbt 64   -nbf 4   -ne 1   -nc 1   -m -sl  run </dev/null &>$LOG_DIR/test_ycsb_yugabytedb_tmp6.log &

#########################  No loading, with debug
nohup python ycsb.py -ms 1 -tr   -sf 1   -sfo 1   --workload a   -dbms YugabyteDB   -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK   -tb 16384   -nlp 8   -nlt 64   -nlf 4   -nbp 1   -nbt 64   -nbf 4   -ne 1   -nc 1   -m -sl -db run </dev/null &>$LOG_DIR/test_ycsb_yugabytedb_tmp6db.log &










nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms YugabyteDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_yugabytedb_1.log &





nohup python benchbase.py -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms DatabaseService \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -sl \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_benchbase_databaseservice_1.log &




#### TCP-H Monitoring (Example-TPC-H.md)
nohup python tpch.py -ms 2 -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_databaseservice_1.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"


#### TCP-H Monitoring (Example-TPC-H.md)
nohup python tpch.py -ms 2 -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -sl \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_databaseservice_2.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"


# delete pvc
kubectl delete pvc bexhoma-storage-databaseservice-tpch-3

sleep 10

# delete database service
kubectl delete deployment bexhoma-deployment-postgres
kubectl delete svc bexhoma-service

sleep 30

# start database service
kubectl create -f k8s/deploymenttemplate-PostgreSQLService.yml


#### TCP-H Monitoring (Example-TPC-H.md)
nohup python tpch.py -ms 2 -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 1Gi \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_databaseservice_3.db.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"


#### TCP-H Monitoring (Example-TPC-H.md)
nohup python tpch.py -ms 2 -dt -tr \
  -dbms DatabaseService \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -ii -ic -is \
  -t 1200 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 1Gi \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_databaseservice_4.db.log &

#### Wait so that next experiment receives a different code
#sleep 600
wait_process "tpch"




###########################################
############## Clean Folder ###############
###########################################



export MYDIR=$(pwd)
cd $LOG_DIR
# remove connection errors from logs
grep -rl "Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens." . | xargs sed -i '/Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens./d'
cd $MYDIR

# Loop over each text file in the source directory
for file in "$LOG_DIR"/*.log; do
    # Get the filename without the path and extension
    echo "Cleaning $file"
    filename=$(basename "$file" .log)
    # Extract lines starting from "## Show Summary" and save as <filename>_summary.txt in the destination directory
    awk '/## Show Summary/ {show=1} show {print}' "$file" > "$LOG_DIR/${filename}_summary.txt"
done

echo "Extraction complete! Files are saved in $LOG_DIR."

