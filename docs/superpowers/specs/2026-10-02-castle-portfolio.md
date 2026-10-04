# Castle portfolio scene

## Goal

Replace the small wireframe on the homepage with a full-viewport, original stylized Japanese castle scene. Reuse restrained 3D views in the Projects and Writing page headers. Keep the site's existing content, navigation, theme behavior, project evidence, and article reading layout.

Reference: [ThreeUI Country Towers Japan](https://threeui.com/three-js/japanese-tower/japan). Its preview shows a tiered Japanese tower with stone base, plaster walls, and wide tiled eaves in a landscape. Use it as visual direction, not as code, model, texture, screenshot, or an exact reproduction.

## Experience

```text
Home:    full first viewport = readable introduction | original 3D castle
         selected work, writing and about remain below
Projects: title and listing + one small still castle detail in page header
Writing:  title and archive + a different still view of the same model
Posts/contact/quick profile: unchanged reading and contact surfaces
```

Make the castle the hero, not a background texture under the text. On desktop, reserve a clear left column for the headline and actions and place the tower to the right against an atmospheric but quiet scene. On mobile, keep name, headline and contact links in the first viewport; show a cropped castle below or to the side without forcing horizontal scrolling. The scene ends at the hero boundary. Interior accents are 3D renderings of the same geometry at different camera angles, not unrelated effects.

Palette: keep the site's existing mineral light/dark tokens for the body. The scene uses muted stone, charcoal roof, and a low-detail horizon in both themes. Text remains on an opaque or nearly opaque surface where necessary to meet WCAG contrast. Avoid glass, particles, flying leaves, fake technical graphs, photorealistic textures, shader packages, or themed copy that implies castle-building is Hitendra's work. In reduced motion, render one still frame; pointer movement is optional and bounded to the home scene only. Never intercept scrolling or keyboard navigation.

## Implementation

Use the installed Three.js dependency and one focused reusable Astro component, with a `hero` or `accent` variant. Build the castle from original procedural primitives and simple roof geometry. Mount only where used: homepage, Projects header and Writing header. Do not load the Three.js chunk on posts, Contact, Quick profile or 404. A static original illustration or CSS composition should preserve the castle silhouette when WebGL/JS fails, while all copy and links remain HTML. Maintain light/dark color handling, resize, pixel-ratio cap, GPU disposal, and reduced-motion support. Replace the existing `DepthField` rather than leaving two competing scenes.

This is a visual redesign, not a source copy. Do not add a UI framework, asset download, content schema, admin change, new contact flow, or site-wide scroll animation. The previous quiet-gallery changes are already in the uncommitted `redesign/quiet-gallery` worktree; do not reset or commit them. No commit, push, or deployment without separate permission.

## Verification

Run `npm run build && node scripts/check-site.mjs` and the complete `scripts/check-browser.py` suite against the production preview. Confirm one hero and two accent mounts; no 3D chunk on other routes; castle visible in both themes at 390 × 844 and 1440 × 900; contact links above fold; no page overflow at 320px; reduced-motion frame stays still; and WebGL-disabled fallback keeps the silhouette and content without a blank region. Review screenshots, keyboard flow, console/network errors, and page load cost. Report the actual downloaded 3D bundle size and any unverifiable GPU limitation.
