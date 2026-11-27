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

######################## Data-job suffix for parallel-loading-job keys ########################
# Always set by Python, even for a single loader entry — no conditional needed.
BEXHOMA_DATA_JOB="${BEXHOMA_DATA_JOB:-1}"

######################## Get number of client in job queue ########################
# Queue is scoped by BEXHOMA_EXPERIMENT_RUN because loading (and this chunk
# assignment) is redone from scratch for every experiment_run, not once per
# experiment -- reusing an unscoped key would risk picking up a leftover
# entry from a previous run's queue.
echo "Querying message queue bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_DATA_JOB"
BEXHOMA_CHILD="$(redis-cli -h 'bexhoma-messagequeue' lpop bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_DATA_JOB)"
if [ -z "$BEXHOMA_CHILD" ]
then
	# Do not default to a fixed chunk index here: another pod may already own
	# it, and silently duplicating its chunk (while some other chunk never
	# gets loaded at all) is far worse than failing the pod outright.
	echo "FATAL: no chunk index available from message queue bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_DATA_JOB (queue empty or Redis unreachable)"
	exit 1
fi

######################## Read per-pod config from Redis ########################
BEXHOMA_POD_CONFIG_KEY="bexhoma-loading-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT-$BEXHOMA_EXPERIMENT_RUN-$BEXHOMA_DATA_JOB-config-$BEXHOMA_CHILD"
echo "Querying per-pod config at $BEXHOMA_POD_CONFIG_KEY"
BEXHOMA_POD_CONFIG_JSON="$(redis-cli -h 'bexhoma-messagequeue' get "$BEXHOMA_POD_CONFIG_KEY")"
if [ -z "$BEXHOMA_POD_CONFIG_JSON" ] || [ "$BEXHOMA_POD_CONFIG_JSON" = "nil" ]; then
	echo "No per-pod config found in Redis."
else
	eval "$(echo "$BEXHOMA_POD_CONFIG_JSON" \
	  | tr -d '{}' \
	  | tr ',' '\n' \
	  | awk 'BEGIN{FS="\""} NF>=4 && $2!="" {print "export BEXHOMA_POD_"$2"=\""$4"\""; print "echo \"BEXHOMA_POD_"$2"="$4"\""}')"
fi

######################## Show more parameters ########################
echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS:$BEXHOMA_NUM_PODS"
echo "SF:$SF"
echo "$BEXHOMA_CHILD" > /tmp/tpcds/BEXHOMA_CHILD

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
	######################## Wait until all pods of experiment are ready ########################
	if [ "$BEXHOMA_TENANT_BY" = "container" ]; then
		echo "Decrementing experiment counter bexhoma-generator-podcount-exp-$BEXHOMA_EXPERIMENT"
		redis-cli -h 'bexhoma-messagequeue' decr "bexhoma-generator-podcount-exp-$BEXHOMA_EXPERIMENT"
		while : ; do
			PODS_MISSING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-generator-podcount-exp-$BEXHOMA_EXPERIMENT)"
			echo "Pods still missing in experiment: $PODS_MISSING"
			if [[ "$PODS_MISSING" =~ ^-?[0-9]+$ ]] && test "$PODS_MISSING" -le 0
			then
				echo "OK, all pods in experiment are ready."
				break
			else
				sleep 1
			fi
		done
	fi
fi

######################## Start measurement of time ########################
bexhoma_start_epoch=$(date -u +%s)
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"

######################## Destination of raw data ########################
# /data/tpcds/SF<SF>[/<N>/<child>] (STORE_RAW_DATA=1, shared) or /tmp/tpcds/SF<SF>/<N>/<child> (local)
if test $STORE_RAW_DATA -gt 0
then
	if test $BEXHOMA_NUM_PODS -gt 1
	then
		destination_raw=/data/tpcds/SF$SF/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD
	else
		destination_raw=/data/tpcds/SF$SF
	fi
else
	destination_raw=/tmp/tpcds/SF$SF/$BEXHOMA_NUM_PODS/$BEXHOMA_CHILD
fi
mkdir -p $destination_raw
echo "destination_raw:$destination_raw"

