# OAEI Bio-ML — Biomedical Ontology Matching

OAEI Bio-ML is an [OAEI](https://oaei.ontologymatching.org/) ontology-matching track over **whole biomedical ontologies** — *(with roots in/based on LargeBio)* [8]. It evaluates equivalence ~~and subsumption~~ matching across three pairs — **NCIT–DOID**, **SNOMED–FMA**, and **SNOMED–NCIT** (the NCI Thesaurus [11], the Human Disease Ontology [12], SNOMED CT [14], and the Foundational Model of Anatomy [13]) — with references grounded in curated biomedical knowledge (UMLS [9] / Mondo [10]) and repaired for logical coherence.

## Tracks

* **Track 1 — Equivalence**
  * **Subtrack 1 — Global equivalence alignment.** Submit one full alignment per pair (full OWL IRIs). Semi-supervised: a public `refs_equiv/train.tsv` is provided per pair; the test reference is hidden and scored organiser-side. Headline metric: repaired, coherence-aware P/R/F1, with a reasoner-checked Global Coherence score.
  * **Subtrack 2 — Local equivalence ranking.** Rank a fixed, gold-stripped candidate pool per source entity. Metrics: MRR and Hits@{1,5,10}.

Full definitions are on the [evaluation metrics](./evaluation-metrics.md) page. All headline metrics are macro-averaged over the three pairs.

## How the references were built

For each pair, the reference alignment is grounded in the UMLS Metathesaurus [9] and Mondo [10]. Because a reference assembled from these sources can be logically **incoherent**, it is **repaired** before use: the set of correspondences to remove (or weaken) is computed as a **union over three repair tools** — ALCOMO [6], LogMap [5], and AML [4] — following the LargeBio [8] repair tradition, and verified coherent with the ELK reasoner [7]. Under the track's annotation scheme, surviving correspondences keep their (possibly weakened) equivalence/subsumption relation; only fully-removed correspondences are marked uncertain (`?`) and ignored at scoring time.

The track therefore ships **two references** per pair: the **standard** (complete, possibly-incoherent) reference and the **repaired** (coherence-aware) reference. The **repaired reference is the headline** and is what this site reports; the standard reference is retained for the CodaBench leaderboard's standard scoring. The two are **not directly comparable** — see [evaluation metrics](./evaluation-metrics.md).

## Serialisation

By design, **Track 1 uses full OWL IRIs**. Public local-ranking candidate files (`*.test.cands.tsv`) are **gold-stripped**: they contain the source entity and its candidate list only.

## Data

The 2026 datasets are **publicly available** on the Hugging Face Hub as [`OAEI-ML/bio-ml`](https://huggingface.co/datasets/OAEI-ML/bio-ml) (edition tag `2026`) — the task data is entity IRIs and downloads without gating. The Hugging Face dataset is **data only**; the self-contained `scoring_kit/` (validators + self-scorers) ships separately with the [track repository](https://github.com/liseda-lab/OAEI-Bio-ML). The licence-restricted **source ontologies** (SNOMED CT [14], UMLS [9]) are **not re-hosted** — see [ontologies](./ontologies/ontologies.md) for where to obtain each and under which licence. The [quickstart](./quickstart.md) walks through cloning the scoring kit, downloading the data, and validating and self-scoring a submission.

## Baselines & results

Organiser-run baseline systems (a naive lexical baseline, SapBERT [3], and the BERTMap [2] family) are published before the competition on the [baselines](./BASELINES.md) page, rendered directly from the machine-readable `leaderboard.json`. Participant standings appear on the CodaBench leaderboards, surfaced on the [results](https://liseda-lab.github.io/OAEI-Bio-ML/results/) page once the evaluation window opens.

## Participate

Two CodaBench competitions — [Track 1 Global Alignment](https://www.codabench.org/competitions/17424/) and [Track 1 Local Ranking](https://www.codabench.org/competitions/17423/) — open on **12 July 2026**. See the [quickstart](./quickstart.md).

## Organisers & contact

OAEI Bio-ML 2026 is organised by [Jon Dilworth](https://dilworth.io/), [Pedro Cotovio](https://pedrocotovio.github.io/), [Ernesto Jiménez-Ruiz](https://ernestojimenezruiz.github.io/), and [Catia Pesquita](https://www.di.fc.ul.pt/~catiapesquita/). The benchmark design follows the original machine-learning-friendly Bio-ML datasets (He et al. [1]).

Questions or corrections: open an issue on the [track repository](https://github.com/liseda-lab/OAEI-Bio-ML) or email <contact@oaei-ml.org>.

## References

1. He, Y., Chen, J., Dong, H., Jiménez-Ruiz, E., Hadian, A., & Horrocks, I. (2022). Machine Learning-Friendly Biomedical Datasets for Equivalence and Subsumption Ontology Matching. In: The Semantic Web — ISWC 2022. LNCS 13489, pp. 575–591. Springer. <https://doi.org/10.1007/978-3-031-19433-7_33>
2. He, Y., Chen, J., Antonyrajah, D., & Horrocks, I. (2022). BERTMap: A BERT-based Ontology Alignment System. In: Proceedings of the AAAI Conference on Artificial Intelligence, 36(5), 5684–5691. <https://doi.org/10.1609/aaai.v36i5.20510>
3. Liu, F., Shareghi, E., Meng, Z., Basaldella, M., & Collier, N. (2021). Self-Alignment Pretraining for Biomedical Entity Representations. In: NAACL-HLT 2021, pp. 4228–4238. <https://doi.org/10.18653/v1/2021.naacl-main.334>
4. Faria, D., Pesquita, C., Santos, E., Palmonari, M., Cruz, I. F., & Couto, F. M. (2013). The AgreementMakerLight Ontology Matching System. In: OTM 2013. LNCS 8185, pp. 527–541. Springer. <https://doi.org/10.1007/978-3-642-41030-7_38>
5. Jiménez-Ruiz, E., & Cuenca Grau, B. (2011). LogMap: Logic-based and Scalable Ontology Matching. In: The Semantic Web — ISWC 2011. LNCS 7031, pp. 273–288. Springer. <https://doi.org/10.1007/978-3-642-25073-6_18>
6. Meilicke, C. (2011). Alignment Incoherence in Ontology Matching. PhD thesis, University of Mannheim. <https://madoc.bib.uni-mannheim.de/29351/>
7. Kazakov, Y., Krötzsch, M., & Simančík, F. (2014). The Incredible ELK: From Polynomial Procedures to Efficient Reasoning with ℰℒ Ontologies. Journal of Automated Reasoning, 53(1), 1–61. <https://doi.org/10.1007/s10817-013-9296-3>
8. Ontology Alignment Evaluation Initiative — Large BioMed (LargeBio) track. <https://www.cs.ox.ac.uk/isg/projects/SEALS/oaei/>
9. Bodenreider, O. (2004). The Unified Medical Language System (UMLS): Integrating Biomedical Terminology. Nucleic Acids Research, 32(Database issue), D267–D270. <https://doi.org/10.1093/nar/gkh061>
10. Vasilevsky, N. A., et al. (2022). Mondo: Unifying Diseases for the World, by the World. medRxiv 2022.04.13.22273750. <https://doi.org/10.1101/2022.04.13.22273750>
11. Sioutos, N., de Coronado, S., Haber, M. W., Hartel, F. W., Shaia, W.-L., & Wright, L. W. (2007). NCI Thesaurus: A Semantic Model Integrating Cancer-related Clinical and Molecular Information. Journal of Biomedical Informatics, 40(1), 30–43. <https://doi.org/10.1016/j.jbi.2006.02.013>
12. Schriml, L. M., et al. (2022). The Human Disease Ontology 2022 Update. Nucleic Acids Research, 50(D1), D1255–D1261. <https://doi.org/10.1093/nar/gkab1063>
13. Rosse, C., & Mejino, J. L. V. (2003). A Reference Ontology for Biomedical Informatics: the Foundational Model of Anatomy. Journal of Biomedical Informatics, 36(6), 478–500. <https://doi.org/10.1016/j.jbi.2003.11.007>
14. Donnelly, K. (2006). SNOMED-CT: The Advanced Terminology and Coding System for eHealth. Studies in Health Technology and Informatics, 121, 279–290.

### References (Webpage Animation)

The homepage hero is a *schematic* depiction of geometric model-based ontology embeddings — not a faithful reproduction of any single method. Its two scenes are drawn after the works cited below (the method keys — **ELEm**, **BoxEL**, **Box²EL**, **HiT**, **OnT** — are the labels shown in the animation itself): the Euclidean box scene after the ℰℒ⁺⁺ box-embedding line of work, and the hyperbolic scene directly after OnT, which builds on HiT's Poincaré-ball hierarchy encoding.

* **ELEm** — Kulmanov, M., Liu-Wei, W., Yan, Y., & Hoehndorf, R. (2019). EL Embeddings: Geometric Construction of Models for the Description Logic ℰℒ⁺⁺. In: Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence (IJCAI 2019), pp. 6103–6109. <https://doi.org/10.24963/ijcai.2019/845>
* **BoxEL** — Xiong, B., Potyka, N., Tran, T.-K., Nayyeri, M., & Staab, S. (2022). Faithful Embeddings for ℰℒ⁺⁺ Knowledge Bases. In: The Semantic Web — ISWC 2022. LNCS 13489, pp. 22–38. Springer. <https://doi.org/10.1007/978-3-031-19433-7_2>
* **Box²EL** — Jackermeier, M., Chen, J., & Horrocks, I. (2024). Dual Box Embeddings for the Description Logic ℰℒ⁺⁺. In: Proceedings of the ACM Web Conference 2024 (WWW '24), pp. 2250–2258. <https://doi.org/10.1145/3589334.3645648>
* **HiT** — He, Y., Yuan, Z., Chen, J., & Horrocks, I. (2024). Language Models as Hierarchy Encoders. In: Advances in Neural Information Processing Systems 37 (NeurIPS 2024). <https://arxiv.org/abs/2401.11374>
* **OnT** — Yang, H., Chen, J., He, Y., Gao, Y., & Horrocks, I. (2025). Language Models as Ontology Encoders. arXiv:2507.14334. <https://arxiv.org/abs/2507.14334>

---

*OAEI Bio-ML 2026 (first edition). Track repository: <https://github.com/liseda-lab/OAEI-Bio-ML>.*
