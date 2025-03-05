#!/bin/bash

######################## Start timing ########################
bexhoma_start_epoch=$(date -u +%s)
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "$DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS

######################## Show general parameters ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_DBMS:$BEXHOMA_DBMS"

######################## Wait for synched starting time ########################
echo "benchmark started at $DBMSBENCHMARKER_NOW"
echo "benchmark should wait until $DBMSBENCHMARKER_START"
if test "$DBMSBENCHMARKER_START" != "0"
then
    benchmark_start_epoch=$(date -u -d "$DBMSBENCHMARKER_NOW" +%s)
    echo "that is $benchmark_start_epoch"

    TZ=UTC printf -v current_epoch '%(%Y-%m-%d %H:%M:%S)T\n' -1 
    echo "now is $current_epoch"
    current_epoch=$(date -u +%s)
    echo "that is $current_epoch"
    target_epoch=$(date -u -d "$DBMSBENCHMARKER_START" +%s)
    echo "wait until $DBMSBENCHMARKER_START"
    echo "that is $target_epoch"
    sleep_seconds=$(( $target_epoch - $current_epoch ))
    echo "that is wait $sleep_seconds seconds"

    if test $sleep_seconds -lt 0
    then
        echo "start time has already passed"
        exit 0
    fi

    sleep $sleep_seconds
    bexhoma_start_epoch=$(date -u +%s)
else
    echo "ignore that start time"
fi

######################## Make sure result folder exists ########################
mkdir -p /results/$BEXHOMA_EXPERIMENT

######################## Get number of client in job queue ########################
echo "Querying message queue bexhoma-benchmarker-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
# redis-cli -h 'bexhoma-messagequeue' lpop "bexhoma-benchmarker-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
CHILD="$(redis-cli -h 'bexhoma-messagequeue' lpop bexhoma-benchmarker-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
if [ -z "$CHILD" ]
then
    echo "No entry found in message queue. I assume this is the first child."
    CHILD=1
else
    echo "Found entry number $CHILD in message queue."
fi

######################## Adjust parameter to job number ########################
if [ -z "$YCSB_ROWS" ]
then
    YCSB_ROWS=$((SF*100000))
fi

if [ -z "$YCSB_OPERATIONS" ]
then
    YCSB_OPERATIONS=$((SF*100000))
fi

######################## Generate workflow ########################
# for parallel benchmarking pods
OPERATIONS_TOTAL=$(($YCSB_OPERATIONS*$NUM_PODS))
# for loading phase
ROW_PART=$(($YCSB_ROWS/$NUM_PODS))
ROW_START=$(($YCSB_ROWS/$NUM_PODS*($CHILD-1)))
# for benchmarking phase - workload E, we again insert 5% new rows
#ROWS_TO_INSERT=$(awk "BEGIN {print 0.05*$OPERATIONS_TOTAL}")
# assume 100% of operations are INSERTs
ROWS_TO_INSERT=$OPERATIONS_TOTAL
ROW_PART_AFTER_LOADING=$(($ROWS_TO_INSERT/$NUM_PODS))
ROW_START_AFTER_LOADING=$(($ROWS_TO_INSERT/$NUM_PODS*($CHILD-1)+$YCSB_ROWS))
# if new rows are to be inserted in benchmark, too
ROWS_AFTER_BENCHMARK=$((ROW_START_AFTER_LOADING+ROW_PART_AFTER_LOADING))

#### execution of workload known complete key range from 0 to (all) rows
ROW_PART=$YCSB_ROWS
ROW_START=0

######################## Wait until all pods of job are ready ########################
if test "$BEXHOMA_SYNCH_LOAD" != "0"
then
    echo "Querying counter bexhoma-benchmarker-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
    # add this pod to counter
    redis-cli -h 'bexhoma-messagequeue' incr "bexhoma-benchmarker-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
    # wait for number of pods to be as expected
    while : ; do
        PODS_RUNNING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-benchmarker-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
        echo "Found $PODS_RUNNING / $NUM_PODS running pods"
        if [[ "$PODS_RUNNING" =~ ^[0-9]+$ ]]
        then
            echo "PODS_RUNNING contains a number."
        else
            echo "PODS_RUNNING does not contain a number."
            exit 0
        fi
        if  test "$PODS_RUNNING" == $NUM_PODS
        then
            echo "OK, found $NUM_PODS ready pods."
            break
        elif test "$PODS_RUNNING" -gt $NUM_PODS
        then
            echo "Too many pods! Restart occured?"
            exit 0
        else
            echo "We have to wait"
            sleep 1
        fi
    done
else
    echo "Start immediately without waiting for other pods"
fi

######################## Show more parameters ########################
echo "CHILD $CHILD"
echo "NUM_PODS $NUM_PODS"
echo "SF $SF"
echo "YCSB_ROWS $YCSB_ROWS"
echo "ROW_PART $ROW_PART"
echo "ROW_START $ROW_START"
echo "ROWS_TO_INSERT $ROWS_TO_INSERT"
echo "ROWS_AFTER_BENCHMARK $ROWS_AFTER_BENCHMARK"
echo "ROW_PART_AFTER_LOADING $ROW_PART_AFTER_LOADING"
echo "ROW_START_AFTER_LOADING $ROW_START_AFTER_LOADING"
echo "OPERATIONS_TOTAL $OPERATIONS_TOTAL"
echo "YCSB_OPERATIONS $YCSB_OPERATIONS"
echo "YCSB_THREADCOUNT $YCSB_THREADCOUNT"
echo "YCSB_TARGET $YCSB_TARGET"
echo "YCSB_WORKLOAD $YCSB_WORKLOAD"
echo "YCSB_BATCHSIZE:$YCSB_BATCHSIZE"
echo "YCSB_MEASUREMENT_TYPE:$YCSB_MEASUREMENT_TYPE"

