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
######### Benchbase TPC-H Multi-Tenant PVC #########
####################################################

BEXHOMA_NUM_TENANTS=2

kubectl delete pvc bexhoma-storage-postgresql-schema-2-tpch-1

nohup python tpch.py -tr \
  --dbms PostgreSQL \
  -ii -ic -is -nlp $BEXHOMA_NUM_TENANTS -nlt 1 -nbp $BEXHOMA_NUM_TENANTS -nbt 64 -ne $BEXHOMA_NUM_TENANTS -mtn $BEXHOMA_NUM_TENANTS -mtb schema \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_schema.log &

wait_process "tpch"

kubectl delete pvc bexhoma-storage-postgresql-database-2-tpch-1

nohup python tpch.py -tr \
  --dbms PostgreSQL \
  -ii -ic -is -nlp $BEXHOMA_NUM_TENANTS -nlt 1 -nbp $BEXHOMA_NUM_TENANTS -nbt 64 -ne $BEXHOMA_NUM_TENANTS -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_database.log &


kubectl delete pvc bexhoma-storage-postgresql-0-2-tpch-1
kubectl delete pvc bexhoma-storage-postgresql-1-2-tpch-1

nohup python tpch.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp 1 -nbp 1 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_tpch_run_postgresql_tenants_container.log &

wait_process "tpch"




####################################################
######### Benchbase TPC-C Multi-Tenant PVC #########
####################################################

BEXHOMA_NUM_TENANTS=2

kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-1

nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb schema \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_schema.log &

wait_process "benchbase"

kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-1

nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_database.log &

wait_process "benchbase"

kubectl delete pvc bexhoma-storage-postgresql-0-2-benchbase-tpcc-1
kubectl delete pvc bexhoma-storage-postgresql-1-2-benchbase-tpcc-1

nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/test_benchbase_run_postgresql_tenants_container.log &

wait_process "benchbase"


















####################################################
#### Benchbase TPC-C Multi-Tenant PVC No Limits ####
####################################################

BEXHOMA_DURATION=10
BEXHOMA_TARGET=65536
BEXHOMA_SF=10
BEXHOMA_THREADS=$((BEXHOMA_SF * 10))
BEXHOMA_CPU=40
BEXHOMA_RAM=200

for i in {1..10}; do
    # Set environment variables
    export BEXHOMA_TENANTS=$i
    tenants=$BEXHOMA_TENANTS
    sizeInGi=$((tenants * 50))
    export BEXHOMA_SIZE_ALL="${sizeInGi}Gi"
    # Calculate RAM and CPU per tenant (integers)
    ramPerTenant=$(( $BEXHOMA_RAM / tenants ))
    cpuPerTenant=$(( $BEXHOMA_CPU / tenants ))

    # Export environment variable
    export BEXHOMA_LIMIT_RAM="${ramPerTenant}Gi"
    export BEXHOMA_LIMIT_RAM_TOTAL="${BEXHOMA_RAM}Gi"

    # Run schema mode
    python ./benchbase.py run -rc 0 -rr $BEXHOMA_LIMIT_RAM_TOTAL -lc 0 -lr $BEXHOMA_LIMIT_RAM_TOTAL -m -mc -ma -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms PostgreSQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
        -mtn "$BEXHOMA_TENANTS" -mtb schema \
        -rst shared -rss "$BEXHOMA_SIZE_ALL" \
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_schema_${BEXHOMA_TENANTS}_nolimit.log"

    bexperiments stop

    # Run database mode
    python ./benchbase.py run -rc 0 -rr $BEXHOMA_LIMIT_RAM_TOTAL -lc 0 -lr $BEXHOMA_LIMIT_RAM_TOTAL -m -mc -ma -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms PostgreSQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
        -mtn "$BEXHOMA_TENANTS" -mtb database \
        -rst shared -rss "$BEXHOMA_SIZE_ALL" \
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_database_${BEXHOMA_TENANTS}_nolimit.log"

    bexperiments stop

    # Run container mode (fixed 50Gi size)
    python ./benchbase.py run -rc 0 -rr $BEXHOMA_LIMIT_RAM -lc 0 -lr $BEXHOMA_LIMIT_RAM -m -mc -ma -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms PostgreSQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne 1,1 \
        -mtn "$BEXHOMA_TENANTS" -mtb container \
        -rst shared -rss 50Gi \
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_container_${BEXHOMA_TENANTS}_nolimit.log"

    bexperiments stop

    clean_logs
