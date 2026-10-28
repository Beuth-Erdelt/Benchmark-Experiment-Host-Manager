#!/bin/bash

######################## Start timing ########################
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS

######################## Show general parameters ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
echo "BEXHOMA_VOLUME:$BEXHOMA_VOLUME"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "SSB_SCHEMA_VARIANT:$SSB_SCHEMA_VARIANT"

######################## Show more parameters ########################
BEXHOMA_CHILD=$(cat /tmp/ssb/BEXHOMA_CHILD )
echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS:$BEXHOMA_NUM_PODS"
echo "SF:$SF"

######################## Data-job suffix for parallel-loading-job keys ########################
# Always set by Python, even for a single loader entry — no conditional needed.
BEXHOMA_DATA_JOB="${BEXHOMA_DATA_JOB:-1}"

######################## Destination of raw data ########################
# same folders as the generator: normal /data/ssb/SF<SF>[/<N>/<child>], flat .../flat[/<N>/<child>]
if test $STORE_RAW_DATA -gt 0
then
    base_raw=/data/ssb/SF$SF
else
    base_raw=/tmp/ssb/SF$SF
fi
if test $BEXHOMA_NUM_PODS -gt 1
then
    part_raw=/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD
else
    part_raw=""
fi
if [ "$SSB_SCHEMA_VARIANT" = "flat" ]
then
    destination_raw=$base_raw/flat$part_raw
else
    destination_raw=$base_raw$part_raw
fi
echo "destination_raw:$destination_raw"
cd $destination_raw

######################## Show generated files ########################
echo "Found these files:"
ls $destination_raw/*tbl* -lh

######################## Add login parameters for MonetDB ########################
# outside the data folder, which may be the shared /data volume
echo "user=monetdb
password=monetdb" > /tmp/ssb/.monetdb
export DOTMONETDBFILE=/tmp/ssb/.monetdb

######################## Wait until all pods of job are ready ########################
if test $BEXHOMA_SYNCH_LOAD -gt 0
then
    echo "Decrementing job counter bexhoma-loader-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_DATA_JOB"
    redis-cli -h 'bexhoma-messagequeue' decr "bexhoma-loader-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_DATA_JOB"
    while : ; do
        PODS_MISSING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-loader-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_DATA_JOB)"
        echo "Pods still missing in job: $PODS_MISSING"
        if [[ "$PODS_MISSING" =~ ^-?[0-9]+$ ]] && test "$PODS_MISSING" -le 0
        then
            echo "OK, all pods in job are ready."
            break
        else
            sleep 1
        fi
    done
fi

######################## Wait until all pods of round are ready ########################
if test $BEXHOMA_SYNCH_LOAD -gt 0
then
    echo "Decrementing round counter bexhoma-loader-podcount-round-$BEXHOMA_CONFIGURATION-$BEXHOMA_EXPERIMENT"
    redis-cli -h 'bexhoma-messagequeue' decr "bexhoma-loader-podcount-round-$BEXHOMA_CONFIGURATION-$BEXHOMA_EXPERIMENT"
    while : ; do
        PODS_MISSING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-loader-podcount-round-$BEXHOMA_CONFIGURATION-$BEXHOMA_EXPERIMENT)"
        echo "Pods still missing in round: $PODS_MISSING"
        if [[ "$PODS_MISSING" =~ ^-?[0-9]+$ ]] && test "$PODS_MISSING" -le 0
        then
            echo "OK, all pods in round are ready."
            break
        else
            sleep 1
        fi
    done
fi

######################## Start measurement of time ########################
bexhoma_start_epoch=$(date -u +%s)
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"

######################## Execute loading ###################
# file -> table: date.tbl -> dates (date is a reserved word), lineorder.tbl.<k> -> lineorder;
# the dimensions are only in the folder of child 1 (see generator.sh)
FAILED_TABLES=""
for i in *tbl*; do
    basename=${i%.tbl*}
    if [[ $basename == "date" ]]
    then
        table=dates
    else
        table=$basename
    fi
    # skip table if limit to other table is set
    if [ -z "${SSB_TABLE}" ]
    then
        echo "table limit not set"
    elif [ "${SSB_TABLE}" == "$table" ]
    then
        echo "limit import to this table $SSB_TABLE"
    else
        echo "skipping $table, import is limited to other table ($SSB_TABLE)"
        continue
    fi
    wordcount=($(wc -l $i))
    lines=${wordcount[0]}
    COMMAND="COPY $lines RECORDS INTO $table FROM STDIN USING DELIMITERS '|' NULL AS ''"
    echo "============================"
    echo "$COMMAND"
    SECONDS_START_TABLE=$SECONDS
    # retry only on the known transient errors (as in the TPC-H loader); any other
    # answer than "<lines> affected rows" fails the pod
    FAILED=1
    ATTEMPTS=0
    while [ $FAILED == 1 ] && [ $ATTEMPTS -lt 10 ]
    do
        FAILED=2
        ATTEMPTS=$((ATTEMPTS+1))
        echo "========== attempt $ATTEMPTS"
        time mclient --host $BEXHOMA_HOST --database $BEXHOMA_DATABASE --port $BEXHOMA_PORT -E UTF-8 -s "$COMMAND" - < $i &> /tmp/OUTPUT.txt
        OUTPUT=$(cat /tmp/OUTPUT.txt )
        echo "$OUTPUT"
        if [[ $OUTPUT == *"$lines affected row"* ]]; then echo "Import ok"; FAILED=0; fi
        if [[ $OUTPUT == *"ROLLBACK"* ]]; then echo "ROLLBACK occured"; FAILED=1; fi
        if [[ $OUTPUT == *"failed to start worker thread"* ]]; then echo "No worker thread"; FAILED=1; fi
        if [[ $OUTPUT == *"failed to start producer thread"* ]]; then echo "No producer thread"; FAILED=1; fi
        if [[ $OUTPUT == *"Challenge string is not valid, it is empty"* ]]; then echo "No Login possible"; FAILED=1; fi
        if [[ $FAILED == 1 ]]; then echo "Wait 1s before retrying"; sleep 1; fi
    done
    DURATION=$((SECONDS-SECONDS_START_TABLE))
    echo "Duration $DURATION seconds"
    if [[ $FAILED != 0 ]]
    then
        echo "Import failed at $table (expected $lines affected rows)"
        FAILED_TABLES="$FAILED_TABLES $table"
    fi
done

######################## End measurement of time ########################
bexhoma_end_epoch=$(date -u +%s)
SECONDS_END=$SECONDS
echo "End $SECONDS_END seconds"

DURATION=$((SECONDS_END-SECONDS_START))
echo "Duration $DURATION seconds"

######################## Show timing information ###################
echo "Loading done"

DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"

SECONDS_END_SCRIPT=$SECONDS
DURATION_SCRIPT=$((SECONDS_END_SCRIPT-SECONDS_START_SCRIPT))
echo "Duration $DURATION_SCRIPT seconds (script total)"
echo "BEXHOMA_DURATION:$DURATION_SCRIPT"
echo "BEXHOMA_START:$bexhoma_start_epoch"
echo "BEXHOMA_END:$bexhoma_end_epoch"

######################## Parameters summary ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
echo "BEXHOMA_VOLUME:$BEXHOMA_VOLUME"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS:$BEXHOMA_NUM_PODS"
echo "SF:$SF"
echo "SSB_SCHEMA_VARIANT:$SSB_SCHEMA_VARIANT"
echo "destination_raw:$destination_raw"

######################## Exit ###################
if [ -n "$FAILED_TABLES" ]
then
    echo "Failed tables:$FAILED_TABLES"
    exit 1
fi
exit 0
