"""Shared page chrome: <head>, header, footer. Every page goes through `page()`."""
import hashlib
import json
from html import escape
from pathlib import Path

from data import (ARTICLES, CASE_STUDIES, FRAMEWORKS, INDUSTRIES_MATRIX, PERSON,
                  SERVICES, SITE_URL, TOOLS_SHOWCASE)

NAV = [
    ("about", "About", "about/"),
    ("services", "Services", "services/"),
    ("work", "Case studies", "case-studies/"),
    ("tools", "Tools", "tools/"),
    ("frameworks", "Frameworks", "frameworks/"),
    ("roi", "ROI Calc", "roi-calculator/"),
    ("contact", "Contact", "contact/"),
]

FONTS = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800"
         "&family=Manrope:wght@500;600;700;800&family=Caveat:wght@600;700&display=swap")


ASSETS = Path(__file__).parent.parent / "design" / "assets"


def asset(root, rel):
    """URL for a file under design/assets, with a content hash so browsers refetch after edits."""
    digest = hashlib.sha1((ASSETS / rel).read_bytes()).hexdigest()[:8]
    return f"{root}assets/{rel}?v={digest}"


def person_ref():
    return {"@id": f"{SITE_URL}/#person"}


def person_node():
    return {
        "@type": "Person",
        "@id": f"{SITE_URL}/#person",
        "name": PERSON["name"],
        "url": f"{SITE_URL}/",
        "image": f"{SITE_URL}/assets/bibek-khatiwada-profile.webp",
        "jobTitle": PERSON["role"],
        "description": "SEO strategist specializing in technical SEO, content systems, automation, AI search visibility, and Search Console-led growth.",
        "email": f"mailto:{PERSON['email']}",
        "telephone": PERSON["phone_href"],
        "address": {"@type": "PostalAddress", "addressLocality": "Kathmandu", "addressCountry": "NP"},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "Ratna Rajya Campus, Tribhuvan University"},
        "knowsLanguage": ["en", "ne"],
        "sameAs": [PERSON["linkedin"], PERSON["github"], PERSON["whatsapp"], PERSON["google_profile"]],
        "knowsAbout": ["Technical SEO", "On-page SEO", "Off-page SEO", "Content strategy", "SEO automation",
                       "AI search optimization", "LLM tracking", "Search Console analytics"],
    }


def breadcrumbs(trail):
    """trail: list of (name, path) from the home page down."""
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": f"{SITE_URL}/{path}"}
            for i, (name, path) in enumerate(trail)
        ],
    }


def head(meta, root):
    url = f"{SITE_URL}/{meta['path']}"
    title = escape(meta["title"])
    desc = escape(meta["description"])
    image = f"{SITE_URL}/assets/bibek-khatiwada-profile.webp"
    graph = json.dumps({"@context": "https://schema.org", "@graph": meta.get("graph", [])},
                       indent=2, ensure_ascii=False)
    robots = '\n  <meta name="robots" content="noindex">' if meta.get("noindex") else ""
    canonical = "" if meta.get("noindex") else f'\n  <link rel="canonical" href="{url}">'
    return f"""<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">{canonical}{robots}
  <meta property="og:type" content="{meta.get('og_type', 'website')}">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{image}">
  <meta property="og:image:alt" content="Bibek Khatiwada, SEO strategist">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{image}">
  <script type="application/ld+json">
{graph}
  </script>
  <meta name="theme-color" content="#ff8a65">
  <link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="{asset(root, 'css/site.css')}">
</head>"""


