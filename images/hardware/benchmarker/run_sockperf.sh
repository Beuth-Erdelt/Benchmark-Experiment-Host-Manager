#!/bin/bash

######################## Show parameters ########################
echo "BEXHOMA_HOST:$BEXHOMA_HOST"
echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
echo "HARDWARE_DURATION:$HARDWARE_DURATION"
echo "HARDWARE_SOCKPERF_MODE:$HARDWARE_SOCKPERF_MODE"
echo "HARDWARE_SOCKPERF_PROTOCOL:$HARDWARE_SOCKPERF_PROTOCOL"
echo "HARDWARE_SOCKPERF_MSGSIZE:$HARDWARE_SOCKPERF_MSGSIZE"
echo "HARDWARE_SOCKPERF_MPS:$HARDWARE_SOCKPERF_MPS"

######################## Pick this pod's dedicated sockperf server ########################
# Several benchmarker pods (BEXHOMA_NUM_PODS > 1) share one SUT, which runs
# SOCKPERF_NUM_SERVERS independent UDP+TCP server pairs (see
# images/hardware/sut/entrypoint.sh); BEXHOMA_CHILD picks one so pods don't
# contend on the same socket, mirroring how run_fio.sh scopes its test
# directory by the same index. Modulo wraps around (server reuse) instead of
# failing if a sweep ever asks for more pods than provisioned servers.
SOCKPERF_PORT=$((SOCKPERF_BASE_PORT + (BEXHOMA_CHILD - 1) % SOCKPERF_NUM_SERVERS))
echo "HARDWARE_SOCKPERF_PORT:$SOCKPERF_PORT"

######################## Build sockperf argument list ########################
SOCKPERF_ARGS="-i ${BEXHOMA_HOST} -p ${SOCKPERF_PORT} -t ${HARDWARE_DURATION} -m ${HARDWARE_SOCKPERF_MSGSIZE} --mps=${HARDWARE_SOCKPERF_MPS}"
if [ "$HARDWARE_SOCKPERF_PROTOCOL" = "tcp" ]; then
    SOCKPERF_ARGS="$SOCKPERF_ARGS --tcp"
fi

######################## Run sockperf benchmark ########################
echo "=== sockperf: mode=$HARDWARE_SOCKPERF_MODE protocol=$HARDWARE_SOCKPERF_PROTOCOL msgsize=$HARDWARE_SOCKPERF_MSGSIZE mps=$HARDWARE_SOCKPERF_MPS port=$SOCKPERF_PORT ==="
UUID=$(cat /proc/sys/kernel/random/uuid)
RESULT_LOG="/results/$BEXHOMA_EXPERIMENT/sockperf.$BEXHOMA_CONNECTION.$BEXHOMA_CLIENT.$UUID.fulllog.csv"
RESULT_CSV="/results/$BEXHOMA_EXPERIMENT/sockperf.$BEXHOMA_CONNECTION.$BEXHOMA_CLIENT.$UUID.csv"
SOCKPERF_STDOUT="$(mktemp)"
# shellcheck disable=SC2086
sockperf "$HARDWARE_SOCKPERF_MODE" $SOCKPERF_ARGS --full-log "$RESULT_LOG" >"$SOCKPERF_STDOUT" 2>&1
SOCKPERF_EXIT=$?
echo "=== sockperf exit code: $SOCKPERF_EXIT ==="
cat "$SOCKPERF_STDOUT"
echo "$RESULT_LOG"

######################## Validate sockperf output before parsing ########################
# A connection failure or invalid argument combination prints an "ERROR:" line
# and never reaches the summary section below; every field would otherwise
# silently default to 0 with no indication of the actual cause. Presence of
# the summary line is checked directly instead of relying on the exit code.
if grep -q '^sockperf: Summary: Latency is' "$SOCKPERF_STDOUT"; then
    SOCKPERF_VALID=1
else
    SOCKPERF_VALID=0
    echo "ERROR: sockperf did not produce a valid summary (exit code $SOCKPERF_EXIT). Raw output was above."
