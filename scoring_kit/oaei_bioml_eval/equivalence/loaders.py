"""
oaei_bioml_eval.equivalence.loaders: read Track 1 submissions + gold off disk.

Global alignment comes as OAEI Alignment RDF or a DeepOnto `(SrcEntity, TgtEntity
[, Score])` TSV, both reduced to a set of `(src, tgt)` pairs. Local ranking comes
as either a per-query `TgtCandidates` list (pre-ranked) or a scored block TSV
(`SrcEntity, TgtEntity, Score`, `candidate_count` rows/query, positional query
order); the gold is one `(src, tgt)` per query in that same order.

RDF/XML alignments (`.rdf`/`.xml`/`.owl`) parse with the pure-stdlib `xml.etree` — no
dependency, so global scoring runs in the no-pip CodaBench container and the TSV path
stays dependency-free; Turtle/N3 (`.ttl`/`.n3`) fall back to rdflib (the `[rdf]` extra),
imported lazily. All forms reduce to the same `(src, tgt)` pairs (verified equal).
"""
from __future__ import annotations

from pathlib import Path

from ..io import parse_list, read_tsv
from .metrics import rank_by_score

_RDF_SUFFIXES = {".rdf", ".xml", ".owl", ".ttl", ".n3"}
_RDF_XML_SUFFIXES = {".rdf", ".xml", ".owl"}   # RDF/XML — parseable with the stdlib xml.etree
_ALIGN_NS = "http://knowledgeweb.semanticweb.org/heterogeneity/alignment#"
_RDF_SYNTAX_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"   # rdf:resource on entity1/entity2
_EQUIVALENCE_RELATIONS = {"=", "equivalent", "equiv"}
# one-directional weakenings kept by an Option-Two reference (LogMap bare `<`/`>` and the
# organiser-canonical `<=`/`>=`): coherence-aware but still a reference POSITIVE, since the
# global task scores only the EXISTENCE of a correspondence, not its relation symbol.
_SUBSUMPTION_RELATIONS = {"<", ">", "<=", ">="}
_FLAGGED_RELATION = "?"   # OAEI LargeBio: an incoherence-causing reference mapping


def load_pairs_tsv(path: str | Path) -> set[tuple[str, str]]:
    """`(SrcEntity, TgtEntity)` pairs from a DeepOnto-style alignment TSV"""
    return {(row["SrcEntity"], row["TgtEntity"]) for row in read_tsv(path)}


def _alignment_cells(path: str | Path) -> list[tuple[str, str, str]]:
    """Every OAEI Alignment cell as `(entity1, entity2, relation_text)`. RDF/XML parses with the
    pure-stdlib `xml.etree`; Turtle/N3 with rdflib. One parser, so the three loaders below just
    filter by relation — and the xml.etree and rdflib forms are provably interchangeable (verified
    to yield identical pair sets on every reference + baseline alignment)."""
    if Path(path).suffix.lower() in _RDF_XML_SUFFIXES:
        return _alignment_cells_xml(path)
    return _alignment_cells_rdflib(path)


def _alignment_cells_xml(path: str | Path) -> list[tuple[str, str, str]]:
    """RDF/XML alignment cells via the standard library (no rdflib — runs in the CodaBench container).
    A cell is ANY element carrying an `entity1` child — a typed `align:Cell` OR an untyped
    `rdf:Description` — mirroring the rdflib union `subjects(RDF.type, Cell) | subjects(entity1, None)`
    (the `map`/`Alignment` wrappers have no direct `entity1` child, so they are not matched).
    Namespace-tolerant on local tag names; entity1/entity2 read from the `rdf:resource` attribute."""
    import xml.etree.ElementTree as ET

    local = lambda tag: tag.rsplit("}", 1)[-1]   # noqa: E731 — strip any XML namespace
    resource = f"{{{_RDF_SYNTAX_NS}}}resource"
    out: list[tuple[str, str, str]] = []
    for element in ET.parse(str(path)).getroot().iter():
        entity1 = entity2 = None
        relation_text = ""
        for child in element:
            tag = local(child.tag)
            if tag == "entity1":
                entity1 = child.get(resource) or child.get("resource")
            elif tag == "entity2":
                entity2 = child.get(resource) or child.get("resource")
            elif tag == "relation":
                relation_text = (child.text or "").strip()
        if entity1 is not None and entity2 is not None:
            out.append((entity1, entity2, relation_text))
    return out


def _alignment_cells_rdflib(path: str | Path) -> list[tuple[str, str, str]]:
    """Turtle/N3 alignment cells via rdflib (the `[rdf]` extra), imported lazily."""
    from rdflib import Graph, URIRef    # type: ignore
    from rdflib.namespace import RDF    # type: ignore

    align = lambda local: URIRef(_ALIGN_NS + local)   # noqa: E731 — terse local alias
    graph = Graph()
    graph.parse(str(path))
    # union, NOT `or`: a mixed file (some cells typed align:Cell, some only carrying align:entity1)
    # would otherwise drop whichever set the `or` skips. Same BNode subjects dedupe, so this is safe.
    cells = set(graph.subjects(RDF.type, align("Cell"))) | set(graph.subjects(align("entity1"), None))
    out: list[tuple[str, str, str]] = []
    for cell in cells:
        entity1 = next(graph.objects(cell, align("entity1")), None)
        entity2 = next(graph.objects(cell, align("entity2")), None)
        relation = next(graph.objects(cell, align("relation")), None)
        if entity1 is None or entity2 is None:
            continue
        out.append((str(entity1), str(entity2), "" if relation is None else str(relation).strip()))
    return out


