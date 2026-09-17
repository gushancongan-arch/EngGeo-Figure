---
name: enggeo-figure
description: Create, revise, and audit publication-grade geology, geotechnical, and landslide figures in Python/Matplotlib using the user's calibrated Origin-inspired style. Use for geological time series, hydro-mechanical dual/triple-axis plots, depth profiles, group comparisons, pie/donut composition charts, distributions, heatmaps, validation plots, and labelled multi-panel figures. Do not use for GIS map production, photo editing, or AI-generated mechanism illustrations.
metadata:
  version: "1.0"
---

# EngGeo Figure v1.0

Create evidence-led scientific figures with a consistent personal visual language. Default to high-saturation primary series, a manuscript-wide variable-to-colour mapping, and subordinate raw traces, uncertainty and backgrounds. Mixed layouts follow evidence roles rather than equal panel sizes. Use Python/Matplotlib for every render and export produced by this skill.

## Before plotting

1. State the one-sentence scientific claim or, for a style test, state that no scientific claim is being made.
2. Map each panel to a distinct evidence role. Do not add panels merely to display another metric.
   Choose a content-appropriate canvas width and balanced aspect ratio; do not automatically fill the available column or page width. Use explicit dimensions where the reference presets are unnecessarily wide.
3. Preserve every supplied observation unless an exclusion is scientifically justified and reported.
4. Use generated data only for an explicitly labelled calibration or demonstration workflow. Never present generated values as measurements.

## Required style contract

Read [references/style-contract.md](references/style-contract.md) before every render. It owns matrix notation, dimensions, typography, boxed axes, colour semantics, legends, and dual/triple-axis rules.

Read [references/chart-recipes.md](references/chart-recipes.md) when choosing a chart family, arranging multi-panel evidence, or using more than one y axis.

Read [references/data-and-qa.md](references/data-and-qa.md) before final export or whenever real data, uncertainty, missing values, filtering, or statistical annotations are involved.

## Reusable implementation

Prefer [scripts/enggeo_style.py](scripts/enggeo_style.py) instead of recreating rcParams, dimensions, panel labels, multi-axis styling, alignment checks, and exports.

Use [scripts/calibration_demo.py](scripts/calibration_demo.py) only to verify installation or deliberately generate style-test figures. Its output is demonstrative, not evidence.

## Delivery contract

- Figures contain no figure-level or per-panel titles, palette card, demo banner, logo, watermark, decorative heading or extra footer explanation unless explicitly requested. Retain panel letters, axis labels and legends; identify synthetic examples in accompanying notes and the delivery message.
- Export editable SVG only by default. Export PDF, PNG, TIFF or any additional image format only when the user explicitly requests it; do not automatically generate previews in those formats.
- Keep every rendered glyph at or above 6 pt; default body text is 8 pt.
- For two or more primary panels, audit intended plot-area alignment at a 1.5 pt tolerance AND measure decorated content spacing after the final draw. Alignment alone is not a spacing check. Include twin axes, labels, legends and colour bars. Target 2-3 mm, normally 2.5 mm; justify larger gaps by actual content or grouping. Reduce the canvas when compressing gaps rather than moving whitespace to its edges.
- Inspect the final SVG in an SVG-capable viewer, or inspect an in-memory rendering without exporting another image format, for clipping, label collisions, ambiguous axis mappings, hidden uncertainty, and misleading scales.
- Deliver the plotting source and source data or a traceable data-export file with the figure bundle.
