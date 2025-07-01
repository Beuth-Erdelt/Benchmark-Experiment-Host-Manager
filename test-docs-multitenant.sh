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
######### Benchbase TPC-C Multi-Tenant PVC #########
####################################################


kubectl delete pvc bexhoma-storage-postgresql-tpch-1

nohup python tpch.py -ms 5 -tr -db \
  --dbms PostgreSQL \
  -ii -ic -is -nlp 2 -nlt 1 -nbp 2 -nbt 64 -ne 2 -mtn 2 -mtb schema \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_schema.log &

kubectl delete pvc bexhoma-storage-postgresql-tpch-1

nohup python tpch.py -ms 5 -tr -db \
  --dbms PostgreSQL \
  -ii -ic -is -nlp 2 -nlt 1 -nbp 2 -nbt 64 -ne 2 -mtn 2 -mtb schema -ss \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_schema.log &

kubectl delete pvc bexhoma-storage-postgresql-tpch-1

nohup python tpch.py -ms 5 -tr -db \
  --dbms PostgreSQL \
  -ii -ic -is -nlp 2 -nlt 1 -nbp 2 -nbt 64 -ne 2 -mtn 2 -mtb database \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_database.log &

kubectl delete pvc bexhoma-storage-postgresql-tpch-1

nohup python tpch.py -ms 5 -tr -db \
  --dbms PostgreSQL \
  -ii -ic -is -nlp 2 -nlt 1 -nbp 2 -nbt 64 -ne 2 -mtn 2 -mtb database \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_database.log &












####################################################
######### Benchbase TPC-C Multi-Tenant PVC #########
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





####################################################
###### Benchbase TPC-C Multi-Tenant Local HDD ######
####################################################

BEXHOMA_DURATION=10
BEXHOMA_TARGET=65536
BEXHOMA_SF=10
BEXHOMA_THREADS=$((BEXHOMA_SF * 10))

for i in {1..10}; do
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
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_schema_${BEXHOMA_TENANTS}.log"

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
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_database_${BEXHOMA_TENANTS}.log"

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
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_container_${BEXHOMA_TENANTS}.log"

    bexperiments stop

    clean_logs
done


BEXHOMA_TENANTS=2
BEXHOMA_SF=1

nohup python tpch.py run -rcp -shq -nr 5 \
  -mtn $BEXHOMA_TENANTS -mtb schema \
  -sf $BEXHOMA_SF \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp $BEXHOMA_TENANTS -nbp 1 \
  -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK -ss \
  </dev/null &> "$LOG_DIR/test_tpch_run_postgresql_tenants_schema_test.log"


####################################################
################ TPC-H Multi-Tenant ################
####################################################

BEXHOMA_SF=10
BEXHOMA_NUM_RUN=10

for i in {1..10}; do
    # Set environment variables
    export BEXHOMA_TENANTS=$i
    tenants=$BEXHOMA_TENANTS
    sizeInGi=$((tenants * 50))
    export BEXHOMA_SIZE_ALL="${sizeInGi}Gi"
    # Calculate limit RAM per tenant
    ramPerTenant=$((480 / tenants))
    export BEXHOMA_LIMIT_RAM="${ramPerTenant}Gi"

    # For debugging/verification
    echo "TENANTS=$BEXHOMA_TENANTS SIZE=$BEXHOMA_SIZE_ALL LIMIT_RAM=$BEXHOMA_LIMIT_RAM"

    # Run schema mode
    nohup python tpch.py run -rc 2 -lr 480Gi -m -mc -rcp -shq -t 3600 -nr $BEXHOMA_NUM_RUN \
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
    nohup python tpch.py run -rc 2 -lr 480Gi -m -mc -rcp -shq -t 3600 -nr $BEXHOMA_NUM_RUN \
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

    # Run container mode (fixed 50Gi size)
    nohup python tpch.py run -rc 2 -lr $BEXHOMA_LIMIT_RAM -m -mc -rcp -shq -t 3600 -nr $BEXHOMA_NUM_RUN \
      -mtn $BEXHOMA_TENANTS -mtb container \
      -sf $BEXHOMA_SF \
      --dbms PostgreSQL \
      -ii -ic -is \
      -nlp 1 -nbp 1 \
      -ne 1,1 \
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
      -rst shared -rss 50Gi \
      </dev/null &> "$LOG_DIR/test_tpch_run_postgresql_tenants_container_${BEXHOMA_TENANTS}_db.log"

    bexperiments stop

    clean_logs
done






###########################################
############## Clean Folder ###############
###########################################


clean_logs
