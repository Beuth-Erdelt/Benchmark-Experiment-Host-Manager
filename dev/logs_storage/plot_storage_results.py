"""
Storage class sweep nvme vs cephcsi - results from logs_storage (2026-10-15/17).

All numbers are copied statically from the experiment summaries / result folders:
  write_throughput  1792091105  TPC-H SF30 load only, 8 pods, storage removed per repetition
  write_latency     1792099970  Benchbase TPC-C SF16, 16/64 terminals, targets 1024/16384
                    cephcsi from the rerun 1792262926 (tpcc_cephcsi_rerun.log, quiet pool)
  read_throughput   1792116019  TPC-H SF30 Q1+Q6, 3 runs per query, loading inherited after rep 1
  read_latency      1792123892  YCSB C2, 30M rows, loading inherited after rep 1
  fio_*  (nvme / cephcsi), raw volume, storage removed per repetition:
    write_latency_overwrite  1792232342 / 1792239127  8k write + fdatasync per write, QD1, 1/16 jobs,
                      fresh vs prefilled file (-xfow 0,1); replaces write_latency 1792162949 / 1792178408
    write_throughput  1792157398 / 1792257393  1M write, libaio, QD 1/4/16, 1/8 jobs (cephcsi: rerun)
    read_latency      1792169021 / 1792199302  8k randread, io_uring, QD1, 1/16/64 jobs
    read_throughput   1792165007 / 1792272971  128k read, io_uring, QD 1/32, 1/8 jobs (cephcsi: rerun)

Every repetition is one dot; the whisker spans min..max, the tick marks the mean.

Usage:  python plot_storage_results.py [--out FILE.png] [--no-show]
"""
import argparse
import os
import statistics

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter

# --- palette: categorical slots 1 and 2 (fixed order), ink and surface tokens ---
COLORS = {"nvme": "#2a78d6", "cephcsi": "#eb6834"}
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
CLASSES = ["nvme", "cephcsi"]

# --- central tendency; plot_storage_results_geomean.py swaps these --------------
MEAN = statistics.fmean
MEAN_LABEL = "mean"
OUT_NAME = "storage_results.png"

# --- data: per group, per storage class, one value per repetition ---------------
# None = not available (yet)

LOAD_TIME_S = {  # loading time [s]
    "TPC-H SF30\nload only (8 pods)": {"nvme": [251, 254, 265], "cephcsi": [1390, 1566, 1373]},
    "TPC-H SF30\n+ index + stats": {"nvme": [280], "cephcsi": [1883]},
    "TPC-C SF16\n(1 pod)": {"nvme": [102, 97, 95], "cephcsi": [654, 604, 593]},
    "YCSB 30M rows\n(8 pods)": {"nvme": [757], "cephcsi": [28108]},
}

CEPH_WRITE_LAT_MS = {  # Ceph RBD write latency of the SUT volume during TPC-H load [ms]
    "TPC-H SF30 load": {"nvme": [3.9, 3.7, 4.2], "cephcsi": [120.1, 126.1, 118.6]},
}

TPCH_QUERY_S = {  # mean execution time per query and repetition [s]
    "Q1": {"nvme": [47.60, 16.10, 15.83], "cephcsi": [316.17, 101.00, 100.86]},
    "Q6": {"nvme": [18.22, 12.80, 15.86], "cephcsi": [93.93, 107.16, 102.60]},
}
TPCH_FLAGS = {("Q6", "nvme", 2)}  # rep 3: SUT restart, one Q6 run failed

# Disturbed repetitions (drawn hollow): (group label, class, repetition index).
# "Foreign I/O" = ceph_others_* metrics of the phase show other volumes busy on the same pool
# (quiet baseline: ~60 write ops/s, ~1.5 MiB/s, <10 read ops/s).

TPCC_PHASES = ["16 term.\ntarget 1024", "64 term.\ntarget 1024",
               "16 term.\ntarget 16384", "64 term.\ntarget 16384"]
