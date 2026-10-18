"""
Was the Ceph pool quiet while an experiment ran?

Prints, per benchmarking phase (connection), the mean of the ceph_others_* metrics:
I/O on the same pool from volumes that do not belong to this SUT. Quiet baseline on
cephcsi (k8svol): ~60 write ops/s, ~1.5 MiB/s, < 10 read ops/s. Phases clearly above
that were disturbed by another workload.

Usage:  python check_ceph_others.py CODE_OR_FOLDER [...]   (code -> C:/data/benchmarks/CODE)
"""
import glob
import os
import re
import sys

import pandas as pd

QUIET = {"read_ops_rate": 15.0, "write_ops_rate": 85.0, "write_rate": 5.0}

for arg in sys.argv[1:]:
    folder = arg if os.path.isdir(arg) else os.path.join("C:/data/benchmarks", arg)
    print("==", folder)
    rows = {}
    for f in sorted(glob.glob(os.path.join(folder, "query_benchmarker_metric_ceph_others_*.csv"))):
        m = re.match(r"query_benchmarker_metric_ceph_others_(.+)_([a-z]+-\d+-\d+-\d+-\d+)\.csv",
                     os.path.basename(f))
        if not m:
            continue
        metric, connection = m.groups()
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        if not df.empty:
            rows.setdefault(connection, {})[metric] = df.select_dtypes("number").sum(axis=1).mean()
    if not rows:
        print("   no ceph_others metrics found")
        continue
    table = pd.DataFrame(rows).T.sort_index()
    table["disturbed"] = [", ".join(k for k, limit in QUIET.items() if row.get(k, 0) > limit)
                          for _, row in table.iterrows()]
    with pd.option_context("display.width", 200, "display.max_columns", 10, "display.max_rows", 500,
                           "display.float_format", "{:,.1f}".format):
        print(table)