done






####################################################
###### MySQL TPC-C Multi-Tenant PVC No Limits ######
####################################################

BEXHOMA_DURATION=10
BEXHOMA_TARGET=65536
BEXHOMA_SF=10
BEXHOMA_THREADS=$((BEXHOMA_SF * 10))
BEXHOMA_CPU=40
BEXHOMA_RAM=200

for i in {1..10}; do
    # Set environment variables
    export BEXHOMA_TENANTS=$i
    tenants=$BEXHOMA_TENANTS
    sizeInGi=$((tenants * 20))
    export BEXHOMA_SIZE_ALL="${sizeInGi}Gi"
    # Calculate RAM and CPU per tenant (integers)
    ramPerTenant=$(( $BEXHOMA_RAM / tenants ))
    cpuPerTenant=$(( $BEXHOMA_CPU / tenants ))

    # Export environment variable
    export BEXHOMA_LIMIT_RAM="${ramPerTenant}Gi"
    export BEXHOMA_LIMIT_RAM_TOTAL="${BEXHOMA_RAM}Gi"

    # Run database mode
    python ./benchbase.py run -rc 0 -rr $BEXHOMA_LIMIT_RAM_TOTAL -lc 0 -lr $BEXHOMA_LIMIT_RAM_TOTAL -m -mc -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms MySQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
        -mtn "$BEXHOMA_TENANTS" -mtb database \
        -rst shared -rss "$BEXHOMA_SIZE_ALL" \
        </dev/null &> "$LOG_DIR/test_benchbase_run_mysql_tenants_database_${BEXHOMA_TENANTS}_nolimit.log"

    bexperiments stop

    # Run container mode (fixed 5Gi size)
    python ./benchbase.py run -rc 0 -rr $BEXHOMA_LIMIT_RAM -lc 0 -lr $BEXHOMA_LIMIT_RAM -m -mc -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms MySQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne 1,1 \
        -mtn "$BEXHOMA_TENANTS" -mtb container \
        -rst shared -rss 20Gi \
        </dev/null &> "$LOG_DIR/test_benchbase_run_mysql_tenants_container_${BEXHOMA_TENANTS}_nolimit.log"

    bexperiments stop

    clean_logs
done



####################################################
######### Benchbase TPC-C Multi-Tenant PVC #########
####################################################

BEXHOMA_DURATION=10
BEXHOMA_TARGET=65536
BEXHOMA_SF=10
BEXHOMA_THREADS=$((BEXHOMA_SF * 10))
BEXHOMA_CPU=40
BEXHOMA_RAM=200

