#!/bin/bash
# Benchmark-Experiment-Host-Manager | images/ssb/generator
# Authors: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.
#
# Dev tool (plan-ssb M1b): builds lineorder_flat for one lineorder chunk with
#   C   sort + join (customer) + gawk lookup (supplier, part), as generator.sh,
#       with and without restoring the lineorder order,
#   A   gawk lookup for customer, supplier and part (one pass, no sort),
#   D   DuckDB (flat.sql), with and without ORDER BY,
# on the same input and appends one CSV line per run: wall time, CPU time,
# largest RSS of a single process, peak size of the work folder (temp files),
# output size, rows, and whether the output equals C's ordered output (the
# unordered outputs compared after sorting).
# Needs the dev image (INCLUDE_DUCKDB=1: duckdb, GNU time).
#
# usage: compare-flat.sh <SF> <N chunks> <chunk k> <repetitions> <results.csv> [methods]
#   methods: comma list of C_ordered,C_unordered,A,D_ordered,D_unordered (default: all)
# env: SSB_COMPARE_DIR (default /work/compare), SSB_SORT_MEM (512M), SSB_DUCKDB_MEMORY (1GB)

SF=$1
N=$2
K=$3
REPEATS=${4:-3}
RESULTS=$5
METHODS=${6:-C_ordered,C_unordered,A,D_ordered,D_unordered}
D=${SSB_COMPARE_DIR:-/work/compare}
SORT_MEM=${SSB_SORT_MEM:-512M}
DUCKDB_MEMORY=${SSB_DUCKDB_MEMORY:-1GB}
export LC_ALL=C

######################## Input: one lineorder chunk and the full dimensions ########################
input=$D/input
rm -rf $D
mkdir -p $input
cd $input
if test $N -gt 1
then
	/tmp/dbgen -b /tmp/dists.dss -f -q -s $SF -T l -C $N -S $K
	lineorder=$input/lineorder.tbl.$K
else
	/tmp/dbgen -b /tmp/dists.dss -f -q -s $SF -T l
	lineorder=$input/lineorder.tbl
fi
for t in c s p; do /tmp/dbgen -b /tmp/dists.dss -f -q -s $SF -T $t; done
rows_input=$(wc -l < $lineorder)
echo "input: SF $SF, chunk $K of $N, $rows_input rows, $(du -sb $lineorder | cut -f1) bytes"

# A: all three dimensions as gawk lookup tables, lineorder streamed in its order
cat > $D/flat-a.awk <<'EOF'
function iso_date(d) { return substr(d, 1, 4) "-" substr(d, 5, 2) "-" substr(d, 7, 2) }
FNR == 1 { file++ }
file <= 3 { key = $1; sub(/^[^|]*\|/, ""); dim[file, key] = $0; next }
{
    c = dim[1, $3]; s = dim[2, $5]; p = dim[3, $4]
    $6 = iso_date($6); $16 = iso_date($16)
    print $0, c, s, p
}
EOF

JOIN_FIELDS="1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,1.10,1.11,1.12,1.13,1.14,1.15,1.16,1.17,2.2,2.3,2.4,2.5,2.6,2.7,2.8"

