# SoccerDream AI — Graded Prediction Dataset

A small, real, schema-documented slice of an open prediction pipeline: 1,000 graded football predictions written before kickoff, published as-is — wins and losses, no filtering.

The point of this repository is not the volume. It is the **grading discipline**: every row here was written to an append-only table before the fixture started, and graded exactly once afterwards. Bad weeks are still in the file.

- Rows: **1,000**
- Distinct models: **157**
- Kickoff window: **2026-07-04 → 2026-10-07**
- Missing/edited rows: **none**

## Files

| Path | What it is |
|---|---|
| `data/graded_predictions.csv` | The dataset — 1,000 graded rows |
| `schema/predictions.sql` | The table design that makes the rows tamper-evident |
| `docs/data-dictionary.md` | Every column, its meaning, its allowed values |
| `CITATION.cff` | Machine-readable citation |

## What is in a row

One row = one model's pre-kickoff view of one fixture, plus the result.

```csv
prediction_id,fixture_id,model_ref,mkt_p_home,mkt_p_draw,mkt_p_away,direction,confidence,kickoff_date,final_score,outcome
1292108,26102,40076,0.7016,0.1760,0.1224,home,4,2026-08-12,1-2,A
```

- `mkt_p_*` are **market-implied probabilities** for home / draw / away, derived from publicly quoted pre-kickoff prices and normalised to sum to 1. They are a baseline, not a prediction.
- `direction` is the model's stated lean and may be a single outcome (`home`, `draw`, `away`) or a two-way lean (`home/draw`, `away/draw`).
- `confidence` is the model's own integer scale (1–10), not a probability.
- `outcome` is `H` / `D` / `A` from the final score.

What is deliberately **not** here: training corpora, feature sets, weights, and the internal reasoning text. Those are the parts that are not public. The record of what was claimed and how it turned out is.

## Honest notes on this slice

I would rather state the awkward properties than let someone rediscover them:

1. **Draw rate is 37.9%** (379 of 1,000). That is high against long-run football norms (~26%) and it inflates the difficulty of every baseline computed on this slice. It is a property of this window, not a claim about football.
2. **Market baseline Brier on this slice is 0.6530.** With a uniform 3-way baseline at 0.6667, that is a thin edge — which is exactly what a high-draw window does to a baseline.
3. **`direction` exact-match is 38.9%.** Do not read that as model accuracy: 246 rows carry a two-way lean (`home/draw` or `away/draw`), and a two-way lean is scored as a miss under exact matching. A proper evaluation scores the stated set, not a single label.
4. **157 models, 1,000 rows** — the average model contributes ~6 rows. This slice is not sufficient for per-model inference, and I am not presenting it that way.

Items 1–4 are computed from the file itself (`scripts/verify.py`), so you can reproduce every number.

## Reproducing

```bash
python scripts/verify.py data/graded_predictions.csv
```

It prints row count, outcome distribution, market-baseline Brier, and direction hit rate — the same four numbers quoted above.

## Why publish this at all

A hit-rate number that nobody can recompute is a marketing claim. A file with prediction IDs, timestamps, and results is a falsifiable record. If the platform's stated performance is wrong, this file is how you would find out — so it should be available in the least convenient form for us and the most useful form for you.

## License

Data: **CC BY 4.0** — use it, cite it, train on it.
The schema and scripts: **MIT**.

## Citation

```
SoccerDream AI (2026). SoccerDream AI Graded Prediction Dataset (2026-07 to 2026-10).
https://github.com/SoccerDreamAI/soccerdream-ai-dataset
```

---

Maintained by [SoccerDream AI](https://soccerdreamai.com/insights). Analytics and research content. Not betting advice. 18+