for i in {1..10}; do
    # Set environment variables
    export BEXHOMA_TENANTS=$i
    tenants=$BEXHOMA_TENANTS
    sizeInGi=$((tenants * 20))
    export BEXHOMA_SIZE_ALL="${sizeInGi}Gi"
    # Calculate RAM and CPU per tenant (integers)
    ramPerTenant=$(( $BEXHOMA_RAM / tenants ))
    cpuPerTenant=$(( $BEXHOMA_CPU / tenants ))

    # Export environment variable
    export BEXHOMA_LIMIT_RAM="${ramPerTenant}Gi"
    export BEXHOMA_LIMIT_RAM_TOTAL="${BEXHOMA_RAM}Gi"

    # Optional: print results
    echo "RAM per total: $BEXHOMA_LIMIT_RAM_TOTAL"
    echo "CPU per total: $BEXHOMA_CPU"
    echo "RAM per tenant: $BEXHOMA_LIMIT_RAM"
    echo "CPU per tenant: ${cpuPerTenant}"

    # Run schema mode
    python ./benchbase.py run -rc $BEXHOMA_CPU -lc $BEXHOMA_CPU -rr $BEXHOMA_LIMIT_RAM_TOTAL -lr $BEXHOMA_LIMIT_RAM_TOTAL -m -mc -ma -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
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
    python ./benchbase.py run -rc $BEXHOMA_CPU -lc $BEXHOMA_CPU -rr $BEXHOMA_LIMIT_RAM_TOTAL -lr $BEXHOMA_LIMIT_RAM_TOTAL -m -mc -ma -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
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
    python ./benchbase.py run -rc $cpuPerTenant -lc $cpuPerTenant -rr $ramPerTenant -lr $ramPerTenant -m -mc -ma -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
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
##### Benchbase TPC-C Multi-Tenant PVC Loading #####
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
    python ./benchbase.py load -rc 2 -m -mc -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms PostgreSQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
        -mtn "$BEXHOMA_TENANTS" -mtb schema \
        -rst shared -rss "$BEXHOMA_SIZE_ALL" \
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_schema_${BEXHOMA_TENANTS}_load.log"

    bexperiments stop

    # Run database mode
    python ./benchbase.py load -rc 2 -m -mc -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms PostgreSQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
        -mtn "$BEXHOMA_TENANTS" -mtb database \
        -rst shared -rss "$BEXHOMA_SIZE_ALL" \
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_database_${BEXHOMA_TENANTS}_load.log"

    bexperiments stop

    # Run container mode (fixed 5Gi size)
    python ./benchbase.py load -rc 2 -m -mc -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms PostgreSQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne 1,1 \
        -mtn "$BEXHOMA_TENANTS" -mtb container \
        -rst shared -rss 20Gi \
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_container_${BEXHOMA_TENANTS}_load.log"

    bexperiments stop

    clean_logs
done








####################################################
## Benchbase TPC-C Multi-Tenant PVC Run preloaded ##
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
        -rst shared -rss "$BEXHOMA_SIZE_ALL" \
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_schema_${BEXHOMA_TENANTS}_db_load.log"

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
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_database_${BEXHOMA_TENANTS}_db_load.log"

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
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_container_${BEXHOMA_TENANTS}_db_load.log"

    bexperiments stop

    clean_logs
done





####################################################
## Benchbase TPC-C Multi-Tenant PVC Run new args ###
####################################################

BEXHOMA_DURATION=10
BEXHOMA_TARGET=65536
BEXHOMA_SF=10
BEXHOMA_THREADS=$((BEXHOMA_SF * 10))

for i in {1..10}; do
    # Set environment variables
    export BEXHOMA_TENANTS=$i # $((11-$i))
    tenants=$BEXHOMA_TENANTS
    sizeInGi=$((tenants * 20))
    export BEXHOMA_SIZE_ALL="${sizeInGi}Gi"
    # Calculate limit RAM per tenant
    ramPerTenant=$((480 / tenants))
    export BEXHOMA_LIMIT_RAM="${ramPerTenant}Gi"

    # For debugging/verification
    echo "TENANTS=$BEXHOMA_TENANTS SIZE=$BEXHOMA_SIZE_ALL LIMIT_RAM=$BEXHOMA_LIMIT_RAM"

    # Run schema mode
    python ./benchbase.py run -rc 2 -lr 480Gi -m -mc -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms PostgreSQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
        -mtn "$BEXHOMA_TENANTS" -mtb schema \
        -rst shared -rss "$BEXHOMA_SIZE_ALL" \
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_schema_${BEXHOMA_TENANTS}_args.log"

    bexperiments stop

    # Run database mode
    python ./benchbase.py run -rc 2 -lr 480Gi -m -mc -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms PostgreSQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
        -mtn "$BEXHOMA_TENANTS" -mtb database \
        -rst shared -rss "$BEXHOMA_SIZE_ALL" \
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_database_${BEXHOMA_TENANTS}_args.log"

    bexperiments stop

    # Run container mode (fixed 5Gi size)
    python ./benchbase.py run -rc 2 -lr $BEXHOMA_LIMIT_RAM -m -mc -tb $BEXHOMA_TARGET -sf $BEXHOMA_SF -sd $BEXHOMA_DURATION \
        --dbms PostgreSQL \
        -rnn "$BEXHOMA_NODE_SUT" \
        -rnl "$BEXHOMA_NODE_LOAD" \
        -rnb "$BEXHOMA_NODE_BENCHMARK" \
        -nlp 1 -nlt $BEXHOMA_THREADS -nbp 1 -nbt $BEXHOMA_THREADS \
        -ne 1,1 \
        -mtn "$BEXHOMA_TENANTS" -mtb container \
        -rst shared -rss 20Gi \
        </dev/null &> "$LOG_DIR/test_benchbase_run_postgresql_tenants_container_${BEXHOMA_TENANTS}_args.log"

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




