"""Reusable Matplotlib style and export helpers for enggeo-figure."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt


PALETTE = {
    "blue": "#003F88",
    "mid_blue": "#0099E6",
    "pale_blue": "#D6E8FF",
    "yellow": "#F2C000",
    "orange": "#FF8000",
    "red": "#E60000",
    "green": "#008A00",
    "purple": "#9500B3",
    "charcoal": "#252525",
    "black": "#000000",
    "light_gray": "#D8D8D8",
}


# Per-call dictionaries: callers may override scientific mappings and visual roles.
MARKERS = ("o", "s", "^", "D", "v")
MARKER_SIZE_PT = {"ordinary": 4.5, "focal": 6.5}
MARKER_EDGE_WIDTH_PT = 0.6
MARKER_FILL_WHITE_FRACTION = 0.25


def marker_fill_color(color: str, white_fraction: float = MARKER_FILL_WHITE_FRACTION) -> str:
    """Opaque same-series tint; mix RGB with white rather than reducing alpha."""
    if not 0 <= white_fraction <= 1:
        raise ValueError("white_fraction must be between 0 and 1")
    rgb = mpl.colors.to_rgb(color)
    return mpl.colors.to_hex(tuple(v + (1 - v) * white_fraction for v in rgb))


def marker_style(
    color: str, *, kind: str = "plot", marker: str = "o",
    role: str = "ordinary", size_pt: float | None = None,
    hollow: bool = False, edgecolor: str | None = None,
    edgewidth_pt: float = MARKER_EDGE_WIDTH_PT,
    fill_white_fraction: float = MARKER_FILL_WHITE_FRACTION,
) -> dict:
    """Marker-only properties; scatter size is nominal pt squared, not diameter."""
    size = MARKER_SIZE_PT[role] if size_pt is None else size_pt
    if size <= 0 or edgewidth_pt < 0:
        raise ValueError("marker size must be positive and edge width non-negative")
    edge = PALETTE["black"] if edgecolor is None else edgecolor
    fill = "none" if hollow else marker_fill_color(color, fill_white_fraction)
    if kind == "plot":
        return {"marker": marker, "markersize": size, "markerfacecolor": fill,
                "markeredgecolor": edge, "markeredgewidth": edgewidth_pt}
    if kind == "scatter":
        return {"marker": marker, "s": size ** 2, "facecolors": fill,
                "edgecolors": edge, "linewidths": edgewidth_pt}
    raise ValueError("kind must be 'plot' or 'scatter'")


VISUAL_ROLES = {
    "raw": {"linewidth": 0.75, "alpha": 0.35, "zorder": 2},
    "trend": {"linewidth": 1.4, "alpha": 1.0, "zorder": 3},
    "uncertainty": {"alpha": 0.20, "linewidth": 0, "zorder": 1},
    "window": {"alpha": 0.15, "linewidth": 0, "zorder": 0},
    "reference": {"color": "#999999", "linewidth": 0.8, "linestyle": "--", "zorder": 1},
}


def visual_style(role: str, **overrides) -> dict:
    """Return an independent style dictionary for plot/fill_between/axvspan."""
    return {**VISUAL_ROLES[role], **overrides}


def mm_to_in(value_mm: float) -> float:
    return value_mm / 25.4


def apply_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans", "Arial", "sans-serif"],
            "font.size": 8,
            "text.color": "#000000",
            "axes.labelcolor": "#000000",
            "axes.titlecolor": "#000000",
            "xtick.labelcolor": "#000000",
            "ytick.labelcolor": "#000000",
            "legend.labelcolor": "#000000",
            "axes.prop_cycle": mpl.cycler(color=[PALETTE[k] for k in ["blue", "orange", "green", "purple", "red", "mid_blue"]]),
            "axes.labelsize": 8.5,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 7.5,
            "axes.linewidth": 0.75,
            "lines.linewidth": 1.4,
            "lines.markersize": MARKER_SIZE_PT["ordinary"],
            "lines.markeredgewidth": MARKER_EDGE_WIDTH_PT,
            "lines.markeredgecolor": "#000000",
            "scatter.marker": MARKERS[0],
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
            "xtick.major.size": 3.0,
            "ytick.major.size": 3.0,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "legend.frameon": False,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )


def default_dimensions_mm(rows: int, cols: int, complex_layout: bool = False) -> tuple[float, float]:
    """Fallback reference dimensions, not mandatory or minimum figure widths.

    Choose content-appropriate width_mm/height_mm in create_layout when narrower
    proportions work better; keep final-size typography and marker sizes intact.
    """
    if rows < 1 or cols < 1:
        raise ValueError("rows and cols must be positive integers")
    if cols >= 2:
        width_mm = 180.0
    elif rows >= 2 and complex_layout:
        width_mm = 180.0
    else:
        width_mm = 89.0

    if rows == 1:
        height_mm = 70.0 if cols == 1 else 72.0
    elif complex_layout:
        height_mm = 60.0 * rows + 6.0 * (rows - 1)
    else:
        height_mm = 50.0 * rows + 6.0 * (rows - 1)
    return width_mm, height_mm


def create_layout(
    rows: int,
    cols: int,
    *,
    complex_layout: bool = False,
    width_mm: float | None = None,
    height_mm: float | None = None,
    sharex: bool = False,
    sharey: bool = False,
) -> tuple[mpl.figure.Figure, list[mpl.axes.Axes]]:
    apply_style()
    default_width, default_height = default_dimensions_mm(rows, cols, complex_layout)
    width_mm = default_width if width_mm is None else width_mm
    height_mm = default_height if height_mm is None else height_mm
    fig, axes_array = plt.subplots(
        rows,
        cols,
        figsize=(mm_to_in(width_mm), mm_to_in(height_mm)),
        squeeze=False,
        sharex=sharex,
        sharey=sharey,
    )
    return fig, list(axes_array.ravel())


def compact_layout(
    fig: mpl.figure.Figure, *, clearance_mm: float = 2.5,
    outer_pad_mm: float = 2.5, rect=None,
) -> None:
    """Initial spacing for regular grids after labels are added; visually verify.

    Padding is measured between decorated subplot bounds, not spines.
    Manual axes and figure-level legends need explicit arrangement. This does
    not resize the canvas: reduce excess height separately and rerun layout.
    """
    if clearance_mm <= 0 or outer_pad_mm < 0:
        raise ValueError("clearance must be positive and outer padding non-negative")
    fig.canvas.draw()
    fontsize = float(mpl.rcParams["font.size"])
    factor = 72 / 25.4 / fontsize
    fig.tight_layout(pad=outer_pad_mm * factor,
                     h_pad=clearance_mm * factor,
                     w_pad=clearance_mm * factor, rect=rect)
    fig.canvas.draw()


def style_boxed_axes(ax: mpl.axes.Axes) -> None:
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.75)
        spine.set_color(PALETTE["charcoal"])
    ax.tick_params(which='both', direction='out', colors=PALETTE["charcoal"], labelcolor=PALETTE["black"], pad=3)
    ax.xaxis.label.set_color(PALETTE["black"])
    ax.yaxis.label.set_color(PALETTE["black"])
    ax.grid(False)


def add_panel_labels(axes: Sequence[mpl.axes.Axes], labels: Sequence[str] | None = None) -> None:
    if labels is None:
        labels = [chr(ord("a") + index) for index in range(len(axes))]
    if len(labels) != len(axes):
        raise ValueError("labels must match the number of axes")
    for ax, label in zip(axes, labels):
        offset = mpl.transforms.ScaledTranslation(-9 / 72, 3 / 72, ax.figure.dpi_scale_trans)
        ax.text(
            0,
            1,
            label,
            transform=ax.transAxes + offset,
            ha="left",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            color="black",
        )


def set_y_axis_color(ax: mpl.axes.Axes, color: str, side: str) -> None:
    if side not in {"left", "right"}:
        raise ValueError("side must be 'left' or 'right'")
    ax.yaxis.label.set_color(color)
    ax.tick_params(axis='y', which='both', direction='out', colors=color)
    ax.spines[side].set_color(color)
    ax.spines[side].set_linewidth(0.9)


def add_right_axis(
    ax: mpl.axes.Axes,
    *,
    color: str,
    outward_pt: float = 0.0,
) -> mpl.axes.Axes:
    twin = ax.twinx()
    if outward_pt:
        twin.spines["right"].set_position(("outward", outward_pt))
    twin.patch.set_visible(False)
    twin.spines["top"].set_visible(False)
    twin.spines["bottom"].set_visible(False)
    twin.spines["left"].set_visible(False)
    set_y_axis_color(twin, color, "right")
    return twin


def _bbox_points(fig: mpl.figure.Figure, ax: mpl.axes.Axes) -> list[float]:
    width_in, height_in = fig.get_size_inches()
    box = ax.get_position()
    return [
        box.x0 * width_in * 72,
        box.y0 * height_in * 72,
        box.x1 * width_in * 72,
        box.y1 * height_in * 72,
    ]


def audit_panel_alignment(
    fig: mpl.figure.Figure,
    axes: Sequence[mpl.axes.Axes],
    *,
    rows: int = 1,
    cols: int = 1,
    groups: Sequence[dict] | None = None,
    tolerance_pt: float = 1.5,
    json_out: str | Path | None = None,
) -> dict:
    if groups is None and len(axes) != rows * cols:
        raise ValueError("primary axes count must equal rows * cols")
    fig.canvas.draw()
    boxes = [_bbox_points(fig, ax) for ax in axes]
    failures: list[dict] = []

    def compare(check: str, panel_a: int, panel_b: int, value_a: float, value_b: float) -> None:
        delta = abs(value_a - value_b)
        if delta > tolerance_pt:
            failures.append(
                {
                    "check": check,
                    "panels": [panel_a, panel_b],
                    "delta_pt": round(delta, 4),
                }
            )

    if groups is not None:
        # Each group: {"panels": [0, 1], "checks": ["left", "right"]}.
        # Other supported checks: top, bottom, width, height.
        if len(axes) > 1 and not groups:
            raise ValueError("mixed layouts require explicit alignment groups")
        extract = {
            "left": lambda b: b[0], "bottom": lambda b: b[1],
            "right": lambda b: b[2], "top": lambda b: b[3],
            "width": lambda b: b[2]-b[0], "height": lambda b: b[3]-b[1],
        }
        for group in groups:
            indices = list(group["panels"])
            checks = list(group["checks"])
            if len(set(indices)) < 2 or len(set(indices)) != len(indices) or not checks:
                raise ValueError("each group needs distinct panels and explicit checks")
            if any(i < 0 or i >= len(axes) for i in indices):
                raise ValueError("alignment group panel index out of range")
            if any(check not in extract for check in checks):
                raise ValueError("unknown alignment check")
            ref = indices[0]
            for index in indices[1:]:
                for check in checks:
                    compare(check, ref, index, extract[check](boxes[ref]), extract[check](boxes[index]))
    else:
        for row in range(rows):
            indices = [row * cols + col for col in range(cols)]
            reference = indices[0]
            ref = boxes[reference]
            for index in indices[1:]:
                box = boxes[index]
                compare("row-bottom", reference, index, ref[1], box[1])
                compare("row-top", reference, index, ref[3], box[3])
                compare("row-height", reference, index, ref[3] - ref[1], box[3] - box[1])
                compare("panel-width", reference, index, ref[2] - ref[0], box[2] - box[0])

        for col in range(cols):
            indices = [row * cols + col for row in range(rows)]
            reference = indices[0]
            ref = boxes[reference]
            for index in indices[1:]:
                box = boxes[index]
                compare("column-left", reference, index, ref[0], box[0])
                compare("column-right", reference, index, ref[2], box[2])
                compare("column-width", reference, index, ref[2] - ref[0], box[2] - box[0])

    report = {
        "schema_version": 2,
        "layout": "mixed" if groups is not None else "grid",
        "groups": groups,
        "applicable": len(axes) > 1,
        "verdict": "PASS" if not failures else "FIX BEFORE DELIVERY",
        "tolerance_pt": tolerance_pt,
        "rows": rows,
        "cols": cols,
        "panels": [{"index": index, "bbox_pt": box} for index, box in enumerate(boxes)],
        "failures": failures,
    }
    if json_out is not None:
        path = Path(json_out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if failures:
        raise RuntimeError(f"panel alignment failed: {failures}")
    return report


def audit_content_spacing(
    fig, panel_artists, pairs, *, target_mm=2.5, tolerance_mm=0.5,
    exceptions=None, json_out=None,
):
    """Measure decorated bounds. Pairs are (left, right, 'horizontal') or
    (upper, lower, 'vertical'). Supply every twin/colourbar in its panel list.
    For circles, explicit wedges/text may replace an invisible axes rectangle.
    Exceptions map pair index to a documented reason; overlaps always fail.
    """
    from matplotlib.transforms import Bbox
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    boxes = []
    for artists in panel_artists:
        extents = [a.get_tightbbox(renderer) for a in artists if a.get_visible()]
        extents = [b for b in extents if b is not None]
        if not extents:
            raise ValueError('each panel needs visible content')
        boxes.append(Bbox.union(extents))
    records, failures = [], []
    exceptions = exceptions or {}
    for index, (first, second, direction) in enumerate(pairs):
        a, b = boxes[first], boxes[second]
        if direction == 'horizontal':
            gap = b.x0 - a.x1
        elif direction == 'vertical':
            gap = a.y0 - b.y1
        else:
            raise ValueError('direction must be horizontal or vertical')
        gap_mm = gap * 25.4 / fig.dpi
        reason = exceptions.get(index)
        valid = gap_mm >= 0 and (abs(gap_mm-target_mm) <= tolerance_mm or bool(reason))
        record = {'panels':[first,second], 'direction':direction,
                  'gap_mm':float(gap_mm), 'exception_reason':reason, 'passed':bool(valid)}
        records.append(record)
        if not valid:
            failures.append(record)
    report = {'verdict':'PASS' if not failures else 'FIX BEFORE DELIVERY',
              'target_mm':target_mm, 'tolerance_mm':tolerance_mm,
              'canvas_mm':(fig.get_size_inches()*25.4).tolist(), 'pairs':records}
    if json_out is not None:
        Path(json_out).write_text(json.dumps(report,indent=2),encoding='utf-8')
    if failures:
        raise RuntimeError(f'content spacing failed: {failures}')
    return report


def save_bundle(
    fig: mpl.figure.Figure,
    output_base: str | Path,
    *,
    primary_axes: Iterable[mpl.axes.Axes] | None = None,
    rows: int = 1,
    cols: int = 1,
    alignment_groups: Sequence[dict] | None = None,
    formats: Sequence[str] = ("svg",),
    tight_crop: bool = True,
    padding_mm: float = 1.5,
) -> dict | None:
    """Export SVG by default; additional formats require an explicit user request."""
    selected = list(dict.fromkeys(fmt.lower().lstrip(".") for fmt in formats))
    if not selected or any(fmt not in {"svg", "pdf", "png", "tiff", "tif"} for fmt in selected):
        raise ValueError("formats must specify svg, pdf, png, tiff or tif")
    base = Path(output_base)
    base.parent.mkdir(parents=True, exist_ok=True)
    axes = list(primary_axes) if primary_axes is not None else []
    report = None
    if rows * cols > 1 or len(axes) > 1 or alignment_groups is not None:
        report = audit_panel_alignment(
            fig,
            axes,
            rows=rows,
            cols=cols,
            groups=alignment_groups,
            json_out=str(base) + ".alignment.json",
        )
    for fmt in selected:
        options = {"bbox_inches": "tight", "pad_inches": padding_mm / 25.4} if tight_crop else {}
        if fmt == "png":
            options.update({"dpi": 300})
        elif fmt in {"tiff", "tif"}:
            options.update({"dpi": 600, "pil_kwargs": {"compression": "tiff_lzw"}})
        fig.savefig(str(base) + "." + fmt, **options)
    return report
