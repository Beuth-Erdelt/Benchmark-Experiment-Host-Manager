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
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "SF:$SF"
echo "TPCH_REFRESH_STREAMS:$TPCH_REFRESH_STREAMS"
echo "TPCH_REFRESH_STREAM_OFFSET:$TPCH_REFRESH_STREAM_OFFSET"
echo "STORE_RAW_DATA:$STORE_RAW_DATA"

######################## Compute total sets needed ########################
LAST_SET=$((TPCH_REFRESH_STREAM_OFFSET + TPCH_REFRESH_STREAMS))
echo "LAST_SET:$LAST_SET"

######################## Destination of raw data ########################
if test $STORE_RAW_DATA -gt 0
then
    destination_raw=/data/tpch-refresh/SF$SF
else
    destination_raw=/tmp/tpch-refresh/SF$SF
fi
echo "destination_raw:$destination_raw"
mkdir -p $destination_raw

######################## Check if all required sets already present ########################
if [ -f "$destination_raw/delete.$LAST_SET" ]
then
    echo "delete.$LAST_SET already present — all sets up to $LAST_SET exist, skipping generation"
    SECONDS_END_SCRIPT=$SECONDS
    DURATION_SCRIPT=$((SECONDS_END_SCRIPT-SECONDS_START_SCRIPT))
    bexhoma_end_epoch=$(date -u +%s)
    DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
    echo "NOW: $DATEANDTIME"
    echo "Duration $DURATION_SCRIPT seconds (script total)"
    echo "BEXHOMA_DURATION:$DURATION_SCRIPT"
    echo "BEXHOMA_START:$bexhoma_start_epoch"
    echo "BEXHOMA_END:$bexhoma_end_epoch"
    exit 0
fi

######################## Start measurement of time ########################
bexhoma_start_epoch=$(date -u +%s)
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"

######################## Copy generator executables ########################
cd $destination_raw
cp /tmp/dbgen ./dbgen
cp /tmp/dists.dss ./dists.dss

######################## Generate refresh data ########################
# dbgen -U N generates sets 1..N: orders.tbl.u1..uN, lineitem.tbl.u1..uN, delete.1..delete.N
# Existing sets are overwritten with identical deterministic content — harmless.
echo "./dbgen -s $SF -U $LAST_SET"
time ./dbgen -s $SF -U $LAST_SET

######################## Remove last character per line ###################
if test $TRANSFORM_RAW_DATA -gt 0
then
	echo "Remove last character per line"
	for i in $destination_raw/delete.*; do
		echo "$i"
	    time sed 's/.$//' -i $i
	done
	for i in $destination_raw/*.tbl.*; do
		echo "$i"
	    time sed 's/.$//' -i $i
	done
fi

######################## Remove generator executables ########################
rm ./dbgen ./dists.dss

######################## Show generated files ########################
echo "Generated these files:"
ls $destination_raw -lh

######################## End measurement of time ########################
bexhoma_end_epoch=$(date -u +%s)
SECONDS_END_SCRIPT=$SECONDS
DURATION_SCRIPT=$((SECONDS_END_SCRIPT-SECONDS_START_SCRIPT))

echo "Generation done"
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"
echo "Duration $DURATION_SCRIPT seconds (script total)"
echo "BEXHOMA_DURATION:$DURATION_SCRIPT"
echo "BEXHOMA_START:$bexhoma_start_epoch"
echo "BEXHOMA_END:$bexhoma_end_epoch"

######################## Parameters summary ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_EXPERIMENT:$BEXHOMA_EXPERIMENT"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "SF:$SF"
echo "TPCH_REFRESH_STREAMS:$TPCH_REFRESH_STREAMS"
echo "TPCH_REFRESH_STREAM_OFFSET:$TPCH_REFRESH_STREAM_OFFSET"
echo "STORE_RAW_DATA:$STORE_RAW_DATA"
echo "LAST_SET:$LAST_SET"
echo "destination_raw:$destination_raw"

######################## Exit successfully ########################
exit 0
