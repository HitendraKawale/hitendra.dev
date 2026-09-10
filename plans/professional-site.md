# Professional website redesign

## Context

The current site presents Hitendra's AI engineering work through a Berserk-themed design. The new version should make his work and qualifications easier to assess, retain restrained interaction, and preserve the old version separately.

Status: approved and implemented on `redesign/professional`. The user authorized committing and pushing the professional and archive branches. Production release remains unapproved; verification limitations and review gates are recorded below.

Execution: use the `executing-plans` skill and complete each phase with its verification checkpoint. This document contains both the design and implementation plan. Branch commit/push was requested after implementation; merging into `main` and changing production still require separate permission.

Confirmed audience: AI/ML hiring managers first, with research and freelance opportunities secondary.

### Goal

Replace the fantasy presentation with a professional personal website.
Keep existing project and blog content infrastructure, with an independently recoverable old version.
Prove the result through a production build and browser checks across routes, mobile, keyboard, and reduced motion.

### Findings so far

- Working tree was clean on `main` at `dcc0afe` before this plan was created.
- Astro 6 supplies static pages. Installed runtime dependencies are Astro and Lenis. No test or lint scripts exist.
- `src/data/profile.ts` contains identity, links, resume path, skills, and languages.
- `src/data/projects.json` contains eight projects, including three featured engineering projects and two research projects. Several descriptions already include measured results. These are supplied claims, not independently verified evidence.
- The homepage queries featured projects and the three latest non-draft posts.
- The opening of `BaseLayout.astro` couples the shared shell to the ash canvas, spine, Eclipse palette, and animated overlay. A palette-only change would leave the themed structure intact.
- Routes include `/contact` and `/tldr` as well as home, projects, blog, blog posts, and 404. Repository guidance omits these two routes from its architecture table.
- Fully inspected shared script, global CSS, navigation, footer, cards, projects page, blog index, post layout, slug routing, content schema, and deployment configuration.
- The shared script owns smooth scrolling, reveals, spine progress, Eclipse, mobile overlay, pointer parallax, greeting cycling, cursor-following project previews, and ash rendering. The project preview hides stack information from touch users; put it inline instead.
- `/tldr` owns a separate HTML shell and Eclipse restoration. It also provides clipboard copy and a London clock. Move this route onto the shared professional shell to prevent theme and metadata drift; retain copy, omit the clock.
- Current reveal CSS hides content until JavaScript runs. New content must render visibly without JavaScript.
- The admin routes are injected only during `astro dev`. Preserve that boundary and the permanent draft seed.
- Public assets are `favicon.svg`, `favicon.ico`, `og.png`, and `resume.pdf`. Keep the resume unchanged.
- Read the rendered-content portions of `/contact` and `/tldr` and the first 100 lines of `ProjectIndex`. Their remaining legacy styles have not been read. Read every file end to end before editing it during implementation.

## Approach

Retain Astro and the existing content sources. Redesign the shared presentation and page hierarchy on a separate branch instead of maintaining two themes in one application.

Confirmed: keep the old website publicly accessible as a separate Vercel app.

After plan approval, preserve `dcc0afe` on `archive/chronicle`. When deployment is separately authorized, create a Vercel project bound to `deploy/chronicle`, a branch from that snapshot with only archive metadata adjustments, using its assigned `.vercel.app` address. Develop the professional version on `redesign/professional`. Leave `main` and `hitendra.dev` unchanged until the new version is approved for release. Do not move the custom domain to the archive project.

`astro.config.mjs` currently hardcodes `site: 'https://hitendra.dev'`; the archive needs its own canonical URL rather than pointing its distinct pages at the redesigned site. Keep the original snapshot recoverable and make any archive-only metadata adjustments as separate changes. Verify Vercel branch settings, public access, and the assigned URL before declaring the archive available. No Vercel resources have been created.

```text
[Current main] --> [Preserved old version]
       |
       v
[Professional branch] --> [Preview review] --> [Approved live replacement]
```

Recommend a light-first editorial design: off-white background, charcoal text, one muted blue accent, readable sans-serif typography, compact navigation, and selected work near the top. Use fine separators and whitespace rather than decorative panels. This is a proposed direction, not a measured extraction from the references.

Keep a conventional light/dark toggle, restrained hover/focus feedback, native expandable project details, and email copy. Remove the Eclipse takeover, ash particles, fantasy symbols, oversized theatrical hero, rotating greetings, scroll reveals, and forced smooth scrolling. Keep languages in a compact about section. The retained interactions provide utility without delaying access to content.

