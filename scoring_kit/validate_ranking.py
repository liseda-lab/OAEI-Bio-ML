#!/usr/bin/env python3
"""
Validate a BioML 2026 LOCAL ranking submission (Track 1 / Subtrack 2). Stdlib only.

Two accepted layouts (the scorer reads either):
  * LIST form  — columns: SrcEntity, TgtCandidates   (one row per query; TgtCandidates
                 is a Python-list literal of the ranked candidate IRIs, best first)
  * BLOCK form — columns: SrcEntity, TgtEntity[, Score]   (CANDIDATE_COUNT consecutive
                 rows per query; if Score is present, rows are sorted by score at scoring)

Validation is POSITIONAL: your submission's queries must be in the SAME order as the
released pool file (the scorer pairs them by position), and each query's ranking must be
a PERMUTATION of that query's frozen 100-candidate pool. Entities are full OWL IRIs.

Usage:  python3 validate_ranking.py POOL.cands.tsv SUBMISSION.tsv [--candidate-count 100]
        (POOL is the released local.<split>.cands.tsv you ranked.)
"""
import argparse
import ast
import csv
import sys


def parse_list(cell):
    cell = (cell or "").strip()
    return list(ast.literal_eval(cell)) if cell else []


def read_tsv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _rankings_from_submission(rows, candidate_count, problems):
    """-> list of (SrcEntity, [ranked targets]) in submission order, or [] on fatal error."""
    if not rows:
        problems.append("submission is empty")
        return []
    header = rows[0].keys()
    out = []
    if "TgtCandidates" in header:
        for i, r in enumerate(rows, 1):
            try:
                out.append((r["SrcEntity"], parse_list(r["TgtCandidates"])))
            except (ValueError, SyntaxError) as exc:
                problems.append(f"row {i} ({r.get('SrcEntity')}): TgtCandidates is not a valid list ({exc})")
        return out
    if "TgtEntity" not in header:
        problems.append(f"block submission needs columns SrcEntity, TgtEntity[, Score]; got {list(header)}")
        return []
    for start in range(0, len(rows), candidate_count):
        block = rows[start:start + candidate_count]
        srcs = {b["SrcEntity"] for b in block}
        if len(srcs) != 1:
            problems.append(f"block at row {start + 1}: spans multiple sources {sorted(srcs)}")
            out.append((None, []))
            continue
        src = block[0]["SrcEntity"]
        if all(b.get("Score", "") != "" for b in block):
            try:
                ranked = [b["TgtEntity"] for b in sorted(block, key=lambda b: -float(b["Score"]))]
            except ValueError:
                problems.append(f"block at row {start + 1} ({src}): non-numeric Score")
                ranked = [b["TgtEntity"] for b in block]
        else:
            ranked = [b["TgtEntity"] for b in block]
        out.append((src, ranked))
    return out


def validate(pool_path, sub_path, candidate_count):
    problems = []
    pool_rows = read_tsv(pool_path)
    sub_rows = read_tsv(sub_path)
    rankings = _rankings_from_submission(sub_rows, candidate_count, problems)
    if not rankings:
        return problems or ["submission produced no rankings"]
    if len(rankings) != len(pool_rows):
        problems.append(f"submission has {len(rankings)} queries, the pool has {len(pool_rows)} "
                        "(one ranking per pool query, in the same order)")
    for i, (src, ranking) in enumerate(rankings):
        if i >= len(pool_rows):
            break
        pool = parse_list(pool_rows[i]["TgtCandidates"])
        psrc = pool_rows[i]["SrcEntity"]
        if src is not None and src != psrc:
            problems.append(f"query {i + 1}: SrcEntity {src!r} != pool SrcEntity {psrc!r} (order mismatch)")
        if len(ranking) != len(pool) or set(ranking) != set(pool):
            problems.append(f"query {i + 1} ({psrc}): ranking must be a permutation of its {len(pool)} "
                            f"pool candidates (got {len(ranking)}, {len(set(ranking) & set(pool))} in common)")
    return problems


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pool", help="the released local.<split>.cands.tsv you ranked")
    ap.add_argument("submission", help="your ranking submission")
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
    print("OK - local ranking submission is valid.")
