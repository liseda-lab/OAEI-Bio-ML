// Central place for values that flip when the CodaBench competitions go live.
//
// OAEI Bio-ML runs TWO CodaBench competitions — one per scored subtrack:
//   CODABENCH_GLOBAL_URL  Track 1 · Subtrack 1 — Global equivalence alignment
//   CODABENCH_LOCAL_URL   Track 1 · Subtrack 2 — Local equivalence ranking
// Set each to its competition's public URL once published (see the CodaBench
// setup guide). Every "submission portal" link and call-to-action on the site
// renders from these constants; while a URL is null the site says that channel
// is "to be announced".
export const CODABENCH_GLOBAL_URL: string | null = 'https://www.codabench.org/competitions/17424/';
export const CODABENCH_LOCAL_URL: string | null = 'https://www.codabench.org/competitions/17423/';

// Path (repo-root-relative) of the CI-written live-leaderboard snapshot.
// The results page renders from it when it exists.
export const LIVE_RESULTS_REL = 'results/live/codabench.json';

// The Hugging Face dataset release (OAEI-ML org) — the canonical download
// location for the task data from the 2026 edition onward (edition tag 2026).
export const HF_DATASET = 'https://huggingface.co/datasets/OAEI-ML/bio-ml';

// The public track repository (GitHub) that backs this site and the CI.
export const GITHUB_REPO = 'https://github.com/liseda-lab/OAEI-Bio-ML';

// Prefix an internal absolute path with the deployment's base path
// (site/site.config.mjs → astro.config `base`). Every hand-written internal
// href/src in .astro files must go through this so the site works both at a
// domain root and under a GitHub Pages project subpath.
export const withBase = (path: string): string =>
  import.meta.env.BASE_URL.replace(/\/$/, '') + path;
