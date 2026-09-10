import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync } from 'node:fs';

const pages = readdirSync('dist', { recursive: true }).filter(file => file.endsWith('.html'));
assert(pages.length > 0, 'Build the site first');
for (const file of pages) {
  const html = readFileSync(`dist/${file}`, 'utf8');
  assert.equal((html.match(/<main\b/g) ?? []).length, 1, `${file}: one main landmark`);
  assert.match(html, /<link rel="canonical" href="https:\/\/hitendra\.dev\//, `${file}: canonical`);
  assert.match(html, /href="\/projects"/, `${file}: projects navigation`);
  assert.match(html, /href="\/blog"/, `${file}: writing navigation`);
  assert.match(html, /href="\/contact"/, `${file}: contact navigation`);
  assert.doesNotMatch(html, /id="(?:ash|sun)"|data-eclipse/, `${file}: legacy presentation`);
  assert.match(html, /href="#content"/, `${file}: skip link`);
}
for (const route of ['index.html', 'projects/index.html', 'blog/index.html', 'contact/index.html', 'tldr/index.html', '404.html']) {
  assert(existsSync(`dist/${route}`), `Missing ${route}`);
}
for (const file of readdirSync('src/content/blog').filter(file => /\.mdx?$/.test(file))) {
  const frontmatter = readFileSync(`src/content/blog/${file}`, 'utf8').split('---')[1];
  const draft = /^draft:\s*true\s*$/m.test(frontmatter);
  const slug = file.replace(/\.mdx?$/, '');
  assert.equal(existsSync(`dist/blog/${slug}/index.html`), !draft, `${slug}: publication state`);
}
assert(!existsSync('dist/admin'), 'Admin must remain dev-only');
assert(existsSync('dist/resume.pdf'), 'Resume missing');
const projects = JSON.parse(readFileSync('src/data/projects.json', 'utf8'));
const home = readFileSync('dist/index.html', 'utf8');
const listing = readFileSync('dist/projects/index.html', 'utf8');
assert.equal((home.match(/data-project\b/g) ?? []).length, projects.filter(p => p.featured).slice(0, 3).length);
assert.equal((listing.match(/data-project\b/g) ?? []).length, projects.length);
assert.match(listing, /<details\b/, 'Project details must work without JavaScript');
console.log(`Static site checks passed (${pages.length} pages)`);
