#!/usr/bin/env bash

# apt-get -y install fio jq sysbench bsdextrautils


set -euo pipefail

TEST_DIR=${1:-/data/fiotest}
DURATION=${2:-60}
SIZE=${3:-8G}
BLOCKSIZE=${4:-8k}

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTDIR="fio_results_${TIMESTAMP}"

mkdir -p "$OUTDIR"
mkdir -p "$TEST_DIR"

echo "=== Starting baseline benchmark ==="
echo "Test dir: $TEST_DIR"
echo "Duration: $DURATION seconds"
echo "Size: $SIZE"
echo "Output: $OUTDIR"
echo

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
echo "Running WAL-like sequential write test..."
fio --name=wal_write \
  --filename=$TEST_DIR/testfile \
  --size=$SIZE \
  --bs=$BLOCKSIZE \
  --rw=write \
  --ioengine=libaio \
  --direct=1 \
  --iodepth=1 \
  --numjobs=1 \
  --runtime=$DURATION \
  --time_based \
  --group_reporting \
  --output-format=json \
  > "$OUTDIR/wal_write.json"

# -------------------------------
# Fsync test (CRITICAL for WAL)
# -------------------------------
echo "Running fsync test..."
fio --name=fsync_test \
  --filename=$TEST_DIR/testfile \
  --size=1G \
  --bs=$BLOCKSIZE \
  --rw=write \
  --fsync=1 \
  --ioengine=sync \
  --runtime=$DURATION \
  --time_based \
  --group_reporting \
  --output-format=json \
  > "$OUTDIR/fsync.json"

# -------------------------------
# Random read/write test
# -------------------------------
echo "Running random read/write test..."
fio --name=rand_rw \
  --filename=$TEST_DIR/testfile \
  --size=$SIZE \
  --bs=$BLOCKSIZE \
  --rw=randrw \
  --rwmixread=50 \
  --ioengine=libaio \
  --direct=1 \
  --iodepth=32 \
  --numjobs=4 \
  --runtime=$DURATION \
  --time_based \
  --group_reporting \
  --output-format=json \
  > "$OUTDIR/randrw.json"

# -------------------------------
# Concurrency sweep (important for io_uring)
# -------------------------------
echo "Running concurrency sweep..."
for depth in 1 2 4 8 16 32 64; do
  fio --name=iodepth_${depth} \
    --filename=$TEST_DIR/testfile \
    --size=$SIZE \
    --bs=$BLOCKSIZE \
    --rw=randrw \
    --rwmixread=50 \
    --ioengine=libaio \
    --direct=1 \
    --iodepth=$depth \
    --numjobs=2 \
    --runtime=$DURATION \
    --time_based \
    --group_reporting \
    --output-format=json \
    > "$OUTDIR/randrw_iodepth_${depth}.json"
done

# -------------------------------
# Random read sweep (important for effective_io_concurrency, random_page_cost)
# -------------------------------
for depth in 1 2; do
  echo "=================================================="
  echo "Running fio randread test: iodepth=$depth"
  echo "Target file: $TEST_DIR/testfile"
  echo "Size: $SIZE | bs: $BLOCKSIZE | runtime: $DURATION"
  echo "=================================================="

  OUTFILE="$OUTDIR/randread_iodepth_${depth}.json"

  fio --name=randread_${depth} \
    --filename=$TEST_DIR/testfile \
    --size=$SIZE \
    --bs=$BLOCKSIZE \
    --rw=randread \
    --ioengine=libaio \
    --direct=1 \
    --iodepth=$depth \
    --numjobs=1 \
    --runtime=$DURATION \
    --time_based \
    --group_reporting \
    --output-format=json \
    > "$OUTFILE"

  echo
  echo "📊 Summary for iodepth=$depth"

  jq '{
    iodepth: "'"$depth"'",
    iops: .jobs[0].read.iops,
    avg_lat_ns: .jobs[0].read.clat_ns.mean,
    p99_lat_ns: .jobs[0].read.clat_ns.percentile["99.000000"]
  }' "$OUTFILE"

  echo
done

echo -e "run,iodepth,iops,avg_lat_ms,p99_lat_ms"

#for depth in 1 2 4 8 16 32 64; do
for depth in 1 2; do
  file="$OUTDIR/randread_iodepth_${depth}.json"

  iops=$(jq '.jobs[0].read.iops' "$file")

  avg_lat_ns=$(jq '.jobs[0].read.clat_ns.mean' "$file")
  p99_lat_ns=$(jq '.jobs[0].read.clat_ns.percentile["99.000000"]' "$file")

  # convert ns → ms
  avg_lat_ms=$(awk "BEGIN {print $avg_lat_ns/1000000}")
  p99_lat_ms=$(awk "BEGIN {print $p99_lat_ns/1000000}")

  echo "randread,$depth,$iops,$avg_lat_ms,$p99_lat_ms"
done | column -t -s ","

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