#!/usr/bin/env python3
"""
Pull the OAEI Bio-ML leaderboards from CodaBench and write the site's
live-results snapshot (results/live/codabench.json).

Runs inside the deploy workflow, before the site build. Uses only the
PUBLIC, unauthenticated CodaBench API:

    GET /api/competitions/<pk>/                    -> phase ids
    GET /api/phases/<pk>/get_leaderboard/?page_size=all

No credentials are needed (and none should be added — the admin results.*
endpoints are unnecessary for this).

OAEI Bio-ML runs TWO competitions, one per scored subtrack. Each is wired
through its own environment variable (competition pk):

    CODABENCH_GLOBAL_COMPETITION   Track 1 · Subtrack 1 — Global equivalence alignment
    CODABENCH_LOCAL_COMPETITION    Track 1 · Subtrack 2 — Local equivalence ranking

Any unset variable => that section is written empty. With NONE set the
script exits 0 without writing anything, so the workflow is a no-op until
the competitions exist (see the CodaBench setup guide).

Output schema (consumed by site/src/pages/results.astro and index.astro):
{
  "fetched_at": "<ISO-8601 UTC>",
  "competition_url": "https://www.codabench.org/competitions/<first-set-pk>/",
  "global": [ {"system", "team", "date", "scores": {<column_key>: float}} ],
  "local":  [ ... ]
}
Column keys come straight from the CodaBench leaderboard columns, which the
competition bundles define (e.g. macro_f1_repaired/global_coherence for
global, and macro_mrr/macro_hits_at_1 for local).
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

BASE = os.environ.get("CODABENCH_BASE", "https://www.codabench.org")
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "results", "live", "codabench.json")

# (output-section key, environment variable) in leaderboard-display order.
SECTIONS = (
    ("global", "CODABENCH_GLOBAL_COMPETITION"),
    ("local", "CODABENCH_LOCAL_COMPETITION"),
)


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "oaei-bio-ml-site-sync"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def leaderboard_rows(competition_pk):
    comp = get_json(f"{BASE}/api/competitions/{competition_pk}/")
    phases = comp.get("phases") or []
    if not phases:
        print(f"competition {competition_pk}: no phases; skipping", file=sys.stderr)
        return []
    rows = []
    for phase in phases:
        board = get_json(f"{BASE}/api/phases/{phase['id']}/get_leaderboard/?page_size=all")
        for sub in board.get("submissions", []):
            scores = {}
            for s in sub.get("scores", []):
                try:
                    scores[s["column_key"]] = float(s["score"])
                except (KeyError, TypeError, ValueError):
                    continue
            if not scores:
                continue
            facts = sub.get("fact_sheet_answers") or {}
            org = sub.get("organization")
            rows.append({
                "system": facts.get("system_name") or sub.get("owner") or "anonymous",
                "team": (org.get("name") if isinstance(org, dict) else org) or sub.get("owner"),
                "date": sub.get("created_when"),
                "scores": scores,
            })
    return rows


def main():
    pks = {key: os.environ.get(env, "").strip() for key, env in SECTIONS}
    if not any(pks.values()):
        print("CODABENCH_{GLOBAL,LOCAL}_COMPETITION unset — "
              "nothing to fetch (this is fine pre-launch)")
        return 0

    first_pk = next(pk for pk in pks.values() if pk)
    snapshot = {
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "competition_url": f"{BASE}/competitions/{first_pk}/",
    }
    for key, _ in SECTIONS:
        snapshot[key] = leaderboard_rows(pks[key]) if pks[key] else []

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(snapshot, f, indent=1)
    print(f"wrote {os.path.normpath(OUT)}: " + ", ".join(
        f"{len(snapshot[key])} {key} rows" for key, _ in SECTIONS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
