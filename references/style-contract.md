# Personal style contract

## Matrix notation and dimensions

Interpret layout dimensions as mathematical matrices:

- `1 x 2` means one row and two columns.
- `2 x 1` means two rows and one column.
- `3 x 1` means three vertically stacked panels; `3 x 2` means three rows and two columns (six panels).
- In general, use `rows x columns`.

Reference widths (not mandatory full-width targets):

| Layout | Default width | Use |
|---|---:|---|
| `1 x 1` | 89 mm | ordinary single panel |
| `1 x 2` | 180 mm | horizontal two-panel composite |
| simple `2 x 1` | 89 mm | vertical single-column composite |
| complex `2 x 1` | 180 mm | heatmaps, long labels, dual/triple axes, or dense legends |
| simple `3 x 1` | 89 mm | three compact single-column panels |
| complex `3 x 1` | 180 mm | three dense full-width panels |
| `2 x 2`, `3 x 2` | 180 mm | four or six panels organized into comparison rows/columns |
| other `rows x columns` | 180 mm for multiple columns or complex multi-row layouts | supported when the evidence requires more panels; assess each panel's usable width |

These examples are not a limit on panel count. Choose rows and columns from the evidence structure. The helper supports arbitrary positive integer row and column counts. For multiple rows, compact initial height is `50 * rows + 6 * (rows - 1)` mm, or `60 * rows + 6 * (rows - 1)` mm with `complex_layout=True`. Thus a 3-row canvas starts at 162 mm or 192 mm high. These are editable starting sizes, not fixed journal limits or actual inter-panel gaps. Override width/height for plot aspect, labels and journal requirements; reduce excess canvas height after arranging the content. For three or more columns, check legibility at the final publication width; rearrange or split a crowded figure instead of reducing the prescribed font sizes.

Choose width from the content, usable panel area and overall proportions rather than always filling a publication column or page. The 89 mm and 180 mm values are reference presets, not minimum widths. A compact two-panel figure may, for example, use 120-160 mm; a simple single panel may use 70-89 mm. These are starting examples, not fixed ranges. Complex figures may also be narrower when labels and evidence remain clear.

Set `width_mm` explicitly when a narrower composition is appropriate. Keep font and marker sizes at their prescribed final physical sizes: redraw at the selected width rather than shrinking an exported figure. Reconsider the height with the width to avoid an unnecessarily tall or wide canvas. Comparable figures may share widths for consistency, but every figure need not have the same width. Preserve intended within-group alignment, not a requirement that every panel span the entire canvas.

Verified journal production requirements take precedence; distinguish mandatory column widths from maximum allowed widths. Inspect at intended final size before delivery. A narrower canvas must not create label overlap, obscure data or compress critical variation.

Allow spanning rows/columns and unequal panel sizes for mixed evidence (e.g. a wide map above small time series). Equal-sized panels are preferred within direct comparison groups, not required globally. Keep shared-time-axis panels aligned left/right. Audit explicitly declared comparison groups at 1.5 pt tolerance; see `audit_panel_alignment(groups=...)` in the helper.

## Compact panel spacing

- Default to compact composition. After rendering all labels, ticks, panel letters and legends, target about 2-3 mm clear space between the nearest visible content of adjacent panels. This is content-to-content clearance, not spine-to-spine distance and not a universal maximum.
- For shared-x stacked time series, hide redundant upper tick labels and x-axis titles. Start from a 3-5 mm spine gap only when labels/letters fit; content clearance takes precedence.
- Omit panel titles and use shared legends where useful. Do not reserve empty strips for titles or footer explanations.
- Keep direct comparison groups close with consistent spacing; distinct evidence groups may have a slightly larger gap. Mixed layouts need not have globally identical gaps.
- Reduce canvas height when removing vertical whitespace; do not merely move the blank area into outer margins. Preserve scientifically useful plot heights and aspect ratios, especially maps and images.
- Keep prescribed font sizes. Increase space only where actual content requires it. Do not achieve compactness through overlapping labels, cropping or hidden observations.
- For regular subplot grids, call `compact_layout(fig)` after adding decorations as a starting adjustment. It uses Matplotlib's rendered layout bounds; verify the result at final size. For manually placed axes, twins, figure-level legends and spanning/mixed layouts, explicitly measure all relevant artist bounds and arrange the groups; do not assume this helper handles them automatically.

