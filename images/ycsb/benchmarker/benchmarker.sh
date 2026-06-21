#!/bin/bash

######################## Start timing ########################
bexhoma_start_epoch=$(date -u +%s)
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "$DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS

######################## Show general parameters ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_EXPERIMENT:$BEXHOMA_EXPERIMENT"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "BEXHOMA_DBMS:$BEXHOMA_DBMS"
echo "BEXHOMA_DBMS_TYPE:$BEXHOMA_DBMS_TYPE"

######################## Wait for synched starting time ########################
echo "benchmark started at $BEXHOMA_TIME_NOW"
echo "benchmark should wait until $BEXHOMA_TIME_START"
if test "$BEXHOMA_TIME_START" != "0"
then
    benchmark_start_epoch=$(date -u -d "$BEXHOMA_TIME_NOW" +%s)
    echo "that is $benchmark_start_epoch"

    TZ=UTC printf -v current_epoch '%(%Y-%m-%d %H:%M:%S)T\n' -1
    echo "now is $current_epoch"
    current_epoch=$(date -u +%s)
    echo "that is $current_epoch"
    target_epoch=$(date -u -d "$BEXHOMA_TIME_START" +%s)
    echo "wait until $BEXHOMA_TIME_START"
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
BEXHOMA_CHILD="$(redis-cli -h 'bexhoma-messagequeue' lpop bexhoma-benchmarker-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
if [ -z "$BEXHOMA_CHILD" ]
then
    echo "No entry found in message queue. I assume this is the first child."
    BEXHOMA_CHILD=1
else
    echo "Found entry number $BEXHOMA_CHILD in message queue."
fi

######################## Read per-pod config from Redis ########################
BEXHOMA_POD_CONFIG_KEY="bexhoma-benchmarker-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-config-$BEXHOMA_CHILD"
echo "Querying per-pod config at $BEXHOMA_POD_CONFIG_KEY"
BEXHOMA_POD_CONFIG_JSON="$(redis-cli -h 'bexhoma-messagequeue' get "$BEXHOMA_POD_CONFIG_KEY")"
if [ -z "$BEXHOMA_POD_CONFIG_JSON" ] || [ "$BEXHOMA_POD_CONFIG_JSON" = "nil" ]; then
    echo "No per-pod config found in Redis."
else
    eval "$(echo "$BEXHOMA_POD_CONFIG_JSON" \
      | tr -d '{}' \
      | tr ',' '\n' \
      | awk 'BEGIN{FS="\""} NF>=4 && $2!="" {print "export BEXHOMA_POD_"$2"=\""$4"\""; print "echo \"BEXHOMA_POD_"$2"="$4"\""}')"
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
OPERATIONS_TOTAL=$(($YCSB_OPERATIONS*$BEXHOMA_NUM_PODS))
# for loading phase
ROW_PART=$(($YCSB_ROWS/$BEXHOMA_NUM_PODS))
ROW_START=$(($YCSB_ROWS/$BEXHOMA_NUM_PODS*($BEXHOMA_CHILD-1)))
# for benchmarking phase - workload D and E, we again insert 5% new rows
ROWS_TO_INSERT=$(awk "BEGIN {print 0.05*$OPERATIONS_TOTAL}")
ROW_PART_AFTER_LOADING=$(($ROWS_TO_INSERT/$BEXHOMA_NUM_PODS))
ROW_START_AFTER_LOADING=$(($ROWS_TO_INSERT/$BEXHOMA_NUM_PODS*($BEXHOMA_CHILD-1)+$YCSB_ROWS))
# if new rows are to be inserted in benchmark, too
ROWS_AFTER_BENCHMARK=$((ROW_START_AFTER_LOADING+ROW_PART_AFTER_LOADING))

# benchmarking uses the complete key range so all parallel pods cover the full dataset
ROW_PART=$YCSB_ROWS
ROW_START=0

######################## Wait until all pods of job are ready ########################
echo "Decrementing job counter bexhoma-benchmarker-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
redis-cli -h 'bexhoma-messagequeue' decr "bexhoma-benchmarker-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
while : ; do
    PODS_MISSING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-benchmarker-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
    echo "Pods still missing in job: $PODS_MISSING"
    if [[ "$PODS_MISSING" =~ ^-?[0-9]+$ ]] && test "$PODS_MISSING" -le 0
    then
        echo "OK, all pods in job are ready."
        break
    else
        sleep 1
    fi
done

######################## Wait until all pods of round are ready ########################
echo "Decrementing round counter bexhoma-benchmarker-podcount-round-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_CLIENT-$BEXHOMA_CONFIGURATION-$BEXHOMA_EXPERIMENT"
redis-cli -h 'bexhoma-messagequeue' decr "bexhoma-benchmarker-podcount-round-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_CLIENT-$BEXHOMA_CONFIGURATION-$BEXHOMA_EXPERIMENT"
while : ; do
    PODS_MISSING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-benchmarker-podcount-round-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_CLIENT-$BEXHOMA_CONFIGURATION-$BEXHOMA_EXPERIMENT)"
    echo "Pods still missing in round: $PODS_MISSING"
    if [[ "$PODS_MISSING" =~ ^-?[0-9]+$ ]] && test "$PODS_MISSING" -le 0
    then
        echo "OK, all pods in round are ready."
        break
    else
        sleep 1
    fi
