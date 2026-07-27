#!/bin/bash

######################## Start timing ########################
bexhoma_start_epoch=$(date -u +%s)
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "$DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS

######################## Show general parameters ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_EXPERIMENT:$BEXHOMA_EXPERIMENT"
BEXHOMA_DATABASE_INITIAL="$BEXHOMA_DATABASE"
echo "BEXHOMA_DATABASE_INITIAL:$BEXHOMA_DATABASE_INITIAL"
BEXHOMA_SCHEMA_INITIAL="$BEXHOMA_SCHEMA"
echo "BEXHOMA_SCHEMA_INITIAL:$BEXHOMA_SCHEMA_INITIAL"
echo "BEXHOMA_VOLUME:$BEXHOMA_VOLUME"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "BEXHOMA_DBMS:$BEXHOMA_DBMS"
echo "BEXHOMA_TENANT_NUM:$BEXHOMA_TENANT_NUM"
echo "BEXHOMA_TENANT_BY:$BEXHOMA_TENANT_BY"

######################## Data-job suffix for parallel-loading-job keys ########################
# Always set by Python, even for a single loader entry — no conditional needed.
BEXHOMA_DATA_JOB="${BEXHOMA_DATA_JOB:-1}"

######################## Get number of client in job queue ########################
# Queue is scoped by BEXHOMA_EXPERIMENT_RUN because loading (and this chunk
# assignment) is redone from scratch for every experiment_run, not once per
# experiment -- reusing an unscoped key would risk picking up a leftover
# entry from a previous run's queue.
echo "Querying message queue bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_DATA_JOB"
BEXHOMA_CHILD="$(redis-cli -h 'bexhoma-messagequeue' lpop bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_DATA_JOB)"
if [ -z "$BEXHOMA_CHILD" ]
then
    # Do not default to a fixed chunk index here: another pod may already own
    # it, and silently duplicating its chunk (while some other chunk never
    # gets loaded at all) is far worse than failing the pod outright.
    echo "FATAL: no chunk index available from message queue bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_DATA_JOB (queue empty or Redis unreachable)"
    exit 1
else
    echo "Found entry number $BEXHOMA_CHILD in message queue."
fi

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

######################## Patch parameters ########################
if [ "$BENCHBASE_TERMINALS" = "0" ]; then
    BENCHBASE_TERMINALS="unlimited"
fi

############ Show more parameters ############
echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS:$BEXHOMA_NUM_PODS"
echo "SF:$SF"
BENCHBASE_BENCH_INITIAL="$BENCHBASE_BENCH"
echo "BENCHBASE_BENCH_INITIAL:$BENCHBASE_BENCH_INITIAL"
echo "BENCHBASE_PROFILE:$BENCHBASE_PROFILE"
echo "BENCHBASE_TARGET:$BENCHBASE_TARGET"
echo "BENCHBASE_TIME:$BENCHBASE_TIME"
echo "BENCHBASE_TERMINALS:$BENCHBASE_TERMINALS"
echo "BENCHBASE_BATCHSIZE:$BENCHBASE_BATCHSIZE"
echo "BENCHBASE_CREATE_SCHEMA:$BENCHBASE_CREATE_SCHEMA"
echo "BENCHBASE_NEWCONNPERTXN:$BENCHBASE_NEWCONNPERTXN"

######################## Multi-Tenant parameters ########################
BEXHOMA_NUM_PODS_TMP=$BEXHOMA_NUM_PODS
if [ "$BEXHOMA_TENANT_BY" = "schema" ]; then
    echo "BEXHOMA_TENANT_BY is schema"
    BEXHOMA_NUM_PODS=1
    BEXHOMA_SCHEMA="tenant_$((BEXHOMA_CHILD - 1))"
    BEXHOMA_TENANT_ID=$((BEXHOMA_CHILD - 1))
    echo "BEXHOMA_SCHEMA:$BEXHOMA_SCHEMA"
    echo "BEXHOMA_TENANT_ID:$BEXHOMA_TENANT_ID"
elif [ "$BEXHOMA_TENANT_BY" = "database" ]; then
    echo "BEXHOMA_TENANT_BY is database"
    BEXHOMA_NUM_PODS=1
    BEXHOMA_DATABASE="tenant_$((BEXHOMA_CHILD - 1))"
    BEXHOMA_TENANT_ID=$((BEXHOMA_CHILD - 1))
    echo "BEXHOMA_DATABASE:$BEXHOMA_DATABASE"
    echo "BEXHOMA_TENANT_ID:$BEXHOMA_TENANT_ID"