def header(active, root):
    home = root or "./"
    links = []
    for key, label, href in NAV:
        target = (home + href) if href.startswith("#") else root + href
        current = ' aria-current="page"' if key == active else ""
        links.append(f'<a href="{target}"{current}>{label}</a>')
    nav = "\n        ".join(links)
    return f"""<a class="skip" href="#main">Skip to content</a>
  <div class="float-shapes" aria-hidden="true">
    <div class="shape s1"></div>
    <div class="shape s2"></div>
    <div class="shape s3"></div>
  </div>

  <header class="topbar">
    <div class="wrap topbar-in">
      <a class="brand" href="{home}">
        <div class="brand-badge" aria-hidden="true">BK</div>
        <div class="brand-name">
          <b>Bibek Khatiwada</b>
          <span>SEO Strategist</span>
        </div>
      </a>
      <nav class="nav" id="site-nav" aria-label="Primary">
        {nav}
        <button class="search-trigger" type="button" data-search-open aria-haspopup="dialog"><span aria-hidden="true">⌕</span> Search <kbd>⌘K</kbd></button>
        <a class="nav-cta" href="{PERSON['whatsapp']}" target="_blank" rel="noreferrer">WhatsApp</a>
      </nav>
      <a class="cta" href="{PERSON['whatsapp']}" target="_blank" rel="noreferrer">WhatsApp</a>
      <button class="nav-toggle" type="button" aria-controls="site-nav" aria-expanded="false">
        <span class="nav-toggle-bars" aria-hidden="true"></span><span class="sr-only">Menu</span>
      </button>
    </div>
  </header>"""


def search_overlay(root):
    """Site-wide command palette. The catalog is generated from the same data as the pages."""
    entries = [
        ("Home", "Overview, selected work and capabilities", "", "page"),
        ("About Bibek", "Career, background and working style", "about/", "page"),
        ("Services", "Technical SEO, content systems, automation and AI search", "services/", "page"),
        ("How I work", "Engagement process, deliverables and collaboration model", "process/", "page"),
        ("Case studies", "Nine anonymized Search Console case studies", "case-studies/", "page"),
        ("Tools", "Interactive SEO utilities and system prototypes", "tools/", "page"),
        ("Frameworks", "Search mechanics and technical playbooks", "frameworks/", "page"),
        ("Industries", "Search blueprints by market and site model", "industries/", "page"),
        ("Insights", "Technical writing on search and AI visibility", "blog/", "page"),
        ("SEO diagnostic", "Build a diagnostic brief in three steps", "audit/", "action"),
        ("Contact", "Email, WhatsApp and project brief builder", "contact/", "action"),
    ]
    entries += [(f"Case {c['n']}: {c['short']}", c['chip'], f"case-studies/{c['slug']}/", "case study") for c in CASE_STUDIES]
    entries += [(f["title"], f["summary"], f"frameworks/{f['slug']}/", "framework") for f in FRAMEWORKS]
    entries += [(i["title"], i["summary"], f"industries/{i['slug']}/", "industry") for i in INDUSTRIES_MATRIX]
    entries += [(a["title"], a["summary"], f"blog/{a['slug']}/", "insight") for a in ARTICLES
                if (Path(__file__).parent / "content" / f"{a['slug']}.html").exists()]
    entries += [(s["name"], s["summary"], f"services/#{s['id']}", "service") for s in SERVICES]
    entries += [(t["name"], t["summary"], "tools/", "tool") for t in TOOLS_SHOWCASE]
    payload = json.dumps([
        {"title": title, "description": description, "url": root + path, "type": kind}
        for title, description, path, kind in entries
    ], ensure_ascii=False).replace("</", "<\\/")
    return f"""<div class="site-progress" aria-hidden="true"><i></i></div>
  <div class="site-search" data-site-search hidden>
    <div class="site-search-backdrop" data-search-close></div>
    <section class="site-search-panel" role="dialog" aria-modal="true" aria-labelledby="site-search-title">
      <div class="site-search-head">
        <div><span class="mini-note">Navigate the portfolio</span><h2 id="site-search-title">Find a page, proof point or service</h2></div>
        <button type="button" class="search-close" data-search-close aria-label="Close search">×</button>
      </div>
      <label class="search-field"><span class="sr-only">Search the portfolio</span><span aria-hidden="true">⌕</span><input type="search" data-search-input placeholder="Try ‘crawl budget’, ‘SaaS’, or ‘process’" autocomplete="off"></label>
      <div class="search-meta"><span data-search-count></span><span>↑ ↓ move · Enter open · Esc close</span></div>
      <div class="search-results" data-search-results role="listbox" aria-label="Search results"></div>
      <p class="search-empty" data-search-empty hidden>No close match. Try a service, industry, case number or technical topic.</p>
    </section>
    <script type="application/json" data-search-index>{payload}</script>
  </div>
  <button class="page-outline-toggle" type="button" data-outline-toggle hidden aria-expanded="false" aria-controls="page-outline"><span aria-hidden="true">☰</span><span>On this page</span></button>
  <aside class="page-outline" id="page-outline" data-page-outline hidden aria-label="On this page">
    <div class="page-outline-head"><span>On this page</span><button type="button" data-outline-close aria-label="Close section navigation">×</button></div>
    <nav data-outline-links></nav>
  </aside>"""


