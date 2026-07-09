# Submission format — Track 1 / Subtrack 1 (Global equivalence alignment)

Produce a **complete alignment** between the source and target ontology of a pair and submit it — one file per ontology pair — as **either** an **OAEI Alignment RDF/XML** file (the long-standing OAEI format) **or** a simple **TSV**. Both are scored identically.

## Format

- One `<rdf:RDF>` root containing one `<Alignment>` with one `<map><Cell>…</Cell></map>` per correspondence.
- Each `<Cell>` has `<entity1 rdf:resource="…"/>`, `<entity2 rdf:resource="…"/>`, and an optional `<relation>` (`=`, `<`, `>`). Entities are **full absolute OWL IRIs**.
- `<measure>` (confidence) is optional and ignored by the metric.

```xml
<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns="http://knowledgeweb.semanticweb.org/heterogeneity/alignment#">
  <Alignment>
    <map><Cell>
      <entity1 rdf:resource="http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C101044"/>
      <entity2 rdf:resource="http://purl.obolibrary.org/obo/DOID_0080073"/>
      <relation>=</relation>
    </Cell></map>
    <!-- ... one <map><Cell> per correspondence ... -->
  </Alignment>
</rdf:RDF>
```

## TSV alternative

Instead of RDF, submit a tab-separated file with `SrcEntity` and `TgtEntity` columns (an optional `Relation` — `=`/`<`/`>` — and `Score` are ignored by the metric). Entities are full absolute OWL IRIs.

```tsv
SrcEntity	TgtEntity	Relation
http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C101044	http://purl.obolibrary.org/obo/DOID_0080073	=
```

## Scoring

- Scored against **two** references: the *standard* (complete) reference with traditional set **P/R/F1**, and the *repaired* (coherence-aware) reference — **relation-agnostic** (a reference `<`/`>` is credited by a predicted correspondence of any relation) and **`?`-ignored** (incoherence-flagged mappings are removed from both denominators). The headline is the **repaired** F1; standard is shown alongside. These P/R/F1 columns are **auto-scored on submission**. **Global Coherence** (degree of incoherence, reasoner-based) is computed off-platform and added to that column afterwards (blank until then).
- Naming your file: include the pair slug (`ncit-doid`, `snomed-fma`, `snomed-ncit`) in the filename, e.g. `ncit-doid.rdf`.
- The evaluation follows the semi-supervised protocol: a public `refs_equiv/train.tsv` of positive equivalence mappings is provided per pair for supervised systems; the test reference is held out and scored on the hidden test slice (train/valid mappings are masked).

## Validate

```bash
python3 validate_global.py my_alignment.rdf     # or:  validate_global.py my_alignment.tsv
```

There is no public self-scorer for this task (the reference is private); validate structure before submitting. `alignment.rng` is an optional RelaxNG schema for stricter checking.