######################## Exit if data is already there ########################
# Several pods may generate the same folder at the same time (one job per DBMS configuration,
# each with its own pods, all sharing /data). So every pod generates into its own staging
# folder next to the destination (same file system) and moves the finished files in with mv
# (atomic rename); .bexhoma_generated is written after the move. A loader never sees a
# half-written file, and no pod deletes files of another pod. dsdgen is deterministic, so all
# copies are equal. Files without the marker (a generator that failed or was killed, or an
# image before the marker) are not reused, the move replaces them.
# Recreate removes only files: with one pod the folder is /data/tpcds/SF<SF> itself, which also
# holds the <N>/<child> folders of split data.
if [ -f "$destination_raw/.bexhoma_generated" ]
then
	if test $STORE_RAW_DATA_RECREATE -gt 0
	then
		echo "Recreate raw folder"
		rm -f "$destination_raw"/*.dat "$destination_raw/.bexhoma_generated"
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
	shopt -s nullglob
	existing_dat_files=("$destination_raw"/*.dat)
	shopt -u nullglob
	if [ ${#existing_dat_files[@]} -gt 0 ]; then
		echo "Raw folder has no completion marker (generation incomplete, or from an older image): generate again"
	fi
fi
staging_raw=$destination_raw/.staging-${HOSTNAME:-$$}
rm -rf $staging_raw
mkdir -p $staging_raw
echo "staging_raw:$staging_raw"
# Remove the staging folder on every exit, also on failure: leftover copies fill the shared /data.
# The TERM/INT trap turns a signal into an exit, so the EXIT trap also runs when the pod is stopped.
trap 'rm -rf "$staging_raw"' EXIT
trap 'exit 143' TERM INT

######################## Copy generator executables ########################
cd $staging_raw
cp /tmp/tpcds.idx ./tpcds.idx
cp /tmp/dsdgen ./dsdgen

######################## Execute workload ###################
############ Differ between single-pod and multi-pod setting ############
if test $BEXHOMA_NUM_PODS -gt 1
then
	echo "./dsdgen -dir $staging_raw -scale $SF -parallel $BEXHOMA_NUM_PODS -child $BEXHOMA_CHILD -RNGSEED $RNGSEED"
	time ./dsdgen -dir $staging_raw -scale $SF -parallel $BEXHOMA_NUM_PODS -child $BEXHOMA_CHILD -RNGSEED $RNGSEED
	DSDGEN_RC=$?
else
	echo "./dsdgen -dir $staging_raw -scale $SF -RNGSEED $RNGSEED"
	time ./dsdgen -dir $staging_raw -scale $SF -RNGSEED $RNGSEED
	DSDGEN_RC=$?
fi
# -verbose

######################## Fail if generation failed (#848) ###################
# Only reached when generating: existing data exits above
shopt -s nullglob
generated_dat_files=("$staging_raw"/*.dat)
shopt -u nullglob
if [ $DSDGEN_RC -ne 0 ] || [ ${#generated_dat_files[@]} -eq 0 ]; then
	echo "FATAL: dsdgen failed (exit code $DSDGEN_RC, ${#generated_dat_files[@]} files in $staging_raw)"
	exit 1
fi

######################## Show generated files ###################
echo "Generated these files:"
ls $staging_raw/*.dat -lh

######################## End time measurement ###################
SECONDS_END=$SECONDS
echo "End $SECONDS_END seconds"

DURATION=$((SECONDS_END-SECONDS_START))
echo "Duration $DURATION seconds"

######################## Translate customer to utf8 ###################
if test $TRANSFORM_RAW_DATA -gt 0
then
	if [ -f "$staging_raw/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat" ]
	then
		# convert into new file
		echo "Convert customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat"
		if ! iconv -f ISO_8859-1 -t UTF-8 $staging_raw/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat > customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}_utf8.tmp; then
			echo "FATAL: converting customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat to UTF-8 failed"
			exit 1
		fi
		# rename to original name
		mv customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}_utf8.tmp $staging_raw/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat
		# show head of file
		head $staging_raw/customer_${BEXHOMA_CHILD}_${BEXHOMA_NUM_PODS}.dat
	fi
	if [ -f "$staging_raw/customer.dat" ]
	then
		# convert into new file
		echo "Convert customer.dat"
		if ! iconv -f ISO_8859-1 -t UTF-8 $staging_raw/customer.dat > customer_utf8.tmp; then
			echo "FATAL: converting customer.dat to UTF-8 failed"
			exit 1
		fi
		# rename to original name
		mv customer_utf8.tmp $staging_raw/customer.dat
		# show head of file
		head $staging_raw/customer.dat
	fi
fi

######################## Remove last character per line ###################
if test $TRANSFORM_RAW_DATA -gt 0
then
	echo "Remove last character per line"
	for i in $staging_raw/*.dat; do
		echo "$i"
	    time sed 's/.$//' -i $i
	    SED_RC=$?
	    if [ $SED_RC -ne 0 ]; then
	        echo "FATAL: removing the last character of $i failed (exit code $SED_RC)"
	        exit 1
	    fi
	done
fi

######################## Move generated files into place and mark them complete ###################
# Only reached when dsdgen and the transformation succeeded; a later pod reuses
# the folder only with the marker (see above)
cd /
if [ -f "$destination_raw/.bexhoma_generated" ] && test $STORE_RAW_DATA_RECREATE -eq 0
then
	echo "Another pod completed $destination_raw meanwhile, discarding this copy"
else
	if ! mv -f "${generated_dat_files[@]}" "$destination_raw"/; then
		echo "FATAL: moving the files to $destination_raw failed"
		exit 1
	fi
	echo "SF=$SF BEXHOMA_CHILD=$BEXHOMA_CHILD BEXHOMA_NUM_PODS=$BEXHOMA_NUM_PODS generated=$(date -u +%s)" > "$destination_raw/.bexhoma_generated"
fi
rm -rf $staging_raw
echo "Files in $destination_raw:"
ls $destination_raw/*.dat -lh

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
echo "BEXHOMA_CHILD:$BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS:$BEXHOMA_NUM_PODS"
echo "SF:$SF"
echo "destination_raw:$destination_raw"

######################## Exit successfully ###################
exit 0
