#!/bin/bash

######################## Start timing ########################
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS
bexhoma_start_epoch=$(date -u +%s)

######################## Show general parameters ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"

######################## Get number of client in job queue ########################
echo "Querying message queue bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
# redis-cli -h 'bexhoma-messagequeue' lpop "bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
CHILD="$(redis-cli -h 'bexhoma-messagequeue' lpop bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
if [ -z "$CHILD" ]
then
	CHILD=1
fi

######################## Show more parameters ########################
echo "CHILD $CHILD"
echo "NUM_PODS $NUM_PODS"
echo "SF $SF"
echo "$CHILD" > /tmp/tpch/CHILD

######################## Wait until all pods of job are ready ########################
if test $BEXHOMA_SYNCH_GENERATE -gt 0
then
	echo "Querying counter bexhoma-generator-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
	# add this pod to counter
	redis-cli -h 'bexhoma-messagequeue' incr "bexhoma-generator-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
	# wait for number of pods to be as expected
	while : ; do
		PODS_RUNNING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-generator-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
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
fi

######################## Start measurement of time ########################
bexhoma_start_epoch=$(date -u +%s)
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"

######################## Destination of raw data ########################
if test $STORE_RAW_DATA -gt 0
then
	# store in (distributed) file system
	if test $NUM_PODS -gt 1
	then
		# data should be split into parts
		destination_raw=/data/tpch/SF$SF/$NUM_PODS/$CHILD
	else
		# data is not split into parts
		destination_raw=/data/tpch/SF$SF
	fi
	if [ -d "$destination_raw" ] && [ -f "$destination_raw/nation.tbl" ]; then
		### raw folder and nation table exist ###
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
	destination_raw=/tmp/tpch/SF$SF/$NUM_PODS/$CHILD
	mkdir -p $destination_raw
fi
echo "destination_raw $destination_raw"

######################## Copy generator executables ########################
cd $destination_raw
cp /tmp/dists.dss ./dists.dss
cp /tmp/dbgen ./dbgen

######################## Execute workload ###################
############ Differ between single-pod and multi-pod setting ############
if test $NUM_PODS -gt 1
then
	echo "./dbgen -s $SF -S $CHILD -C $NUM_PODS"
	time ./dbgen -s $SF -S $CHILD -C $NUM_PODS
else
	echo "./dbgen -s $SF"
	time ./dbgen -s $SF
fi

#time /tmp/dsdgen -dir /tmp/tpcds/ -scale $SF -parallel $NUM_PODS -child $CHILD -verbose -RNGSEED $RNGSEED
# -v for verbose
# -q for quite

######################## Show generated files ###################
#echo "Move generated files:"
#time mv *tbl* /tmp/tpch
#time mv *tbl* $destination_raw
echo "Generated these files:"
ls $destination_raw/*tbl* -lh

######################## End timing before transformation and show timing information ###################
#bexhoma_end_epoch=$(date -u +%s)
#echo "BEXHOMA_START:$bexhoma_start_epoch"
#echo "BEXHOMA_END:$bexhoma_end_epoch"

######################## Translate customer to utf8 ###################
#echo "Translate customer to utf8"
#if [ -f "$destination_raw/customer_${CHILD}_${NUM_PODS}.dat" ]
#then
#	# convert into new file
#	echo "Convert customer.dat"
#	iconv -f ISO_8859-1 -t UTF-8 $destination_raw/customer_${CHILD}_${NUM_PODS}.dat > customer_${CHILD}_${NUM_PODS}_utf8.dat
#	# rename to original name
#	mv customer_${CHILD}_${NUM_PODS}_utf8.dat $destination_raw/customer_${CHILD}_${NUM_PODS}.dat
#	# remove first character (damaged?)
#	#tail -c +2 customer_${CHILD}_${NUM_PODS}_utf8.dat > /tmp/tpcds/customer_${CHILD}_${NUM_PODS}.dat
#	# show head of file
#	head $destination_raw/customer_${CHILD}_${NUM_PODS}.dat
#fi

######################## Remove last character per line ###################
if test $TRANSFORM_RAW_DATA -gt 0
then
	echo "Remove last character per line"
	for i in $destination_raw/*tbl*; do
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