fi

######################## Transform result for evaluation ########################
# usec_to_ms: sockperf reports latency in microseconds; converted to milliseconds
# so column names can keep the same _MS suffix the evaluator's aggregation
# already treats as "max across parallel pods" (see evaluators/hardware.py).
usec_to_ms() {
    awk "BEGIN{printf \"%.6f\", $1 / 1000}"
}
percentile_usec() {
    local percentile="$1"
    grep -E "percentile ${percentile} =" "$SOCKPERF_STDOUT" | awk -F'=' '{gsub(/ /, "", $2); print $2}'
}

if [ "$SOCKPERF_VALID" = "1" ]; then
    latency_avg_usec=$(grep -oE 'Latency is [0-9.]+' "$SOCKPERF_STDOUT" | awk '{print $3}')
    dropped=$(grep -oE '# dropped messages = [0-9]+' "$SOCKPERF_STDOUT" | grep -oE '[0-9]+$')
    valid_duration_line=$(grep '\[Valid Duration\]' "$SOCKPERF_STDOUT")
    runtime_sec=$(echo "$valid_duration_line" | grep -oE 'RunTime=[0-9.]+' | cut -d= -f2)
    received_messages=$(echo "$valid_duration_line" | grep -oE 'ReceivedMessages=[0-9]+' | cut -d= -f2)
    p50_usec=$(percentile_usec "50.000")
    p99_usec=$(percentile_usec "99.000")
    p999_usec=$(percentile_usec "99.900")
    msg_rate=$(awk "BEGIN{if (${runtime_sec:-0} == 0) print 0; else printf \"%.6f\", ${received_messages:-0} / ${runtime_sec:-0}}")
else
    latency_avg_usec=0
    dropped=0
    received_messages=0
    p50_usec=0
    p99_usec=0
    p999_usec=0
    msg_rate=0
fi

latency_avg_ms=$(usec_to_ms "${latency_avg_usec:-0}")
latency_p50_ms=$(usec_to_ms "${p50_usec:-0}")
latency_p99_ms=$(usec_to_ms "${p99_usec:-0}")
latency_p999_ms=$(usec_to_ms "${p999_usec:-0}")
dropped_per_sec=$(awk "BEGIN{if (${HARDWARE_DURATION:-0} == 0) print 0; else printf \"%.6f\", ${dropped:-0} / ${HARDWARE_DURATION}}")

######################## Echo KEY:VALUE summary ########################
echo "HARDWARE_SOCKPERF_LATENCY_AVG_MS:$latency_avg_ms"
echo "HARDWARE_SOCKPERF_LATENCY_P50_MS:$latency_p50_ms"
echo "HARDWARE_SOCKPERF_LATENCY_P99_MS:$latency_p99_ms"
echo "HARDWARE_SOCKPERF_LATENCY_P999_MS:$latency_p999_ms"
echo "HARDWARE_SOCKPERF_MSG_RATE_PER_SEC:$msg_rate"
echo "HARDWARE_SOCKPERF_DROPPED_PER_SEC:$dropped_per_sec"

rm -f "$SOCKPERF_STDOUT"

######################## Write CSV summary ########################
{
    echo "mode,protocol,msgsize,mps,port,duration,latency_avg_ms,latency_p50_ms,latency_p99_ms,latency_p999_ms,msg_rate_per_sec,dropped_per_sec"
    echo "$HARDWARE_SOCKPERF_MODE,$HARDWARE_SOCKPERF_PROTOCOL,$HARDWARE_SOCKPERF_MSGSIZE,$HARDWARE_SOCKPERF_MPS,$SOCKPERF_PORT,\
$HARDWARE_DURATION,$latency_avg_ms,$latency_p50_ms,$latency_p99_ms,$latency_p999_ms,$msg_rate,$dropped_per_sec"
} > "$RESULT_CSV"

echo "$RESULT_CSV"
cat "$RESULT_CSV"
