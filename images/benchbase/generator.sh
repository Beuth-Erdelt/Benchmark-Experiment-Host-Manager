#!/bin/bash

######################## Start timing ########################
bexhoma_start_epoch=$(date -u +%s)
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "$DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS

######################## Show general parameters ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
echo "BEXHOMA_SCHEMA:$BEXHOMA_SCHEMA"
echo "BEXHOMA_VOLUME:$BEXHOMA_VOLUME"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_DBMS:$BEXHOMA_DBMS"
echo "BEXHOMA_TENANT_NUM:$BEXHOMA_TENANT_NUM"
echo "BEXHOMA_TENANT_BY:$BEXHOMA_TENANT_BY"

######################## Get number of client in job queue ########################
echo "Querying message queue bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
# redis-cli -h 'bexhoma-messagequeue' lpop "bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
BEXHOMA_CHILD="$(redis-cli -h 'bexhoma-messagequeue' lpop bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
if [ -z "$BEXHOMA_CHILD" ]
then
    echo "No entry found in message queue. I assume this is the first child."
    BEXHOMA_CHILD=1
else
    echo "Found entry number $BEXHOMA_CHILD in message queue."
fi
#if [ -z "$BEXHOMA_CHILD" ]
#then
#	BEXHOMA_CHILD=1
#fi


############ Show more parameters ############
echo "BEXHOMA_CHILD $BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS $BEXHOMA_NUM_PODS"
echo "SF $SF"
echo "BENCHBASE_BENCH $BENCHBASE_BENCH"
echo "BENCHBASE_PROFILE $BENCHBASE_PROFILE"
echo "BENCHBASE_TARGET $BENCHBASE_TARGET"
echo "BENCHBASE_TIME $BENCHBASE_TIME"
echo "BENCHBASE_TERMINALS $BENCHBASE_TERMINALS"
echo "BENCHBASE_BATCHSIZE $BENCHBASE_BATCHSIZE"
echo "BENCHBASE_CREATE_SCHEMA $BENCHBASE_CREATE_SCHEMA"
echo "BENCHBASE_NEWCONNPERTXN $BENCHBASE_NEWCONNPERTXN"

######################## Multi-Tenant parameters ########################
BEXHOMA_NUM_PODS_TMP=$BEXHOMA_NUM_PODS
if [ "$BEXHOMA_TENANT_BY" = "schema" ]; then
    echo "BEXHOMA_TENANT_BY is schema"
    BEXHOMA_NUM_PODS=1
    BEXHOMA_SCHEMA="tenant_$((BEXHOMA_CHILD - 1))"
    echo "BEXHOMA_SCHEMA:$BEXHOMA_SCHEMA"
elif [ "$BEXHOMA_TENANT_BY" = "database" ]; then
    echo "BEXHOMA_TENANT_BY is database"
    BEXHOMA_NUM_PODS=1
    BEXHOMA_DATABASE="tenant_$((BEXHOMA_CHILD - 1))"
else
    echo "BEXHOMA_TENANT_BY is not set"
fi
######################## Multi-Tenant parameters ########################
BEXHOMA_NUM_PODS=$BEXHOMA_NUM_PODS_TMP

######################## Wait until all pods of experiment are ready ########################
if [ "$BEXHOMA_TENANT_BY" = "container" ]; then
    echo "Querying counter bexhoma-benchmarker-podcount-$BEXHOMA_EXPERIMENT"
    # add this pod to counter
    redis-cli -h 'bexhoma-messagequeue' incr "bexhoma-benchmarker-podcount-$BEXHOMA_EXPERIMENT"
    # wait for number of pods to be as expected
    while : ; do
        PODS_RUNNING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-benchmarker-podcount-$BEXHOMA_EXPERIMENT)"
        echo "Found $PODS_RUNNING / $BEXHOMA_NUM_PODS_TOTAL running pods"
        if [[ "$PODS_RUNNING" =~ ^[0-9]+$ ]]
        then
            echo "PODS_RUNNING contains a number."
        else
            echo "PODS_RUNNING does not contain a number."
            exit 0
        fi
        if  test "$PODS_RUNNING" == $BEXHOMA_NUM_PODS_TOTAL
        then
            echo "OK, found $BEXHOMA_NUM_PODS_TOTAL ready pods."
            break
        elif test "$PODS_RUNNING" -gt $BEXHOMA_NUM_PODS_TOTAL
        then
            echo "Too many pods! Restart occured?"
            exit 0
        else
            echo "We have to wait"
            sleep 1
        fi
    done
fi

############ Start measurement of time of execution ############
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"
bexhoma_start_epoch=$(date -u +%s)

######################## Benchmark Config File ###################
if [ "$BENCHBASE_BENCH" == "tpcc" ]; then
    FILENAME=/tmp/config/$BENCHBASE_PROFILE/sample_tpcc_config.xml
elif [ "$BENCHBASE_BENCH" == "twitter" ]; then
    FILENAME=/tmp/config/$BENCHBASE_PROFILE/sample_twitter_config.xml
