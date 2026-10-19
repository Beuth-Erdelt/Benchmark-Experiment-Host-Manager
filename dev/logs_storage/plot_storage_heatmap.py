"""
Storage class sweep nvme vs cephcsi - the results of plot_storage_results.py as heatmaps.

Every cell is a factor: how much better nvme is than cephcsi (throughput nvme / cephcsi,
times and latencies cephcsi / nvme). Color = factor on a log scale, the same scale in both
figures. The data comes from plot_storage_results.py.

  storage_heatmap.png         every measurement: factor per repetition (run i vs run i),
                              and ratio of the means
  storage_heatmap_params.png  geometric-mean factor over the parameters of each benchmark
                              (terminals x target, jobs, file state, ...), with the absolute
                              geometric means of both classes in each cell
  storage_heatmap_values.png  absolute values per repetition and mean of both classes, one
                              color scale and unit per panel

Usage:  python plot_storage_heatmap.py [--outdir DIR] [--no-show]
"""
import argparse
import math
import os
import statistics

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.patches import Rectangle
from matplotlib.ticker import FixedLocator, FuncFormatter, LogLocator

import plot_storage_results as base

SURFACE, INK, INK_2, GRID = base.SURFACE, base.INK, base.INK_2, base.GRID
# sequential green ramp, light -> dark
RAMP = ["#d9f0d3", "#b2e0a6", "#82c874", "#4fab4a", "#2a8a33", "#136a24", "#074a17"]
CMAP = LinearSegmentedColormap.from_list("green_seq", RAMP)
NORM = LogNorm(vmin=1, vmax=100)
DARK = 0.62  # NORM above this (~17x): white text on the cell
GEOMEAN = statistics.geometric_mean


def factor(nvme, ceph, higher_is_better):
    return nvme / ceph if higher_is_better else ceph / nvme


def fmt_factor(f):
    return f"{base.fmt_factor(f)}×"


def cell(ax, x, y, f, text, sub=None, flagged=False, w=1.0, h=1.0, fontsize=8.5, norm=NORM,
         invert=False):
    """
    One cell at (x, y) (lower left), surface gap of 0.04 around it.
    invert: small values get the dark end of the ramp (lower is better).
    """
    gap = 0.04
    t = norm(min(max(f, norm.vmin), norm.vmax))
    if invert:
        t = 1 - t
    color = CMAP(t)
    ax.add_patch(Rectangle((x + gap, y + gap), w - 2 * gap, h - 2 * gap, facecolor=color,
                           edgecolor=SURFACE, linewidth=0, zorder=2))
    if flagged:  # disturbed repetition: dashed ring inside the cell
        ax.add_patch(Rectangle((x + 0.12, y + 0.12), w - 0.24, h - 0.24, facecolor="none",
                               edgecolor=SURFACE if t > DARK else INK,
                               linestyle=(0, (2, 2)), linewidth=1.1, zorder=3))
    ink = "#ffffff" if t > DARK else INK
    ink_2 = "#dcefd8" if t > DARK else INK_2
    if sub is None:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize,
                color=ink, fontweight="semibold", zorder=4)
    else:
        ax.text(x + w / 2, y + h * 0.62, text, ha="center", va="center", fontsize=fontsize,
                color=ink, fontweight="semibold", zorder=4)
        ax.text(x + w / 2, y + h * 0.30, sub, ha="center", va="center", fontsize=7,
                color=ink_2, zorder=4)


def bare(ax):
    ax.set_facecolor(SURFACE)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.tick_params(length=0, colors=INK_2, labelsize=8)


def colorbar(fig, rect):
    cax = fig.add_axes(rect)
    sm = plt.cm.ScalarMappable(norm=NORM, cmap=CMAP)
    cb = fig.colorbar(sm, cax=cax, orientation="horizontal")
    ticks = [1, 2, 5, 10, 20, 50, 100]
    cb.ax.xaxis.set_major_locator(FixedLocator(ticks))
    cb.ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}×"))
    cb.ax.xaxis.set_minor_locator(FixedLocator([]))
    cb.ax.tick_params(labelsize=8, colors=INK_2, length=0)
    cb.outline.set_visible(False)
    cb.ax.set_title("nvme advantage (log)", fontsize=8.5, color=INK_2, loc="left")


