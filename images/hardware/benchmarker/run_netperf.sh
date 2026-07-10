#!/bin/bash

######################## Show parameters ########################
echo "BEXHOMA_HOST:$BEXHOMA_HOST"
echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
echo "HARDWARE_DURATION:$HARDWARE_DURATION"
echo "HARDWARE_THREADS:$HARDWARE_THREADS"
echo "HARDWARE_NETPERF_PROTOCOL:$HARDWARE_NETPERF_PROTOCOL"

######################## Pick this pod's slice of the fixed data-port pool ########################
# netperf has no built-in concurrency (one client process = one connection; see
# https://github.com/Mellanox/sockperf/issues/133-style limitation, except netperf's
# manual documents running many instances as the supported way to get aggregate
# concurrency - "Care and Feeding of Netperf", section 7). HARDWARE_THREADS concurrent
# client instances are launched below, each pinned via netperf's test-specific
# "-P local,remote" option to its own port out of [NETPERF_DATA_BASE_PORT,
# NETPERF_DATA_BASE_PORT+NETPERF_DATA_NUM_PORTS) - required because the k8s Service
# only forwards explicitly declared ports (see k8s/deploymenttemplate-Hardware.yml),
# so an OS-assigned ephemeral data port would be unreachable. Each pod's slice starts
# at (BEXHOMA_CHILD-1)*HARDWARE_THREADS, which is safe (no two pods' slices overlap)
# because every pod in one round is launched with the same HARDWARE_THREADS value.
POOL_START=$(( (BEXHOMA_CHILD - 1) * HARDWARE_THREADS ))
POOL_END=$(( POOL_START + HARDWARE_THREADS ))
if [ "$POOL_END" -gt "$NETPERF_DATA_NUM_PORTS" ]; then
    echo "Error: this pod's data-port slice [$POOL_START,$POOL_END) exceeds the" \
         "NETPERF_DATA_NUM_PORTS=$NETPERF_DATA_NUM_PORTS pool - reduce -nbt/-nbp or" \
         "raise NETPERF_DATA_NUM_PORTS (images/hardware/sut/Dockerfile and" \
         "k8s/deploymenttemplate-Hardware.yml must then expose the wider range too)."
    exit 1
fi

######################## Pick netperf test type ########################
if [ "$HARDWARE_NETPERF_PROTOCOL" = "udp" ]; then
    NETPERF_TEST_TYPE="UDP_RR"
else
    NETPERF_TEST_TYPE="TCP_RR"
fi

######################## Run HARDWARE_THREADS concurrent netperf instances ########################
echo "=== netperf: test=$NETPERF_TEST_TYPE instances=$HARDWARE_THREADS duration=${HARDWARE_DURATION}s data-ports=[$POOL_START,$POOL_END) ==="
OUT_DIR="$(mktemp -d)"
i=0
while [ "$i" -lt "$HARDWARE_THREADS" ]; do
    port=$((NETPERF_DATA_BASE_PORT + POOL_START + i))
    netperf -H "$BEXHOMA_HOST" -p "$NETPERF_CONTROL_PORT" -t "$NETPERF_TEST_TYPE" -l "$HARDWARE_DURATION" \
        -- -P ,"$port" -o TRANSACTION_RATE,MEAN_LATENCY,P50_LATENCY,P90_LATENCY,P99_LATENCY \
        >"$OUT_DIR/instance_$i.csv" 2>&1 &
    i=$((i + 1))
done
wait

