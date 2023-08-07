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


############ Start measurement of time of execution ############
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

cat $FILENAME

ls -lh

pwd

######################## Execute workload ###################
time sh ./entrypoint.sh run --bench $BENCHBASE_BENCH -c $FILENAME --create=true --load=true --execute=false


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
