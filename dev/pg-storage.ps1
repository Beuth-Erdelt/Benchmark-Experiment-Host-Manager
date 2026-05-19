
$LOG_DIR="./logs_tests"

$BEXHOMA_NODE_SUT = "cl-worker3"
$BEXHOMA_NODE_LOAD = "cl-worker19"
$BEXHOMA_NODE_BENCHMARK = "cl-worker19"
$BEXHOMA_DURATION = 15
$BEXHOMA_EXECUTIONS = "1"
$BEXHOMA_REPETITIONS = "3"


function clean_logs {
    if (-not $LOG_DIR) {
        Write-Output "ERROR: Environment variable LOG_DIR is not set."
        return
    }

    $logFiles = Get-ChildItem -Path $LOG_DIR -Filter "*.log"
    Write-Output "Found log files: $($logFiles.Count)"

    foreach ($file in $logFiles) {
        Write-Output "Processing file: $($file.FullName)"

        $filename = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
        $outputFile = Join-Path -Path $LOG_DIR -ChildPath "$filename`_summary.md"

        $content = Get-Content $file.FullName
        $startIndex = $content | Select-String -SimpleMatch "## Show Summary" | Select-Object -First 1

        if ($startIndex) {
            Write-Output "Match found at line: $($startIndex.LineNumber)"
            $summaryContent = $content[($startIndex.LineNumber - 1)..($content.Length - 1)]
            $summaryContent | Set-Content -Path $outputFile
            Write-Output "Summary written to: $outputFile"
        } else {
            Write-Output "No summary found in $($file.FullName)"
        }
    }
}


######################################################
######################## RAMDISK #####################
######################################################

kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-160

bexperiments stop

######################################################
########################### B1 #######################
######################################################
# B1 Default — Wie verhält sich PostgreSQL 18 out-of-the-box auf diesem Storage-Backend? Das ist die Baseline.

bexhoma benchbase run -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne $BEXHOMA_EXECUTIONS `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst ramdisk -rss 20Gi -rsr `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=8GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=sync `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_scale_factor=0.2 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_threshold=50 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_delay=2ms `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_limit=200 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_max_threshold=100000000 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].vacuum_buffer_usage_limit=256kB `
  *> "$LOG_DIR\_test_pg_b1_ramdisk.log"

bexperiments stop

######################################################
########################### B2 #######################
######################################################
# B2 Aggressiv — Was passiert wenn Autovacuum maximalen I/O-Druck macht? Zeigt den worst case für tpmC-Einbrüche — besonders auf Ceph wo Autovacuum direkt mit TPC-C um Netzwerk-I/O konkurriert.

bexhoma benchbase run -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne $BEXHOMA_EXECUTIONS `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst ramdisk -rss 20Gi -rsr `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=8GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=sync `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_scale_factor=0.05 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_threshold=50 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_delay=0 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_limit=800 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_max_threshold=500000 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].vacuum_buffer_usage_limit=256kB `
  *> "$LOG_DIR\_test_pg_b2_ramdisk.log"

bexperiments stop

######################################################
########################### B3 #######################
######################################################
# B3 Konservativ — Kann man durch Drosselung von Autovacuum die tpmC-Varianz reduzieren, ohne dass Dead Tuples unkontrolliert akkumulieren? Das ist die klassische DBA-Tuning-Empfehlung für langsame Storage.

bexhoma benchbase run -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne $BEXHOMA_EXECUTIONS `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst ramdisk -rss 20Gi -rsr `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=8GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=sync `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_scale_factor=0.2 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_threshold=50 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_delay=20ms `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_limit=200 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_max_threshold=100000000 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].vacuum_buffer_usage_limit=256kB `
  *> "$LOG_DIR\_test_pg_b3_ramdisk.log"

bexperiments stop

######################################################
########################### B4 #######################
######################################################
# B4 PG18 Neu - Hilft der neue autovacuum_vacuum_max_threshold Parameter dabei, Autovacuum-Bursts vorhersehbarer zu machen? Das ist der PostgreSQL-18-spezifische Beitrag des Papers.

bexhoma benchbase run -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne $BEXHOMA_EXECUTIONS `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst ramdisk -rss 20Gi -rsr `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=8GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=sync `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_scale_factor=0.2 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_threshold=50 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_delay=2ms `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_limit=200 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_max_threshold=100000 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].vacuum_buffer_usage_limit=2MB `
  *> "$LOG_DIR\_test_pg_b4_ramdisk.log"


######################################################
######################### SHARED #####################
######################################################

bexperiments stop
kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-160

######################################################
########################### B1 #######################
######################################################

bexhoma benchbase load -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne 1 `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst shared -rss 20Gi -rsr `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=1GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=4GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  *> "$LOG_DIR\_test_pg_b1_load_ceph.log"

bexperiments stop

bexhoma benchbase run -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne $BEXHOMA_EXECUTIONS `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst shared -rss 20Gi `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=8GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=sync `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_scale_factor=0.2 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_threshold=50 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_delay=2ms `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_limit=200 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_max_threshold=100000000 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].vacuum_buffer_usage_limit=256kB `
  *> "$LOG_DIR\_test_pg_b1_ceph.log"

bexperiments stop

######################################################
########################### B2 #######################
######################################################

