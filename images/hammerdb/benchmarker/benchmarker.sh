#!/bin/bash

######################## Start timing ########################
bexhoma_start_epoch=$(date -u +%s)
DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "$DATEANDTIME"
SECONDS_START_SCRIPT=$SECONDS

######################## Show general parameters ########################
echo "HAMMERDB_TYPE=$HAMMERDB_TYPE"
echo "BEXHOMA_CONNECTION:$BEXHOMA_CONNECTION"
echo "BEXHOMA_EXPERIMENT_RUN:$BEXHOMA_EXPERIMENT_RUN"
echo "BEXHOMA_CONFIGURATION:$BEXHOMA_CONFIGURATION"
echo "BEXHOMA_CLIENT:$BEXHOMA_CLIENT"
echo "BEXHOMA_CHILD $BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS $BEXHOMA_NUM_PODS"
echo "SF $SF"
echo "HAMMERDB_NUM_VU $HAMMERDB_NUM_VU"
echo "HAMMERDB_ITERATIONS $HAMMERDB_ITERATIONS"
echo "HAMMERDB_DURATION $HAMMERDB_DURATION"
echo "HAMMERDB_RAMPUP $HAMMERDB_RAMPUP"
echo "HAMMERDB_TIMEPROFILE $HAMMERDB_TIMEPROFILE"
echo "HAMMERDB_ALLWAREHOUSES $HAMMERDB_ALLWAREHOUSES"
echo "HAMMERDB_KEYANDTHINK $HAMMERDB_KEYANDTHINK"

######################## Wait for synched starting time ########################
echo "benchmark started at $BEXHOMA_TIME_NOW"
echo "benchmark should wait until $BEXHOMA_TIME_START"
if test "$BEXHOMA_TIME_START" != "0"
then
    benchmark_start_epoch=$(date -u -d "$BEXHOMA_TIME_NOW" +%s)
    echo "that is $benchmark_start_epoch"

    TZ=UTC printf -v current_epoch '%(%Y-%m-%d %H:%M:%S)T\n' -1 
    echo "now is $current_epoch"
    current_epoch=$(date -u +%s)
    echo "that is $current_epoch"
    target_epoch=$(date -u -d "$BEXHOMA_TIME_START" +%s)
    echo "wait until $BEXHOMA_TIME_START"
    echo "that is $target_epoch"
    sleep_seconds=$(( $target_epoch - $current_epoch ))
    echo "that is wait $sleep_seconds seconds"

    if test $sleep_seconds -lt 0
    then
        echo "start time has already passed"
        exit 0
    fi

    sleep $sleep_seconds
    bexhoma_start_epoch=$(date -u +%s)
else
    echo "ignore that start time"
fi

######################## Make sure result folder exists ########################
mkdir -p /results/$BEXHOMA_EXPERIMENT

######################## Get number of client in job queue ########################
echo "Querying message queue bexhoma-benchmarker-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
# redis-cli -h 'bexhoma-messagequeue' lpop "bexhoma-benchmarker-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
BEXHOMA_CHILD="$(redis-cli -h 'bexhoma-messagequeue' lpop bexhoma-benchmarker-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
if [ -z "$BEXHOMA_CHILD" ]
then
    echo "No entry found in message queue. I assume this is the first child."
    BEXHOMA_CHILD=1
else
    echo "Found entry number $BEXHOMA_CHILD in message queue."
fi

######################## Wait until all pods of job are ready ########################
echo "Querying counter bexhoma-benchmarker-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
# add this pod to counter
redis-cli -h 'bexhoma-messagequeue' incr "bexhoma-benchmarker-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT"
# wait for number of pods to be as expected
while : ; do
    PODS_RUNNING="$(redis-cli -h 'bexhoma-messagequeue' get bexhoma-benchmarker-podcount-$BEXHOMA_CONNECTION-$BEXHOMA_EXPERIMENT)"
    echo "Found $PODS_RUNNING / $BEXHOMA_NUM_PODS running pods"
    if [[ "$PODS_RUNNING" =~ ^[0-9]+$ ]]
    then
        echo "PODS_RUNNING contains a number."
    else
        echo "PODS_RUNNING does not contain a number."
        exit 0
    fi
    if  test "$PODS_RUNNING" == $BEXHOMA_NUM_PODS
    then
        echo "OK, found $BEXHOMA_NUM_PODS ready pods."
        break
    elif test "$PODS_RUNNING" -gt $BEXHOMA_NUM_PODS
    then
        echo "Too many pods! Restart occured?"
        exit 0
    else
        echo "We have to wait"
        sleep 1
    fi
done

######################## Show more parameters ########################
echo "BEXHOMA_CHILD $BEXHOMA_CHILD"
echo "BEXHOMA_NUM_PODS $BEXHOMA_NUM_PODS"
echo "SF $SF"

