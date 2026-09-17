# Data integrity and QA

## Source-data boundary

- Preserve the raw input and use all supplied observations by default.
- Never silently drop missing values, outliers, replicates, sites, sensors, dates, or categories.
- Report every exclusion with the exact predicate and before/after counts.
- Do not replace missing observations with zero unless zero is a documented physical observation.
- Generated data are allowed only for installation checks, style calibration, or explicit demonstrations. Keep them in a separate demo output and label them as illustrative.
- A fitted coefficient is not independent validation. Keep fit, conditional extrapolation, external validation, and transportability distinct.

## Uncertainty and statistics

For every aggregate, identify:

- replicate unit and sample size;
- centre statistic;
- SD, SE, confidence interval, quantile interval, or other spread definition;
- statistical test and multiplicity correction, if any;
- exact comparison represented by each annotation.

Use the same uncertainty definition across directly comparable panels or document the exception. For small samples, show raw observations where practical.

## Geometry and alignment

- Measure alignment after the final draw, not from source GridSpec values alone.
- Default tolerance is 1.5 pt for intended shared edges, plot-area widths/heights, and repeated gutters. For mixed/spanning layouts, declare the intended comparison groups; do not force all panels to equal sizes. Record which edges/dimensions are checked. Gutter checks, when applicable, must be measured separately if not covered by the helper.
- In `1 x 2`, panels share top and bottom plot-area edges.
- In `2 x 1`, panels share left and right plot-area edges.
- Exclude auxiliary twins and colour bars from primary plot-area alignment, but INCLUDE them in decorated content-spacing checks. Record horizontal and vertical gaps in mm, the final canvas dimensions, and any justified gap exceptions. Do not report layout QA passed from alignment alone.

## Export bundle

- Editable SVG only by default; retain editable text.
- Additional image formats require an explicit user request, including preview files. When requested, use editable-text PDF, PNG normally at 300 dpi, or TIFF at 600 dpi unless specified otherwise.
- `save_bundle` defaults to `formats=("svg",)`. Pass an explicit formats list only matching the user's request. A generic request to draw, preview or package a figure is not a request for all formats.
- Inspect SVG directly or use an in-memory canvas for visual QA; do not automatically save a PNG/PDF solely for inspection. Retain internal code, source data and QA records for reproducibility; default user-facing figure links should point to SVG.
- Plotting source and traceable source data.
- Alignment report for multi-panel figures.

## Final inspection

Inspect each panel and the assembled figure at final physical size:

- no clipping, text-text overlap, or data line crossing through labels;
- panel labels are aligned and legible;
- panel spacing is compact at final size: normally 2-3 mm between adjacent content bounds, with larger gaps justified by grouping or actual labels; excess canvas height is removed without shrinking the prescribed fonts;
- legends do not obscure evidence;
- axis colours and units are unambiguous, especially for dual/triple axes;
- primary series use the agreed high-saturation colours consistently; raw traces, bands and backgrounds remain subordinate; red is interpreted through the documented mapping rather than assumed to indicate hazard;
- continuous maps remain interpretable in greyscale and common colour-vision deficiencies;
- no generated data, placeholder labels, or private local paths remain in a production figure.
