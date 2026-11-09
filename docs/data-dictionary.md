# Data dictionary

`data/graded_predictions.csv` — 1,000 rows, UTF-8, comma-separated, header row present.

| Column | Type | Meaning | Notes |
|---|---|---|---|
| `prediction_id` | int | Prediction record identifier | Monotonic. Gaps mean the row was never graded, not that it was deleted. |
| `fixture_id` | int | Fixture identifier | Joins to the platform's fixture table (not included). |
| `model_ref` | int | Model identifier | An opaque integer. Training data, features and weights are not published. |
| `mkt_p_home` | float, 4dp | Market-implied probability, home win | Derived from publicly quoted pre-kickoff prices, normalised so the row sums to 1. |
| `mkt_p_draw` | float, 4dp | Market-implied probability, draw | Same derivation. |
| `mkt_p_away` | float, 4dp | Market-implied probability, away win | Same derivation. |
| `direction` | enum | The model's stated lean | `home` / `draw` / `away` / `home/draw` / `away/draw` |
| `confidence` | int 1–10 | The model's own confidence scale | Not a probability. Not comparable across models. |
| `kickoff_date` | date | Fixture date (YYYY-MM-DD) | All rows satisfy `created_at < kickoff`. |
| `final_score` | string | Full-time score as `home-away` | Includes stoppage time, excludes penalties. |
| `outcome` | char | `H` home win / `D` draw / `A` away win | Derived from `final_score`. |

## Constraints a consumer should assume

1. `mkt_p_home + mkt_p_draw + mkt_p_away = 1.0000` (±0.0001 rounding), always.
2. `direction` is never empty; `confidence` is never null.
3. No row has been modified after grading. Re-derived `outcome` from `final_score` must match column `outcome` — that check is in `scripts/verify.py`.
4. `model_ref` values are stable across the file but are not published as a mapping. Two rows with the same `model_ref` are the same model instance.

## What is not published, deliberately

- Training corpora and training words per model
- Feature definitions and weights
- The free-text reasoning behind each prediction
- Any mapping from `model_ref` to a public model name

The published part is the part that can be checked: what was claimed, when, and what happened.
