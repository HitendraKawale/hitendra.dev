# Castle portfolio implementation plan

> **For agentic workers:** Execute only after Plannotator approval. Use `executing-plans` and track checkboxes. Do not commit, push, or deploy without separate permission.

**Goal:** Replace the small 3D wireframe with a full-viewport Japanese castle on home, plus restrained 3D views on Projects and Writing; preserve readable content and no-WebGL fallback.

**Architecture:** One original procedural Three.js castle renderer with `hero`/`accent` variants, mounted only on three routes. The hero gets a full-bleed viewport-height section while the remaining content keeps the existing `.wrap`. A local SVG silhouette shows before WebGL initializes or when it cannot. No ThreeUI source, assets, or exact reproduction.

**Tech stack:** Astro 6, installed Three.js, CSS, Node static checker, Agent Browser.

**Spec:** `docs/superpowers/specs/2026-10-02-castle-portfolio.md`

## Context and approach

The prior approved worktree `redesign/quiet-gallery` already contains a small `DepthField.astro` hero and the supporting Three.js dependency. The user wants the castle to dominate the homepage, not sit in a framed aside. The current main stays constrained to 1040px, so merely enlarging the canvas inside `.intro-aside` cannot do that. Keep server-rendered copy outside the renderer and replace the small scene at its source.

```text
Before  home: [large text] | [tiny wireframe + credentials]
After   home: [full-width first viewport: text | castle landscape]
        below: [selected work / writing / about in original measure]
        lists: [title | small castle camera crop] -> unchanged rows
Failure home: [text | static castle silhouette], no missing links
```

## Files to modify

| File | Today | Decision |
| --- | --- | --- |
| `src/components/DepthField.astro` | One wireframe in small canvas | Replace with `src/components/CastleScene.astro`; single original procedural tower, hero/accent camera framing, theme, motion, resize and GPU cleanup |
| `public/castle-fallback.svg` (new) | No castle fallback | Original flat castle silhouette usable before JS and when WebGL is blocked |
| `src/pages/index.astro` | Constrained two-column intro and small scene | Full-bleed viewport-height hero with text on one side, castle on other; content sections unchanged |
| `src/pages/projects.astro` | Plain title and status-grouped work | One small decorative castle view beside the existing title; groups unchanged |
| `src/pages/blog/index.astro` | Plain Writing title and year-grouped list | One different still castle view beside the existing title; archive unchanged |
| `src/styles/global.css` | Shared page-head/section styles | Add one `.page-head.with-castle` two-column layout for both listing pages; do not change tokens or article prose |
| `scripts/check-site.mjs` | Checks a hidden `depth-field` home canvas | Assert hero and two accent mounts, static fallback on each, no canvas or Three.js script on other routes |
| `scripts/check-browser.py` | Tests wireframe, theme and fallback | Test castle render and static fallback, above-fold actions, reduced motion and chunk isolation across all routes |

## Reuse

- Keep `BaseLayout.astro` theme persistence, header, SEO, and `.wrap`; no new shared layout prop.
- Reuse `DepthField.astro` patterns for WebGL2 probe, dynamic `import('three')`, resizing, CSS-token colors, reduced-motion still frame and disposal.
- Keep existing `ProjectCard.astro`, `BlogCard.astro`, project data, blog content and all URLs unchanged.
- Keep one `three` dependency already in `package.json`; add no further runtime packages.

## Decisions shown as diffs

Mount one component in three places, with text before the decorative scene in source order:

```diff
- import DepthField from "../components/DepthField.astro";
+ import CastleScene from "../components/CastleScene.astro";
- <DepthField />
+ <CastleScene variant="hero" />
```

```diff
- <header class="page-head"><h1>Projects</h1><p>Systems I've built and research I've worked on. Each entry includes the tools, implementation details, and available source code.</p></header>
+ <header class="page-head with-castle"><div><h1>Projects</h1><p>Systems I've built and research I've worked on. Each entry includes the tools, implementation details, and available source code.</p></div><CastleScene variant="accent" view="stone" /></header>
```

Writing gets the same structure with `view="roof"`; article routes do not mount the scene. Put the shared two-column accent layout in `global.css` under `.page-head.with-castle`, stacking at 640px. No card wrapper around the title.

Home stays full bleed without changing other pages' layout:

```diff
- <section class="intro section">
+ <section class="intro castle-hero section">
```

