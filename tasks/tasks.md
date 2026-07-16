# Bio-ML 2026 — Task Overview

OAEI Bio-ML 2026 comprises **Track 1 — Equivalence** over three whole-ontology pairs, evaluating equivalence matching in two complementary settings: a global alignment subtrack and a local ranking subtrack.

| Track | Subtrack | You submit | Headline metric |
|---|---|---|---|
| **Track 1 — Equivalence** | **Subtrack 1 — Global equivalence alignment** | one full OAEI Alignment RDF per pair | repaired, coherence-aware macro-F1 |
| **Track 1 — Equivalence** | **Subtrack 2 — Local equivalence ranking** | a best-first ranking of each query's 100-candidate pool | macro-MRR |

## The three ontology pairs

Every track is evaluated over the same three biomedical ontology pairs:

| Pair | Source → Target | Bridges |
|---|---|---|
| `NCIT-DOID`   | NCIt → DOID       | cancer terminology ↔ human disease |
| `SNOMED-FMA`  | SNOMED CT → FMA   | clinical terms ↔ anatomy |
| `SNOMED-NCIT` | SNOMED CT → NCIt  | clinical terms ↔ cancer terminology |

Scores are **macro-averaged** across the three pairs (each pair weighted equally). Directory names use the uppercase form (`NCIT-DOID`, `SNOMED-FMA`, `SNOMED-NCIT`); URL slugs use the lowercase form (`ncit-doid`, `snomed-fma`, `snomed-ncit`).

## Track 1 — Equivalence

### Subtrack 1 — Global equivalence alignment

| | |
|---|---|
| **Pairs (3)** | NCIT-DOID, SNOMED-FMA, SNOMED-NCIT |
| **You submit** | one full [OAEI Alignment RDF](./global/submission-format.md) per pair (full OWL IRIs, `=` cells) |
| **Setting** | **semi-supervised** — the public `refs_equiv/train.tsv` is released per pair; the **test reference is hidden** |
| **Scored** | organiser-side, against a **repaired, coherence-aware** reference (**headline**), plus **Global Coherence** (reasoner-based) |
| **Metric** | repaired, coherence-aware precision / recall / F1, macro-averaged over the 3 pairs |
| **Details** | [Subtrack 1 — Global Equivalence Alignment](./global/alignment_task_index.md) · [submission format](./global/submission-format.md) |

### Subtrack 2 — Local equivalence ranking

| | |
|---|---|
| **Pairs (3)** | NCIT-DOID, SNOMED-FMA, SNOMED-NCIT |
| **You submit** | one ranking per query: its **100-candidate** pool ordered best-first ([format](./local/submission-format.md)) |
| **Pools** | the gold-stripped `local.test.cands.tsv` per pair — full OWL IRIs, 100 target candidates per source entity |
| **Scored** | organiser-side, against the hidden gold |
| **Metric** | **MRR** + **Hits@{1, 5, 10}**, macro-averaged over the 3 pairs |
| **Details** | [Subtrack 2 — Local Equivalence Ranking](./local/ranking_task_index.md) · [submission format](./local/submission-format.md) |

## Serialisation

Track 1 (both the global alignment and local ranking subtracks) uses **full OWL IRIs** (e.g. `http://purl.obolibrary.org/obo/DOID_1612`) for entity serialisation.

All public `*.test.cands.tsv` files are **gold-stripped** — they carry the candidate pool only, never the answer.

## Data

The datasets and candidate pools are distributed as one Hugging Face dataset, [`OAEI-ML/bio-ml`](https://huggingface.co/datasets/OAEI-ML/bio-ml) (edition tag `2026`); the self-contained `scoring_kit/` (validators + local scorers) ships separately with the [track repository](https://github.com/liseda-lab/OAEI-Bio-ML). Get both, side by side:

```bash
git clone https://github.com/liseda-lab/OAEI-Bio-ML && cd OAEI-Bio-ML   # the scoring kit
hf download OAEI-ML/bio-ml --repo-type dataset --revision 2026 --local-dir ./bio-ml   # the data
```

Under `bio-ml/`, each pair (`NCIT-DOID`, `SNOMED-FMA`, `SNOMED-NCIT`) ships the public equivalence reference `refs_equiv/train.tsv`, the local-ranking pools `local.train.cands.tsv` / `local.valid.cands.tsv` (gold-bearing) plus `local.test.cands.tsv` (gold-stripped); a `repaired/` tree mirrors the same files against the coherence-repaired reference. The download also bundles the **NCIT, DOID and FMA** ontology files; only **SNOMED CT** (for the two SNOMED pairs) is obtained separately — under an Affiliate Licence or by [contacting us](mailto:contact@oaei-ml.org) for a research-only copy (see [ontologies](../ontologies/ontologies.md)). Run `python scoring_kit/self_check.py --data ./bio-ml` to confirm the data downloaded intact.

## Key dates

| Date | Milestone |
|---|---|
| 2026-07-06 | provisional materials |
| 2026-07-07 | datasets finalised |
| **2026-07-12** | **competition starts — leaderboards open** |
| 2026-09-01 | evaluation closes |
| 2026-09-06 | competition ends — results published (grace period to 2026-09-12) |

Participant results are collected and ranked on **two CodaBench competitions** — one per subtrack (Track 1 global alignment, Track 1 local ranking). Competition URLs are announced at launch.
