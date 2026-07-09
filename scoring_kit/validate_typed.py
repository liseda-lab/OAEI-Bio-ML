#!/usr/bin/env python3
"""
Validate a BioML 2026 TYPED ranking submission (Track 2). Stdlib only; no install.

BLOCK form: columns SrcEntity, TgtEntity, Relation, Score — 300 rows per query
(100 candidates x 3 relations), blocks in the SAME order as the released pool file
(the scorer recovers QueryID positionally). For each query every pool candidate must
appear once with each of the three relations. Entities are CURIEs (e.g. NCIT:C101044).

Usage:  python3 validate_typed.py POOL.track2.cands.tsv SUBMISSION.tsv [--candidate-count 100]
        (POOL is the released track2.<split>.cands.tsv, or track2.<split>.answers.tsv.)
"""
import argparse
import ast
import csv
import sys

RELATIONS = ("equivalent", "source_subsumed_by_target", "source_subsumes_target")


def parse_list(cell):
    cell = (cell or "").strip()
    return list(ast.literal_eval(cell)) if cell else []


def read_tsv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(pool_path, sub_path, candidate_count):
    problems = []
    pools = read_tsv(pool_path)
    sub = read_tsv(sub_path)
    if not sub:
        return ["submission is empty"]
    need = ("SrcEntity", "TgtEntity", "Relation", "Score")
    missing = [c for c in need if c not in sub[0]]
    if missing:
        return [f"typed submission needs columns {list(need)}; missing {missing} (got {list(sub[0].keys())})"]

    block = candidate_count * len(RELATIONS)  # 300
    if len(sub) != len(pools) * block:
        problems.append(f"expected {len(pools) * block} rows ({len(pools)} queries x {block}), got {len(sub)}")
    n = min(len(pools), len(sub) // block)
    for i in range(n):
        rows = sub[i * block:(i + 1) * block]
        psrc = pools[i]["SrcEntity"]
        pcands = set(parse_list(pools[i]["TgtCandidates"]))
        srcs = {r["SrcEntity"] for r in rows}
        if srcs != {psrc}:
            problems.append(f"query {i} ({psrc}): block sources {sorted(srcs)} != pool source")
            continue
        bad_rel = {r["Relation"] for r in rows} - set(RELATIONS)
        if bad_rel:
            problems.append(f"query {i} ({psrc}): invalid relation(s) {sorted(bad_rel)}")
        if {r["TgtEntity"] for r in rows} != pcands:
            got = {r["TgtEntity"] for r in rows}
            problems.append(f"query {i} ({psrc}): targets != pool candidates "
                            f"({len(got & pcands)} of {len(pcands)} match)")
        pairs = [(r["TgtEntity"], r["Relation"]) for r in rows]
        if len(pairs) != len(set(pairs)):
            problems.append(f"query {i} ({psrc}): duplicate (target, relation) rows")
        for r in rows:
            try:
                float(r["Score"])
            except (ValueError, TypeError):
                problems.append(f"query {i} ({psrc}): non-numeric Score {r.get('Score')!r}")
                break
    return problems


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pool", help="the released track2.<split>.cands.tsv (or .answers.tsv)")
    ap.add_argument("submission", help="your typed block submission")
    ap.add_argument("--candidate-count", type=int, default=100)
    args = ap.parse_args()
    problems = validate(args.pool, args.submission, args.candidate_count)
    if problems:
        print("INVALID submission:")
        for p in problems[:50]:
            print("  -", p)
        if len(problems) > 50:
            print(f"  ... and {len(problems) - 50} more")
        sys.exit(1)
    print("OK - typed ranking submission is valid.")
