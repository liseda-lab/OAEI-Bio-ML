# Quickstart

This guide takes you from an empty directory to a validated (and, where possible, self-scored) submission. Everything the scoring kit runs is Python 3.10+ standard library only.

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

* `refs_equiv/train.tsv` and `refs_equiv/valid.tsv` — the public equivalence reference for global alignment (`SrcEntity`, `TgtEntity`, `Score`, `Relation`; full IRIs; semi-supervised setting), drawn from the **repaired** reference the headline metric scores against,
* `local.train.cands.tsv` / `local.valid.cands.tsv` — the local-ranking pools that **carry the gold** `TgtEntity` (use them to self-score), and `local.test.cands.tsv` — the **gold-stripped** test pool (source entity + candidate list only).

Local ranking is scored against the **standard** (unrepaired) reference; coherence repair applies to the global alignment task only.

The download also bundles the **NCIT, DOID and FMA** ontology files alongside the task data, so for the `NCIT-DOID` pair there is nothing more to fetch. The one exception is **SNOMED CT** (needed for `SNOMED-FMA` and `SNOMED-NCIT`), which we cannot redistribute: obtain it under a [SNOMED CT Affiliate Licence](https://www.snomed.org/) or [contact us](mailto:contact@oaei-ml.org) for a copy strictly for research purposes (see [ontologies](./ontologies/ontologies.md)). The `scoring_kit/` used below is the one you cloned in step 1a.

## 2. Sanity-check your copy

Run the self-check against your downloaded data before you do anything else — it builds an oracle ranking from each pair's `local.valid.cands.tsv` and confirms it scores perfectly:

```bash
python3 scoring_kit/self_check.py --data ./bio-ml
```

## 3. Subtrack 1 — Global equivalence alignment

For each pair, produce one alignment file using **full OWL IRIs**. The setting is **semi-supervised**: `refs_equiv/train.tsv` and `refs_equiv/valid.tsv` are public for training and tuning, but the test reference is hidden and scored organiser-side (there is no public global scorer). Validate the structure locally before submitting:

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

The evaluation window ran from 12 July to 30 September 2026 (00:00 Anywhere on Earth) and is now closed. Each scored subtrack has its own CodaBench competition:

* Subtrack 1 — Global equivalence alignment — **[open on CodaBench](https://www.codabench.org/competitions/17424/)**,
* Subtrack 2 — Local equivalence ranking — **[open on CodaBench](https://www.codabench.org/competitions/17423/)**.

**Before you submit:** as with every OAEI track, your system must be registered with the [OAEI 2026 campaign](https://oaei.ontologymatching.org/2026/) via its [registration form](https://docs.google.com/forms/d/e/1FAIpQLSdGMuD_-kWhCYQIK5amsCvMDmYICViUJEci-M1CySoMaJ0wqA/viewform); a CodaBench account alone is not OAEI registration.

Register on the relevant competition, then upload your submission as described on its Overview page. Package it as one zip per competition with one file per pair, each filename containing the **hyphenated** pair slug (`ncit-doid`, `snomed-fma`, `snomed-ncit`), and build the zip from the command line (`zip -X -j submission.zip ncit-doid.rdf snomed-fma.rdf snomed-ncit.rdf`) — on macOS avoid Finder's *Compress*, which adds hidden `__MACOSX` files the scorer can read instead of yours. If a submission scores `0.000` on every pair, see [submission support](./support.md). Results are published as *provisional* to the leaderboard; organisers verify, reproduce where possible, and mark accepted results alongside the organiser-run [baselines](./BASELINES.md).