TPCC_TPUT = {  # requests/second
    "nvme": [[1023.99, 1023.99, 1023.98], [1023.99, 1023.99, 1023.99],
             [2930.96, 2582.07, 2705.83], [8140.03, 7987.85, 8479.41]],
    # rerun 1792262926; the first run (rep 1 at target 16384 had 47 / 23 MiB/s foreign writes)
    # gave [[386.44, 180.83, 345.21], [647.49, 476.29, 695.94], [142.43, 339.75, 375.48], [55.60, 545.56, 687.13]]
    "cephcsi": [[253.76, 239.39, 262.09], [479.47, 596.10, 543.33],
                [257.29, 261.81, 263.02], [567.57, 536.97, 571.55]],
}
TPCC_AVG_MS = {  # average latency [ms]
    "nvme": [[5.317, 5.189, 5.551], [5.964, 5.778, 5.088],
             [5.454, 6.192, 5.910], [7.856, 8.005, 7.539]],
    "cephcsi": [[63.015, 66.687, 60.654], [133.067, 106.857, 117.416],
                [62.054, 61.013, 60.641], [112.425, 118.757, 111.629]],
}
TPCC_P95_MS = {  # 95th percentile latency [ms]
    "nvme": [[12.125, 12.457, 12.797], [14.519, 13.786, 12.558],
             [14.711, 16.578, 14.881], [35.746, 35.417, 36.551]],
    "cephcsi": [[225.128, 238.660, 199.915], [541.860, 400.474, 448.684],
                [239.826, 197.610, 197.008], [444.305, 450.089, 433.846]],
}
TPCC_FLAGS = frozenset()   # rerun: pool quiet in all phases

YCSB_PHASES = ["target 4096", "target 16384", "target 65536"]
YCSB_TPUT = {  # ops/second
    "nvme": [[4094.43, 4094.80, 4094.21], [16363.76, 16363.22, 16360.54],
             [21880.24, 20853.03, 22699.24]],
    "cephcsi": [[949.23, 818.00, 904.21], [977.74, 975.63, 979.67],
                [977.49, 1066.61, 1021.57]],
}
YCSB_AVG_MS = {  # average READ latency [ms]
    "nvme": [[0.753, 0.803, 0.843], [0.684, 0.588, 0.644], [0.551, 0.673, 0.567]],
    "cephcsi": [[16.763, 19.442, 17.552], [16.234, 16.279, 16.223], [16.295, 14.905, 15.523]],
}
YCSB_P99_MS = {  # 99th percentile READ latency [ms]
    "nvme": [[1.709, 1.839, 1.890], [1.563, 1.402, 1.472], [1.371, 1.531, 1.426]],
    "cephcsi": [[145.663, 154.239, 139.775], [142.847, 144.767, 140.159],
                [143.103, 132.991, 137.471]],
}
# rep 2 at target 4096 (19:55-20:52) overlapped fio_write_throughput_cephcsi: 39.8 MiB/s foreign writes
YCSB_FLAGS = {(YCSB_PHASES[0], "cephcsi", 1)}

