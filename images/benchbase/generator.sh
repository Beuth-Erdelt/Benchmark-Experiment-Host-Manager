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

######################## Get number of client in job queue ########################
#echo "Querying message queue bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
#redis-cli -h 'bexhoma-messagequeue' lpop "bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
#CHILD="$(redis-cli -h 'bexhoma-messagequeue' lpop bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
if [ -z "$CHILD" ]
then
	CHILD=1
fi
# echo "$CHILD" > /tmp/ycsb/CHILD


############ Show more parameters ############
echo "CHILD $CHILD"
echo "NUM_PODS $NUM_PODS"
echo "SF $SF"
echo "BENCHBASE_BENCH $BENCHBASE_BENCH"
echo "BENCHBASE_PROFILE $BENCHBASE_PROFILE"
echo "BENCHBASE_TARGET $BENCHBASE_TARGET"
echo "BENCHBASE_TIME $BENCHBASE_TIME"
echo "BENCHBASE_TERMINALS $BENCHBASE_TERMINALS"
echo "BENCHBASE_BATCHSIZE $BENCHBASE_BATCHSIZE"
echo "BENCHBASE_CREATE_SCHEMA $BENCHBASE_CREATE_SCHEMA"
echo "BENCHBASE_NEWCONNPERTXN $BENCHBASE_NEWCONNPERTXN"



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

######################## Replace parameters in workload file ###################
echo "FILENAME $FILENAME"

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