# --- data in one place ---------------------------------------------------------------

def sections():
    """[(panel title, {group: {class: [reps]}}, higher_is_better, flags)] in figure order"""
    by = base.by_group
    return [
        ("Loading time", base.LOAD_TIME_S, False, frozenset()),
        ("Ceph RBD write latency (load)", base.CEPH_WRITE_LAT_MS, False, frozenset()),
        ("TPC-H SF30 query time", base.TPCH_QUERY_S, False, base.TPCH_FLAGS),
        ("TPC-C throughput", by(base.TPCC_PHASES, base.TPCC_TPUT), True, base.TPCC_FLAGS),
        ("TPC-C average latency", by(base.TPCC_PHASES, base.TPCC_AVG_MS), False, base.TPCC_FLAGS),
        ("TPC-C p95 latency", by(base.TPCC_PHASES, base.TPCC_P95_MS), False, base.TPCC_FLAGS),
        ("YCSB C2 throughput", by(base.YCSB_PHASES, base.YCSB_TPUT), True, base.YCSB_FLAGS),
        ("YCSB C2 avg read latency", by(base.YCSB_PHASES, base.YCSB_AVG_MS), False, base.YCSB_FLAGS),
        ("YCSB C2 p99 read latency", by(base.YCSB_PHASES, base.YCSB_P99_MS), False, base.YCSB_FLAGS),
        ("fio 8k write + fdatasync", base.FIO_SYNC_WRITE_IOPS, True, base.FIO_SYNC_WRITE_FLAGS),
        ("fio 8k random read", base.FIO_RANDREAD_IOPS, True, frozenset()),
        ("fio sequential throughput", base.iops_to_mibs(base.FIO_SEQ), True, base.FIO_SEQ_FLAGS),
    ]


# --- figure 1: every measurement ------------------------------------------------------

def overview(path):
    secs = sections()
    columns = ["run 1", "run 2", "run 3", "mean"]
    col_x = [0, 1, 2, 3.25]  # gap before the aggregate
    rows = []  # (kind, payload)
    for title, groups, hib, flags in secs:
        rows.append(("header", title))
        for label, per in groups.items():
            rows.append(("data", (title, label, per, hib, flags)))
    n = len(rows)

    height = 0.36 * n + 3.2
    fig = plt.figure(figsize=(9.5, height), facecolor=SURFACE)
    top = 1 - 2.35 / height
    ax = fig.add_axes([0.30, 0.035, 0.66, top - 0.035])
    bare(ax)
    for ri, (kind, payload) in enumerate(rows):
        y = n - 1 - ri
        if kind == "header":
            ax.annotate(payload, (-0.05, y + 0.35), xycoords=("axes fraction", "data"),
                        ha="right", va="center", fontsize=9, color=INK, fontweight="semibold",
                        annotation_clip=False)
            ax.axhline(y + 0.98, color=GRID, linewidth=0.8, zorder=1)
            continue
        title, label, per, hib, flags = payload
        ax.annotate(label.replace("\n", " "), (-0.05, y + 0.5), xycoords=("axes fraction", "data"),
                    ha="right", va="center", fontsize=8, color=INK_2, annotation_clip=False)
        nv, ce = per["nvme"], per["cephcsi"]
        if len(nv) == len(ce):
            for i, (a, b) in enumerate(zip(nv, ce)):
                f = factor(a, b, hib)
                flagged = (label, "nvme", i) in flags or (label, "cephcsi", i) in flags
                cell(ax, col_x[i], y, f, fmt_factor(f), flagged=flagged)
        f = factor(statistics.fmean(nv), statistics.fmean(ce), hib)
        cell(ax, col_x[3], y, f, fmt_factor(f))
    for x, label in zip(col_x, columns):
        ax.text(x + 0.5, n + 0.15, label, ha="center", va="bottom", fontsize=8.5, color=INK)
    ax.set_xlim(0, col_x[-1] + 1)
    ax.set_ylim(0, n + 0.9)
    ax.set_xticks([])
    ax.set_yticks([])

    fig.text(0.03, 1 - 0.35 / height, "Storage classes nvme vs cephcsi - nvme advantage per measurement",
             fontsize=13, color=INK, fontweight="semibold", va="top")
    fig.text(0.03, 1 - 0.75 / height, va="top", fontsize=8.5, color=INK_2, s=
             "Factor = throughput nvme / cephcsi, or time / latency cephcsi / nvme. Run i = the same "
             "experiment run on both classes;\nempty = only one repetition. mean = ratio of "
             "the means over the repetitions.\nDashed ring = disturbed repetition "
             "(SUT restart or foreign I/O on the pool, see plot_storage_results.py).\n"
             "TPC-C / YCSB throughput at the lowest target: nvme is capped, the factor is a lower bound.")
    colorbar(fig, [0.03, 1 - 1.95 / height, 0.30, 0.012])
    fig.savefig(path, dpi=130, facecolor=SURFACE)
    print(f"saved {path}")
    return fig