######################## Generate workflow file ########################
# https://www.hammerdb.com/docs3.3/ch08s08.html
# duration: in minutes
# https://www.hammerdb.com/docs/ch09s03.html
# runtimer deprecated starting with v4.6
######################## Workflow: MySQL ###################

if [ "$HAMMERDB_TYPE" = "mysql" ]; then
    USER=root
    PASSWORD=root
    echo "#!/bin/tclsh
proc runtimer { seconds } {
set x 0
set timerstop 0
while {!\$timerstop} {
incr x
after 1000
  if { ![ expr {\$x % 60} ] } {
          set y [ expr \$x / 60 ]
          puts \"Timer: \$y minutes elapsed\"
  }
update
if {  [ vucomplete ] || \$x eq \$seconds } { set timerstop 1 }
    }
return
}
puts \"SETTING CONFIGURATION\"
dbset db mysql
diset connection mysql_host $BEXHOMA_HOST
diset connection mysql_port $BEXHOMA_PORT
diset tpcc mysql_count_ware $SF
diset tpcc mysql_num_vu $HAMMERDB_NUM_VU
diset tpcc mysql_user $BEXHOMA_USER
diset tpcc mysql_pass $BEXHOMA_PASSWORD
diset tpcc mysql_driver timed
diset tpcc mysql_rampup $HAMMERDB_RAMPUP
diset tpcc mysql_duration $HAMMERDB_DURATION
diset tpcc mysql_total_iterations $HAMMERDB_ITERATIONS
diset tpcc mysql_timeprofile $HAMMERDB_TIMEPROFILE
diset tpcc mysql_allwarehouse $HAMMERDB_ALLWAREHOUSES
diset tpcc mysql_keyandthink $HAMMERDB_KEYANDTHINK
vuset logtotemp 1
loadscript
puts \"SEQUENCE STARTED\"
foreach z { $HAMMERDB_VUSERS } {
puts \"\$z VU TEST\"
vuset vu \$z
vucreate
vurun
runtimer 600
vudestroy
after 5000
        }
puts \"TEST SEQUENCE COMPLETE\"" > benchmark.tcl
fi

######################## Generate workflow file ########################
######################## Workflow: MariaDB ###################

if [ "$HAMMERDB_TYPE" = "mariadb" ]; then
    USER=root
    PASSWORD=root
    echo "#!/bin/tclsh
proc runtimer { seconds } {
set x 0
set timerstop 0
while {!\$timerstop} {
incr x
after 1000
  if { ![ expr {\$x % 60} ] } {
          set y [ expr \$x / 60 ]
          puts \"Timer: \$y minutes elapsed\"
  }
update
if {  [ vucomplete ] || \$x eq \$seconds } { set timerstop 1 }
    }
return
}
puts \"SETTING CONFIGURATION\"
dbset db maria
diset connection maria_host $BEXHOMA_HOST
diset connection maria_port $BEXHOMA_PORT
diset tpcc maria_count_ware $SF
diset tpcc maria_num_vu $HAMMERDB_NUM_VU
diset tpcc maria_user $BEXHOMA_USER
diset tpcc maria_pass $BEXHOMA_PASSWORD
diset tpcc maria_driver timed
diset tpcc maria_rampup $HAMMERDB_RAMPUP
diset tpcc maria_duration $HAMMERDB_DURATION
diset tpcc maria_total_iterations $HAMMERDB_ITERATIONS
diset tpcc maria_timeprofile $HAMMERDB_TIMEPROFILE
diset tpcc maria_allwarehouse $HAMMERDB_ALLWAREHOUSES
diset tpcc maria_keyandthink $HAMMERDB_KEYANDTHINK
vuset logtotemp 1
loadscript
puts \"SEQUENCE STARTED\"
foreach z { $HAMMERDB_VUSERS } {
puts \"\$z VU TEST\"
vuset vu \$z
vucreate
vurun
runtimer 600
vudestroy
after 5000
        }
puts \"TEST SEQUENCE COMPLETE\"" > benchmark.tcl
fi

######################## Generate workflow file ########################
######################## Workflow: PostgreSQL ###################

if [ "$HAMMERDB_TYPE" = "postgresql" ]; then
    echo "#!/bin/tclsh