# --- fio on the raw volume (no DBMS) ------------------------------------------------
FIO_SYNC_WRITE_IOPS = {  # 8k sequential write, fdatasync after every write, QD1 (WAL-like)
    # fresh file: every fdatasync commits an ext4 journal entry (unwritten extents)
    "fresh file\n1 job": {"nvme": [387.79, 493.53, 391.78], "cephcsi": [12.96, 6.50, 8.80]},
    "fresh file\n16 jobs": {"nvme": [4298.30, 3962.20, 4424.88], "cephcsi": [100.51, 77.52, 87.99]},
    # prefilled file: like PostgreSQL's zero-filled, recycled WAL segments
    "prefilled\n1 job": {"nvme": [1506.02, 1557.12, 1512.42], "cephcsi": [22.14, 30.36, 35.15]},
    "prefilled\n16 jobs": {"nvme": [22344.59, 25382.11, 24475.30], "cephcsi": [643.42, 720.65, 659.24]},
}
FIO_RANDREAD_IOPS = {  # 8k random read, QD1 per job (index lookups)
    "1 job": {"nvme": [1676.46, 1707.69, 1496.49], "cephcsi": [44.36, 51.93, 49.61]},
    "16 jobs": {"nvme": [30498.75, 28834.74, 31349.76], "cephcsi": [799.77, 852.42, 813.19]},
    "64 jobs": {"nvme": [93138.85, 93412.82, 89581.07], "cephcsi": [2883.83, 3104.18, 3009.30]},
}
FIO_SEQ = {  # label: (block size [KiB], {class: IOPS per repetition}) -> plotted as MiB/s
    # cephcsi from the reruns 1792272971 (read) and 1792257393 (write), quiet pool
    "read 128k\nQD1, 1 job": (128, {"nvme": [1438.29, 1423.64, 1319.54],
                                    "cephcsi": [216.00, 164.26, 165.83]}),
    "read 128k\nQD32, 8 jobs": (128, {"nvme": [22345.99, 22322.45, 22341.43],
                                      "cephcsi": [4546.60, 5251.80, 4757.04]}),
    "write 1M\nQD1, 1 job": (1024, {"nvme": [458.76, 375.90, 380.31],
                                    "cephcsi": [10.45, 11.46, 14.60]}),
    "write 1M\nQD16, 8 jobs": (1024, {"nvme": [2801.29, 2801.36, 2800.03],
                                      "cephcsi": [572.82, 585.91, 587.75]}),
}
# The first fio cephcsi throughput runs were disturbed (writes next to YCSB on cephcsi, read rep 2
# next to a foreign writer); the reruns above ran on a quiet pool.
# write_latency_overwrite: cephcsi quiet throughout; nvme ran next to the tenancy runs on the
# nvme pool (34-3,475 foreign write ops/s, up to 194 MiB/s) in these rounds:
FIO_SYNC_WRITE_FLAGS = {("fresh file\n1 job", "nvme", 1), ("fresh file\n1 job", "nvme", 2),
                        ("fresh file\n16 jobs", "nvme", 0), ("fresh file\n16 jobs", "nvme", 2),
                        ("prefilled\n1 job", "nvme", 2),
                        ("prefilled\n16 jobs", "nvme", 1), ("prefilled\n16 jobs", "nvme", 2)}
FIO_SEQ_FLAGS = frozenset()


def iops_to_mibs(groups):
    """{label: (bs_kib, {class: [iops]})} -> {label: {class: [MiB/s]}}"""
    return {label: {c: [v * bs / 1024 for v in reps] for c, reps in per.items()}
            for label, (bs, per) in groups.items()}


def by_group(phases, per_class):
    """{class: [[reps] per phase]} -> {phase: {class: [reps]}}"""
    return {p: {c: (per_class[c][i] if per_class.get(c) else None) for c in CLASSES}
            for i, p in enumerate(phases)}


# --- drawing ---------------------------------------------------------------------

def fmt_value(v):
    if v >= 100:
        return f"{v:,.0f}"
    if v >= 10:
        return f"{v:.1f}"
    return f"{v:.2f}"


def style_axes(ax, title, ylabel, log):
    ax.set_facecolor(SURFACE)
    ax.set_title(title, loc="left", fontsize=10.5, color=INK, fontweight="semibold", pad=8)
    ax.set_ylabel(ylabel, fontsize=8.5, color=INK_2)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=8, length=0)
    ax.grid(axis="y", color=GRID, linewidth=0.8, which="major")
    ax.set_axisbelow(True)
    if log:
        ax.set_yscale("log")
        ax.yaxis.set_major_locator(LogLocator(base=10, subs=(1.0, 2.0, 5.0)))
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))


def fmt_factor(ratio):
    return f"{ratio:.0f}" if ratio >= 10 else f"{ratio:.1f}"


