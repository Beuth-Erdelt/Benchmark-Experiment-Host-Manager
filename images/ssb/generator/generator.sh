#!/bin/bash

######################## Start timing ########################
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS
bexhoma_start_epoch=$(date -u +%s)

######################## Show general parameters ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_EXPERIMENT:$BEXHOMA_EXPERIMENT"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "SSB_SCHEMA_VARIANT:$SSB_SCHEMA_VARIANT"

######################## Data-job suffix for parallel-loading-job keys ########################
# Always set by Python, even for a single loader entry — no conditional needed.
BEXHOMA_DATA_JOB="${BEXHOMA_DATA_JOB:-1}"

######################## Get number of client in job queue ########################
# Queue is scoped by BEXHOMA_EXPERIMENT_RUN because loading (and this chunk
# assignment) is redone from scratch for every experiment_run.
echo "Querying message queue bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_DATA_JOB"
BEXHOMA_CHILD="$(redis-cli -h 'bexhoma-messagequeue' lpop bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_DATA_JOB)"
if [ -z "$BEXHOMA_CHILD" ]
then
	# Do not default to a fixed chunk index: another pod may already own it.
	echo "FATAL: no chunk index available from message queue bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_DATA_JOB (queue empty or Redis unreachable)"
	exit 1
fi

######################## Show more parameters ########################
echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS:$BEXHOMA_NUM_PODS"
echo "SF:$SF"
mkdir -p /tmp/ssb
echo "$BEXHOMA_CHILD" > /tmp/ssb/BEXHOMA_CHILD

######################## Destination of raw data ########################
# normal: /data/ssb/SF<SF>[/<N>/<child>]       lineorder chunk (+ dimensions in child 1)
# flat:   /data/ssb/SF<SF>/flat[/<N>/<child>]  lineorder_flat chunk
if test $STORE_RAW_DATA -gt 0
then
	base_raw=/data/ssb/SF$SF
else
	base_raw=/tmp/ssb/SF$SF
fi
if test $BEXHOMA_NUM_PODS -gt 1
then
	part_raw=/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD
else
	part_raw=""
fi
normal_raw=$base_raw$part_raw
if [ "$SSB_SCHEMA_VARIANT" = "flat" ]
then
	destination_raw=$base_raw/flat$part_raw
else
	destination_raw=$normal_raw
fi
echo "destination_raw:$destination_raw"