else
    echo "BEXHOMA_TENANT_BY is not set"
    echo "BEXHOMA_TENANT_ID:$BEXHOMA_TENANT_ID"
fi
######################## Multi-Tenant parameters ########################
BEXHOMA_NUM_PODS=$BEXHOMA_NUM_PODS_TMP

######################## Wait until all pods of job are ready ########################
if test "${BEXHOMA_SYNCH_LOAD:-0}" -gt 0
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
    ######################## Wait until all pods of round are ready ########################
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
    ######################## Wait until all pods of experiment are ready ########################
    if [ "$BEXHOMA_TENANT_BY" = "container" ]; then
        echo "Decrementing experiment counter bexhoma-generator-podcount-exp-$BEXHOMA_EXPERIMENT"
        redis-cli -h 'bexhoma-messagequeue' decr "bexhoma-generator-podcount-exp-$BEXHOMA_EXPERIMENT"
        while : ; do
            PODS_MISSING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-generator-podcount-exp-$BEXHOMA_EXPERIMENT)"
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
else
    echo "Start immediately without waiting for other pods"
fi

############ Start measurement of time of execution ############
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"
bexhoma_start_epoch=$(date -u +%s)

######################## Benchmark Config File ###################
if [ "$BENCHBASE_BENCH" == "tpcc" ]; then
    FILENAME=/tmp/config/$BENCHBASE_PROFILE/sample_tpcc_config.xml
elif [ "$BENCHBASE_BENCH" == "twitter" ]; then
    FILENAME=/tmp/config/$BENCHBASE_PROFILE/sample_twitter_config.xml
elif [ "$BENCHBASE_BENCH" == "chbenchmark" ]; then
    FILENAME=/tmp/config/$BENCHBASE_PROFILE/sample_chbenchmark_config.xml
	BENCHBASE_BENCH="tpcc,chbenchmark"
elif [ "$BENCHBASE_BENCH" == "ycsb" ]; then
    FILENAME=/tmp/config/$BENCHBASE_PROFILE/sample_ycsb_config.xml
else
    echo "Unknown benchmark"
    exit 0
fi

######################## Show workload file ###################
echo "FILENAME:$FILENAME"

######################## Remove schema parameter from PGBouncer URL ###################
if [[ "$BEXHOMA_DBMS" == "PGBouncer" ]]; then
    sed -i 's/&amp;currentSchema=BEXHOMA_SCHEMA//g' "$FILENAME"
fi

######################## Replace parameters in workload file ###################
if [[ "$BENCHBASE_BENCH" == "ycsb" && "$BENCHBASE_YCSB_WORKLOAD" == "a" ]]; then
    BENCHBASE_YCSB_WEIGHTS=50,0,0,50,0,0
elif [[ "$BENCHBASE_BENCH" == "ycsb" && "$BENCHBASE_YCSB_WORKLOAD" == "b" ]]; then
    BENCHBASE_YCSB_WEIGHTS=95,0,0,5,0,0
elif [[ "$BENCHBASE_BENCH" == "ycsb" && "$BENCHBASE_YCSB_WORKLOAD" == "c" ]]; then
    BENCHBASE_YCSB_WEIGHTS=100,0,0,0,0,0
elif [[ "$BENCHBASE_BENCH" == "ycsb" && "$BENCHBASE_YCSB_WORKLOAD" == "d" ]]; then
    BENCHBASE_YCSB_WEIGHTS=95,5,0,0,0,0
elif [[ "$BENCHBASE_BENCH" == "ycsb" && "$BENCHBASE_YCSB_WORKLOAD" == "e" ]]; then
    BENCHBASE_YCSB_WEIGHTS=0,5,95,0,0,0
elif [[ "$BENCHBASE_BENCH" == "ycsb" && "$BENCHBASE_YCSB_WORKLOAD" == "f" ]]; then
    BENCHBASE_YCSB_WEIGHTS=50,0,0,0,0,50
fi

echo "FILENAME:$FILENAME"

