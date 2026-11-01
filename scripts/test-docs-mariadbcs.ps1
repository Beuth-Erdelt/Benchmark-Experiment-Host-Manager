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


#### TPC-H next to MariaDB, the result sets of both are stored per connection
bexhoma tpch `
  -dbms MariaDB MariaDBCS       <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nlp 8                        <# number of data loader pods (MariaDBCS always uses 1) #> `
  -xii                          <# create indexes after data load (MariaDB: Q20 times out without) #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# store the result sets of the queries #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 16Gi                      <# RAM limit for the SUT container #> `
  -rr 16Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  -rss 20Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_mariadbcs_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H MariaDB MariaDBCS  sf=1"


#### TPC-DS next to MariaDB; the test SQL warnings fails on Q33, see docs/DBMS.md
bexhoma tpcds `
  -dbms MariaDB MariaDBCS       <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -xii                          <# create indexes after data load #> `
  -xic                          <# enforce constraints after data load #> `
  -xis                          <# run ANALYZE after data load #> `
  -xdt                          <# store the result sets of the queries #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 32Gi                      <# RAM limit for the SUT container #> `
  -rr 32Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  -rss 30Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_mariadbcs_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS MariaDBCS  sf=1"


#### SSB star schema
bexhoma ssb `
  -dbms MariaDBCS               <# DBMS under test #> `
  -sf 1                         <# scaling factor (lineorder has about 6 million rows per SF) #> `
  -xis                          <# run statistics after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 16Gi                      <# RAM limit for the SUT container #> `
  -rr 16Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  -rss 20Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ssb_mariadbcs_1.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] SSB MariaDBCS  sf=1"


#### SSB flat schema
bexhoma ssb `
  -dbms MariaDBCS               <# DBMS under test #> `
  -sf 1                         <# scaling factor (lineorder has about 6 million rows per SF) #> `
  -xsv flat                     <# one denormalized table lineorder_flat #> `
  -xis                          <# run statistics after data load #> `
  -m                            <# collect SUT resource metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 16Gi                      <# RAM limit for the SUT container #> `
  -rr 16Gi                      <# RAM requested for the SUT container #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class of the persistent volume #> `
  -rss 20Gi                     <# size of the persistent volume claim #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -nc 2                         <# two runs, the second restarts the SUT on the same data #> `
  -ar                           <# run the reset scripts before each round #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_ssb_mariadbcs_2.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] SSB MariaDBCS flat  sf=1"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
