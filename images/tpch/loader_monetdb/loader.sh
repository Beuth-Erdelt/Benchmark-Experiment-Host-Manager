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

######################## Show more parameters ########################
BEXHOMA_CHILD=$(cat /tmp/tpch/BEXHOMA_CHILD )
echo "BEXHOMA_CHILD $BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS $BEXHOMA_NUM_PODS"
echo "SF $SF"

######################## Destination of raw data ########################
if test $STORE_RAW_DATA -gt 0
then
    # store in (distributed) file system
    if test $BEXHOMA_NUM_PODS -gt 1
    then
        destination_raw=/data/tpch/SF$SF/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD
    else
        destination_raw=/data/tpch/SF$SF
    fi
else
    # only store locally
    destination_raw=/tmp/tpch/SF$SF/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD
fi
echo "destination_raw $destination_raw"
cd $destination_raw

######################## Show generated files ########################
echo "Found these files:"
ls $destination_raw/*tbl* -lh

######################## Add login parameters for MonetDB ########################
#cd /tmp/tpch/
echo "user=monetdb
password=monetdb" > .monetdb

######################## Wait until all pods of job are ready ########################
if test $BEXHOMA_SYNCH_LOAD -gt 0
then
    echo "Querying counter bexhoma-loader-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
    # add this pod to counter
    redis-cli -h 'bexhoma-messagequeue' incr "bexhoma-loader-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
    # wait for number of pods to be as expected
    while : ; do
        PODS_RUNNING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-loader-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
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

######################## Execute loading ###################
# shuffled
#for i in `ls *tbl* | shuf`; do
# ordered
for i in *tbl*; do
    basename=${i%.tbl*}
    wordcount=($(wc -l $i))
    lines=${wordcount[0]}
    # skip table if limit to other table is set
    if [ -z "${TPCH_TABLE}" ]
    then
        echo "table limit not set"
    elif [ "${TPCH_TABLE}" == "$basename" ]
    then
        echo "limit import to this table $TPCH_TABLE"
    else
        echo "limit import to other table $TPCH_TABLE"
        continue
    fi
    if [[ $basename == "nation" ]]
    then
        if test $BEXHOMA_CHILD -gt 1
        then
            continue
        fi
    fi
    if [[ $basename == "region" ]]
    then
        if test $BEXHOMA_CHILD -gt 1
        then
            continue
        fi
    fi
    #COMMAND="COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|','\\n','\"' NULL AS ''"
    COMMAND="COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|' NULL AS ''"
    echo "============================"
    echo "$COMMAND"
    #OUTPUT="$(mclient --host $BEXHOMA_HOST --database $BEXHOMA_DATABASE --port $BEXHOMA_PORT -s \"COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|' NULL AS ''\" - < $i)"

    #FAILED=0 # everything ok
    #FAILED=1 # known error
    #FAILED=2 # unknown error
    FAILED=1
    while [ $FAILED == 1 ]
    do
        FAILED=2
        SECONDS_START=$SECONDS
        echo "=========="
        time mclient --host $BEXHOMA_HOST --database $BEXHOMA_DATABASE --port $BEXHOMA_PORT -E UTF-8 -s "$COMMAND" - < $i &> /tmp/OUTPUT.txt
        echo "Start $SECONDS_START seconds"
        SECONDS_END=$SECONDS
        echo "End $SECONDS_END seconds"
        DURATION=$((SECONDS_END-SECONDS_START))
        echo "Duration $DURATION seconds"
        #mclient --host $BEXHOMA_HOST --database $BEXHOMA_DATABASE --port $BEXHOMA_PORT -E UTF-8 -L import.log -s "$COMMAND" - < $i &>OUTPUT.txt
        #mclient --host $BEXHOMA_HOST --database $BEXHOMA_DATABASE --port $BEXHOMA_PORT -s "COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|','\\n','\"' NULL AS ''" - < $i &>OUTPUT.txt
        #cat import.log
        OUTPUT=$(cat /tmp/OUTPUT.txt )
        echo "$OUTPUT"
        # everything worked well ("row" and "rows" string checked)
        if [[ $OUTPUT == *"$lines affected row"* ]]; then echo "Import ok"; FAILED=0; fi
        # rollback, we have to do it again (?)
        if [[ $OUTPUT == *"ROLLBACK"* ]]; then echo "ROLLBACK occured"; FAILED=1; fi
        # no thread left, we have to do it again (?)
        if [[ $OUTPUT == *"failed to start worker thread"* ]]; then echo "No worker thread"; FAILED=1; fi
        if [[ $OUTPUT == *"failed to start producer thread"* ]]; then echo "No producer thread"; FAILED=1; fi
        if [[ $OUTPUT == *"Challenge string is not valid, it is empty"* ]]; then echo "No Login possible"; FAILED=1; fi
        # something else - what?
        if [[ $OUTPUT == 2 ]]; then echo "Something unexpected happend"; fi
        echo "FAILED = $FAILED at $basename"
        if [[ $FAILED != 0 ]]; then echo "Wait 1s before retrying"; sleep 1; fi
    done
    #echo "COPY $lines RECORDS INTO $basename FROM '/tmp/$i' ON CLIENT DELIMITERS '|' NULL AS '';" >> load.sql
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

######################## Exit successfully ###################
# while true; do sleep 2; done
exit 0
