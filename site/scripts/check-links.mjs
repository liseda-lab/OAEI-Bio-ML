/**
 * Post-build link gate. Scans every built HTML page in dist/ and fails when:
 *   1. an internal href/src does not start with BASE_PATH (a link that would
 *      escape the GitHub Pages project subpath and 404), or
 *   2. an internal link's target does not exist in dist/ (a broken link).
 * External (http/https/mailto), fragment-only, and data: URLs are ignored.
 * Relative links — emitted only by the legacy docs/<year>/ campaign archives
 * copied in by scripts/copy-assets.mjs — are resolved against their page and
 * checked too, so the archives keep loading their stylesheets, results and
 * examples. Gaps that already exist in the archived content warn instead of
 * failing: the archives are served verbatim, not edited to satisfy the gate.
 * Runs automatically after `npm run build` (postbuild), locally and in CI.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { BASE_PATH } from '../site.config.mjs';

const DIST = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../dist');
if (!fs.existsSync(DIST)) {
  console.error('check-links: dist/ not found — run `npm run build` first.');
  process.exit(2);
}

const htmlFiles = [];
const walk = (dir) => {
  for (const f of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, f.name);
    if (f.isDirectory()) walk(full);
    else if (f.name.endsWith('.html')) htmlFiles.push(full);
  }
};
walk(DIST);

const targetExists = (urlPath) => {
  const rel = decodeURIComponent(urlPath.slice(BASE_PATH.length)).replace(/^\//, '');
  const p = path.join(DIST, rel);
  return (
    (fs.existsSync(p) && (fs.statSync(p).isFile() || fs.existsSync(path.join(p, 'index.html')))) ||
    fs.existsSync(p + '.html') ||
    fs.existsSync(p + '/index.html')
  );
};

// top-level /<year>/ pages are the legacy archives served verbatim
const isArchivePage = (page) => /^\/\d{4}\//.test(page);

let violations = 0;
let warnings = 0;
for (const file of htmlFiles) {
  const html = fs.readFileSync(file, 'utf8');
  const page = '/' + path.relative(DIST, file).split(path.sep).join('/');
  for (const m of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
    const url = m[1];
    if (/^(https?:|mailto:|data:|#)/i.test(url)) continue;
    const clean = url.split('#')[0].split('?')[0];
    if (!clean) continue;
    if (url.startsWith('/')) {
      if (BASE_PATH && !clean.startsWith(BASE_PATH + '/') && clean !== BASE_PATH) {
        console.error(`✗ ${page}: missing base prefix — ${url}`);
        violations++;
      } else if (!targetExists(clean)) {
        console.error(`✗ ${page}: broken internal link — ${url}`);
        violations++;
      }
    } else {
      // relative link: resolve against the page's directory; it must land on
      // a file inside dist/ (escaping dist/ would 404 on GitHub Pages even if
      // the path happens to exist locally)
      const target = path.resolve(path.dirname(file), decodeURIComponent(clean));
      const ok =
        target.startsWith(DIST + path.sep) &&
        fs.existsSync(target) &&
        (fs.statSync(target).isFile() || fs.existsSync(path.join(target, 'index.html')));
      if (!ok) {
        if (isArchivePage(page)) {
          console.warn(`⚠ ${page}: broken link in archived page (pre-existing) — ${url}`);
          warnings++;
        } else {
          console.error(`✗ ${page}: broken internal link — ${url}`);
          violations++;
        }
      }
    }
  }
}

if (violations) {
  console.error(`\ncheck-links: ${violations} violation(s) — failing the build.`);
  process.exit(1);
}
if (warnings) console.warn(`check-links: ${warnings} pre-existing gap(s) in archived pages (non-fatal).`);
console.log(`check-links: ${htmlFiles.length} pages scanned — all internal links base-prefixed and resolvable.`);
