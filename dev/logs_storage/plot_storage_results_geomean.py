"""
Storage class sweep nvme vs cephcsi - same figure as plot_storage_results.py, but with geometric means.

The geometric mean treats a rate and its inverse consistently (geomean(1/x) = 1/geomean(x)),
so in a closed-loop benchmark (throughput = terminals / latency) the throughput factor and the
latency factor agree, and one outlier repetition no longer dominates the mean on a log axis.
The data and all drawing code come from plot_storage_results.py.

Usage:  python plot_storage_results_geomean.py [--out FILE.png] [--no-show]
"""
import statistics

import plot_storage_results as base

base.MEAN = statistics.geometric_mean
base.MEAN_LABEL = "geometric mean"
base.OUT_NAME = "storage_results_geomean.png"

if __name__ == "__main__":
    base.main()
