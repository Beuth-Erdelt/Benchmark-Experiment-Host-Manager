#!/usr/bin/env python
"""
Validator for BenchbaseCollector (Collector-Benchbase.ipynb).
Checks: no exceptions, non-empty DataFrames, important columns present.
Shows head() for every DataFrame and prints a bottom-line summary.
"""
import traceback
import numpy as np
import pandas as pd
from bexhoma.benchmarks.benchbase.collector import BenchbaseCollector
from validate_collector_common import Validation

validation = Validation("benchbase")
codes, failures = validation.codes, validation.failures
sep, check_df = validation.sep, validation.check_df

# phase = configuration-experiment_run-client (3-part identifier)
# job   = phase-benchmark_run            (4-part identifier)
HEADER_COLS = ["phase", "job", "code", "configuration", "experiment_run",
               "benchmark_run", "client", "type_tenants", "num_tenants", "vol_tenants"]
TS_COLS     = ["timestamp", "phase", "job", "value", "code", "metric", "component"]
LOAD_COLS   = ["SF", "time_load", "time_ingest", "Throughput [SF/h]"]
PERF_COLS   = ["Goodput (requests/second)",
               "Latency Distribution.Average Latency (microseconds)"]


# ── SETUP ─────────────────────────────────────────────────────────────────────
collect = validation.create_collector(BenchbaseCollector, "BenchbaseCollector")

# ── CONNECTIONS ───────────────────────────────────────────────────────────────
sep("get_connections()")
try:
    df = collect.get_connections()
    check_df(df, "connections", HEADER_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_connections() exception")

# ── MONITORING AGGREGATED PER PHASE ───────────────────────────────────────────
sep("get_monitoring_aggregated_per_phase('benchmarking') + add_metadata")
try:
    df = collect.get_monitoring_aggregated_per_phase("benchmarking")
    df = collect.add_metadata(df)
    check_df(df, "monitoring_aggregated_per_phase", HEADER_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_monitoring_aggregated_per_phase() exception")

# ── MONITORING AGGREGATED PER JOB ─────────────────────────────────────────────
sep("get_monitoring_aggregated_per_job('benchmarking') + add_metadata")
try:
    df = collect.get_monitoring_aggregated_per_job("benchmarking")
    df = collect.add_metadata(df)
    check_df(df, "monitoring_aggregated_per_job", HEADER_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_monitoring_aggregated_per_job() exception")

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
    check_df(df_performance, "performance_aggregated_per_phase", ["phase"] + PERF_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_performance_aggregated_per_phase() exception")

# ── PERFORMANCE AGGREGATED PER JOB ────────────────────────────────────────────
sep("get_performance_aggregated_per_job()")
try:
    df_performance = collect.get_performance_aggregated_per_job()
    df_performance.dropna(inplace=True)
    check_df(df_performance, "performance_aggregated_per_job", ["phase", "job"] + PERF_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_performance_aggregated_per_job() exception")

# ── LOADING PER RUN ───────────────────────────────────────────────────────────
sep("get_loading_per_run()")
try:
    df = collect.get_loading_per_run()
    check_df(df, "loading_per_run", LOAD_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_loading_per_run() exception")

# ── LOADING PER CONNECTION ────────────────────────────────────────────────────
sep("get_loading_per_connection()")
try:
    df = collect.get_loading_per_connection()
    check_df(df, "loading_per_connection", LOAD_COLS)
except Exception:
    traceback.print_exc()
    failures.append("get_loading_per_connection() exception")

# ── MERGED PERFORMANCE + MONITORING (efficiency metrics) ──────────────────────
sep("Merged performance + monitoring with E_Tpx / E_Lat / E_RAM")
try:
    df_mon  = collect.get_monitoring_aggregated_per_phase(type="benchmarking")
    df_perf = collect.get_performance_aggregated_per_phase()
    merged_df = pd.merge(df_perf, df_mon, left_index=True, right_index=True, how="left")
    merged_df = merged_df[merged_df["client"] == 1]
    merged_df["E_Tpx"] = (merged_df["Goodput (requests/second)"]
                           / merged_df["CPU Utilization Time [s]"] * 600.)
    merged_df["E_Lat"] = 1. / np.sqrt(
        merged_df["Latency Distribution.Average Latency (microseconds)"]
        * merged_df["CPU Utilization Time [s]"] / 1e6)
    merged_df["E_RAM"] = (merged_df["Goodput (requests/second)"]
                          / merged_df["Memory Usage, Working Set [MiB]"])
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

# ── EVALUATOR: SUMMARY PER PHASE ──────────────────────────────────────────────
sep("evaluator.get_summary_benchmark_per_phase()")
try:
    ev = collect.get_evaluator(codes[0])
    df = ev.get_summary_benchmark_per_phase()
    check_df(df, "evaluator_summary_per_phase", ["phase"])
except Exception:
    traceback.print_exc()
    failures.append("evaluator.get_summary_benchmark_per_phase() exception")

# ── EVALUATOR: SUMMARY PER CONNECTION ─────────────────────────────────────────
sep("evaluator.get_summary_benchmark_per_connection()")
try:
    ev = collect.get_evaluator(codes[0])
    df = ev.get_summary_benchmark_per_connection()
    check_df(df, "evaluator_summary_per_connection", ["phase", "job"])
except Exception:
    traceback.print_exc()
    failures.append("evaluator.get_summary_benchmark_per_connection() exception")

# ── BOTTOM LINE ───────────────────────────────────────────────────────────────
validation.finish()
