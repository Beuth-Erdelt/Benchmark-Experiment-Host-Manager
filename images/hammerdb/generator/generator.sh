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
echo "CHILD $CHILD"
echo "NUM_PODS $NUM_PODS"
echo "SF $SF"
echo "PARALLEL $PARALLEL"
echo "HAMMERDB_ITERATIONS $HAMMERDB_ITERATIONS"
echo "HAMMERDB_DURATION $HAMMERDB_DURATION"
echo "HAMMERDB_RAMPUP $HAMMERDB_RAMPUP"
echo "HAMMERDB_VUSERS $HAMMERDB_VUSERS"

######################## Generate workflow file ########################
######################## Workflow: MySQL ###################

if [ "$HAMMERDB_TYPE" = "mysql" ]; then
    #USER=root
    #PASSWORD=root
	echo "puts \"SETTING CONFIGURATION\"
global complete
proc wait_to_complete {} {
global complete
set complete [vucomplete]
if {!\$complete} { after 5000 wait_to_complete } else { exit }
}
dbset db mysql
diset connection mysql_host $BEXHOMA_HOST
diset connection mysql_port $BEXHOMA_PORT
diset tpcc mysql_user $USER
diset tpcc mysql_pass $PASSWORD
diset tpcc mysql_partition true
diset tpcc mysql_storage_engine $HAMMERDB_MYSQL_ENGINE
diset tpcc mysql_count_ware $SF
diset tpcc mysql_num_vu $HAMMERDB_VUSERS
print dict
buildschema
wait_to_complete
vwait forever" > load.tcl
fi

######################## Generate workflow file ########################
######################## Workflow: MariaDB ###################

if [ "$HAMMERDB_TYPE" = "mariadb" ]; then
    USER=root
    PASSWORD=root
	echo "puts \"SETTING CONFIGURATION\"
global complete
proc wait_to_complete {} {
global complete
set complete [vucomplete]
if {!\$complete} { after 5000 wait_to_complete } else { exit }
}
dbset db maria
diset connection maria_host $BEXHOMA_HOST
diset connection maria_port $BEXHOMA_PORT
diset tpcc maria_user $USER
diset tpcc maria_pass $PASSWORD
diset tpcc maria_partition true
diset tpcc maria_storage_engine $HAMMERDB_MYSQL_ENGINE
diset tpcc maria_count_ware $SF
diset tpcc maria_num_vu $HAMMERDB_VUSERS
print dict
buildschema
wait_to_complete
vwait forever" > load.tcl
fi

######################## Generate workflow file ########################
######################## Workflow: PostgreSQL ###################

if [ "$HAMMERDB_TYPE" = "postgresql" ]; then
    echo "puts \"SETTING CONFIGURATION\"
global complete
proc wait_to_complete {} {
global complete
set complete [vucomplete]
if {!\$complete} { after 5000 wait_to_complete } else { exit }
}
dbset db pg
diset connection pg_host $BEXHOMA_HOST
diset connection pg_port $BEXHOMA_PORT
diset tpcc pg_count_ware $SF
diset tpcc pg_num_vu $HAMMERDB_VUSERS
diset tpcc pg_superuser postgres
diset tpcc pg_superuserpass postgres
diset tpcc pg_defaultdbase postgres
diset tpcc pg_user $USER
diset tpcc pg_pass $PASSWORD
diset tpcc pg_dbase tpcc
print dict
buildschema
wait_to_complete
vwait forever" > load.tcl
fi

######################## Generate workflow file ########################
######################## Workflow: Citus ###################

if [ "$HAMMERDB_TYPE" = "citus" ]; then
    echo "puts \"SETTING CONFIGURATION\"
global complete
proc wait_to_complete {} {
global complete
set complete [vucomplete]
if {!\$complete} { after 5000 wait_to_complete } else { exit }
}
dbset db pg
diset connection pg_host $BEXHOMA_HOST
diset connection pg_port $BEXHOMA_PORT
diset tpcc pg_count_ware $SF
diset tpcc pg_num_vu $HAMMERDB_VUSERS
diset tpcc pg_superuser postgres
diset tpcc pg_superuserpass postgres
diset tpcc pg_defaultdbase postgres
diset tpcc pg_user $USER
diset tpcc pg_pass $PASSWORD
diset tpcc pg_dbase $DATABASE
diset tpcc pg_cituscompat true
print dict
buildschema
wait_to_complete
vwait forever" > load.tcl
fi


######################## Show workflow file ########################
cat load.tcl

######################## Start measurement of time ########################
SECONDS_START=$SECONDS
echo "Start $SECONDS_START seconds"
bexhoma_start_epoch=$(date -u +%s)

######################## Execute workload ###################
./hammerdbcli auto load.tcl

######################## End time measurement ###################
SECONDS_END=$SECONDS
echo "End $SECONDS_END seconds"

DURATION=$((SECONDS_END-SECONDS_START))
echo "Duration $DURATION seconds"

######################## Show timing information ###################
echo "Generating done"

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

