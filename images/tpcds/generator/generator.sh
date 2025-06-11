#!/bin/bash

######################## Start timing ########################
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS
bexhoma_start_epoch=$(date -u +%s)

######################## Show general parameters ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_EXPERIMENT:$BEXHOMA_EXPERIMENT"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"

######################## Get number of client in job queue ########################
echo "Querying message queue bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
# redis-cli -h 'bexhoma-messagequeue' lpop "bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
BEXHOMA_CHILD="$(redis-cli -h 'bexhoma-messagequeue' lpop bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
if [ -z "$BEXHOMA_CHILD" ]
then
	BEXHOMA_CHILD=1
fi

######################## Show more parameters ########################
echo "BEXHOMA_CHILD $BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS $BEXHOMA_NUM_PODS"
echo "SF $SF"
echo "$BEXHOMA_CHILD" > /tmp/tpcds/BEXHOMA_CHILD

######################## Wait until all pods of job are ready ########################
if test $BEXHOMA_SYNCH_GENERATE -gt 0
then
	echo "Querying counter bexhoma-generator-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
	# add this pod to counter
	redis-cli -h 'bexhoma-messagequeue' incr "bexhoma-generator-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
	# wait for number of pods to be as expected
	while : ; do
		PODS_RUNNING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-generator-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
		echo "Found $PODS_RUNNING / $BEXHOMA_NUM_PODS running pods"
		if  test "$PODS_RUNNING" == $BEXHOMA_NUM_PODS
		then
			echo "OK"
			break
        elif test "$PODS_RUNNING" -gt $BEXHOMA_NUM_PODS
        then
            echo "Too many pods! Restart occured?"
            exit 0
		else
			echo "We have to wait"
			sleep 1
		fi
	done
fi

######################## Start measurement of time ########################
bexhoma_start_epoch=$(date -u +%s)
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"

######################## Destination of raw data ########################
if test $STORE_RAW_DATA -gt 0
then
	# store in (distributed) file system
	if test $BEXHOMA_NUM_PODS -gt 1
	then
		# data should be split into parts
		destination_raw=/data/tpcds/SF$SF/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD/
	else
		# data is not split into parts
		destination_raw=/data/tpcds/SF$SF/
	fi
	if [ -d "$destination_raw" ]; then
		### raw folder exists ###
		if test $STORE_RAW_DATA_RECREATE -gt 0
		then
			echo "Recreate raw folder"
			rm -r $destination_raw
			mkdir -p $destination_raw
		else
			### Exit successfully ###
			echo "Raw folder exists, I do nothing"
			SECONDS_END_SCRIPT=$SECONDS
			DURATION_SCRIPT=$((SECONDS_END_SCRIPT-SECONDS_START_SCRIPT))
			echo "Duration $DURATION_SCRIPT seconds"
			echo "BEXHOMA_DURATION:$DURATION_SCRIPT"
			bexhoma_end_epoch=$(date -u +%s)
			echo "BEXHOMA_START:$bexhoma_start_epoch"
			echo "BEXHOMA_END:$bexhoma_end_epoch"
			exit 0
		fi
	else
		###  create raw folder ###
		mkdir -p $destination_raw
	fi
else
	# only store locally
	destination_raw=/tmp/tpcds/SF$SF/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD
	mkdir -p $destination_raw
fi
echo "destination_raw $destination_raw"

######################## Copy generator executables ########################
cd $destination_raw
cp /tmp/tpcds.idx ./tpcds.idx
cp /tmp/dsdgen ./dsdgen

######################## Execute workload ###################
############ Differ between single-pod and multi-pod setting ############
if test $BEXHOMA_NUM_PODS -gt 1
then
	echo "./dsdgen -dir $destination_raw -scale $SF -parallel $BEXHOMA_NUM_PODS -child $BEXHOMA_CHILD -RNGSEED $RNGSEED"
	time ./dsdgen -dir $destination_raw -scale $SF -parallel $BEXHOMA_NUM_PODS -child $BEXHOMA_CHILD -RNGSEED $RNGSEED
else
	echo "./dsdgen -dir $destination_raw -scale $SF -RNGSEED $RNGSEED"
	time ./dsdgen -dir $destination_raw -scale $SF -RNGSEED $RNGSEED
fi
# -verbose

######################## Show generated files ###################
#echo "Move generated files:"
#time mv *tbl* /tmp/tpch
#time mv *tbl* $destination_raw
echo "Generated these files:"
ls $destination_raw/*.dat -lh

######################## End time measurement ###################
SECONDS_END=$SECONDS
echo "End $SECONDS_END seconds"

DURATION=$((SECONDS_END-SECONDS_START))
echo "Duration $DURATION seconds"

######################## Translate customer to utf8 ###################
if test $TRANSFORM_RAW_DATA -gt 0
then
	if [ -f "$destination_raw/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat" ]
	then
		# convert into new file
		echo "Convert customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat"
		iconv -f ISO_8859-1 -t UTF-8 $destination_raw/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat > customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}_utf8.dat
		# rename to original name
		mv customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}_utf8.dat $destination_raw/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat
		# remove first character (damaged?)
		#tail -c +2 customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}_utf8.dat > /tmp/tpcds/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat
		# show head of file
		head $destination_raw/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat
	fi
	if [ -f "$destination_raw/customer.dat" ]
	then
		# convert into new file
		echo "Convert customer.dat"
		iconv -f ISO_8859-1 -t UTF-8 $destination_raw/customer.dat > customer_utf8.dat
		# rename to original name
		mv customer_utf8.dat $destination_raw/customer.dat
		# remove first character (damaged?)
		#tail -c +2 customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}_utf8.dat > /tmp/tpcds/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat
		# show head of file
		head $destination_raw/customer.dat
	fi
fi

######################## Remove last character per line ###################
if test $TRANSFORM_RAW_DATA -gt 0
then
	echo "Remove last character per line"
	for i in $destination_raw/*.dat; do
		echo "$i"
	    time sed 's/.$//' -i $i
	done
fi

######################## End measurement of time ########################
bexhoma_end_epoch=$(date -u +%s)
SECONDS_END=$SECONDS
echo "End $SECONDS_END seconds"

DURATION=$((SECONDS_END-SECONDS_START))
echo "Duration $DURATION seconds"

######################## Show timing information ###################
echo "Generating done"

DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"

SECONDS_END_SCRIPT=$SECONDS
DURATION_SCRIPT=$((SECONDS_END_SCRIPT-SECONDS_START_SCRIPT))
echo "Duration $DURATION_SCRIPT seconds (script total)"
echo "BEXHOMA_DURATION:$DURATION_SCRIPT"
echo "BEXHOMA_START:$bexhoma_start_epoch"
echo "BEXHOMA_END:$bexhoma_end_epoch"

######################## Exit successfully ###################
exit 0
