# Quiet gallery redesign

## Goal

Make the entire portfolio feel more distinctive and considered without obscuring Hitendra's AI engineering work. Keep every public route, project, post, contact path, and the light/dark theme. Prove the redesign with a production build, the existing static checker, and browser checks at desktop and mobile sizes.

## Visual direction

A quiet gallery, not a dashboard or an animation demo. The homepage spends its visual emphasis on one asymmetric, oversized introduction; project evidence and writing follow in spacious rows. Interior pages reuse the same type, colors, spacing, and navigation while keeping article text narrow.

```text
Before: generic heading -> stacked sections -> uniform rows
After:  large introduction | concise credentials
        selected work as evidence-led rows
        writing and about in a calmer lower register
```

Original palette, light: mineral `#F1F5F3`, paper `#FFFFFF`, deep blue-green `#15343B`, secondary ink `#4B6569`, teal `#006D77`, rule `#C5D5D2`. Dark: background `#10262C`, surface `#19343A`, ink `#E8F2F0`, secondary `#B3C8C6`, accent `#76CED0`, rule `#39555A`. Contrast is a constraint: check the chosen combinations and adjust any value that fails 4.5:1 for text or 3:1 for controls. The palette is a design choice, not a claim to reproduce a reference site.

Use the existing system sans-serif stack for copy and display, with the existing native monospace stack for code. Build the identity through scale, tighter headline tracking, and the asymmetric composition rather than a font download. Headlines are large but never clipped. Left-align copy; constrain body text to readable measures. Keep the existing 1040px content width unless the hero needs a slightly wider measure. No gradients, glass effects, faux diagrams, repeated cards, or decorative numbering.

## Page treatment

- Home: large first-person engineering statement, clearly named author, MSc credential, focus areas, availability, resume/contact links; then three featured projects, the existing selected SAGA writing, and an abbreviated about/languages area. Preserve the meaning of existing biography and claims. No invented results.
- Projects: retain status groups and every project. Title, subtitle, stack, status, and available source remain visible; native details retain long descriptions. Give each row more typographic hierarchy and space, not a box.
- Writing: retain year groups, post dates, summaries, and tags. The list should feel like a reading shelf rather than project cards.
- Posts: keep the current reading measure, code/table overflow, metadata, and adjacent links. Apply the new palette and display hierarchy without touching article content or slugs.
- Contact: make email and resume the obvious actions. Keep copy feedback and secondary links. Do not add a form.
- Quick profile: keep the printable information density and both columns on wide screens; inherit the common visual language.
- 404, header, footer: same identity and palette, straightforward recovery/navigation. Keep archive link and theme toggle.

## Behavior and boundaries

Reuse Astro, the existing data files, components, tokens, and theme/clipboard scripts. Content and native details must work without JavaScript. Saved dark mode still loads before paint; keyboard focus, skip link, visible mobile navigation, 44px controls, and reduced-motion support remain. Existing page metadata, draft filtering, dev-only admin, resume, canonical URLs, and social asset remain unchanged unless a visual-only change requires a matching metadata color.

Change only the shared presentation and page-specific composition. No new UI framework, animation package, CMS, project schema, blog rewrite, 3D canvas, or speculative interaction. Do not commit, push, or deploy without separate permission.

## Verification

Run `npm run build && node scripts/check-site.mjs`. Serve a local production preview and run `python3 scripts/check-browser.py <preview-url>` if Agent Browser is available; supplement with manual visual review of home, projects, writing, a post, contact, and quick profile at mobile and desktop widths in both themes. Check keyboard, project details, no-JS content, contrast, text overflow, and console errors. Capture screenshots and report any checks blocked by missing browser tools.
