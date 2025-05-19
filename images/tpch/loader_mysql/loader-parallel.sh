#!/bin/bash

# Reference for tool
# https://dev.mysql.com/doc/mysql-shell/8.3/en/mysql-shell-utilities-parallel-table.html
# , 'bytesPerChunk': '50M' #  Util.import_table: The 'bytesPerChunk' option cannot be used when loading from multiple files.


######################## Start timing ########################
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS

######################## Show general parameters ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
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

######################## Fix missing locale - in Dockerfile ########################
#export LC_ALL="en_US.UTF-8"
#export LANG="en_US.utf8"

######################## Parallel loading (several scripts at once) only makes sense for more than 1 pod ########################
if test $BEXHOMA_NUM_PODS -gt 1
then
    echo "MYSQL_LOADING_PARALLEL:$MYSQL_LOADING_PARALLEL"
else
    MYSQL_LOADING_PARALLEL=0
    echo "MYSQL_LOADING_PARALLEL:$MYSQL_LOADING_PARALLEL"
fi

######################## Only first loader pod should be active ########################
# this holds for parallel loading, i.e. one client writes all files to host
if test $MYSQL_LOADING_PARALLEL -gt 0
then
    if test $BEXHOMA_CHILD -gt 1
    then
        echo "Only first loader pod should be active"
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
        exit 0
    fi
fi

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
        echo "skipping $basename, import is limited to other table ($TPCH_TABLE)"
        continue
    fi
    if test $MYSQL_LOADING_PARALLEL -gt 0
    then
        # first pod: table nation or region will be imported olny one, others: we will import all parts at once
        if [[ $basename == "nation" ]]
        then
            COMMAND="util.import_table('$destination_raw/$i', {'schema': 'tpch', 'table': '$basename', 'dialect': 'csv-unix', 'skipRows': 0, 'showProgress': True, 'fieldsTerminatedBy': '|', 'threads': $MYSQL_LOADING_THREADS})"
            #if test $BEXHOMA_CHILD -gt 1
            #then
            #    continue
            #fi
        elif [[ $basename == "region" ]]
        then
            COMMAND="util.import_table('$destination_raw/$i', {'schema': 'tpch', 'table': '$basename', 'dialect': 'csv-unix', 'skipRows': 0, 'showProgress': True, 'fieldsTerminatedBy': '|', 'threads': $MYSQL_LOADING_THREADS})"
            #if test $BEXHOMA_CHILD -gt 1
            #then
            #    continue
            #fi
        else
            COMMAND="util.import_table(["
            for ((j=1;j<=$BEXHOMA_NUM_PODS;j++)); 
            do 
               #echo $j
               file="'$destination_raw/../$j/$basename.tbl.$j',"
               COMMAND=$COMMAND$file
            done
            COMMAND_END="], {'schema': 'tpch', 'table': '$basename', 'dialect': 'csv-unix', 'skipRows': 0, 'showProgress': True, 'fieldsTerminatedBy': '|', 'threads': $MYSQL_LOADING_THREADS})"
            COMMAND=${COMMAND::-1}$COMMAND_END
        fi
    else
        # first pod or not table nation or region: we will import single part
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
        COMMAND="util.import_table('$destination_raw/$i', {'schema': 'tpch', 'table': '$basename', 'dialect': 'csv-unix', 'skipRows': 0, 'showProgress': True, 'fieldsTerminatedBy': '|', 'threads': $MYSQL_LOADING_THREADS})"
    fi
    #COMMAND="COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|','\\n','\"' NULL AS ''"
    #COMMAND="COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|' NULL AS ''"
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
        #time mysqlsh --sql --password=root --host $BEXHOMA_HOST --database $BEXHOMA_DATABASE --port $BEXHOMA_PORT -e "$COMMAND" &>OUTPUT.txt
        time mysqlsh --python --password=root --host $BEXHOMA_HOST --database $BEXHOMA_DATABASE --port $BEXHOMA_PORT -e "$COMMAND" &> /tmp/OUTPUT.txt
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
        FAILED=0
        # everything worked well ("row" and "rows" string checked)
        if [[ $OUTPUT == *"Total rows affected in tpch.$basename: Records: $lines"* ]]; then echo "Import ok"; FAILED=0; fi
        # rollback, we have to do it again (?)
        if [[ $OUTPUT == *"ROLLBACK"* ]]; then echo "ROLLBACK occured"; FAILED=1; fi
        # no thread left, we have to do it again (?)
        #if [[ $OUTPUT == *"failed to start worker thread"* ]]; then echo "No worker thread"; FAILED=1; fi
        #if [[ $OUTPUT == *"failed to start producer thread"* ]]; then echo "No producer thread"; FAILED=1; fi
        #if [[ $OUTPUT == *"Challenge string is not valid, it is empty"* ]]; then echo "No Login possible"; FAILED=1; fi
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
