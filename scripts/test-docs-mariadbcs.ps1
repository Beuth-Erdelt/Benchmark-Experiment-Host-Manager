#Requires -Version 5.1
# Generates test logs for MariaDB ColumnStore, one run per workload that works on it.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and
# extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1




####################################################
#### Main Example ##################################
####################################################


# Main example: TPC-H on MariaDB ColumnStore, quick, without monitoring
bexhoma tpch `
  -dbms MariaDBCS               <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# two runs, the second restarts the SUT on the same data #> `
  -ks no                        <# remove the SUT at the end #> `
  -nlp 8                        <# number of data loader pods (MariaDBCS always uses 1) #> `
  -xis                          <# run ANALYZE after data load #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 16Gi                      <# RAM limit for the SUT container #> `
  -rr 16Gi                      <# RAM requested for the SUT container #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_mariadbcs.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-H MariaDBCS  sf=1"


####################################################
#### Monitoring ####################################
####################################################


# Monitoring: TPC-H on MariaDB ColumnStore at SF 10, at least 1 minute of benchmarking
bexhoma tpch `
  -dbms MariaDBCS               <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# two runs, the second restarts the SUT on the same data #> `
  -ks no                        <# remove the SUT at the end #> `
  -nlp 8                        <# number of data loader pods (MariaDBCS always uses 1) #> `
  -xis                          <# run ANALYZE after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_mariadbcs_monitoring.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-H MariaDBCS monitoring  sf=10"


####################################################
#### Persistent Storage ############################
####################################################


# Persistent storage: TPC-H next to MariaDB, the result sets of both are stored per connection
bexhoma tpch `
  -dbms MariaDB MariaDBCS       <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  -nlp 8                        <# number of data loader pods (MariaDBCS always uses 1) #> `
  -xii                          <# create indexes after data load (MariaDB: Q20 times out without) #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# store the result sets of the queries #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 16Gi                      <# RAM limit for the SUT container #> `
  -rr 16Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 20Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_mariadbcs_storage.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-H MariaDB MariaDBCS  sf=1"


####################################################
#### TPC-DS ########################################
####################################################


# TPC-DS next to MariaDB; the test SQL warnings fails on Q39, which has columns of the same name
bexhoma tpcds `
  -dbms MariaDB MariaDBCS       <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# store the result sets of the queries #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 32Gi                      <# RAM limit for the SUT container #> `
  -rr 32Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_mariadbcs.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-DS MariaDBCS  sf=1"


####################################################
#### SSB ###########################################
####################################################


# SSB star schema
bexhoma ssb `
  -dbms MariaDBCS               <# DBMS under test #> `
  -sf 1                         <# scaling factor (lineorder has about 6 million rows per SF) #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  -xis                          <# run statistics after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 16Gi                      <# RAM limit for the SUT container #> `
  -rr 16Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 20Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ssb_mariadbcs.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "SSB MariaDBCS  sf=1"


# SSB flat schema
bexhoma ssb `
  -dbms MariaDBCS               <# DBMS under test #> `
  -sf 1                         <# scaling factor (lineorder has about 6 million rows per SF) #> `
  -xsv flat                     <# one denormalized table lineorder_flat #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  -xis                          <# run statistics after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 16Gi                      <# RAM limit for the SUT container #> `
  -rr 16Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 20Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ssb_mariadbcs_flat.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "SSB MariaDBCS flat  sf=1"


#### TPC-H Refresh Stream (Example-TPC-H.md)
# TPC-H with a refresh stream on MariaDBCS: 3 query streams and one RF1/RF2 stream in parallel
bexhoma tpch `
  -dbms MariaDBCS               <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -ne 3                         <# parallel query streams #> `
  -xrs 3                        <# refresh stream: apply 3 RF1+RF2 pairs per benchmarking round, in parallel with the query streams #> `
  -nlp 8                        <# number of data loader pods #> `
  -nlt 8                        <# threads per loader pod #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_mariadbcs_refresh.log" -Encoding utf8

Write-ExperimentResult $LASTEXITCODE "TPC-H MariaDBCS refresh  sf=1  ne=3"


###########################################
############## Clean Folder ###############
###########################################


Write-ExperimentTotal
Invoke-CleanLogs
