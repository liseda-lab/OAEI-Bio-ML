# Evaluation Metrics

This page summarises how OAEI Bio-ML submissions are scored, per track. A full description appears in the supplementary material (available at track launch).

## Subtrack 1 — Global equivalence alignment

Each submission is a full alignment per pair (full OWL IRIs). It is scored with **precision, recall and F1** against **two references**:

$$
\mathrm{Precision} = \frac{\vert A \cap R \vert}{\vert A \vert}, \qquad
\mathrm{Recall} = \frac{\vert A \cap R \vert}{\vert R \vert}, \qquad
\mathrm{F1} = \frac{2 \cdot \mathrm{Precision} \cdot \mathrm{Recall}}{\mathrm{Precision} + \mathrm{Recall}}.
$$

* **Repaired reference (headline).** Coherence-aware and relation-agnostic: correspondences flagged as uncertain (`?`) are ignored from both the predictions and the reference, and a reference subsumption (`<` / `>`) is credited by a predicted correspondence of any relation. The headline score is the **repaired, coherence-aware F1**.
* **Standard reference (secondary).** The complete, possibly-incoherent reference scored with traditional P/R/F1.

**The two references are not directly comparable.** They differ in both membership and scoring rules, so a repaired-vs-standard difference is *not* an accuracy delta — read each within its own reference.

**Global Coherence.** Alongside P/R/F1 we report a reasoner-checked coherence measure — the degree of logical incoherence induced by the submitted alignment on the merged ontologies (0 = coherent). Because it needs a description-logic reasoner, coherence is computed **organiser-side**, not in the participant scoring kit.

## Subtrack 2 — Local equivalence ranking

For each source entity, the system ranks a fixed candidate pool best-first. Writing $\mathrm{rank}(q)$ for the 1-based position of the correct target in query $q$'s ranking, over the query set $Q$:

$$
\mathrm{Hits@}k = \frac{1}{\vert Q \vert} \sum_{q \in Q} \mathbb{1}[\mathrm{rank}(q) \leq k], \qquad
\mathrm{MRR} = \frac{1}{\vert Q \vert} \sum_{q \in Q} \frac{1}{\mathrm{rank}(q)}.
$$

Reported: **MRR** and **Hits@{1,5,10}**. MRR rewards placing the correct target as early as possible (rank 1 scores 1, rank 2 scores 1/2, and so on); Hits@$k$ is the fraction of queries whose correct target lands in the top $k$.

## Averaging

Every headline metric is **macro-averaged over the three pairs** (NCIT–DOID, SNOMED–FMA, SNOMED–NCIT) — the unweighted mean of the per-pair values, so a system must do well on all three rather than being carried by the largest.

## Timeline

The evaluation window and reporting dates (all 00:00 Anywhere on Earth):

| Milestone | Date |
|---|---|
| Provisional materials released | 6 July 2026 |
| Finalised datasets published | 7 July 2026 |
| Competition starts, evaluation + leaderboards open | 12 July 2026 |
| Evaluation closes | 1 September 2026 |
| Competition ends, results reported *(grace period until 12 September)* | 6 September 2026 |