Measure and record each adjacent pair after the final draw, including auxiliary axes and external decorations. A spacing result is separate from the plot-area alignment result. Use `audit_content_spacing` with explicit panel artist groups and adjacency pairs. Fix overlaps and unjustified gaps before delivery; larger intentional grouping gaps must have a recorded reason. Do not hard-code column origins (for example 15 and 103 mm) and assume that alignment implies compactness.

For mixed circular and Cartesian charts, retain meaningful row/group alignment rather than forcing identical column origins that introduce empty space. Measure visible wedges and labels where an invisible axes rectangle would overstate occupied content. Do not shrink fonts or distort circles to close a gap.

## Export extent and background

Default SVG exports crop to the full visible artwork with about 1.5 mm outer padding, including external annotations and colour bars. Keep the white background by default. Background transparency does not remove canvas margins; adjust the export bounds instead. If the user requires an exact physical canvas size, lay out to that size and disable tight cropping explicitly.

## Typography

- Ordinary text defaults to pure black (`#000000`): annotations, panel titles/letters, legend text, axis titles and tick labels. Use series-coloured text only where it identifies a variable directly, especially dual/triple axes; neutral reference lines and borders may remain grey.
- Font family: Matplotlib's default DejaVu Sans first, then Arial. For Chinese or other missing glyphs, append an available language font (e.g. Microsoft YaHei) after these; retain DejaVu Sans for Latin letters and numbers where supported.
- Default body and ticks: 8 pt. Legends: 8 pt normally, 7.5 pt for compact layouts (the helper default).
- Axis labels: 8.5-9 pt.
- Lowercase bold panel labels: 9.5-10 pt, outside the upper-left plot corner with a fixed point offset.
- Absolute rendered glyph floor: 6 pt.
- Font sizes are increased by 1 pt from the previous style at the final physical output size. Increase other explicitly sized annotations by 1 pt when revising a figure to this style; reflow spacing instead of shrinking the text. Do not repeatedly add 1 pt to figures already using the updated style.
- Keep variables, symbols, subscripts, superscripts, and units scientifically correct; do not shrink them below the floor.

## Axes and line language

- White figure and axes background.
- Four-sided boxed axes are the default.
- Major and minor ticks point outward; do not show a default grid.
- Default spine width: 0.75 pt.
- Default data-line width: 1.3-1.6 pt.
- Reference lines use light grey and 0.8-1.0 pt. Dashed lines may also distinguish depth ranges, scenarios, periods or observed/modelled series. Define this second encoding in a legend and use it consistently; avoid ambiguous reuse for both a reference and a data category.
- Do not hide relevant baselines or truncate scales merely to enlarge an effect.

## Colour mapping and high-saturation palette

High-saturation colours are the default for primary curves, points and bars. Use a manuscript-wide variable/object-to-colour mapping across maps, time series, comparisons and subsequent figures. This mapping takes precedence over the suggested roles below. Do not silently recolour accepted existing figures as a side effect of a skill update.

| Colour | Hex | Suggested role (not mandatory) |
|---|---|---|
| deep blue | `#003F88` | baseline, rainfall or a primary series; preferred over bright electric blue |
| cyan-blue | `#0099E6` | a related secondary series |
| green | `#008A00` | another variable or model |
| purple | `#9500B3` | another variable, scenario or region |
| orange | `#FF8000` | reservoir variation or a contrast |
| red | `#E60000` | a contrast, positive anomaly or strong response |
| yellow | `#F2C000` | optional highlight; avoid thin yellow lines on white |
| pale blue | `#D6E8FF` | subordinate backgrounds or defined windows |

Red does not necessarily mean hazard; interpretation follows the variable mapping or colour scale. Grey is preferred for pairing lines, neutral references and secondary structure. Limit simultaneous categorical colours to what can be distinguished clearly. Saturation alone does not establish accessibility: use line styles or marker shapes when needed and check greyscale and common colour-vision deficiencies, especially red/green pairs.

- Absolute quantities or one-direction intensity: a perceptually ordered sequential scale.
- Signed anomalies, differences and residuals: a diverging scale centred on the meaningful reference (usually zero), with balanced limits when direct positive/negative comparison is intended. Report any asymmetric limits.
- Discrete categories: distinct high-saturation colours, stable across the manuscript.
- Do not use rainbow, jet or HSV colour maps. High saturation does not require strongly coloured backgrounds or uniformly saturated continuous fills.

## Visual hierarchy

These are adjustable starting values, not measurements extracted from the reference papers:

