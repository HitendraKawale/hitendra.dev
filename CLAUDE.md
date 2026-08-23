# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev       # Dev server at localhost:4321
npm run build     # Production build → ./dist/
npm run preview   # Preview the production build locally
```

No lint or test commands exist.

## Vercel deployment

Live at **https://hitendra.dev**, hosted on Vercel — pushes to `main` deploy automatically.

Static output, no adapter needed. `vercel.json` pins `buildCommand: npm run build` and `outputDirectory: dist`; Astro is auto-detected otherwise. The domain was bought through Vercel, so Vercel is registrar and nameserver both — there are no DNS records to hand-manage and TLS renews itself.

`site` in `astro.config.mjs` must stay in sync with the live domain: `BaseLayout` resolves every page's `<link rel="canonical">` and `og:url` against it, so a stale value silently points the whole site's canonicals at the wrong host.

## Architecture

Multi-page Astro 6 portfolio. Four routes:

| Route | File |
|---|---|
| `/` | `src/pages/index.astro` |
| `/projects` | `src/pages/projects.astro` |
| `/blog` | `src/pages/blog/index.astro` |
| `/blog/[slug]` | `src/pages/blog/[slug].astro` |

There is also a `404.astro`.

**Layouts:**
- `BaseLayout.astro` — shell (`<head>`, `AshCanvas`, `Rail`, `Nav`, `<main>`, `Footer`, the Eclipse overlay) plus **all site JavaScript** in one `<script>`. Requires `title` and `description` props.
- `PostLayout.astro` — wraps `BaseLayout` for blog posts. Takes `frontmatter`, plus `minutes` (reading time) and `prev`/`next` adjacent-post props supplied by `[slug].astro`. Never referenced from markdown frontmatter.

**Components:** `Nav`, `Footer`, `Rail`, `Behelit`, `AshCanvas`, `Marquee`, `ProjectIndex`, `ProjectCard`, `BlogCard`, `Brand`. All self-contained with scoped `<style>` blocks.

## The Chronicle — design direction

The site is a **bound volume**: engraved, printed, ink-on-paper — not a glowing dark UI. Berserk identity is explicit and deliberate; do not "professionalize" it away.

- `Brand.astro` — Brand of Sacrifice sigil (`currentColor`, `size` prop) in nav, rail, footer, chapter caps, post end-marks, favicon.
- **Naming:** Armoury (/projects), Chronicles (/blog), Send Word (/contact). Sections are numbered chapters. Project cards are "plates". Empty states reference the Dragonslayer.
- **The spine (`Rail.astro`)** — fixed left binding edge shown at ≥1080px (`body { padding-left: var(--rail-w) }`), carrying the sigil, a vertical running head, and a scroll-progress line.
- **The Behelit (`Behelit.astro`)** — nav toggle that fires the Eclipse: a black sun swallows the screen (`#sun` in `BaseLayout`), then `data-eclipse` is set on `<html>`, swapping the whole palette. Persisted in `localStorage` and restored pre-paint by an inline head script.
- **The Tongues interlude** (home) — a bone-parchment page pasted into the black volume, cycling greetings through all eight of his languages. Full colour inversion is the point; keep it.
- **Signature type treatment** — the hero/masthead display lines use a `background-clip: text` gradient so the type reads as *lit by the eclipse* (bone on the left, blood on the right).

### Design tokens

In `src/styles/global.css`, imported once by `BaseLayout`. `:root[data-eclipse]` redefines the same names for the Eclipse state, so **use the tokens** — anything hardcoded won't transform.