def load_pairs_rdf(path: str | Path) -> set[tuple[str, str]]:
    """`(entity1, entity2)` pairs from an OAEI Alignment-API RDF (equivalence cells)"""
    return {(entity1, entity2) for entity1, entity2, relation_text in _alignment_cells(path)
            if relation_text == "" or relation_text in _EQUIVALENCE_RELATIONS}   # absent/empty -> equivalence


def load_global_pairs(path: str | Path) -> set[tuple[str, str]]:
    """a global alignment (submission OR reference) -> `(src, tgt)` pairs; RDF or TSV by suffix.
    Equivalence-only by design — the coherence pipeline reuses this to build EquivalentClasses
    bridges, so it must NOT silently absorb subsumption cells. Use load_global_submission for the
    relation-agnostic existence set the equivalence metric scores."""
    return load_pairs_rdf(path) if Path(path).suffix.lower() in _RDF_SUFFIXES else load_pairs_tsv(path)


def load_global_submission(path: str | Path) -> set[tuple[str, str]]:
    """
    a global alignment SUBMISSION -> `(src, tgt)` pairs, RELATION-AGNOSTIC (existence-only).
    The global task scores only WHETHER a correspondence exists, never its relation symbol, so a
    matcher cell counts whatever it asserts (`=`/`<`/`>`/`<=`/`>=`); only a `?` cell — which a
    matcher never emits — is not a positive assertion. This is what makes a predicted `=` matching
    a reference subsumption (and the vice-versa) score as a hit. RDF or TSV by suffix. Distinct
    from load_global_pairs, which stays equivalence-only for the coherence bridge.
    """
    if Path(path).suffix.lower() not in _RDF_SUFFIXES:
        return load_pairs_tsv(path)
    return {(entity1, entity2) for entity1, entity2, relation_text in _alignment_cells(path)
            if relation_text != _FLAGGED_RELATION}   # any asserted relation is an existence claim


def _load_reference_rdf(path: str | Path) -> tuple[set[tuple[str, str]], set[tuple[str, str]]]:
    """(R, U) from a reference RDF: R = equivalence/subsumption/`?` cells, U = the `?` cells only.
    Option-Two references keep coherence-weakened correspondences as one-directional subsumptions
    (`<`/`>`/`<=`/`>=`); those count as reference POSITIVES (in R, never U) because the global
    task scores existence only — see _SUBSUMPTION_RELATIONS."""
    reference: set[tuple[str, str]] = set()
    flagged: set[tuple[str, str]] = set()
    for entity1, entity2, relation_text in _alignment_cells(path):
        pair = (entity1, entity2)
        if relation_text == _FLAGGED_RELATION:
            reference.add(pair)   # a `?` cell is still a reference mapping for the standard metric
            flagged.add(pair)
        elif (relation_text == "" or relation_text in _EQUIVALENCE_RELATIONS
              or relation_text in _SUBSUMPTION_RELATIONS):
            # `=`/absent OR an Option-Two subsumption (`<`/`>`/`<=`/`>=`): a reference positive in
            # R+ (= R - U). The subsumption is NOT flagged — the equivalence task credits the mere
            # existence of the correspondence, so a predicted `=` here still counts as a true positive.
            reference.add(pair)
    return reference, flagged


def load_global_reference(path: str | Path) -> tuple[set[tuple[str, str]], set[tuple[str, str]]]:
    """
    the complete reference + its `?`-flagged (incoherence-causing) subset -> `(R, U)`.
    R is every equivalence-, subsumption-, or `?`-cell (the standard metric counts `?` as a
    positive); U is the `?` subset only (ignored by the coherence-aware metric). An Option-Two
    reference's `<`/`>`/`<=`/`>=` cells are positives in R+ = R - U, not flagged. Inline
    OAEI-canonical `?` is auto-detected in an RDF reference; a TSV reference cannot carry `?` so
    `U = ∅` (coherent == standard).
    """
    if Path(path).suffix.lower() in _RDF_SUFFIXES:
        return _load_reference_rdf(path)
    return load_pairs_tsv(path), set()


def load_local_gold(path: str | Path) -> list[tuple[str, str]]:
    """one `(src, gold_target)` per ranking query, in the canonical row order"""
    return [(row["SrcEntity"], row["TgtEntity"]) for row in read_tsv(path)]


def load_local_ranking(path: str | Path, candidate_count: int) -> list[tuple[str, list[str]]]:
    """
    per-query `(src, ranked_targets)` in the canonical query order. accepts either a
    `TgtCandidates` list cell per query (the list IS the ranking) or a scored block
    (`candidate_count` `(TgtEntity, Score)` rows per query, sorted best-first). the
    block form is validated SrcEntity-homogeneous + full-length so a ragged/misaligned
    block can't silently corrupt every later query's ranking.
    """
    rows = read_tsv(path)
    if rows and "TgtCandidates" in rows[0]:
        return [(row["SrcEntity"], parse_list(row["TgtCandidates"])) for row in rows]
    rankings: list[tuple[str, list[str]]] = []
    for start in range(0, len(rows), candidate_count):
        block = rows[start:start + candidate_count]
        sources = {row["SrcEntity"] for row in block}
        if len(sources) != 1:
            raise ValueError(f"local ranking block at row {start} spans multiple sources {sorted(sources)}; "
                             f"each query must be {candidate_count} consecutive rows for one source.")
        if len(block) != candidate_count:
            raise ValueError(f"local ranking block at row {start} has {len(block)} rows, expected {candidate_count}.")
        source = block[0]["SrcEntity"]
        if block[0].get("Score", "") != "":
            ranked = rank_by_score([(row["TgtEntity"], float(row["Score"])) for row in block])
        else:
            ranked = [row["TgtEntity"] for row in block]
        rankings.append((source, ranked))
    return rankings
