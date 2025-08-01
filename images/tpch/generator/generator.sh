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
echo "$BEXHOMA_CHILD" > /tmp/tpch/BEXHOMA_CHILD

######################## Multi-Tenant parameters ########################
BEXHOMA_NUM_PODS_TMP=$BEXHOMA_NUM_PODS
BEXHOMA_CHILD_TMP=$BEXHOMA_CHILD
if [ "$BEXHOMA_TENANT_BY" = "schema" ]; then
    echo "BEXHOMA_TENANT_BY is schema"
    #BEXHOMA_NUM_PODS=1
	BEXHOMA_NUM_PODS=$(( BEXHOMA_NUM_PODS / BEXHOMA_TENANT_NUM ))
	BEXHOMA_CHILD=$(( BEXHOMA_CHILD % BEXHOMA_TENANT_NUM + 1 ))
    BEXHOMA_SCHEMA="tenant_$((BEXHOMA_CHILD - 1))"
    echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
    echo "BEXHOMA_SCHEMA:$BEXHOMA_SCHEMA"
	echo "BEXHOMA_CHILD $BEXHOMA_CHILD"
	echo "BEXHOMA_NUM_PODS $BEXHOMA_NUM_PODS"
elif [ "$BEXHOMA_TENANT_BY" = "database" ]; then
    echo "BEXHOMA_TENANT_BY is database"
    #BEXHOMA_NUM_PODS=1
	BEXHOMA_NUM_PODS=$(( BEXHOMA_NUM_PODS / BEXHOMA_TENANT_NUM ))
	BEXHOMA_CHILD=$(( BEXHOMA_CHILD % BEXHOMA_TENANT_NUM + 1 ))
    BEXHOMA_DATABASE="tenant_$((BEXHOMA_CHILD - 1))"
    echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
    echo "BEXHOMA_SCHEMA:$BEXHOMA_SCHEMA"
	echo "BEXHOMA_CHILD $BEXHOMA_CHILD"
	echo "BEXHOMA_NUM_PODS $BEXHOMA_NUM_PODS"
elif [ "$BEXHOMA_TENANT_BY" = "container" ]; then
    echo "BEXHOMA_TENANT_BY is container"
    echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
    echo "BEXHOMA_SCHEMA:$BEXHOMA_SCHEMA"
    echo "BEXHOMA_CHILD $BEXHOMA_CHILD"
    echo "BEXHOMA_NUM_PODS $BEXHOMA_NUM_PODS"
else
    echo "BEXHOMA_TENANT_BY is not set"
fi
BEXHOMA_NUM_PODS_REDUCED=$BEXHOMA_NUM_PODS

######################## Destination of raw data ########################
if test $STORE_RAW_DATA -gt 0
then
	# store in (distributed) file system
	if test $BEXHOMA_NUM_PODS -gt 1
	then
		# data should be split into parts
		destination_raw=/data/tpch/SF$SF/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD
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
	if test $BEXHOMA_NUM_PODS -gt 1
	then
		# data should be split into parts
		#destination_raw=/data/tpch/SF$SF/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD
		destination_raw=/tmp/tpch/SF$SF/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD
	else
		# data is not split into parts
		#destination_raw=/data/tpch/SF$SF
		destination_raw=/tmp/tpch/SF$SF
	fi
	mkdir -p $destination_raw
fi
echo "destination_raw $destination_raw"

######################## Multi-Tenant parameters ########################
BEXHOMA_NUM_PODS=$BEXHOMA_NUM_PODS_TMP

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

######################## Copy generator executables ########################
cd $destination_raw
cp /tmp/dists.dss ./dists.dss
cp /tmp/dbgen ./dbgen

######################## Execute workload ###################
############ Differ between single-pod and multi-pod setting ############
BEXHOMA_NUM_PODS=$BEXHOMA_NUM_PODS_REDUCED
if test $BEXHOMA_NUM_PODS -gt 1
then
	echo "./dbgen -s $SF -S $BEXHOMA_CHILD -C $BEXHOMA_NUM_PODS"
	time ./dbgen -s $SF -S $BEXHOMA_CHILD -C $BEXHOMA_NUM_PODS
else
	echo "./dbgen -s $SF"
	time ./dbgen -s $SF
fi

#time /tmp/dsdgen -dir /tmp/tpcds/ -scale $SF -parallel $BEXHOMA_NUM_PODS -child $BEXHOMA_CHILD -verbose -RNGSEED $RNGSEED
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
#if [ -f "$destination_raw/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat" ]
#then
#	# convert into new file
#	echo "Convert customer.dat"
#	iconv -f ISO_8859-1 -t UTF-8 $destination_raw/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat > customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}_utf8.dat
#	# rename to original name
#	mv customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}_utf8.dat $destination_raw/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat
#	# remove first character (damaged?)
#	#tail -c +2 customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}_utf8.dat > /tmp/tpcds/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat
#	# show head of file
#	head $destination_raw/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat
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
