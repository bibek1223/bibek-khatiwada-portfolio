"""Shared page chrome: <head>, header, footer. Every page goes through `page()`."""
import hashlib
import json
from html import escape
from pathlib import Path

from data import PERSON, SITE_URL

NAV = [
    ("about", "About", "about/"),
    ("services", "Services", "services/"),
    ("work", "Case studies", "case-studies/"),
    ("process", "Process", "#process"),
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
        <a class="nav-cta" href="{PERSON['whatsapp']}" target="_blank" rel="noreferrer">WhatsApp</a>
      </nav>
      <a class="cta" href="{PERSON['whatsapp']}" target="_blank" rel="noreferrer">WhatsApp</a>
      <button class="nav-toggle" type="button" aria-controls="site-nav" aria-expanded="false">
        <span class="nav-toggle-bars" aria-hidden="true"></span><span class="sr-only">Menu</span>
      </button>
    </div>
  </header>"""


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
  {header(active, root)}

  <main id="main">
{body.replace('{{root}}', root).replace('{{home}}', root or './')}
  </main>

  {footer(root)}
  <script src="{asset(root, 'js/site.js')}" defer></script>{extra}
</body>
</html>
"""
