# Track 2 — Mixed Equivalence + Subsumption Typed Ranking

_Equivalence and subsumption evaluated together, as a single typed ranking problem._

Track 2 asks not only **which** target entity a source entity relates to, but **how**. For each **query** — one source entity — you are given a pool of **100 candidate target entities**, and for every candidate three **relation hypotheses**:

* `equivalent` — the source is equivalent to the candidate,
* `source_subsumed_by_target` — the source is a sub-class of the candidate,
* `source_subsumes_target` — the source is a super-class of the candidate.

That gives **300 typed hypotheses per query** (100 candidates × 3 relations). Your system assigns a score to each, and the pool is ranked by those scores. Exactly one typed hypothesis is the **preferred** (gold) answer; the others are graded by how close they sit in the hierarchy.

## The three ontology pairs

| Pair | Source → Target | Test queries |
|---|---|--:|
| `NCIT-DOID`   | NCIt → DOID       | 3,556 |
| `SNOMED-FMA`  | SNOMED CT → FMA   | 6,114 |
| `SNOMED-NCIT` | SNOMED CT → NCIt  | 19,954 |

The score is **macro-averaged** across the three pairs (each pair weighted equally).

## The candidate pools

Each pair's pools live in `track2.test.cands.tsv` inside the [`OAEI-ML/bio-ml`](https://huggingface.co/datasets/OAEI-ML/bio-ml) dataset. Track 2 uses **CURIEs** (e.g. `NCIT:C101044`), **not** the full OWL IRIs of Track 1. The public file is **gold-stripped**: it lists the 300 `(source, candidate, relation)` hypotheses per query but never marks which one is preferred. The public Track 2 training and validation answer keys (`track2.train.answers.tsv` / `track2.valid.answers.tsv`, with their `.preferred.tsv` and `.graded.tsv` files) and the equivalence reference `refs_equiv/train.tsv` are available as (distant) supervision.

## Metrics

**Preferred Typed-MRR (headline).** Rank all 300 typed hypotheses of a query by your score; find the 1-based position of the single **preferred** (gold) `(candidate, relation)` hypothesis. The reciprocal-rank of that position, averaged over queries, is Preferred Typed-MRR. The companion Preferred Typed-Hits@{1, 5, 10} report how often the preferred hypothesis lands in the top 1 / 5 / 10.

$$
\text{Preferred Typed-MRR} = \frac{1}{\vert Q \vert} \sum_{q \in Q} \frac{1}{\mathrm{rank}(q_{\text{preferred}})}.
$$

**Hierarchy-aware Typed-nDCG@10.** A graded metric: hypotheses that are wrong on the exact relation but *hierarchically close* (e.g. predicting a subsumption where equivalence holds, or naming an ancestor of the true target) earn partial relevance, discounted by rank and truncated at 10. This rewards systems whose top-10 is hierarchically sensible even when the exact preferred hypothesis is not rank 1.

Both are computed per pair and **macro-averaged** over the three pairs. Scores are also reported over the `equivalence-only` and `subsumption-only` slices of the queries.

## Leaderboard columns

Results are published to the Track 2 — Typed Ranking CodaBench leaderboard, with columns `macro_preferred_typed_mrr` (headline), `macro_hnDCG_at_10`, `macro_preferred_typed_hits_at_1` / `_5` / `_10`, and the per-pair `preferred_typed_mrr_<pair>` / `hnDCG_at_10_<pair>`. Organiser baseline numbers are on the [baselines page](../../BASELINES.md).

## Validating & scoring

* Validation needs only Python 3.12+ (standard library): `scoring_kit/validate_typed.py`.
* The official test answers (preferred relation + hierarchy-graded relevance) are private and scored organiser-side.
* You may self-score on the public validation answer keys (`track2.valid.answers.tsv` + `.preferred.tsv` / `.graded.tsv`) with `scoring_kit/score_typed.py` to estimate the metrics before submitting.

```bash
# structural check: every query present, all 300 typed hypotheses scored
python scoring_kit/validate_typed.py  bio-ml/NCIT-DOID/track2.test.cands.tsv  my_ncit-doid.tsv
```

Exact submission spec + worked example: [Track 2 submission format](./submission-format.md).
