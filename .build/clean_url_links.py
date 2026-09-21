#!/usr/bin/env python3
"""
clean_url_links.py - point every internal reference at the URL the host actually
serves, instead of the one that 308-redirects to it.

WHY. On 2026-09-21 Google Search Console had 12 of TPE's 16 pages outside the
index: 8 "Discovered - currently not indexed" and 4 "URL is unknown to Google",
among them /services, /services/shoring and all six regional screw piling pages,
live since at least 2026-09-03. It was not robots.txt (Allow: /), not the sitemap
(all 16 clean URLs, downloaded by Google on 09-16) and not the canonicals (0034caa
already moved those). It was discovery: every internal link, every og:url and
every BreadcrumbList item still named the `.html` form, and Cloudflare Pages 308s
`.html` to the extension-less URL. So the only path Google had into a page was a
redirect, and the clean URL - the one the canonical and the sitemap both nominate -
was linked from nowhere on the site. Same fault, same fix, as TJM Detailing on
2026-09-03.

WHAT IT REWRITES, and nothing else:

    href="/page.html"          -> href="/page"           (index.html -> "/")
    href="/page.html#anchor"   -> href="/page#anchor"
    href="/services/x.html"    -> href="/services/x"
    <meta og:url ...>          -> the clean URL
    JSON-LD "url"/"item"/"@id" -> the clean URL

Every `.html` href on this site is root-absolute (checked before writing this), so
the rewrite is a strip, not a resolve. Anything on another domain is left alone.

The regional pages are generated - gen_city_pages.py was fixed in the same commit
to emit clean URLs, or the next rebuild would have put every one of these back.

Idempotent - a second run finds nothing to do. Dry run by default, --apply writes.
"""

import argparse
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://www.totalpilingandexcavations.com.au"

# href="/slug.html", href="/services/slug.html", either with an optional #anchor.
HREF = re.compile(r'(href\s*=\s*")/((?:[A-Za-z0-9_-]+/)*)([A-Za-z0-9._-]+)\.html((?:#[^"]*)?")')
# Absolute self-referencing URLs inside content="" and JSON-LD "url"/"item"/"@id".
ABS = re.compile(r'(' + re.escape(DOMAIN) + r'/)((?:[A-Za-z0-9_-]+/)*)([A-Za-z0-9._-]+)\.html\b')


def clean_href(m):
    folder, slug = m.group(2), m.group(3)
    return m.group(1) + "/" + folder + ("" if slug == "index" else slug) + m.group(4)


def clean_abs(m):
    folder, slug = m.group(2), m.group(3)
    return m.group(1) + folder + ("" if slug == "index" else slug)


def pages():
    return sorted(glob.glob(os.path.join(ROOT, "*.html"))
                  + glob.glob(os.path.join(ROOT, "services", "*.html")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    total = 0
    touched = 0
    for path in pages():
        txt = open(path, encoding="utf-8").read()
        new, n1 = HREF.subn(clean_href, txt)
        new, n2 = ABS.subn(clean_abs, new)
        n = n1 + n2
        if not n:
            continue
        touched += 1
        total += n
        print("  %-46s %4d  (%d href, %d absolute)"
              % (os.path.relpath(path, ROOT), n, n1, n2))
        if args.apply:
            open(path, "w", encoding="utf-8").write(new)

    print("\n%d reference(s) across %d file(s)%s"
          % (total, touched, "" if args.apply else "  [dry run - use --apply]"))

    if args.apply:
        # Nothing may name a .html URL afterwards. A leftover means a form this
        # script does not understand, and a silent partial sweep is worse than none.
        left = []
        for path in pages():
            txt = open(path, encoding="utf-8").read()
            for m in re.finditer(r'(?:href\s*=\s*"[^"]*|' + re.escape(DOMAIN)
                                 + r'/[^"\s]*)\.html\b', txt):
                left.append("%s: %s" % (os.path.relpath(path, ROOT), m.group(0)[:70]))
        if left:
            print("\nFAIL - %d reference(s) survived the sweep:" % len(left))
            for line in left[:20]:
                print("  " + line)
            return 1
        print("verified: no internal reference names a .html URL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
