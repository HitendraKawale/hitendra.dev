# Quiet gallery implementation plan

> **For agentic workers:** Use `executing-plans` or `subagent-driven-development` after approval. Steps use checkboxes for tracking. Do not commit, push, or deploy without separate permission.

**Goal:** Replace the current uniform portfolio styling with the approved quiet-gallery design across all public pages, without changing content or routes.

**Architecture:** Keep Astro's shared `BaseLayout`, tokenized global CSS, and page-local styles. Spend visual emphasis on the homepage hero; keep work and writing as accessible rows. No new runtime dependency or content model.

**Tech stack:** Astro 6, CSS, existing static and Agent Browser checks.

**Spec:** `docs/superpowers/specs/2026-10-02-quiet-gallery-redesign.md`

## Context

The current site is readable, but the same typographic scale and bordered-row treatment make the hero, projects, and writing feel alike. The redesign changes composition and visual hierarchy, not the site's factual content or behavior.

## Approach

```text
Before  shared neutral tokens -> uniform headings/sections -> similar rows
After   mineral tokens -> asymmetric home introduction -> quiet evidence rows
                       -> matching interior pages and narrow articles
```

## Files to modify

| File | Current role | Planned decision |
| --- | --- | --- |
| `src/styles/global.css` | Shared palette, type and spacing | Set exact light/dark mineral tokens, distinct display scale, section rhythm and print palette; preserve accessible focus/reduced motion |
| `src/pages/index.astro` | Home content and hero | Split introduction into large statement and compact credentials; keep real featured work, writing and about content |
| `src/components/Nav.astro` | Visible responsive navigation | Give name and links more deliberate spacing; retain current-link semantics and toggle |
| `src/components/Footer.astro` | Contact and archive links | Simplify visual weight; keep all outgoing links |
| `src/components/ProjectCard.astro` | Native details and evidence row | Lead with project title and subtitle; put status opposite title and stack below; retain source link and details |
| `src/components/BlogCard.astro` | Dated article row | Give title more emphasis than the date; preserve description and tags |
| `src/layouts/PostLayout.astro` | 68ch article with code/table overflow | Bring headings and metadata into the display scale; retain prose measure and overflow |
| `src/pages/contact.astro` | Email/copy, resume and profiles | Give email first visual priority; keep all actions and status feedback |
| `src/pages/tldr.astro` | Two-column printable profile | Bring page head and rules into the new system; retain facts and print density |
| `src/layouts/BaseLayout.astro` | Pre-paint theme, metadata and shared script | Match both theme-color values to the new backgrounds; leave scripts unchanged |
| `scripts/check-site.mjs` | Static route/content checks | Keep existing checks; add a small assertion for new home structure |
| `scripts/check-browser.py` | Theme, copy and responsive checks | Keep existing flow and add writing/quick-profile screenshots and theme-color assertions |

## Reuse

- `BaseLayout.astro` already handles the saved theme, clipboard status, metadata and skip link.
- `global.css` already exposes semantic color/type/layout tokens and reduced-motion rules.
- `ProjectCard.astro` uses native `<details>`; `BlogCard.astro` preserves post dates, tags and slugs.
- `scripts/check-site.mjs` verifies generated routes, projects and publication state. `scripts/check-browser.py` checks theme, copy, keyboard details and overflow.

## Decisions shown as diffs

The CSS scale, not a new component framework, carries the identity:

```diff
- --bg: #fafaf8; --text: #20252b; --accent: #315d8a;
+ --bg: #F1F5F3; --surface: #FFFFFF; --text: #15343B;
+ --muted: #4B6569; --accent: #006D77; --border: #C5D5D2;
- [data-theme="dark"] --bg: #151719;
+ [data-theme="dark"] --bg: #10262C; --surface: #19343A;
+ [data-theme="dark"] --text: #E8F2F0; --muted: #B3C8C6;
+ [data-theme="dark"] --accent: #76CED0; --border: #39555A;
```

Light ink, muted and accent contrast against the new background is 12.04:1, 5.68:1 and 5.53:1; dark counterparts are 13.77:1, 8.98:1 and 8.62:1. Rules are decorative, not the sole control indicator. Keep accent outlines for buttons/focus. Set `--accent-hi` to `#004F58` light and `#ACE8E5` dark; set `--surface-2` to `#E4ECE9` light and `#254047` dark. Update print colors to preserve legibility. Verify all control and hover combinations against their actual backgrounds.

The home is the only intentionally dramatic composition. The statement is copy, not a new credential:

