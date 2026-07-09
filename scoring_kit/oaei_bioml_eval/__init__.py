"""
Common evaluation logic for the OAEI Bio-ML tracks.

Consumed by both the public participant scoring kit and the organiser-side
evaluation, so the same code produces both a participant's local scores and
the official leaderboard numbers.

Surface:

  equivalence/   Track 1 P/R/F1 (global) + MRR/H@k (local), DeepOnto-backed,
                 plus the official reasoner-based coherence (organiser-side)

  typed/         Track 2 Preferred Relation-Aware Typed MRR + H-nDCG@10,
                 dependency-free, seeded from BioKG-Align's scorer
                 
  coherence/     a lightweight STRUCTURAL coherence proxy for participant
                 self-guidance (named distinctly from the official value)
"""

__version__ = "0.1.0.dev0"
