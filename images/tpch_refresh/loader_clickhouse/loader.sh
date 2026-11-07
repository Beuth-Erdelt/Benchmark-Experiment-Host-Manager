#!/bin/bash

######################## Start timing ########################
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS
bexhoma_start_epoch=$(date -u +%s)

######################## Show general parameters ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
echo "BEXHOMA_EXPERIMENT:$BEXHOMA_EXPERIMENT"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "BEXHOMA_HOST:$BEXHOMA_HOST"
echo "BEXHOMA_PORT:$BEXHOMA_PORT"
echo "CLICKHOUSE_PORT:$CLICKHOUSE_PORT"
echo "BEXHOMA_CLICKHOUSE_CLUSTER:$BEXHOMA_CLICKHOUSE_CLUSTER"
echo "SF:$SF"
echo "TPCH_REFRESH_STREAMS:$TPCH_REFRESH_STREAMS"
echo "TPCH_REFRESH_STREAM_OFFSET:$TPCH_REFRESH_STREAM_OFFSET"

######################## Compute set range ########################
FIRST_SET=$((TPCH_REFRESH_STREAM_OFFSET + 1))
LAST_SET=$((TPCH_REFRESH_STREAM_OFFSET + TPCH_REFRESH_STREAMS))
echo "Applying refresh sets $FIRST_SET to $LAST_SET"

######################## Destination of raw data ########################
if test $STORE_RAW_DATA -gt 0
then
    destination_raw=/data/tpch-refresh/SF$SF
else
    destination_raw=/tmp/tpch-refresh/SF$SF
fi
echo "destination_raw:$destination_raw"
cd $destination_raw

######################## Show refresh files ########################
echo "Found these refresh files:"
ls $destination_raw -lh

######################## ClickHouse connection and table options ########################
# Native protocol (BEXHOMA_PORT is the HTTP port of the service, used by JDBC).
# The host is not part of CLICKHOUSE_CLIENT: clickhouse-client takes the first --host it is given.
CLICKHOUSE_CLIENT="clickhouse-client --port $CLICKHOUSE_PORT --database $BEXHOMA_DATABASE"
CLICKHOUSE="$CLICKHOUSE_CLIENT --host $BEXHOMA_HOST"
# '|'-separated, trailing '|' removed by the generator (TRANSFORM_RAW_DATA); double quotes are data.
# A Distributed table sends the rows to the shards before the INSERT returns.
CSV_OPTS="--format_csv_delimiter=| --format_csv_allow_double_quotes=0 --distributed_foreground_insert=1"
# On a cluster, orders and lineitem are Distributed tables on top of <name>_local on every shard,
# and a Distributed table cannot be deleted from: RF2 runs on the local tables of all shards.
# The coordinator holds only the Distributed tables, so the loader connects to each shard.
DELETE_SUFFIX=""
DELETE_HOSTS="$BEXHOMA_HOST"
if test -n "$BEXHOMA_CLICKHOUSE_CLUSTER"
then
    DELETE_SUFFIX="_local"
    DELETE_HOSTS=$($CLICKHOUSE --query "SELECT host_name FROM system.clusters WHERE cluster = '$BEXHOMA_CLICKHOUSE_CLUSTER' ORDER BY shard_num, replica_num")
    echo "RF2 runs on: $DELETE_HOSTS"
fi
# lightweight DELETE, returns when the rows are masked on all replicas
DELETE_OPTS="--lightweight_deletes_sync=2 --max_query_size=4194304"
# order keys per DELETE statement, keeps the statement far below max_query_size
KEYS_PER_DELETE=10000
FAILED=""

######################## Wait until all pods of job are ready ########################
echo "Decrementing job counter bexhoma-benchmarker-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
redis-cli -h 'bexhoma-messagequeue' decr "bexhoma-benchmarker-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
while : ; do
    PODS_MISSING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-benchmarker-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
    echo "Pods still missing in job: $PODS_MISSING"
    if [[ "$PODS_MISSING" =~ ^-?[0-9]+$ ]] && test "$PODS_MISSING" -le 0
    then
        echo "OK, all pods in job are ready."
        break
    else
        sleep 1
    fi
done

