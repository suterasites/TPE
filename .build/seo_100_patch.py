#!/usr/bin/env python3
"""seo_100_patch.py - idempotent on-page SEO patcher for the Total Piling site.

Brings every page to a clean pass on the machine-checkable checks in
Apps/sutera-seo/checklist.py (the engine behind SEO HQ). Safe to re-run.

The site is already strong (main, skip-link, twitter, landmarks all pass), so
this only touches the remaining findings:
  - trim 10 over-long meta descriptions (190-248 -> 150-160)
  - trim 8 over-long titles (75-98 -> 50-60)
  - footer column headings h4 -> h3 (kills the H2->H4 skip); the .footer-col h3
    CSS rule in styles.css replicates the old h4 look
  - faq: add the LocalBusiness node (mirrored from index) it was missing
  - explicit width/height on every <img> from the real asset (styles.css now
    carries a global img{height:auto} so the attrs are a pure CLS/aspect hint)

Copy respects the TPE hard rules: no speed/turnaround claims, no "Tier 1",
family-owned / 20 years / VIC kept prominent, no em dashes.

Homepage breadcrumb (visible + schema) is deliberately left as the only two
warns - a homepage crumb is pointless UX - and the pooled score rounds to 100.
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALL_FILES = [
    "index.html", "services.html", "services/screw-piling.html",
    "services/underpinning.html", "services/shoring.html", "order-piles.html",
    "about.html", "projects.html", "faq.html", "contact.html",
]

# title rewrites (50-60 band)
TITLES = {
    "services.html": "Screw Piling & Shoring Victoria | Total Piling & Excavations",
    "services/underpinning.html": "Underpinning Melbourne | Total Piling & Excavations",
    "services/shoring.html": "Shoring & Protection Melbourne | Total Piling & Excavations",
    "order-piles.html": "Buy Screw Piles Direct | Total Piling & Excavations",
    "about.html": "About Total Piling & Excavations | Screw Piling Victoria",
    "projects.html": "Screw Piling Projects Victoria | Total Piling & Excavations",
    "faq.html": "Screw Piling FAQ, Answered | Total Piling & Excavations",
    "contact.html": "Contact Total Piling & Excavations | Melbourne & Echuca",
}

# meta-description rewrites (150-160 band, no speed/turnaround claims)
METAS = {
    "index.html": "Specialist screw piling, underpinning and shoring across Victoria. 20 years of certified foundation work for residential, commercial and civil projects.",
    "services.html": "Specialist piling and foundation services across Victoria: screw piling, underpinning, shoring, and Australian-made screw pile sales. Melbourne and Echuca based.",
    "services/screw-piling.html": "Certified screw pile installation across Melbourne, Echuca and all of Victoria. AS2159 engineered, 100% Australian-made piles, certificate on completion.",
    "services/underpinning.html": "Screw pile underpinning across Melbourne and Victoria. Stabilise settling foundations, cracking walls and uneven floors with minimal, tight-access excavation.",
    "services/shoring.html": "Shoring and protection across Melbourne and Victoria. Residential panels through to heavy commercial systems for pool digs, basements and boundary protection.",
    "order-piles.html": "Direct supply of 100% Australian-made screw piles across Victoria. 76mm to 114mm stocked, custom sizes to order, plus drive tools and pile caps. No minimum order.",
    "about.html": "Family-owned Victorian foundation specialists. 20 years installing certified screw piles across residential, commercial and civil sites. Melbourne and Echuca based.",
    "projects.html": "20 years of certified screw piling across Victoria: CBD commercial, residential developments, waterfront builds, pool foundations and rural regional installs.",
    "faq.html": "Plain-English answers to common screw piling questions: how they work, install method, soil types, AS2159 certification, costs and ordering piles direct.",
    "contact.html": "Get in touch with Total Piling & Excavations. Call Rob on 0419 008 549 or Tom on 0448 725 807, or email rob@totalpiling.com.au. Quotes across Victoria.",
}

_DIM_CACHE = {}


def img_dims(src, base):
    """Measure a local asset. src is resolved relative to `base` (the page's own
    directory) so ../assets paths on the services/ subpages resolve correctly,
    or relative to ROOT for a root-anchored /path."""
    src = src.split("?")[0].split("#")[0]
    if src.startswith(("http://", "https://", "data:", "//")):
        return None
    anchor = ROOT if src.startswith("/") else base
    path = os.path.normpath(os.path.join(anchor, src.lstrip("/")))
    if path in _DIM_CACHE:
        return _DIM_CACHE[path]
    if not path.startswith(ROOT) or not os.path.isfile(path):
        _DIM_CACHE[path] = None
        return None
    import subprocess
    try:
        out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
                             capture_output=True, text=True, timeout=20).stdout
        w = re.search(r"pixelWidth:\s*(\d+)", out)
        h = re.search(r"pixelHeight:\s*(\d+)", out)
        dims = (int(w.group(1)), int(h.group(1))) if w and h else None
    except Exception:
        dims = None
    _DIM_CACHE[path] = dims
    return dims


def business_node():
    """Pull the LocalBusiness node verbatim from index.html's @graph."""
    h = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        for node in d.get("@graph", [d]):
            t = node.get("@type", "")
            if t == "LocalBusiness" or (isinstance(t, list) and "LocalBusiness" in t):
                return node
    return None


