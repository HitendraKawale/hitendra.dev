# Three-dimensional homepage hero implementation plan

> **For agentic workers:** Use `executing-plans` after approval. Track steps with checkboxes. Do not commit, push, or deploy without separate permission.

**Goal:** Add one original, accessible Three.js hero scene inspired by ThreeUI Halvorsen, without using its Pro source or replacing the readable portfolio.

**Architecture:** A homepage-only Astro component renders a decorative canvas after WebGL capability and the module load succeed. The existing headline, credentials, actions, theme toggle and all interior routes remain HTML/CSS. Hidden canvas is the fallback; no global 3D script.

**Tech stack:** Astro 6, Three.js, existing Node static checker and Agent Browser CLI.

**Spec:** `docs/superpowers/specs/2026-10-02-three-dimensional-hero.md`

## Context

The approved quiet-gallery redesign is uncommitted on `redesign/quiet-gallery`. It has a typographic, two-column home introduction but no ThreeUI-derived 3D element. The user approved one original Three.js scene. Halvorsen is a Pro reference, so its code, artwork and assets are out of scope.

```text
Current: home intro [headline] | [credentials + links]
Target:  home intro [headline] | [3D study / credentials + links]
Mobile:  [headline] -> [credentials + links] -> [3D study]
Failure: [headline] -> [credentials + links], no empty canvas area
```

## Files to modify

| File | Today | After |
| --- | --- | --- |
| `src/pages/index.astro` | Two-column text introduction | Mount scene in the aside after the actions in source order; CSS places it first on desktop and last on mobile |
| `src/components/DepthField.astro` (new) | Absent | One decorative Three.js wireframe/point scene, scoped styling, capability fallback, resize, theme and reduced-motion handling |
| `package.json`, `package-lock.json` | Only Astro runtime dependency | Add `three` and its TypeScript declarations for the Astro client script; no other packages |
| `scripts/check-site.mjs` | Checks routes, project count and intro structure | Also assert a canvas is present only on home and the HTML headline/actions still exist |
| `scripts/check-browser.py` | Tests pages, theme, copy, details and viewports | Assert successful WebGL render, reduced-motion static frame, and no blank space when Three.js is blocked |

## Reuse

`src/pages/index.astro` already owns the two-column hero and keeps actions within the mobile fold. `BaseLayout.astro` owns light/dark state and metadata; do not move theme logic. Existing `scripts/check-site.mjs` asserts generated HTML, and `scripts/check-browser.py` drives Agent Browser against production preview. All text and navigation remain the existing server-rendered HTML.

## Decisions, shown as diffs

One mounted scene. The aside stays the source-order container; CSS reorders only the decorative viewport on desktop:

```diff
         <a href="/contact">Contact</a>
       </div>
+      <DepthField />
     </div>
+ @media (min-width: 761px) { .intro-aside { display: flex; flex-direction: column; } .intro-aside :global(.depth-field) { order: -1; } }
```

Do not make the decorative viewport focusable. In the component, hide it until it has rendered a first frame:

```diff
+ <div class="depth-field" hidden aria-hidden="true"><canvas></canvas></div>
```

The component script first checks `canvas.getContext('webgl2')`, then dynamically imports `three`; it never unhides the wrapper until its first render succeeds. Failed WebGL or module load leaves the entire wrapper hidden.

The implementation fills in the scene with `IcosahedronGeometry`, `EdgesGeometry` and `Points` using the same geometry, with thin low-contrast lines and a small set of bright vertices. Use a `PerspectiveCamera` and `WebGLRenderer({ canvas, context, alpha: true, antialias: true })`, cap pixel ratio at 2, size to the container, and draw on resize. A bounded pointer offset and a slow `requestAnimationFrame` turn the shape. `matchMedia('(prefers-reduced-motion: reduce)')` must stop an active loop and draw one still frame; if the preference later clears, restart it. Read `--accent` and `--muted` from CSS and refresh material colors on `data-theme` changes. On an initialization or import error, keep the wrapper hidden. The scene is abstract decoration, not SAGA data. Three.js [documents the existing-context renderer option and `dispose()`](https://github.com/mrdoob/three.js/blob/dev/docs/pages/WebGLRenderer.html); dispose the renderer, geometry and materials on pagehide.

Avoid a test-only implementation hook. Browser checks inspect actual canvas dimensions, screenshot pixels and runtime failures; static checks prove no content moves into the WebGL path. Confirm interior routes do not request the Three.js chunk.

## Steps

### 1. Baseline and regression checks

- [x] Save screenshots of the current home at 390 × 844 and 1440 × 900 in both themes, plus the existing `npm run build && node scripts/check-site.mjs` output.
- [x] Add static assertions that home contains one canvas inside a hidden `aria-hidden="true"` wrapper, plus existing headline and contact action, and interior routes contain no canvas. Build/check against the current branch and confirm the missing-scene assertion fails for that reason.

### 2. Scene

- [x] Add `three` and its TypeScript declarations via npm. Keep the lockfile focused; do not upgrade unrelated dependencies.
- [x] Create `DepthField.astro` as the only owner of canvas and Three.js lifecycle. Probe WebGL2 before import, reveal after first render, render still under reduced motion, resize with the component, and read CSS colors on theme changes.
- [x] Mount it on the home aside, put it above credentials on wide screens and below contact links on mobile using CSS only. Keep contact actions above the fold at 390 × 844. Run `npm run build && node scripts/check-site.mjs` until green.

### 3. Browser proof and review

- [x] Extend the browser checker: home WebGL canvas has nonzero dimensions and becomes visible; under reduced motion take two element screenshots separated by animation frames and compare them byte-for-byte; block the Three.js chunk in a fresh session and confirm the HTML/actions remain visible with no empty viewport. Check interior routes do not request the chunk.
- [x] Run the full browser checker, review screenshots in both themes at 390/1440, verify no 320px overflow, no console errors, all public routes still load, and keyboard/theme/copy/details behavior still passes.
- [x] Inspect `git diff --check` and verify project data, posts, admin, resume, layout scripts and article routes are unchanged. Open `/plannotator-review` for the diff and stop for feedback. No commit or deployment.

## Verification

Use the existing production preview in the task worktree after a fresh `npm run build`. Run `node scripts/check-site.mjs` and `SITE_EVIDENCE=/tmp/quiet-gallery-3d-evidence python3 scripts/check-browser.py http://127.0.0.1:4367`. The current fallback preview URL is `http://127.0.0.1:4367/`; check it still responds before relying on it, and follow the named-server rule if restarted. Capture exact build/check output and screenshots. If Chromium cannot initialize WebGL, report that separately instead of claiming visual verification.

## Not doing

No Halvorsen source or assets, full-page animation, 3D on interior routes, dataset claim, UI framework, shader library, model downloads, new contact flow, or production release.
