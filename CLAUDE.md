# CLAUDE.md - Total Piling & Excavations

## Business Context

**Business Name:** Total Piling & Excavations
**Primary Contact:** Tom (day-to-day point of contact)
**Owner / Quote Email:** Rob - rob@totalpiling.com.au
**Phone:** 0419 008 549
**Locations:** Melbourne and Echuca, VIC (family-owned, services all of Victoria)
**Domain:** totalpilingandexcavations.com.au
**Instagram:** @totalpilingandexcavations
**Facebook:** https://www.facebook.com/profile.php?id=61583985463235
**Tagline / Positioning:** 20 years of foundation work. Government project experience.

### About
- Family-owned screw piling specialist serving Victoria for ~20 years
- Specialises in screw piling, underpinning, shoring/protection works, and screw pile sales
- Project mix spans residential, commercial, civil, and government work (government experience is the high-end anchor - lead with it on trust collateral). NOTE: "Tier 1" capability claims were removed from the whole site on 2026-06-23 at Tom + Harry's request; do not reintroduce "Tier 1" anywhere. Keep "government".
- Melbourne and Echuca dual base lets them quote regional VIC work other Melbourne-based piling contractors can't service economically
- Branding is dark/industrial - deep navy + sky-blue brand colour, amber accent, condensed display type. Already locked in via design tokens in `styles.css`. Do not invent new brand colours.

### Services
- **Screw Piling** - certified screw piles for residential, commercial, civil, and government foundations
- **Screw Pile Underpinning** - remediation of subsiding or failing foundations
- **Shoring and Protection Works** - temporary works for excavation safety
- **Screw Pile Sales and Distribution** - direct sales of piles to other contractors (Order Piles page)

### Service Area
Victoria-wide with hubs in Melbourne and Echuca. SEO targeting should lean on "screw piling Melbourne", "screw piles Victoria", "underpinning Melbourne", "shoring Melbourne", "helical piles", "foundation contractor Victoria" (already in `index.html` keywords meta).

### Trust / Compliance Assets in Site
- AA Steel Works partnership badge
- Australian Made and Owned badge
- Both live in `assets/trust/`. Only these two trust marks are signed-off - do not add new "as seen in" or certification logos without confirming with James.

---

## Always Do First
- **Invoke the `frontend-design` skill** before writing any frontend code, every session, no exceptions.
- Read this file end-to-end before touching markup, CSS, or assets. The brand system and "no contact form" rule below are easy to violate by reflex.

## Project Stack (this is a SHIPPED PRODUCTION SITE, not a mockup)
- Plain HTML/CSS/JS - **no Tailwind CDN, no build step, no framework**
- External stylesheet: `styles.css` (single file, design-token driven)
- External script: `script.js`
- Multi-page site, each page is its own `.html` file
- Fonts: Inter (body) + Barlow Condensed (display/headings, uppercase) - loaded via Google Fonts in each page's `<head>`
- Hero video: `assets/hero/hero-video.mp4`

### Design Tokens (locked - in `styles.css :root`)
| Token | Value | Use |
|---|---|---|
| `--c-bg` | `#0A0E13` | Page background |
| `--c-bg-elevated` | `#11161D` | Elevated surfaces |
| `--c-bg-card` | `#161D26` | Cards |
| `--c-border` | `#1F2832` | Borders / hairlines |
| `--c-text` | `#ECEFF4` | Primary text |
| `--c-text-muted` | `#9AA5B4` | Secondary text |
| `--c-brand` | `#5BA7CC` | Brand primary (sky blue) |
| `--c-brand-bright` | `#7EC4E8` | Brand hover / link |
| `--c-brand-deep` | `#2B6A8A` | Brand deep accent |
| `--c-accent` | `#F5A623` | Amber accent (use sparingly) |

Reuse the existing tokens, spacing scale (`--space-1` through `--space-8`), and easing variable (`--ease-out`). Do not introduce parallel colour or spacing systems.

## Page Inventory
Top-level (in folder root):
- `index.html` - Home
- `services.html` - Services overview (4 alternating sections + 5-step process + capability band)
- `about.html`
- `projects.html`
- `faq.html`
- `contact.html`
- `order-piles.html` - Screw pile sales / distribution funnel

Per-service deep dives (in `services/`):
- `services/screw-piling.html`
- `services/underpinning.html`
- `services/shoring.html`

When adding a new page, update `sitemap.xml` in the same commit.

## Assets
- `assets/logo/Logo.avif` - canonical logo, used for favicon, apple-touch-icon, and schema `logo`/`image`
- `assets/hero/hero-video.mp4` - homepage hero background
- `assets/projects/` - real project photography (screw piling Melbourne CBD, rural aerial grids, residential, pool/pit work, waterfront, etc.) - prefer these over stock
- `assets/services/` - service section hero stills (screw-piling, shoring, underpinning, sales, about)
- `assets/photo for services etc/` - newer raw photos (HEIC + JPG). Convert HEIC to .avif/.webp before referencing from HTML
- `assets/trust/` - AA Steel Works, Australian Made + Owned badges only

