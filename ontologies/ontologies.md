# Ontologies

OAEI Bio-ML matches **whole biomedical ontologies**. To keep licensing clean, the track **does not re-host** any source ontology: each is obtained from its original publisher under that publisher's licence. This page lists the sources, their licences, and which pair needs which. The reference alignments themselves are distributed with the [task data](../quickstart.md).

## Which ontologies each pair needs

| Pair | Ontologies to obtain | Also used in reference construction |
|---|---|---|
| **NCIT–DOID** | NCIT, DOID | MONDO, UMLS |
| **SNOMED–FMA** | SNOMED CT, FMA | UMLS |
| **SNOMED–NCIT** | SNOMED CT, NCIT | UMLS |

NCIT, DOID, SNOMED CT and FMA are the four ontologies matched across the three pairs. MONDO and the UMLS Metathesaurus underlie the reference construction (the gold references are grounded in UMLS/Mondo).

## Sources and licences

Three sources are openly downloadable; three are access-controlled and require a licence/account.

### Openly downloadable

* **NCIT — NCI Thesaurus** *(cancer / clinical; licence: CC BY 4.0)*
  A reference terminology covering cancer and general clinical concepts, published by the U.S. National Cancer Institute. Obtain from the [NCI Thesaurus](https://ncithesaurus.nci.nih.gov/) or the OBO PURL [`purl.obolibrary.org/obo/ncit.owl`](http://purl.obolibrary.org/obo/ncit.owl); also on [BioPortal](https://bioportal.bioontology.org/ontologies/NCIT).

* **MONDO — Mondo Disease Ontology** *(disease; licence: CC BY 4.0)*
  A harmonised disease ontology from the Monarch Initiative, used here in reference construction. Obtain from [mondo.monarchinitiative.org](https://mondo.monarchinitiative.org/) or the OBO PURL [`purl.obolibrary.org/obo/mondo.owl`](http://purl.obolibrary.org/obo/mondo.owl).

* **DOID — Human Disease Ontology** *(disease; licence: CC0 1.0)*
  A standardised ontology of human diseases. Obtain from [disease-ontology.org](https://disease-ontology.org/) or the OBO PURL [`purl.obolibrary.org/obo/doid.owl`](http://purl.obolibrary.org/obo/doid.owl).

### Access-controlled (licence / account required)

* **SNOMED CT** *(clinical terminology; licence: SNOMED CT Affiliate Licence)*
  A comprehensive clinical healthcare terminology from SNOMED International. Access requires a SNOMED CT Affiliate Licence — free of charge in UMLS-member territories via the [UMLS Terminology Services (UTS)](https://uts.nlm.nih.gov/), or otherwise through [SNOMED International](https://www.snomed.org/).

* **UMLS Metathesaurus** *(metathesaurus; licence: UMLS Metathesaurus Licence via UTS)*
  The Unified Medical Language System integrates many biomedical vocabularies; it underlies the reference construction for every pair. Requires a free UTS account: [uts.nlm.nih.gov](https://uts.nlm.nih.gov/) — see the [UMLS overview](https://www.nlm.nih.gov/research/umls/).

* **FMA — Foundational Model of Anatomy** *(anatomy; per its own licence)*
  A reference ontology of human anatomy from the Structural Informatics Group, University of Washington. Obtain per its licence from the [FMA project page](http://si.washington.edu/projects/fma) or [BioPortal](https://bioportal.bioontology.org/ontologies/FMA).

## Notes

* Use the ontology **versions pinned by the 2026 edition** where indicated on the dataset card; matching against a different release may shift entity IRIs.
* Correspondences use **full OWL IRIs** (e.g. `http://purl.obolibrary.org/obo/DOID_1612`).
* Nothing on this page is re-distributed by OAEI Bio-ML; all links point to the original publishers.