bexhoma benchbase load -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne 1 `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst shared -rss 20Gi -rsr `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=1GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=4GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  *> "$LOG_DIR\_test_pg_b2_load_ceph.log"

bexperiments stop

bexhoma benchbase run -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne $BEXHOMA_EXECUTIONS `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst shared -rss 20Gi `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=8GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=sync `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_scale_factor=0.05 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_threshold=50 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_delay=0 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_limit=800 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_max_threshold=500000 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].vacuum_buffer_usage_limit=256kB `
  *> "$LOG_DIR\_test_pg_b2_ceph.log"

bexperiments stop

######################################################
########################### B3 #######################
######################################################

bexhoma benchbase load -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne 1 `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst shared -rss 20Gi -rsr `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=1GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=4GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  *> "$LOG_DIR\_test_pg_b3_load_ceph.log"

bexperiments stop

bexhoma benchbase run -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne $BEXHOMA_EXECUTIONS `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst shared -rss 20Gi `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=8GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=sync `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_scale_factor=0.2 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_threshold=50 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_delay=20ms `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_limit=200 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_max_threshold=100000000 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].vacuum_buffer_usage_limit=256kB `
  *> "$LOG_DIR\_test_pg_b3_ceph.log"

bexperiments stop

######################################################
########################### B4 #######################
######################################################

bexhoma benchbase load -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne 1 `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst shared -rss 20Gi -rsr `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=1GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=4GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  *> "$LOG_DIR\_test_pg_b4_load_ceph.log"

bexperiments stop

bexhoma benchbase run -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne $BEXHOMA_EXECUTIONS `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst shared -rss 20Gi `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=8GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=sync `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_scale_factor=0.2 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_threshold=50 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_delay=2ms `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_limit=200 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_max_threshold=100000 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].vacuum_buffer_usage_limit=2MB `
  *> "$LOG_DIR\_test_pg_b4_ceph.log"


######################################################
###################### LOCAL-HDD ####################
######################################################

bexperiments stop
kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-160

######################################################
########################### B1 #######################
######################################################

bexhoma benchbase load -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne 1 `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst local-hdd -rss 20Gi -rsr `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=1GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=4GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  *> "$LOG_DIR\_test_pg_b1_load_local.log"

bexperiments stop

bexhoma benchbase run -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne $BEXHOMA_EXECUTIONS `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst local-hdd -rss 20Gi `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=8GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=sync `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_scale_factor=0.2 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_threshold=50 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_delay=2ms `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_limit=200 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_max_threshold=100000000 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].vacuum_buffer_usage_limit=256kB `
  *> "$LOG_DIR\_test_pg_b1_local.log"

bexperiments stop

######################################################
########################### B2 #######################
######################################################

bexhoma benchbase load -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne 1 `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst local-hdd -rss 20Gi -rsr `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=1GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=4GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  *> "$LOG_DIR\_test_pg_b2_load_local.log"

bexperiments stop

bexhoma benchbase run -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne $BEXHOMA_EXECUTIONS `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst local-hdd -rss 20Gi `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=8GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=sync `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_scale_factor=0.05 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_threshold=50 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_delay=0 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_limit=800 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_max_threshold=500000 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].vacuum_buffer_usage_limit=256kB `
  *> "$LOG_DIR\_test_pg_b2_local.log"

bexperiments stop

######################################################
########################### B3 #######################
######################################################

bexhoma benchbase load -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne 1 `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst local-hdd -rss 20Gi -rsr `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=1GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=4GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  *> "$LOG_DIR\_test_pg_b3_load_local.log"

bexperiments stop

bexhoma benchbase run -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne $BEXHOMA_EXECUTIONS `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst local-hdd -rss 20Gi `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=8GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=sync `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_scale_factor=0.2 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_threshold=50 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_delay=20ms `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_limit=200 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_max_threshold=100000000 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].vacuum_buffer_usage_limit=256kB `
  *> "$LOG_DIR\_test_pg_b3_local.log"

bexperiments stop

######################################################
########################### B4 #######################
######################################################

bexhoma benchbase load -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne 1 `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst local-hdd -rss 20Gi -rsr `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=off `
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=1GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=4GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  *> "$LOG_DIR\_test_pg_b4_load_local.log"

bexperiments stop

bexhoma benchbase run -tr `
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK `
  -sf 160 `
  -sd $BEXHOMA_DURATION `
  -dbms PostgreSQL `
  -nlp 1 `
  -nbp 1 `
  -nbt 16 `
  -nbf 16 `
  -tb 1024 `
  -ne $BEXHOMA_EXECUTIONS `
  -nc $BEXHOMA_REPETITIONS `
  -rr 32Gi -lr 32Gi `
  -m -mc -ma `
  -rst local-hdd -rss 20Gi `
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_connections=256 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=8GB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].wal_buffers=64MB `
  --set deployment[bexhoma-deployment-postgres].container[dbms].fsync=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].synchronous_commit=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on `
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=sync `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_scale_factor=0.2 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_threshold=50 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_delay=2ms `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_cost_limit=200 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum_vacuum_max_threshold=100000 `
  --set deployment[bexhoma-deployment-postgres].container[dbms].vacuum_buffer_usage_limit=2MB `
  *> "$LOG_DIR\_test_pg_b4_local.log"
