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

# Oracle: the schema is the user of the JDBC connection (BEXHOMA_DATABASE), unless BEXHOMA_SCHEMA is set
if [ -z "$BEXHOMA_SCHEMA" ]; then BEXHOMA_SCHEMA_LOAD=$BEXHOMA_DATABASE; else BEXHOMA_SCHEMA_LOAD=$BEXHOMA_SCHEMA; fi
echo "BEXHOMA_SCHEMA_LOAD:$BEXHOMA_SCHEMA_LOAD"
# password in a parameter file and a login script, not on the command line (ps)
umask 077
CONNECT="$BEXHOMA_USER/\"$BEXHOMA_PASSWORD\"@//$BEXHOMA_HOST:$BEXHOMA_PORT/$ORACLE_SERVICE"
echo "userid=$CONNECT" > /tmp/sqlldr.par
echo "CONNECT $CONNECT" > /tmp/connect.sql
# sqlplus: stops at the first error with exit code 1
run_sql() {
    { echo "WHENEVER SQLERROR EXIT FAILURE"; echo "WHENEVER OSERROR EXIT FAILURE"; echo "SET FEEDBACK ON"; echo "@/tmp/connect.sql"; echo "$1"; echo "EXIT"; } \
        | sqlplus -S -L /nolog
}
# SQL*Loader: the reported rows of the log; ERRORS=0 stops at the first bad row
run_sqlldr() {
    # $1 control file (in /tmp/ctl), $2 table, $3 data file
    sed "s/BEXHOMA_TABLE/$2/" /tmp/ctl/$1.ctl > /tmp/run_$1.ctl
    rm -f /tmp/run_$1.log
    sqlldr parfile=/tmp/sqlldr.par control=/tmp/run_$1.ctl data="$3" log=/tmp/run_$1.log bad=/tmp/run_$1.bad errors=0 rows=50000 bindsize=20000000 readsize=20000000 silent=header,feedback
    RC=$?
    grep -E 'Rows? (successfully loaded|not loaded due to data errors)|^(ORA|SQL\*Loader)-[0-9]+' /tmp/run_$1.log 2>/dev/null
    REPORTED=$(grep -oE '[0-9]+ Rows? successfully loaded' /tmp/run_$1.log 2>/dev/null | head -1 | cut -d' ' -f1)
    return $RC
}

for K in $(seq $FIRST_SET $LAST_SET); do
    echo "============================"
    echo "Applying refresh set $K"

    #### RF1: insert new orders and lineitems ####
    # conventional path (the query streams run at the same time), one commit per 50000 rows;
    # the generator strips the trailing '|'
    for TABLE in orders lineitem; do
        echo "RF1: inserting $TABLE.tbl.u$K"
        expected=$(wc -l < "$destination_raw/$TABLE.tbl.u$K")
        run_sqlldr $TABLE "$BEXHOMA_SCHEMA_LOAD.$TABLE" "$destination_raw/$TABLE.tbl.u$K"
        RC=$?
        ingest_result "rf1-$TABLE-$K" "$expected" "$REPORTED" $RC
    done

    #### RF2: delete orders identified in delete file ####
    # the order keys go into a staging table of this set (SQL*Loader needs a table), then one
    # transaction deletes lineitems and orders; no expected count: a set applied again
    # (reused volume) deletes nothing
    echo "RF2: deleting rows from delete.$K"
    STAGE="$BEXHOMA_SCHEMA_LOAD.tpch_refresh_delete_$K"
    RC=0
    run_sql "DROP TABLE IF EXISTS $STAGE PURGE;
CREATE TABLE $STAGE (orderkey NUMBER(12) NOT NULL);" || RC=$?
    if [ $RC -eq 0 ]; then
        run_sqlldr delete "$STAGE" "$destination_raw/delete.$K" || RC=$?
    fi
    if [ $RC -eq 0 ]; then
        run_sql "DELETE FROM $BEXHOMA_SCHEMA_LOAD.lineitem WHERE l_orderkey IN (SELECT orderkey FROM $STAGE);
DELETE FROM $BEXHOMA_SCHEMA_LOAD.orders WHERE o_orderkey IN (SELECT orderkey FROM $STAGE);
COMMIT;" || RC=$?
    fi
    run_sql "DROP TABLE IF EXISTS $STAGE PURGE;"
    ingest_result "rf2-$K" "" "" $RC

    echo "Refresh set $K done"
done
rm -f /tmp/sqlldr.par /tmp/connect.sql

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
