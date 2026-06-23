#!C:\Users\Patrick\anaconda3\envs\bexhoma\python.exe
"""
Validator for collectors.dbmsbenchmarker multi-tenancy (Collector-TPC-H-MT.ipynb).
Checks: no exceptions, non-empty DataFrames, important columns present.
Shows head() for every DataFrame and prints a bottom-line summary.
"""
import sys
import re
import os
import ast
import zipfile
import traceback
import pandas as pd
from bexhoma import collectors

pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", None)
pd.options.display.max_columns = None
pd.options.display.float_format = "{:.2f}".format

_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cluster.config")
with open(_CONFIG) as _cf:
    path = ast.literal_eval(_cf.read())["benchmarker"]["resultfolder"]

_LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs_tests")

def _code_from_log(filename):
    try:
        with open(os.path.join(_LOG_DIR, filename)) as _f:
            for _line in _f:
                _m = re.search(r"Experiment\s+: has code (\d+)", _line)
                if _m:
                    return _m.group(1)
    except FileNotFoundError:
        pass
    return None

codes = [c for c in [
    _code_from_log("doc_tpch_testcase_collector_tenants_schema.log"),
    _code_from_log("doc_tpch_testcase_collector_tenants_database.log"),
    _code_from_log("doc_tpch_testcase_collector_tenants_container.log"),
] if c is not None]
if not codes:
    print("ERROR: no experiment codes found in logs_tests/ — run test-docs-collector first.", file=sys.stderr)
    sys.exit(1)

_VALIDATIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dev", "validations")
os.makedirs(_VALIDATIONS_DIR, exist_ok=True)

for code in codes:
    code_folder = os.path.join(path, code)
    zip_file = os.path.join(_VALIDATIONS_DIR, f"{code}.zip")
    if os.path.isdir(code_folder) and not os.path.isfile(zip_file):
        print(f"Archiving result {code} -> dev/validations/{code}.zip")
        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zf:
            for _root, _dirs, _files in os.walk(code_folder):
                for _file in _files:
                    _fp = os.path.join(_root, _file)
                    zf.write(_fp, os.path.relpath(_fp, path))
    elif not os.path.isdir(code_folder) and os.path.isfile(zip_file):
        print(f"Extracting dev/validations/{code}.zip -> result {code}")
        with zipfile.ZipFile(zip_file, "r") as zf:
            zf.extractall(path)

HEADER_COLS = ["phase", "code", "configuration", "experiment_run",
               "benchmark_run", "client", "type_tenants", "num_tenants", "vol_tenants"]
TS_COLS     = ["timestamp", "phase", "value", "code", "metric", "component"]
TS_MT_COLS  = ["timestamp", "configuration", "value", "type_tenants"]
LOAD_COLS   = ["SF", "time_load", "time_ingest", "Throughput [SF/h]"]
PERF_COLS   = ["Power@Size [~Q/h]",
               "Throughput@Size", "num_of_queries"]

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
    if required_cols and df is not None:
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            print(f"  FAIL  {label}: missing columns {missing}")
            failures.append(f"{label}: missing columns {missing}")
            ok = False
    if ok:
        #print(df.head())
        pass
    return ok


# ── SETUP ─────────────────────────────────────────────────────────────────────
sep("Setup: collectors.dbmsbenchmarker (TPC-H multi-tenancy)")
try:
    collect = collectors.dbmsbenchmarker(path, codes)
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