done

######################## Wait until all pods of experiment are ready ########################
if [ "$BEXHOMA_TENANT_BY" = "container" ]; then
    echo "Decrementing experiment counter bexhoma-benchmarker-podcount-exp-$BEXHOMA_EXPERIMENT"
    redis-cli -h 'bexhoma-messagequeue' decr "bexhoma-benchmarker-podcount-exp-$BEXHOMA_EXPERIMENT"
    while : ; do
        PODS_MISSING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-benchmarker-podcount-exp-$BEXHOMA_EXPERIMENT)"
        echo "Pods still missing in experiment: $PODS_MISSING"
        if [[ "$PODS_MISSING" =~ ^-?[0-9]+$ ]] && test "$PODS_MISSING" -le 0
        then
            echo "OK, all pods in experiment are ready."
            break
        else
            sleep 1
        fi
    done
fi

######################## Show more parameters ########################
echo "BEXHOMA_CHILD $BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS $BEXHOMA_NUM_PODS"
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
echo "YCSB_INSERTORDER:$YCSB_INSERTORDER"
echo "YCSB_MAX_EXECUTION:$YCSB_MAX_EXECUTION"

######################## Generate driver file ########################
# Redis or JDBC
#redis.cluster=false  # Set to true if using Redis Cluster
#redis.pipeline=true  # Enable pipelining for performance
#redis.pipeline.maxsize=50  # Adjust based on workload
if [[ "$YCSB_USE_HOSTLIST" == "1" || "$YCSB_USE_HOSTLIST" == "true" ]]; then
    echo "YCSB_USE_HOSTLIST is enabled"
    URL=$BEXHOMA_URL_LIST
else
    echo "YCSB_USE_HOSTLIST is not enabled"
    URL=$BEXHOMA_URL
fi

if [[ "$BEXHOMA_DBMS_TYPE" == "redis" || "$BEXHOMA_DBMS_TYPE" == "redis-cluster" ]]; then
    echo "BEXHOMA_DBMS_TYPE is set to Redis"
    echo "redis.host=$BEXHOMA_HOST
redis.port=$BEXHOMA_PORT
redis.passwd=$BEXHOMA_PASSWORD
" > db.properties
else
    echo "db.driver=$BEXHOMA_DRIVER
db.url=$URL
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
sed -i "s/YCSB_INSERTORDER/$YCSB_INSERTORDER/" $FILENAME

cat $FILENAME

######################## Start measurement of time ########################
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"
bexhoma_start_epoch=$(date -u +%s)

######################## Build optional flags ###################
if [ "${YCSB_MAX_EXECUTION:-0}" -gt 0 ]; then
    YCSB_MAXEXECTIME_FLAG="-p maxexecutiontime=$YCSB_MAX_EXECUTION"
else
    YCSB_MAXEXECTIME_FLAG=""
fi

######################## Execute workload ###################
# to force "new" method of measurement: -p measurementtype=hdrhistogram
if [[ "$BEXHOMA_DBMS_TYPE" == "redis" ]]; then
    if test $YCSB_STATUS -ne 0
    then
        # report status
        time bin/ycsb run redis -P $FILENAME -P db.properties -cp jars/$BEXHOMA_JAR $YCSB_MAXEXECTIME_FLAG -s
    else
        time bin/ycsb run redis -P $FILENAME -P db.properties -cp jars/$BEXHOMA_JAR $YCSB_MAXEXECTIME_FLAG
    fi
elif [[ "$BEXHOMA_DBMS_TYPE" == "redis-cluster" ]]; then
    if test $YCSB_STATUS -ne 0
    then
        # report status
        time bin/ycsb run redis -P $FILENAME -P db.properties -cp jars/$BEXHOMA_JAR -p redis.cluster=true $YCSB_MAXEXECTIME_FLAG -s
    else
        time bin/ycsb run redis -P $FILENAME -P db.properties -cp jars/$BEXHOMA_JAR -p redis.cluster=true $YCSB_MAXEXECTIME_FLAG
    fi
else
    if test $YCSB_STATUS -ne 0
    then
        # report status
        time bin/ycsb run jdbc -P $FILENAME -P db.properties -cp jars/$BEXHOMA_JAR $YCSB_MAXEXECTIME_FLAG -s
    else
        time bin/ycsb run jdbc -P $FILENAME -P db.properties -cp jars/$BEXHOMA_JAR $YCSB_MAXEXECTIME_FLAG
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