### Homepage hierarchy

1. Compact header: Hitendra Kawale, Projects, Writing, Contact, theme button. Keep these links visible and wrapping on mobile rather than hiding them in a full-screen menu.
2. Introduction: `AI engineer building LLM systems, RAG pipelines, and 3D vision tools.` Supporting line: `MSc Artificial Intelligence, University of Surrey. I focus on backend systems, evaluation, and deployment.` Show availability and Resume, GitHub, and Contact links. Name, focus, qualification, and contact route must be visible without scrolling at 390 × 844 and 1440 × 900.
3. Selected work: the existing three featured projects in a vertical list. Each displays title, subtitle, description, stack, status, and source link. Do not put technical evidence behind hover or inside a carousel. No oversized project tiles.
4. Selected writing: the existing `saga-scribble-segmentation` post, followed by a link to the full writing archive. Do not fabricate technical posts or promote personal diary entries as technical evidence.
5. About: short education and engineering-focus copy, then languages with their existing proficiency levels. Keep freelance availability secondary. No invented employment timeline or headshot placeholder.
6. Compact footer: contact/social links, Quick profile at `/tldr`, copyright year, and Previous design linking to the verified archive URL.

### Other routes

- `/projects`: retain all eight projects and status grouping. Native `<details>` exposes the longer description on this listing; subtitle, stack, status, and source link stay visible. The homepage displays featured descriptions directly. A project without a URL gets no fake link or disabled button.
- `/blog`: label it Writing; preserve all non-draft personal and technical posts, year grouping, tags, summaries, and URLs. Do not rewrite the user's articles.
- `/blog/[slug]`: readable 68-character text measure, normal headings instead of drop caps, visible code blocks and tables, dates, reading time, and previous/next navigation.
- `/contact`: prioritize hiring inquiries and email, then resume and social links. Retain a short freelance paragraph. Remove the one-day reply promise rather than presenting it as a guarantee.
- `/tldr`: retain the URL as Quick profile, use `BaseLayout`, central profile data, featured work, and email copy. Remove the duplicate head, independent theme logic, clock, and hardcoded project count.
- `404`: plain Page not found with Home, Projects, and Writing links.

### Visual specification

These are original design choices, not copied reference values.

| Token | Light | Dark |
| --- | --- | --- |
| `--bg` | `#fafaf8` | `#151719` |
| `--surface` | `#ffffff` | `#1e2125` |
| `--surface-2` | `#f0f2f4` | `#282d33` |
| `--text` / `--ink` | `#20252b` | `#edf0f2` |
| `--muted` | `#59636e` | `#a7b0bc` |
| `--accent` | `#315d8a` | `#8db9e3` |
| `--accent-hi` | `#23466b` | `#bed9f2` |
| `--border` | `#d7dce1` | `#454d57` |

Use `system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif` for body and headings, and `ui-monospace, SFMono-Regular, monospace` for code. Remove Google Fonts requests. Set body to 17px with 1.65 line height, metadata at least 14px, hero heading `clamp(2rem, 4vw, 3.25rem)`. Content max-width 1040px with 24px mobile gutters. Section spacing 48px mobile / 72px desktop. Use 1px separators, at most 6px corner radii, and no decorative gradients or large shadows.

First visit is light. Explicit dark preference persists across routes and reloads through the `theme` localStorage key. Ignore the old `eclipse` key. Storage failures must leave the toggle functional in memory. Apply saved preference pre-paint and update `color-scheme`, theme-color metadata, and the button's accessible state.

Limit hover/focus transitions to 160ms and disable them for reduced motion. Native scrolling and the browser scrollbar remain intact. Nothing needs an animation or JavaScript to become readable.

## Reference research

Fetched all four first-party homepages successfully with Python `urllib.request` and inspected extracted text. Also opened Chip Huyen's homepage in an isolated Agent Browser session, inspected its accessibility tree and computed styles, and closed that session. Observed a near-white `rgb(253, 253, 253)` background, Lora serif body, and an 815px wrapper at the browser's 1280px viewport. The proposed sans-serif treatment is a deliberate difference.

No screenshot comparison was performed because planning permits only Markdown artifact writes. Capture the implementation after approval; no pixel-match claim is intended. No background-agent tool is available, so research ran directly.

