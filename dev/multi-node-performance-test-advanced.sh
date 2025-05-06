#!/bin/bash

# Farben
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

NODES=("$@")
CSV_FILE="performance_results.csv"

echo "Received nodes: $@"

if [ ${#NODES[@]} -eq 0 ]; then
  echo -e "${RED}Usage: $0 <node1> <node2> <node3> ...${NC}"
  exit 1
fi

echo "Node,CPU Bogo Ops,Memory Ops,Disk Write Speed (MiB/s),Network Speed (Mbit/s)" > "$CSV_FILE"

NODE_COUNT=${#NODES[@]}
CURRENT=0

# echo "$NODE_COUNT"
# exit 0

for NODE in "${NODES[@]}"; do
  CURRENT=$((CURRENT + 1))
  echo -e "${YELLOW}[$CURRENT/$NODE_COUNT] Starte Test auf Node: $NODE${NC}"

  # Pod starten
  cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: node-performance-test-advanced
spec:
  tolerations:
  - key: "nvidia.com/gpu"
    effect: "NoSchedule"
  nodeSelector:
    kubernetes.io/hostname: $NODE
  restartPolicy: Never
  containers:
  - name: performance-tester
    image: ubuntu:22.04
    command: ["/bin/bash", "-c"]
    args:
      - |
        apt-get update && apt-get install -y stress-ng fio iperf3;
        stress-ng --cpu 4 --timeout 60 --metrics-brief > /cpu.txt;
        stress-ng --vm 2 --vm-bytes 512M --timeout 60 --metrics-brief > /mem.txt;
        fio --name=writefile --size=100M --filename=/tmp/testfile --bs=4k --rw=randwrite --direct=1 --numjobs=1 --runtime=60 --group_reporting > /fio.txt;
        iperf3 -s & sleep 3 && iperf3 -c localhost -t 30 > /iperf.txt;
        cat /cpu.txt /mem.txt /fio.txt /iperf.txt;
        sleep 5;
EOF

  # Auf Pod warten
  echo "Warte auf Testabschluss..."
  while true; do
    phase=$(kubectl get pod node-performance-test-advanced -o jsonpath='{.status.phase}')
    if [[ "$phase" == "Succeeded" ]]; then
      echo "✅ Pod completed successfully!"
      break
    elif [[ "$phase" == "Failed" ]]; then
      echo "❌ Pod failed!"
      echo "$NODE,FAILED,FAILED,FAILED,FAILED" >> "$CSV_FILE"
      continue
      # exit 1
    else
      echo "⏳ Waiting, current phase: $phase"
      sleep 5
    fi
  done

  #if kubectl wait --for=condition=Succeeded pod/node-performance-test-advanced --timeout=600s > /dev/null 2>&1; then
  #  echo -e "${GREEN}Test abgeschlossen!${NC}"
  #else
  #  echo -e "${RED}Test auf Node $NODE fehlgeschlagen.${NC}"
  #  LOGS=$(kubectl logs node-performance-test-advanced)
  #  cat LOGS
  #  #kubectl delete pod node-performance-test-advanced --ignore-not-found
  #  echo "$NODE,FAILED,FAILED,FAILED,FAILED" >> "$CSV_FILE"
  #  continue
  #fi

  # Logs holen
  LOGS=$(kubectl logs node-performance-test-advanced)

  CPU_OPS=$(echo "$LOGS" | grep "info:" | grep -E "\scpu\s+[0-9]" | awk '{print $5}')
  MEM_OPS=$(echo "$LOGS" | grep "info:" | grep -E "\svm\s+[0-9]" | awk '{print $5}')

  # CPU Bogo-Ops extrahieren
  #CPU_OPS=$(echo "$LOGS" | grep "cpu bogo ops" | awk '{print $4}')
  if [ -z "$CPU_OPS" ]; then CPU_OPS="N/A"; fi

  # Memory Ops extrahieren
  #MEM_OPS=$(echo "$LOGS" | grep "vm bogo ops" | awk '{print $4}')
  if [ -z "$MEM_OPS" ]; then MEM_OPS="N/A"; fi

  # Disk Write Speed extrahieren (MiB/s)
  DISK_SPEED=$(echo "$LOGS" | grep WRITE: | awk -F',' '{print $1}' | awk -F'=' '{print $2}' | sed 's/ //g')
  if [ -z "$DISK_SPEED" ]; then DISK_SPEED="N/A"; fi

  # Network Speed extrahieren (Mbit/s)
  #NET_SPEED=$(echo "$LOGS" | grep 'receiver' | tail -n1 | awk '{print $(NF-1)}')
  #NET_SPEED=$(echo "$LOGS" | grep -E "\[ *[0-9]+\]" | grep -v "sender" | tail -n1 | awk '{print $7, $8}')
  #NET_SPEED=$(echo "$LOGS" | grep -E "\[ *[0-9]+\]" | grep -v sender | tail -n1 | awk '{if ($8=="Gbits/sec") print $7*1000; else if ($8=="Mbits/sec") print $7}')
  NET_SPEED_RAW=$(echo "$LOGS" | grep -E "\[ *[0-9]+\]" | grep -v sender | tail -n1 | awk '{print $7, $8}')
  VALUE=$(echo "$NET_SPEED_RAW" | awk '{print $1}')
  UNIT=$(echo "$NET_SPEED_RAW" | awk '{print $2}')

  # Now do math with bc
  if [[ "$UNIT" == "Gbits/sec" ]]; then
    NET_SPEED=$(echo "$VALUE * 1000" | bc)
  elif [[ "$UNIT" == "Mbits/sec" ]]; then
    NET_SPEED=$VALUE
  else
    echo "⚠️ Unknown unit: $UNIT"
    NET_SPEED="0"
  fi
  echo "Speed: ${NET_SPEED} Mbit/s"
  #echo "Speed: $SPEED_MBIT Mbit/s"

  if [ -z "$NET_SPEED" ]; then NET_SPEED="N/A"; fi

  # Ergebnis in CSV schreiben
  echo "$NODE,$CPU_OPS,$MEM_OPS,$DISK_SPEED,$NET_SPEED" >> "$CSV_FILE"

  # Pod löschen
  kubectl delete pod node-performance-test-advanced --ignore-not-found

  echo -e "${GREEN}[$CURRENT/$NODE_COUNT] Node $NODE fertig getestet.${NC}"
  echo "--------------------------------------------"
done

echo -e "${GREEN}Alle Tests abgeschlossen.${NC}"
echo "Ergebnisse gespeichert in ${YELLOW}$CSV_FILE${NC}"
