#!/bin/bash

######################## Start timing ########################
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS

################### Turn Some Parameters into Numbers ###################
BEXHOMA_CHILD=${BEXHOMA_CHILD//[^0-9]/}
BEXHOMA_TENANT_NUM=${BEXHOMA_TENANT_NUM//[^0-9]/}

######################## Db2 client (not part of the image) ########################
# installs ibm_db from PyPI into the cache on the data volume, exports PYTHONPATH
source /tmp/install-driver.sh

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

######################## Data-job suffix for parallel-loading-job keys ########################
# Always set by Python (see LoadingCoordinator.start_pod()), even for a single
# loader entry, so this key suffix is unconditional here — no "only if there's
# more than one entry" branch to forget. Default covers manual/standalone runs.
BEXHOMA_DATA_JOB="${BEXHOMA_DATA_JOB:-1}"

######################## Read per-pod config from Redis ########################
BEXHOMA_POD_CONFIG_KEY="bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_DATA_JOB-config-$BEXHOMA_CHILD"
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
# load.py (ibm_db, IBM Data Server Driver for ODBC and CLI): remote external table
# (INSERT ... SELECT * FROM EXTERNAL ... REMOTESOURCE 'YES'), the file is sent by
# this pod. One transaction per chunk of DB2_LOAD_CHUNK_ROWS lines; several loader
# pods may load into the same table at the same time, and the primary keys of
# initschema-tpch.sql are maintained row by row. The generator strips the
# trailing '|' (TRANSFORM_RAW_DATA=1).
# The tables are in the default schema of BEXHOMA_USER unless BEXHOMA_SCHEMA is set.
FAILED_TABLES=""
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
    # only the first pod (of each tenant) loads the reference tables
    if [[ $basename == "nation" ]] || [[ $basename == "region" ]]
    then
        if [ "$BEXHOMA_CHILD" -gt 1 ]; then
            continue
        fi
    fi
    echo "============================"
    echo "load $basename from $i ($lines lines)"
    # #848: load.py retries a chunk only on known transient errors (no connection); any other
    # answer (error, fewer rows) fails this file, the pod exits 1 at the end; one BEXHOMA_INGEST line per file
    SECONDS_START_FILE=$SECONDS
    python3 /tmp/load.py "$basename" "$i" &> /tmp/OUTPUT.txt
    LOAD_RC=$?
    DURATION=$((SECONDS-SECONDS_START_FILE))
    echo "Duration $DURATION seconds, exit code $LOAD_RC"
    cat /tmp/OUTPUT.txt
    REPORTED=$(grep -oE '^BEXHOMA_LOADED:[0-9]+' /tmp/OUTPUT.txt | tail -1 | cut -d: -f2)
    if [ "$LOAD_RC" == "0" ] && [[ "$REPORTED" == "$lines" ]]
    then
        echo "Import ok"
        echo "BEXHOMA_INGEST:$i:$lines:$lines:ok"
    else
        echo "Import failed at $basename ($i, expected $lines rows, reported ${REPORTED:-none})"
        echo "BEXHOMA_INGEST:$i:$lines:$REPORTED:failed"
        FAILED_TABLES="$FAILED_TABLES $i"
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

######################## Exit ###################
# #848: a file that failed fails the pod (and the loading job, backoffLimit 0)
if [ -n "$FAILED_TABLES" ]
then
    echo "Failed tables:$FAILED_TABLES"
    exit 1
fi
exit 0
