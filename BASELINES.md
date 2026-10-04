# OAEI Bio-ML — Baselines

These are the organiser-run baseline systems, published before the competition; participant submissions are not added to these tables. The exact scores are rendered directly from the machine-readable `leaderboard.json` on the **[baselines page](https://liseda-lab.github.io/OAEI-Bio-ML/baselines/)** of the website, so the numbers here never drift from the data. The final participant results are on the [results page](https://liseda-lab.github.io/OAEI-Bio-ML/results/). Changes between editions are recorded in the [changelog](./changelog.md); OAEI Bio-ML 2026 is the first edition, so there are no previous years yet.

All baseline scores are **macro-averaged over the three pairs** (NCIT–DOID, SNOMED–FMA, SNOMED–NCIT).

## Subtrack 1 — Global equivalence alignment

Scored with **repaired, coherence-aware P/R/F1** (headline). Baseline systems include a naive lexical matcher, LogMap and LogMapLt, AML, and the BERTMap family. See the [baselines page](https://liseda-lab.github.io/OAEI-Bio-ML/baselines/) for the full table and the [evaluation metrics](./evaluation-metrics.md) for the standard-vs-repaired distinction (the two references are **not directly comparable**).

## Subtrack 2 — Local equivalence ranking

Scored with **MRR** and **Hits@{1,5,10}** against the **standard** reference alignment (coherence repair does not apply to the ranking task). Baseline systems include a lexical baseline, SapBERT, and the BERTMap family (BERTMap, BERTMapLt, BERTMap-ss).

## Coherence

Each baseline's own global alignment is also checked with a reasoner. The [baseline coherence](https://liseda-lab.github.io/OAEI-Bio-ML/baselines/#baseline-coherence) table gives the unsatisfiable classes and the incoherence degree per pair (ELK on all three pairs, HermiT on NCIT–DOID), next to the coherence of the reference alignments before and after repair. They are computed under the same conventions as the participant results (see [evaluation metrics](./evaluation-metrics.md)). The machine-readable sources are `baseline_coherence.json` and `reference_coherence.json` at the repository root.

## Runtime and hardware

Wall-clock times for every baseline run — per pair and over all three, for both the Subtrack-1 matching phase and the Subtrack-2 ranking runs — are listed under [wall-clock times](https://liseda-lab.github.io/OAEI-Bio-ML/baselines/#runtime) on the baselines page, together with the specification of the single workstation they were run on. The machine-readable source is `baseline_runtime.json` at the repository root.

---

*The organiser baselines are provided as reference points, not as a target to beat; the contribution of the track is the task and reference design. Full methodology appears in the supplementary material (available at track launch).*
