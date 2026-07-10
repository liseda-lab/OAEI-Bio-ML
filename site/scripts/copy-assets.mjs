/**
 * Copies the repository's downloadable assets into site/public/ so the built
 * site serves them at their existing repo-relative URLs. Unlike default Jekyll,
 * this pipeline has no underscore exclusions, so every path publishes as-is.
 *
 * OAEI Bio-ML re-hosts NO task data or ontologies: the biomedical ontologies
 * are already published elsewhere, and the task splits live on the (gated)
 * Hugging Face dataset. So this step only publishes the small, redistributable
 * pieces that exist at the repo root — the organiser-baseline leaderboard, any
 * CI-written live results, the licence, (if present) the participant validator
 * scripts, and the archived docs/<year>/ campaign pages at their original
 * URLs. Every source is guarded: a missing one is skipped, never fatal.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { CNAME } from '../site.config.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const PUB = path.resolve(HERE, '../public');

const jobs = [
  { from: 'leaderboard.json', to: 'leaderboard.json' },
  { from: 'reference_coherence.json', to: 'reference_coherence.json' },
  { from: 'results', to: 'results' },
  { from: 'LICENSE', to: 'LICENSE' },
];

// CNAME comes from site.config.mjs: written for a custom-domain deployment,
// absent for a GitHub Pages project site (where a stray CNAME would break it).
fs.rmSync(path.join(PUB, 'CNAME'), { force: true });
if (CNAME) fs.writeFileSync(path.join(PUB, 'CNAME'), CNAME + '\n');

// scripts/: participants download the validators (.py) and any schema (.rng).
// The BioML scoring kit ships from the Hugging Face dataset, so a root
// scripts/ dir may be absent in this repo — tolerate that.
const scriptsDir = path.join(ROOT, 'scripts');
if (fs.existsSync(scriptsDir)) {
  for (const f of fs.readdirSync(scriptsDir)) {
    if (/\.(py|rng)$/.test(f)) jobs.push({ from: `scripts/${f}`, to: `scripts/${f}` });
  }
}

// docs/: the previous GitHub Pages site was served from this folder, so its
// campaign archives lived at /<year>/... — keep those URLs alive by publishing
// each docs/<year>/ folder at the site root, along with the shared assets the
// year pages reference relatively (../style.css, ../oaeismall.jpg). The legacy
// docs/index.html is deliberately NOT copied: the Astro homepage owns / now,
// which is also where the year pages' "../index.html" back-links land.
const docsDir = path.join(ROOT, 'docs');
if (fs.existsSync(docsDir)) {
  for (const f of fs.readdirSync(docsDir)) {
    if (/^\d{4}$/.test(f) || /\.(css|jpg|png)$/.test(f)) jobs.push({ from: `docs/${f}`, to: f });
  }
}

let n = 0;
for (const { from, to } of jobs) {
  const src = path.join(ROOT, from);
  const dest = path.join(PUB, to);
  if (!fs.existsSync(src)) {
    console.warn(`copy-assets: missing ${from} — skipped`);
    continue;
  }
  // clean first so files deleted/renamed in the repo stop being served
  fs.rmSync(dest, { recursive: true, force: true });
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.cpSync(src, dest, { recursive: true });
  n++;
}
console.log(`copy-assets: ${n} asset roots copied into site/public/`);
