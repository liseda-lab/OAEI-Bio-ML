#!/usr/bin/env python3
"""
Self-score a BioML 2026 LOCAL ranking submission (Track 1 / Subtrack 2) against public
gold — the SAME MRR + Hits@{1,5,10} the leaderboard reports. Zero-install (uses the
vendored oaei_bioml_eval alongside this script; pure standard library).

Usage:
  python3 score_local.py RANKING.tsv GOLD.tsv [--candidate-count 100] [--output scores.json]

GOLD is a per-query (SrcEntity, TgtEntity) TSV. The released local.valid.cands.tsv works
directly as GOLD (its SrcEntity/TgtEntity columns are the gold; extra columns are ignored).
You can only self-score the TRAIN/VALID splits — the test gold is held back for the
organiser-side leaderboard.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oaei_bioml_eval.equivalence.cli import main  # noqa: E402

if __name__ == "__main__":
    # forward to `oaei-bioml-equivalence-score local ...`
    raise SystemExit(main(["local"] + sys.argv[1:]))
