#!/usr/bin/env bash
PYTHON="python"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TESTS=(
    validate_collector_benchbase.py
    validate_collector_benchbase_mt.py
    validate_collector_hammerdb.py
    validate_collector_tpch.py
    validate_collector_tpch_mt.py
    validate_collector_ycsb.py
)

failed=0
results=()

echo "============================================================"
echo " Bexhoma Collector Functional Tests"
echo "============================================================"

for t in "${TESTS[@]}"; do
    echo ""
    echo "[$t]"
    "$PYTHON" "$DIR/$t"
    if [ $? -ne 0 ]; then
        ((failed++))
        results+=("FAIL: $t")
    else
        results+=("PASS: $t")
    fi
done

echo ""
echo "============================================================"
echo " Summary  ($failed failed / ${#TESTS[@]} total)"
echo "============================================================"
for r in "${results[@]}"; do
    echo "  $r"
done
echo "============================================================"

exit $failed
