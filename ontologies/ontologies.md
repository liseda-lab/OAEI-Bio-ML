# Ontologies

OAEI Bio-ML matches **whole biomedical ontologies**. Most of them now ship with the dataset: the [Hugging Face download](../quickstart.md) bundles the **NCIT**, **DOID**, and **FMA** ontology files alongside the task data, so for most pairs there is nothing extra to obtain. The one exception is **SNOMED CT**, which its licence does not permit us to redistribute — you obtain it yourself, either under a SNOMED CT Affiliate Licence or by [contacting us](mailto:contact@oaei-ml.org) for a copy strictly for research purposes. This page lists each source, its licence, and which pair needs which. The public-facing references are distributed with the [task data](../quickstart.md).

## Which ontologies each pair needs

| Pair | Provided in the download | You obtain yourself |
|---|---|---|
| **NCIT–DOID** | NCIT, DOID | — |
| **SNOMED–FMA** | FMA | SNOMED CT |
| **SNOMED–NCIT** | NCIT | SNOMED CT |

NCIT, DOID, SNOMED CT and FMA are the four ontologies matched across the three pairs; three of them (NCIT, DOID, FMA) travel with the download and only SNOMED CT is obtained separately. MONDO and the UMLS Metathesaurus underlie the **organiser-side reference construction** (the gold references are grounded in UMLS/Mondo) — participants do **not** need them to run the tasks.

## Sources and licences

### Provided in the Hugging Face download

These three ship with the [`OAEI-ML/bio-ml`](https://huggingface.co/datasets/OAEI-ML/bio-ml) dataset (edition tag `2026`), so you do not need to fetch them separately. The publisher links are kept for provenance and version reference.

* **NCIT — NCI Thesaurus** *(cancer / clinical; licence: CC BY 4.0)*
  A reference terminology covering cancer and general clinical concepts, published by the U.S. National Cancer Institute. Provenance: the [NCI Thesaurus](https://ncithesaurus.nci.nih.gov/) or the OBO PURL [`purl.obolibrary.org/obo/ncit.owl`](http://purl.obolibrary.org/obo/ncit.owl); also on [BioPortal](https://bioportal.bioontology.org/ontologies/NCIT).

* **DOID — Human Disease Ontology** *(disease; licence: CC0 1.0)*
  A standardised ontology of human diseases. Provenance: [disease-ontology.org](https://disease-ontology.org/) or the OBO PURL [`purl.obolibrary.org/obo/doid.owl`](http://purl.obolibrary.org/obo/doid.owl).

* **FMA — Foundational Model of Anatomy** *(anatomy; per its own licence)*
  A reference ontology of human anatomy from the Structural Informatics Group, University of Washington. Provenance: the [FMA project page](http://si.washington.edu/projects/fma) or [BioPortal](https://bioportal.bioontology.org/ontologies/FMA).

### Obtain yourself: SNOMED CT

* **SNOMED CT** *(clinical terminology; licence: SNOMED CT Affiliate Licence)*
  A comprehensive clinical healthcare terminology from SNOMED International, used in the `SNOMED-FMA` and `SNOMED-NCIT` pairs. Its licence does not permit us to redistribute it, so you obtain a copy yourself by **either** route:
  1. **Under a SNOMED CT Affiliate Licence** — free of charge in UMLS-member territories via the [UMLS Terminology Services (UTS)](https://uts.nlm.nih.gov/), or otherwise through [SNOMED International](https://www.snomed.org/); **or**
  2. **[Contact us](mailto:contact@oaei-ml.org)** to obtain a copy strictly for research purposes.

### Reference-construction resources (organiser-side)

These underlie how the gold references were built. **Participants do not need them** to produce or score submissions; they are documented here for transparency.

* **MONDO — Mondo Disease Ontology** *(disease; licence: CC BY 4.0)*
  A harmonised disease ontology from the Monarch Initiative. Source: [mondo.monarchinitiative.org](https://mondo.monarchinitiative.org/) or the OBO PURL [`purl.obolibrary.org/obo/mondo.owl`](http://purl.obolibrary.org/obo/mondo.owl).

* **UMLS Metathesaurus** *(metathesaurus; licence: UMLS Metathesaurus Licence via UTS)*
  The Unified Medical Language System integrates many biomedical vocabularies; it underlies the reference construction for every pair. Source (free UTS account): [uts.nlm.nih.gov](https://uts.nlm.nih.gov/) — see the [UMLS overview](https://www.nlm.nih.gov/research/umls/).

## Notes

* Use the ontology **versions pinned by the 2026 edition** where indicated on the dataset card; matching against a different release may shift entity IRIs.
* Correspondences use **full OWL IRIs** (e.g. `http://purl.obolibrary.org/obo/DOID_1612`).
* OAEI Bio-ML redistributes the NCIT, DOID, and FMA ontology files with the dataset; **SNOMED CT is not redistributed** — obtain it under your own Affiliate Licence or by contacting us for a research-only copy (see above).
