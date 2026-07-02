#!/bin/bash

######################## Start timing ########################
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS

################### Turn Some Parameters into Numbers ###################
BEXHOMA_CHILD=${BEXHOMA_CHILD//[^0-9]/}
BEXHOMA_TENANT_NUM=${BEXHOMA_TENANT_NUM//[^0-9]/}

######################## Show general parameters ########################
BEXHOMA_DATABASE_INITIAL="$BEXHOMA_DATABASE"
BEXHOMA_SCHEMA_INITIAL="$BEXHOMA_SCHEMA"
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_DATABASE_INITIAL:$BEXHOMA_DATABASE_INITIAL"
echo "BEXHOMA_SCHEMA_INITIAL:$BEXHOMA_SCHEMA_INITIAL"
echo "BEXHOMA_VOLUME:$BEXHOMA_VOLUME"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "BEXHOMA_TENANT_NUM:$BEXHOMA_TENANT_NUM"
echo "BEXHOMA_TENANT_BY:$BEXHOMA_TENANT_BY"

######################## Show more parameters ########################
BEXHOMA_CHILD=$(cat /tmp/tpch/BEXHOMA_CHILD )
BEXHOMA_CHILD_INITIAL="$BEXHOMA_CHILD"
echo "BEXHOMA_CHILD_INITIAL:$BEXHOMA_CHILD_INITIAL"
echo "BEXHOMA_NUM_PODS:$BEXHOMA_NUM_PODS"
echo "SF:$SF"

######################## Read per-pod config from Redis ########################
BEXHOMA_POD_CONFIG_KEY="bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-config-$BEXHOMA_CHILD"
echo "Querying per-pod config at $BEXHOMA_POD_CONFIG_KEY"
BEXHOMA_POD_CONFIG_JSON="$(redis-cli -h 'bexhoma-messagequeue' get "$BEXHOMA_POD_CONFIG_KEY")"
if [ -z "$BEXHOMA_POD_CONFIG_JSON" ] || [ "$BEXHOMA_POD_CONFIG_JSON" = "nil" ]; then
    echo "No per-pod config found in Redis."
else
    eval "$(echo "$BEXHOMA_POD_CONFIG_JSON" \
      | tr -d '{}' \
      | tr ',' '\n' \
      | awk 'BEGIN{FS="\""} NF>=4 && $2!="" {print "export BEXHOMA_POD_"$2"=\""$4"\""; print "echo \"BEXHOMA_POD_"$2"="$4"\""}')"
fi

######################## Multi-Tenant parameters ########################
BEXHOMA_NUM_PODS_TMP=$BEXHOMA_NUM_PODS
BEXHOMA_CHILD_TMP=$BEXHOMA_CHILD
if [ "$BEXHOMA_TENANT_BY" = "schema" ]; then
    echo "BEXHOMA_TENANT_BY is schema"
    #BEXHOMA_NUM_PODS=1
    BEXHOMA_NUM_PODS=$(( BEXHOMA_NUM_PODS / BEXHOMA_TENANT_NUM ))
    BEXHOMA_NUM_PODS_TENANT="$BEXHOMA_NUM_PODS"
    #BEXHOMA_CHILD=$(( ( BEXHOMA_CHILD - 1 ) % BEXHOMA_TENANT_NUM + 1 ))
    #SCHEMA_INDEX=$(( ( BEXHOMA_CHILD - 1 ) / BEXHOMA_TENANT_NUM ))
    SCHEMA_INDEX=$(( ( BEXHOMA_CHILD - 1 ) % BEXHOMA_TENANT_NUM ))
    BEXHOMA_CHILD=$(( ( BEXHOMA_CHILD - 1 ) / BEXHOMA_TENANT_NUM + 1 ))
    BEXHOMA_SCHEMA="tenant_${SCHEMA_INDEX}"
    #BEXHOMA_SCHEMA="tenant_$((BEXHOMA_CHILD - 1))"
    BEXHOMA_TENANT_ID=$SCHEMA_INDEX
    echo "BEXHOMA_TENANT_ID:$BEXHOMA_TENANT_ID"
    echo "SCHEMA_INDEX:$SCHEMA_INDEX"
    echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
    echo "BEXHOMA_SCHEMA:$BEXHOMA_SCHEMA"
    echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
    echo "BEXHOMA_NUM_PODS_TENANT:$BEXHOMA_NUM_PODS_TENANT"
elif [ "$BEXHOMA_TENANT_BY" = "database" ]; then
    echo "BEXHOMA_TENANT_BY is database"
    #BEXHOMA_NUM_PODS=1
    BEXHOMA_NUM_PODS=$(( BEXHOMA_NUM_PODS / BEXHOMA_TENANT_NUM ))
    BEXHOMA_NUM_PODS_TENANT="$BEXHOMA_NUM_PODS"
    #BEXHOMA_CHILD=$(( ( BEXHOMA_CHILD - 1 ) % BEXHOMA_TENANT_NUM + 1 ))
    #DB_INDEX=$(( ( BEXHOMA_CHILD - 1 ) / BEXHOMA_TENANT_NUM ))
    DB_INDEX=$(( ( BEXHOMA_CHILD - 1 ) % BEXHOMA_TENANT_NUM ))
    BEXHOMA_CHILD=$(( ( BEXHOMA_CHILD - 1 ) / BEXHOMA_TENANT_NUM + 1 ))
    BEXHOMA_DATABASE="tenant_${DB_INDEX}"
    #BEXHOMA_DATABASE="tenant_$((BEXHOMA_CHILD - 1))"
    BEXHOMA_TENANT_ID=$DB_INDEX
    echo "BEXHOMA_TENANT_ID:$BEXHOMA_TENANT_ID"
    echo "DB_INDEX:$DB_INDEX"
    echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
    echo "BEXHOMA_SCHEMA:$BEXHOMA_SCHEMA"
    echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
    echo "BEXHOMA_NUM_PODS_TENANT:$BEXHOMA_NUM_PODS_TENANT"
elif [ "$BEXHOMA_TENANT_BY" = "container" ]; then
    echo "BEXHOMA_TENANT_BY is container"
    echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
    echo "BEXHOMA_SCHEMA:$BEXHOMA_SCHEMA"
    echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
    echo "BEXHOMA_NUM_PODS:$BEXHOMA_NUM_PODS"
else
    echo "BEXHOMA_TENANT_BY is not set"
fi

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
    if test $BEXHOMA_NUM_PODS -gt 1
    then
        #destination_raw=/data/tpch/SF$SF/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD
        destination_raw=/tmp/tpch/SF$SF/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD
    else
        #destination_raw=/data/tpch/SF$SF
        destination_raw=/tmp/tpch/SF$SF
    fi
fi
echo "destination_raw:$destination_raw"
cd $destination_raw

######################## Show generated files ########################
echo "Found these files:"
ls $destination_raw/*tbl* -lh

######################## Multi-Tenant parameters ########################
BEXHOMA_NUM_PODS=$BEXHOMA_NUM_PODS_TMP

######################## Wait until all pods of job are ready ########################
if test $BEXHOMA_SYNCH_LOAD -gt 0
then
    echo "Decrementing job counter bexhoma-loader-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
    redis-cli -h 'bexhoma-messagequeue' decr "bexhoma-loader-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
    while : ; do
        PODS_MISSING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-loader-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
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

######################## Wait until all pods of experiment are ready ########################
if [ "$BEXHOMA_TENANT_BY" = "container" ]; then
    if test $BEXHOMA_SYNCH_LOAD -gt 0
    then
        echo "Decrementing experiment counter bexhoma-loader-podcount-exp-$BEXHOMA_EXPERIMENT"
        redis-cli -h 'bexhoma-messagequeue' decr "bexhoma-loader-podcount-exp-$BEXHOMA_EXPERIMENT"
        while : ; do
            PODS_MISSING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-loader-podcount-exp-$BEXHOMA_EXPERIMENT)"
            echo "Pods still missing in experiment: $PODS_MISSING"
            if [[ "$PODS_MISSING" =~ ^-?[0-9]+$ ]] && test "$PODS_MISSING" -le 0
            then
                echo "OK, all pods in experiment are ready."
                break
            else
                sleep 1
            fi
        done
    fi
fi

######################## Multi-Tenant parameters ########################
#BEXHOMA_NUM_PODS=1

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
        echo "skipping $basename, import is limited to other table ($TPCH_TABLE)"
        continue
    fi
    if [[ $basename == "nation" ]]
    then
        if [ "$BEXHOMA_CHILD" -gt 1 ] && [ -z "$BEXHOMA_TENANT_BY" ]; then
            continue
        fi
    fi
    if [[ $basename == "region" ]]
    then
        if [ "$BEXHOMA_CHILD" -gt 1 ] && [ -z "$BEXHOMA_TENANT_BY" ]; then
            continue
        fi
    fi
    #echo "Remove last character per line"
    #time sed 's/.$//' -i $i
    #COMMAND="COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|','\\n','\"' NULL AS ''"
    #COMMAND="COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|' NULL AS ''"
    COMMAND="\COPY $basename FROM '$i' delimiter '|' null ''"
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
        #time mclient --host $BEXHOMA_HOST --database $BEXHOMA_DATABASE --port $BEXHOMA_PORT -E UTF-8 -s "$COMMAND" - < $i &>OUTPUT.txt
        echo "PGOPTIONS='--search_path=$BEXHOMA_SCHEMA' psql -U $BEXHOMA_USER -d $BEXHOMA_DATABASE -h $BEXHOMA_HOST -p $BEXHOMA_PORT"
        time PGOPTIONS="--search_path=$BEXHOMA_SCHEMA" psql -U $BEXHOMA_USER -d $BEXHOMA_DATABASE -h $BEXHOMA_HOST -p $BEXHOMA_PORT -c "$COMMAND" &> /tmp/OUTPUT.txt
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
        if [[ $OUTPUT == *"copy $lines"* ]]; then echo "Import ok"; FAILED=0; fi
        # rollback, we have to do it again (?)
        #if [[ $OUTPUT == *"ROLLBACK"* ]]; then echo "ROLLBACK occured"; FAILED=1; fi
        # no thread left, we have to do it again (?)
        #if [[ $OUTPUT == *"failed to start worker thread"* ]]; then echo "No worker thread"; FAILED=1; fi
        #if [[ $OUTPUT == *"failed to start producer thread"* ]]; then echo "No producer thread"; FAILED=1; fi
        #if [[ $OUTPUT == *"Challenge string is not valid, it is empty"* ]]; then echo "No Login possible"; FAILED=1; fi
        # something else - what?
        #if [[ $OUTPUT == 2 ]]; then echo "Something unexpected happend"; fi
        FAILED=0
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

######################## Parameters summary ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_DATABASE_INITIAL:$BEXHOMA_DATABASE_INITIAL"
echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
echo "BEXHOMA_SCHEMA_INITIAL:$BEXHOMA_SCHEMA_INITIAL"
echo "BEXHOMA_SCHEMA:$BEXHOMA_SCHEMA"
echo "BEXHOMA_VOLUME:$BEXHOMA_VOLUME"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "BEXHOMA_TENANT_NUM:$BEXHOMA_TENANT_NUM"
echo "BEXHOMA_TENANT_BY:$BEXHOMA_TENANT_BY"
echo "BEXHOMA_CHILD_INITIAL:$BEXHOMA_CHILD_INITIAL"
echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS:$BEXHOMA_NUM_PODS"
echo "BEXHOMA_NUM_PODS_TENANT:$BEXHOMA_NUM_PODS_TENANT"
echo "SF:$SF"
echo "BEXHOMA_TENANT_ID:$BEXHOMA_TENANT_ID"
echo "destination_raw:$destination_raw"

######################## Exit successfully ###################
# while true; do sleep 2; done
exit 0
