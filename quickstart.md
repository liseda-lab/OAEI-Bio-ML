# Quickstart

This guide takes you from an empty directory to a validated (and, where possible, self-scored) submission. Everything the scoring kit runs is Python 3.12+ standard library only.

## 1. Get the scoring kit and the data

The **scoring kit** (validators + self-scorers) and the **task data** come from two places: the kit ships with the track's GitHub repository, and the data is published on the Hugging Face Hub. Get both, side by side:

```bash
# 1a. the scoring kit — clone (or download) the track repository
git clone https://github.com/liseda-lab/OAEI-Bio-ML
cd OAEI-Bio-ML

# 1b. the task data — download the Hugging Face dataset into ./bio-ml
pip install -U huggingface_hub
hf download OAEI-ML/bio-ml --repo-type dataset --revision 2026 --local-dir ./bio-ml
```

The 2026 task data is **publicly available** under the OAEI-ML organisation — [`huggingface.co/datasets/OAEI-ML/bio-ml`](https://huggingface.co/datasets/OAEI-ML/bio-ml), edition tag `2026` — and downloads freely, without gating (entity IRIs only). Under `bio-ml/`, each pair (`NCIT-DOID`, `SNOMED-FMA`, `SNOMED-NCIT`) contains:

* `refs_equiv/train.tsv` — the public equivalence training reference for global alignment (`SrcEntity`, `TgtEntity`, `Score`; full IRIs; semi-supervised setting),
* `local.train.cands.tsv` / `local.valid.cands.tsv` — the local-ranking pools that **carry the gold** `TgtEntity` (use them to self-score), and `local.test.cands.tsv` — the **gold-stripped** test pool (source entity + candidate list only),
* `repaired/` — the same set of files scored against the coherence-repaired reference.

The download also bundles the **NCIT, DOID and FMA** ontology files alongside the task data, so for the `NCIT-DOID` pair there is nothing more to fetch. The one exception is **SNOMED CT** (needed for `SNOMED-FMA` and `SNOMED-NCIT`), which we cannot redistribute: obtain it under a [SNOMED CT Affiliate Licence](https://www.snomed.org/) or [contact us](mailto:contact@oaei-ml.org) for a copy strictly for research purposes (see [ontologies](./ontologies/ontologies.md)). The `scoring_kit/` used below is the one you cloned in step 1a.

## 2. Sanity-check your copy

Run the self-check against your downloaded data before you do anything else — it builds oracle submissions from the public splits and confirms they score perfectly:

```bash
python3 scoring_kit/self_check.py --data ./bio-ml
```

## 3. Subtrack 1 — Global equivalence alignment

For each pair, produce one alignment file using **full OWL IRIs**. The setting is **semi-supervised**: `refs_equiv/train.tsv` is public for tuning, but the test reference is hidden and scored organiser-side (there is no public global scorer). Validate the structure locally before submitting:

```bash
python3 scoring_kit/validate_global.py my-ncit-doid.rdf
```

Submissions are scored against the **repaired, coherence-aware** reference, plus reasoner-checked Global Coherence - see [evaluation metrics](./evaluation-metrics.md).

## 4. Subtrack 2 — Local equivalence ranking

For each pair, read the gold-stripped candidate pools in `bio-ml/<PAIR>/local.test.cands.tsv` and emit a ranking of each query's candidates, best-first. Validate the format against the pool, then self-score on the gold-bearing validation pool (`local.valid.cands.tsv`, whose `TgtEntity` column is the gold — usable directly):

```bash
python3 scoring_kit/validate_ranking.py bio-ml/NCIT-DOID/local.test.cands.tsv my-ranking.tsv
python3 scoring_kit/score_local.py my-ranking.tsv bio-ml/NCIT-DOID/local.valid.cands.tsv
```

Local ranking is scored with **MRR** and **Hits@{1,5,10}**, macro-averaged over the three pairs.

## 5. Submit

The evaluation window runs from 12 July to 30 September 2026 (00:00 Anywhere on Earth). Each scored subtrack has its own CodaBench competition:

* Subtrack 1 — Global equivalence alignment — **[open on CodaBench](https://www.codabench.org/competitions/17424/)**,
* Subtrack 2 — Local equivalence ranking — **[open on CodaBench](https://www.codabench.org/competitions/17423/)**.

Register on the relevant competition, then upload your submission as described on its Overview page. Results are published as *provisional* to the leaderboard; organisers verify, reproduce where possible, and mark accepted results alongside the organiser-run [baselines](./BASELINES.md).
