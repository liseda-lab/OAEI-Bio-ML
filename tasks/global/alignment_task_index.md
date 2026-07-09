# Subtrack 1 — Global Equivalence Alignment

_The traditional, whole-ontology alignment setting of Bio-ML 2026 (Track 1 — Equivalence)._

For each of the three ontology pairs you submit **one complete equivalence alignment** between the source and target ontologies, in the [OAEI Alignment RDF format](https://moex.gitlabpages.inria.fr/alignapi/format.html), using **full OWL IRIs**. Submissions are scored **organiser-side** against a hidden test reference; the headline number is the **repaired, coherence-aware** F1, with a reasoner-based **Global Coherence** figure reported alongside.

## The three ontology pairs

| Pair | Source → Target | Reference used for scoring |
|---|---|---|
| `NCIT-DOID`   | NCIt → DOID       | repaired (headline) + standard |
| `SNOMED-FMA`  | SNOMED CT → FMA   | repaired (headline) + standard |
| `SNOMED-NCIT` | SNOMED CT → NCIt  | repaired (headline) + standard |

The **source ontologies are not re-hosted** in the [`OAEI-ML/bio-ml`](https://huggingface.co/datasets/OAEI-ML/bio-ml) dataset — obtain each from its original publisher (see the [ontologies](../../ontologies/ontologies.md) page and the dataset's own `ontologies.md`).

## A semi-supervised setting

The equivalence reference is split **source-stratified 60 / 10 / 30** into train / validation / test. The **public training slice** is released as `refs_equiv/train.tsv` (one `SrcEntity`, `TgtEntity`, `Score` correspondence per line, full IRIs); the **validation and test slices are held back** and scored organiser-side. You may train, tune, and threshold on the public correspondences however you like; you then submit a full alignment over the two ontologies, and the organisers score the portion that falls on the hidden test entities.

Because the test reference is hidden, Subtrack 1 is **scored organiser-side**. Participants validate their submission's format locally (see [submission format](./submission-format.md)) and submit; the leaderboard reports the scores.

## Two references, two semantics

The gold equivalence reference is derived from UMLS/Mondo and is therefore, as published, potentially **logically incoherent**. Every submission is scored against **two** views of it:

**Standard reference — traditional P/R/F1.** The complete (possibly-incoherent) reference, scored with ordinary set-based precision, recall and F1 over equivalence correspondences.

**Repaired reference — coherence-aware, relation-agnostic P/R/F1 (headline).** The reference after mapping repair. Correspondences that repair fully removed are annotated `?` and are **ignored from both the precision and the recall denominators** (they neither help nor hurt). Correspondences that repair *weakened* rather than removed survive as subsumption (`<` / `>`), and are **credited relation-agnostically** — a reference `<` or `>` is satisfied by a predicted correspondence of **any** relation between the same entities. This is the **headline** metric.

$$
\mathrm{Precision} = \frac{\vert A \cap R^{+} \vert}{\vert A \setminus R^{?} \vert}, \qquad
\mathrm{Recall} = \frac{\vert A \cap R^{+} \vert}{\vert R^{+} \vert}, \qquad
\mathrm{F1} = \frac{2\,\mathrm{P}\,\mathrm{R}}{\mathrm{P} + \mathrm{R}},
$$

where $R^{+}$ are the surviving (credited) reference correspondences and $R^{?}$ the `?`-flagged ones removed from both denominators. Both P/R/F1 sets are **macro-averaged** across the three pairs.

### How the repaired reference was constructed

Repair follows the LargeBio "remove-if-any" convention, computed as the **union of removed** across three established repair tools — **ALCOMO** (run under the ELK reasoner), **LogMap-repair**, and **AML-repair**. A correspondence is dropped (annotated `?`) if **any** of the three removes it; where LogMap merely *weakens* an equivalence to a subsumption, the weakened `<` / `>` is kept (subsumption takes priority). `owl:deprecated` correspondences are out-of-task and dropped from both the reference and the predictions before scoring. Full construction detail is deferred to the supplementary materials (available at track launch).

## Global Coherence

Alongside P/R/F1, each submitted alignment is checked for the **logical incoherence it induces** when merged with the two ontologies. A reasoner computes `global_coherence` — the degree of incoherence in $[0, 1]$ (lower is better) — together with the number of unsatisfiable classes and the size of the merged class set. Because it requires a reasoner, Global Coherence is computed **organiser-side only**; it is never part of the participant-side kit.

## Scoring and leaderboard columns

Subtrack 1 is scored organiser-side and published to the Track 1 — Global Alignment CodaBench leaderboard. Its columns are `macro_f1_repaired` (headline), `macro_precision_repaired`, `macro_recall_repaired`, `macro_f1_standard`, `global_coherence`, and the per-pair `f1_repaired_<pair>`. Organiser baseline numbers are on the [baselines page](../../BASELINES.md).

For the exact file shape, a worked example, a copy-paste template, and local validation, see the [submission format](./submission-format.md).
