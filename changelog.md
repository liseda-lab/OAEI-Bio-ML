# Changelog

Notable changes to the OAEI Bio-ML datasets, baselines, and published results are recorded here, per edition.

## 2026 edition (first edition)

### 2026-08-01 — Public reference aligned to the basis it is scored on

Two changes to the Hugging Face dataset, both bringing the published files into line with how submissions are actually evaluated. **No submission format, metric, or scoring behaviour changes**, and no previously-private data is disclosed.

**Global alignment — `refs_equiv` matches the repaired reference, and `valid` is published.** The headline metric scores against the coherence-repaired reference. The public validation split is now released as `refs_equiv/valid.tsv` alongside train; its positives were already public inside `local.valid.cands.tsv`, so nothing new is exposed. Per-pair positives, train / valid: NCIT-DOID 3,262 / 530 (was 3,845 train), SNOMED-FMA 3,239 / 541 (was 6,817), SNOMED-NCIT 17,283 / 2,864 (was 21,669). The reference split is 60 / 10 / 30 train / valid / test; the test slice remains private.

**Local ranking — the `repaired/` pools have been removed.** The per-pair `repaired/` trees (`local.{train,valid,test}.cands.tsv` against the repaired reference) are gone. Local ranking is evaluated against the **standard** (unrepaired) reference throughout — in the released pools, on the CodaBench leaderboard, and in the organiser baselines — so the repaired variant was unused, and shipping it invited the reading that ranking was scored on the repaired basis. Coherence repair applies to **global** alignment only. Participants who downloaded a `repaired/` directory can discard it.

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
