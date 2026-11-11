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
echo "BEXHOMA_HOST:$BEXHOMA_HOST"
echo "BEXHOMA_PORT:$BEXHOMA_PORT"
echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
echo "BEXHOMA_SCHEMA:$BEXHOMA_SCHEMA"
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
######################## Result per unit (#848) ########################
# one BEXHOMA_INGEST line per statement; a failed one fails the pod at the end
FAILED_UNITS=""
ingest_result() {
    # $1 unit, $2 expected rows (empty: not known), $3 reported rows, $4 exit code of the client
    if [ "$4" -eq 0 ] && { [ -z "$2" ] || [ "$2" == "$3" ]; }
    then
        echo "BEXHOMA_INGEST:$1:$2:$3:ok"
    else
        echo "Refresh failed at $1 (exit code $4, expected ${2:-?} rows, reported ${3:-none})"
        echo "BEXHOMA_INGEST:$1:$2:$3:failed"
        FAILED_UNITS="$FAILED_UNITS $1"
    fi
}

# the JDBC database of the connection is master; the TPC-H database is the volume (as for MySQL)
BEXHOMA_DATABASE=${BEXHOMA_VOLUME:-$BEXHOMA_DATABASE}
echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
if [ -z "$BEXHOMA_SCHEMA" ]; then BEXHOMA_SCHEMA_BCP=dbo; else BEXHOMA_SCHEMA_BCP=$BEXHOMA_SCHEMA; fi
# sqlcmd/bcp of mssql-tools18: -C/-u trust the self-signed certificate, -b exits 1 on an error
SQLCMD="sqlcmd -S $BEXHOMA_HOST,$BEXHOMA_PORT -U $BEXHOMA_USER -P $BEXHOMA_PASSWORD -d $BEXHOMA_DATABASE -C -b -I"

for K in $(seq $FIRST_SET $LAST_SET); do
    echo "============================"
    echo "Applying refresh set $K"

    #### RF1: insert new orders and lineitems ####
    # one transaction per file; the generator strips the trailing '|', rows end with LF (0x0a)
    for TABLE in orders lineitem; do
        echo "RF1: inserting $TABLE.tbl.u$K"
        expected=$(wc -l < "$destination_raw/$TABLE.tbl.u$K")
        bcp "$BEXHOMA_SCHEMA_BCP.$TABLE" in "$destination_raw/$TABLE.tbl.u$K" \
            -S "$BEXHOMA_HOST,$BEXHOMA_PORT" -U "$BEXHOMA_USER" -P "$BEXHOMA_PASSWORD" -d "$BEXHOMA_DATABASE" \
            -u -c -t '|' -r 0x0a -m 1 &> /tmp/OUTPUT.txt
        RC=$?
        cat /tmp/OUTPUT.txt
        reported=$(grep -oE '[0-9]+ rows copied' /tmp/OUTPUT.txt | head -1 | cut -d' ' -f1)
        ingest_result "rf1-$TABLE-$K" "$expected" "$reported" $RC
    done

    #### RF2: delete orders identified in delete file ####
    # the order keys go into a staging table of this set (bcp needs a table, a #temp
    # table would not survive the connection); no expected count: a set applied again
    # (reused volume) deletes nothing
    echo "RF2: deleting rows from delete.$K"
    STAGE="$BEXHOMA_SCHEMA_BCP.tpch_refresh_delete_$K"
    RC=0
    $SQLCMD -Q "DROP TABLE IF EXISTS $STAGE; CREATE TABLE $STAGE (orderkey BIGINT NOT NULL);" &> /tmp/OUTPUT.txt || RC=$?
    cat /tmp/OUTPUT.txt
    if [ $RC -eq 0 ]; then
        bcp "$STAGE" in "$destination_raw/delete.$K" \
            -S "$BEXHOMA_HOST,$BEXHOMA_PORT" -U "$BEXHOMA_USER" -P "$BEXHOMA_PASSWORD" -d "$BEXHOMA_DATABASE" \
            -u -c -t '|' -r 0x0a -m 1 &> /tmp/OUTPUT.txt || RC=$?
        cat /tmp/OUTPUT.txt
    fi
    if [ $RC -eq 0 ]; then
        $SQLCMD -Q "SET XACT_ABORT ON; BEGIN TRANSACTION; DELETE FROM $BEXHOMA_SCHEMA_BCP.lineitem WHERE l_orderkey IN (SELECT orderkey FROM $STAGE); DELETE FROM $BEXHOMA_SCHEMA_BCP.orders WHERE o_orderkey IN (SELECT orderkey FROM $STAGE); COMMIT;" &> /tmp/OUTPUT.txt || RC=$?
        cat /tmp/OUTPUT.txt
    fi
    $SQLCMD -Q "DROP TABLE IF EXISTS $STAGE;" &> /tmp/OUTPUT.txt
    cat /tmp/OUTPUT.txt
    ingest_result "rf2-$K" "" "" $RC

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
echo "BEXHOMA_EXPERIMENT:$BEXHOMA_EXPERIMENT"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "BEXHOMA_HOST:$BEXHOMA_HOST"
echo "BEXHOMA_PORT:$BEXHOMA_PORT"
echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
echo "BEXHOMA_SCHEMA:$BEXHOMA_SCHEMA"
echo "SF:$SF"
echo "TPCH_REFRESH_STREAMS:$TPCH_REFRESH_STREAMS"
echo "TPCH_REFRESH_STREAM_OFFSET:$TPCH_REFRESH_STREAM_OFFSET"
echo "destination_raw:$destination_raw"

######################## Exit ########################
if test -n "$FAILED_UNITS"
then
    echo "Refresh stream failed:$FAILED_UNITS"
    exit 1
fi
exit 0
