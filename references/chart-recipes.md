# Geology chart recipes

Choose the smallest chart family that establishes the intended claim.

## Event time series

Use rainfall bars, reservoir-level lines, displacement curves, velocity curves, pore-pressure ratios, or other event-aligned variables. Keep one shared time basis. Use pale-blue intervals only when an event window has a defined meaning.

- Discovery: forcing in panel `a`, response in panel `b`.
- Mechanism: displacement in panel `a`, velocity or pore pressure in panel `b`.
- Multi-axis: use only when synchronization is the inference; otherwise use stacked panels.
- For a key episode, pair the full record with a labelled zoom panel. Mark the same interval in the full record; add restrained connectors only if they clarify the relationship.
- Use distinct marker shapes for discrete external events, with timing and magnitude defined. Raw traces, trends, uncertainty and event windows follow the visual hierarchy in the style contract; none should be confused with the others.

## Group comparisons

- Use grouped bars for genuine aggregate comparisons. For estimated quantities, define the uncertainty interval. Exact descriptive inventory/cohort counts may have no error bars: state their counting scope and do not invent sampling uncertainty.
- Prefer raw points plus box/violin summaries when sample size is modest.
- Use horizontal point-range plots for effect estimates and confidence intervals.
- Show paired before-after lines when the replicate unit is matched.

## Depth and spatial profiles

Plot depth increasing downward. Keep the same depth direction and limits across comparable panels. A shaded slip-zone interval is acceptable when independently defined; it must not be inferred merely from the plotted peak.

Typical pairs include pore pressure versus depth and shear strain versus depth, or displacement versus depth and material/interface annotations.

## Spatiotemporal matrices

Use a perceptually ordered sequential colour scale for absolute quantities, a reference-centred diverging scale for signed anomalies, and a categorical palette for discrete classes. Show units on both axes and a compact colour bar. Preserve missing regions rather than filling them with zero. Rasterize dense cells when needed, but keep labels and vector annotations editable.

## Relationships and validation

- Scatter plots should retain all observations unless a reported exclusion rule applies.
- Distinguish observed-versus-predicted validation from calibration or training fit.
- A 1:1 reference line is not a fitted regression.
- Report metrics only when their data partition and definition are known.

## Model performance

ROC and precision-recall curves answer different questions; pair them when class imbalance matters. Keep model colours consistent and preserve names such as `XGBoost`, `RF`, and `LR` without blind title casing.

## Multi-panel evidence logic

Each figure should normally support one major claim. Panels must contribute different evidence roles such as forcing, response, mechanism, validation, comparison, robustness, or failure boundary. If removing a panel does not weaken the argument, merge, demote, or remove it.

## Composition charts and mixed chart examples

Pie and donut charts are available for a small number of parts forming one explicitly defined total. Use flat, undistorted circles, stable category colours, and readable direct category/percentage labels; no 3D effects. Keep labels clear of wedge boundaries and check rounding totals. Cartesian boxes and ticks do not apply to circular charts. Prefer bars when precise comparisons or many categories are the evidence need. A chart-type demonstration may repeat one synthetic dataset to compare representations; state that it is not independent evidence.

Box plots should identify median, quartiles, whisker rule and sample size externally; for small samples retain all raw points, including outliers. Horizontal jitter changes only display position. Heatmaps need a sequential scale for counts/absolute values and a diverging scale for signed deviations; use a labelled colour bar and account for it in panel spacing.

For repeated dual-y panels, use identical left/right limits for directly comparable variables unless a documented reason requires otherwise. Keep colour, shape, line style and variable mapping consistent. Upper x labels may be omitted with a shared time basis; every variable still needs a clear name and unit. All auxiliary y axes participate in the content-spacing audit.