# --- figure 2: over the parameters ------------------------------------------------------

def grid(ax, title, rows, cols, values, hib, unit, note=None):
    """
    values[r][c] = {class: [reps]}; cell = geomean factor + absolute geomeans.
    hib: higher_is_better, one bool or one per row.
    """
    bare(ax)
    ax.set_title(title, loc="left", fontsize=10.5, color=INK, fontweight="semibold", pad=22)
    nr, nc = len(rows), len(cols)
    hib_rows = hib if isinstance(hib, list) else [hib] * nr
    for r in range(nr):
        for c in range(nc):
            per = values[r][c]
            nv, ce = GEOMEAN(per["nvme"]), GEOMEAN(per["cephcsi"])
            f = factor(nv, ce, hib_rows[r])
            cell(ax, c, nr - 1 - r, f, fmt_factor(f), sub=f"{base.fmt_value(nv)} vs {base.fmt_value(ce)}",
                 fontsize=10)
    ax.set_xlim(0, nc)
    ax.set_ylim(0, nr)
    ax.set_xticks([c + 0.5 for c in range(nc)], cols, fontsize=8, color=INK)
    ax.xaxis.tick_top()
    ax.set_yticks([nr - 0.5 - r for r in range(nr)], rows, fontsize=8, color=INK)
    ax.set_aspect("equal")
    ax.text(0, -0.08, f"cell: factor; nvme vs cephcsi in {unit}" + (f"\n{note}" if note else ""),
            transform=ax.transAxes, fontsize=7.5, color=INK_2, va="top")


