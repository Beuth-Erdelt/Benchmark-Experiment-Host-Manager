"""
Tenancy sweep on nvme - N PostgreSQL containers on cl-worker36 run TPC-C at the same time.

Reads the summaries of tenancy_1/2/4/8.log in this folder (rerun 2026-10-18, experiments
1792289210, 1792293612, 1792298276, 1792304068; the first run of 2026-10-17 was
1792224763, 1792229322, 1792235214, 1792244800): per tenant 8 CPU / 16 GiB, its own 20 GiB nvme
volume (fresh per repetition), TPC-C SF16 loaded with 1 thread, then 16 terminals at
target 1024 (light) and 16384 (unthrottled), 5 minutes each, 3 repetitions.

Every tenant and repetition is one dot; the tick marks the mean. Boxed values compare
with a single tenant (N = 1).

Usage:  python plot_tenancy_results.py [--out FILE.png] [--no-show]
"""
import argparse
import os
import statistics

import matplotlib.pyplot as plt

from plot_storage_results import GRID, INK, INK_2, SURFACE, fmt_value, style_axes

COLOR = "#2a78d6"   # nvme, as in storage_results.png
HERE = os.path.dirname(os.path.abspath(__file__))
TENANTS = [1, 2, 4, 8]
LIGHT, FULL = 1024, 16384

# Disturbed repetitions (drawn hollow): {N: {experiment_run}}.
# Rerun 2026-10-18: no other experiment ran, nvme pool quiet during 1 tenant. (In the first run,
# tenancy_4 rep 1 overlapped fio_write_latency_overwrite_nvme on the same pool.)
DISTURBED = {}

TPUT = "Throughput (requests/second)"
P95 = "Latency Distribution.95th Percentile Latency (microseconds)"
AVG = "Latency Distribution.Average Latency (microseconds)"


# --- reading the summaries ------------------------------------------------------------

def read_table(lines, section, subsection):
    """Rows of the markdown table under '### section' / '#### subsection' as dicts."""
    start = lines.index(f"### {section}")
    start = next(i for i in range(start, len(lines)) if lines[i] == f"#### {subsection}")
    header_at = next(i for i in range(start, len(lines)) if lines[i].startswith("|"))
    header = [h.strip() for h in lines[header_at].strip("|").split("|")]
    rows = []
    for line in lines[header_at + 2:]:
        if not line.startswith("|"):
            break
        rows.append(dict(zip(header, (c.strip() for c in line.strip("|").split("|")))))
    return rows


def read_log(n):
    """{'bench': [(run, tenant, target, tput, avg_ms, p95_ms)], 'load': [(run, tenant, seconds)]}"""
    path = os.path.join(HERE, f"tenancy_{n}.log")
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    summary = lines.index("## Show Summary")
    lines = lines[summary:]
    bench = [(int(r["experiment_run"]), int(r["tenant_id"]), int(r["target"]), float(r[TPUT]),
              float(r[AVG]) / 1000, float(r[P95]) / 1000)
             for r in read_table(lines, "Benchmarking", "Per Phase")]
    load = [(int(r["experiment_run"]), int(r["tenant_id"]), float(r["time_load"]))
            for r in read_table(lines, "Loading", "Per Run")]
    return {"bench": bench, "load": load}


# --- drawing --------------------------------------------------------------------------

def mark(ax, x, values, hollow, label_side=1):
    """Dots (hollow = disturbed), a whisker min..max and a mean tick with its value."""
    mean = statistics.fmean(values)
    if len(values) > 1:
        ax.vlines(x, min(values), max(values), color=COLOR, linewidth=2, alpha=0.35, zorder=2)
    ax.hlines(mean, x - 0.16, x + 0.16, color=COLOR, linewidth=2.5, zorder=3)
    width = 0.24
    for i, (v, h) in enumerate(zip(values, hollow)):
        dx = (i / max(len(values) - 1, 1) - 0.5) * width if len(values) > 1 else 0
        ax.scatter([x + dx], [v], s=30, zorder=4, linewidth=1.3,
                   facecolor=SURFACE if h else COLOR, edgecolor=COLOR if h else SURFACE)
    ax.annotate(fmt_value(mean), (x + label_side * 0.2, mean), va="center",
                ha="left" if label_side > 0 else "right", fontsize=7.5, color=INK_2)
    return mean


