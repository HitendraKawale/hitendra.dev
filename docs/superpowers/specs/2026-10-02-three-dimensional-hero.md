# Three-dimensional homepage hero

## Goal

Add one original, minimal 3D moment to the portfolio, taking visual direction from [ThreeUI Halvorsen](https://threeui.com/landing-pages/halvorsen-landing-page) without using its Pro source or copying its glass-hands asset. The homepage introduction remains clear and usable before the 3D scene loads and when it cannot load. All other routes, content, links, and theme behavior stay intact.

## Visual and interaction design

Keep the quiet-gallery typography, mineral palette, content width, project rows, and reading layouts. The homepage intro retains its first-person headline and credentials. Give the hero a single contained 3D viewport alongside that text, not a full-page background. On wide screens, the headline stays left; a contained scene sits above the credentials and actions in the right column. On phones, place the scene after the actions, as a shallow strip, so the contact links stay within the first viewport at 390 × 844.

The scene is an abstract, sparse 3D point-and-line structure inspired by Hitendra's work in 3D vision and retrieval systems. It is clearly decorative, not a rendering of his research dataset or an interactive project demo. Use one neutral depth field and a few connected points. Shape, perspective, subtle occlusion, and slow orientation change provide depth. Match light/dark CSS tokens; avoid particles over text, bloom, gradients, orbit controls, scroll capture, and 3D content on interior pages.

Pointer movement may rotate the structure by a small bounded angle. Without a pointer, it settles at its initial orientation. With `prefers-reduced-motion: reduce`, render one still frame and do not attach animation or pointer motion. Keyboard users need no new control: the canvas is decorative and hidden from the accessibility tree. Text, actions, skip link, theme toggle, and project details remain normal HTML. If WebGL or JS is unavailable, hide the canvas and retain the composed HTML hero with no blank reserved box.

## Implementation boundary

Use the existing Astro homepage and layout; create one focused 3D component for the canvas and its scoped styles. Three.js is acceptable as the single new runtime dependency because it handles real 3D rendering and cleanup more safely than a custom WebGL renderer. Load it only on the homepage, not in the shared layout. Do not import Halvorsen code, screenshots, assets, or branding. Do not introduce a UI framework, animation engine, shader library, model download, or new content schema.

The current working branch `redesign/quiet-gallery` already contains an uncommitted, reviewed redesign. Build on it without resetting or committing it. Keep the no-JS page meaningful. No commit, push, or deployment without separate permission.

## Verification

Run the full production build and existing static/browser checks. Add a browser check that the headline, contact actions, and project rows remain available when canvas initialization is blocked. Verify the scene visibly renders in light and dark at 1440px and 390px, does not cause page overflow, and stops motion under reduced motion. Check the browser console for WebGL errors, compare screenshots with the quiet-gallery baseline, and inspect bundle loading to ensure Three.js does not load on interior pages. If browser or GPU acceleration is unavailable, report the limitation instead of claiming 3D verification.