```diff
- <section class="intro section"><h1>{profile.bio}</h1>
+ <section class="intro section">
+   <div class="intro-main"><p class="intro-name">{profile.name}</p>
+     <h1>I build AI systems that hold up outside the demo.</h1></div>
+   <div class="intro-aside">MSc AI, Surrey; LLM systems, retrieval and 3D vision;
+     existing availability and actions</div>
```

Preserve `profile.bio` for metadata. Do not alter measured project claims. Use `grid-template-columns: minmax(0, 1.5fr) minmax(230px, 1fr)` on wide screens and one column below 760px. Set the home heading to `clamp(3rem, 6vw, 5.5rem)` with about 11ch max measure; keep the rest of the site at a quieter scale. Ensure the contact action stays above the fold at 390 × 844 or change the layout, not the test. Keep text in HTML; no animation or script for reveal.

Use the existing row components and shared page primitives, not parallel versions:

```diff
- .project { padding-block: 28px; border-top: 1px solid var(--border); }
+ .project { padding-block: 36px; border-top: 1px solid var(--border); }
+ .project h3 { font-size: clamp(1.25rem, 2vw, 1.6rem); }
- .entry { grid-template-columns: 120px minmax(0, 1fr); }
+ .entry { grid-template-columns: 100px minmax(0, 1fr); }
+ .entry h3 { font-size: 1.35rem; }
```

Status stays opposite the title, the stack and native details stay below. The date stays in its own column on desktop and stacks above the title on mobile. No second renderer.

Keep `page-head`, `section`, `section-head`, `wrap`, `.stack` and `.actions` as shared hooks. Projects, blog index and 404 already use those hooks, so do not edit their markup. Contact gets a larger email link via local CSS, quick profile gets adjusted head spacing, and PostLayout gets a larger article title. Do not rewrite data queries, route content, or the admin. The only shared script edit is the theme-color string in `BaseLayout`, alongside the initial metadata value:

```diff
- <meta name="theme-color" content="#fafaf8" />
+ <meta name="theme-color" content="#F1F5F3" />
- meta.content = dark ? "#151719" : "#fafaf8";
+ meta.content = dark ? "#10262C" : "#F1F5F3";
```

The inline pre-paint dark branch also sets `#10262C`. Extend `scripts/check-site.mjs` with `assert.match(home, /class="intro-main"/)` and `assert.match(home, /class="intro-aside"/)`. Extend the browser screenshot route list from home/projects/contact/SAGA to include `/blog` and `/tldr`, and assert the `<meta name="theme-color">` tracks the theme.

## Steps

### 1. Baseline and shared design

- [ ] Run `npm run build && node scripts/check-site.mjs`; capture baseline home/project/post screenshots at 390 × 844 and 1440 × 900 in light/dark.
- [ ] Add one static check for the new home introduction (`.intro-main` and `.intro-aside`); run it against baseline to confirm failure.
- [ ] Change global tokens/type/spacing and the two `theme-color` values in `BaseLayout`; update nav/footer local spacing. Check light/dark text and control contrast and the existing toggle.

### 2. Public pages

- [ ] Recompose `index.astro` and restyle ProjectCard/BlogCard. Keep all content queries and links. Verify home on mobile/desktop, including the existing above-fold action check.
- [ ] Apply local typography to PostLayout, contact and quick profile; projects, blog index and 404 inherit the shared CSS without markup edits.
- [ ] Compare route/content counts against baseline and inspect article code/table overflow, print quick profile and keyboard-accessible native details.

### 3. Full verification and review

- [ ] Run production build and full static/browser checks; inspect screenshots of every public page type in both themes and check console errors. Confirm page count and published slugs match baseline.
- [ ] Check git diff for unchanged project data, articles, admin code and resume; only the two verification scripts change. Open `/plannotator-review` for the implementation diff; stop for annotations. No commit or deployment.

## Verification

Run `npm run build && node scripts/check-site.mjs`. Check `portless --help`, `portless list`, and Node version before starting a background local production preview; use a distinct named URL or an unused pinned port. Then run `python3 scripts/check-browser.py <preview-url>` with installed Agent Browser. Capture 390px and 1440px screenshots for home, projects, writing, an article, contact and quick profile in both themes. Verify no horizontal overflow at 320px, links/details without JS, keyboard focus, contrast, reduced motion, browser errors and the updated `theme-color`. Compare against baseline and report the exact URL and command outputs. Browser checks cannot substitute for visual review; report any blocker.

## Not doing

No new pages, fonts downloaded at runtime, UI framework, animation library, project schema, article rewrite, admin redesign, assets refresh, commit, push, or deployment.