| Element | Default treatment |
|---|---|
| Raw fluctuation trace | 0.6-0.9 pt; same hue, alpha 0.25-0.45 |
| Main trend or focal curve | 1.2-1.6 pt; alpha 1.0 |
| Uncertainty band | Same hue, alpha 0.15-0.25; normally no edge |
| Defined event window | Light grey or pale colour behind the data; alpha about 0.10-0.20 |
| Zero/reference line | Grey, 0.8-1.0 pt; weaker than data |

Low-opacity raw lines, uncertainty bands and event windows encode different things: label their meaning explicitly. Preserve all observations; do not introduce smoothing for appearance alone. When a trend is scientifically justified, state the smoother and window. Monthly count data may remain bars without a smoothed overlay.

## Data markers

- Prefer circle, square, upward triangle, diamond, then downward triangle (`o`, `s`, `^`, `D`, `v`). Keep object-to-colour and object-to-shape mappings consistent across the manuscript; the order is a default, not a fixed scientific meaning.
- Ordinary marker size: 4-5 pt (helper default 4.5 pt). Focal markers: 6-7 pt (default 6.5 pt). Dense scatter may use smaller symbols after checking final-size legibility.
- Solid marker fills use a slightly lighter tint of the corresponding line/series colour: mix 25% white into the base colour by default. Keep the line at its original colour and the marker fill opaque; do not use transparency to obtain this tint. Adjust the white fraction if needed, retaining a recognizable same-colour relationship. For standalone scatter, tint its assigned series colour in the same way. Hollow symbols encode an explicitly defined second category; do not switch fill styles arbitrarily.
- Data-marker edges default to pure black (`#000000`), width 0.5-0.75 pt (default 0.6 pt), for both solid and hollow markers. Hollow markers retain a black outline; use shape or another explicit encoding to distinguish categories where fill colour is absent. Override the outline only when explicitly requested or scientifically necessary. These marker rules do not change the colours of lines, bars or uncertainty bands.
- Sparse line series may show each observed point. Dense time series should not place a large marker at every point. If symbols are drawn only at selected positions, preserve the full underlying series and do not imply that unmarked observations were excluded.
- Reserve stars and other conspicuous shapes for defined focal cases or events rather than ordinary categories. Explain their meaning in the legend/caption.
- Sizes refer to the final physical figure. Matplotlib `plot` uses `markersize` in pt; `scatter` uses `s` in pt squared. For the same nominal size `d`, use `markersize=d` or `s=d**2`. This is a nominal conversion, not equal perceived area across different shapes; inspect shape balance and edge effects.
- Use `marker_style(..., kind="plot" or "scatter")` from the helper. It returns marker properties only; do not add markers to every line automatically.

## Legends and direct labels

- Place a legend inside the plot only when a genuine empty region exists.
- Move the legend outside when it crosses data, uncertainty, bars, heatmaps, or reference lines.
- Use one shared legend for repeated categories across panels.
- Prefer direct end labels for stable line identities when they remain clear.
- Do not mask a curve with an opaque white text box.
- Do not add a redundant legend when colour-matched axis labels make a dual/triple-axis mapping unambiguous.

## Dual and triple y axes

Dual and triple axes are allowed, not mandatory.

- All y variables must share the same x domain and observation basis.
- Every axis shows a complete variable name and unit.
- The left axis carries the primary forcing or response.
- The first right axis remains at the normal right spine.
- A third y axis is placed on an outward-shifted right spine, normally 36-44 pt.
- Axis label, tick, and spine colour must map one-to-one to the corresponding data series.
- Keep the primary axes four-sided; auxiliary twins should not duplicate top, bottom, or left spines.
- Reserve enough right margin for the outer axis; never solve crowding by shrinking text below the minimum.
- If three axes remain ambiguous or collide at 180 mm width, replace them with stacked panels.

## Panel titles

Do not add titles above individual panels by default. Retain lowercase panel letters and necessary axis labels, units and legends. Put panel explanations in the external caption, not inside a title or footer. Add titles only if the user explicitly requests an exception.

## Formal-figure boundary

Do not add a figure-level title, colour card, colour hex labels, demo banner, institution logo, watermark, decorative headline or extra bottom explanatory text. Put explanations in the external caption, manuscript text or accompanying notes. For synthetic style examples, identify the synthetic data clearly in the accompanying notes and delivery message rather than adding a footer to the image.

For cell-value labels on dark heatmap cells, white is allowed when required for contrast; ordinary text elsewhere remains black.
