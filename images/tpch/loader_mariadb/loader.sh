#!/bin/bash

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
CHILD=$(cat /tmp/tpch/CHILD )
echo "CHILD $CHILD"
echo "NUM_PODS $NUM_PODS"
echo "SF $SF"

######################## Destination of raw data ########################
if test $STORE_RAW_DATA -gt 0
then
    # store in (distributed) file system
    if test $NUM_PODS -gt 1
    then
        destination_raw=/data/tpch/SF$SF/$NUM_PODS/$CHILD
    else
        destination_raw=/data/tpch/SF$SF
    fi
else
    # only store locally
    destination_raw=/tmp/tpch/SF$SF/$NUM_PODS/$CHILD
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
        echo "Found $PODS_RUNNING / $NUM_PODS running pods"
        if  test "$PODS_RUNNING" == $NUM_PODS
        then
            echo "OK"
            break
        elif test "$PODS_RUNNING" -gt $NUM_PODS
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
        echo "skipping $basename, import is limited to other table ($TPCH_TABLE)"
        continue
    fi
    if [[ $basename == "nation" ]]
    then
        if test $CHILD -gt 1
        then
            continue
        fi
    fi
    if [[ $basename == "region" ]]
    then
        if test $CHILD -gt 1
        then
            continue
        fi
    fi
    if [[ $basename == "customer" ]]
    then
        COMMAND="LOAD DATA $MYSQL_LOADING_FROM INFILE '$i' INTO TABLE tpch.$basename FIELDS TERMINATED BY '|'
        (@c_custkey, @c_name, @c_address, @c_nationkey, @c_phone, @c_acctbal, @c_mktsegment, @c_comment) SET c_custkey=NULLIF(@c_custkey,''), c_name=NULLIF(@c_name,''), c_address=NULLIF(@c_address,''), c_nationkey=NULLIF(@c_nationkey,''), c_phone=NULLIF(@c_phone,''), c_acctbal=NULLIF(@c_acctbal,''), c_mktsegment=NULLIF(@c_mktsegment,''), c_comment=NULLIF(@c_comment,'')"
    fi
    if [[ $basename == "lineitem" ]]
    then
        COMMAND="LOAD DATA $MYSQL_LOADING_FROM INFILE '$i' INTO TABLE tpch.$basename FIELDS TERMINATED BY '|'
        (@l_orderkey, @l_partkey, @l_suppkey, @l_linenumber, @l_quantity, @l_extendedprice, @l_discount, @l_tax, @l_returnflag, @l_linestatus, @l_shipdate, @l_commitdate, @l_receiptdate, @l_shipinstruct, @l_shipmode, @l_comment) SET l_orderkey=NULLIF(@l_orderkey,''), l_partkey=NULLIF(@l_partkey,''), l_suppkey=NULLIF(@l_suppkey,''), l_linenumber=NULLIF(@l_linenumber,''), l_quantity=NULLIF(@l_quantity,''), l_extendedprice=NULLIF(@l_extendedprice,''), l_discount=NULLIF(@l_discount,''), l_tax=NULLIF(@l_tax,''), l_returnflag=NULLIF(@l_returnflag,''), l_linestatus=NULLIF(@l_linestatus,''), l_shipdate=NULLIF(@l_shipdate,''), l_commitdate=NULLIF(@l_commitdate,''), l_receiptdate=NULLIF(@l_receiptdate,''), l_shipinstruct=NULLIF(@l_shipinstruct,''), l_shipmode=NULLIF(@l_shipmode,''), l_comment=NULLIF(@l_comment,'')"
    fi
    if [[ $basename == "nation" ]]
    then
        COMMAND="LOAD DATA $MYSQL_LOADING_FROM INFILE '$i' INTO TABLE tpch.$basename FIELDS TERMINATED BY '|'
        (@n_nationkey, @n_name, @n_regionkey, @n_comment) SET n_nationkey=NULLIF(@n_nationkey,''), n_name=NULLIF(@n_name,''), n_regionkey=NULLIF(@n_regionkey,''), n_comment=NULLIF(@n_comment,'')"
    fi
    if [[ $basename == "orders" ]]
    then
        COMMAND="LOAD DATA $MYSQL_LOADING_FROM INFILE '$i' INTO TABLE tpch.$basename FIELDS TERMINATED BY '|'
        (@o_orderkey, @o_custkey, @o_orderstatus, @o_totalprice, @o_orderdate, @o_orderpriority, @o_clerk, @o_shippriority, @o_comment) SET o_orderkey=NULLIF(@o_orderkey,''), o_custkey=NULLIF(@o_custkey,''), o_orderstatus=NULLIF(@o_orderstatus,''), o_totalprice=NULLIF(@o_totalprice,''), o_orderdate=NULLIF(@o_orderdate,''), o_orderpriority=NULLIF(@o_orderpriority,''), o_clerk=NULLIF(@o_clerk,''), o_shippriority=NULLIF(@o_shippriority,''), o_comment=NULLIF(@o_comment,'')"
    fi
    if [[ $basename == "part" ]]
    then
        COMMAND="LOAD DATA $MYSQL_LOADING_FROM INFILE '$i' INTO TABLE tpch.$basename FIELDS TERMINATED BY '|'
        (@p_partkey, @p_name, @p_mfgr, @p_brand, @p_type, @p_size, @p_container, @p_retailprice, @p_comment) SET p_partkey=NULLIF(@p_partkey,''), p_name=NULLIF(@p_name,''), p_mfgr=NULLIF(@p_mfgr,''), p_brand=NULLIF(@p_brand,''), p_type=NULLIF(@p_type,''), p_size=NULLIF(@p_size,''), p_container=NULLIF(@p_container,''), p_retailprice=NULLIF(@p_retailprice,''), p_comment=NULLIF(@p_comment,'')"
    fi
    if [[ $basename == "partsupp" ]]
    then
        COMMAND="LOAD DATA $MYSQL_LOADING_FROM INFILE '$i' INTO TABLE tpch.$basename FIELDS TERMINATED BY '|'
        (@ps_partkey, @ps_suppkey, @ps_availqty, @ps_supplycost, @ps_comment) SET ps_partkey=NULLIF(@ps_partkey,''), ps_suppkey=NULLIF(@ps_suppkey,''), ps_availqty=NULLIF(@ps_availqty,''), ps_supplycost=NULLIF(@ps_supplycost,''), ps_comment=NULLIF(@ps_comment,'')"
    fi
    if [[ $basename == "region" ]]
    then
        COMMAND="LOAD DATA $MYSQL_LOADING_FROM INFILE '$i' INTO TABLE tpch.$basename FIELDS TERMINATED BY '|'
        (@r_regionkey, @r_name, @r_comment) SET r_regionkey=NULLIF(@r_regionkey,''), r_name=NULLIF(@r_name,''), r_comment=NULLIF(@r_comment,'')"
    fi
    if [[ $basename == "supplier" ]]
    then
        COMMAND="LOAD DATA $MYSQL_LOADING_FROM INFILE '$i' INTO TABLE tpch.$basename FIELDS TERMINATED BY '|'
        (@s_suppkey, @s_name, @s_address, @s_nationkey, @s_phone, @s_acctbal, @s_comment) SET s_suppkey=NULLIF(@s_suppkey,''), s_name=NULLIF(@s_name,''), s_address=NULLIF(@s_address,''), s_nationkey=NULLIF(@s_nationkey,''), s_phone=NULLIF(@s_phone,''), s_acctbal=NULLIF(@s_acctbal,''), s_comment=NULLIF(@s_comment,'')"
    fi
    #COMMAND="COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|','\\n','\"' NULL AS ''"
    #COMMAND="COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|' NULL AS ''"
    echo "============================"
    echo "$COMMAND"
    #OUTPUT="$(mclient --host $BEXHOMA_HOST --database $DATABASE --port $BEXHOMA_PORT -s \"COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|' NULL AS ''\" - < $i)"

    #FAILED=0 # everything ok
    #FAILED=1 # known error
    #FAILED=2 # unknown error
    FAILED=1
    while [ $FAILED == 1 ]
    do
        FAILED=2
        SECONDS_START=$SECONDS
        echo "=========="
        time mysql --host $BEXHOMA_HOST --database $DATABASE --port $BEXHOMA_PORT -e "$COMMAND" &> /tmp/OUTPUT.txt
        echo "Start $SECONDS_START seconds"
        SECONDS_END=$SECONDS
        echo "End $SECONDS_END seconds"
        DURATION=$((SECONDS_END-SECONDS_START))
        echo "Duration $DURATION seconds"
        #mclient --host $BEXHOMA_HOST --database $DATABASE --port $BEXHOMA_PORT -E UTF-8 -L import.log -s "$COMMAND" - < $i &>OUTPUT.txt
        #mclient --host $BEXHOMA_HOST --database $DATABASE --port $BEXHOMA_PORT -s "COPY $lines RECORDS INTO $basename FROM STDIN USING DELIMITERS '|','\\n','\"' NULL AS ''" - < $i &>OUTPUT.txt
        #cat import.log
        OUTPUT=$(cat /tmp/OUTPUT.txt )
        echo "$OUTPUT"
        FAILED=0
        # everything worked well ("row" and "rows" string checked)
        if [[ $OUTPUT == *"$lines affected row"* ]]; then echo "Import ok"; FAILED=0; fi
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