######################## Exit if data is already there ########################
# .complete is written as the last step, so a folder left by a pod that died halfway is regenerated.
# Only files are removed: with one pod the folder is /data/ssb/SF<SF> itself, which also
# holds flat/ and the <N>/<child> folders of other splits.
remove_raw_files() {
	rm -f "$destination_raw"/*.tbl* "$destination_raw"/.complete
}
if [ -f "$destination_raw/.complete" ]
then
	if test $STORE_RAW_DATA_RECREATE -gt 0
	then
		echo "Recreate raw folder"
		remove_raw_files
	else
		echo "Raw folder exists, I do nothing"
		DURATION_SCRIPT=$((SECONDS-SECONDS_START_SCRIPT))
		echo "Duration $DURATION_SCRIPT seconds"
		echo "BEXHOMA_DURATION:$DURATION_SCRIPT"
		bexhoma_end_epoch=$(date -u +%s)
		echo "BEXHOMA_START:$bexhoma_start_epoch"
		echo "BEXHOMA_END:$bexhoma_end_epoch"
		exit 0
	fi
else
	# incomplete leftovers of an earlier attempt
	remove_raw_files
fi
mkdir -p $destination_raw

######################## Wait until all pods of job are ready ########################
if test $BEXHOMA_SYNCH_GENERATE -gt 0
then
	echo "Decrementing job counter bexhoma-generator-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_DATA_JOB"
	redis-cli -h 'bexhoma-messagequeue' decr "bexhoma-generator-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_DATA_JOB"
	while : ; do
		PODS_MISSING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-generator-podcount-job-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_DATA_JOB)"
		echo "Pods still missing in job: $PODS_MISSING"
		if [[ "$PODS_MISSING" =~ ^-?[0-9]+$ ]] && test "$PODS_MISSING" -le 0
		then
			echo "OK, all pods in job are ready."
			break
		else
			sleep 1
		fi
	done
fi

######################## Start measurement of time ########################
bexhoma_start_epoch=$(date -u +%s)
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"

######################## dbgen helpers ########################
# Only lineorder is chunked (-C/-S): in the chunked path dbgen scales part linearly
# instead of 200,000*floor(1+log2 SF) and gives date 2557*SF/N rows, so the
# dimensions are always generated unchunked
run_dbgen() {
	# run_dbgen <folder> <dbgen arguments...>
	local folder=$1
	shift
	echo "(cd $folder && dbgen -b /tmp/dists.dss -f -q -s $SF $*)"
	(cd $folder && time /tmp/dbgen -b /tmp/dists.dss -f -q -s $SF "$@")
	local rc=$?
	if [ $rc -ne 0 ]; then
		echo "FATAL: dbgen $* failed with exit code $rc"
		exit 1
	fi
}
generate_lineorder() {
	# generate_lineorder <folder>: this pod's lineorder chunk
	if test $BEXHOMA_NUM_PODS -gt 1
	then
		run_dbgen $1 -T l -C $BEXHOMA_NUM_PODS -S $BEXHOMA_CHILD
	else
		run_dbgen $1 -T l
	fi
}
count_lines() {
	local wordcount=($(wc -l "$1"))
	echo ${wordcount[0]}
}

######################## Execute workload ###################
if [ "$SSB_SCHEMA_VARIANT" = "flat" ]
then
	######################## Flat: stream lineorder through the dimensions ########################
	work=$SSB_WORK_DIR/ssb-$BEXHOMA_EXPERIMENT-$BEXHOMA_CHILD
	rm -rf $work
	mkdir -p $work/sorttmp
	echo "work:$work"
	# lineorder chunk: reuse a complete normal chunk, otherwise generate it
	lineorder_file=""
	if [ -f "$normal_raw/.complete" ]
	then
		shopt -s nullglob
		existing=("$normal_raw"/lineorder.tbl*)
		shopt -u nullglob
		if [ ${#existing[@]} -eq 1 ]; then
			lineorder_file=${existing[0]}
			echo "Reusing normal lineorder chunk $lineorder_file"
		fi
	fi
	if [ -z "$lineorder_file" ]
	then
		generate_lineorder $work
		shopt -s nullglob
		existing=("$work"/lineorder.tbl*)
		shopt -u nullglob
		lineorder_file=${existing[0]}
	fi
	# full dimensions: dbgen is deterministic, every pod gets the same rows
	run_dbgen $work -T c
	run_dbgen $work -T s
	run_dbgen $work -T p
	export LC_ALL=C
	SSB_SORT_MEM=${SSB_SORT_MEM:-512M}
	echo "Sort customer by c_custkey"
	time sort -t'|' -k1,1 -S $SSB_SORT_MEM -T $work/sorttmp $work/customer.tbl > $work/customer.sorted
	# join output: all 17 lineorder columns, then the customer columns without the key
	JOIN_FIELDS="1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,1.10,1.11,1.12,1.13,1.14,1.15,1.16,1.17,2.2,2.3,2.4,2.5,2.6,2.7,2.8"
	if test $SSB_FLAT_RESTORE_ORDER -gt 0
	then
		flat_unsorted=$work/lineorder_flat.unsorted
	else
		flat_unsorted=$destination_raw/lineorder_flat.tbl
	fi
	echo "Stream lineorder: sort by lo_custkey | join customer | awk supplier, part"
	time sort -t'|' -k3,3 -S $SSB_SORT_MEM -T $work/sorttmp $lineorder_file \
		| join -t'|' --check-order -1 3 -2 1 -o $JOIN_FIELDS - $work/customer.sorted \
		| gawk -F'|' -v OFS='|' -f /tmp/flat.awk $work/supplier.tbl $work/part.tbl - \
		> $flat_unsorted
	PIPE_RC=("${PIPESTATUS[@]}")
	if [ "${PIPE_RC[0]}" -ne 0 ] || [ "${PIPE_RC[1]}" -ne 0 ] || [ "${PIPE_RC[2]}" -ne 0 ]; then
		echo "FATAL: flat pipeline failed (sort ${PIPE_RC[0]}, join ${PIPE_RC[1]}, awk ${PIPE_RC[2]})"
		exit 1
	fi
	if test $SSB_FLAT_RESTORE_ORDER -gt 0
	then
		echo "Restore lineorder order (lo_orderkey, lo_linenumber)"
		time sort -t'|' -k1,1n -k2,2n -S $SSB_SORT_MEM -T $work/sorttmp $flat_unsorted > $destination_raw/lineorder_flat.tbl
		if [ $? -ne 0 ]; then
			echo "FATAL: sort by lo_orderkey failed"
			exit 1
		fi
	fi
	# join drops unmatched lines without an error, so the row count is the real check
	lines_lineorder=$(count_lines $lineorder_file)
	lines_flat=$(count_lines $destination_raw/lineorder_flat.tbl)
	echo "Rows lineorder chunk: $lines_lineorder"
	echo "Rows lineorder_flat:  $lines_flat"
	if [ "$lines_lineorder" != "$lines_flat" ]; then
		echo "FATAL: lineorder_flat has $lines_flat rows, lineorder chunk has $lines_lineorder"
		exit 1
	fi
	rm -rf $work
else
	######################## Normal: lineorder chunk, dimensions in child 1 ########################
	generate_lineorder $destination_raw
	if test $BEXHOMA_CHILD -eq 1
	then
		run_dbgen $destination_raw -T c
		run_dbgen $destination_raw -T s
		run_dbgen $destination_raw -T p
		run_dbgen $destination_raw -T d
	fi
fi

######################## Fail if generation failed ###################
shopt -s nullglob
generated_tbl_files=("$destination_raw"/*tbl*)
shopt -u nullglob
if [ ${#generated_tbl_files[@]} -eq 0 ]; then
	echo "FATAL: no files in $destination_raw"
	exit 1
fi

######################## Show generated files ###################
# No trailing '|' to remove: the image builds dbgen with EOL_HANDLING
echo "Generated these files:"
ls $destination_raw/*tbl* -lh
touch $destination_raw/.complete

######################## End measurement of time ########################
bexhoma_end_epoch=$(date -u +%s)
SECONDS_END=$SECONDS
echo "End $SECONDS_END seconds"

DURATION=$((SECONDS_END-SECONDS_START))
echo "Duration $DURATION seconds"

######################## Show timing information ###################
echo "Generating done"

DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "NOW: $DATEANDTIME"

SECONDS_END_SCRIPT=$SECONDS
DURATION_SCRIPT=$((SECONDS_END_SCRIPT-SECONDS_START_SCRIPT))
echo "Duration $DURATION_SCRIPT seconds (script total)"
echo "BEXHOMA_DURATION:$DURATION_SCRIPT"
echo "BEXHOMA_START:$bexhoma_start_epoch"
echo "BEXHOMA_END:$bexhoma_end_epoch"

######################## Parameters summary ########################
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_EXPERIMENT:$BEXHOMA_EXPERIMENT"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_BENCHMARK_RUN:$BEXHOMA_BENCHMARK_RUN"
echo "SF:$SF"
echo "SSB_SCHEMA_VARIANT:$SSB_SCHEMA_VARIANT"
echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS:$BEXHOMA_NUM_PODS"
echo "destination_raw:$destination_raw"

######################## Exit successfully ###################
exit 0