Always check `assets/` before reaching for placeholders or stock imagery.

---

## Deployment
- **Git remote:** `git@github.com:suterasites/TPE.git` (push to `main`)
- **Cloudflare Pages project:** `tpe-12t`
- **Preview URL:** https://tpe-12t.pages.dev/
- **Production URL:** https://www.totalpilingandexcavations.com.au/ (DNS cutover from Wix pending - until then, the preview URL is the live URL for testing)
- Cloudflare auto-deploys on push to `main`. After any code change: `git add` → `git commit` → `git push origin main`, then watch the Cloudflare deploy.
- Do NOT cancel the Wix Business plan until DNS is cut over and Tom has confirmed the new site is serving on the apex domain.

## Multi-Page Consistency
- **Header / nav:** Desktop mega-nav, mobile nav, and footer must stay in sync across every `.html` file. Service links across all three nav surfaces point to `/services.html#anchor` (not standalone service pages from the nav itself - the per-service pages are linked from the overview).
- **Footer:** Identical across all pages.
- **Internal links:** When adding a new page, scan all existing pages and update any references to that topic to link in.

---

## Hard Rules - Client-Specific
- **NO contact form anywhere on the site.** Tom explicitly removed the homepage form on 2026-05-20. TPE takes enquiries via phone and email only. Any new page or section must use oversized phone (0419 008 549) + email (rob@totalpiling.com.au) blocks, not a Formspree form. (This is the opposite of the Apollo / ANSC pattern - do not copy-paste a contact form from another client site into TPE.)
- **Do not change the brand colour palette** or swap the dark theme for light. The dark + sky-blue + amber system was signed off with Tom and his boss on 2026-05-20.
- **No "Tier 1" anywhere on the site.** Tom + Harry asked to remove all Tier 1 capability claims on 2026-06-23 (site-wide pass done that day). "Government" experience is retained and is now the high-end trust anchor. Do not reintroduce "Tier 1" in copy, meta, schema, or keywords.
- **No "same-day / next-day dispatch" promises for pile supply.** Removed on 2026-06-23 because TPE cannot always hit it. Frame pile dispatch as "ships from our own inventory" with "a firm dispatch date confirmed on your quote".
- **No quote / response / turnaround time promises anywhere.** Removed on 2026-06-23: no "24 hours", "inside one business day", "next/same business day", "come back same day", "inside the hour", "phone replies during business hours", "monitored daily", "price quickly", or even the vague "fast turnaround" (was in the shared mega-nav blurb -> now "family-run"). Frame quoting by what it IS, not how fast: "itemised quotes off your real documents (plans, engineering, soil report), not estimates, no obligation". The About + Contact "turnaround" stats were re-themed to "Quoting / Off real documents". 2026-06-23 (later): James escalated to remove ALL install-speed claims too: "hours not days", "no curing time", "immediate load capability", "installed in hours", "done in a day / same day", underpinning "1 to 3 days", "on site within the week", plus the "Hours Not Days" page title. Re-leaned copy on non-speed benefits (no excavation/concrete/spoil, minimal disruption, reactive-clay strength, removable, AS2159, Australian-made). ONLY timing that stays: the operating-hours stat (Mon-Fri 7-5 / Sat 10-1). Do not reintroduce any speed/turnaround claim anywhere.
- **FAQ page content = client's 14-question set (supplied 2026-06-23).** faq.html visible + JSON-LD FAQPage were replaced with Tom + Harry's 14 questions. NOTE: their supplied FAQ #3 ("benefits vs concrete") listed "quick installation (often within hours)" and "no curing time (can build immediately)" - these were dropped to honour the no-speed-claims rule above. If James later says to restore them, that rule has been overridden for the FAQ.
- **Family-owned, ~20 years, VIC-based** - all three are load-bearing trust facts; keep them prominent on Home and About.

## Hard Rules - Inherited
- Do not add sections, features, or content not in the brief or backlog (see `CRM/clients/Total Piling & Excavations/status.md` for current page backlog)
- Do not use `transition-all`
- Do not use default Tailwind blue/indigo as primary colour (n/a here - we're not on Tailwind, but the spirit applies: stick to the locked palette)
- Do not use em dashes (—) or en dashes (–) anywhere in content, code, or comments. Use hyphens (-), commas, or periods instead
- Mobile-first responsive on every change
- Every interactive element needs hover, focus-visible, and active states

---

## Cross-References
- **CRM profile:** `../../../CRM/clients/Total Piling & Excavations/profile.md`
- **CRM status (current page backlog + next actions):** `../../../CRM/clients/Total Piling & Excavations/status.md`
- **Subscription / billing:** `../../../CRM/clients/Total Piling & Excavations/financials.md` ($150/mo, 6-month lock-in through 2026-11-20)
- **Website service summary:** `../../../CRM/clients/Total Piling & Excavations/services/website.md`
- **Monthly update SOP:** `../../../CRM/clients/Total Piling & Excavations/services/monthly-update.md`