sed -i "s/BEXHOMA_HOST/$BEXHOMA_HOST/" $FILENAME
sed -i "s/BEXHOMA_PORT/$BEXHOMA_PORT/" $FILENAME
sed -i "s/BEXHOMA_USER/$BEXHOMA_USER/" $FILENAME
sed -i "s/BEXHOMA_PASSWORD/$BEXHOMA_PASSWORD/" $FILENAME
sed -i "s/BEXHOMA_DATABASE/$BEXHOMA_DATABASE/" $FILENAME
sed -i "s/BEXHOMA_SCHEMA/$BEXHOMA_SCHEMA/" $FILENAME
sed -i "s/BENCHBASE_TIME/$BENCHBASE_TIME/" $FILENAME
sed -i "s/BENCHBASE_TARGET/$BENCHBASE_TARGET/" $FILENAME
sed -i "s/BEXHOMA_SF/$SF/" $FILENAME
sed -i "s/BENCHBASE_BATCHSIZE/$BENCHBASE_BATCHSIZE/" $FILENAME
sed -i "s/BENCHBASE_TERMINALS/$BENCHBASE_TERMINALS/" $FILENAME
sed -i "s/BENCHBASE_ISOLATION/$BENCHBASE_ISOLATION/" $FILENAME
sed -i "s/BENCHBASE_NEWCONNPERTXN/$BENCHBASE_NEWCONNPERTXN/" $FILENAME
sed -i "s/BENCHBASE_YCSB_WEIGHTS/$BENCHBASE_YCSB_WEIGHTS/" $FILENAME

cat $FILENAME

ls -lh

pwd

######################## Execute workload ###################
if echo "$BENCHBASE_STATUS_INTERVAL" | grep -qE '^[0-9]+$'; then
    echo "Benchbase dump status"
	time sh ./entrypoint.sh run --bench $BENCHBASE_BENCH -c $FILENAME --create=$BENCHBASE_CREATE_SCHEMA --load=true --execute=false  --interval-monitor $BENCHBASE_STATUS_INTERVAL
else
	time sh ./entrypoint.sh run --bench $BENCHBASE_BENCH -c $FILENAME --create=$BENCHBASE_CREATE_SCHEMA --load=true --execute=false
fi



######################## End time measurement ###################
SECONDS_END=$SECONDS
echo "End $SECONDS_END seconds"

DURATION=$((SECONDS_END-SECONDS_START))
echo "Duration $DURATION seconds"

######################## Show result files ###################
ls -lh /benchbase/results

######################## Show result summary ###################
echo "####BEXHOMA####"
cat /benchbase/results/*.summary.json
echo "####BEXHOMA####"

######################## Show timing information ###################
echo "Generating done"

DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "$DATEANDTIME"

SECONDS_END_SCRIPT=$SECONDS
DURATION_SCRIPT=$((SECONDS_END_SCRIPT-SECONDS_START_SCRIPT))
echo "Duration $DURATION_SCRIPT seconds"
echo "BEXHOMA_DURATION:$DURATION_SCRIPT"

bexhoma_end_epoch=$(date -u +%s)
echo "BEXHOMA_START:$bexhoma_start_epoch"
echo "BEXHOMA_END:$bexhoma_end_epoch"

######################## Parameters summary ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_EXPERIMENT:$BEXHOMA_EXPERIMENT"
echo "BEXHOMA_DATABASE_INITIAL:$BEXHOMA_DATABASE_INITIAL"
echo "BEXHOMA_SCHEMA_INITIAL:$BEXHOMA_SCHEMA_INITIAL"
echo "BEXHOMA_VOLUME:$BEXHOMA_VOLUME"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "BEXHOMA_DBMS:$BEXHOMA_DBMS"
echo "BEXHOMA_TENANT_NUM:$BEXHOMA_TENANT_NUM"
echo "BEXHOMA_TENANT_BY:$BEXHOMA_TENANT_BY"
echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS:$BEXHOMA_NUM_PODS"
echo "SF:$SF"
echo "BENCHBASE_BENCH_INITIAL:$BENCHBASE_BENCH_INITIAL"
echo "BENCHBASE_PROFILE:$BENCHBASE_PROFILE"
echo "BENCHBASE_TARGET:$BENCHBASE_TARGET"
echo "BENCHBASE_TIME:$BENCHBASE_TIME"
echo "BENCHBASE_TERMINALS:$BENCHBASE_TERMINALS"
echo "BENCHBASE_BATCHSIZE:$BENCHBASE_BATCHSIZE"
echo "BENCHBASE_CREATE_SCHEMA:$BENCHBASE_CREATE_SCHEMA"
echo "BENCHBASE_NEWCONNPERTXN:$BENCHBASE_NEWCONNPERTXN"
echo "BEXHOMA_TENANT_ID:$BEXHOMA_TENANT_ID"
echo "FILENAME:$FILENAME"

######################## Exit successfully ###################
exit 0
