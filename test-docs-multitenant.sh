#!/bin/bash
######################################################################################
# Bash Script for Bexhoma Modes - Start / Load
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


# Import functions from testfunctions.sh
source ./testfunctions.sh

BEXHOMA_NODE_SUT="cl-worker11"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

if ! prepare_logs; then
    echo "Error: prepare_logs failed with code $?"
    exit 1
fi

# Wait for all previous jobs to complete
wait_process "tpch"
wait_process "tpcds"
wait_process "hammerdb"
wait_process "benchbase"
wait_process "ycsb"










####################################################
########### Benchbase TPC-C Multi-Tenant ###########
####################################################

BEXHOMA_DURATION=10
BEXHOMA_TARGET=65536
BEXHOMA_SF=10
BEXHOMA_THREADS=$((BEXHOMA_SF * 10))

for i in {1..0}; do
    # Set environment variables
    export BEXHOMA_TENANTS=$i
    tenants=$BEXHOMA_TENANTS
    sizeInGi=$((tenants * 20))
    export BEXHOMA_SIZE_ALL="${sizeInGi}Gi"

    # Run schema mode
    python ./benchbase.py run -rc 2 -m -mc -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms PostgreSQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
        -mtn "$BEXHOMA_TENANTS" -mtb schema \
        -rst shared -rss "$BEXHOMA_SIZE_ALL" \
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_schema_${BEXHOMA_TENANTS}_db.log"

    bexperiments stop

    # Run database mode
    python ./benchbase.py run -rc 2 -m -mc -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms PostgreSQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
        -mtn "$BEXHOMA_TENANTS" -mtb database \
        -rst shared -rss "$BEXHOMA_SIZE_ALL" \
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_database_${BEXHOMA_TENANTS}_db.log"

    bexperiments stop

    # Run container mode (fixed 5Gi size)
    python ./benchbase.py run -rc 2 -m -mc -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms PostgreSQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne 1,1 \
        -mtn "$BEXHOMA_TENANTS" -mtb container \
        -rst shared -rss 20Gi \
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_container_${BEXHOMA_TENANTS}_db.log"

    bexperiments stop

    clean_logs
done



nohup python tpch.py \
  -mtn $BEXHOMA_TENANTS -mtb schema \
  -sf $BEXHOMA_SF \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp $BEXHOMA_TENANTS -nbp 1 \
  -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss "$BEXHOMA_SIZE_ALL" \
  </dev/null &> "$LOG_DIR/test_tpch_run_postgresql_tenants_schema_${BEXHOMA_TENANTS}_db.log"


####################################################
################ TPC-H Multi-Tenant ################
####################################################

BEXHOMA_SF=1

for i in {1..10}; do
    # Set environment variables
    export BEXHOMA_TENANTS=$i
    tenants=$BEXHOMA_TENANTS
    sizeInGi=$((tenants * 20))
    export BEXHOMA_SIZE_ALL="${sizeInGi}Gi"

    # Run schema mode
    nohup python tpch.py run -rc 2 -m -mc \
      -mtn $BEXHOMA_TENANTS -mtb schema \
      -sf $BEXHOMA_SF \
      --dbms PostgreSQL \
      -ii -ic -is \
      -nlp $BEXHOMA_TENANTS -nbp 1 \
      -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
      -rst shared -rss "$BEXHOMA_SIZE_ALL" \
      </dev/null &> "$LOG_DIR/test_tpch_run_postgresql_tenants_schema_${BEXHOMA_TENANTS}_db.log"

    bexperiments stop

    # Run database mode
    nohup python tpch.py run -rc 2 -m -mc \
      -mtn $BEXHOMA_TENANTS -mtb database \
      -sf $BEXHOMA_SF \
      --dbms PostgreSQL \
      -ii -ic -is \
      -nlp $BEXHOMA_TENANTS -nbp 1 \
      -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
      -rst shared -rss "$BEXHOMA_SIZE_ALL" \
      </dev/null &> "$LOG_DIR/test_tpch_run_postgresql_tenants_database_${BEXHOMA_TENANTS}_db.log"

    bexperiments stop

    # Run container mode (fixed 5Gi size)
    nohup python tpch.py run -rc 2 -m -mc \
      -mtn $BEXHOMA_TENANTS -mtb container \
      -sf $BEXHOMA_SF \
      --dbms PostgreSQL \
      -ii -ic -is \
      -nlp 1 -nbp 1 \
      -ne 1,1 \
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
      -rst shared -rss 20Gi \
      </dev/null &> "$LOG_DIR/test_tpch_run_postgresql_tenants_container_${BEXHOMA_TENANTS}_db.log"

    bexperiments stop

    clean_logs
done






###########################################
############## Clean Folder ###############
###########################################


clean_logs
