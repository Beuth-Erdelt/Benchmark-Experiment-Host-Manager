$PYTHON = "C:\Users\Patrick\anaconda3\envs\bexhoma\python.exe"
$DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

$tests = @(
    "test_collector_benchbase.py"
    "test_collector_benchbase_mt.py"
    "test_collector_hammerdb.py"
    "test_collector_tpch.py"
    "test_collector_tpch_mt.py"
    "test_collector_ycsb.py"
)

$failed = 0
$results = @()

Write-Host "============================================================"
Write-Host " Bexhoma Collector Functional Tests"
Write-Host "============================================================"

foreach ($t in $tests) {
    Write-Host ""
    Write-Host "[$t]"
    & $PYTHON "$DIR\$t"
    if ($LASTEXITCODE -ne 0) {
        $failed++
        $results += "FAIL: $t"
    } else {
        $results += "PASS: $t"
    }
}

Write-Host ""
Write-Host "============================================================"
Write-Host " Summary  ($failed failed / $($tests.Count) total)"
Write-Host "============================================================"
foreach ($r in $results) {
    Write-Host "  $r"
}
Write-Host "============================================================"

exit $failed
