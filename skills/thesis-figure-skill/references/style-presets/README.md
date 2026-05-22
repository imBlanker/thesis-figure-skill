# Style Presets — Token-Based Visual Identity Swapping

> Lets sub-agents pick `style × structure` independently — colors are abstracted via tokens, so swapping a preset changes the entire visual identity without touching body code.

## How it works

Each token-ized skeleton (currently **D, E, F, G** — B/C still use hardcoded colors) contains a **PRESET DEFINITION block** at the top, marked clearly:

```latex
% ----- BEGIN PRESET DEFINITION -----
\definecolor{c_primary_line}{HTML}{3B82F6}       \definecolor{c_primary_fill}{HTML}{DBEAFE}
\definecolor{c_hero_line}{HTML}{7030E0}          \definecolor{c_hero_fill}{HTML}{EDE9FE}
...
% ----- END PRESET DEFINITION -----
```

Below that block is a **BACKWARDS-COMPAT ALIASES** block that maps the legacy color names (`acaBlueLine`, `purpleDeep`, etc.) to the new tokens via `\colorlet`. The body code is unchanged — it still uses `acaBlueLine`, but `acaBlueLine` now resolves to `c_primary_line` which is defined by whichever preset is active.

**To switch styles**: replace the PRESET DEFINITION block with the contents of one of the preset files in this directory. Do NOT touch the BACKWARDS-COMPAT ALIASES block or the body code.

## Token semantics

**Core 16 (all token-ized skeletons use a subset of these)**:

| Token | Role |
|---|---|
| `c_primary_line` / `c_primary_fill` | Main entity layer (clients / inputs / parties / parallel instances) |
| `c_hero_line` / `c_hero_fill` | Core processing zone — the visual focal point |
| `c_hero_deep` / `c_hero_mid` / `c_hero_light` / `c_hero_pale` | Hero zone internal depth (4 levels, deepest to palest) — used by D |
| `c_accent_line` / `c_accent_fill` | Secondary / specialty zone (security, analysis, etc.) |
| `c_success_line` / `c_success_fill` | Positive indicators (checks, "OK", confirmations) |
| `c_data_curve_line` / `c_data_curve_fill` | Time-series chart curves and area fills |
| `c_warning_line` / `c_warning_fill` | Alerts, errors, dangers |
| `c_neutral_line` / `c_neutral_fill` | Grey strokes, fills, axes, dim text |
| `c_bar_1` / `c_bar_2` / `c_bar_3` | Multi-bar chart palette (≤3 categories) |

**Extended tokens (used by E/F for richer data viz)**:

| Token | Role |
|---|---|
| `c_bar_4` | 4th bar color (when ≥4 grouped categories needed) — used by E, F |
| `c_heat_5` / `c_heat_4` / `c_heat_3` / `c_heat_2` | Heatmap gradient (5=deepest, 2=lightest) — used by E, F |
| `c_heat_bg` | Heatmap background tint — used by E, F |

**Skeleton-internal hardcoded colors (NOT preset-controlled, kept stable across styles)**:

- **G**: `drawPurpleLine` / `drawPurpleFill` — G's "上传/下发" federated feedback flow signature
- **F**: 5 signal colors (`acaGoldLine/Fill`, `acaCyanLine/Fill`, `acaPinkLine/Fill`, `acaYellowLine/Fill`, `acaLimeLine/Fill`) + 5 zone background colors (`zone{Blue,Green,Purple,Red,Yellow}Bg`) — protocol-annotation specific, bound to phase identity

## Available presets

| Preset | File | Visual Identity |
|---|---|---|
| **Academic Professional** (default) | `preset-academic.tex` (D's values) | **Per-skeleton** — each token-ized skeleton's PRESET DEFINITION block holds its own Academic identity (D uses purple hero, G uses red hero, etc.). `preset-academic.tex` documents D's values as a representative example. |
| **Brutalism / High Contrast** | `preset-brutalism.tex` | **Universal** — same values work across D/E/F/G. Pure B&W with a single bright yellow hero accent. Validated on D and G. |
| **Editorial / Magazine** | `preset-editorial.tex` | **Universal** — deep navy hero + cream backgrounds + single deep-red accent + warm greyscale. New Yorker / Atlantic aesthetic. Validated on D. |
| **Light Luxury** | `preset-luxury.tex` | **Universal** — dusty mauve hero + sage / champagne / soft pink palette. Refined low-contrast. Validated on E. |

## Workflow for sub-agent in Mode A

1. User asks for figure → ⓪.5 mode = A (skeleton)
2. Sub-agent picks structure (B/C/D/E/F/G) based on layout fit
3. Sub-agent picks style (academic / brutalism / editorial / luxury) — defaults to academic
4. Sub-agent copies the chosen skeleton entirely
5. If style ≠ academic: sub-agent finds the `BEGIN PRESET DEFINITION` block and replaces it with the chosen preset's content from this directory. **For universal presets (Brutalism / Editorial / Luxury) the same paste-ready block works across all token-ized skeletons.** For Academic the skeleton's own existing block already encodes its Academic identity — no swap needed.
6. Sub-agent proceeds with content changes (renames, etc.) as before, **never touching the ALIASES block or body color references**

## Caveats

- Tokens cover **colors only**. Style attributes like border thickness, drop shadow opacity, corner radius are controlled by the `base_box` / arrow `.style` definitions in the tikzpicture — these are NOT yet token-ized.
- The `\colorlet` aliasing means `acaBlueLine!70!black` still works because xcolor's `!N!c` mix operator works on any registered color name, whether defined via `\definecolor` or `\colorlet`.
- **F's mixed-look caveat** — F has 5 zone backgrounds + 5 signal colors kept hardcoded for protocol-annotation identity. Under a non-Academic preset, F's phase-chip backgrounds stay colored while phase internals become preset-styled. This is intentional but if you want strict styling on F, manually override the `zoneXxxBg` and `acaGold/Cyan/Pink/Yellow/Lime` definitions too.
- Brutalism radar polygons may visually merge because both polygons use shades of black — semantic limitation worth noting.
