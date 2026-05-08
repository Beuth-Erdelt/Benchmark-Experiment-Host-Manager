#!/usr/bin/env bash
PYTHON="C:/Users/Patrick/anaconda3/envs/bexhoma/python.exe"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TESTS=(
    test_collector_benchbase.py
    test_collector_benchbase_mt.py
    test_collector_hammerdb.py
    test_collector_tpch.py
    test_collector_tpch_mt.py
    test_collector_ycsb.py
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
