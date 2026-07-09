# Subtrack 2 — Local Equivalence Ranking

_The candidate-ranking setting of Bio-ML 2026 (Track 1 — Equivalence)._

For each **query** — one source entity — you are given a fixed **pool of 100 candidate target entities** (full OWL IRIs) drawn from the target ontology. Your system re-orders that pool so that the true equivalent target appears as early as possible. Participants do **not** generate candidates; they rank the ones we provide.

## The three ontology pairs

| Pair | Source → Target | Test queries |
|---|---|--:|
| `NCIT-DOID`   | NCIt → DOID       | 1,819 |
| `SNOMED-FMA`  | SNOMED CT → FMA   | 3,414 |
| `SNOMED-NCIT` | SNOMED CT → NCIt  | 10,911 |

The score is **macro-averaged** across the three pairs (each pair weighted equally).

## The candidate pools

Each pair's pools live in `local.test.cands.tsv` inside the [`OAEI-ML/bio-ml`](https://huggingface.co/datasets/OAEI-ML/bio-ml) dataset. Every query pins **100 candidates** — the (hidden) gold target plus hard negatives sampled from the target ontology's signature. The public file is **gold-stripped**: it carries only the source entity and its candidate pool, never the answer. Candidates are **full OWL IRIs** (e.g. `http://purl.obolibrary.org/obo/DOID_1612`), consistent with the rest of Track 1.

## A semi-supervised setting

The public equivalence correspondences (`refs_equiv/train.tsv`) and the gold-bearing local pools (`local.train.cands.tsv`, `local.valid.cands.tsv`) may be used as (distant) supervision for building or tuning a ranker. The **test pools are gold-stripped and scored organiser-side**: you validate your ranking's format, submit it, and the organisers score it against the hidden gold. Because a per-pair gold target exists for every query, there is **no NIL / abstention candidate** in Bio-ML 2026 — every query has exactly one correct target somewhere in its pool.

## Metrics

* **Mean Reciprocal Rank (MRR)**
* **Hits@k** for $k \in \{1, 5, 10\}$

Writing $\mathrm{rank}(q)$ for the 1-based position of the gold target in your ranking of query $q$'s pool,

$$
\mathrm{Hits@}k = \frac{1}{\vert Q \vert} \sum_{q \in Q} \mathbb{1}[\mathrm{rank}(q) \leq k], \qquad
\mathrm{MRR} = \frac{1}{\vert Q \vert} \sum_{q \in Q} \frac{1}{\mathrm{rank}(q)}.
$$

Each metric is computed per pair, then **macro-averaged** over the three pairs. The headline is macro-MRR.

## Leaderboard columns

Results are published to the Track 1 — Local Ranking CodaBench leaderboard, with columns `macro_mrr` (headline), `macro_hits_at_1`, `macro_hits_at_5`, `macro_hits_at_10`, and the per-pair `mrr_<pair>` / `hits_at_1_<pair>`. Organiser baseline numbers are on the [baselines page](../../BASELINES.md).

## Validating & scoring

* Validation needs only Python 3.12+ (standard library): `scoring_kit/validate_ranking.py`.
* The official test gold is private — participants do not score their own official submission; the organisers do.
* You may self-score on the gold-bearing validation pool (`local.valid.cands.tsv`, whose `TgtEntity` column is the gold) with `scoring_kit/score_local.py` to estimate MRR / Hits@k before submitting.

```bash
# structural check: every query present, each ranking a permutation of its 100-candidate pool
python scoring_kit/validate_ranking.py  bio-ml/NCIT-DOID/local.test.cands.tsv  my_ncit-doid.tsv
```

Exact submission spec + worked example: [Subtrack 2 submission format](./submission-format.md).
