#!/usr/bin/env python
"""
Validator for HardwareCollector / Hardware (fio, sysbench, sockperf, netperf).
Checks: no exceptions, non-empty DataFrames, important columns present.
Shows head() for every DataFrame and prints a bottom-line summary.

Each experiment runs one tool (-xht is not swept), so the combined tables hold
the columns of all four tools, and a row only has values in its own tool's
columns. The checks therefore go per tool: every tool has rows, its result
column has a value in each of them, and the other tools' result columns stay
empty there (NaN, not 0).
"""
import traceback
from bexhoma.benchmarks.hardware.collector import HardwareCollector
from validate_collector_common import Validation

validation = Validation("hardware")
codes, failures = validation.codes, validation.failures
sep, check_df = validation.sep, validation.check_df

# phase = configuration-experiment_run-client (3-part identifier)
# job   = phase-benchmark_run            (4-part identifier)
HEADER_COLS = ["phase", "job", "code", "configuration", "experiment_run",
               "benchmark_run", "client", "type_tenants", "num_tenants", "vol_tenants"]
TS_COLS     = ["timestamp", "phase", "job", "value", "code", "metric", "component"]
#: One result column per tool (HARDWARE_TYPE) that every round of it fills.
RESULT_COLS = {
    "fio":      "hardware_fio_write_iops",
    "sysbench": "hardware_sysbench_cpu_events_per_sec",
    "sockperf": "hardware_sockperf_msg_rate_per_sec",
    "netperf":  "hardware_netperf_transaction_rate",
}


def check_types(df, label: str) -> None:
    """Check the rows of every tool in a combined performance table."""
    if "hardware_type" not in df.columns:
        print(f"  FAIL  {label}: no column hardware_type")
        failures.append(f"{label}: no column hardware_type")
        return
    for hardware_type, column in RESULT_COLS.items():
        rows = df[df["hardware_type"] == hardware_type]
        if rows.empty:
            print(f"  FAIL  {label}: no rows of {hardware_type}")
            failures.append(f"{label}: no rows of {hardware_type}")
            continue
        if column not in rows.columns or rows[column].isna().any():
            print(f"  FAIL  {label}: {hardware_type} rows without {column}")
            failures.append(f"{label}: {hardware_type} rows without {column}")
            continue
        foreign = [other for other, other_column in RESULT_COLS.items()
                   if other != hardware_type and other_column in rows.columns
                   and rows[other_column].notna().any()]
        if foreign:
            print(f"  FAIL  {label}: {hardware_type} rows have values of {foreign}")
            failures.append(f"{label}: {hardware_type} rows have values of {foreign}")
            continue
        print(f"  OK    {label}: {len(rows)} row(s) of {hardware_type}")


# ── SETUP ─────────────────────────────────────────────────────────────────────
collect = validation.create_collector(HardwareCollector, "HardwareCollector (Hardware)")

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
    df = collect.get_performance_per_connection()
    if check_df(df, "performance_per_connection", ["client", "hardware_type"]):
        check_types(df, "performance_per_connection")
except Exception:
    traceback.print_exc()
    failures.append("get_performance_per_connection() exception")

# ── PERFORMANCE AGGREGATED PER PHASE ──────────────────────────────────────────
sep("get_performance_aggregated_per_phase()")
try:
    df = collect.get_performance_aggregated_per_phase()
    if check_df(df, "performance_aggregated_per_phase", ["phase", "code", "hardware_type"]):
        check_types(df, "performance_aggregated_per_phase")
except Exception:
    traceback.print_exc()
    failures.append("get_performance_aggregated_per_phase() exception")

# ── PERFORMANCE AGGREGATED PER JOB ────────────────────────────────────────────
sep("get_performance_aggregated_per_job()")
try:
    df = collect.get_performance_aggregated_per_job()
    if check_df(df, "performance_aggregated_per_job", ["phase", "job", "code", "hardware_type"]):
        check_types(df, "performance_aggregated_per_job")
except Exception:
    traceback.print_exc()
    failures.append("get_performance_aggregated_per_job() exception")

# ── SUMMARY ───────────────────────────────────────────────────────────────────
sep("get_summary()")
try:
    df = collect.get_summary()
    check_df(df, "summary", list(RESULT_COLS.values()))
except Exception:
    traceback.print_exc()
    failures.append("get_summary() exception")

# ── EVALUATOR: SUMMARIES OF EVERY EXPERIMENT ──────────────────────────────────
# one experiment per tool, and each tool has its own summary columns
for code in codes:
    sep(f"evaluator({code}).get_summary_benchmark_per_phase() / _per_connection()")
    try:
        ev = collect.get_evaluator(code)
        check_df(ev.get_summary_benchmark_per_phase(),
                 f"evaluator_summary_per_phase {code}")
        check_df(ev.get_summary_benchmark_per_connection(),
                 f"evaluator_summary_per_connection {code}")
    except Exception:
        traceback.print_exc()
        failures.append(f"evaluator({code}) summary exception")

# ── BOTTOM LINE ───────────────────────────────────────────────────────────────
validation.finish()
