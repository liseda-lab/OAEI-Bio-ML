#!/usr/bin/env python3
"""
Self-score a BioML 2026 TYPED ranking submission (Track 2) against public gold answers —
the SAME Preferred Typed-MRR + Hierarchy-aware Typed-nDCG@10 the leaderboard reports.
Zero-install (uses the vendored oaei_bioml_eval alongside this script; pure stdlib).

Usage:
  python3 score_typed.py PREDICTIONS.tsv ANSWERS.tsv \
      [--preferred track2.valid.preferred.tsv] [--graded track2.valid.graded.tsv] \
      [--candidate-count 100] [--k 10] [--output scores.json]

ANSWERS / PREFERRED / GRADED are the released track2.<split>.{answers,preferred,graded}.tsv.
You can only self-score TRAIN/VALID — the test gold is held back for the leaderboard.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oaei_bioml_eval.typed.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