| Source | Observed content pattern | Adaptation for Hitendra |
| --- | --- | --- |
| [Andrej Karpathy](https://karpathy.ai/) | Brief introduction, chronological work history, linked teaching, writing, projects, and publications | Put concrete work and direct evidence links ahead of visual effects; do not invent a publication section |
| [Chip Huyen](https://huyenchip.com/) | First-person introduction connects production AI work, tools, books, personal background, and contact | Explain the engineering focus plainly and retain a small amount of personal context |
| [Lilian Weng](https://lilianweng.github.io/) | Technical writing with summaries, dates, reading times, archives, and tags | Make the blog a readable technical resource using existing post metadata |
| [Hamel Husain](https://hamel.dev/) | Applied AI focus stated upfront, followed by selected writing and explicit OSS/teaching navigation | Make specialization and useful work easy to find; avoid promotional banners and newsletter features outside this scope |

Shared lesson: content establishes credibility. Adapt that hierarchy without copying their biographies, branding, or career claims. Use a more polished visual treatment while keeping the pages lightweight.

## Files to modify

| File | Today | After |
| --- | --- | --- |
| `src/layouts/BaseLayout.astro` | Themed shell and nine initializers | Metadata, skip link, shared shell, theme and clipboard handlers only |
| `src/styles/global.css` | Chronicle tokens, textures, hidden reveals | Above tokens, typography, focus states, normal scrolling, reduced motion |
| `src/components/Nav.astro` | Sigil, Behelit, full-screen mobile menu | Text identity, visible responsive links, `aria-current`, theme button |
| `src/components/Footer.astro` | Quote and themed labels | Small footer with existing links and public archive link |
| `src/components/ProjectCard.astro` | Plate with shadow and full description | Shared project row with `expanded?: boolean`; true displays description, false uses native details |
| `src/components/BlogCard.astro` | Large engraved date and title | Compact date, title, description, and tags |
| `src/pages/index.astro` | Theatrical hero and chapters | Approved hierarchy; ProjectCard with expanded descriptions; selected existing article |
| `src/pages/projects.astro` | Armoury, status groups, wide plates | Projects, same groups, ProjectCard with native details |
| `src/pages/blog/index.astro` | Chronicles and year groups | Writing, same archive queries and URLs |
| `src/layouts/PostLayout.astro` | Drop caps and sigil end-marks | Reading layout, code/table overflow, same metadata and adjacent links |
| `src/pages/contact.astro` | Send Word and service promotion | Hiring-first contact with direct links and copy button |
| `src/pages/tldr.astro` | Independent document and scripts | Quick profile using BaseLayout, same source data, no duplicate scripts |
| `src/pages/404.astro` | Fantasy error copy | Plain error and recovery links |
| `src/data/profile.ts` | Long bio and existing personal data | Concise professional bio/cardBio and verified archive URL; preserve identity and proficiency facts |
| `public/favicon.svg` | Berserk identity | Original HK monogram using the professional palette |
| `public/favicon.ico` | Existing fallback icon | Matching monogram fallback |
| `public/og.png` | Existing share card | 1200 × 630 name, AI Engineer, focus, and domain card |
| `package.json` | Astro and Lenis | Remove unused Lenis, keep Astro and existing commands |
| `package-lock.json` | Includes Lenis | Regenerate with the dependency removal, no unrelated upgrades |
| `scripts/check-site.mjs` | Absent | Dependency-free assertions against generated production HTML |
| `CLAUDE.md` | Requires Chronicle design | Professional design rules, accurate route table, archive/release boundary |
| `plans/professional-site.md` | This plan | Execution checklist and evidence paths |
| `astro.config.mjs`, archive branch only | Canonicals use custom domain | Set `site` to actual assigned archive URL; professional branch keeps `https://hitendra.dev` |

Delete obsolete components only after all imports are removed: `src/components/ProjectIndex.astro`, `Brand.astro`, `Behelit.astro`, `Rail.astro`, `AshCanvas.astro`, and `Marquee.astro`. Verify all callers first. The archive retains them.

`src/data/projects.json`, `src/data/projects.ts`, `src/content.config.ts`, `src/pages/blog/[slug].astro`, `src/content/blog/*`, `public/resume.pdf`, `src/admin/*`, and `vercel.json` retain their data/contracts. The admin already references `--bg`, `--text`, `--ink`, `--heading`, and related token names; define those in the new global CSS rather than reskinning the admin.

### Decision diffs

Shared shell and interaction removal:

```diff
- AshCanvas + Rail + Behelit + Eclipse overlay
- initScroll / initProgress / initHero / initTongues / initIndex / initAsh
- initReveals / initMenu / initBehelit
+ Skip to content + text navigation + native responsive layout
+ theme initialization + clipboard handler
```

Reuse one project renderer instead of maintaining two presentations:

```diff
- <ProjectIndex projects={featured} />
+ {featured.slice(0, 3).map(project => <ProjectCard project={project} expanded />)}

- index: number;
- wide?: boolean;
+ expanded?: boolean;
```

Choose writing intentionally without adding schema or admin fields:

```diff
- const posts = nonDraftPosts.sort(byDate).slice(0, 3);
+ const posts = nonDraftPosts.filter(post => post.id === 'saga-scribble-segmentation');
```

The existing draft query remains authoritative; hide the section if that post is absent or becomes a draft. The full archive still lists every published post.

Replace themed tokens across public consumers rather than keeping a second palette mapping:

```diff
- --void / --bone / --blood / --display / data-eclipse
+ --bg / --text / --accent / --heading / data-theme="dark"
- opacity: 0; /* content awaits observer */
+ /* Content is visible in initial HTML. */
```

Clipboard failure must tell the visitor what actually happened:

```diff
- btn.textContent = 'press ⌘C';
+ status.textContent = 'Could not copy. Select the email address and copy it.';
```

Use an adjacent `role="status"` element and keep the visible mailto link usable. Do not claim clipboard success before the promise resolves.

## Reuse

- Profile links, resume path, skills, and languages from `src/data/profile.ts`.
- Project data and featured flags from `src/data/projects.json`.
- Existing content collection queries and draft filtering in `src/pages/index.astro`.
- Canonical URLs and social metadata handling in `src/layouts/BaseLayout.astro`.
- ProjectCard data rendering, BlogCard links and dates, PostLayout reading time and adjacent-post props.
- Clipboard API handling from `/tldr`, with explicit success/failure status, shared through BaseLayout.
- Admin data contracts and dev-only injection, unchanged. No new content schema or editing interface.

## Approval and deployment boundaries

Audience and public preservation are confirmed. This review approves the proposed design and implementation scope, not a commit, push, or change to production. The archive URL is assigned during Vercel setup, not guessed in code. If account access is unavailable, finish the local redesign and report archive deployment as blocked; do not ship a placeholder footer link.

Preserve the exact original `dcc0afe` as `archive/chronicle`. Use a separate `deploy/chronicle` branch for archive-only canonical adjustments and bind the archive Vercel project to that branch. This keeps the snapshot exact. Use a separate worktree for archive changes so its config cannot enter the professional branch. Check existing branch names before creating anything; never overwrite an existing branch.

Before any authorized Vercel setup, inspect the account's available settings and current official documentation. Do not copy environment variables, custom domains, or project credentials. Static output needs no backend secrets. The archive must be accessible without login. Verify its `/`, `/projects`, `/blog`, `/contact`, `/tldr`, and a post before linking it. The main site changes only after a separate release approval.

## Steps

### 1. Preserve and establish a baseline

- [x] Inspect repository architecture and primary reference content.
- [x] Confirm hiring-first audience and publicly retained old version.
- [x] Obtain Plannotator approval before code changes.
- [x] Recheck git status and the recorded original commit. Create the archive reference and isolated professional worktree without altering `main`.
- [x] Read all touched files end to end, including styles skipped during discovery, admin token consumption, identity assets, and local instructions.
- [x] Install existing locked dependencies only if needed after planning. Run `npm run build` before changes and capture route count and output.
- [x] Start an isolated local server using the named-server rules and capture baseline screenshots at 390 × 844 and 1440 × 900. Record current route, link, and content counts.

Checkpoint: old commit preserved locally; baseline build and screenshots captured. Public deployment remains a separately authorized step.

### 2. Replace the presentation, retain the content contracts

- [x] Add `scripts/check-site.mjs` using `node:assert/strict` and `node:fs`. Assert that each generated public route has one main landmark, a canonical under `https://hitendra.dev`, expected navigation, and no `id="ash"`, `id="sun"`, or `data-eclipse`. Assert `/admin` and the seed post are absent from `dist`, and existing published post URLs still exist. Run against baseline and confirm the new-theme assertions fail.
- [x] Replace global styles and BaseLayout shell using the specified tokens. Add `--body` and `--heading` with the shared sans-serif stack and `--mono` with the native monospace stack. Preserve SEO and social metadata, add a skip link, and remove Google Fonts.
- [x] Replace navigation/footer, implement theme persistence and clipboard status, and remove the full-screen menu. No focus trap or scroll locking is needed when navigation remains visible.
- [x] Rework ProjectCard and BlogCard, implement the homepage hierarchy, and migrate all remaining public routes together. Keep post URLs and draft filtering unchanged.
- [x] Update profile bio/cardBio without changing resume or project claims. Keep original long descriptions as evidence; do not shorten away benchmark qualifiers.
- [x] Remove unused components and Lenis only after searching all imports. Regenerate the lockfile without upgrades.
- [x] Run `npm run build && node scripts/check-site.mjs` and exercise all routes in the browser.

Checkpoint: every route uses the professional design, all current content remains reachable, static checks pass, and theme/details/copy work with keyboard and touch.

### 3. Finish identity and verify

- [x] Produce the original HK favicon variants and 1200 × 630 social card. Use existing asset tooling when available; no runtime graphics dependency.
- [x] Update `CLAUDE.md` to describe the new direction and accurate routes. Leave archive instructions on its own branch.
- [ ] Run the complete verification matrix below, retain screenshots and exact command outputs, and inspect the final diff for unintended content or admin changes.
- [ ] Open `/plannotator-review` after implementation for visual diff review. Stop for annotations. Do not commit automatically.

Checkpoint: local implementation verified and ready for user review, with any unresolved external deployment access named explicitly.

### 4. Publish only when separately authorized

- [ ] Create the archive Vercel app from `deploy/chronicle`, record its assigned URL, and update only that branch's `site`. Verify public access and canonicals.
- [ ] Add the verified archive URL to the professional profile/footer and verify the outgoing link.
- [ ] Obtain release approval before committing, pushing, merging to `main`, or changing the production domain. Keep the original snapshot available for rollback.
- [ ] After authorized release, verify both the custom domain and archive URL and report their exact addresses.

## Verification

No build or local product tests have been run during planning. Reference HTTP fetches and the Chip Huyen browser inspection succeeded; the temporary browser session was closed.

After approval, run `npm run build && node scripts/check-site.mjs`. Expected result: build exits 0 and the checker prints `Static site checks passed`. Save real output, not this expectation.

Use Agent Browser in a task-specific session. Check `command -v portless` and `node -v`, inspect `portless list`, and start a background named server. If unavailable, use a free recorded local port without changing tracked configuration. Confirm its URL loads before testing.

| Check | Required result |
| --- | --- |
| Routes | `/`, `/projects`, `/blog`, every published post, `/contact`, `/tldr` load; unknown route shows 404 |
| Viewports | Screenshots at 390 × 844, 768 × 1024, 1440 × 900; no page overflow at 320px or 200% zoom |
| Theme | Light on first visit; dark/light toggles; survives navigation/reload; ignores legacy Eclipse storage; works with blocked storage |
| Project details | Native summaries respond to click, touch, Enter and Space; links stay separately usable; missing href never creates a fake anchor |
| Clipboard | Real copy succeeds on a secure local origin; denied permission shows honest failure text in a live status region; mailto remains usable |
| No JavaScript | All navigation, project content, details, articles and contact links usable; theme/copy controls hidden or harmless |
| Reduced motion | No animation loops or forced smooth scrolling; transitions disabled |
| Accessibility | Visible keyboard focus, skip link, current navigation state, 44px touch targets, logical headings; text contrast at least 4.5:1, UI indicators at least 3:1 |
| Blog rendering | Paragraphs, lists, code and tables legible in both themes; long content scrolls within its block, not the page |
| Content | Eight projects initially; three featured initially; all published posts retained; seed and other drafts absent |
| Metadata | Unique titles/descriptions, correct canonicals including `/tldr`, new favicon and 1200 × 630 social card; resume download remains intact |
| Admin | `/admin` renders in dev and lists existing items with the new tokens; create/delete temporary fixtures only in an isolated worktree, never overwrite user posts; no admin routes in production |
| Runtime | No uncaught browser errors or unexpected local asset failures; report third-party link failures separately |
| Archive | Exact snapshot reference preserved; public archive matches old presentation, with only declared metadata adjustments; new production remains unchanged until authorized |

Capture desktop/mobile home, projects, a real post, contact, and both theme states. Record the local URL, commands, console/network failures, screenshots, and static-check output in this plan. If browser test tooling cannot run, report the blocker rather than substituting a build for UI verification.

## Execution evidence

- Worktree: `/Users/hitesh/hitendra.dev-professional`, branch `redesign/professional`. Main remains at `dcc0afe9ba5fa5ae1bd90fbfd866bf87b12cb2cc`; `archive/chronicle` points to that exact commit.
- Used a sibling worktree to avoid changing main's ignore configuration. No commits were made.
- Production preview: `http://127.0.0.1:4322/`, command `npm run preview -- --host 127.0.0.1 --port 4322`.
- Initial dev server: `http://127.0.0.1:4321/`. A fresh dev server on `http://127.0.0.1:4323/` verified content-watcher behavior after dependency changes. Ports and owned process IDs are recorded under `/tmp/hitendra-professional-evidence/`.
- Portless is installed with Node 26, but no routes were active. Used loopback ports instead of starting a privileged proxy or altering shared trust/hosts settings.
- `npm ci` reported 10 pre-existing vulnerabilities: 1 low, 8 high, 1 critical. No unrelated dependency upgrades applied. The regenerated lockfile removes only Lenis.
- Baseline: 14 pages, eight projects, 30 home links. Build printed `14 page(s) built in 1.09s` and `Complete!`.
- Test-first static check failed against baseline with `404.html: legacy presentation`. Redesign passed with `Static site checks passed (14 pages)`.
- Added `scripts/check-browser.py` using Python's standard library and the installed Agent Browser CLI. Run with `python3 scripts/check-browser.py http://127.0.0.1:4322`. No test dependency added.
- Browser suite printed `Browser checks passed`: every public route at 320, 390, 768, and 1440px; theme persistence; legacy-key isolation; keyboard details; missing project URL; real clipboard write; denied clipboard status; blocked storage writes; reduced motion; skip-link focus; 404; introduction visible above fold.
- Separate blocked-storage session verified both reads and writes throwing before app startup. Separate JavaScript-disabled Chromium session verified visible project content, hidden theme control, and working native details.
- HTTP checks: resume, SVG/ICO icons, and social card return 200 with correct content types; production `/admin` and an unknown route return 404.
- Axe: homepage light, projects dark, and a real post dark report zero violations after transitions settle. An initial audit taken during the 160ms theme transition sampled outgoing text colors; the settled rerun passed.
- Admin panel renders existing items. Temporary post create/delete APIs returned 201/200. The old dev process missed a new route after dependency-triggered restart; a fresh process discovered it correctly. No application code changed for this. All temporary post fixtures were deleted.
- The temporary long-code/table post rendered at 320px without page overflow; code scrolled within its block and table text wrapped within the table.
- `git diff --check` passed. A content comparison against the archive showed no changes to project data, posts, admin code, resume, Astro config, or Vercel config.
- Evidence directory: `/tmp/hitendra-professional-evidence/`. Includes baseline screenshots, light/dark desktop/mobile captures of home/projects/contact/a real post, asset preview, build logs, browser logs, and axe JSON. These are local temporary artifacts, not committed files.

### Still open

- Step 17 remains partially complete: full physical touch interaction and actual browser-chrome 200% zoom were not verified. Responsive viewport checks and a 720px zoom-equivalent layout check passed. Not all third-party project URLs were fetched. Additional audit coverage can be run before release.
- Step 18: no `plannotator` CLI is on PATH and no code-review tool is exposed to this agent. The installed Pi extension documents `/plannotator-review`; invoke it from a Pi session opened in the professional worktree. Do not substitute chat approval for that review.
- Steps 19–22: the user authorized pushing the professional and preserved archive branches, not merging into `main`. Archive Vercel setup, archive footer link, and production release remain pending separate authorization and account access. No Vercel CLI is on PATH. The footer intentionally omits an unverified archive URL.

## Not doing

- No framework migration, new CMS, UI library, or backend.
- No invented publications, credentials, testimonials, or performance claims.
- No deleting the original version or publishing during planning.
- No full-site theme switch that bundles the old and new designs together.
- No chatbot, neural-network background, particle effects, carousels, project search, analytics, newsletter, or contact backend.
- No deletion or rewrite of personal blog posts. The professional homepage curates what it promotes.
- No publications section, fabricated work experience, new case-study routes, or mandatory portrait.
- No admin redesign, project schema migration, or test-framework dependency.