def params(path):
    tpcc = {"tput": base.TPCC_TPUT, "avg": base.TPCC_AVG_MS, "p95": base.TPCC_P95_MS}

    def tpcc_grid(metric):  # TPCC_PHASES order: 16/1024, 64/1024, 16/16384, 64/16384
        d = tpcc[metric]
        return [[{c: d[c][t * 2 + term] for c in base.CLASSES} for t in range(2)] for term in range(2)]

    ycsb = [[{c: d[c][i] for c in base.CLASSES} for i in range(3)]
            for d in (base.YCSB_TPUT, base.YCSB_AVG_MS, base.YCSB_P99_MS)]
    sync = base.FIO_SYNC_WRITE_IOPS
    seq = base.iops_to_mibs(base.FIO_SEQ)
    seq_keys = list(seq)
    tpch = [[{c: [base.TPCH_QUERY_S[q][c][i]] for c in base.CLASSES} for i in range(3)]
            for q in ("Q1", "Q6")]

    fig, axes = plt.subplots(2, 4, figsize=(17, 9.6), facecolor=SURFACE,
                             gridspec_kw={"hspace": 0.55, "wspace": 0.45})
    t_rows, t_cols = ["16 terminals", "64 terminals"], ["target\n1024", "target\n16384"]
    cap = "target 1024 caps nvme: factor is a lower bound"
    grid(axes[0, 0], "TPC-C throughput", t_rows, t_cols, tpcc_grid("tput"), True, "req/s", cap)
    grid(axes[0, 1], "TPC-C average latency", t_rows, t_cols, tpcc_grid("avg"), False, "ms")
    grid(axes[0, 2], "TPC-C p95 latency", t_rows, t_cols, tpcc_grid("p95"), False, "ms")
    grid(axes[0, 3], "YCSB C2 (16 terminals)", ["throughput\nops/s", "avg read\nlatency ms",
                                                 "p99 read\nlatency ms"],
         ["target\n4096", "target\n16384", "target\n65536"], ycsb, [True, False, False],
         "ops/s or ms", "target 4096 caps nvme; run 2 there disturbed")
    grid(axes[1, 0], "fio 8k write + fdatasync", ["fresh file", "prefilled"], ["1 job", "16 jobs"],
         [[sync["fresh file\n1 job"], sync["fresh file\n16 jobs"]],
          [sync["prefilled\n1 job"], sync["prefilled\n16 jobs"]]], True, "IOPS")
    grid(axes[1, 1], "fio 8k random read", ["QD1 per job"], ["1 job", "16 jobs", "64 jobs"],
         [[base.FIO_RANDREAD_IOPS[k] for k in ("1 job", "16 jobs", "64 jobs")]], True, "IOPS")
    grid(axes[1, 2], "fio sequential throughput", ["read 128k", "write 1M"],
         ["QD1\n1 job", "QD32 / QD16\n8 jobs"],
         [[seq[seq_keys[0]], seq[seq_keys[1]]], [seq[seq_keys[2]], seq[seq_keys[3]]]], True, "MiB/s")
    grid(axes[1, 3], "TPC-H SF30 query time", ["Q1", "Q6"], ["run 1\n(cold)", "run 2", "run 3"],
         tpch, False, "s", "run 3 Q6 nvme: SUT restart, one run failed")

    fig.suptitle("Storage classes nvme vs cephcsi - nvme advantage over the benchmark parameters",
                 x=0.04, y=0.985, ha="left", fontsize=14, color=INK, fontweight="semibold")
    fig.text(0.04, 0.945, va="top", fontsize=9, color=INK_2, s=
             "Factor = ratio of the geometric means over 3 repetitions (TPC-H: one repetition per cell): "
             "throughput nvme / cephcsi, time and latency cephcsi / nvme.\n"
             "Same color scale as storage_heatmap.png. Data: plot_storage_results.py.")
    colorbar(fig, [0.70, 0.955, 0.26, 0.012])
    fig.subplots_adjust(left=0.07, right=0.97, top=0.80, bottom=0.05)
    fig.savefig(path, dpi=130, facecolor=SURFACE)
    print(f"saved {path}")
    return fig


# --- figure 3: absolute values -----------------------------------------------------------

UNITS = {  # panel title -> unit of the values
    "Loading time": "s",
    "Ceph RBD write latency (load)": "ms per write op",
    "TPC-H SF30 query time": "s per run",
    "TPC-C throughput": "requests / s",
    "TPC-C average latency": "ms",
    "TPC-C p95 latency": "ms",
    "YCSB C2 throughput": "ops / s",
    "YCSB C2 avg read latency": "ms",
    "YCSB C2 p99 read latency": "ms",
    "fio 8k write + fdatasync": "IOPS",
    "fio 8k random read": "IOPS",
    "fio sequential throughput": "MiB / s",
}


