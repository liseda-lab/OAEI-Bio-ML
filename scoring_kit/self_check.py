#!/usr/bin/env python3
"""
Self-check gate for the BioML 2026 scoring kit. Builds ORACLE submissions from the
PUBLIC valid split and confirms the vendored scorer returns perfect scores — proving
the kit and your downloaded data are self-consistent before you trust a real score.

  Local  (Subtrack 2): oracle ranking, gold ranked first  ->  MRR = Hits@1 = 1.0
  Typed  (Track 2):    oracle block, gold pair scored 1.0  ->  preferred_typed_mrr = Hits@1 = 1.0

Usage:  python3 self_check.py --data PUBLIC_DATA_DIR
                              [--pairs NCIT-DOID,SNOMED-FMA,SNOMED-NCIT]
PUBLIC_DATA_DIR holds per-pair dirs, each with local.valid.cands.tsv and
track2.valid.{answers,preferred,graded}.tsv.
"""
import argparse
import csv
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oaei_bioml_eval.io import parse_list, read_tsv           # noqa: E402
from oaei_bioml_eval.equivalence.report import score_local_files  # noqa: E402
from oaei_bioml_eval.typed.report import score_files          # noqa: E402
from oaei_bioml_eval.typed.metrics import DEFAULT_RELATIONS   # noqa: E402


def _write(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        w = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(rows)


def check_local(pair_dir, tmp):
    valid = list(read_tsv(os.path.join(pair_dir, "local.valid.cands.tsv")))
    gold = os.path.join(tmp, "gold.tsv")
    sub = os.path.join(tmp, "oracle.tsv")
    _write(gold, [{"SrcEntity": r["SrcEntity"], "TgtEntity": r["TgtEntity"]} for r in valid],
           ["SrcEntity", "TgtEntity"])

    def oracle(r):
        cands = parse_list(r["TgtCandidates"])
        g = r["TgtEntity"]
        return {"SrcEntity": r["SrcEntity"], "TgtCandidates": repr([g] + [c for c in cands if c != g])}

    _write(sub, [oracle(r) for r in valid], ["SrcEntity", "TgtCandidates"])
    m = score_local_files(sub, gold, candidate_count=100)
    ok = abs(m["mrr"] - 1.0) < 1e-9 and abs(m["hits_at_1"] - 1.0) < 1e-9
    return ok, f"mrr={m['mrr']:.4f} hits@1={m['hits_at_1']:.4f} queries={int(m['queries'])}"


def check_typed(pair_dir, tmp):
    answers_path = os.path.join(pair_dir, "track2.valid.answers.tsv")
    answers = list(read_tsv(answers_path))
    sub = os.path.join(tmp, "typed_oracle.tsv")
    rows = []
    for r in answers:
        cands = parse_list(r["TgtCandidates"])
        gtgt, grel = r["TgtEntity"], r["Relation"]
        for tgt in cands:
            for rel in DEFAULT_RELATIONS:
                rows.append({"SrcEntity": r["SrcEntity"], "TgtEntity": tgt, "Relation": rel,
                             "Score": "1.0" if (tgt == gtgt and rel == grel) else "0.0"})
    _write(sub, rows, ["SrcEntity", "TgtEntity", "Relation", "Score"])
    kw = {"candidate_count": 100}
    pref = os.path.join(pair_dir, "track2.valid.preferred.tsv")
    grad = os.path.join(pair_dir, "track2.valid.graded.tsv")
    if os.path.exists(pref):
        kw["preferred_pairs_path"] = pref
    if os.path.exists(grad):
        kw["graded_relevance_path"] = grad
    m = score_files(sub, answers_path, **kw)
    ok = abs(m["preferred_typed_mrr"] - 1.0) < 1e-9 and abs(m["preferred_typed_hits_at_1"] - 1.0) < 1e-9
    return ok, (f"preferred_typed_mrr={m['preferred_typed_mrr']:.4f} "
                f"hits@1={m['preferred_typed_hits_at_1']:.4f} "
                f"hnDCG@10={m.get('hierarchy_aware_typed_ndcg_at_10', float('nan')):.4f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="public dataset dir with per-pair subdirs")
    ap.add_argument("--pairs", default="NCIT-DOID,SNOMED-FMA,SNOMED-NCIT")
    args = ap.parse_args()
    all_ok = True
    ran_any = False
    for pair in args.pairs.split(","):
        pair_dir = os.path.join(args.data, pair)
        if not os.path.isdir(pair_dir):
            print(f"[skip] {pair}: not found under {args.data}")
            continue
        ran_any = True
        with tempfile.TemporaryDirectory() as tmp:
            lok, lmsg = check_local(pair_dir, tmp)
            tok, tmsg = check_typed(pair_dir, tmp)
        print(f"[{'PASS' if lok else 'FAIL'}] {pair} local  {lmsg}")
        print(f"[{'PASS' if tok else 'FAIL'}] {pair} typed  {tmsg}")
        all_ok = all_ok and lok and tok
    if not ran_any:
        print("no pairs found — check --data path")
        return 2
    print("\nSELF-CHECK:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
