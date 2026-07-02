#!/bin/bash

######################## Show parameters ########################
echo "BEXHOMA_HOST:$BEXHOMA_HOST"
echo "BEXHOMA_SUT_USER:$BEXHOMA_SUT_USER"
echo "BEXHOMA_SUT_KEY:$BEXHOMA_SUT_KEY"
echo "HARDWARE_THREADS:$HARDWARE_THREADS"

######################## Set SSH options ########################
SSH_OPTS="-i ${BEXHOMA_SUT_KEY} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

######################## Store raw results ########################
UUID=$(cat /proc/sys/kernel/random/uuid)
RESULT_CPU="/results/$BEXHOMA_EXPERIMENT/sysbench.$BEXHOMA_CONNECTION.$BEXHOMA_CLIENT.$UUID.cpu.txt"
RESULT_MEMORY="/results/$BEXHOMA_EXPERIMENT/sysbench.$BEXHOMA_CONNECTION.$BEXHOMA_CLIENT.$UUID.memory.txt"

######################## Run sysbench CPU benchmark ########################
echo "=== sysbench CPU ==="
ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_HOST}" \
  "sysbench cpu --cpu-max-prime=20000 --threads=${HARDWARE_THREADS} run" > "$RESULT_CPU"
cat "$RESULT_CPU"
echo "$RESULT_CPU"

######################## Run sysbench memory benchmark ########################
echo "=== sysbench Memory ==="
ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_HOST}" \
  "sysbench memory --memory-block-size=1K --memory-total-size=10G --threads=${HARDWARE_THREADS} run" > "$RESULT_MEMORY"
cat "$RESULT_MEMORY"
echo "$RESULT_MEMORY"

######################## Transform result for evaluation ########################
# sysbench has no JSON output mode, so the summary lines are pulled out with sed
# instead of parsed structurally.
cpu_events_per_sec=$(grep -m1 "events per second" "$RESULT_CPU" | sed -n 's/.*events per second: *\([0-9.]*\).*/\1/p')
cpu_total_time_s=$(grep -m1 "total time:" "$RESULT_CPU" | sed -n 's/.*total time: *\([0-9.]*\)s.*/\1/p')
cpu_lat_p95_ms=$(grep -m1 "95th percentile" "$RESULT_CPU" | sed -n 's/.*95th percentile: *\([0-9.]*\).*/\1/p')

memory_ops_per_sec=$(grep -m1 "per second)" "$RESULT_MEMORY" | sed -n 's/.*(\([0-9.]*\) per second).*/\1/p')
memory_throughput_mibps=$(grep -m1 "MiB/sec)" "$RESULT_MEMORY" | sed -n 's/.*(\([0-9.]*\) MiB\/sec).*/\1/p')
memory_lat_p95_ms=$(grep -m1 "95th percentile" "$RESULT_MEMORY" | sed -n 's/.*95th percentile: *\([0-9.]*\).*/\1/p')

######################## Echo KEY:VALUE summary ########################
echo "HARDWARE_SYSBENCH_CPU_EVENTS_PER_SEC:$cpu_events_per_sec"
echo "HARDWARE_SYSBENCH_CPU_TOTAL_TIME_S:$cpu_total_time_s"
echo "HARDWARE_SYSBENCH_CPU_LAT_P95_MS:$cpu_lat_p95_ms"
echo "HARDWARE_SYSBENCH_MEMORY_OPS_PER_SEC:$memory_ops_per_sec"
echo "HARDWARE_SYSBENCH_MEMORY_THROUGHPUT_MIBPS:$memory_throughput_mibps"
echo "HARDWARE_SYSBENCH_MEMORY_LAT_P95_MS:$memory_lat_p95_ms"