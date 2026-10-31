"""February SIA error ranking for the SIPN South hindcast benchmark (2022-2026).

Reads ``data/sipn_south_feb_sia_ranking.csv`` and draws a 2 x 3 figure:

* five season panels of |February SIA error| against every external SIPN South
  submission of that season;
* a summary panel: the spread of all SIPN submissions per season, the two GlacioSeer
  products, the SIPN climatology and the rank of both products.

Verification products (NSIDC / OSI) are drawn in near-black in the season panels, and a
dotted line marks the largest error among them, i.e. the spread between observational
products.

Typography follows journal conventions: Arial throughout, one type scale
(title 12.5 / panel 9.5 / axis and ticks 7.0 / legend 7.4 pt), thin axes without top or
right spines, and no explanatory notes inside the figure.

Usage
-----
    python scripts/plot_sipn_south_ranking.py

Outputs go to ``figures/sipn_south/``.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "sipn_south_feb_sia_ranking.csv"
OUT = ROOT / "figures" / "sipn_south"
YEARS = (2022, 2023, 2024, 2025, 2026)

# palette: the two GlacioSeer products take the two warmest, most saturated hues; the
# SIPN groups sit in cooler tones, the submission spread in grey-green, and the two
# neutral classes recede to grey and near-black
RED = "#C1272D"
VIOLET = "#7D3C98"
BLUE = "#3A7CA5"
GREEN = "#4E9A62"
GREY = "#8A8A8A"
INK = "#151515"
SPREAD = "#A9C0B3"      # grey-green band: spread of all external submissions
SPREAD_DARK = "#6E8B7B"  # its median tick

COLOR = {"ours": RED, "ours_rollout": VIOLET, "d": BLUE, "s": GREEN, "b": GREY,
         "verification": INK}
LEGEND = [
    ("ours", "GlacioSeer-SIC"),
    ("ours_rollout", "GlacioSeer-SIC-Rollout"),
    ("d", "SIPN dynamical (d)"),
    ("s", "SIPN statistical (s)"),
    ("b", "Climatology / other"),
    ("spread", "SIPN submissions"),
    ("verification", "Verification product"),
]

mpl.rcParams.update({
    "font.family": "Arial",
    "font.size": 7.0,
    "mathtext.fontset": "custom",
    "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic",
    "mathtext.bf": "Arial:bold",
    "axes.linewidth": 0.6,
    "axes.edgecolor": "0.2",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.0,
    "xtick.major.size": 2.4,
    "xtick.major.pad": 2.0,
    "xtick.color": "0.3",
    "ytick.color": "0.3",
    "savefig.dpi": 300,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "pdf.fonttype": 42,
})

XLABEL = r"|February SIA error|  ($10^6$ km$^2$)"
TITLE = "SIPN South hindcast benchmark"

# composite geometry, in inches
W, H = 12.72, 9.75
X0 = 0.06           # left margin
LBL = 1.22          # gutter reserved for y tick labels
PW = 2.86           # panel plot width
CLEAR = 0.14        # clearance between a plot and the next column's labels
STEP = LBL + PW + CLEAR
COL_X = tuple(X0 + LBL + i * STEP for i in range(3))
PANEL_H = 3.75
TITLE_OFF = 0.34
LEGEND_OFF = 0.72
HEADER = 1.15
ROW_GAP = 0.58
BOTTOM_OFF = 0.50
BAR_IN = 0.102      # physical bar thickness, identical in every panel


def load() -> pd.DataFrame:
    df = pd.read_csv(CSV)
    for c in ("mean", "truth", "err", "abserr", "rank", "n_field", "n_submissions"):
        df[c] = pd.to_numeric(df[c])
    return df


def draw_panel(ax, rows: pd.DataFrame, year: int, *, bar_h: float = 0.70,
               xlabel: bool = True) -> None:
    rows = rows.sort_values("abserr", ascending=True).reset_index(drop=True)
    y = np.arange(len(rows))
    ax.barh(y, rows.abserr, color=[COLOR[g] for g in rows.group], height=bar_h, lw=0,
            zorder=2)

    ax.set_yticks(y)
    ax.set_yticklabels(rows.model, fontsize=7.0)
    ax.tick_params(axis="y", length=0, pad=4)
    for tick, group in zip(ax.get_yticklabels(), rows.group):
        if group in ("ours", "ours_rollout"):
            tick.set_color(COLOR[group])
            tick.set_fontweight("bold")
    ax.invert_yaxis()

    band = float(rows.loc[rows.group == "verification", "abserr"].max())
    ax.axvline(band, color="0.30", ls=(0, (1.4, 1.6)), lw=0.8, zorder=3)

    xmax = float(rows.abserr.max()) * 1.07
    ax.set_xlim(0, xmax)
    ax.tick_params(axis="x", labelsize=7.0)
    ax.grid(axis="x", lw=0.45, color="0.90", zorder=0)
    ax.set_axisbelow(True)

    for i, r in rows.iterrows():
        if r.group in ("ours", "ours_rollout"):
            ax.text(r.abserr + xmax * 0.024, i, f"{r.abserr:.3f}", va="center", ha="left",
                    fontsize=6.8, color=COLOR[r.group], fontweight="bold", zorder=4)

    ax.set_title(str(year), fontsize=9.5, fontweight="bold", loc="left", pad=5,
                 color="0.05")
    if xlabel:
        ax.set_xlabel(XLABEL, fontsize=7.0, color="0.25", labelpad=2.0)


def legend_handles(include_spread: bool = True) -> tuple[list, list[str]]:
    """Legend entries; the submission-spread swatch only exists in the summary panel."""
    entries = [e for e in LEGEND if include_spread or e[0] != "spread"]
    handles = []
    for key, _ in entries:
        if key == "spread":
            handles.append(Rectangle((0, 0), 1, 1, facecolor=SPREAD, alpha=0.32,
                                     edgecolor="none"))
        else:
            handles.append(Rectangle((0, 0), 1, 1, color=COLOR[key]))
    return handles, [lab for _, lab in entries]


def draw_individual(df: pd.DataFrame, year: int, out: Path) -> None:
    rows = df[df.target_year == year]
    height = 0.170 * len(rows) + 0.95
    fig, ax = plt.subplots(figsize=(4.7, height))
    draw_panel(ax, rows, year, bar_h=BAR_IN * len(rows) / (height * 0.80))

    handles, labels = legend_handles(include_spread=False)
    ax.legend(handles, labels, loc="upper right", frameon=False, fontsize=7.2,
              handlelength=1.25, handleheight=0.9, labelspacing=0.42,
              borderaxespad=0.4, handletextpad=0.55)
    fig.subplots_adjust(left=0.395, right=0.978, top=0.930, bottom=0.115)
    fig.savefig(out / f"feb_sia_ranking_{year}.png")
    fig.savefig(out / f"feb_sia_ranking_{year}.pdf")
    plt.close(fig)


def draw_summary_panel(ax, df: pd.DataFrame) -> None:
    """Per-season spread of all SIPN submissions, with the two products and climatology."""
    years = np.array(YEARS, dtype=float)
    ext = df[df.group.isin(("d", "s"))]

    lo, hi = [], []
    for year in YEARS:
        v = ext[ext.target_year == year].abserr.sort_values()
        lo.append(v.iloc[0])
        hi.append(v.iloc[-1])
    lo, hi = np.array(lo), np.array(hi)

    ax.bar(years, hi - lo, bottom=lo, width=0.54, color=SPREAD, alpha=0.32, lw=0, zorder=1)

    clim = [float(df[(df.target_year == y) & (df.model == "SIPN climatology")]
                  .abserr.iloc[0]) for y in YEARS]
    ax.plot(years, clim, ls=(0, (2.8, 2.0)), color=GREY, lw=0.9, marker="s", ms=3.8,
            mfc=GREY, mec="white", mew=0.6, zorder=3)

    for group, color, marker, filled, dx in (("ours", RED, "D", True, -0.17),
                                             ("ours_rollout", VIOLET, "o", False, 0.17)):
        vals = [float(df[(df.target_year == y) & (df.group == group)].abserr.iloc[0])
                for y in YEARS]
        ax.plot(years + dx, vals, color=color, lw=0.9, marker=marker, ms=4.2,
                mfc=color if filled else "white", mec=color, mew=0.9, zorder=4)

    ax.set_xlim(2021.45, 2026.55)
    ax.set_ylim(0, hi.max() * 1.06)
    ax.set_xticks(years)
    ax.set_xticklabels([str(int(y)) for y in years])
    ax.tick_params(axis="x", labelsize=7.0)
    ax.set_ylabel(XLABEL, fontsize=7.0, color="0.25")
    ax.yaxis.set_label_coords(-0.20, 0.5)
    ax.grid(axis="y", lw=0.45, color="0.90", zorder=0)
    ax.set_axisbelow(True)
    ax.set_title("summary", fontsize=9.5, fontweight="bold", loc="left", pad=5,
                 color="0.05")


# ---------------------------------------------------------------- key figure
# A single, README-first figure. It has to survive being shown at ~880 px wide on
# GitHub, so it carries one message only: where the two GlacioSeer products sit in the
# distribution of all external SIPN South submissions, season by season. Model names are
# deliberately omitted here and live in the full-ranking figure instead.
HERO_W, HERO_H = 7.10, 5.12
HERO_X0, HERO_X1 = 0.64, 6.10     # plot area; the rank column lives to its right
HERO_TOP, HERO_BOT = 1.20, 4.62
SCATTER = "#74887E"


def draw_hero(df: pd.DataFrame, out: Path) -> None:
    """One row per season: the whole field of submissions, our two products, climatology."""
    fig = plt.figure(figsize=(HERO_W, HERO_H))
    ax = fig.add_axes([HERO_X0 / HERO_W, (HERO_H - HERO_BOT) / HERO_H,
                       (HERO_X1 - HERO_X0) / HERO_W, (HERO_BOT - HERO_TOP) / HERO_H])
    rank_tr = mpl.transforms.blended_transform_factory(ax.transAxes, ax.transData)

    ext = df[df.group.isin(("d", "s"))]
    rng = np.random.default_rng(20260101)
    n_rows = len(YEARS)

    for i, year in enumerate(YEARS):
        yc = n_rows - 1 - i
        sub = ext[ext.target_year == year].abserr.to_numpy()
        lo, hi = float(sub.min()), float(sub.max())

        ax.hlines(yc, 0.0079, 4.30, color="0.905", lw=0.5, zorder=1)
        jit = rng.uniform(-0.215, 0.215, size=sub.size)
        ax.plot(sub, yc + jit, "o", ms=3.9, mfc=SCATTER, mec="none", alpha=0.52, zorder=3)

        clim = float(df[(df.target_year == year) & (df.model == "SIPN climatology")]
                     .abserr.iloc[0])
        ax.vlines(clim, yc - 0.33, yc + 0.33, color="0.42", ls=(0, (2.0, 1.8)),
                  lw=1.0, zorder=2)

        rows = {}
        for group, color, marker, filled, dy in (
                ("ours", RED, "D", True, 0.175),
                ("ours_rollout", VIOLET, "o", False, -0.205)):
            r = df[(df.target_year == year) & (df.group == group)].iloc[0]
            rows[group] = r
            ax.plot(r.abserr, yc + dy, marker=marker, ms=8.4,
                    mfc=color if filled else "white",
                    mec="white" if filled else color,
                    mew=1.1 if filled else 1.5, zorder=6)
            ax.text(1.028, yc + (0.178 if group == "ours" else -0.208),
                    f"{int(r['rank'])}/{int(r.n_field)}", transform=rank_tr,
                    fontsize=7.8, color=color, fontweight="bold", ha="left", va="center")

    ax.set_xscale("log")
    ax.set_xlim(0.0076, 4.35)
    ax.set_ylim(-0.46, n_rows - 0.26)
    ax.set_xticks([0.01, 0.1, 1.0, 3.0])
    ax.set_xticklabels(["0.01", "0.1", "1", "3"], fontsize=7.8)
    ax.xaxis.set_minor_locator(mpl.ticker.NullLocator())
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels([str(y) for y in reversed(YEARS)], fontsize=9.4)
    ax.tick_params(axis="y", length=0, pad=4)
    for t in ax.get_yticklabels():
        t.set_fontweight("bold")
        t.set_color("0.12")
    ax.grid(axis="x", lw=0.42, color="0.955", zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", pad=4)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_bounds(0.01, 4.35)
    ax.set_xlabel(XLABEL, fontsize=8.2, color="0.22", labelpad=6)

    ax.text(1.028, n_rows - 0.44, "rank", transform=rank_tr, fontsize=7.4,
            color="0.38", ha="left", va="bottom")

    fig.text(HERO_X0 / HERO_W, 1 - 0.38 / HERO_H, TITLE, fontsize=12.0,
             fontweight="bold", ha="left", va="center", color="0.05")

    handles, labels = hero_legend()
    fig.legend(handles, labels, loc="upper left",
               bbox_to_anchor=(HERO_X0 / HERO_W, 1 - 0.80 / HERO_H), ncol=4,
               frameon=False, fontsize=7.8, handlelength=1.25, handleheight=0.9,
               columnspacing=1.75, handletextpad=0.5, borderaxespad=0.0)

    fig.savefig(out / "sipn_south_benchmark.png")
    fig.savefig(out / "sipn_south_benchmark.pdf")
    plt.close(fig)


def hero_legend() -> tuple[list, list[str]]:
    handles = [
        plt.Line2D([], [], marker="D", ls="", ms=6.4, mfc=RED, mec="white", mew=1.0),
        plt.Line2D([], [], marker="o", ls="", ms=6.4, mfc="white", mec=VIOLET, mew=1.4),
        plt.Line2D([], [], marker="o", ls="", ms=3.0, mfc=SCATTER, mec="none", alpha=0.6),
        plt.Line2D([], [], color="0.42", ls=(0, (2.0, 1.8)), lw=1.0),
    ]
    return handles, ["GlacioSeer-SIC", "GlacioSeer-SIC-Rollout",
                     "SIPN South submission", "SIPN climatology"]


# ------------------------------------------------------------ ranking grid
# Four seasons in a 2 x 2 grid on one shared axis, so the bars are comparable across
# panels. The error distribution has a long tail -- the worst submission of 2025 is 3.86
# while the median entry is near 0.4 -- so the axis is cut at GCAP and the few bars that
# run past it are flagged with a wedge instead of being allowed to squash every other bar.
GRID = ((2023, 2024), (2025, 2026))
# The error distribution has a long tail: the median entry sits near 0.4 while the worst
# submission of 2025 reaches 3.86. A linear axis would squeeze every bar into the left
# fifth, so positions beyond KNEE are compressed by KDAMP and the tick labels say so.
KNEE, KDAMP, GMAX = 1.0, 0.25, 4.2


def gs(v):
    """Compress the axis beyond KNEE so the tail cannot dominate the panel."""
    v = np.asarray(v, dtype=float)
    return np.where(v <= KNEE, v, KNEE + (v - KNEE) * KDAMP)
GRID_W, GRID_H = 7.10, 6.94
G_LBL, G_PW = 1.12, 2.28
G_X = (1.17, 4.75)
G_R1, G_R2, G_PH = 0.62, 3.64, 2.60
G_BAR = 0.062      # physical bar thickness, identical in the four panels


def draw_ranking_panel(ax, rows: pd.DataFrame, year: int, panel_h: float,
                       xticks: bool) -> None:
    # Verification products are not forecast entries: sorting them together with the
    # submissions would put two black bars at the top and read as "two models beat us".
    fc = rows[rows.group != "verification"].sort_values("abserr", ascending=True)
    vr = rows[rows.group == "verification"].sort_values("abserr", ascending=True)
    rows = pd.concat([fc, vr]).reset_index(drop=True)
    y = np.arange(len(rows))
    vals = rows.abserr.to_numpy()
    height = G_BAR * len(rows) / panel_h
    if len(vr):
        ax.axhline(len(fc) - 0.5, color="0.86", lw=0.6, zorder=3)

    ax.barh(y, gs(vals), color=[COLOR[g] for g in rows.group], height=height, lw=0, zorder=2)

    ax.set_yticks(y)
    ax.set_yticklabels(rows.model, fontsize=6.5)
    ax.tick_params(axis="y", length=0, pad=3)
    for tick, group in zip(ax.get_yticklabels(), rows.group):
        if group in ("ours", "ours_rollout"):
            tick.set_color(COLOR[group])
            tick.set_fontweight("bold")
    ax.invert_yaxis()

    ax.set_xlim(0, gs(GMAX))
    ax.set_xticks([gs(t) for t in (0, 0.5, 1.0, 2.0, 3.0, 4.0)])
    ax.set_xticklabels(["0", "0.5", "1.0", "2", "3", "4"] if xticks else [])
    ax.tick_params(axis="x", labelsize=6.8, pad=2.5)
    band = float(rows.loc[rows.group == "verification", "abserr"].max())
    ax.axvline(band, color="0.05", ls=(0, (1.0, 1.7)), lw=0.9, zorder=3)

    ax.grid(axis="x", lw=0.42, color="0.93", zorder=0)
    ax.axvline(KNEE, color="0.58", ls=(0, (2.2, 2.0)), lw=0.75, zorder=1)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(0.7)
        ax.spines[side].set_color("0.15")

    for i, r in rows.iterrows():
        if r.group in ("ours", "ours_rollout"):
            ax.text(float(gs(r.abserr)) + gs(GMAX) * 0.022, i, f"{r.abserr:.3f}", va="center", ha="left",
                    fontsize=6.2, color=COLOR[r.group], fontweight="bold", zorder=5)

    ax.set_title(str(year), fontsize=9.0, fontweight="bold", loc="left", pad=4.0,
                 color="0.05")


def draw_ranking_grid(df: pd.DataFrame, out: Path) -> None:
    fig = plt.figure(figsize=(GRID_W, GRID_H))
    axes = {}
    for r, row in enumerate(GRID):
        top = G_R1 if r == 0 else G_R2
        bottom = GRID_H - top - G_PH
        for c, year in enumerate(row):
            ax = fig.add_axes([G_X[c] / GRID_W, bottom / GRID_H, G_PW / GRID_W, G_PH / GRID_H])
            draw_ranking_panel(ax, df[df.target_year == year], year, G_PH, xticks=(r == 1))
            axes[year] = ax

    left = (G_X[0] - G_LBL) / GRID_W
    fig.text(left, 1 - 0.26 / GRID_H, "SIPN South: full ranking, 2023–2026",
             fontsize=11.0, fontweight="bold", ha="left", va="center", color="0.05")

    # one legend for the whole grid, placed in the first panel's empty upper-right corner
    # (its top rows are all short bars) so it is found before the eye moves on
    handles, labels = grid_legend()
    axes[GRID[0][0]].legend(handles, labels, loc="upper right", frameon=False,
                            fontsize=6.3, handlelength=1.05, handleheight=0.88,
                            labelspacing=0.46, borderaxespad=0.55, handletextpad=0.45)

    fig.text(0.5, 1 - (GRID_H - 0.36) / GRID_H,
             XLABEL, fontsize=7.4, color="0.25", ha="center", va="center")

    fig.savefig(out / "feb_sia_ranking_2023_2026.png")
    fig.savefig(out / "feb_sia_ranking_2023_2026.pdf")
    plt.close(fig)


def grid_legend() -> tuple[list, list[str]]:
    keys = [("ours", "GlacioSeer-SIC"), ("ours_rollout", "GlacioSeer-SIC-Rollout"),
            ("d", "Dynamical"), ("s", "Statistical"), ("b", "Climatology"),
            ("verification", "Verification")]
    handles = [Rectangle((0, 0), 1, 1, color=COLOR[k]) for k, _ in keys]
    return handles, [lab for _, lab in keys]


def draw_composite(df: pd.DataFrame, out: Path) -> None:
    fig = plt.figure(figsize=(W, H))

    tops = []
    y = H - HEADER
    for _ in range(2):
        y -= PANEL_H
        tops.append(y)
        y -= ROW_GAP

    cells = {(0, 0): 2022, (0, 1): 2023, (0, 2): 2024,
             (1, 0): 2025, (1, 1): 2026}
    for (r, c), year in cells.items():
        rows = df[df.target_year == year]
        ax = fig.add_axes([COL_X[c] / W, tops[r] / H, PW / W, PANEL_H / H])
        draw_panel(ax, rows, year, bar_h=BAR_IN * len(rows) / PANEL_H)
    draw_summary_panel(
        fig.add_axes([COL_X[2] / W, tops[1] / H, PW / W, PANEL_H / H]), df)

    fig.text(COL_X[0] / W, 1 - TITLE_OFF / H, TITLE, fontsize=12.5, fontweight="bold",
             ha="left", va="center", color="0.05")

    handles, labels = legend_handles()
    fig.legend(handles, labels, loc="upper left",
               bbox_to_anchor=(COL_X[0] / W, 1 - LEGEND_OFF / H), ncol=7, frameon=False,
               fontsize=7.4, handlelength=1.0, handleheight=0.85, columnspacing=1.15,
               handletextpad=0.45, borderaxespad=0.0)

    fig.savefig(out / "feb_sia_ranking_2022_2026.png")
    fig.savefig(out / "feb_sia_ranking_2022_2026.pdf")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = load()
    for year in YEARS:
        draw_individual(df, year, OUT)
    draw_composite(df, OUT)
    draw_hero(df, OUT)
    draw_ranking_grid(df, OUT)

    for year in YEARS:
        rows = df[df.target_year == year]
        parts = []
        for name, group in (("GlacioSeer-SIC", "ours"),
                            ("GlacioSeer-SIC-Rollout", "ours_rollout")):
            r = rows[rows.group == group].iloc[0]
            parts.append(f"{name} {r['mean']:.3f} ({r.err:+.3f}) "
                         f"{int(r['rank'])}/{int(r.n_field)}")
        print(f"{year}  truth {rows.truth.iloc[0]:.3f} | " + " | ".join(parts), flush=True)
    print(f"[ok] figures in {OUT}", flush=True)


if __name__ == "__main__":
    main()