######################## Parse and aggregate results across instances ########################
# Each instance's output is "MIGRATED ... REQUEST/RESPONSE TEST ...\nheader\nvalue"
# (see the -o selector list above); the banner line is checked for before trusting the
# last line as the data row, same convention as run_sockperf.sh's SOCKPERF_VALID check
# (a connection failure/refused port never prints that banner).
sum_transaction_rate=0
max_mean_latency_usec=0
max_p50_latency_usec=0
max_p90_latency_usec=0
max_p99_latency_usec=0
num_failed=0
i=0
while [ "$i" -lt "$HARDWARE_THREADS" ]; do
    csv_file="$OUT_DIR/instance_$i.csv"
    if ! grep -q 'REQUEST/RESPONSE TEST' "$csv_file"; then
        echo "Error: netperf instance $i produced no result:"
        cat "$csv_file"
        num_failed=$((num_failed + 1))
    else
        data_line="$(tail -n1 "$csv_file")"
        transaction_rate=$(echo "$data_line" | cut -d',' -f1)
        mean_latency_usec=$(echo "$data_line" | cut -d',' -f2)
        p50_latency_usec=$(echo "$data_line" | cut -d',' -f3)
        p90_latency_usec=$(echo "$data_line" | cut -d',' -f4)
        p99_latency_usec=$(echo "$data_line" | cut -d',' -f5)
        sum_transaction_rate=$(awk "BEGIN{printf \"%.6f\", $sum_transaction_rate + ${transaction_rate:-0}}")
        max_mean_latency_usec=$(awk "BEGIN{print (${mean_latency_usec:-0} > $max_mean_latency_usec) ? ${mean_latency_usec:-0} : $max_mean_latency_usec}")
        max_p50_latency_usec=$(awk "BEGIN{print (${p50_latency_usec:-0} > $max_p50_latency_usec) ? ${p50_latency_usec:-0} : $max_p50_latency_usec}")
        max_p90_latency_usec=$(awk "BEGIN{print (${p90_latency_usec:-0} > $max_p90_latency_usec) ? ${p90_latency_usec:-0} : $max_p90_latency_usec}")
        max_p99_latency_usec=$(awk "BEGIN{print (${p99_latency_usec:-0} > $max_p99_latency_usec) ? ${p99_latency_usec:-0} : $max_p99_latency_usec}")
    fi
    i=$((i + 1))
done
rm -rf "$OUT_DIR"

######################## Transform result for evaluation ########################
# usec_to_ms: netperf reports latency in microseconds; converted to milliseconds for
# the same _MS-suffix convention run_sockperf.sh already uses.
usec_to_ms() {
    awk "BEGIN{printf \"%.6f\", $1 / 1000}"
}
latency_avg_ms=$(usec_to_ms "$max_mean_latency_usec")
latency_p50_ms=$(usec_to_ms "$max_p50_latency_usec")
latency_p90_ms=$(usec_to_ms "$max_p90_latency_usec")
latency_p99_ms=$(usec_to_ms "$max_p99_latency_usec")

######################## Echo KEY:VALUE summary ########################
echo "HARDWARE_NETPERF_TRANSACTION_RATE:$sum_transaction_rate"
echo "HARDWARE_NETPERF_LATENCY_AVG_MS:$latency_avg_ms"
echo "HARDWARE_NETPERF_LATENCY_P50_MS:$latency_p50_ms"
echo "HARDWARE_NETPERF_LATENCY_P90_MS:$latency_p90_ms"
echo "HARDWARE_NETPERF_LATENCY_P99_MS:$latency_p99_ms"
echo "HARDWARE_NETPERF_INSTANCES_FAILED:$num_failed"

######################## Write CSV summary ########################
UUID=$(cat /proc/sys/kernel/random/uuid)
RESULT_CSV="/results/$BEXHOMA_EXPERIMENT/netperf.$BEXHOMA_CONNECTION.$BEXHOMA_CLIENT.$UUID.csv"
{
    echo "test_type,instances,duration,transaction_rate,latency_avg_ms,latency_p50_ms,latency_p90_ms,latency_p99_ms,instances_failed"
    echo "$NETPERF_TEST_TYPE,$HARDWARE_THREADS,$HARDWARE_DURATION,$sum_transaction_rate,\
$latency_avg_ms,$latency_p50_ms,$latency_p90_ms,$latency_p99_ms,$num_failed"
} > "$RESULT_CSV"

echo "$RESULT_CSV"
cat "$RESULT_CSV"