def footer(root):
    home = root or "./"
    return f"""<footer>
    <div class="wrap footer-grid">
      <div>
        <div class="footer-name">Bibek Khatiwada</div>
        <div class="tiny" style="margin-top:.35rem;color:var(--purple)">SEO Strategist · Entity-based, Semantic &amp; AI Search Optimization</div>
        <p class="footer-note">Kathmandu, Nepal · Open to remote work</p>
      </div>
      <nav aria-label="Site">
        <div class="tiny footer-h">Pages</div>
        <a href="{home}">Home</a>
        <a href="{root}about/">About</a>
        <a href="{root}services/">Services</a>
        <a href="{root}case-studies/">Case studies</a>
        <a href="{root}tools/">Tools</a>
        <a href="{root}frameworks/">Frameworks</a>
        <a href="{root}industries/">Industries</a>
        <a href="{root}roi-calculator/">ROI Calculator</a>
        <a href="{root}glossary/">Search Glossary</a>
        <a href="{root}blog/">Insights</a>
        <a href="{root}audit/">Audit Diagnostic</a>
        <a href="{root}contact/">Contact</a>
      </nav>
      <nav aria-label="Elsewhere">
        <div class="tiny footer-h">Elsewhere</div>
        <a href="{PERSON['linkedin']}" target="_blank" rel="noreferrer">LinkedIn</a>
        <a href="{PERSON['github']}" target="_blank" rel="noreferrer">GitHub</a>
        <a href="{PERSON['whatsapp']}" target="_blank" rel="noreferrer">WhatsApp</a>
        <a href="{PERSON['google_profile']}" target="_blank" rel="noreferrer">Google profile</a>
      </nav>
      <div>
        <div class="tiny footer-h">Direct</div>
        <a href="mailto:{PERSON['email']}">{PERSON['email']}</a>
        <a href="tel:{PERSON['phone_href']}">{PERSON['phone_display']}</a>
        <a href="{root}privacy/">Privacy</a>
      </div>
    </div>
    <div class="wrap footer-base tiny">
      <span>© <span data-year>2026</span> Bibek Khatiwada</span>
      <a href="#main" class="to-top">Back to top ↑</a>
    </div>
  </footer>"""


def page(meta, body, active="", scripts=()):
    """Assemble a full HTML document. meta['path'] is the URL path, '' for home."""
    depth = meta["path"].count("/")
    root = "../" * depth
    if meta.get("absolute_root"):
        root = "/"
    extra = "".join(f'\n  <script src="{asset(root, "js/" + s)}" defer></script>' for s in scripts)
    return f"""<!doctype html>
<!-- Generated by site/build.py. Edit the source in /site, then run: python3 site/build.py -->
<html lang="en">
{head(meta, root)}
<body class="page-{meta.get('slug', 'home')}">
  {search_overlay(root)}
  {header(active, root)}

  <main id="main">
{body.replace('{{root}}', root).replace('{{home}}', root or './')}
  </main>

  {footer(root)}
  <script src="{asset(root, 'js/site.js')}" defer></script>{extra}
</body>
</html>
"""