puts \"SETTING CONFIGURATION\"
dbset db pg
diset connection pg_host $BEXHOMA_HOST
diset connection pg_port $BEXHOMA_PORT
diset tpcc pg_count_ware $SF
diset tpcc pg_num_vu $HAMMERDB_NUM_VU
diset tpcc pg_superuser postgres
diset tpcc pg_superuserpass postgres
diset tpcc pg_defaultdbase postgres
diset tpcc pg_user $BEXHOMA_USER
diset tpcc pg_pass $BEXHOMA_PASSWORD
diset tpcc pg_dbase tpcc
diset tpcc pg_driver timed
diset tpcc pg_rampup $HAMMERDB_RAMPUP
diset tpcc pg_duration $HAMMERDB_DURATION
diset tpcc pg_total_iterations $HAMMERDB_ITERATIONS
diset tpcc pg_timeprofile $HAMMERDB_TIMEPROFILE
diset tpcc pg_allwarehouse $HAMMERDB_ALLWAREHOUSES
diset tpcc pg_keyandthink $HAMMERDB_KEYANDTHINK
vuset logtotemp 1
tcset unique 0
tcset refreshrate 10
tcset timestamps 1
tcset logtotemp 1
loadscript
puts \"SEQUENCE STARTED\"
foreach z { $HAMMERDB_VUSERS } {
    puts \"\$z VU TEST\"
    vuset vu \$z
    vucreate
    vurun
    vudestroy
    after 5000
}
puts \"TEST SEQUENCE COMPLETE\"" > benchmark.tcl
fi

######################## Generate workflow file ########################
######################## Workflow: Citus ###################

if [ "$HAMMERDB_TYPE" = "citus" ]; then
    echo "#!/bin/tclsh
proc runtimer { seconds } {
set x 0
set timerstop 0
while {!\$timerstop} {
incr x
after 1000
  if { ![ expr {\$x % 60} ] } {
          set y [ expr \$x / 60 ]
          puts \"Timer: \$y minutes elapsed\"
  }
update
if {  [ vucomplete ] || \$x eq \$seconds } { set timerstop 1 }
    }
return
}
puts \"SETTING CONFIGURATION\"
dbset db pg
diset connection pg_host $BEXHOMA_HOST
diset connection pg_port $BEXHOMA_PORT
diset tpcc pg_count_ware $SF
diset tpcc pg_num_vu $HAMMERDB_NUM_VU
diset tpcc pg_superuser postgres
diset tpcc pg_superuserpass postgres
diset tpcc pg_defaultdbase postgres
diset tpcc pg_user $BEXHOMA_USER
diset tpcc pg_pass $BEXHOMA_PASSWORD
diset tpcc pg_dbase $BEXHOMA_DATABASE
diset tpcc pg_driver timed
diset tpcc pg_rampup $HAMMERDB_RAMPUP
diset tpcc pg_duration $HAMMERDB_DURATION
diset tpcc pg_total_iterations $HAMMERDB_ITERATIONS
diset tpcc pg_cituscompat true
diset tpcc pg_storedprocs false
diset tpcc pg_timeprofile $HAMMERDB_TIMEPROFILE
diset tpcc pg_allwarehouse $HAMMERDB_ALLWAREHOUSES
diset tpcc pg_keyandthink $HAMMERDB_KEYANDTHINK
vuset logtotemp 1
loadscript
print vuconf
puts \"SEQUENCE STARTED\"
foreach z { $HAMMERDB_VUSERS } {
puts \"\$z VU TEST\"
vuset vu \$z
vucreate
runtimer $HAMMERDB_DURATION
vurun
vudestroy
after 5000
        }
puts \"TEST SEQUENCE COMPLETE\"" > benchmark.tcl
fi

######################## Show workflow file ########################
cat benchmark.tcl

######################## Start measurement of time ########################
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"
bexhoma_start_epoch=$(date -u +%s)

######################## Execute workload ###################
./hammerdbcli auto benchmark.tcl

######################## End time measurement ###################
SECONDS_END=$SECONDS
echo "End $SECONDS_END seconds"

DURATION=$((SECONDS_END-SECONDS_START))
echo "Duration $DURATION seconds"

######################## Store results ###################
UUID=$(cat /proc/sys/kernel/random/uuid)
cp /tmp/hammerdb.log /results/$BEXHOMA_EXPERIMENT/hammerdb.$BEXHOMA_CONNECTION.$BEXHOMA_CLIENT.$UUID.log
echo "/results/$BEXHOMA_EXPERIMENT/hammerdb.$BEXHOMA_CONNECTION.$BEXHOMA_CLIENT.$UUID.log"
# cat /results/$BEXHOMA_EXPERIMENT/hammerdb.$BEXHOMA_CONNECTION.$BEXHOMA_CLIENT.$UUID.log
echo "/tmp/hdbxtprofile.log"
cat /tmp/hdbxtprofile.log
ls /tmp -lh

######################## Show timing information ###################
echo "Benchmarking done"

DATEANDTIME=$(date '+%d.%m.%Y %H:%M:%S');
echo "$DATEANDTIME"

SECONDS_END_SCRIPT=$SECONDS
DURATION_SCRIPT=$((SECONDS_END_SCRIPT-SECONDS_START_SCRIPT))
echo "Duration $DURATION_SCRIPT seconds"
echo "BEXHOMA_DURATION:$DURATION_SCRIPT"

bexhoma_end_epoch=$(date -u +%s)
echo "BEXHOMA_START:$bexhoma_start_epoch"
echo "BEXHOMA_END:$bexhoma_end_epoch"

######################## Exit successfully ###################
exit 0

