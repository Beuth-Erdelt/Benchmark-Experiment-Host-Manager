#!/usr/bin/env bash

# apt-get -y install fio jq sysbench bsdextrautils


set -euo pipefail

#TEST_DIR=${1:-/data/fiotest}
TEST_DIR=${1:-/tmp/fiotest}
DURATION=${2:-60}
SIZE=${3:-64G}
BLOCKSIZE=${4:-8k}
WORKLOAD_RANDREAD="no"
WORKLOAD_RANDRW="no"
WORKLOAD_SYNC="yes"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTDIR="fio_results_${TIMESTAMP}"

mkdir -p "$OUTDIR"
mkdir -p "$TEST_DIR"
META_FILE="$OUTDIR/meta.csv"
echo "run,workload,engine,iodepth,bs,size,numjobs,duration,\
read_iops,write_iops,read_p01,read_p05,read_p10,read_p20,read_p30,read_p40,read_p50,read_p60,read_p70,read_p80,read_p90,read_p95,read_p99,read_p995,read_p999,read_p9995,read_p9999,\
write_p01,write_p05,write_p10,write_p20,write_p30,write_p40,write_p50,write_p60,write_p70,write_p80,write_p90,write_p95,write_p99,write_p995,write_p999,write_p9995,write_p9999" \
> "$META_FILE"

echo "=== Starting baseline benchmark ==="
echo "Test dir: $TEST_DIR"
echo "Duration: $DURATION seconds"
echo "Size: $SIZE"
echo "Output: $OUTDIR"
echo

print_header () {
  local run="$1"
  local workload="$2"
  local engine="$3"
  local iodepth="$4"
  local numjobs="$5"
  local bs="$6"
  local size="$7"
  local duration="$8"

  echo "=================================================="
  echo "🚀 FIO BENCHMARK START"
  echo "--------------------------------------------------"
  echo "Run       : $run"
  echo "Workload  : $workload"
  echo "Engine    : $engine"
  echo "IO depth  : $iodepth"
  echo "Num jobs  : $numjobs"
  echo "Block size: $bs"
  echo "Size      : $size"
  echo "Duration  : $duration"
  echo "Target    : $TEST_DIR/testfile"
  echo "Mode      : direct I/O"
  echo "=================================================="
}

get_pct() {
  jq -r "$1 // 0" "$file"
}

ns_to_ms() {
  awk "BEGIN {print $1/1000000}"
}

write_pct() {

  # --------------------------
  # throughput (read/write)
  # --------------------------
  r_iops=$(jq -r '.jobs[0].read.iops // 0' "$file")
  w_iops=$(jq -r '.jobs[0].write.iops // 0' "$file")

  # --------------------------
  # helper: latency conversion
  # --------------------------
  ns_to_ms() {
    awk "BEGIN {print $1/1000000}"
  }

  # --------------------------
  # READ percentiles (ms)
  # --------------------------
  r01=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["1.000000"]')")
  r05=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["5.000000"]')")
  r10=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["10.000000"]')")
  r20=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["20.000000"]')")
  r30=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["30.000000"]')")
  r40=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["40.000000"]')")
  r50=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["50.000000"]')")
  r60=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["60.000000"]')")
  r70=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["70.000000"]')")
  r80=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["80.000000"]')")
  r90=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["90.000000"]')")
  r95=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["95.000000"]')")
  r99=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["99.000000"]')")
  r995=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["99.500000"]')")
  r999=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["99.900000"]')")
  r9995=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["99.950000"]')")
  r9999=$(ns_to_ms "$(get_pct '.jobs[0].read.clat_ns.percentile["99.990000"]')")

  # --------------------------
  # WRITE percentiles (ms)
  # --------------------------
  w01=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["1.000000"]')")
  w05=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["5.000000"]')")
  w10=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["10.000000"]')")
  w20=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["20.000000"]')")
  w30=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["30.000000"]')")
  w40=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["40.000000"]')")
  w50=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["50.000000"]')")
  w60=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["60.000000"]')")
  w70=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["70.000000"]')")
  w80=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["80.000000"]')")
  w90=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["90.000000"]')")
  w95=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["95.000000"]')")
  w99=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["99.000000"]')")
  w995=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["99.500000"]')")
  w999=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["99.900000"]')")
  w9995=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["99.950000"]')")
  w9999=$(ns_to_ms "$(get_pct '.jobs[0].write.clat_ns.percentile["99.990000"]')")

  # --------------------------
  # CSV output
  # --------------------------
  echo "$run,$workload,$engine,$iodepth,$bs,$size,$numjobs,$duration,\
$r_iops,$w_iops,\
$r01,$r05,$r10,$r20,$r30,$r40,$r50,$r60,$r70,$r80,$r90,$r95,$r99,$r995,$r999,$r9995,$r9999,\
$w01,$w05,$w10,$w20,$w30,$w40,$w50,$w60,$w70,$w80,$w90,$w95,$w99,$w995,$w999,$w9995,$w9999" \
>> "$META_FILE"
}