elif [ "$BENCHBASE_BENCH" == "chbenchmark" ]; then
    FILENAME=/tmp/config/$BENCHBASE_PROFILE/sample_chbenchmark_config.xml
	BENCHBASE_BENCH="tpcc,chbenchmark"
elif [ "$BENCHBASE_BENCH" == "ycsb" ]; then
    FILENAME=/tmp/config/$BENCHBASE_PROFILE/sample_ycsb_config.xml
else
    echo "Unknown benchmark"
    exit 0
fi

######################## Show workload file ###################
echo "FILENAME $FILENAME"

######################## Remove schema parameter from PGBouncer URL ###################
if [[ "$BEXHOMA_DBMS" == "PGBouncer" ]]; then
	sed -i "s/&amp;currentSchema=BEXHOMA_SCHEMA/" $FILENAME
fi


######################## Replace parameters in workload file ###################
if [[ "$BENCHBASE_BENCH" == "ycsb" && "$BENCHBASE_YCSB_WORKLOAD" == "a" ]]; then
    BENCHBASE_YCSB_WEIGHTS=50,0,0,50,0,0
elif [[ "$BENCHBASE_BENCH" == "ycsb" && "$BENCHBASE_YCSB_WORKLOAD" == "b" ]]; then
    BENCHBASE_YCSB_WEIGHTS=95,0,0,5,0,0
elif [[ "$BENCHBASE_BENCH" == "ycsb" && "$BENCHBASE_YCSB_WORKLOAD" == "c" ]]; then
    BENCHBASE_YCSB_WEIGHTS=100,0,0,0,0,0
elif [[ "$BENCHBASE_BENCH" == "ycsb" && "$BENCHBASE_YCSB_WORKLOAD" == "d" ]]; then
    BENCHBASE_YCSB_WEIGHTS=95,5,0,0,0,0
elif [[ "$BENCHBASE_BENCH" == "ycsb" && "$BENCHBASE_YCSB_WORKLOAD" == "e" ]]; then
    BENCHBASE_YCSB_WEIGHTS=0,5,95,0,0,0
elif [[ "$BENCHBASE_BENCH" == "ycsb" && "$BENCHBASE_YCSB_WORKLOAD" == "f" ]]; then
    BENCHBASE_YCSB_WEIGHTS=50,0,0,0,0,50
fi

echo "FILENAME $FILENAME"

sed -i "s/BEXHOMA_HOST/$BEXHOMA_HOST/" $FILENAME
sed -i "s/BEXHOMA_PORT/$BEXHOMA_PORT/" $FILENAME
sed -i "s/BEXHOMA_USER/$BEXHOMA_USER/" $FILENAME
sed -i "s/BEXHOMA_PASSWORD/$BEXHOMA_PASSWORD/" $FILENAME
sed -i "s/BEXHOMA_DATABASE/$BEXHOMA_DATABASE/" $FILENAME
sed -i "s/BEXHOMA_SCHEMA/$BEXHOMA_SCHEMA/" $FILENAME
sed -i "s/BENCHBASE_TIME/$BENCHBASE_TIME/" $FILENAME
sed -i "s/BENCHBASE_TARGET/$BENCHBASE_TARGET/" $FILENAME
sed -i "s/BEXHOMA_SF/$SF/" $FILENAME
sed -i "s/BENCHBASE_BATCHSIZE/$BENCHBASE_BATCHSIZE/" $FILENAME
sed -i "s/BENCHBASE_TERMINALS/$BENCHBASE_TERMINALS/" $FILENAME
sed -i "s/BENCHBASE_ISOLATION/$BENCHBASE_ISOLATION/" $FILENAME
sed -i "s/BENCHBASE_NEWCONNPERTXN/$BENCHBASE_NEWCONNPERTXN/" $FILENAME
sed -i "s/BENCHBASE_YCSB_WEIGHTS/$BENCHBASE_YCSB_WEIGHTS/" $FILENAME

cat $FILENAME

ls -lh

pwd

######################## Execute workload ###################
if echo "$BENCHBASE_STATUS_INTERVAL" | grep -qE '^[0-9]+$'; then
    echo "Benchbase dump status"
	time sh ./entrypoint.sh run --bench $BENCHBASE_BENCH -c $FILENAME --create=$BENCHBASE_CREATE_SCHEMA --load=true --execute=false  --interval-monitor $BENCHBASE_STATUS_INTERVAL
else
	time sh ./entrypoint.sh run --bench $BENCHBASE_BENCH -c $FILENAME --create=$BENCHBASE_CREATE_SCHEMA --load=true --execute=false
fi



######################## End time measurement ###################
SECONDS_END=$SECONDS
echo "End $SECONDS_END seconds"

DURATION=$((SECONDS_END-SECONDS_START))
echo "Duration $DURATION seconds"

######################## Show result files ###################
ls -lh /benchbase/results

######################## Show result summary ###################
echo "####BEXHOMA####"
cat /benchbase/results/*.summary.json
echo "####BEXHOMA####"

######################## Show timing information ###################
echo "Generating done"

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