######################## Wait until all pods of round are ready ########################
echo "Decrementing round counter bexhoma-benchmarker-podcount-round-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_CLIENT-$BEXHOMA_CONFIGURATION-$BEXHOMA_EXPERIMENT"
redis-cli -h 'bexhoma-messagequeue' decr "bexhoma-benchmarker-podcount-round-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_CLIENT-$BEXHOMA_CONFIGURATION-$BEXHOMA_EXPERIMENT"
while : ; do
    PODS_MISSING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-benchmarker-podcount-round-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_CLIENT-$BEXHOMA_CONFIGURATION-$BEXHOMA_EXPERIMENT)"
    echo "Pods still missing in round: $PODS_MISSING"
    if [[ "$PODS_MISSING" =~ ^-?[0-9]+$ ]] && test "$PODS_MISSING" -le 0
    then
        echo "OK, all pods in round are ready."
        break
    else
        sleep 1
    fi
done

######################## Start measurement of time ########################
bexhoma_start_epoch=$(date -u +%s)
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"

######################## Apply RF1 and RF2 for each refresh set ########################
for K in $(seq $FIRST_SET $LAST_SET); do
    echo "============================"
    echo "Applying refresh set $K"

    #### RF1: insert new orders and lineitems ####
    for TABLE in orders lineitem; do
        echo "RF1: inserting $TABLE.tbl.u$K"
        $CLICKHOUSE $CSV_OPTS --query "INSERT INTO $TABLE FORMAT CSV" < $destination_raw/$TABLE.tbl.u$K
        if test $? -ne 0
        then
            echo "RF1 failed at $TABLE of set $K"
            FAILED="$FAILED RF1:$TABLE:$K"
        fi
    done

    #### RF2: delete orders identified in delete file, lineitem first ####
    echo "RF2: deleting rows from delete.$K"
    KEY_CHUNKS=/tmp/keys.$K.
    split -l $KEYS_PER_DELETE $destination_raw/delete.$K $KEY_CHUNKS
    for CHUNK in ${KEY_CHUNKS}*; do
        KEYS=$(paste -sd, $CHUNK)
        for DELETE_HOST in $DELETE_HOSTS; do
            $CLICKHOUSE_CLIENT --host $DELETE_HOST $DELETE_OPTS --query \
                "DELETE FROM lineitem$DELETE_SUFFIX WHERE l_orderkey IN ($KEYS)"
            if test $? -ne 0
            then
                echo "RF2 failed at lineitem of set $K ($CHUNK) on $DELETE_HOST"
                FAILED="$FAILED RF2:lineitem:$K"
            fi
            $CLICKHOUSE_CLIENT --host $DELETE_HOST $DELETE_OPTS --query \
                "DELETE FROM orders$DELETE_SUFFIX WHERE o_orderkey IN ($KEYS)"
            if test $? -ne 0
            then
                echo "RF2 failed at orders of set $K ($CHUNK) on $DELETE_HOST"
                FAILED="$FAILED RF2:orders:$K"
            fi
        done
        rm -f $CHUNK
    done

    echo "Refresh set $K done"
done

######################## End measurement of time ########################
bexhoma_end_epoch=$(date -u +%s)
SECONDS_END_SCRIPT=$SECONDS
DURATION_SCRIPT=$((SECONDS_END_SCRIPT-SECONDS_START_SCRIPT))

echo "Refresh stream done"
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"
echo "Duration $DURATION_SCRIPT seconds (script total)"
echo "BEXHOMA_DURATION:$DURATION_SCRIPT"
echo "BEXHOMA_START:$bexhoma_start_epoch"
echo "BEXHOMA_END:$bexhoma_end_epoch"

######################## Parameters summary ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
echo "BEXHOMA_EXPERIMENT:$BEXHOMA_EXPERIMENT"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "BEXHOMA_HOST:$BEXHOMA_HOST"
echo "BEXHOMA_PORT:$BEXHOMA_PORT"
echo "SF:$SF"
echo "TPCH_REFRESH_STREAMS:$TPCH_REFRESH_STREAMS"
echo "TPCH_REFRESH_STREAM_OFFSET:$TPCH_REFRESH_STREAM_OFFSET"
echo "destination_raw:$destination_raw"

######################## Exit ########################
# no retry on failure: a repeated RF1 would insert the rows twice (no primary key to refuse them)
if test -n "$FAILED"
then
    echo "Refresh stream failed:$FAILED"
    exit 1
fi
exit 0