# -------------------------------
# System Info
# -------------------------------
echo "Collecting system info..."
{
  echo "===== DATE ====="
  date
  echo "===== KERNEL ====="
  uname -a
  echo "===== CPU ====="
  lscpu
  echo "===== MEMORY ====="
  free -h
  echo "===== DISK ====="
  lsblk
  echo "===== MOUNT ====="
  mount
} > "$OUTDIR/system_info.txt"

# -------------------------------
# Warmup
# -------------------------------
echo "Warming up disk..."
fio --name=warmup \
  --filename=$TEST_DIR/testfile \
  --size=1G \
  --bs=1M \
  --rw=write \
  --direct=1 \
  --iodepth=16 \
  --numjobs=1 \
  --runtime=30 \
  --time_based \
  --group_reporting > "$OUTDIR/warmup.txt"

# -------------------------------
# WAL-like test (sequential write)
# -------------------------------
# echo "Running WAL-like sequential write test..."

# run="wal_write"
# workload="seq_write"
# engine="libaio"
# iodepth=1
# numjobs=1
# bs="$BLOCKSIZE"
# size="$SIZE"
# duration="$DURATION"

# print_header "$run" "$workload" "$engine" "$iodepth" "$numjobs" "$bs" "$size" "$duration"

# file="$OUTDIR/wal_write.json"

# fio --name="$run" \
#   --filename="$TEST_DIR/testfile" \
#   --size="$size" \
#   --bs="$bs" \
#   --rw=write \
#   --ioengine=libaio \
#   --direct=1 \
#   --iodepth="$iodepth" \
#   --numjobs="$numjobs" \
#   --runtime="$duration" \
#   --time_based \
#   --group_reporting \
#   --output-format=json \
#   > "$file"

# write_pct

# -------------------------------
# Fsync test (CRITICAL for WAL)
# -------------------------------
if [[ "$WORKLOAD_SYNC" == "yes" ]]; then
  echo "Running fsync test..."

  for jobs in 1; do
    run="fsync_test"
    workload="seq_write"
    engine="sync"
    iodepth=1
    #numjobs=1
    numjobs=$jobs
    bs="$BLOCKSIZE"
    #size=1G
    size="$SIZE"
    duration="$DURATION"

    print_header "$run" "$workload" "$engine" "$iodepth" "$numjobs" "$bs" "$size" "$duration"

    #file="$OUTDIR/wal_write.json"
    file="$OUTDIR/wal_write_${numjobs}.json"

    fio --name="$run" \
      --filename="$TEST_DIR/testfile" \
      --size="$size" \
      --bs="$bs" \
      --rw=write \
      --fsync=32 \
      --direct=1 \
      --iodepth="$iodepth" \
      --ioengine=$engine \
      --runtime="$duration" \
      --time_based \
      --group_reporting \
      --output-format=json \
      > "$file"
    # --sync_file_range=write:4096

    write_pct
  done
