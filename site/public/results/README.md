# Archived results by edition

- `results/<year>/leaderboard.json` — the machine-readable baselines-and-results snapshot for each edition, in the same schema as the repo-root `leaderboard.json` (which the website's baselines page renders at build time).
  - `2026/leaderboard.json` — the 2026 baselines, frozen when the 2026 evaluation closed (identical to the root `leaderboard.json`). The final 2026 participant results are in the repo-root `participant_results.json`, served at `/participant_results.json`.
- `results/live/codabench.json` — written by CI from the CodaBench leaderboard during the evaluation window; not hand-edited. The website's results page renders from this file when it exists and no `participant_results.json` does. The CI sync is disabled outside the evaluation window (see `.github/workflows/deploy.yml`).
