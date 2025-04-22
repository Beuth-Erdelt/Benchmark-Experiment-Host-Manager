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

######################## Wait until all pods of job are ready ########################
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

######################## Show more parameters ########################
echo "CHILD $CHILD"
echo "NUM_PODS $NUM_PODS"
echo "SF $SF"
echo "BENCHBASE_BENCH $BENCHBASE_BENCH"
echo "BENCHBASE_PROFILE $BENCHBASE_PROFILE"
echo "BENCHBASE_TARGET $BENCHBASE_TARGET"
echo "BENCHBASE_TIME $BENCHBASE_TIME"
echo "BENCHBASE_TERMINALS $BENCHBASE_TERMINALS"
echo "BENCHBASE_BATCHSIZE $BENCHBASE_BATCHSIZE"
echo "BENCHBASE_KEY_AND_THINK $BENCHBASE_KEY_AND_THINK"
echo "BENCHBASE_NEWCONNPERTXN $BENCHBASE_NEWCONNPERTXN"


######################## Start measurement of time of execution ########################
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"
bexhoma_start_epoch=$(date -u +%s)

######################## TPC-C ###################
if [ "$BENCHBASE_BENCH" = "tpcc" ]; then
	#FILENAME=/benchbase/profiles/postgres/config/postgres/sample_tpcc_config.xml
	FILENAME=/tmp/config/$BENCHBASE_PROFILE/sample_tpcc_config.xml
fi

######################## Twitter ###################
if [ "$BENCHBASE_BENCH" = "twitter" ]; then
    #FILENAME=/benchbase/profiles/postgres/config/postgres/sample_tpcc_config.xml
    FILENAME=/tmp/config/$BENCHBASE_PROFILE/sample_twitter_config.xml
fi

######################## CHBenchmark ###################
if [ "$BENCHBASE_BENCH" = "chbenchmark" ]; then
    #FILENAME=/benchbase/profiles/postgres/config/postgres/sample_tpcc_config.xml
    FILENAME=/tmp/config/$BENCHBASE_PROFILE/sample_chbenchmark_config.xml
fi

######################## Replace parameters in workload file ###################
echo "FILENAME $FILENAME"

sed -i "s/BEXHOMA_HOST/$BEXHOMA_HOST/" $FILENAME
sed -i "s/BEXHOMA_PORT/$BEXHOMA_PORT/" $FILENAME
sed -i "s/BEXHOMA_USER/$BEXHOMA_USER/" $FILENAME
sed -i "s/BEXHOMA_PASSWORD/$BEXHOMA_PASSWORD/" $FILENAME
sed -i "s/BEXHOMA_DATABASE/$BEXHOMA_DATABASE/" $FILENAME
sed -i "s/BENCHBASE_TIME/$BENCHBASE_TIME/" $FILENAME
sed -i "s/BENCHBASE_TARGET/$BENCHBASE_TARGET/" $FILENAME
sed -i "s/BEXHOMA_SF/$SF/" $FILENAME
sed -i "s/BENCHBASE_BATCHSIZE/$BENCHBASE_BATCHSIZE/" $FILENAME
sed -i "s/BENCHBASE_TERMINALS/$BENCHBASE_TERMINALS/" $FILENAME
sed -i "s/BENCHBASE_ISOLATION/$BENCHBASE_ISOLATION/" $FILENAME
sed -i "s/BENCHBASE_NEWCONNPERTXN/$BENCHBASE_NEWCONNPERTXN/" $FILENAME

if [ "$BENCHBASE_KEY_AND_THINK" = "true" ]; then
    sed -i 's/<!--<preExecutionWait>/<preExecutionWait>/g' $FILENAME
    sed -i 's/preExecutionWait>-->/preExecutionWait>/g' $FILENAME
    sed -i 's/<!--<postExecutionWait>/<postExecutionWait>/g' $FILENAME
    sed -i 's/postExecutionWait>-->/postExecutionWait>/g' $FILENAME
fi

cat $FILENAME

ls -lh

pwd

######################## Execute workload ###################
if echo "$BENCHBASE_STATUS_INTERVAL" | grep -qE '^[0-9]+$'; then
    echo "Benchbase dump status"
    time sh ./entrypoint.sh run --bench $BENCHBASE_BENCH -c $FILENAME --create=false --load=false --execute=true --interval-monitor $BENCHBASE_STATUS_INTERVAL
else
    time sh ./entrypoint.sh run --bench $BENCHBASE_BENCH -c $FILENAME --create=false --load=false --execute=true
fi




######################## End time measurement ###################
SECONDS_END=$SECONDS
echo "End $SECONDS_END seconds"

DURATION=$((SECONDS_END-SECONDS_START))
echo "Duration $DURATION seconds"

######################## Show result files ###################
ls -lh /benchbase/results
# cat /benchbase/results/*

######################## Show result summary ###################
echo "####BEXHOMA####"
cat /benchbase/results/*.summary.json
echo "####BEXHOMA####"

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