# ── MONITORING AGGREGATED PER PHASE AND TENANCY ───────────────────────────────
sep("get_monitoring_aggregated_per_phase_multitenant('stream') + add_metadata")
try:
    df = collect.get_monitoring_aggregated_per_phase_multitenant("stream")
    df = collect.add_metadata(df)
    check_df(df, "monitoring_aggregated_multitenant", HEADER_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_monitoring_aggregated_per_phase_multitenant() exception")

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

# ── MONITORING TIMESERIES ALL MULTITENANT ─────────────────────────────────────
sep("get_monitoring_timeseries_all_multitenant()")
try:
    df = collect.get_monitoring_timeseries_all_multitenant(metric="total_cpu_memory")
    check_df(df, "monitoring_timeseries_all_multitenant", TS_MT_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_monitoring_timeseries_all_multitenant() exception")

# ── MONITORING TIMESERIES ALL (regular) ───────────────────────────────────────
sep("get_monitoring_timeseries_all()")
try:
    df = collect.get_monitoring_timeseries_all(metric="total_cpu_util")
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

# ── PERFORMANCE AGGREGATED PER PHASE MULTITENANT ──────────────────────────────
sep("get_performance_aggregated_per_phase_multitenant()")
try:
    df_perf_mt = collect.get_performance_aggregated_per_phase_multitenant()
    df_perf_mt.dropna(inplace=True)
    check_df(df_perf_mt, "performance_aggregated_multitenant",
             ["type_tenants", "num_tenants"])
except Exception:
    traceback.print_exc()
    failures.append("get_performance_aggregated_per_phase_multitenant() exception")

# ── LOADING PER RUN ───────────────────────────────────────────────────────────
sep("get_loading_per_run()")
try:
    df = collect.get_loading_per_run()
    check_df(df, "loading_per_run", LOAD_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_loading_per_run() exception")

# ── LOADING PER RUN MULTITENANT ───────────────────────────────────────────────
sep("get_loading_per_run_multitenant()")
try:
    df = collect.get_loading_per_run_multitenant()
    check_df(df, "loading_per_run_multitenant",
             ["SF", "time_load", "Throughput [SF/h]", "type_tenants", "num_tenants"])
except Exception:
    traceback.print_exc()
    failures.append("get_loading_per_run_multitenant() exception")

# ── MERGED PERFORMANCE + MONITORING ───────────────────────────────────────────
sep("Merged performance_multitenant + monitoring_multitenant")
try:
    df_mon  = collect.get_monitoring_aggregated_per_phase_multitenant(type="stream")
    df_perf = collect.get_performance_aggregated_per_phase_multitenant()
    join_keys = ['code', 'experiment_run', 'client', 'type_tenants', 'num_tenants']
    cols_to_use = [c for c in df_mon.columns if c not in df_perf.columns]
    df_perf_k = df_perf.copy()
    df_mon_k = df_mon[join_keys + cols_to_use].copy()
    for k in join_keys:
        if df_perf_k[k].dtype != df_mon_k[k].dtype:
            df_perf_k[k] = df_perf_k[k].astype(str)
            df_mon_k[k] = df_mon_k[k].astype(str)
    merged_df = df_perf_k.merge(df_mon_k, on=join_keys, how='inner')
    merged_df = collect.add_metadata(merged_df).copy()
    check_df(merged_df, "merged_perf_monitoring_mt", HEADER_COLS)
except Exception:
    traceback.print_exc()
    failures.append("merged performance+monitoring (MT) exception")

# ── WARNINGS PER CONNECTION ────────────────────────────────────────────────────
sep("get_total_warnings(query_titles=False)")
try:
    df = collect.get_total_warnings(query_titles=False)
    check_df(df, "total_warnings")
except Exception:
    traceback.print_exc()
    failures.append("get_total_warnings(query_titles=False) exception")

sep("get_total_warnings(query_titles=True)")
try:
    df = collect.get_total_warnings(query_titles=True)
    check_df(df, "total_warnings_titled")
except Exception:
    traceback.print_exc()
    failures.append("get_total_warnings(query_titles=True) exception")

# ── ERRORS PER CONNECTION ──────────────────────────────────────────────────────
sep("get_total_errors(query_titles=True)")
try:
    df = collect.get_total_errors(query_titles=True)
    check_df(df, "total_errors_titled")
except Exception:
    traceback.print_exc()
    failures.append("get_total_errors() exception")

# ── QUERY LATENCIES ────────────────────────────────────────────────────────────
sep("get_query_latencies(query_titles=True)")
try:
    df = collect.get_query_latencies(query_titles=True)
    check_df(df, "query_latencies")
except Exception:
    traceback.print_exc()
    failures.append("get_query_latencies() exception")

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
