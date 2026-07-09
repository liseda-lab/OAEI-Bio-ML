# Global Alignment: Submission Format

Subtrack 1 is a whole-ontology equivalence alignment over the three Bio-ML 2026 pairs:

* `NCIT-DOID`
* `SNOMED-FMA`
* `SNOMED-NCIT`

For each pair you submit **one complete alignment** in the [OAEI Alignment RDF format](https://moex.gitlabpages.inria.fr/alignapi/format.html), using **full OWL IRIs**. Submissions are scored organiser-side against the hidden test reference — repaired, coherence-aware P/R/F1 (headline) and Global Coherence (see the [task description](./alignment_task_index.md)).

## File format

Root is `rdf:RDF`. The default namespace (`xmlns=`) is the OAEI Alignment namespace: `http://knowledgeweb.semanticweb.org/heterogeneity/alignment`. Exactly one `<Alignment>` with a header (`<xml>yes</xml>`, `<level>0</level>`, `<type>??</type>`, and `<onto1>` / `<onto2>` URIs). Each correspondence is a `<map>` wrapping one `<Cell>`:

  - `<entity1 rdf:resource="IRI"/>` — the source ontology entity's **full OWL IRI**,
  - `<entity2 rdf:resource="IRI"/>` — the target ontology entity's **full OWL IRI**,
  - `<relation>=</relation>` — equivalence,
  - `<measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">1.0</measure>` — confidence in `[0, 1]`.

Submit one file per pair. Entity IRIs MUST be absolute. The order of `<map>` elements is irrelevant. Submit a full alignment over the two ontologies; the organisers score the portion that lands on the hidden test entities.

## Worked example (illustrative)

The cell below is illustrative — it shows the exact shape, using full OWL IRIs of the kind found in `NCIT-DOID`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns="http://knowledgeweb.semanticweb.org/heterogeneity/alignment"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:xsd="http://www.w3.org/2001/XMLSchema#">
  <Alignment>
    <xml>yes</xml>
    <level>0</level>
    <type>??</type>
    <onto1>http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl</onto1>
    <onto2>http://purl.obolibrary.org/obo/doid.owl</onto2>
    <map>
      <Cell>
        <entity1 rdf:resource="http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C3262"/>
        <entity2 rdf:resource="http://purl.obolibrary.org/obo/DOID_162"/>
        <relation>=</relation>
        <measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">1.0</measure>
      </Cell>
    </map>
  </Alignment>
</rdf:RDF>
```

## Minimal copy-paste template

```xml
<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns="http://knowledgeweb.semanticweb.org/heterogeneity/alignment"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:xsd="http://www.w3.org/2001/XMLSchema#">
  <Alignment>
    <xml>yes</xml>
    <level>0</level>
    <type>??</type>
    <onto1>SOURCE_ONTOLOGY_URI</onto1>
    <onto2>TARGET_ONTOLOGY_URI</onto2>
    <map>
      <Cell>
        <entity1 rdf:resource="SOURCE_IRI"/>
        <entity2 rdf:resource="TARGET_IRI"/>
        <relation>=</relation>
        <measure rdf:datatype="http://www.w3.org/2001/XMLSchema#float">1.0</measure>
      </Cell>
    </map>
  </Alignment>
</rdf:RDF>
```

## Validate — scoring is organiser-side

Subtrack 1 is **semi-supervised**: the test reference is hidden, so you cannot self-score against it. Validate the structure of each alignment file with the kit's `validate_global.py` (Python 3.12+, standard library; it also checks against the bundled RelaxNG schema `alignment.rng`), then submit:

```bash
# structural + schema validation of one alignment file
python scoring_kit/validate_global.py  my-ncit-doid.rdf
```

To sanity-check your matcher before submitting, compare its output against the **public** `refs_equiv/train.tsv` correspondences (a proxy — there is no public global scorer, and the hidden test slice is scored organiser-side). The organisers then compute the headline repaired, coherence-aware P/R/F1, the standard P/R/F1, and Global Coherence, and publish them to the Track 1 — Global Alignment leaderboard.
