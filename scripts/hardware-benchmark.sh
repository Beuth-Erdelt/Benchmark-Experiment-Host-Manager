#!/usr/bin/env bash

# apt-get -y install fio


set -euo pipefail

TEST_DIR=${1:-/data/fiotest}
DURATION=${2:-60}
SIZE=${3:-8G}

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
  --bs=8k \
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
  --bs=8k \
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
  --bs=8k \
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
for depth in 1 8 32; do
  fio --name=iodepth_${depth} \
    --filename=$TEST_DIR/testfile \
    --size=$SIZE \
    --bs=8k \
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