| Token | Value | Usage |
|---|---|---|
| `--void` | `#0a0806` | Page ground (warm near-black) |
| `--pitch` | `#000000` | Gutters, panel caps |
| `--soot` / `--soot-2` | `#12100c` / `#1a1611` | Panel fill / elevated fill |
| `--bone` | `#ece4d4` | Primary text |
| `--ash` / `--ash-dim` | `#8a8175` / `#5d574e` | Secondary / tertiary text |
| `--line` | `#2a2419` | Hairlines (the only border weight) |
| `--blood` / `--blood-hi` | `#93171b` / `#cf3520` | Accent, hover, blood floods |
| `--brass` / `--brass-dim` | `#c8a24a` / `#7d6528` | Gold leaf — numerals, plate marks |
| `--paper` / `--paper-ink` | `#e4dac2` / `#14110c` | The parchment insert |
| `--display` | Bodoni Moda | Headings, engraved plate type |
| `--body` | Spectral | Body copy |
| `--mono` | IBM Plex Mono | Labels, metadata, technical text |
| `--han` | Noto Serif SC | 泽贤 name seal |
| `--rail-w` / `--nav-h` | `68px` / `68px` | Spine width / nav height |
| `--measure` | `1180px` | Content width (`.wrap`) |

Fonts load from Google Fonts in `BaseLayout`; the Noto Serif SC request is glyph-subset via `&text=` so the CJK seal costs almost nothing.

### Shared utilities

`.wrap` (content column), `.bleed` (full width), `.label` + `.label-brass`/`-blood`/`-ash` (mono eyebrows, written as `[ Bracketed ]`), `.numeral`, `.chapter` head, `.rule`, `.blade` (underline-on-hover link), `.tone` (halftone screentone), `.hatch` (engraver's cross-hatch, inherits `currentColor`).

### Reveals — read this before adding one

`[data-reveal="rise"|"wipe"]` + `--d` for stagger; a single IntersectionObserver in `BaseLayout` adds `.in`. **The observed element must keep a non-zero visible box**, or the observer never fires. That is why `wipe` is declared on the overflow-hidden mask and animates its child — never put a reveal on something that starts clipped to nothing (`clip-path`, `scaleX(0)`, or translated outside a clipping parent).

## Home page content selection

`src/pages/index.astro` renders:
- **Featured projects**: `projects.filter(p => p.featured)` — up to 3 recommended
- **Recent posts**: 3 latest non-draft posts, sorted descending by date

## Content — how to update things

### Local admin panel (preferred)
Run `npm run dev` and open `http://localhost:4321/admin`. The "Scriptorium" panel adds/deletes projects and blog posts by writing the repo files directly — commit and push afterwards to publish. The panel is **dev-only**: its routes are injected by the inline `localAdmin` integration in `astro.config.mjs` only when `command === 'dev'`, so the production build contains no trace of it. Code lives in `src/admin/` (`panel.astro` + `api/projects.ts` + `api/posts.ts`), deliberately outside `src/pages/` so it never auto-routes.

`src/content/blog/scriptorium-seed.md` is a permanent `draft: true` post that must not be deleted: if the blog collection is empty when `astro dev` starts, the glob loader never registers its file watcher and newly added posts don't appear until a restart. The admin API refuses to delete it and the panel hides it; drafts never render publicly.

### Add a project (manually)
Edit `src/data/projects.json` — append to the array (`src/data/projects.ts` just re-exports it with types; the admin API writes this JSON). Set `featured: true` to show it on the home page (keep to ≤3). Status must be `"Built" | "Research" | "In Progress"`. `href` is optional.

### Add a blog post (manually)
Create a Markdown file in `src/content/blog/your-slug.md`. Required frontmatter:

```md
---
title: "Post title"
description: "One-line summary shown in cards."
date: 2025-06-01
tags: ["Tag1", "Tag2"]   # optional
draft: false              # set true to hide
---
```

The filename becomes the URL slug (e.g., `my-post.md` → `/blog/my-post`). Do not add a `layout:` key — `[slug].astro` wires the layout automatically via the content layer.

### Update personal info, skills, languages
Edit `src/data/profile.ts`. All pages pull from this single source.

## Content collections

Blog uses the Astro content layer with a `glob` loader (`src/content.config.ts`). The collection is typed — adding a post with missing required frontmatter will fail the build, which is intentional. Drafts are filtered out at query time via `getCollection("blog", ({ data }) => !data.draft)`.
