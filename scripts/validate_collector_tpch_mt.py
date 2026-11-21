#!/usr/bin/env python
"""
Validator for DbmsBenchmarkerCollector multi-tenancy (Collector-TPC-H-MT.ipynb).
Checks: no exceptions, non-empty DataFrames, important columns present.
Shows head() for every DataFrame and prints a bottom-line summary.
"""
import traceback
import pandas as pd
from bexhoma.benchmarks.dbmsbenchmarker.collector import DbmsBenchmarkerCollector
from validate_collector_common import Validation

validation = Validation("tpch_mt")
codes, failures = validation.codes, validation.failures
sep, check_df = validation.sep, validation.check_df

HEADER_COLS = ["phase", "code", "configuration", "experiment_run",
               "benchmark_run", "client", "type_tenants", "num_tenants", "vol_tenants"]
TS_COLS     = ["timestamp", "phase", "value", "code", "metric", "component"]
TS_MT_COLS  = ["timestamp", "configuration", "value", "type_tenants"]
LOAD_COLS   = ["SF", "time_load", "time_ingest", "Throughput [SF/h]"]
PERF_COLS   = ["Power@Size [~Q/h]",
               "Throughput@Size", "num_of_queries"]


# ── SETUP ─────────────────────────────────────────────────────────────────────
collect = validation.create_collector(DbmsBenchmarkerCollector, "DbmsBenchmarkerCollector (TPC-H multi-tenancy)")

# ── CONNECTIONS ───────────────────────────────────────────────────────────────
sep("get_connections()")
try:
    df = collect.get_connections()
    check_df(df, "connections", HEADER_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_connections() exception")

# ── MONITORING AGGREGATED PER PHASE AND TENANCY ───────────────────────────────
sep("get_monitoring_aggregated_per_phase_multitenant('benchmarking') + add_metadata")
try:
    df = collect.get_monitoring_aggregated_per_phase_multitenant("benchmarking")
    df = collect.add_metadata(df)
    check_df(df, "monitoring_aggregated_multitenant", HEADER_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_monitoring_aggregated_per_phase_multitenant() exception")

# ── MONITORING AGGREGATED PER PHASE ───────────────────────────────────────────
sep("get_monitoring_aggregated_per_phase('benchmarking') + add_metadata")
try:
    df = collect.get_monitoring_aggregated_per_phase("benchmarking")
    df = collect.add_metadata(df)
    check_df(df, "monitoring_aggregated_benchmarking", HEADER_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_monitoring_aggregated_per_phase() exception")

# ── MONITORING TIMESERIES PER PHASE ───────────────────────────────────────────
sep("get_monitoring_timeseries_per_phase() + add_metadata")
try:
    df = collect.get_monitoring_timeseries_per_phase(
        codes[0], metric="total_cpu_memory", component="benchmarking")
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
    df_mon  = collect.get_monitoring_aggregated_per_phase_multitenant(type="benchmarking")
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
    for col in merged_df.columns:
        if merged_df[col].dtype == object:
            merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce').fillna(merged_df[col]).infer_objects(copy=False)
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
validation.finish()
