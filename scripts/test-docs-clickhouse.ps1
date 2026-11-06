#Requires -Version 5.1
# Generates documentation summaries for ClickHouse experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2026 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1




####################################################
#### Main Example ##################################
####################################################


# Main example: TPC-H on ClickHouse, quick, without monitoring
bexhoma tpch `
  -dbms ClickHouse              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# number of repeated runs per configuration (2nd run: data survives the SUT restart) #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lc 16                        <# CPU limit for the SUT container #> `
  -rc 16                        <# CPU requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_clickhouse.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H ClickHouse  sf=1"


####################################################
#### Monitoring ####################################
####################################################


# Monitoring: TPC-H on ClickHouse at SF 10 with application metrics, at least 1 minute of benchmarking
bexhoma tpch `
  -dbms ClickHouse              <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# number of repeated runs per configuration (2nd run: data survives the SUT restart) #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -xqr 10                       <# repeat each query 10 times, so the benchmarking phase lasts long enough for monitoring #> `
  -nlp 8                        <# number of data loader pods #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lc 16                        <# CPU limit for the SUT container #> `
  -rc 16                        <# CPU requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_clickhouse_monitoring.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H ClickHouse monitoring  sf=10"


####################################################
#### Persistent Storage ############################
####################################################


# Persistent storage: TPC-H on ClickHouse, the second run finds the data on the volume
bexhoma tpch `
  -dbms ClickHouse              <# DBMS under test #> `
  -sf 10                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration (2nd run: data survives the SUT restart) #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lc 16                        <# CPU limit for the SUT container #> `
  -rc 16                        <# CPU requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_clickhouse_storage.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H ClickHouse  sf=10  nc=2"


####################################################
#### Variants ######################################
####################################################


# Variant cluster: TPC-H on ClickHouseCluster with 3 shards
bexhoma tpch `
  -dbms ClickHouseCluster       <# DBMS under test #> `
  -nw 3                         <# number of worker nodes (shards) #> `
  -sf 10                         <# scaling factor (controls database size in GB) #> `
  -nc 2                         <# number of repeated runs per configuration (2nd run: data survives the SUT restart) #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lc 16                        <# CPU limit for the SUT container and each worker #> `
  -rc 16                        <# CPU requested for the SUT container and each worker #> `
  -lr 64Gi                      <# RAM limit for the SUT container and each worker #> `
  -rr 64Gi                      <# RAM requested for the SUT container and each worker #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 50Gi                     <# size of the persistent volume claims #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rnw $BEXHOMA_NODES_WORKER    <# schedule worker pods on these nodes (joined by '+') #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpch_clickhouse_cluster.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-H ClickHouseCluster  sf=10  nw=3  nc=2"


####################################################
#### TPC-DS ########################################
####################################################


# TPC-DS on ClickHouse
bexhoma tpcds `
  -dbms ClickHouse              <# DBMS under test #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lc 16                        <# CPU limit for the SUT container #> `
  -rc 16                        <# CPU requested for the SUT container #> `
  -lr 64Gi                      <# RAM limit for the SUT container #> `
  -rr 64Gi                      <# RAM requested for the SUT container #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_clickhouse.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS ClickHouse  sf=3"


# TPC-DS on ClickHouseCluster with 3 shards
bexhoma tpcds `
  -dbms ClickHouseCluster       <# DBMS under test #> `
  -nw 3                         <# number of worker nodes (shards) #> `
  -sf 3                         <# scaling factor (controls database size in GB) #> `
  -nc 1                         <# number of repeated runs per configuration #> `
  -ne 1                         <# parallel client counts to sweep (comma-separated) #> `
  -nlp 8                        <# number of data loader pods #> `
  -xdt                          <# also measure data transfer volume per query #> `
  -m                            <# collect SUT resource metrics #> `
  -ma                           <# collect application-level metrics #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lc 16                        <# CPU limit for the SUT container and each worker #> `
  -rc 16                        <# CPU requested for the SUT container and each worker #> `
  -lr 64Gi                      <# RAM limit for the SUT container and each worker #> `
  -rr 64Gi                      <# RAM requested for the SUT container and each worker #> `
  -rsr                          <# delete any existing PVC for the SUT before starting #> `
  -rss 50Gi                     <# size of the persistent volume claims #> `
  -rst $BEXHOMA_STORAGE_CLASS   <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  -rnw $BEXHOMA_NODES_WORKER    <# schedule worker pods on these nodes (joined by '+') #> `
  -ks no                        <# remove the SUT at the end #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_tpcds_clickhouse_cluster.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] TPC-DS ClickHouseCluster  sf=3  nw=3"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