####################################################
######### TPC-H Multi-Tenant Loading only ##########
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
    nohup python tpch.py load -rc 2 -lr 480Gi -m -mc -rcp -shq -t 3600 -nr $BEXHOMA_NUM_RUN \
      -mtn $BEXHOMA_TENANTS -mtb schema \
      -sf $BEXHOMA_SF \
      --dbms PostgreSQL \
      -ii -ic -is \
      -nlp $BEXHOMA_TENANTS -nbp 1 \
      -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
      -rst shared -rss "$BEXHOMA_SIZE_ALL" \
      </dev/null &> "$LOG_DIR/test_tpch_run_postgresql_tenants_schema_${BEXHOMA_TENANTS}_load.log"

    bexperiments stop

    # Run database mode
    nohup python tpch.py load -rc 2 -lr 480Gi -m -mc -rcp -shq -t 3600 -nr $BEXHOMA_NUM_RUN \
      -mtn $BEXHOMA_TENANTS -mtb database \
      -sf $BEXHOMA_SF \
      --dbms PostgreSQL \
      -ii -ic -is \
      -nlp $BEXHOMA_TENANTS -nbp 1 \
      -ne "$BEXHOMA_TENANTS,$BEXHOMA_TENANTS" \
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
      -rst shared -rss "$BEXHOMA_SIZE_ALL" \
      </dev/null &> "$LOG_DIR/test_tpch_run_postgresql_tenants_database_${BEXHOMA_TENANTS}_load.log"

    bexperiments stop

    # Run container mode (fixed 50Gi size)
    nohup python tpch.py load -rc 2 -lr $BEXHOMA_LIMIT_RAM -m -mc -rcp -shq -t 3600 -nr $BEXHOMA_NUM_RUN \
      -mtn $BEXHOMA_TENANTS -mtb container \
      -sf $BEXHOMA_SF \
      --dbms PostgreSQL \
      -ii -ic -is \
      -nlp 1 -nbp 1 \
      -ne 1,1 \
      -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
      -rst shared -rss 50Gi \
      </dev/null &> "$LOG_DIR/test_tpch_run_postgresql_tenants_container_${BEXHOMA_TENANTS}_load.log"

    bexperiments stop

    clean_logs
done



####################################################
######### TPC-H Multi-Tenant Run preloaded #########
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
      </dev/null &> "$LOG_DIR/test_tpch_run_postgresql_tenants_schema_${BEXHOMA_TENANTS}_db_load.log"

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
      </dev/null &> "$LOG_DIR/test_tpch_run_postgresql_tenants_database_${BEXHOMA_TENANTS}_db_load.log"

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
      </dev/null &> "$LOG_DIR/test_tpch_run_postgresql_tenants_container_${BEXHOMA_TENANTS}_db_load.log"

    bexperiments stop

    clean_logs
done




###########################################
############## Clean Folder ###############
###########################################


clean_logs
