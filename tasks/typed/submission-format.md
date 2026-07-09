# Track 2 — Typed Ranking: Submission Format

For each query in a pair's `track2.test.cands.tsv`, your system scores **all 300 typed hypotheses** — 100 candidates × 3 relations — for that query. See the [Track 2 task description](./typed_task_index.md) for the setting and metrics.

Track 2 uses **CURIEs** (e.g. `NCIT:C101044`), **not** full OWL IRIs. The three relations are, verbatim:

* `equivalent`
* `source_subsumed_by_target`
* `source_subsumes_target`

## The pool file (gold-stripped)

Each query contributes 300 rows to `track2.test.cands.tsv` — every `(SrcEntity, TgtCandidate, Relation)` hypothesis, with the answer removed:

```tsv
SrcEntity	TgtCandidate	Relation
NCIT:C101044	DOID:0050686	equivalent
NCIT:C101044	DOID:0050686	source_subsumed_by_target
NCIT:C101044	DOID:0050686	source_subsumes_target
NCIT:C101044	DOID:1240	equivalent
...296 more rows for this source entity...
```

## Submission format — score every hypothesis

Return the same rows with a `Score` column added: a tab-separated file with header `SrcEntity`, `TgtCandidate`, `Relation`, `Score`. Emit **all 300 rows per query** — one score per typed hypothesis. The scorer ranks each query's 300 hypotheses by **descending `Score`** (ties broken deterministically), then reads off the rank of the preferred hypothesis and the graded relevance of the top-10.

```tsv
SrcEntity	TgtCandidate	Relation	Score
NCIT:C101044	DOID:0050686	equivalent	0.91
NCIT:C101044	DOID:0050686	source_subsumed_by_target	0.12
NCIT:C101044	DOID:0050686	source_subsumes_target	0.05
NCIT:C101044	DOID:1240	equivalent	0.40
...296 more rows for this source entity...
```

`Score` is a real number; only the induced order within each query matters (scores are not compared across queries). Every `(TgtCandidate, Relation)` pair present in the pool must be scored exactly once; the validator rejects a submission with missing, extra, or duplicated hypotheses, or an unknown relation label.

## Worked example

If the preferred (gold) answer for query `NCIT:C101044` is `(DOID:0050686, equivalent)`, then the scores above rank it first among the 300 hypotheses — contributing Preferred Typed-Hits@1 = 1 and preferred reciprocal-rank 1.0. A candidate scored high on `source_subsumed_by_target` for a hierarchically-near target still earns partial Hierarchy-aware Typed-nDCG@10 credit even when it is not the preferred hypothesis.

## Template

```tsv
SrcEntity	TgtCandidate	Relation	Score
<src-CURIE>	<cand-CURIE>	equivalent	<score>
<src-CURIE>	<cand-CURIE>	source_subsumed_by_target	<score>
<src-CURIE>	<cand-CURIE>	source_subsumes_target	<score>
...300 rows per query, one block per source entity...
```

## Validate (participant) — scoring is organiser-side

The official answers are private, so you validate the format and submit; the organisers score. `validate_typed.py` checks that every query is present and that all 300 typed hypotheses are scored exactly once:

```bash
python scoring_kit/validate_typed.py  bio-ml/NCIT-DOID/track2.test.cands.tsv  my_ncit-doid.tsv
```

To estimate the metrics before submitting, `score_typed.py` takes your submission plus the public validation answer keys — the `answers` pool, a `preferred` file (the gold `(candidate, relation)` per query), and a `graded` file (hierarchy relevance per hypothesis):

```bash
python scoring_kit/score_typed.py  my_dev_sub.tsv  bio-ml/NCIT-DOID/track2.valid.answers.tsv  --preferred bio-ml/NCIT-DOID/track2.valid.preferred.tsv  --graded bio-ml/NCIT-DOID/track2.valid.graded.tsv
```
