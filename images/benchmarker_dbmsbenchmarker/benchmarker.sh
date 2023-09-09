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

######################## Make sure result folder exists ########################
mkdir -p /results/$BEXHOMA_EXPERIMENT

######################## Get number of client in job queue ########################
echo "Querying message queue bexhoma-benchmarker-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
# redis-cli -h 'bexhoma-messagequeue' lpop "bexhoma-benchmarker-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
CHILD="$(redis-cli -h 'bexhoma-messagequeue' lpop bexhoma-benchmarker-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
if [ -z "$CHILD" ]
then
	CHILD=1
fi

######################## Wait until all pods of job are ready ########################
echo "Querying counter bexhoma-benchmarker-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
# add this pod to counter
redis-cli -h 'bexhoma-messagequeue' incr "bexhoma-benchmarker-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
# wait for number of pods to be as expected
while : ; do
	PODS_RUNNING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-benchmarker-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
	echo "Found $PODS_RUNNING / $NUM_PODS running pods"
    if  test "$PODS_RUNNING" == $NUM_PODS
    then
        echo "OK"
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

######################## Start measurement of time ########################
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"
bexhoma_start_epoch=$(date -u +%s)
echo "Start at $bexhoma_start_epoch epoch seconds"

######################## Dev mode ###################
if test $DBMSBENCHMARKER_DEV -gt 0
then
	# dev environment
	git pull
fi

######################## Execute workload ###################
# run dbmsbenchmarker
if test $DBMSBENCHMARKER_VERBOSE -gt 0
then
	python ./benchmark.py run -b -w connection \
		-f /results/$DBMSBENCHMARKER_CODE \
		-r /results/$DBMSBENCHMARKER_CODE \
		-mps \
		-cs -sf $DBMSBENCHMARKER_CONNECTION \
		-ms $DBMSBENCHMARKER_CLIENT \
		-c "$DBMSBENCHMARKER_CONNECTION" \
		-ca "$DBMSBENCHMARKER_ALIAS" \
		-cf ${DBMSBENCHMARKER_CONNECTION}.config \
		-rcp $DBMSBENCHMARKER_RECREATE_PARAMETER \
		-d \
		-vq \
		-vr \
		-vp \
		-vs \
		-sid $CHILD \
		-ssh $DBMSBENCHMARKER_SHUFFLE_QUERIES \
		| tee /tmp/dbmsbenchmarker.log
		#-sl $DBMSBENCHMARKER_SLEEP \
		#-st "$DBMSBENCHMARKER_START" \
else
	python ./benchmark.py run -b -w connection \
		-f /results/$DBMSBENCHMARKER_CODE \
		-r /results/$DBMSBENCHMARKER_CODE \
		-mps \
		-cs -sf $DBMSBENCHMARKER_CONNECTION \
		-ms $DBMSBENCHMARKER_CLIENT \
		-c "$DBMSBENCHMARKER_CONNECTION" \
		-ca "$DBMSBENCHMARKER_ALIAS" \
		-cf ${DBMSBENCHMARKER_CONNECTION}.config \
		-rcp $DBMSBENCHMARKER_RECREATE_PARAMETER \
		-sid $CHILD \
		-ssh $DBMSBENCHMARKER_SHUFFLE_QUERIES \
		| tee /tmp/dbmsbenchmarker.log
		#-sl $DBMSBENCHMARKER_SLEEP \
		#-st "$DBMSBENCHMARKER_START" \
fi
# -f   config folder
# -r   result folder
# -mps monitor per stream
# -cs -sf subfolder per dbms (connection)
# -ms  max number of subfolders
# -sl  sleep seconds before start benchmarking
# -st  start time for operating
# -c   name of dbms (connection) to benchmark
# -ca  alias for dbms (connection) to benchmark
# -cf  config of dbms (connection)
# -rcp force recreation of parameter - otherwise all instances of an experiment use the same parameters
# -sid id of a stream in parallel execution of streams
# -ssh shuffle query execution based on id of stream

######################## End time measurement ###################
SECONDS_END=$SECONDS
echo "End $SECONDS_END seconds"

DURATION=$((SECONDS_END-SECONDS_START))
echo "Duration $DURATION seconds"


######################## Find duration output of DBMSBenchmarker ###################
# default end time is now
bexhoma_end_epoch_computed=$(date -u +%s)
# better: read pure benchmarking time from log of dbmsbenchmarker and compute end of benchmarking
DBMSBenchmarker_duration_seconds=$(sed -n 's/DBMSBenchmarker duration: //p' /tmp/dbmsbenchmarker.log)
# remove " [s]" at the end
DBMSBenchmarker_duration=${DBMSBenchmarker_duration_seconds::-4}
bexhoma_end_epoch_computed=$((bexhoma_start_epoch+DBMSBenchmarker_duration))
echo "Computed end at $bexhoma_end_epoch_computed epoch seconds"
echo "because of DBMSBenchmarker_duration:$DBMSBenchmarker_duration"

######################## Show timing information ###################
echo "Benchmarking done"

DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "$DATEANDTIME"

SECONDS_END_SCRIPT=$SECONDS
DURATION_SCRIPT=$((SECONDS_END_SCRIPT-SECONDS_START_SCRIPT))
echo "Duration script $DURATION_SCRIPT seconds"
echo "BEXHOMA_DURATION:$DURATION_SCRIPT"

bexhoma_end_epoch=$(date -u +%s)
echo "End at $bexhoma_start_epoch epoch seconds"
echo "BEXHOMA_START:$bexhoma_start_epoch"
echo "BEXHOMA_END:$bexhoma_end_epoch_computed"
#echo "BEXHOMA_START:$SECONDS_START"
#echo "BEXHOMA_END:$SECONDS_END"

######################## Exit successfully ###################
exit 0