def value_panel(ax, title, groups, hib, flags, height):
    """Rows = groups; columns = runs + mean per class. Own log color scale per panel."""
    bare(ax)
    reps = 3
    col_x = {cls: [k * (reps + 1.4) + i + (0.25 if i == reps else 0) for i in range(reps + 1)]
             for k, cls in enumerate(base.CLASSES)}
    values = [v for per in groups.values() for c in base.CLASSES for v in per[c]]
    norm = LogNorm(vmin=min(values), vmax=max(values))
    labels = list(groups)
    for ri, label in enumerate(labels):
        y = height - 1 - ri
        for cls in base.CLASSES:
            vs = groups[label][cls]
            for i, v in enumerate(vs):
                cell(ax, col_x[cls][i], y, v, base.fmt_value(v), flagged=(label, cls, i) in flags,
                     fontsize=7.5, norm=norm, invert=not hib)
            m = statistics.fmean(vs)
            cell(ax, col_x[cls][reps], y, m, base.fmt_value(m), fontsize=7.5, norm=norm,
                 invert=not hib)
        ax.annotate(label, (-0.15, y + 0.5), xycoords="data", ha="right", va="center",
                    fontsize=7.5, color=INK_2, annotation_clip=False)
    for cls in base.CLASSES:
        xs = col_x[cls]
        for x, name in zip(xs, ["run 1", "run 2", "run 3", "mean"]):
            ax.text(x + 0.5, height + 0.08, name, ha="center", va="bottom", fontsize=7.5, color=INK_2)
        ax.text((xs[0] + xs[-1] + 1) / 2, height + 0.55, cls, ha="center", va="bottom", fontsize=9,
                color=INK, fontweight="semibold")
    right = col_x[base.CLASSES[-1]][-1] + 1
    ax.set_xlim(0, right)
    ax.set_ylim(-1.6, height + 1.0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, loc="left", fontsize=10.5, color=INK, fontweight="semibold", pad=4)

    # legend: own scale and unit, directly below the last row of this panel
    y_cb = height - len(labels) - 0.75
    cax = ax.inset_axes([0, y_cb, right * 0.6, 0.22], transform=ax.transData)
    cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=CMAP if hib else CMAP.reversed()),
                      cax=cax, orientation="horizontal")
    if not hib:  # worse on the left, better (dark) on the right in every panel
        cax.invert_xaxis()
    decades = math.log10(norm.vmax / norm.vmin)
    subs = (1.0, 2.0, 5.0) if decades <= 2 else (1.0, 3.0) if decades <= 3 else (1.0,)
    cb.ax.xaxis.set_major_locator(LogLocator(base=10, subs=subs))
    cb.ax.xaxis.set_minor_locator(FixedLocator([]))
    cb.ax.xaxis.set_major_formatter(FuncFormatter(
        lambda v, _: f"{v / 1000:g}k" if v >= 1000 else f"{v:g}"))
    cb.ax.tick_params(labelsize=7, colors=INK_2, length=0)
    cb.outline.set_visible(False)
    better = "higher is better" if hib else "lower is better"
    ax.text(right * 0.62, y_cb + 0.11, f"{UNITS[title]} (log), {better} → dark", ha="left", va="center",
            fontsize=7.5, color=INK_2)


def values(path):
    secs = sections()
    heights = [max(len(g) for _, g, _, _ in secs[r * 3:r * 3 + 3]) for r in range(4)]
    fig, axes = plt.subplots(4, 3, figsize=(20, sum(h + 2.6 for h in heights) * 0.40 + 1.6),
                             facecolor=SURFACE,
                             gridspec_kw={"height_ratios": [h + 2.6 for h in heights],
                                          "hspace": 0.35, "wspace": 0.42})
    for i, (title, groups, hib, flags) in enumerate(secs):
        value_panel(axes[i // 3, i % 3], title, groups, hib, flags, heights[i // 3])
    fig.suptitle("Storage classes nvme vs cephcsi - absolute values",
                 x=0.06, y=0.99, ha="left", fontsize=14, color=INK, fontweight="semibold")
    fig.text(0.06, 0.972, va="top", fontsize=9, color=INK_2, s=
             "Dark = better in every panel (latency and time scales are reversed). Every panel has its "
             "own log color scale and unit, spanning the smallest to the largest value of that panel.\n"
             "mean = arithmetic mean over "
             "the repetitions; one repetition only: run 1 = mean.\nDashed ring = disturbed repetition "
             "(SUT restart or foreign I/O on the pool, see plot_storage_results.py). "
             "Data: plot_storage_results.py.")
    fig.subplots_adjust(left=0.08, right=0.98, top=0.905, bottom=0.02)
    fig.savefig(path, dpi=130, facecolor=SURFACE)
    print(f"saved {path}")
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--outdir", default=os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()
    plt.rcParams["font.family"] = "DejaVu Sans"
    overview(os.path.join(args.outdir, "storage_heatmap.png"))
    params(os.path.join(args.outdir, "storage_heatmap_params.png"))
    values(os.path.join(args.outdir, "storage_heatmap_values.png"))
    if not args.no_show:
        plt.show()


if __name__ == "__main__":
    main()
