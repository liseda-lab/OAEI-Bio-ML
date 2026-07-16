# OAEI Bio-ML Track

OAEI Bio-ML is an [OAEI](https://oaei.ontologymatching.org/) ontology-matching track over **whole biomedical ontologies**. It evaluates machine-learning and rule-based matching systems on equivalence correspondences across three biomedical ontology pairs: **NCIT–DOID**, **SNOMED–FMA**, and **SNOMED–NCIT**. This website provides the documentation for preparing for and participating in OAEI Bio-ML 2026 in a form that is easy to browse, cite, and reuse. Supporting material on motivation, methods, reference repair, and coherence measures will be published in the accompanying supplementary materials _(available at track launch)_.

## Track Scope

The track targets ontology matching between large, established biomedical ontologies where the reference alignments are grounded in curated biomedical knowledge (UMLS/Mondo). The immediate objective is a coherent set of matching tasks that are:

* large enough to be meaningful (whole-ontology, not fragments, no pruning),
* difficult enough to be interesting to the ontology matching community, and
* well documented enough to support transparent evaluation and future reuse.

## Tasks

OAEI Bio-ML 2026 focuses global alignment and equivalence ranking, scored across **two CodaBench competitions**:

* **Global equivalence alignment.** For each pair, submit one full alignment. Semi-supervised: a public `refs_equiv/train.tsv` is provided per pair, and the test reference is hidden and scored organiser-side. Metrics: **repaired, coherence-aware P/R/F1** (headline), with a reasoner-checked **Global Coherence** score.
* **Local equivalence ranking.** For each source entity, rank a fixed candidate pool, placing high-scoring equivalence correspondences early. The public `*.test.cands.tsv` are gold-stripped (i.e., the answers are private). Metrics: **MRR** and **Hits@{1,5,10}**.

The standard/repaired references are **not directly comparable**; see [evaluation metrics](./evaluation-metrics.md). Submissions are scored using the repaired reference alignment.

## Datasets and Reference Alignments

This resource publishes (and points to):

* [the source ontologies and where to obtain each](./ontologies/ontologies.md),
* [task descriptions](./tasks/tasks.md) and [dataset packaging details](./quickstart.md),
* [evaluation metrics](./evaluation-metrics.md),
* the [baselines page](./BASELINES.md) and the [dataset & results changelog](./changelog.md), and
* extended supplementary material for each released edition _(available at track launch)_.

The 2026 datasets are **publicly available** on the Hugging Face Hub: [`OAEI-ML/bio-ml`](https://huggingface.co/datasets/OAEI-ML/bio-ml) (edition tag `2026`) — the task data is built of entity IRIs and downloads freely. The Hugging Face dataset is **data only**; the self-contained `scoring_kit/` (validators + self-scorers) ships separately with the [track repository](https://github.com/liseda-lab/OAEI-Bio-ML). Licence-restricted **source vocabularies** (SNOMED CT, UMLS) are obtained separately under your own licence (see [ontologies](./ontologies/ontologies.md)).

```bash
git clone https://github.com/liseda-lab/OAEI-Bio-ML   # the scoring kit
pip install -U huggingface_hub
hf download OAEI-ML/bio-ml --repo-type dataset --revision 2026 --local-dir ./bio-ml   # the data
```

The source ontologies are **not re-hosted** here; see [`ontologies/`](./ontologies/ontologies.md) for sources and licences.

## Timeline

> **Status:** 2026 edition — the datasets are final; evaluation and the leaderboards open on 12 July 2026 via the two CodaBench competitions.

| Milestone | Date |
|---|---|
| Provisional materials released | 6 July 2026 |
| Finalised datasets published | 7 July 2026 |
| Competition starts, evaluation + leaderboards open | 12 July 2026 |
| Evaluation closes | 30 September 2026 |
| Competition ends, results reported *(grace period until 13 October)* | 6 October 2026 |

*All dates are 00:00 Anywhere on Earth (AoE).*

## Get Started & Participate

* Read the **[quickstart](./quickstart.md)**: download from Hugging Face, run the scoring kit, obtain the ontologies, and submit on CodaBench.
* Two CodaBench competitions — [Track 1 Global Alignment](https://www.codabench.org/competitions/17424/) and [Track 1 Local Ranking](https://www.codabench.org/competitions/17423/) — open on 12 July 2026.
* Organiser-run [baselines](./BASELINES.md) are published before the competition; participant standings appear on the CodaBench leaderboards.

## Related Material

* [Ontology Alignment Evaluation Initiative (OAEI)](https://oaei.ontologymatching.org/)
* [Track repository](https://github.com/liseda-lab/OAEI-Bio-ML) · [website](https://liseda-lab.github.io/OAEI-Bio-ML/)

## Citation

A citation for the 2026 edition is still **pending** and will be published here once available. The benchmark design follows the original machine-learning-friendly Bio-ML datasets (He et al.).

## Organisers

OAEI Bio-ML 2026 is organised by [Jonathon Dilworth](https://dilworth.io/), [Pedro Cotovio](https://pedrocotovio.github.io/), [Ernesto Jiménez-Ruiz](https://ernestojimenezruiz.github.io/), and [Catia Pesquita](https://www.di.fc.ul.pt/~catiapesquita/).

## Contact

Questions or corrections: open an issue on the [track repository](https://github.com/liseda-lab/OAEI-Bio-ML) or email <contact@oaei-ml.org>.
