# Style Presets — Token-Based Visual Identity Swapping

> Lets sub-agents pick `style × structure` independently — colors are abstracted via tokens, so swapping a preset changes the entire visual identity without touching body code.

## How it works

Each skeleton (D/E/F/G — being rolled out one by one) contains a **PRESET DEFINITION block** at the top, marked clearly:

```latex
% ----- BEGIN PRESET DEFINITION -----
\definecolor{c_primary_line}{HTML}{3B82F6}       \definecolor{c_primary_fill}{HTML}{DBEAFE}
\definecolor{c_hero_line}{HTML}{7030E0}          \definecolor{c_hero_fill}{HTML}{EDE9FE}
...
% ----- END PRESET DEFINITION -----
```

Below that block is a **BACKWARDS-COMPAT ALIASES** block that maps the legacy color names (`acaBlueLine`, `purpleDeep`, etc.) to the new tokens via `\colorlet`. The body code is unchanged — it still uses `acaBlueLine`, but `acaBlueLine` now resolves to `c_primary_line` which is defined by whichever preset is active.

**To switch styles**: replace the PRESET DEFINITION block with the contents of one of the preset files in this directory. Do NOT touch the BACKWARDS-COMPAT ALIASES block or the body code.

## Token semantics (16 tokens)

| Token | Role |
|---|---|
| `c_primary_line` / `c_primary_fill` | Main entity layer (clients / inputs / parties) |
| `c_hero_line` / `c_hero_fill` | Core processing zone — the visual focal point |
| `c_hero_deep` / `c_hero_mid` / `c_hero_light` / `c_hero_pale` | Hero zone internal depth (4 levels, deepest to palest) |
| `c_accent_line` / `c_accent_fill` | Secondary / specialty zone (security, analysis, etc.) |
| `c_success_line` / `c_success_fill` | Positive indicators (checks, "OK", confirmations) |
| `c_data_curve_line` / `c_data_curve_fill` | Time-series chart curves and area fills |
| `c_warning_line` / `c_warning_fill` | Alerts, errors, dangers |
| `c_neutral_line` / `c_neutral_fill` | Grey strokes, fills, axes, dim text |
| `c_bar_1` / `c_bar_2` / `c_bar_3` | Multi-bar chart palette (max 3 categories) |

## Available presets

| Preset | File | Visual Identity |
|---|---|---|
| **Academic Professional** (default) | `preset-academic.tex` | Soft pastel fills, mid-saturation strokes, drop shadows. Mainstream journal aesthetic. |
| **Brutalism / High Contrast** | `preset-brutalism.tex` | Pure B&W with a single bright accent (yellow). No shadows, thick borders ideally (but borders are controlled by `base_box` style, not by tokens). |
| **Editorial / Magazine** | (TODO) | Single accent + grey + lots of whitespace |
| **Light Luxury** | (TODO) | Pastels + hairlines + refined typography |

## Workflow for sub-agent in Mode A

1. User asks for figure → ⓪.5 mode = A (skeleton)
2. Sub-agent picks structure (B/C/D/E/F/G) based on layout fit
3. Sub-agent picks style (academic / brutalism / editorial / luxury) — defaults to academic
4. Sub-agent copies the chosen skeleton entirely
5. If style ≠ academic: sub-agent finds the `BEGIN PRESET DEFINITION` block and replaces it with the chosen preset's content from this directory
6. Sub-agent proceeds with content changes (renames, etc.) as before, **never touching the ALIASES block or body color references**

## Caveats

- Tokens cover **colors only**. Style attributes like border thickness, drop shadow opacity, corner radius are controlled by the `base_box` / arrow `.style` definitions in the tikzpicture — these are NOT yet token-ized.
- The `\colorlet` aliasing means `acaBlueLine!70!black` still works because xcolor's `!N!c` mix operator works on any registered color name, whether defined via `\definecolor` or `\colorlet`.
- Brutalism radar polygons may visually merge because both polygons use shades of black — semantic limitation worth noting.
