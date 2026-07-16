# Changelog

Notable changes to the OAEI Bio-ML datasets, baselines, and published results are recorded here, per edition.

## 2026 edition (first edition)

### 2026-07-16 — Ontology files added to the download

The Hugging Face dataset now bundles the **NCIT, DOID, and FMA** ontology files alongside the task data, so participants no longer obtain those three separately. **SNOMED CT** remains licence-restricted and is not redistributed: obtain it under a SNOMED CT Affiliate Licence, or contact the organisers (<contact@oaei-ml.org>) for a copy strictly for research purposes. See [ontologies](./ontologies/ontologies.md).

### 2026-07-07 — Finalised datasets published

The 2026 datasets are frozen and distributed on the Hugging Face Hub as [`OAEI-ML/bio-ml`](https://huggingface.co/datasets/OAEI-ML/bio-ml) (edition tag `2026`): the per-pair equivalence reference (`refs_equiv/train.tsv`), the local-ranking candidate pools (with gold-stripped test splits), and a `repaired/` tree against the coherence-repaired reference. The Hugging Face dataset is data only; the self-contained `scoring_kit/` ships separately with the [track repository](https://github.com/liseda-lab/OAEI-Bio-ML). Two CodaBench competitions (Track 1 Global Alignment, Track 1 Local Ranking) open on 12 July 2026; the evaluation window runs 12 July – 30 September 2026.

### 2026-07-06 — Provisional materials released

Provisional website, task documentation, and datasets made public for review, together with the organiser-run baselines on the [baselines page](./BASELINES.md).

## Entry format for future editions

From the 2027 edition onward, entries will record, relative to the previous edition:

- **Dataset changes** — ontology version bumps, reference additions/removals/repairs (with correspondence counts), candidate-pool regeneration, and new dataset revisions.
- **Protocol changes** — metric, validation, or submission-format changes.
- **Results** — a pointer to the closed edition's final archived results.
