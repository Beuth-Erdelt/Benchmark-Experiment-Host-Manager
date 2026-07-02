#!/bin/bash

######################## Start timing ########################
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS
bexhoma_start_epoch=$(date -u +%s)

######################## Show general parameters ########################
# MySQL uses BEXHOMA_VOLUME as the database name
BEXHOMA_DATABASE=$BEXHOMA_VOLUME
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
echo "BEXHOMA_VOLUME:$BEXHOMA_VOLUME"
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

######################## MySQL connection options ########################
# --skip-ssl: the Debian default-mysql-client is the MariaDB client, which can fail
# SSL negotiation with MySQL 8.x; --skip-ssl disables SSL, matching the loading loader.
MYSQL_OPTS="-h $BEXHOMA_HOST -P $BEXHOMA_PORT -u $BEXHOMA_USER -p$BEXHOMA_PASSWORD --local-infile=1 --skip-ssl"

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
    echo "RF1: inserting orders.tbl.u$K"
    mysql $MYSQL_OPTS $BEXHOMA_DATABASE -e \
        "LOAD DATA LOCAL INFILE '$destination_raw/orders.tbl.u$K'
         INTO TABLE orders FIELDS TERMINATED BY '|'
         (@o_orderkey, @o_custkey, @o_orderstatus, @o_totalprice, @o_orderdate,
          @o_orderpriority, @o_clerk, @o_shippriority, @o_comment)
         SET o_orderkey=NULLIF(@o_orderkey,''), o_custkey=NULLIF(@o_custkey,''),
             o_orderstatus=NULLIF(@o_orderstatus,''), o_totalprice=NULLIF(@o_totalprice,''),
             o_orderdate=NULLIF(@o_orderdate,''), o_orderpriority=NULLIF(@o_orderpriority,''),
             o_clerk=NULLIF(@o_clerk,''), o_shippriority=NULLIF(@o_shippriority,''),
             o_comment=NULLIF(@o_comment,'')"

    echo "RF1: inserting lineitem.tbl.u$K"
    mysql $MYSQL_OPTS $BEXHOMA_DATABASE -e \
        "LOAD DATA LOCAL INFILE '$destination_raw/lineitem.tbl.u$K'
         INTO TABLE lineitem FIELDS TERMINATED BY '|'
         (@l_orderkey, @l_partkey, @l_suppkey, @l_linenumber, @l_quantity,
          @l_extendedprice, @l_discount, @l_tax, @l_returnflag, @l_linestatus,
          @l_shipdate, @l_commitdate, @l_receiptdate, @l_shipinstruct,
          @l_shipmode, @l_comment)
         SET l_orderkey=NULLIF(@l_orderkey,''), l_partkey=NULLIF(@l_partkey,''),
             l_suppkey=NULLIF(@l_suppkey,''), l_linenumber=NULLIF(@l_linenumber,''),
             l_quantity=NULLIF(@l_quantity,''), l_extendedprice=NULLIF(@l_extendedprice,''),
             l_discount=NULLIF(@l_discount,''), l_tax=NULLIF(@l_tax,''),
             l_returnflag=NULLIF(@l_returnflag,''), l_linestatus=NULLIF(@l_linestatus,''),
             l_shipdate=NULLIF(@l_shipdate,''), l_commitdate=NULLIF(@l_commitdate,''),
             l_receiptdate=NULLIF(@l_receiptdate,''), l_shipinstruct=NULLIF(@l_shipinstruct,''),
             l_shipmode=NULLIF(@l_shipmode,''), l_comment=NULLIF(@l_comment,'')"

    #### RF2: delete orders identified in delete file ####
    echo "RF2: deleting rows from delete.$K"
    mysql $MYSQL_OPTS $BEXHOMA_DATABASE <<SQL
CREATE TEMPORARY TABLE _tpch_refresh_delete (orderkey BIGINT);
LOAD DATA LOCAL INFILE '$destination_raw/delete.$K'
    INTO TABLE _tpch_refresh_delete FIELDS TERMINATED BY '\n';
DELETE l FROM lineitem l WHERE l.l_orderkey IN (SELECT orderkey FROM _tpch_refresh_delete);
DELETE o FROM orders o WHERE o.o_orderkey IN (SELECT orderkey FROM _tpch_refresh_delete);
DROP TEMPORARY TABLE _tpch_refresh_delete;
SQL

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
echo "BEXHOMA_VOLUME:$BEXHOMA_VOLUME"
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

######################## Exit successfully ########################
exit 0