######################## Generate driver file ########################
# Redis or JDBC
#redis.cluster=false  # Set to true if using Redis Cluster
#redis.pipeline=true  # Enable pipelining for performance
#redis.pipeline.maxsize=50  # Adjust based on workload
if [[ "$BEXHOMA_DBMS" == "redis" ]]; then
    echo "BEXHOMA_DBMS is set to Redis"
    echo "redis.host=$BEXHOMA_HOST
redis.port=$BEXHOMA_PORT
redis.passwd=$BEXHOMA_PASSWORD
" > db.properties
else
#    echo "BEXHOMA_DRIVER has a different value or is empty"
    echo "db.driver=$BEXHOMA_DRIVER
db.url=$BEXHOMA_URL
db.user=$BEXHOMA_USER
db.passwd=$BEXHOMA_PASSWORD
" > db.properties
fi


if [ -z "$YCSB_BATCHSIZE" ]
then
    echo "YCSB_BATCHSIZE is empty"
else
    echo "YCSB_BATCHSIZE is NOT empty"
    echo "db.batchsize=$YCSB_BATCHSIZE" >> db.properties
    echo "jdbc.batchupdateapi=true" >> db.properties
fi

cat db.properties

######################## Generate workflow file ########################
FILENAME_TEMPLATE="workloads/workload$YCSB_WORKLOAD"
FILENAME=/tmp/workload
cp $FILENAME_TEMPLATE $FILENAME
echo "FILENAME $FILENAME"
echo "FILENAME_TEMPLATE $FILENAME_TEMPLATE"

sed -i "s/ROWS_AFTER_BENCHMARK/$ROWS_AFTER_BENCHMARK/" $FILENAME
sed -i "s/ROW_START_AFTER_LOADING/$ROW_START_AFTER_LOADING/" $FILENAME
sed -i "s/ROW_PART_AFTER_LOADING/$ROW_PART_AFTER_LOADING/" $FILENAME
sed -i "s/YCSB_ROWS/$YCSB_ROWS/" $FILENAME
sed -i "s/OPERATIONS_TOTAL/$OPERATIONS_TOTAL/" $FILENAME
sed -i "s/YCSB_OPERATIONS/$YCSB_OPERATIONS/" $FILENAME
sed -i "s/ROW_START/$ROW_START/" $FILENAME
sed -i "s/ROW_PART/$ROW_PART/" $FILENAME
sed -i "s/YCSB_THREADCOUNT/$YCSB_THREADCOUNT/" $FILENAME
sed -i "s/YCSB_TARGET/$YCSB_TARGET/" $FILENAME
sed -i "s/YCSB_STATUS_INTERVAL/$YCSB_STATUS_INTERVAL/" $FILENAME
sed -i "s/YCSB_MEASUREMENT_TYPE/$YCSB_MEASUREMENT_TYPE/" $FILENAME

echo "# Yahoo! Cloud System Benchmark
# Workload A: Update heavy workload
#   Application example: Session store recording recent actions
#                        
#   Read/update ratio: 50/50
#   Request distribution: zipfian

recordcount=$YCSB_ROWS
operationcount=$YCSB_OPERATIONS
workload=site.ycsb.workloads.CoreWorkload

readallfields=true

readproportion=0.5
updateproportion=0.5
scanproportion=0
insertproportion=0

requestdistribution=zipfian

status.interval=$YCSB_STATUS_INTERVAL

insertstart=$ROW_START
insertcount=$ROW_PART

threadcount=$YCSB_THREADCOUNT
target=$YCSB_TARGET
" > workload_test

#cat workload_test
cat $FILENAME

######################## Start measurement of time ########################
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"
bexhoma_start_epoch=$(date -u +%s)

######################## Execute workload ###################
if [[ "$BEXHOMA_DBMS" == "redis" ]]; then
    if test $YCSB_STATUS -ne 0
    then
        # report status
        time bin/ycsb run jdbc -P $FILENAME -P db.properties -cp jars/$BEXHOMA_JAR -s
    else
        time bin/ycsb run jdbc -P $FILENAME -P db.properties -cp jars/$BEXHOMA_JAR
    fi
else
    if test $YCSB_STATUS -ne 0
    then
        # report status
        time bin/ycsb run jdbc -P $FILENAME -P db.properties -cp jars/$BEXHOMA_JAR -s
    else
        time bin/ycsb run jdbc -P $FILENAME -P db.properties -cp jars/$BEXHOMA_JAR
    fi
fi

######################## End time measurement ###################
SECONDS_END=$SECONDS
echo "End $SECONDS_END seconds"

DURATION=$((SECONDS_END-SECONDS_START))
echo "Duration $DURATION seconds"

######################## Show timing information ###################
echo "Benchmarking done"

DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "$DATEANDTIME"

SECONDS_END_SCRIPT=$SECONDS
DURATION_SCRIPT=$((SECONDS_END_SCRIPT-SECONDS_START_SCRIPT))
echo "Duration $DURATION_SCRIPT seconds"
echo "BEXHOMA_DURATION:$DURATION_SCRIPT"

bexhoma_end_epoch=$(date -u +%s)
echo "BEXHOMA_START:$bexhoma_start_epoch"
echo "BEXHOMA_END:$bexhoma_end_epoch"

######################## Exit successfully ###################
exit 0
