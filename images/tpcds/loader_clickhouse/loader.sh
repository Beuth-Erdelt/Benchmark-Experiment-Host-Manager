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

######################## Show more parameters ########################
BEXHOMA_CHILD=$(cat /tmp/tpcds/BEXHOMA_CHILD )
echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS:$BEXHOMA_NUM_PODS"
echo "SF:$SF"
# BEXHOMA_PORT is the HTTP port of the SUT service (JDBC); clickhouse-client uses the native port
echo "CLICKHOUSE_PORT:$CLICKHOUSE_PORT"

######################## Data-job suffix for parallel-loading-job keys ########################
# Always set by Python, even for a single loader entry — no conditional needed.
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

######################## Destination of raw data ########################
if test $STORE_RAW_DATA -gt 0
then
    # store in (distributed) file system
    if test $BEXHOMA_NUM_PODS -gt 1
    then
        destination_raw=/data/tpcds/SF$SF/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD/
    else
        destination_raw=/data/tpcds/SF$SF/
    fi
else
    # only store locally
    destination_raw=/tmp/tpcds/SF$SF/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD
fi
echo "destination_raw:$destination_raw"
cd $destination_raw

######################## Show generated files ########################
echo "Found these files:"
ls $destination_raw/*.dat -lh

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
# '|'-separated, trailing '|' removed by the generator (TRANSFORM_RAW_DATA); empty fields
# load as NULL (Nullable columns); double quotes are data, not CSV quoting; a Distributed table (ClickHouseCluster) sends the rows to the
# shards before the INSERT returns, so the load time includes them
FAILED_TABLES=""
for i in *.dat; do
    if test $BEXHOMA_NUM_PODS -gt 1
    then
        basename=${i%_"$BEXHOMA_CHILD"_"$BEXHOMA_NUM_PODS"*}
    else
        basename=${i%.dat*}
    fi
    wordcount=($(wc -l $i))
    lines=${wordcount[0]}
    # skip table if limit to other table is set
    if [ -z "${TPCDS_TABLE}" ]
    then
        echo "table limit not set"
    elif [ "${TPCDS_TABLE}" == "$basename" ]
    then
        echo "limit import to this table $TPCDS_TABLE"
    else
        echo "skipping $basename, import is limited to other table ($TPCDS_TABLE)"
        continue
    fi
    echo "============================"
    echo "INSERT INTO $basename FORMAT CSV ($lines lines)"
    SECONDS_START_TABLE=$SECONDS
    time clickhouse-client --host $BEXHOMA_HOST --port $CLICKHOUSE_PORT --database $BEXHOMA_DATABASE \
        --format_csv_delimiter='|' --format_csv_allow_double_quotes=0 \
        --distributed_foreground_insert=1 \
        --query "INSERT INTO $basename FORMAT CSV" < $i &> /tmp/OUTPUT.txt
    EXITCODE=$?
    cat /tmp/OUTPUT.txt
    DURATION=$((SECONDS-SECONDS_START_TABLE))
    echo "Duration $DURATION seconds"
    if test $EXITCODE -eq 0
    then
        echo "Import ok"
    else
        # no retry: a failed INSERT may have written some blocks already
        echo "Import failed at $basename (exit code $EXITCODE)"
        FAILED_TABLES="$FAILED_TABLES $basename"
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
echo "destination_raw:$destination_raw"

######################## Exit ###################
if [ -n "$FAILED_TABLES" ]
then
    echo "Failed tables:$FAILED_TABLES"
    exit 1
fi
exit 0
