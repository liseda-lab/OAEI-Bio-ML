/**
 * THE single place to change when the site moves between deployments.
 *
 * Production (GitHub Pages project site):
 *   SITE_ORIGIN = 'https://liseda-lab.github.io'
 *   BASE_PATH   = '/OAEI-Bio-ML'   // the repository subpath
 *   CNAME       = null             // project sites must NOT ship a CNAME file
 *
 * Draft (custom domain at the root):
 *   SITE_ORIGIN = 'https://bio-ml-draft.example.org'
 *   BASE_PATH   = ''
 *   CNAME       = 'bio-ml-draft.example.org'
 *
 * Everything else derives from these three values: Astro's site/base, every
 * internal link (via withBase in src/config.ts), the markdown link rewriter,
 * the asset-copy step (which writes the CNAME file), and the a11y audit
 * server. Do not hard-code the origin or base path anywhere else.
 */
export const SITE_ORIGIN = 'https://liseda-lab.github.io';
export const BASE_PATH = '/OAEI-Bio-ML';
export const CNAME = null;