Move the existing headline, credentials and actions into a new `.intro-inner.wrap` inside that section, then mount `<CastleScene variant="hero" />` after the actions in source order. Use `width: 100vw; margin-inline: calc(50% - 50vw)` on the hero within the existing wrapped main. Set the hero's minimum height to `calc(100svh - 92px)` on desktop and `calc(100svh - 116px)` on mobile so the shared header and first screen fit together; selected work begins below it. Desktop castle occupies the right half with left-aligned text on a solid or near-solid backdrop; mobile places contact actions before a cropped castle view within the first screen. Test 320px overflow and revise the hero containment if `100vw` includes classic scrollbar width. Keep normal scrolling and do not overlap links with canvas.

Set the light scene sky to `#d8ded9` and dark sky to `#18323a`; retain existing `--text` colors over those solid backdrops (verify both at 4.5:1). Use muted stone `#aaa595`, pale plaster `#e5e2d5`, and charcoal roof `#283b3e` in light, with darker stone/plaster and a lighter roof edge in dark. The original model is built from a stone-base box, three progressively smaller plaster storeys, broad hipped eaves made from four dark sloped planes per tier, and small repeated window/beam meshes. One muted horizon plane anchors it; no imported textures or model files. Use low-poly materials and one light. For accents, use the same castle group and switch camera angle/scale, not separate models. The SVG fallback has the same broad tier silhouette but is intentionally flat. Show fallback immediately; on successful first render hide only the fallback illustration. Failure leaves the illustration and text visible. All scenes have `aria-hidden="true"` and no keyboard focus.

Only home may respond to pointer position. Accent variants render once. Home stops continuous animation in reduced motion or when offscreen; restore on visibility and preference changes. CSS theme changes recolor both the WebGL scene and fallback. Never run WebGL on 404, posts, Contact or Quick profile. Dispose geometries/materials/renderers when navigating away.

## Steps

### 1. Capture baseline and write failing checks

- [x] Rebuild current worktree and save light/dark home and Projects/Writing screenshots at 390 × 844 and 1440 × 900; save page/chunk counts.
- [x] Update the static checker to assert one hero castle mount, one accent each on Projects and Writing, SVG fallback on each, and zero canvas on remaining routes. Run on current build; confirm failure names the missing hero castle rather than a build error.

### 2. Replace the small scene

- [x] Draw original `public/castle-fallback.svg` with simple tiers/eaves in current palette; no ThreeUI assets.
- [x] Replace `DepthField.astro` with `CastleScene.astro` and its typed `variant` and optional `view` props. Build one tower group from repeated primitives, one renderer per mounted page, CSS-token materials, fallback until first frame, bounded home pointer response and reduced-motion/offscreen pause.
- [x] Recompose `index.astro` into a full-bleed hero with the existing copy and actions. Mount accent variants in Projects and Writing headers and style the shared accent layout. Build and run the static checker; verify desktop/mobile screenshots before proceeding.

### 3. Browser proof and review

- [x] Extend browser checks to prove three canvases on their own routes, no JS/blocked Three.js fallback, still reduced-motion frames, offscreen pause, distinct camera views, and no Three.js request on posts/Contact/Quick profile/404.
- [x] Run `npm run build && node scripts/check-site.mjs` and the full browser suite against the production preview. Inspect full-viewport home in both themes, mobile action visibility, accent headers, 320px overflow, console/network errors, and bundle size.
- [x] Run `git diff --check`, inspect the diff for unchanged project/blog/admin/resume data, and open `/plannotator-review`. Stop for feedback. No commit or deployment.

## Verification

Use the existing isolated worktree `/Users/hitesh/hitendra.dev-worktrees/quiet-gallery` and preview `http://127.0.0.1:4367/` if it still responds. Run the existing static checker and `SITE_EVIDENCE=/tmp/quiet-gallery-castle-evidence python3 scripts/check-browser.py http://127.0.0.1:4367`. Confirm built route count remains 14 and 8 published posts remain. Use Agent Browser screenshots and browser errors, plus a fresh session with the Three.js chunk blocked. Contrast-check hero text over its actual backdrop in both themes. Report exact output, evidence paths and any GPU/performance limitation.

## Not doing

No direct import of ThreeUI code or art, exact 1:1 copy, photorealism, full-page scroll scenes, 3D under article prose, new library, content rewrite, admin work, commit, push, or deployment.