command_for() {
	# command_for <method> <work folder> <output file>: the command line, run with bash -c
	local work=$2 out=$3
	case $1 in
		C_ordered)
			echo "sort -t'|' -k1,1 -S $SORT_MEM -T $work $input/customer.tbl > $work/customer.sorted && \
				sort -t'|' -k3,3 -S $SORT_MEM -T $work $lineorder \
				| join -t'|' --check-order -1 3 -2 1 -o $JOIN_FIELDS - $work/customer.sorted \
				| gawk -F'|' -v OFS='|' -f /tmp/flat.awk $input/supplier.tbl $input/part.tbl - > $work/flat.unsorted && \
				sort -t'|' -k1,1n -k2,2n -S $SORT_MEM -T $work $work/flat.unsorted > $out" ;;
		C_unordered)
			echo "sort -t'|' -k1,1 -S $SORT_MEM -T $work $input/customer.tbl > $work/customer.sorted && \
				sort -t'|' -k3,3 -S $SORT_MEM -T $work $lineorder \
				| join -t'|' --check-order -1 3 -2 1 -o $JOIN_FIELDS - $work/customer.sorted \
				| gawk -F'|' -v OFS='|' -f /tmp/flat.awk $input/supplier.tbl $input/part.tbl - > $out" ;;
		A)
			echo "gawk -F'|' -v OFS='|' -f $D/flat-a.awk $input/customer.tbl $input/supplier.tbl $input/part.tbl $lineorder > $out" ;;
		D_ordered|D_unordered)
			local order=""
			if [ $1 = D_ordered ]; then order="ORDER BY CAST(l.lo_orderkey AS BIGINT), CAST(l.lo_linenumber AS INTEGER)"; fi
			sed -e "s|__MEMORY_LIMIT__|$DUCKDB_MEMORY|" -e "s|__TEMP_DIRECTORY__|$work/duckdb|" \
				-e "s|__LINEORDER__|$lineorder|" -e "s|__CUSTOMER__|$input/customer.tbl|" \
				-e "s|__SUPPLIER__|$input/supplier.tbl|" -e "s|__PART__|$input/part.tbl|" \
				-e "s|__ORDER_BY__|$order|" -e "s|__OUTPUT__|$out|" /tmp/flat.sql > $D/flat-$1.sql
			echo "duckdb < $D/flat-$1.sql" ;;
	esac
}

reference=$D/reference.tbl
reference_sorted_md5=""
if [ ! -f "$RESULTS" ]; then
	echo "method,SF,N,K,rep,rows_input,wall_s,user_s,sys_s,maxrss_single_process_kb,peak_temp_bytes,output_bytes,rows,equal_to_bash" > $RESULTS
fi
for rep in $(seq 1 $REPEATS); do
	for method in ${METHODS//,/ }; do
		work=$D/work-$method
		out=$D/out-$method.tbl
		rm -rf $work $out
		mkdir -p $work
		cmd=$(command_for $method $work $out)
		sync
		start=$(date +%s.%N)
		/usr/bin/time -f "%U %S %M" -o $D/time.txt bash -c "$cmd" &
		pid=$!
		peak=0
		while kill -0 $pid 2>/dev/null; do
			size=$(du -sb $work 2>/dev/null | cut -f1)
			if [ -n "$size" ] && [ "$size" -gt "$peak" ]; then peak=$size; fi
			sleep 0.5
		done
		wait $pid
		rc=$?
		end=$(date +%s.%N)
		wall=$(awk -v a=$start -v b=$end 'BEGIN{printf "%.2f", b-a}')
		read user sys maxrss < $D/time.txt
		rows=$(wc -l < $out)
		bytes=$(du -sb $out | cut -f1)
		# equal: ordered outputs byte for byte with C_ordered, unordered after sorting
		if [ $method = C_ordered ] && [ ! -f $reference ]; then cp $out $reference; fi
		if [ -z "$reference_sorted_md5" ] && [ -f $reference ]; then
			reference_sorted_md5=$(sort -S $SORT_MEM -T $D $reference | md5sum | cut -d' ' -f1)
		fi
		case $method in
			*_ordered|C_ordered) [ -f $reference ] && cmp -s $out $reference && equal=yes || equal=no ;;
			*) [ "$(sort -S $SORT_MEM -T $D $out | md5sum | cut -d' ' -f1)" = "$reference_sorted_md5" ] && equal=yes || equal=no ;;
		esac
		if [ $method = A ]; then
			# A keeps the lineorder order, so it must equal the ordered reference byte for byte
			cmp -s $out $reference && equal=yes || equal=no
		fi
		if [ $rc -ne 0 ]; then equal="failed($rc)"; fi
		line="$method,$SF,$N,$K,$rep,$rows_input,$wall,$user,$sys,$maxrss,$peak,$bytes,$rows,$equal"
		echo "$line" | tee -a $RESULTS
		rm -rf $work $out
	done
done