def ratio_box(ax, x, text):
    ax.annotate(text, (x, 0.985), xycoords=("data", "axes fraction"), ha="center", va="top",
                fontsize=8.5, fontweight="semibold", color=INK,
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#f0efec", edgecolor="none"))


def finish(ax, ylim_from_zero=True, notes=None):
    ax.set_xticks(range(len(TENANTS)), [f"{n} tenant{'s' if n > 1 else ''}" for n in TENANTS],
                  fontsize=8, color=INK)
    ax.set_xlim(-0.6, len(TENANTS) - 0.4)
    for gi in range(1, len(TENANTS)):
        ax.axvline(gi - 0.5, color=INK_2, linestyle=(0, (4, 4)), linewidth=0.8, alpha=0.45, zorder=1)
    if ylim_from_zero:
        top = ax.get_ylim()[1]
        ax.set_ylim(0, top * 1.18)   # headroom for the boxes
    if notes:
        ax.text(0.0, -0.16, notes, transform=ax.transAxes, fontsize=7.5, color=INK_2, va="top")


def per_tenant_panel(ax, data, target, column, title, ylabel, notes=None):
    """One group per N: every tenant x repetition; box = mean relative to N = 1."""
    style_axes(ax, title, ylabel, log=False)
    base = None
    for gi, n in enumerate(TENANTS):
        rows = [r for r in data[n]["bench"] if r[2] == target]
        values = [r[column] for r in rows]
        hollow = [r[0] in DISTURBED.get(n, ()) for r in rows]
        mean = mark(ax, gi, values, hollow)
        if base is None:
            base = mean
        else:
            ratio_box(ax, gi, f"{mean / base:.2f}×")
    finish(ax, notes=notes)


def aggregate_panel(ax, data, notes=None):
    """Sum over tenants per repetition; dashed line = N x single tenant; box = scaling efficiency."""
    style_axes(ax, "Aggregate throughput, unthrottled", "requests / s (all tenants)", log=False)
    single = None
    for gi, n in enumerate(TENANTS):
        runs = sorted({r[0] for r in data[n]["bench"]})
        sums = [sum(r[3] for r in data[n]["bench"] if r[0] == run and r[2] == FULL) for run in runs]
        hollow = [run in DISTURBED.get(n, ()) for run in runs]
        # mean label left of the group, so it does not collide with the dashed reference
        mean = mark(ax, gi, sums, hollow, label_side=-1)
        if single is None:
            single = mean
        if n > 1:
            ax.hlines(n * single, gi - 0.38, gi + 0.38, color=INK_2, linestyle=(0, (2, 2)),
                      linewidth=1.2, zorder=1)
            ratio_box(ax, gi, f"{mean / (n * single):.0%}")
    ax.annotate("N × 1 tenant", (len(TENANTS) - 1 + 0.38, TENANTS[-1] * single), ha="right",
                va="top", xytext=(0, -3), textcoords="offset points", fontsize=7.5, color=INK_2)
    finish(ax, notes=notes)


def load_panel(ax, data, notes=None):
    style_axes(ax, "Loading time per tenant (all load at once)", "seconds", log=False)
    base = None
    for gi, n in enumerate(TENANTS):
        rows = data[n]["load"]
        values = [r[2] for r in rows]
        mean = mark(ax, gi, values, [r[0] in DISTURBED.get(n, ()) for r in rows])
        if base is None:
            base = mean
        else:
            ratio_box(ax, gi, f"{mean / base:.2f}×")
    finish(ax, notes=notes)


def print_table(data):
    print(f"{'N':>2s} {'target':>6s} {'tput/tenant':>12s} {'tput sum':>10s} {'avg ms':>7s} "
          f"{'p95 ms':>7s} {'load s':>7s}")
    for n in TENANTS:
        for target in (LIGHT, FULL):
            rows = [r for r in data[n]["bench"] if r[2] == target]
            runs = sorted({r[0] for r in rows})
            sums = [sum(r[3] for r in rows if r[0] == run) for run in runs]
            print(f"{n:2d} {target:6d} {statistics.fmean(r[3] for r in rows):12.1f} "
                  f"{statistics.fmean(sums):10.1f} {statistics.fmean(r[4] for r in rows):7.2f} "
                  f"{statistics.fmean(r[5] for r in rows):7.2f} "
                  f"{statistics.fmean(r[2] for r in data[n]['load']):7.1f}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--out", default=os.path.join(HERE, "tenancy_results.png"))
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    data = {n: read_log(n) for n in TENANTS}
    print_table(data)

    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, axes = plt.subplots(2, 4, figsize=(19, 10), facecolor=SURFACE,
                             gridspec_kw={"hspace": 0.5, "wspace": 0.3})

    aggregate_panel(axes[0, 0], data,
                    notes="Dashed = N times the single-tenant mean. Box = share of that reached.")
    per_tenant_panel(axes[0, 1], data, FULL, 3, "Throughput per tenant, unthrottled",
                     "requests / s", notes="Box = mean relative to 1 tenant.")
    per_tenant_panel(axes[0, 2], data, FULL, 4, "Average latency, unthrottled", "ms")
    per_tenant_panel(axes[0, 3], data, FULL, 5, "95th percentile latency, unthrottled", "ms")

    load_panel(axes[1, 0], data, notes="TPC-C SF16, 1 loader thread per tenant, fresh volume.")
    per_tenant_panel(axes[1, 1], data, LIGHT, 3, "Throughput per tenant, target 1024",
                     "requests / s", notes="Every tenant reaches its target.")
    per_tenant_panel(axes[1, 2], data, LIGHT, 4, "Average latency, target 1024", "ms")
    per_tenant_panel(axes[1, 3], data, LIGHT, 5, "95th percentile latency, target 1024", "ms")

    fig.suptitle("Tenancy on nvme - N PostgreSQL 18.3 containers on cl-worker36 run TPC-C at once",
                 x=0.05, y=0.985, ha="left", fontsize=14, color=INK, fontweight="semibold")
    fig.text(0.05, 0.955, va="top", fontsize=9, color=INK_2, ha="left", s=
             "Per tenant: 8 CPU / 16 GiB, own 20 GiB nvme volume (fresh per repetition), TPC-C SF16, "
             "16 terminals, 5 min per target, 3 repetitions. Dot = one tenant in one repetition "
             "(aggregate: one repetition), tick = mean.\n"
             "Rerun 2026-10-18, no other experiment running. "
             "Source: logs_storage/tenancy_{1,2,4,8}.log, experiments 1792289210 / 1792293612 / "
             "1792298276 / 1792304068.")
    fig.subplots_adjust(left=0.05, right=0.98, top=0.88, bottom=0.08)

    fig.savefig(args.out, dpi=130, facecolor=SURFACE)
    print(f"\nsaved {args.out}")
    if not args.no_show:
        plt.show()


if __name__ == "__main__":
    main()
