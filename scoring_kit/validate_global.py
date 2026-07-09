#!/usr/bin/env python3
"""
Validate a BioML 2026 GLOBAL alignment submission (Track 1 / Subtrack 1). Python 3 standard
library only; no install required. Accepts EITHER format the scorer accepts (RDF and TSV score
identically):

  * OAEI Alignment RDF/XML (.rdf/.xml/.owl): a root <rdf:RDF>, an <Alignment>, and one or more
    correspondences — each a typed <align:Cell> OR an untyped element carrying align:entity1 —
    with <entity1>/<entity2> as absolute IRIs via rdf:resource and an optional <relation>.
    Parsing is namespace-tolerant. See alignment.rng for an optional RelaxNG schema.
  * TSV (.tsv/.txt/.csv): a header with SrcEntity and TgtEntity columns (optional Relation, Score);
    each row two absolute IRIs.

BioML scores the reference RELATION-AGNOSTICALLY, so '=', '<', '>' (and '<=', '>=') are all valid
and counted — only structure/IRIs are checked here. Entities are full OWL IRIs.

Usage:  python3 validate_global.py SUBMISSION.{rdf,xml,owl,tsv}
"""
import csv
import os
import sys
import xml.etree.ElementTree as ET

RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDF_XML_SUFFIXES = (".rdf", ".xml", ".owl")


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _absolute(iri):
    return "://" in (iri or "")


def validate_rdf(path):
    problems = []
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, FileNotFoundError) as exc:
        return [f"cannot parse XML: {exc}"], 0
    if _local(root.tag) != "RDF":
        problems.append(f"root element should be rdf:RDF (found <{_local(root.tag)}>)")
    if not any(_local(el.tag) == "Alignment" for el in root.iter()):
        problems.append("no <Alignment> element found")
    n = seen = 0
    for element in root.iter():
        e1 = e2 = None
        for ch in element:
            t = _local(ch.tag)
            if t == "entity1":
                e1 = ch.get(f"{{{RDF}}}resource") or ch.get("resource")
            elif t == "entity2":
                e2 = ch.get(f"{{{RDF}}}resource") or ch.get("resource")
        if e1 is None and e2 is None:
            continue   # not a correspondence element (map/Alignment/entity wrappers)
        seen += 1
        if not e1 or not e2:
            problems.append(f"correspondence {seen}: missing entity1/entity2 rdf:resource")
            continue
        for name, iri in (("entity1", e1), ("entity2", e2)):
            if not _absolute(iri):
                problems.append(f"correspondence {seen}: {name} is not an absolute IRI: {iri!r}")
        n += 1
    if seen == 0:
        problems.append("no correspondences found (need <Cell>/<entity1><entity2>)")
    return problems, n


def validate_tsv(path):
    try:
        with open(path, newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
    except FileNotFoundError as exc:
        return [f"cannot open: {exc}"], 0
    if not rows:
        return ["empty TSV (need a header with SrcEntity, TgtEntity and at least one row)"], 0
    problems = [f"missing required column: {c}" for c in ("SrcEntity", "TgtEntity") if c not in rows[0]]
    if problems:
        return problems, 0
    n = 0
    for i, row in enumerate(rows, 1):
        src, tgt = row.get("SrcEntity"), row.get("TgtEntity")
        if not src or not tgt:
            problems.append(f"row {i}: missing SrcEntity/TgtEntity")
            continue
        for name, iri in (("SrcEntity", src), ("TgtEntity", tgt)):
            if not _absolute(iri):
                problems.append(f"row {i}: {name} is not an absolute IRI: {iri!r}")
        n += 1
    return problems, n


def validate(path):
    suffix = os.path.splitext(path)[1].lower()
    return validate_rdf(path) if suffix in RDF_XML_SUFFIXES else validate_tsv(path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python3 validate_global.py SUBMISSION.{rdf,xml,owl,tsv}")
    problems, n = validate(sys.argv[1])
    if problems:
        print("INVALID submission:")
        for p in problems[:50]:
            print("  -", p)
        if len(problems) > 50:
            print(f"  ... and {len(problems) - 50} more")
        sys.exit(1)
    print(f"OK - {n} correspondence(s) found (duplicates are de-duplicated at scoring time).")
