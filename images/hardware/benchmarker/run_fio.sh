#!/bin/bash

######################## Show parameters ########################
echo "BEXHOMA_HOST:$BEXHOMA_HOST"
echo "BEXHOMA_SUT_USER:$BEXHOMA_SUT_USER"
echo "BEXHOMA_SUT_KEY:$BEXHOMA_SUT_KEY"
echo "HARDWARE_TEST_DIR:$HARDWARE_TEST_DIR"
echo "HARDWARE_SIZE:$HARDWARE_SIZE"
echo "HARDWARE_DURATION:$HARDWARE_DURATION"
echo "HARDWARE_FIO_RW:$HARDWARE_FIO_RW"
echo "HARDWARE_FIO_BS:$HARDWARE_FIO_BS"
echo "HARDWARE_FIO_IODEPTH:$HARDWARE_FIO_IODEPTH"
echo "HARDWARE_FIO_NUMJOBS:$HARDWARE_FIO_NUMJOBS"
echo "HARDWARE_FIO_ENGINE:$HARDWARE_FIO_ENGINE"
echo "HARDWARE_FIO_FSYNC:$HARDWARE_FIO_FSYNC"
echo "HARDWARE_FIO_RWMIXREAD:$HARDWARE_FIO_RWMIXREAD"

######################## Scope test directory to this pod ########################
# Parallel benchmarker pods (BEXHOMA_NUM_PODS > 1) share one SUT and one PVC;
# without a per-pod subdirectory they would all run fio against the same
# --directory/--name and corrupt each other's test file.
HARDWARE_TEST_DIR="${HARDWARE_TEST_DIR}/pod-${BEXHOMA_CHILD}"
echo "HARDWARE_TEST_DIR (scoped to pod):$HARDWARE_TEST_DIR"

######################## Set SSH options ########################
SSH_OPTS="-i ${BEXHOMA_SUT_KEY} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

######################## Create test directory on SUT ########################
ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_HOST}" "mkdir -p ${HARDWARE_TEST_DIR}"

######################## Build fio argument list ########################
# rwmixread only applies to mixed read/write workloads; fsync=0 means "never", so
# both flags are appended conditionally instead of always being passed to fio.
FIO_ARGS="--name=hardware_fio --directory=${HARDWARE_TEST_DIR} --rw=${HARDWARE_FIO_RW} \
--bs=${HARDWARE_FIO_BS} --size=${HARDWARE_SIZE} --numjobs=${HARDWARE_FIO_NUMJOBS} \
--iodepth=${HARDWARE_FIO_IODEPTH} --ioengine=${HARDWARE_FIO_ENGINE} \
--runtime=${HARDWARE_DURATION} --time_based --direct=1 --group_reporting \
--output-format=json"

if [ "$HARDWARE_FIO_FSYNC" != "0" ]; then
    FIO_ARGS="$FIO_ARGS --fsync=${HARDWARE_FIO_FSYNC}"
fi
case "$HARDWARE_FIO_RW" in
    randrw)
        FIO_ARGS="$FIO_ARGS --rwmixread=${HARDWARE_FIO_RWMIXREAD}"
        ;;
esac

######################## Run fio benchmark ########################
echo "=== fio: rw=$HARDWARE_FIO_RW bs=$HARDWARE_FIO_BS iodepth=$HARDWARE_FIO_IODEPTH numjobs=$HARDWARE_FIO_NUMJOBS engine=$HARDWARE_FIO_ENGINE fsync=$HARDWARE_FIO_FSYNC ==="
FIO_JSON="$(ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_HOST}" "fio $FIO_ARGS")"

######################## Store raw result ########################
UUID=$(cat /proc/sys/kernel/random/uuid)
RESULT_JSON="/results/$BEXHOMA_EXPERIMENT/fio.$BEXHOMA_CONNECTION.$BEXHOMA_CLIENT.$UUID.json"
RESULT_CSV="/results/$BEXHOMA_EXPERIMENT/fio.$BEXHOMA_CONNECTION.$BEXHOMA_CLIENT.$UUID.csv"
echo "$FIO_JSON" > "$RESULT_JSON"
echo "$RESULT_JSON"

######################## Transform result for evaluation ########################
# ns_to_ms: fio reports completion latency percentiles in nanoseconds; jq does the
# unit conversion directly so the image does not need a separate awk/bc dependency.
percentile_ms() {
    local direction="$1"
    local percentile="$2"
    jq -r ".jobs[0].${direction}.clat_ns.percentile[\"${percentile}\"] // 0 | . / 1000000" "$RESULT_JSON"
}

read_iops=$(jq -r '.jobs[0].read.iops // 0' "$RESULT_JSON")
write_iops=$(jq -r '.jobs[0].write.iops // 0' "$RESULT_JSON")
read_bw_kbps=$(jq -r '.jobs[0].read.bw // 0' "$RESULT_JSON")
write_bw_kbps=$(jq -r '.jobs[0].write.bw // 0' "$RESULT_JSON")

# Eight percentiles per direction: p1/p10 (best case), p50 (median), p90/p95/p99
# (standard SLO markers), p999/p9999 (extreme tail, relevant for WAL fsync latency).
PERCENTILES=("1.000000" "10.000000" "50.000000" "90.000000" "95.000000" "99.000000" "99.900000" "99.990000")
PERCENTILE_LABELS=("p01" "p10" "p50" "p90" "p95" "p99" "p999" "p9999")

read_lat=()
write_lat=()
for percentile in "${PERCENTILES[@]}"; do
    read_lat+=("$(percentile_ms read "$percentile")")
    write_lat+=("$(percentile_ms write "$percentile")")
done

######################## Echo KEY:VALUE summary ########################
echo "HARDWARE_FIO_READ_IOPS:$read_iops"
echo "HARDWARE_FIO_WRITE_IOPS:$write_iops"
echo "HARDWARE_FIO_READ_BW_KBPS:$read_bw_kbps"
echo "HARDWARE_FIO_WRITE_BW_KBPS:$write_bw_kbps"
for i in "${!PERCENTILE_LABELS[@]}"; do
    label="${PERCENTILE_LABELS[$i]}"
    echo "HARDWARE_FIO_READ_LAT_${label^^}_MS:${read_lat[$i]}"
    echo "HARDWARE_FIO_WRITE_LAT_${label^^}_MS:${write_lat[$i]}"
done

######################## Write CSV summary ########################
{
    header="rw,bs,iodepth,numjobs,engine,fsync,size,duration,read_iops,write_iops,read_bw_kbps,write_bw_kbps"
    for label in "${PERCENTILE_LABELS[@]}"; do
        header="$header,read_${label}_ms"
    done
    for label in "${PERCENTILE_LABELS[@]}"; do
        header="$header,write_${label}_ms"
    done
    echo "$header"

    row="$HARDWARE_FIO_RW,$HARDWARE_FIO_BS,$HARDWARE_FIO_IODEPTH,$HARDWARE_FIO_NUMJOBS,$HARDWARE_FIO_ENGINE,\
$HARDWARE_FIO_FSYNC,$HARDWARE_SIZE,$HARDWARE_DURATION,$read_iops,$write_iops,$read_bw_kbps,$write_bw_kbps"
    for value in "${read_lat[@]}"; do
        row="$row,$value"
    done
    for value in "${write_lat[@]}"; do
        row="$row,$value"
    done
    echo "$row"
} > "$RESULT_CSV"

echo "$RESULT_CSV"
cat "$RESULT_CSV"