def speedup_label(ax, x, per, higher_is_better):
    """
    Ratio of means as nvme's advantage over cephcsi, centered above the group.
    Below it the min..max of the per-repetition ratios (repetition i of nvme vs
    repetition i of cephcsi, i.e. the same experiment_run).
    """
    if not (per.get("nvme") and per.get("cephcsi")):
        return

    def ratio(nvme, ceph):
        return nvme / ceph if higher_is_better else ceph / nvme

    mean_ratio = ratio(MEAN(per["nvme"]), MEAN(per["cephcsi"]))
    ax.annotate(f"{fmt_factor(mean_ratio)}×", (x, 0.985), xycoords=("data", "axes fraction"),
                ha="center", va="top", fontsize=8.5, fontweight="semibold", color=INK,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#f0efec", edgecolor="none"))
    if len(per["nvme"]) > 1 and len(per["nvme"]) == len(per["cephcsi"]):
        reps = [ratio(n, c) for n, c in zip(per["nvme"], per["cephcsi"])]
        ax.annotate(f"{fmt_factor(min(reps))}–{fmt_factor(max(reps))}", (x, 0.915),
                    xycoords=("data", "axes fraction"), ha="center", va="top",
                    fontsize=7.5, color=INK_2)


def dotplot(ax, groups, title, ylabel, log=False, flags=frozenset(), notes=None,
            higher_is_better=False):
    """groups: {label: {class: [reps] or None}}"""
    style_axes(ax, title, ylabel, log)
    offset = {"nvme": -0.17, "cephcsi": 0.17}
    labels = list(groups)
    for gi in range(1, len(labels)):
        ax.axvline(gi - 0.5, color=INK_2, linestyle=(0, (4, 4)), linewidth=0.8, alpha=0.45,
                   zorder=1)
    for gi, label in enumerate(labels):
        for cls in CLASSES:
            reps = groups[label].get(cls)
            x = gi + offset[cls]
            if not reps:
                ax.annotate("pending", (x, 0.5), xycoords=("data", "axes fraction"),
                            ha="center", va="center", rotation=90, fontsize=7.5,
                            color=INK_2, style="italic")
                continue
            color = COLORS[cls]
            mean = MEAN(reps)
            if len(reps) > 1:
                ax.vlines(x, min(reps), max(reps), color=color, linewidth=2, alpha=0.55, zorder=2)
            ax.hlines(mean, x - 0.11, x + 0.11, color=color, linewidth=2.5, zorder=3)
            for ri, v in enumerate(reps):
                hollow = (label, cls, ri) in flags
                ax.scatter([x], [v], s=42, zorder=4,
                           facecolor=SURFACE if hollow else color,
                           edgecolor=color if hollow else SURFACE,
                           linewidth=1.6)
            side = -1 if cls == "nvme" else 1
            ax.annotate(fmt_value(mean), (x + side * 0.13, mean),
                        ha="right" if side < 0 else "left", va="center",
                        fontsize=7.5, color=INK_2)
        speedup_label(ax, gi, groups[label], higher_is_better)
    ax.set_xticks(range(len(labels)), labels, fontsize=8, color=INK)
    if len(labels) == 1:
        ax.set_xlim(-1.2, 1.2)
    else:
        ax.set_xlim(-0.6, len(labels) - 0.4)
    if log:
        values = [v for per in groups.values() for reps in per.values() if reps for v in reps]
        ax.set_ylim(min(values) / 2, max(values) * 7)  # headroom for the speedup labels
    if notes:
        ax.text(0.0, -0.22, notes, transform=ax.transAxes, fontsize=7.5,
                color=INK_2, va="top")


def print_table(sections):
    print(f"{'panel':34s} {'group':26s} {'class':8s} {'n':>2s} {MEAN_LABEL[:10]:>10s} "
          f"{'min':>10s} {'max':>10s} {'CV %':>6s}")
    for name, groups in sections:
        for label, per in groups.items():
            for cls in CLASSES:
                reps = per.get(cls)
                if not reps:
                    print(f"{name:34s} {label.replace(chr(10), ' '):26s} {cls:8s}  - pending")
                    continue
                mean = MEAN(reps)
                cv = (statistics.stdev(reps) / statistics.fmean(reps) * 100) if len(reps) > 1 else float("nan")
                print(f"{name:34s} {label.replace(chr(10), ' '):26s} {cls:8s} {len(reps):2d} "
                      f"{mean:10.2f} {min(reps):10.2f} {max(reps):10.2f} {cv:6.1f}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                      OUT_NAME))
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    tpcc_tput = by_group(TPCC_PHASES, TPCC_TPUT)
    tpcc_avg = by_group(TPCC_PHASES, TPCC_AVG_MS)
    tpcc_p95 = by_group(TPCC_PHASES, TPCC_P95_MS)
    ycsb_tput = by_group(YCSB_PHASES, YCSB_TPUT)
    ycsb_avg = by_group(YCSB_PHASES, YCSB_AVG_MS)
    ycsb_p99 = by_group(YCSB_PHASES, YCSB_P99_MS)
    fio_seq = iops_to_mibs(FIO_SEQ)

    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, axes = plt.subplots(4, 3, figsize=(16, 19.5), facecolor=SURFACE,
                             gridspec_kw={"hspace": 0.62, "wspace": 0.28})

    dotplot(axes[0, 0], LOAD_TIME_S, "Loading time", "seconds (log)", log=True,
            notes="TPC-H/TPC-C: fresh volume per repetition. '+ index + stats' and YCSB: one load.\n"
                  "YCSB: ingest only; building the index adds 168 s (nvme) / 4,292 s (cephcsi).")
    dotplot(axes[0, 1], CEPH_WRITE_LAT_MS, "Ceph RBD write latency of SUT volume",
            "ms per Ceph write op, ~1.6 MiB each (log)", log=True,
            notes="OSD-side time per write op (incl. replication), mean over the loading phase.\n"
                  "~101 GiB written per load on both classes (tables + WAL), in ~66k ops.")
    dotplot(axes[0, 2], TPCH_QUERY_S, "TPC-H SF30 query time", "seconds per run (log)",
            log=True, flags=TPCH_FLAGS,
            notes="Rep 1 is cold (highest dot). Hollow: SUT restart, one Q6 run failed.")

    tpcc_note = "cephcsi: rerun 2026-10-17 on a quiet pool (first run had foreign writes)."
    dotplot(axes[1, 0], tpcc_tput, "TPC-C throughput", "requests / s (log)", log=True,
            higher_is_better=True, flags=TPCC_FLAGS,
            notes="Target 1024 caps nvme at 1024 req/s, so the factor there is a lower bound.\n"
                  + tpcc_note)
    dotplot(axes[1, 1], tpcc_avg, "TPC-C average latency", "ms (log)", log=True,
            flags=TPCC_FLAGS, notes=tpcc_note)
    dotplot(axes[1, 2], tpcc_p95, "TPC-C 95th percentile latency", "ms (log)", log=True,
            flags=TPCC_FLAGS, notes=tpcc_note)

    ycsb_note = "Hollow: rep 2 ran next to our own fio write test on cephcsi (40 MiB/s)."
    dotplot(axes[2, 0], ycsb_tput, "YCSB C2 throughput", "ops / s (log)", log=True,
            higher_is_better=True, flags=YCSB_FLAGS,
            notes="16 terminals. Target 4096 caps nvme at 4096 ops/s, so the factor there is a\n"
                  "lower bound; cephcsi stays near 1,000 ops/s at every target.\n" + ycsb_note)
    dotplot(axes[2, 1], ycsb_avg, "YCSB C2 average read latency", "ms (log)", log=True,
            flags=YCSB_FLAGS, notes=ycsb_note)
    dotplot(axes[2, 2], ycsb_p99, "YCSB C2 99th percentile read latency", "ms (log)", log=True,
            flags=YCSB_FLAGS, notes=ycsb_note)

    dotplot(axes[3, 0], FIO_SYNC_WRITE_IOPS, "fio 8k write + fdatasync (WAL-like)",
            "IOPS (log)", log=True, higher_is_better=True, flags=FIO_SYNC_WRITE_FLAGS,
            notes="Raw volume, no DBMS. QD1 per job, fdatasync after every write. Prefilled = like\n"
                  "PostgreSQL's recycled WAL. p99: nvme 1.1-4.3 ms, cephcsi 112-558 ms.\n"
                  "Hollow: tenancy runs wrote to the nvme pool at the same time.")
    dotplot(axes[3, 1], FIO_RANDREAD_IOPS, "fio 8k random read", "IOPS (log)", log=True,
            higher_is_better=True,
            notes="io_uring, QD1 per job, 2 GiB file. p99 latency: nvme 0.8-1.4 ms,\n"
                  "cephcsi 127-167 ms. Pool quiet in all rounds.")
    dotplot(axes[3, 2], fio_seq, "fio sequential throughput", "MiB / s (log)", log=True,
            higher_is_better=True, flags=FIO_SEQ_FLAGS,
            notes="Read: io_uring, 16 GiB file. Write: libaio. nvme saturates at ~2,800 MiB/s.\n"
                  "cephcsi: reruns 2026-10-17 on a quiet pool.")

    fig.suptitle("Storage classes nvme vs cephcsi - PostgreSQL 18.3 on cl-worker36, 8 CPU / 16 GiB",
                 x=0.07, y=0.988, ha="left", fontsize=14, color=INK, fontweight="semibold")
    fig.text(0.07, 0.976, va="top", s=
             f"3 repetitions each. Dot = one repetition, whisker = min..max, tick = {MEAN_LABEL} "
             f"(value printed beside it). Boxed n× = how much better nvme is (ratio of {MEAN_LABEL}s), "
             "below it the range over the repetitions (run i vs run i).\n"
             "Hollow dot = disturbed repetition (SUT restart, or other I/O on the same Ceph pool "
             "per the ceph_others_* metrics); still included in the mean.\n"
             "Source: logs_storage, experiments 1792091105 / 1792099970 (cephcsi: rerun 1792262926) / "
             "1792116019 / 1792123892; bottom row: fio_*.log (codes in the script header).",
             fontsize=9, color=INK_2, ha="left")
    handles = [Line2D([], [], marker="o", linestyle="", markersize=7,
                      markerfacecolor=COLORS[c], markeredgecolor=SURFACE, label=c)
               for c in CLASSES]
    fig.legend(handles=handles, loc="upper right", bbox_to_anchor=(0.97, 0.993), ncol=2,
               frameon=False, fontsize=10, labelcolor=INK)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.935, bottom=0.06)

    print_table([
        ("Loading time [s]", LOAD_TIME_S),
        ("Ceph write latency [ms]", CEPH_WRITE_LAT_MS),
        ("TPC-H query time [s]", TPCH_QUERY_S),
        ("TPC-C throughput [req/s]", tpcc_tput),
        ("TPC-C avg latency [ms]", tpcc_avg),
        ("TPC-C p95 latency [ms]", tpcc_p95),
        ("YCSB throughput [ops/s]", ycsb_tput),
        ("YCSB avg read latency [ms]", ycsb_avg),
        ("YCSB p99 read latency [ms]", ycsb_p99),
        ("fio 8k write+fdatasync [IOPS]", FIO_SYNC_WRITE_IOPS),
        ("fio 8k randread [IOPS]", FIO_RANDREAD_IOPS),
        ("fio sequential [MiB/s]", fio_seq),
    ])

    fig.savefig(args.out, dpi=130, facecolor=SURFACE)
    print(f"\nsaved {args.out}")
    if not args.no_show:
        plt.show()


if __name__ == "__main__":
    main()
