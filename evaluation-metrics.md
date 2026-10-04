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

Each system's whole submitted alignment $M$, not only the test slice, is merged with both ontologies, with each correspondence asserted as an equivalence, and classified. We report the number of unsatisfiable named classes and the **incoherence degree**: that number over the counted named classes. The conventions are:

* only `=` correspondences are asserted, with the same rule for RDF and TSV submissions;
* a correspondence is dropped if either endpoint is an `owl:deprecated` class or is not a class of its task ontology;
* DOID is loaded without the classes and axioms of its `ext.owl` imports; their property declarations are kept, so that DOID's own axioms load unchanged;
* deprecated classes are not counted. The counted classes are NCIT–DOID 220,246, SNOMED–FMA 490,694 and SNOMED–NCIT 592,352.

**ELK** gives a sound lower bound on every pair. **HermiT** gives the exact count but terminates only on NCIT–DOID. Where ELK exhausts a 384 GB heap, the value is unknown and shown as —. The organiser baselines and the reference alignments are measured the same way.

<small>Note: as coherence-aware precision, recall, and F1 are headline measures, we **only** report those here; both the standard (i.e., unrepaired) and the repaired reference are scored via CodaBench.</small>

## Subtrack 2 — Local equivalence ranking

For each source entity, the system ranks a fixed candidate pool best-first. Writing $\mathrm{rank}(q)$ for the 1-based position of the correct target in query $q$'s ranking, over the query set $Q$:

$$
\mathrm{Hits@}k = \frac{1}{\vert Q \vert} \sum_{q \in Q} \mathbb{1}[\mathrm{rank}(q) \leq k], \qquad
\mathrm{MRR} = \frac{1}{\vert Q \vert} \sum_{q \in Q} \frac{1}{\mathrm{rank}(q)}.
$$

Reported: **MRR** and **Hits@{1,5,10}**. MRR rewards placing the correct target as early as possible (rank 1 scores 1, rank 2 scores 1/2, and so on); Hits@$k$ is the fraction of queries whose correct target lands in the top $k$.

## Averaging

Every headline metric is **macro-averaged over the three pairs** (NCIT–DOID, SNOMED–FMA, SNOMED–NCIT) — the unweighted mean of the per-pair values, so a system must do well on all three rather than being carried by the largest.

Global Coherence is the exception. It is reported **per pair**, because some cells cannot be computed, and an average would then mix two-pair and three-pair means.

## Timeline

The evaluation window and reporting dates (all 00:00 Anywhere on Earth):

| Milestone | Date |
|---|---|
| Provisional materials released | 6 July 2026 |
| Finalised datasets published | 7 July 2026 |
| Competition starts, evaluation + leaderboards open | 12 July 2026 |
| Evaluation closes | 30 September 2026 |
| Competition ends, results reported *(grace period until 13 October)* | 6 October 2026 |