fi

# -------------------------------
# Random read/write test
# -------------------------------
# echo "Running random read/write test..."

# run="rand_rw"
# workload="randrw"
# engine="libaio"
# iodepth=32
# numjobs=4
# bs="$BLOCKSIZE"
# size="$SIZE"
# duration="$DURATION"

# print_header "$run" "$workload" "$engine" "$iodepth" "$numjobs" "$bs" "$size" "$duration"

# file="$OUTDIR/randrw.json"

# fio --name="$run" \
#   --filename="$TEST_DIR/testfile" \
#   --size="$size" \
#   --bs="$bs" \
#   --rw=randrw \
#   --rwmixread=50 \
#   --ioengine=libaio \
#   --numjobs="$numjobs" \
#   --direct=1 \
#   --iodepth="$iodepth" \
#   --runtime="$duration" \
#   --time_based \
#   --group_reporting \
#   --output-format=json \
#   > "$file"

# write_pct


# -------------------------------
# Concurrency sweep (important for io_uring)
# -------------------------------
if [[ "$WORKLOAD_RANDREAD" == "yes" ]]; then
  echo "Running concurrency sweep..."

  for depth in 1 2 4 8 12 16 20 24 30 36 48 54 60 66 72 78 84 90; do
    run="randrw_${depth}"
    workload="randrw"
    engine="io_uring" #"libaio"
    iodepth=$depth
    numjobs=16
    bs="$BLOCKSIZE"
    size="$SIZE"
    duration="$DURATION"

    print_header "$run" "$workload" "$engine" "$iodepth" "$numjobs" "$bs" "$size" "$duration"

    file="$OUTDIR/randrw_iodepth_${depth}.json"

    fio --name="$run" \
      --filename="$TEST_DIR/testfile" \
      --size="$size" \
      --bs="$bs" \
      --rw=randrw \
      --rwmixread=50 \
      --ioengine=$engine \
      --numjobs="$numjobs" \
      --direct=1 \
      --iodepth="$iodepth" \
      --runtime="$duration" \
      --time_based \
      --group_reporting \
      --output-format=json \
      > "$file"

    write_pct
  done
fi

# -------------------------------
# Random read sweep (important for effective_io_concurrency, random_page_cost)
# -------------------------------
if [[ "$WORKLOAD_RANDRW" == "yes" ]]; then
  echo "Running read sweep..."

  for depth in 1 2 4 8 12 16 20 24 30 36 48 54 60 66 72 78 84 90; do
    run="randread_${depth}"
    workload="randread"
    engine="io_uring" #"libaio"
    iodepth=$depth
    numjobs=16
    bs="$BLOCKSIZE"
    size="$SIZE"
    duration="$DURATION"

    print_header "$run" "$workload" "$engine" "$iodepth" "$numjobs" "$bs" "$size" "$duration"

    file="$OUTDIR/randread_iodepth_${depth}.json"

    fio --name="$run" \
      --filename="$TEST_DIR/testfile" \
      --size="$size" \
      --bs="$bs" \
      --rw=randread \
      --ioengine=$engine \
      --numjobs="$numjobs" \
      --direct=1 \
      --iodepth="$iodepth" \
      --runtime="$duration" \
      --time_based \
      --group_reporting \
      --output-format=json \
      > "$file"

    write_pct
  done
fi

cat $META_FILE

# -------------------------------
# CPU test (sysbench if available)
# -------------------------------
if command -v sysbench &> /dev/null; then
  echo "Running CPU benchmark..."
  sysbench cpu --cpu-max-prime=20000 run > "$OUTDIR/cpu.txt"
fi

# -------------------------------
# Memory test (optional)
# -------------------------------
if command -v sysbench &> /dev/null; then
  echo "Running memory benchmark..."
  sysbench memory run > "$OUTDIR/memory.txt"
fi

echo
echo "=== Benchmark complete ==="
echo "Results stored in: $OUTDIR"
