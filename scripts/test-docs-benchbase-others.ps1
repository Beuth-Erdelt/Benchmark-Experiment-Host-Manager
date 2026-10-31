#Requires -Version 5.1
# Generates documentation summaries for Benchbase experiments on additional DBMS.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.

. .\scripts\testfunctions.ps1




####################################################
################# Benchbase Others #################
####################################################




#### Benchbase Twitter Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 16                        <# scaling factor (controls database size) #> `
  -xbt twitter                  <# Benchbase benchmark type #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 16                       <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_twitter_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase twitter simple  sf=16  nbp=1"


#### Benchbase Twitter Scale (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1600                      <# scaling factor (controls database size) #> `
  -xbt twitter                  <# Benchbase benchmark type #> `
  -xsd 20                       <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nbp 1,2,4,8                  <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 160                      <# threads per benchmarking pod #> `
  -m                            <# collect SUT resource metrics #> `
  -mc                           <# collect metrics for all cluster nodes #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 1600Gi                   <# size of the persistent volume claim #> `
  -rst nvme                     <# storage class for persistent volumes #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_twitter_scale.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase twitter scale  sf=1600  nbp=1,2,4,8"


#### Benchbase CH-benCHmark Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 10                        <# scaling factor (controls database size) #> `
  -xbt chbenchmark              <# Benchbase benchmark type #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 100                      <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 50Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_chbenchmark_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase chbenchmark simple  sf=10  nbp=1"


#### Benchbase CH-benCHmark Scale (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 100                       <# scaling factor (controls database size) #> `
  -xbt chbenchmark              <# Benchbase benchmark type #> `
  -xsd 20                       <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nbp 1,2,5,10                 <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 100                      <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -lr 128Gi                     <# RAM limit for the SUT container #> `
  -rr 128Gi                     <# RAM requested for the SUT container #> `
  -rss 100Gi                    <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_chbenchmark_scale.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase chbenchmark scale  sf=100  nbp=1,2,5,10"


#### Benchbase YCSB Workload C (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1000                      <# scaling factor (controls database size) #> `
  -xbt ycsb                     <# Benchbase benchmark type #> `
  -xwl c                        <# YCSB workload template (c = 100% read) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 1000Gi                   <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_ycsb_c.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase YCSB workload c  sf=1000  nbp=1,2"


#### Benchbase YCSB Workload A (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1000                      <# scaling factor (controls database size) #> `
  -xbt ycsb                     <# Benchbase benchmark type #> `
  -xwl a                        <# YCSB workload template (a = 50% read / 50% update) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 1000Gi                   <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_ycsb_a.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase YCSB workload a  sf=1000  nbp=1,2"


#### Benchbase YCSB Workload B (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1000                      <# scaling factor (controls database size) #> `
  -xbt ycsb                     <# Benchbase benchmark type #> `
  -xwl b                        <# YCSB workload template (b = 95% read / 5% update) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 1000Gi                   <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_ycsb_b.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase YCSB workload b  sf=1000  nbp=1,2"


#### Benchbase YCSB Workload D (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1000                      <# scaling factor (controls database size) #> `
  -xbt ycsb                     <# Benchbase benchmark type #> `
  -xwl d                        <# YCSB workload template (d = read latest) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 1000Gi                   <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_ycsb_d.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase YCSB workload d  sf=1000  nbp=1"


#### Benchbase YCSB Workload E (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1000                      <# scaling factor (controls database size) #> `
  -xbt ycsb                     <# Benchbase benchmark type #> `
  -xwl e                        <# YCSB workload template (e = scan) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 1000Gi                   <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_ycsb_e.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase YCSB workload e  sf=1000  nbp=1"


#### Benchbase YCSB Workload F (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1000                      <# scaling factor (controls database size) #> `
  -xbt ycsb                     <# Benchbase benchmark type #> `
  -xwl f                        <# YCSB workload template (f = read-modify-write) #> `
  -xsd 5                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 16                      <# throughput target as a multiple of the base ops/s #> `
  -nlt 64                       <# threads per loader pod #> `
  -nbp 1,2                      <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 32                       <# threads per benchmarking pod #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 1000Gi                   <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_ycsb_f.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase YCSB workload f  sf=1000  nbp=1,2"


#### Benchbase auctionmark Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xbt auctionmark              <# Benchbase benchmark type #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_auctionmark_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase auctionmark simple  sf=1  nbp=1"


#### Benchbase epinions Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xbt epinions                 <# Benchbase benchmark type #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_epinions_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase epinions simple  sf=1  nbp=1"


#### Benchbase hyadapt Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xbt hyadapt                  <# Benchbase benchmark type #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_hyadapt_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase hyadapt simple  sf=1  nbp=1"


#### Benchbase noop Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xbt noop                     <# Benchbase benchmark type #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_noop_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase noop simple  sf=1  nbp=1"


#### Benchbase otmetrics Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xbt otmetrics                <# Benchbase benchmark type #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_otmetrics_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase otmetrics simple  sf=1  nbp=1"


#### Benchbase resourcestresser Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xbt resourcestresser         <# Benchbase benchmark type #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_resourcestresser_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase resourcestresser simple  sf=1  nbp=1"


#### Benchbase seats Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xbt seats                    <# Benchbase benchmark type #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_seats_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase seats simple  sf=1  nbp=1"


#### Benchbase sibench Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xbt sibench                  <# Benchbase benchmark type #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_sibench_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase sibench simple  sf=1  nbp=1"


#### Benchbase smallbank Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xbt smallbank                <# Benchbase benchmark type #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_smallbank_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase smallbank simple  sf=1  nbp=1"


#### Benchbase tatp Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xbt tatp                     <# Benchbase benchmark type #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_tatp_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase tatp simple  sf=1  nbp=1"


#### Benchbase voter Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xbt voter                    <# Benchbase benchmark type #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_voter_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase voter simple  sf=1  nbp=1"


#### Benchbase wikipedia Simple (Example-Benchbase-Others.md)
bexhoma benchbase `
  -dbms PostgreSQL              <# DBMS under test #> `
  -sf 1                         <# scaling factor (controls database size) #> `
  -xbt wikipedia                <# Benchbase benchmark type #> `
  -xsd 2                        <# benchmark duration in minutes #> `
  -xtb 1024                     <# base ops/s used to compute the throughput target (2^10) #> `
  -xnbf 1                       <# throughput target as a multiple of the base ops/s #> `
  -nbp 1                        <# benchmarking pod counts to sweep (comma-separated) #> `
  -nbt 4                        <# threads per benchmarking pod #> `
  -ms $BEXHOMA_MS               <# max simultaneous DBMS configurations #> `
  -tr                           <# verify result meets basic sanity requirements #> `
  -rss 10Gi                     <# size of the persistent volume claim #> `
  -rnn $BEXHOMA_NODE_SUT        <# schedule SUT pod on this node #> `
  -rnl $BEXHOMA_NODE_LOAD       <# schedule loader pods on this node #> `
  -rnb $BEXHOMA_NODE_BENCHMARK  <# schedule benchmarker pods on this node #> `
  run 2>&1 | Out-File "$LOG_DIR\docs_benchbase_postgresql_wikipedia_simple.log" -Encoding utf8

Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') [DONE] Benchbase wikipedia simple  sf=1  nbp=1"


###########################################
############## Clean Folder ###############
###########################################


Invoke-CleanLogs
