# Subtrack 2 — Local Ranking: Submission Format

For each query in a pair's `local.test.cands.tsv`, your system submits one **ranking of that query's 100 candidates**, best-first. See the [Subtrack 2 task description](./ranking_task_index.md) for the setting and metrics.

Candidates are **full OWL IRIs** (Track 1 serialisation). The scorer aligns submissions to pools by the source entity, and every candidate in a query's pool must appear exactly once in your ranking (the validator rejects a ranking that is not a permutation of the pool).

## Two accepted TSV encodings

`validate_ranking.py` and `score_local.py` accept either encoding; pick whichever your pipeline emits.

### LIST format — one row per query

A tab-separated file with a header `SrcEntity` and `RankedCandidates`, where `RankedCandidates` is a JSON array of all 100 pool IRIs ordered best-first:

```tsv
SrcEntity	RankedCandidates
http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3262	["http://purl.obolibrary.org/obo/DOID_162", "http://purl.obolibrary.org/obo/DOID_1612", "..."]
```

### BLOCK format — one row per candidate

A tab-separated file with a header `SrcEntity`, `TgtCandidate`, `Score`, holding **100 rows per query** (one per candidate). The scorer groups rows by `SrcEntity` and ranks each block by **descending `Score`**:

```tsv
SrcEntity	TgtCandidate	Score
http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3262	http://purl.obolibrary.org/obo/DOID_162	0.98
http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3262	http://purl.obolibrary.org/obo/DOID_1612	0.41
...98 more rows for this source entity...
```

Both encodings express the same thing: a total order over each query's 100 candidates. In LIST form you commit to the order directly; in BLOCK form the order is induced by the scores (ties are broken by the scorer deterministically).

## Worked example

Given a query whose gold target is `http://purl.obolibrary.org/obo/DOID_162`, a strong system ranks it first. In LIST form:

```tsv
SrcEntity	RankedCandidates
http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3262	["http://purl.obolibrary.org/obo/DOID_162", "http://purl.obolibrary.org/obo/DOID_1612", "..."]
```

Because the gold is at position 1, this query contributes Hits@1 = Hits@5 = Hits@10 = 1 and reciprocal rank 1.0.

## Validate (participant) — scoring is organiser-side

The official gold is private, so you validate the format and submit; the organisers score. `validate_ranking.py` checks that every query in the pool is present and that each ranking is a permutation of its 100-candidate pool:

```bash
python scoring_kit/validate_ranking.py  bio-ml/NCIT-DOID/local.test.cands.tsv  my_ncit-doid.tsv
```

To estimate MRR / Hits@k before submitting, self-score against the gold-bearing validation pool (`local.valid.cands.tsv` doubles as the gold TSV — its `SrcEntity` / `TgtEntity` columns are the answer):

```bash
python scoring_kit/score_local.py  my_dev_ranking.tsv  bio-ml/NCIT-DOID/local.valid.cands.tsv
```
