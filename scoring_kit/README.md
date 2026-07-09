# BioML 2026 — Scoring Kit

A **self-contained, zero-install** kit to validate and self-score your BioML 2026 submissions with the *same* code the official leaderboard uses. Requires only **Python 3.10+** (standard library — no `pip install`, no internet).

`oaei_bioml_eval/` here is a vendored snapshot of the organiser's scorer, so your local numbers match the leaderboard. (Coherence is reasoner-based and scored organiser-side; it is not part of this kit.)

## Tasks (canonical names — see `docs/nomenclature.md`)

| Task | Submission | Entities | Self-score? | Metrics |
|---|---|---|---|---|
| **Subtrack 1** — Global equivalence alignment | OAEI Alignment **RDF**, one per pair | full **IRIs** | no (test gold private) | P/R/F1 (standard + repaired) + Global Coherence |
| **Subtrack 2** — Local equivalence ranking | **TSV** (`local.*` layout) | full **IRIs** | yes, on train/valid | MRR + Hits@{1,5,10} |

Public `*.test.cands.tsv` are gold-stripped and the scorer recovers query order **positionally** — keep your submission's queries in the pool's order.

## Quickstart

```bash
# 0) prove the kit + your downloaded data are self-consistent (oracle -> perfect scores)
python3 self_check.py --data /path/to/bio-ml            # the public dataset dir (per-pair subdirs)

# 1) VALIDATE before you submit
python3 validate_global.py   my_alignment.rdf                              # Subtrack 1
python3 validate_ranking.py  NCIT-DOID/local.test.cands.tsv my_ranking.tsv # Subtrack 2

# 2) SELF-SCORE on the valid split (public gold), to estimate your number
python3 score_local.py  my_ranking.tsv NCIT-DOID/local.valid.cands.tsv
```

The official test scores are computed organiser-side (the test gold, the UMLS-derived evidence, and the reasoner-based coherence are never released). Full per-task submission formats are in `docs/submission-format-*.md`.

## Files
- `validate_global.py` / `validate_ranking.py` / `validate_typed.py` — format checkers (stdlib).
- `score_local.py` / `score_typed.py` — self-scorers over the vendored official scorer.
- `self_check.py` — gate: builds oracle submissions from your valid data and confirms perfect scores.
- `alignment.rng` — optional RelaxNG schema for the global Alignment RDF.
- `oaei_bioml_eval/` — vendored official metric core (pure stdlib; local + typed).
- `docs/` — per-task submission formats and terminology.
