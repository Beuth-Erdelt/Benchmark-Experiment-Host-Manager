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
echo "HARDWARE_FIO_FDATASYNC:$HARDWARE_FIO_FDATASYNC"
echo "HARDWARE_FIO_RWMIXREAD:$HARDWARE_FIO_RWMIXREAD"

######################## Scope test directory to this pod ########################
# Parallel benchmarker pods (BEXHOMA_NUM_PODS > 1) share one SUT and one PVC;
# without a per-pod subdirectory they would all run fio against the same
# --directory/--name and corrupt each other's test file.
HARDWARE_TEST_DIR="${HARDWARE_TEST_DIR}/pod-${BEXHOMA_CHILD}"
echo "HARDWARE_TEST_DIR (scoped to pod):$HARDWARE_TEST_DIR"

######################## Set SSH options ########################
# bexhoma-service maps the SUT's real SSH port (22) to service port 9091,
# same as every other DBMS's port-dbms mapping (see deploymenttemplate-Hardware.yml).
SSH_PORT=9091
SSH_OPTS="-p ${SSH_PORT} -i ${BEXHOMA_SUT_KEY} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

######################## Create test directory on SUT ########################
ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_HOST}" "mkdir -p ${HARDWARE_TEST_DIR}"

######################## Build fio argument list ########################
# rwmixread only applies to mixed read/write workloads; fsync=0/fdatasync=0 mean
# "never", so all three flags are appended conditionally instead of always being
# passed to fio. fsync and fdatasync are alternatives (wal_sync_method=fsync vs.
# fdatasync in PostgreSQL); the caller is expected to set only one of them.
FIO_ARGS="--name=hardware_fio --directory=${HARDWARE_TEST_DIR} --rw=${HARDWARE_FIO_RW} \
--bs=${HARDWARE_FIO_BS} --size=${HARDWARE_SIZE} --numjobs=${HARDWARE_FIO_NUMJOBS} \
--iodepth=${HARDWARE_FIO_IODEPTH} --ioengine=${HARDWARE_FIO_ENGINE} \
--runtime=${HARDWARE_DURATION} --time_based --direct=1 --group_reporting \
--output-format=json"

if [ "$HARDWARE_FIO_FSYNC" != "0" ]; then
    FIO_ARGS="$FIO_ARGS --fsync=${HARDWARE_FIO_FSYNC}"
fi
if [ "$HARDWARE_FIO_FDATASYNC" != "0" ]; then
    FIO_ARGS="$FIO_ARGS --fdatasync=${HARDWARE_FIO_FDATASYNC}"
fi
case "$HARDWARE_FIO_RW" in
    randrw)
        FIO_ARGS="$FIO_ARGS --rwmixread=${HARDWARE_FIO_RWMIXREAD}"
        ;;
esac

######################## Run fio benchmark ########################
echo "=== fio: rw=$HARDWARE_FIO_RW bs=$HARDWARE_FIO_BS iodepth=$HARDWARE_FIO_IODEPTH numjobs=$HARDWARE_FIO_NUMJOBS engine=$HARDWARE_FIO_ENGINE fsync=$HARDWARE_FIO_FSYNC fdatasync=$HARDWARE_FIO_FDATASYNC ==="
FIO_JSON="$(ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_HOST}" "fio $FIO_ARGS")"

######################## Remove fio test files from the SUT ########################
# Without an explicit --filename, fio names one file per numjobs thread
# (either "hardware_fio" alone, or "hardware_fio.<jobid>.<fileno>" for numjobs>1 —
# the glob below matches both), each --size bytes. The PVC is shared and never
# wiped between rounds/experiments (see project notes on -rsr and PVC sharing), so
# leftover files accumulate round over round and can exceed the PVC size entirely
# at high numjobs (e.g. numjobs=32 at --size=4G needs 128G, more than double a
# 50Gi PVC). Removing them right after fio is done keeps steady-state usage to
# just the current round's files.
# HARDWARE_TEST_DIR was scoped to /pod-${BEXHOMA_CHILD} above and the glob only
# matches this job's own hardware_fio* files, so with several benchmarker pods
# running in parallel (BEXHOMA_NUM_PODS > 1) each one only ever removes its own
# test files, never another pod's directory or files.
#
# The before/after listing below is deliberate status output, not just debug
# noise: it shows exactly which files this round leaves behind before cleanup
# runs, and its mere presence in a job's log is proof that *this* version of
# run_fio.sh (the one with cleanup) is what actually executed — if a log is
# missing this section, the pod ran an older image without the fix.
echo "=== fio test files before cleanup ==="
ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_HOST}" "ls -la ${HARDWARE_TEST_DIR}/hardware_fio* 2>/dev/null || echo '(no hardware_fio* files found)'"
echo "=== removing fio test files ==="
# rm -f is silent on success, so -v (verbose) is added here specifically so the
# log shows which files were actually removed, instead of only being able to
# infer it indirectly from the after-listing below being empty.
ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_HOST}" "rm -fv ${HARDWARE_TEST_DIR}/hardware_fio* 2>&1"
echo "=== fio test files after cleanup ==="
ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_HOST}" "ls -la ${HARDWARE_TEST_DIR}/hardware_fio* 2>/dev/null || echo '(no hardware_fio* files found)'"

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
    header="rw,bs,iodepth,numjobs,engine,fsync,fdatasync,size,duration,read_iops,write_iops,read_bw_kbps,write_bw_kbps"
    for label in "${PERCENTILE_LABELS[@]}"; do
        header="$header,read_${label}_ms"
    done
    for label in "${PERCENTILE_LABELS[@]}"; do
        header="$header,write_${label}_ms"
    done
    echo "$header"

    row="$HARDWARE_FIO_RW,$HARDWARE_FIO_BS,$HARDWARE_FIO_IODEPTH,$HARDWARE_FIO_NUMJOBS,$HARDWARE_FIO_ENGINE,\
$HARDWARE_FIO_FSYNC,$HARDWARE_FIO_FDATASYNC,$HARDWARE_SIZE,$HARDWARE_DURATION,$read_iops,$write_iops,$read_bw_kbps,$write_bw_kbps"
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