def patch(fn, biz):
    path = os.path.join(ROOT, fn)
    html = open(path, encoding="utf-8").read()
    orig = html
    did = []
    key = fn.replace(os.sep, "/")

    # --- title ---
    if key in TITLES:
        html2 = re.sub(r"<title>.*?</title>", "<title>" + TITLES[key] + "</title>", html, count=1, flags=re.S)
        if html2 != html:
            html = html2
            did.append(f"title({len(TITLES[key])})")

    # --- meta description ---
    if key in METAS:
        new = METAS[key]
        html2 = re.sub(r'(<meta name="description" content=")[^"]*(")',
                       lambda m: m.group(1) + new + m.group(2), html, count=1)
        if html2 != html:
            html = html2
            did.append(f"desc({len(new)})")

    # --- footer column headings h4 -> h3 (all h4 on the page are footer columns) ---
    if "<h4" in html:
        html = re.sub(r"<h4(\b[^>]*)>", r"<h3\1>", html)
        html = html.replace("</h4>", "</h3>")
        did.append("footer-h3")

    # --- faq: add the missing LocalBusiness node ---
    if key == "faq.html" and biz and '"LocalBusiness"' not in html:
        block = ('<script type="application/ld+json">\n'
                 + json.dumps({"@context": "https://schema.org", **biz}, indent=2, ensure_ascii=False)
                 + "\n</script>\n")
        html = html.replace("</head>", block + "</head>", 1)
        did.append("localbusiness")

    # --- explicit width/height on <img> ---
    page_dir = os.path.dirname(path)

    def add_dims(m):
        tag = m.group(0)
        if re.search(r"\bwidth=", tag) and re.search(r"\bheight=", tag):
            return tag
        s = re.search(r'\bsrc="([^"]+)"', tag)
        if not s:
            return tag
        d = img_dims(s.group(1), page_dir)
        if not d:
            return tag
        return re.sub(r"<img\b", f'<img width="{d[0]}" height="{d[1]}"', tag, count=1)

    new_html = re.sub(r"<img\b[^>]*?>", add_dims, html)
    if new_html != html:
        did.append("img-dims")
        html = new_html

    if html != orig:
        open(path, "w", encoding="utf-8").write(html)
    return did


def main():
    biz = business_node()
    print(f"Patching {len(ALL_FILES)} pages under {ROOT}")
    print(f"business node: {'found' if biz else 'MISSING'}\n")
    for fn in ALL_FILES:
        changed = patch(fn, biz)
        print(f"  {fn:34s} {', '.join(changed) if changed else 'no change'}")
    print("\nDone. Idempotent - safe to re-run.")


if __name__ == "__main__":
    main()
