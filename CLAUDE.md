# Repository guide

## Commands and verification

```bash
npm run dev       # Local Astro server, default port 4321
npm run build     # Static output in dist/
node scripts/check-site.mjs  # Run after building
npm run preview   # Serve production output
```

No lint command or test framework is installed. The static checker verifies routes, draft exclusion, navigation, metadata, and project counts. Browser checks are required for theme, clipboard, responsive layout, and accessibility.

## Release and archive

`https://hitendra.dev` is hosted on Vercel. Pushes to `main` deploy automatically. Commit, push, and deployment require explicit permission.

The original Chronicle design is preserved at `dcc0afe9ba5fa5ae1bd90fbfd866bf87b12cb2cc` on `archive/chronicle`. Professional work belongs on `redesign/professional`. A separate public archive deployment is planned but not yet configured. Add its footer link only after verifying the real URL.

`site` in `astro.config.mjs` stays `https://hitendra.dev` on the professional branch. Both canonical and social URLs resolve against it. Archive-only metadata changes belong on a separate `deploy/chronicle` branch, never on the professional branch.

## Architecture

Astro 6 static portfolio. All public pages use `BaseLayout.astro`, including `/tldr`.

| Route | File |
| --- | --- |
| `/` | `src/pages/index.astro` |
| `/projects` | `src/pages/projects.astro` |
| `/blog` | `src/pages/blog/index.astro` |
| `/blog/[slug]` | `src/pages/blog/[slug].astro` |
| `/contact` | `src/pages/contact.astro` |
| `/tldr` | `src/pages/tldr.astro` |
| Missing page | `src/pages/404.astro` |

`BaseLayout` owns metadata, global CSS, navigation/footer, the skip link, saved-theme restoration, and the theme/clipboard handlers. It requires `title` and `description`; `cardDescription` is optional.

`PostLayout` wraps `BaseLayout` and receives `frontmatter`, reading-time `minutes`, and `prev`/`next` entries from `[slug].astro`. Markdown frontmatter must not specify a layout.

`ProjectCard` receives `project` and optional `expanded`. The homepage sets `expanded` to expose descriptions directly. The projects listing uses native details. Missing project URLs render no source link.

## Professional design

Design for AI/ML hiring managers first. Use plain labels, technical evidence, and direct contact links. Keep the full personal writing archive; the homepage promotes the existing `saga-scribble-segmentation` post only when published.

Use tokens in `src/styles/global.css`. Light is the default; `data-theme="dark"` overrides the same colors. Native system sans-serif serves headings/body; native monospace serves code. Content width is 1040px with 24px gutters. Article text is limited to 68ch.

Keep navigation visible on mobile. Content and native project details must work without JavaScript. The theme and copy buttons are hidden until their handlers attach. Use visible keyboard focus, 44px controls, and reduced-motion rules. Theme storage uses `theme`; the old Eclipse preference has no effect.

Use `.wrap`, `.section`, `.page-head`, `.section-head`, `.actions`, `.button`, `.meta`, `.muted`, and `.stack` for shared layout. The admin consumes the same semantic tokens but retains its own styles.

## Content editing

- Personal information, links, skills, and language proficiency live in `src/data/profile.ts`.
- Projects live in `src/data/projects.json`; `src/data/projects.ts` exports their type. Status is `Built`, `Research`, or `In Progress`; `href` is optional. The homepage and quick profile show up to three featured projects.
- Replace `public/resume.pdf` to update the resume without changing its URL.
- Blog files live in `src/content/blog/`. Required frontmatter: `title`, `description`, `date`. Optional: `tags`, `draft`. The filename becomes the slug.
- `getCollection("blog", ({ data }) => !data.draft)` excludes drafts. Keep all existing article URLs stable.

### Local admin

Run the dev server and visit `/admin`. The panel writes directly to repository content files. Use an isolated worktree for create/delete testing and remove only fixtures created by that test.

The inline `localAdmin` integration injects `/admin` and its API routes only when `command === 'dev'`. Keep `src/admin/` outside `src/pages/` so production never exposes these routes.

Keep `src/content/blog/scriptorium-seed.md` permanently as a draft. It ensures the collection's file watcher registers when otherwise empty. The API refuses to delete it, and the panel hides it.
