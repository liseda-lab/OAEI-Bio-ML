# Submission format — Track 2 (Mixed equivalence + subsumption typed ranking)

For each query you are given a frozen pool of **100 candidate targets**
(`track2.<split>.cands.tsv`). Score **every (candidate, relation) pair** — the three
relations are `equivalent`, `source_subsumed_by_target`, `source_subsumes_target` — so a
query contributes **300 rows** (100 candidates × 3 relations). Entities are **CURIEs**
(e.g. `NCIT:C101044`, `DOID:DOID_0080073`, `SNOMED:10013000`, `FMA:fma44631`).

## Format (BLOCK)

| column | meaning |
|---|---|
| `SrcEntity` | the query source CURIE |
| `TgtEntity` | a candidate target CURIE |
| `Relation` | one of `equivalent` / `source_subsumed_by_target` / `source_subsumes_target` |
| `Score` | your confidence for this (target, relation) — used to rank |

```
SrcEntity	TgtEntity	Relation	Score
NCIT:C101029	DOID:DOID_13088	equivalent	0.91
NCIT:C101029	DOID:DOID_13088	source_subsumed_by_target	0.04
NCIT:C101029	DOID:DOID_13088	source_subsumes_target	0.02
…   (300 rows for this query, then the next query's 300 rows) …
```

## Rules
- **Positional**: emit each query's 300-row block in the **same order** as the pool file
  (`QueryID` is recovered by position — public `track2.test.cands.tsv` drops `QueryID`).
- Every one of the 100 pool candidates must appear once with **each** of the 3 relations.
- Self-scoreable on **train/valid** (gold answers public); **test** gold is held back.

## Metrics
- **Preferred Typed-MRR** — the rank of the single *preferred* gold (target, relation) per
  query (preference order: `equivalent` > `source_subsumed_by_target` > `source_subsumes_target`).
- **Hierarchy-aware Typed-nDCG@10** — graded relevance: exact pair 1.0, same-entity
  subsumption directions 0.6, hierarchical partial credit decaying by 1/(d+1) out to distance 3.
- Both are also reported sliced to equivalence-only and subsumption-only queries.

## Validate & self-score
```bash
python3 validate_typed.py track2.test.cands.tsv my_typed.tsv          # structural: 300/query, pool coverage
python3 score_typed.py    my_typed.tsv track2.valid.answers.tsv \
        --preferred track2.valid.preferred.tsv --graded track2.valid.graded.tsv
```
