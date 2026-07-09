# Submission format — Track 1 / Subtrack 2 (Local equivalence ranking)

For each query source class you are given a frozen pool of **100 candidate targets** (`local.<split>.cands.tsv`). Rank each pool best-first. Entities are **full OWL IRIs**.

## Two accepted layouts (submit either)

**LIST form** (natural — re-order the pool you were given):

| column | meaning |
|---|---|
| `SrcEntity` | the query source IRI |
| `TgtCandidates` | a Python-list literal of the 100 candidate IRIs, **best first** |

```
SrcEntity	TgtCandidates
http://…#C101029	['http://purl.obolibrary.org/obo/DOID_0050651', 'http://…', …]   # 100 IRIs
```

**BLOCK form**:

| column | meaning |
|---|---|
| `SrcEntity`, `TgtEntity` | one candidate per row |
| `Score` (optional) | if present, rows are sorted by descending score |

100 consecutive rows per query.

## Rules

- **Positional**: keep your queries in the **same order** as the pool file — the scorer pairs submission query *i* with pool query *i*. A source may appear more than once.
- Each query's ranking must be a **permutation of that query's 100 pool candidates**.
- You may self-score the **train/valid** splits (their gold is public); the **test** gold is held back (`local.test.cands.tsv` is gold-stripped: `SrcEntity`, `TgtCandidates` only).

## Metrics

**MRR + Hits@{1,5,10}** — the reciprocal rank of the gold target in your ranking.

## Validate & self-score

```bash
python3 validate_ranking.py local.test.cands.tsv  my_ranking.tsv      # structural + permutation
python3 score_local.py      my_ranking.tsv  local.valid.cands.tsv     # MRR/Hits on the valid split
```
`local.valid.cands.tsv` works directly as the gold file (its `SrcEntity`/`TgtEntity` columns are the gold; other columns are ignored).
