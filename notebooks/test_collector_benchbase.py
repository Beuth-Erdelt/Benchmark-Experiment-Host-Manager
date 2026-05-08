"""
Functional test for collectors.benchbase (Collector-Benchbase.ipynb).
Checks: no exceptions, non-empty DataFrames, important columns present.
Shows head() for every DataFrame and prints a bottom-line summary.
"""
import sys
import traceback
import numpy as np
import pandas as pd
from bexhoma import collectors

pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", None)
pd.options.display.max_columns = None
pd.options.display.float_format = "{:.2f}".format

path = r"D:\data\benchmarks"
codes = ["1777812819", "1777815705"]

HEADER_COLS = ["phase", "code", "configuration", "experiment_run",
               "client", "type_tenants", "num_tenants", "vol_tenants"]
TS_COLS     = ["timestamp", "phase", "value", "code", "metric", "component"]
LOAD_COLS   = ["SF", "time_load", "time_ingest", "Throughput [SF/h]"]
PERF_COLS   = ["Goodput (requests/second)",
               "Latency Distribution.Average Latency (microseconds)"]

failures = []


def sep(title):
    print(f"\n{'='*60}\n{title}\n{'='*60}")


def check_df(df, label, required_cols=None):
    ok = True
    if df is None or len(df) == 0:
        print(f"  FAIL  {label}: DataFrame is empty")
        failures.append(f"{label}: empty")
        ok = False
    else:
        print(f"  OK    {label}: shape={df.shape}")
    if required_cols:
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            print(f"  FAIL  {label}: missing columns {missing}")
            failures.append(f"{label}: missing columns {missing}")
            ok = False
    if ok:
        # print(df.head())
        pass
    return ok


# ── SETUP ─────────────────────────────────────────────────────────────────────
sep("Setup: collectors.benchbase")
try:
    collect = collectors.benchbase(path, codes)
    print("  OK    collector created")
except Exception:
    traceback.print_exc()
    failures.append("collector creation failed")
    print(f"\n{'='*60}\nRESULT: FAIL (collector could not be created)\n{'='*60}")
    sys.exit(1)

# ── CONNECTIONS ───────────────────────────────────────────────────────────────
sep("get_connections()")
try:
    df = collect.get_connections()
    check_df(df, "connections", HEADER_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_connections() exception")

# ── MONITORING AGGREGATED PER PHASE ───────────────────────────────────────────
sep("get_monitoring_aggregated_per_phase('stream') + add_metadata")
try:
    df = collect.get_monitoring_aggregated_per_phase("stream")
    df = collect.add_metadata(df)
    check_df(df, "monitoring_aggregated_stream", HEADER_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_monitoring_aggregated_per_phase() exception")

# ── MONITORING TIMESERIES PER PHASE ───────────────────────────────────────────
sep("get_monitoring_timeseries_per_phase() + add_metadata")
try:
    df = collect.get_monitoring_timeseries_per_phase(
        codes[0], metric="total_cpu_memory", component="stream")
    df = collect.add_metadata(df)
    check_df(df, "monitoring_timeseries_per_phase", HEADER_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_monitoring_timeseries_per_phase() exception")

# ── MONITORING TIMESERIES ALL ──────────────────────────────────────────────────
sep("get_monitoring_timeseries_all()")
try:
    df = collect.get_monitoring_timeseries_all(metric="total_cpu_memory")
    check_df(df, "monitoring_timeseries_all", TS_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_monitoring_timeseries_all() exception")

# ── PERFORMANCE PER CONNECTION ─────────────────────────────────────────────────
sep("get_performance_per_connection()")
try:
    df_performance = collect.get_performance_per_connection()
    check_df(df_performance, "performance_per_connection", ["client"])
except Exception:
    traceback.print_exc()
    failures.append("get_performance_per_connection() exception")

# ── PERFORMANCE AGGREGATED PER PHASE ──────────────────────────────────────────
sep("get_performance_aggregated_per_phase()")
try:
    df_performance = collect.get_performance_aggregated_per_phase()
    df_performance.dropna(inplace=True)
    check_df(df_performance, "performance_aggregated_per_phase", PERF_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_performance_aggregated_per_phase() exception")

# ── LOADING PER RUN ───────────────────────────────────────────────────────────
sep("get_loading_per_run()")
try:
    df = collect.get_loading_per_run()
    check_df(df, "loading_per_run", LOAD_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_loading_per_run() exception")

# ── MERGED PERFORMANCE + MONITORING (efficiency metrics) ──────────────────────
sep("Merged performance + monitoring with E_Tpx / E_Lat / E_RAM")
try:
    df_mon  = collect.get_monitoring_aggregated_per_phase(type="stream")
    df_perf = collect.get_performance_aggregated_per_phase()
    merged_df = pd.merge(df_perf, df_mon, left_index=True, right_index=True, how="left")
    merged_df = merged_df[merged_df["client"] == 1]
    merged_df["E_Tpx"] = (merged_df["Goodput (requests/second)"]
                           / merged_df["CPU Utilization Time [s]"] * 600.)
    merged_df["E_Lat"] = 1. / np.sqrt(
        merged_df["Latency Distribution.Average Latency (microseconds)"]
        * merged_df["CPU Utilization Time [s]"] / 1e6)
    merged_df["E_RAM"] = (merged_df["Goodput (requests/second)"]
                          / merged_df["Memory Usage [MiB]"])
    df = collect.add_metadata(merged_df)
    check_df(df, "merged_perf_monitoring", HEADER_COLS + ["E_Tpx", "E_Lat", "E_RAM"])
except Exception:
    traceback.print_exc()
    failures.append("merged performance+monitoring exception")

# ── BENCHMARK TIMESERIES PER PHASE ────────────────────────────────────────────
sep("get_benchmark_timeseries_per_phase()")
try:
    df = collect.get_benchmark_timeseries_per_phase()
    check_df(df, "benchmark_timeseries_per_phase")
except Exception:
    traceback.print_exc()
    failures.append("get_benchmark_timeseries_per_phase() exception")

# ── BENCHMARK TIMESERIES ALL ──────────────────────────────────────────────────
sep("get_benchmark_timeseries_all()")
try:
    df = collect.get_benchmark_timeseries_all()
    check_df(df, "benchmark_timeseries_all")
except Exception:
    traceback.print_exc()
    failures.append("get_benchmark_timeseries_all() exception")

# ── BOTTOM LINE ───────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
if failures:
    print(f"RESULT: FAIL  ({len(failures)} issue(s))")
    for f in failures:
        print(f"  - {f}")
else:
    print("RESULT: ALL CHECKS PASSED")
print("=" * 60)
sys.exit(1 if failures else 0)
