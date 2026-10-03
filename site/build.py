"""Build the static site into ../design (the deploy folder).

Usage:  python3 site/build.py
Stdlib only. Page chrome lives in layout.py, facts in data.py, prose in content/.
"""
import json
import re
from datetime import date
from html import escape
from pathlib import Path

from data import (ACHIEVEMENTS, ARTICLES, CASE_STUDIES, COUNTRIES, FILTERS, FRAMEWORKS,
                  GLOSSARY_TERMS, INDUSTRIES_MATRIX, PERSON, PLATFORMS, ROI_PRESETS,
                  SERVICES, SITE_URL, TIMELINE, TOOLS, TOOLS_SHOWCASE)
from layout import breadcrumbs, page, person_node, person_ref

SRC = Path(__file__).parent
OUT = SRC.parent / "design"
BY_N = {cs["n"]: cs for cs in CASE_STUDIES}
TODAY = date.today().isoformat()


def fragment(name, **blocks):
    html = (SRC / "content" / name).read_text()
    for key, value in blocks.items():
        token = "{{" + key + "}}"
        assert token in html, f"{name} is missing {token}"
        html = html.replace(token, value)
    leftover = re.findall(r"\{\{(?!root|home)\w+\}\}", html)
    assert not leftover, f"{name} has unfilled tokens {leftover}"
    return html


def write(path, html):
    target = OUT / path / "index.html" if path else OUT / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html)
    return path


def webpage(path, name, trail, extra=()):
    return [
        person_node(),
        {"@type": "WebSite", "@id": f"{SITE_URL}/#website", "url": f"{SITE_URL}/",
         "name": "Bibek Khatiwada — SEO Strategist", "publisher": person_ref(), "inLanguage": "en"},
        {"@type": "WebPage", "@id": f"{SITE_URL}/{path}#webpage", "url": f"{SITE_URL}/{path}", "name": name,
         "isPartOf": {"@id": f"{SITE_URL}/#website"}, "about": person_ref(), "inLanguage": "en"},
        breadcrumbs(trail),
        *extra,
    ]


# ---------- shared snippets ----------

def case_card(cs):
    """Compact card used on the case-study index and in 'related' lists."""
    if cs.get("yoy"):
        headline = f'<strong>{cs["clicks_delta"]}</strong><span>clicks, year over year</span>'
    else:
        headline = f'<strong>{cs["clicks_d"]}</strong><span>clicks · {cs["window"]}</span>'
    
    sparkline = ""
    if cs["n"] == "01":
        sparkline = """<div class="cs-sparkline" aria-hidden="true">
            <svg viewBox="0 0 200 44" preserveAspectRatio="none">
              <defs>
                <linearGradient id="grad-cs-01" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.25"/>
                  <stop offset="100%" stop-color="#7c3aed" stop-opacity="0.0"/>
                </linearGradient>
              </defs>
              <path d="M 0 34 C 40 42, 70 36, 100 24 C 130 14, 160 8, 200 4" fill="none" stroke="#7c3aed" stroke-width="2.5" stroke-linecap="round"/>
              <path d="M 0 34 C 40 42, 70 36, 100 24 C 130 14, 160 8, 200 4 L 200 44 L 0 44 Z" fill="url(#grad-cs-01)"/>
              <circle cx="200" cy="4" r="3.5" fill="#7c3aed"/>
            </svg>
            <span class="sparkline-label">16-Mo Trajectory · +1.47B Impressions</span>
          </div>"""
    elif cs["n"] == "02":
        sparkline = """<div class="cs-sparkline" aria-hidden="true">
            <svg viewBox="0 0 200 44" preserveAspectRatio="none">
              <defs>
                <linearGradient id="grad-cs-02" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#0284c7" stop-opacity="0.25"/>
                  <stop offset="100%" stop-color="#0284c7" stop-opacity="0.0"/>
                </linearGradient>
              </defs>
              <path d="M 0 40 C 50 38, 90 26, 130 16 C 160 10, 180 6, 200 4" fill="none" stroke="#0284c7" stroke-width="2.5" stroke-linecap="round"/>
              <path d="M 0 40 C 50 38, 90 26, 130 16 C 160 10, 180 6, 200 4 L 200 44 L 0 44 Z" fill="url(#grad-cs-02)"/>
              <circle cx="200" cy="4" r="3.5" fill="#0284c7"/>
            </svg>
            <span class="sparkline-label">Programmatic Scaling · 117M Impr / 1.12M Clicks</span>
          </div>"""
    elif cs["n"] == "03":
        sparkline = """<div class="cs-sparkline" aria-hidden="true">
            <svg viewBox="0 0 200 44" preserveAspectRatio="none">
              <defs>
                <linearGradient id="grad-cs-03" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#059669" stop-opacity="0.25"/>
                  <stop offset="100%" stop-color="#059669" stop-opacity="0.0"/>
                </linearGradient>
              </defs>
              <path d="M 0 38 C 50 40, 95 30, 135 18 C 165 12, 185 6, 200 4" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round"/>
              <path d="M 0 38 C 50 40, 95 30, 135 18 C 165 12, 185 6, 200 4 L 200 44 L 0 44 Z" fill="url(#grad-cs-03)"/>
              <circle cx="200" cy="4" r="3.5" fill="#059669"/>
            </svg>
            <span class="sparkline-label">Post-SSR Surge · 449K Clicks / 40.8M Impr</span>
          </div>"""

    return f"""<a class="cs-card" href="{{{{root}}}}case-studies/{cs['slug']}/" data-n="{cs['n']}">
          <span class="cs-card-top"><span class="case-id">Case {cs['n']}</span><span class="chipline">{escape(cs['chip'])}</span></span>
          <span class="cs-card-title">{escape(cs['card'])}</span>
          <span class="cs-card-metric">{headline}</span>
          {sparkline}
          <span class="cs-card-meta"><span>{cs['impr_d']} impr.</span><span>{cs['ctr']}% CTR</span><span>Pos. {cs['pos']:g}</span></span>
          <span class="cs-card-go" aria-hidden="true">→</span>
        </a>"""


def article_card(art):
    """Card for blog and technical frameworks."""
    return f"""<a class="cs-card" href="{{{{root}}}}blog/{art['slug']}/">
          <span class="cs-card-top"><span class="case-id">{escape(art['date'])}</span><span class="chipline">{escape(art['chip'])}</span></span>
          <span class="cs-card-title">{escape(art['title'])}</span>
          <p style="margin-top:.6rem;font-size:.9rem;line-height:1.55;color:var(--muted)">{escape(art['summary'])}</p>
          <span class="cs-card-meta" style="margin-top:auto;padding-top:1rem"><span>{escape(art['read_time'])}</span><span>{escape(art['author'])}</span></span>
          <span class="cs-card-go" aria-hidden="true">→</span>
        </a>"""


def cta_band(title, text, primary=("Write me a brief", "contact/"), secondary=None):
    def href(path):
        return path if path.startswith("{{root}}") or re.match(r"^(?:https?:|mailto:|tel:)", path) else "{{root}}" + path
    sec = f'<a class="btn btn-secondary" href="{href(secondary[1])}">{secondary[0]}</a>' if secondary else ""
    return f"""
    <section class="cta-band">
      <div class="wrap cta-band-in">
        <div>
          <span class="kicker">let's talk</span>
          <h2>{title}</h2>
          <p>{text}</p>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{href(primary[1])}">{primary[0]} <span aria-hidden="true">→</span></a>
          {sec}
        </div>
      </div>
    </section>"""


def page_hero(eyebrow, title, lede, crumbs, aside=""):
    trail = ' <span aria-hidden="true">/</span> '.join(
        f'<a href="{{{{home}}}}{p}">{escape(n)}</a>' if p is not None
        else f'<span aria-current="page">{escape(n)}</span>'
        for n, p in crumbs)
    return f"""    <section class="page-hero">
      <div class="wrap">
        <nav class="crumbs" aria-label="Breadcrumb">{trail}</nav>
        <div class="page-hero-grid">
          <div>
            <span class="eyebrow">{eyebrow}</span>
            <h1>{title}</h1>
            <p class="lede">{lede}</p>
          </div>
          {aside}
        </div>
      </div>
    </section>"""


# ---------- pages ----------

def build_home():
    graph = webpage("", "Bibek Khatiwada SEO Portfolio", [("Home", "")])
    graph[2]["@type"] = "ProfilePage"
    graph[2]["mainEntity"] = person_ref()
    meta = {"path": "", "slug": "home", "og_type": "profile", "graph": graph,
            "title": "Bibek Khatiwada | SEO Strategist, Automation & AI Search",
            "description": "Bibek Khatiwada is an SEO strategist specializing in technical SEO, content systems, automation, AI search visibility, and Search Console-led growth."}
    diff_viewer = fragment("diff-viewer.html")
    calculator = fragment("calculator.html")
    leakage_funnel = fragment("leakage-funnel.html")
    peer_proof = fragment("peer-proof.html")
    body = fragment("home.html", diff_viewer=diff_viewer, calculator=calculator,
                    leakage_funnel=leakage_funnel, peer_proof=peer_proof)
    return write("", page(meta, body, "", ["calculator.js", "llm-interactive.js", "entity-graph.js"]))


def build_about():
    last = len(TIMELINE) - 1
    timeline = "\n".join(
        f"""            <li class="tl-item">
              <button class="tl-btn" type="button" aria-expanded="{'true' if i == last else 'false'}" aria-controls="tl-{i}">
                <span class="tl-year">{escape(year)}</span><span class="tl-role">{escape(role)}</span><span class="tl-plus" aria-hidden="true"></span>
              </button>
              <div class="tl-body" id="tl-{i}"{'' if i == last else ' hidden'}><p>{escape(note)}</p></div>
            </li>""" for i, (year, role, note) in enumerate(TIMELINE))
    achievements = "".join(f'<li><span class="bullet"></span><div><p>{escape(a)}</p></div></li>' for a in ACHIEVEMENTS)
    tools = "".join(f'<span class="skill">{escape(t)}</span>' for t in TOOLS)
    platforms = "".join(f'<span class="skill em">{escape(t)}</span>' for t in PLATFORMS)
    countries = "".join(f'<li>{escape(c)}</li>' for c in COUNTRIES)
    body = page_hero(
        "About Bibek",
        'SEO strategist with a <span class="accent-text">computer-science</span> mindset.',
        "I’m Bibek Khatiwada, based in Kathmandu and working remotely with clients in six countries. "
        "I connect search strategy, technical depth, content systems, and automation—and I explain the reasoning behind every priority.",
        [("Home", ""), ("About", None)],
        aside="""<figure class="hero-portrait">
            <img src="{{root}}assets/bibek-khatiwada-portrait.webp" width="900" height="1080" alt="Bibek Khatiwada overlooking Kathmandu" fetchpriority="high">
            <figcaption>Kathmandu, Nepal</figcaption>
          </figure>""")
    body += fragment("about.html", timeline=timeline, achievements=achievements, tools=tools,
                     platforms=platforms, countries=countries)
    body += cta_band("Want this mindset on your search problem?",
                     "Tell me what you are trying to improve and where it is getting stuck.",
                     secondary=("See the case studies", "{{root}}case-studies/"))
    graph = webpage("about/", "About Bibek Khatiwada", [("Home", ""), ("About", "about/")])
    graph[2]["@type"] = "AboutPage"
    meta = {"path": "about/", "slug": "about", "graph": graph,
            "title": "About Bibek Khatiwada | SEO Strategist in Kathmandu",
            "description": "Bibek Khatiwada's background: BCA-trained SEO strategist, career timeline from SEO Intern to SEO Strategist, leadership, tools, and how he works."}
    return write("about/", page(meta, body, "about", ["about-interactive.js"]))


def build_services():
    toc = "".join(f'<a href="#{s["id"]}"><span>{i + 1:02d}</span>{escape(s["name"])}</a>'
                  for i, s in enumerate(SERVICES))
    panels = []
    for i, s in enumerate(SERVICES):
        items = "".join(f"<li>{escape(x)}</li>" for x in s["includes"])
        related = ""
        if s["cases"]:
            links = "".join(
                f'<a class="mini-case" href="{{{{root}}}}case-studies/{BY_N[n]["slug"]}/"><b>Case {n}</b>{escape(BY_N[n]["short"])}</a>'
                for n in s["cases"])
            related = f'<div class="svc-related"><div class="mini-note">Seen in</div>{links}</div>'
        panels.append(f"""
        <article class="svc" id="{s['id']}">
          <div class="svc-head">
            <div class="icon">{i + 1:02d}</div>
            <div>
              <h2>{escape(s['name'])}</h2>
              <p>{escape(s['summary'])}</p>
            </div>
          </div>
          <details class="svc-more"{' open' if i < 3 else ''}>
            <summary>What’s included</summary>
            <ul class="svc-list">{items}</ul>
            {related}
          </details>
        </article>""")
    body = page_hero(
        "Services",
        'Everything a search program needs, <span class="accent-text">under one strategist</span>.',
        "I can own the strategy, coordinate the execution, build the supporting systems, and report the outcome—from the first audit to sustained growth.",
        [("Home", ""), ("Services", None)],
        aside=f'<nav class="svc-toc" aria-label="Services on this page">{toc}</nav>')
    body += f"""
    <section class="svc-section">
      <div class="wrap svc-grid">{''.join(panels)}
      </div>
    </section>
"""
    body += fragment("services-scope.html")
    body += fragment("process.html")
    body += fragment("services-faq.html",
                     platforms=", ".join(PLATFORMS[:-1]) + ", and custom CMS environments",
                     countries=", ".join(COUNTRIES[:-1]) + ", and " + COUNTRIES[-1])
    body += cta_band("Not sure which service you need?",
                     "Describe the symptom—traffic drop, new launch, messy site, slow reporting—and I will tell you where I would start.")
    services_ld = [{"@type": "Service", "@id": f"{SITE_URL}/services/#{s['id']}", "name": s["name"],
                    "description": s["summary"], "provider": person_ref(), "areaServed": "Worldwide"}
                   for s in SERVICES]
    graph = webpage("services/", "SEO Services", [("Home", ""), ("Services", "services/")], services_ld)
    meta = {"path": "services/", "slug": "services", "graph": graph,
            "title": "SEO Services: Technical, Content, Automation & AI Search | Bibek Khatiwada",
            "description": "Technical SEO, content architecture, automation, on-page, off-page, reporting, AI search and LLM tracking, local and e-commerce SEO: what each service includes and where it was used."}
    return write("services/", page(meta, body, "services", ["tabs.js", "services-scope.js"]))


def build_process():
    body = page_hero(
        "How I work",
        'From a search problem to a <span class="accent-text">verified production result</span>.',
        "A systems-first engagement connects evidence, decisions, implementation, and measurement. Explore the delivery model, then use the interactive scope builder to see what a sensible first sprint could include.",
        [("Home", ""), ("How I work", None)],
        aside="""<dl class="glance process-glance">
          <div><dt>01</dt><dd>Diagnose</dd></div><div><dt>02</dt><dd>Architect</dd></div>
          <div><dt>03</dt><dd>Implement</dd></div><div><dt>04</dt><dd>Verify</dd></div>
        </dl>""")
    body += fragment("process-page.html")
    body += cta_band("Have a problem that does not fit a neat category?",
                     "Bring the symptom, the evidence you have, and the business constraint. We can shape the right first investigation together.",
                     primary=("Build a project brief", "contact/?topic=strategy"),
                     secondary=("Run the SEO diagnostic", "{{root}}audit/"))
    graph = webpage("process/", "How Bibek Works", [("Home", ""), ("How I work", "process/")])
    meta = {"path": "process/", "slug": "process", "graph": graph,
            "title": "How I Work: SEO Strategy, Delivery & Verification | Bibek Khatiwada",
            "description": "Bibek Khatiwada's systems-first SEO process: diagnose with evidence, architect the solution, implement with the team, and verify the live result."}
    return write("process/", page(meta, body, "process", ["process-planner.js"]))


def explorer_data():
    keys = ("n", "slug", "short", "chip", "tags", "clicks", "clicks_d", "impr", "impr_d", "ctr", "pos", "months")
    return json.dumps([{k: cs[k] for k in keys} | {"yoy": bool(cs.get("yoy"))} for cs in CASE_STUDIES],
                      ensure_ascii=False)


def build_case_index():
    chips = "".join(
        f'<button type="button" class="filter-chip" data-filter="{key}" aria-pressed="{"true" if key == "all" else "false"}">{escape(label)}</button>'
        for key, label in FILTERS)
    cards = "\n        ".join(case_card(cs) for cs in CASE_STUDIES)
    body = page_hero(
        "Case studies",
        'Nine projects. <span class="accent-text">Real Search Console numbers.</span>',
        "Client names are confidential. The verticals, the approach, and every metric are real and taken directly from Google Search Console. Filter by the kind of problem, sort by the number you care about, and compare them side by side.",
        [("Home", ""), ("Case studies", None)],
        aside="""<div class="agg" aria-live="polite">
            <div class="agg-row"><strong data-agg="clicks">22.9M</strong><span>clicks in the studies shown*</span></div>
            <div class="agg-row"><strong data-agg="impr">1.64B</strong><span>impressions in the studies shown*</span></div>
            <div class="agg-row"><strong data-agg="count">9</strong><span>case studies shown</span></div>
            <p class="agg-note">*Sum of the 16-month totals currently shown. The year-over-year education study covers a different window, so it is left out of the sums.</p>
          </div>""")
    body += f"""
    <section class="explorer" id="explorer">
      <div class="wrap">
        <div class="explorer-bar">
          <div class="filter-chips" role="group" aria-label="Filter case studies">{chips}</div>
          <label class="sort">Sort by
            <select id="cs-sort">
              <option value="impact">Most impact</option>
              <option value="clicks">Clicks</option>
              <option value="impr">Impressions</option>
              <option value="ctr">CTR</option>
              <option value="pos">Best average position</option>
              <option value="n">Case number</option>
            </select>
          </label>
        </div>
        <p class="explorer-empty" hidden>No case study matches that filter.</p>
        <div class="cs-grid" id="cs-grid">
        {cards}
        </div>
      </div>
    </section>

    <section class="chart-section" id="compare">
      <div class="wrap">
        <div class="section-head">
          <div class="copy">
            <span class="eyebrow">Compare</span>
            <h2>Scale and efficiency, side by side.</h2>
            <p>Volume shows how much search demand a site captured. Efficiency shows how well it turns impressions into clicks at a given average position. Hover, tap, or focus a mark for the exact figures.</p>
          </div>
        </div>
        <div class="tabs" data-tabs>
          <div class="tab-list" role="tablist" aria-label="Chart view">
            <button type="button" role="tab" id="tab-vol" aria-controls="panel-vol" aria-selected="true">Clicks volume</button>
            <button type="button" role="tab" id="tab-eff" aria-controls="panel-eff" aria-selected="false" tabindex="-1">CTR vs position</button>
          </div>
          <div class="chart-card" role="tabpanel" id="panel-vol" aria-labelledby="tab-vol">
            <div class="chart" id="chart-volume"></div>
            <p class="chart-note">Log scale: each gridline is 10× the one below it, so the largest and smallest projects fit on one chart. Case 06 is a three-month year-over-year comparison, so it is not plotted here.</p>
          </div>
          <div class="chart-card" role="tabpanel" id="panel-eff" aria-labelledby="tab-eff" hidden>
            <div class="chart" id="chart-efficiency"></div>
            <p class="chart-note">Further left is better: position 1 is the top of page one. Higher is a larger share of impressions turned into clicks. Case 06 uses its current-period values.</p>
          </div>
        </div>
      </div>
    </section>
"""
    body += fragment("metrics-glossary.html")
    body += cta_band("Have a site that looks like one of these?",
                     "Recovery, scale, a new launch, or steady growth—tell me which one sounds like yours.")
    body += f'\n    <script type="application/json" id="cs-data">{explorer_data()}</script>'
    items = [{"@type": "ListItem", "position": i + 1, "url": f"{SITE_URL}/case-studies/{cs['slug']}/",
              "name": cs["short"]} for i, cs in enumerate(CASE_STUDIES)]
    graph = webpage("case-studies/", "SEO Case Studies", [("Home", ""), ("Case studies", "case-studies/")],
                    [{"@type": "ItemList", "@id": f"{SITE_URL}/case-studies/#list", "itemListElement": items}])
    graph[2]["@type"] = "CollectionPage"
    meta = {"path": "case-studies/", "slug": "cases", "graph": graph,
            "title": "SEO Case Studies with Search Console Data | Bibek Khatiwada",
            "description": "Nine anonymized SEO case studies (YMYL recovery, programmatic scale, Shopify rendering, SaaS launches and more) with real Search Console clicks, impressions, CTR and position."}
    return write("case-studies/", page(meta, body, "work", ["tabs.js", "case-explorer.js"]))


def metric_block(cs):
    if cs.get("yoy"):
        return f"""<div class="res-grid">
            <div class="res res-hero"><span>Clicks</span><strong data-count>{cs['clicks_delta']}</strong><small>{cs['clicks_d']} vs {cs['clicks_prev_d']}</small>
              <div class="bar-pair" aria-hidden="true"><i style="--w:{21.1 / 36.8 * 100:.1f}%"></i><i style="--w:100%"></i></div></div>
            <div class="res"><span>Impressions</span><strong data-count>{cs['impr_delta']}</strong><small>{cs['impr_d']} vs {cs['impr_prev_d']}</small>
              <div class="bar-pair" aria-hidden="true"><i style="--w:{672 / 1080 * 100:.1f}%"></i><i style="--w:100%"></i></div></div>
            <div class="res"><span>Average CTR</span><strong data-count>{cs['ctr']}%</strong><small>up from {cs['ctr_prev']}%</small></div>
            <div class="res"><span>Average position</span><strong data-count>{cs['pos']:g}</strong><small>improved from {cs['pos_prev']}</small></div>
          </div>
          <p class="res-legend"><i class="lg lg-prev"></i> Same period a year earlier &nbsp; <i class="lg lg-now"></i> Last 3 months</p>"""
    monthly_c = cs["clicks"] / cs["months"]
    monthly_i = cs["impr"] / cs["months"]
    return f"""<div class="res-toggle" role="group" aria-label="Show totals or monthly averages">
            <button type="button" aria-pressed="true" data-mode="total">{cs['window']} total</button>
            <button type="button" aria-pressed="false" data-mode="monthly">Average per month</button>
          </div>
          <div class="res-grid">
            <div class="res res-hero"><span>Clicks</span><strong data-count data-total="{cs['clicks']}" data-monthly="{monthly_c:.0f}">{cs['clicks_d']}</strong><small data-label>Search Console · {cs['window']}</small></div>
            <div class="res"><span>Impressions</span><strong data-count data-total="{cs['impr']}" data-monthly="{monthly_i:.0f}">{cs['impr_d']}</strong><small data-label>Search Console · {cs['window']}</small></div>
            <div class="res"><span>Average CTR</span><strong data-count>{cs['ctr']}%</strong><small>clicks ÷ impressions</small></div>
            <div class="res"><span>Average position</span><strong data-count>{cs['pos']:g}</strong><small>1 = top of page one</small></div>
          </div>
          <p class="res-legend">Monthly average = {cs['window']} total ÷ {cs['months']}. Real months vary; this is arithmetic, not a trend line.</p>"""


def build_case_detail(i, cs):
    prev_cs = CASE_STUDIES[i - 1] if i > 0 else None
    next_cs = CASE_STUDIES[i + 1] if i + 1 < len(CASE_STUDIES) else None
    situation = "".join(f"<p>{escape(p)}</p>" for p in cs["situation"])
    steps = "".join(
        f'<li class="step-item"><span class="step-n">{j + 1:02d}</span><div><h3>{escape(t)}</h3><p>{escape(d)}</p></div></li>'
        for j, (t, d) in enumerate(cs["approach"]))
    disciplines = "".join(f'<span class="skill">{escape(d)}</span>' for d in cs["disciplines"])
    update = ""
    if cs.get("update"):
        update = f'<aside class="callout"><div class="mini-note">Recent update</div><p>{escape(cs["update"])}</p></aside>'
    related = [c for c in CASE_STUDIES if c is not cs and set(c["tags"]) & set(cs["tags"])][:3]
    related += [c for c in CASE_STUDIES if c is not cs and c not in related][:3 - len(related)]
    pager = (f'<a class="pager-prev" href="../{prev_cs["slug"]}/"><span>← Case {prev_cs["n"]}</span>{escape(prev_cs["short"])}</a>'
             if prev_cs else "<span></span>")
    if next_cs:
        pager += f'<a class="pager-next" href="../{next_cs["slug"]}/"><span>Case {next_cs["n"]} →</span>{escape(next_cs["short"])}</a>'
    glance = [("Vertical", cs["vertical"]), ("Site", cs["site"]), ("Window", cs["window"]),
              ("Source", "Google Search Console")]
    glance_html = "".join(f"<div><dt>{k}</dt><dd>{escape(v)}</dd></div>" for k, v in glance)
    body = '    <div class="progress" aria-hidden="true"><i></i></div>\n'
    body += page_hero(f"Case {cs['n']} · {escape(cs['chip'])}", escape(cs["title"]), escape(cs["situation"][0]),
                      [("Home", ""), ("Case studies", "case-studies/"), (f"Case {cs['n']}", None)],
                      aside=f'<dl class="glance">{glance_html}</dl>')
    body += f"""
    <section class="cs-body">
      <div class="wrap cs-layout">
        <article class="cs-main">
          <h2 id="results">Results</h2>
          {metric_block(cs)}

          <h2 id="situation">The situation</h2>
          {situation}

          <h2 id="approach">What I did</h2>
          <ol class="steps">{steps}</ol>
          {update}

          {"<h2 id='technical-diff'>Before &amp; After Technical Architecture</h2><div class='diff-grid'><div class='diff-card diff-before'><div class='diff-head'><span class='badge badge-error'>BEFORE</span> Scaled Duplicate URLs &amp; Risk</div><ul><li>20,000 duplicate URLs creating scaled-content-abuse risk across core updates</li><li>Fragmented query targeting causing internal keyword cannibalization</li><li>Crawl budget waste on untracked zero-click parameter pages</li></ul></div><div class='diff-card diff-after'><div class='diff-head'><span class='badge badge-success'>AFTER</span> Topic Hubs &amp; Consolidation</div><ul><li>Consolidated blog-to-category taxonomy &amp; Pregnancy Questions Center hub</li><li>301 directory consolidation protecting overall domain threshold value</li><li>Machine-readable llms.txt &amp; schema grounding for AI search readiness</li></ul></div></div>" if cs['n'] == "01" else ""}
          {"<h2 id='technical-diff'>Before &amp; After Technical Architecture</h2><div class='diff-grid'><div class='diff-card diff-before'><div class='diff-head'><span class='badge badge-error'>BEFORE</span> Client-Side JavaScript Bottlenecks</div><ul><li>Client-side JavaScript rendering delaying Googlebot indexation</li><li>Crawl budget exhausted on non-revenue parameter &amp; tag URLs</li><li>Unstructured product attribute schemas causing Merchant Center disconnects</li></ul></div><div class='diff-card diff-after'><div class='diff-head'><span class='badge badge-success'>AFTER</span> SSR &amp; Collection Controls</div><ul><li>Server-Side Rendering (SSR) checks &amp; pre-rendered collection templates</li><li>Strict canonicalization, robots.txt disallows, &amp; dynamic URL pruning</li><li>Dynamic schema integration matching Google Merchant Center feeds</li></ul></div></div>" if cs['n'] == "03" else ""}

          <h2 id="stepper">Forensic Implementation Stepper</h2>
          <div class="stepper-wrap">
            <div class="stepper-tabs" role="tablist" aria-label="Forensic phases">
              <button type="button" class="stepper-tab active" data-phase="1" role="tab" aria-selected="true"><span>01</span> Diagnosis</button>
              <button type="button" class="stepper-tab" data-phase="2" role="tab" aria-selected="false"><span>02</span> Pruning</button>
              <button type="button" class="stepper-tab" data-phase="3" role="tab" aria-selected="false"><span>03</span> Architecture</button>
              <button type="button" class="stepper-tab" data-phase="4" role="tab" aria-selected="false"><span>04</span> Verification</button>
            </div>
            <div class="stepper-content">
              <div class="stepper-panel" data-phase="1">
                <div class="mini-note">Phase 1: Forensic Drop &amp; Crawl Diagnosis</div>
                <h4>Correlating Losses to Google Updates &amp; Server Logs</h4>
                <p>Isolating whether search visibility drops resulted from site-wide algorithmic quality reassessment, template-level duplicate risks, or server-level crawl bottlenecks.</p>
                <div class="stepper-badge">Tools: GSC API Anomaly Engine, Screaming Frog, Log Analyzers</div>
              </div>
              <div class="stepper-panel" data-phase="2" hidden>
                <div class="mini-note">Phase 2: Thin &amp; Duplicate Content Pruning</div>
                <h4>Consolidating Low-Threshold URLs to Restore Crawl Equity</h4>
                <p>Pruning low-value parameter URLs, dynamic facets, or thin pages to protect the domain's holistic quality threshold value and prevent cannibalization.</p>
                <div class="stepper-badge">Technique: 301 Consolidated Hubs, Robots Disallows, Canonicalization</div>
              </div>
              <div class="stepper-panel" data-phase="3" hidden>
                <div class="mini-note">Phase 3: Topic Hubs &amp; Semantic Schema</div>
                <h4>Restructuring Taxonomies with Entity-Attribute-Value Models</h4>
                <p>Building structured category-to-pillar information architecture and deploying JSON-LD schema graphs to clearly delineate entity relationships.</p>
                <div class="stepper-badge">Outcome: Distinct entity triples recognized by Knowledge Graph</div>
              </div>
              <div class="stepper-panel" data-phase="4" hidden>
                <div class="mini-note">Phase 4: Search Console Recovery &amp; AI Readiness</div>
                <h4>Validating Metric Trajectory &amp; Deploying llms.txt</h4>
                <p>Tracking weekly impression and CTR recovery in Search Console while standardizing /llms.txt for retrieval in AI Overviews and answer engines.</p>
                <div class="stepper-badge">Final Metric: {cs['clicks_d']} Clicks · {cs['impr_d']} Impressions</div>
              </div>
            </div>
          </div>

          <h2 id="disciplines">Disciplines involved</h2>
          <div class="skill-cloud">{disciplines}</div>

          <aside class="callout callout-quiet">
            <div class="mini-note">About these numbers</div>
            <p>Client name withheld for confidentiality. Every figure is taken directly from Google Search Console for the stated window. The Search Console view behind them is not published here.</p>
          </aside>
        </article>
        <aside class="cs-side">
          <nav class="toc" aria-label="On this page">
            <div class="mini-note">On this page</div>
            <a href="#results">Results</a><a href="#situation">The situation</a><a href="#approach">What I did</a><a href="#stepper">Forensic Stepper</a><a href="#disciplines">Disciplines</a>
          </nav>
          <a class="btn btn-primary side-cta" href="{{{{root}}}}contact/?topic=case-{cs['n']}">Discuss a similar project</a>
        </aside>
      </div>
    </section>

    <section class="related">
      <div class="wrap">
        <nav class="pager" aria-label="Case study navigation">{pager}</nav>
        <div class="section-head" style="margin-top:2.5rem"><div class="copy"><span class="eyebrow">Related work</span><h2>Similar problems, different sites.</h2></div>
          <a class="btn btn-secondary" href="{{{{root}}}}case-studies/">All case studies</a></div>
        <div class="cs-grid">{''.join(case_card(c) for c in related)}</div>
      </div>
    </section>"""
    body += cta_band("Facing something similar?", "Tell me about your site and what you are seeing in Search Console.",
                     primary=("Discuss a similar project", f"contact/?topic=case-{cs['n']}"))
    path = f"case-studies/{cs['slug']}/"
    article = {"@type": "Article", "@id": f"{SITE_URL}/{path}#article", "headline": cs["title"],
               "description": cs["situation"][0], "author": person_ref(), "publisher": person_ref(),
               "mainEntityOfPage": {"@id": f"{SITE_URL}/{path}#webpage"}, "inLanguage": "en",
               "image": f"{SITE_URL}/assets/bibek-khatiwada-profile.webp",
               "about": [{"@type": "Thing", "name": d} for d in cs["disciplines"][:4]]}
    graph = webpage(path, cs["title"], [("Home", ""), ("Case studies", "case-studies/"), (cs["short"], path)],
                    [article])
    if cs.get("yoy"):
        desc = (f"{cs['short']}: clicks {cs['clicks_delta']} ({cs['clicks_d']} vs {cs['clicks_prev_d']}), "
                f"impressions {cs['impr_delta']}, average position {cs['pos']:g} from {cs['pos_prev']}.")
    else:
        desc = (f"{cs['short']}: {cs['clicks_d']} clicks and {cs['impr_d']} impressions in {cs['window']} "
                f"({cs['ctr']}% CTR, average position {cs['pos']:g}). The situation, what I did, and the results.")
    meta = {"path": path, "slug": "case", "graph": graph, "og_type": "article",
            "title": f"Case {cs['n']}: {cs['short']} | Bibek Khatiwada", "description": desc}
    return write(path, page(meta, body, "work", ["case-detail.js", "case-stepper.js"]))


def build_tools():
    cards = []
    for t in TOOLS_SHOWCASE:
        stack = "".join(f'<span class="skill">{escape(s)}</span>' for s in t["tech_stack"])
        feats = "".join(f'<li>{escape(f)}</li>' for f in t["features"])
        cards.append(f"""
        <article class="tool-card">
          <div class="tool-head">
            <span class="chipline">{escape(t['chip'])}</span>
            <h2>{escape(t['name'])}</h2>
            <p>{escape(t['summary'])}</p>
          </div>
          <div class="tool-body">
            <div class="mini-note">Technologies</div>
            <div class="skill-cloud">{stack}</div>
            <div class="mini-note" style="margin-top:1rem">Key Capabilities</div>
            <ul class="svc-list">{feats}</ul>
            <div class="tool-actions">
              <a class="btn btn-secondary" href="{t['github']}" target="_blank" rel="noreferrer">GitHub Repo →</a>
            </div>
          </div>
        </article>""")
    cards_html = "\n".join(cards)
    body = page_hero(
        "Tools Showcase",
        'Open-Source &amp; Custom <span class="accent-text">SEO Systems Showcase</span>.',
        "Give tangible form to the Computer Science &amp; Automation Engineer identity. Explore Python NLP scripts, n8n automated workflow pipelines, and custom static generators.",
        [("Home", ""), ("Tools", None)])
    body += fragment("tools.html", tools_cards=cards_html)
    body += cta_band("Need a custom SEO automation tool or crawler?",
                     "Tell me your manual reporting or auditing bottleneck and I will build an automated workflow.")
    graph = webpage("tools/", "SEO Tools Showcase", [("Home", ""), ("Tools", "tools/")])
    meta = {"path": "tools/", "slug": "tools", "graph": graph,
            "title": "Open-Source & Custom SEO Tools | Bibek Khatiwada",
            "description": "Custom SEO automation tools built by Bibek Khatiwada: spaCy semantic flow checker, n8n GSC anomaly detector, and automated llms.txt generator."}
    return write("tools/", page(meta, body, "tools", ["tools-sandbox.js"]))


def build_audit():
    body = page_hero(
        "Audit Diagnostic",
        'Qualifying <span class="accent-text">3-Step SEO Diagnostic</span>.',
        "Identify crawl waste, Google update visibility drops, or zero-click AI Overview leaks. Compile your diagnostic brief in 3 minutes.",
        [("Home", ""), ("Audit", None)])
    body += fragment("audit-intake.html")
    body += cta_band("Prefer a direct conversation?", "Send an email or message on WhatsApp for immediate strategy discussion.",
                     primary=("Chat on WhatsApp", PERSON["whatsapp"]))
    graph = webpage("audit/", "Qualifying SEO Audit Diagnostic", [("Home", ""), ("Audit", "audit/")])
    meta = {"path": "audit/", "slug": "audit", "graph": graph,
            "title": "3-Step SEO Diagnostic Audit | Bibek Khatiwada",
            "description": "Get a qualifying 3-step diagnostic audit for your website. Isolate algorithm drops, AI Overview traffic leaks, and crawl budget issues."}
    return write("audit/", page(meta, body, "audit", ["audit.js"]))


def build_frameworks():
    cards = []
    for f in FRAMEWORKS:
        tags = "".join(f'<span class="skill">{escape(t)}</span>' for t in f["tags"])
        cards.append(f"""
        <article class="cs-card fw-card" data-title="{escape(f['title'])}" data-tags="{','.join(f['tags'])}" data-chip="{escape(f['chip'])}">
          <span class="cs-card-top"><span class="chipline">{escape(f['chip'])}</span><span class="tiny">{escape(f['read_time'])}</span></span>
          <a class="cs-card-title" href="{{{{root}}}}frameworks/{f['slug']}/">{escape(f['title'])}</a>
          <p class="tiny" style="color:var(--text-muted);margin-top:.5rem">{escape(f['summary'])}</p>
          <div class="skill-cloud" style="margin-top:1rem">{tags}</div>
          <a class="cs-card-go" href="{{{{root}}}}frameworks/{f['slug']}/" aria-label="Read framework">Read article →</a>
        </article>""")
    cards_html = "\n".join(cards)
    body = page_hero(
        "Technical Frameworks",
        'Search Mechanics &amp; <span class="accent-text">Technical Playbooks</span>.',
        "In-depth technical essays on Entity-Attribute-Value (EAV) modeling, Generative Engine Optimization (GEO), and algorithm recovery mechanics.",
        [("Home", ""), ("Frameworks", None)])
    body += fragment("framework-index.html", framework_cards=cards_html)
    body += cta_band("Have a complex search architecture question?",
                     "Discuss entity modeling, LLM retrieval readiness, or taxonomy structuring.")
    graph = webpage("frameworks/", "Technical Frameworks Hub", [("Home", ""), ("Frameworks", "frameworks/")])
    meta = {"path": "frameworks/", "slug": "frameworks", "graph": graph,
            "title": "Technical SEO Frameworks & AI Search Playbooks | Bibek Khatiwada",
            "description": "Technical essays by Bibek Khatiwada: Entity-Attribute-Value search modeling, AEO/GEO engineering, and 130k-page YMYL recovery mechanics."}
    return write("frameworks/", page(meta, body, "frameworks", ["framework-filter.js"]))



def build_framework_detail(f):
    takeaways = "".join(f'<li>{escape(t)}</li>' for t in f["takeaways"])
    disciplines = "".join(f'<span class="skill">{escape(d)}</span>' for d in f["disciplines"])
    framework_bodies = {
        "llm-tracking": """
    <h2 id="overview">What an LLM visibility system must measure</h2>
    <p>Rank tracking observes a stable results page. Generative answers vary by prompt wording, model, location, retrieval set, and time. A useful tracker therefore stores the prompt, engine, answer, citations, brand mentions, answer position, and run timestamp—not only a screenshot.</p>
    <h2 id="technical-mechanics">A repeatable evaluation loop</h2>
    <ol><li>Define a prompt matrix across informational, comparative, diagnostic, and entity-validation intent.</li><li>Run prompts with controlled settings and record the raw response.</li><li>Extract cited domains, brand mentions, surrounding claims, and token distance.</li><li>Compare citation share of voice and answer inclusion over repeated runs.</li><li>Connect changes back to pages, passages, schema, and third-party corroboration.</li></ol>
    <h2 id="execution-code">Minimum event schema</h2>
    <div class="sandbox-card"><div class="sandbox-header"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span><span class="sandbox-title">llm_observation.json</span></div><pre class="sandbox-code"><code>{
  "prompt_id": "commercial-01",
  "engine": "answer-engine",
  "brand_mentioned": true,
  "cited_urls": ["https://example.com/guide"],
  "claim_context": "recommended for technical teams",
  "observed_at": "2026-10-03T00:00:00Z"
}</code></pre></div>
    <h2 id="takeaways">How to interpret movement</h2><p>A single answer is anecdotal. Direction becomes useful only when the same prompt set, extraction rules, and scoring method are repeated. Report model changes and sampling limits beside the trend.</p>""",
        "entity-attribute-value-search": """
    <h2 id="overview">Use EAV as a planning model, not keyword decoration</h2>
    <p>An Entity–Attribute–Value model forces a page to state what thing it covers, which property is being discussed, and which value answers the question. It is useful for defining page scope, spotting missing attributes, and preventing two URLs from competing for the same semantic job.</p>
    <h2 id="technical-mechanics">From entity inventory to page architecture</h2>
    <ol><li>Name the central entity and the search task the page must satisfy.</li><li>List attributes that are relevant, contextual, and expected by the audience.</li><li>Separate values that belong on the same page from those that deserve distinct page roles.</li><li>Express stable relationships in visible copy and matching structured data.</li><li>Use internal links to connect parent entities, subtypes, comparisons, and evidence.</li></ol>
    <h2 id="execution-code">Example triple set</h2>
    <div class="sandbox-card"><div class="sandbox-header"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span><span class="sandbox-title">page_scope.json</span></div><pre class="sandbox-code"><code>[
  {"entity":"SEO audit","attribute":"input","value":"crawl + GSC data"},
  {"entity":"SEO audit","attribute":"output","value":"prioritized findings"},
  {"entity":"SEO audit","attribute":"verification","value":"live change check"}
]</code></pre></div>
    <h2 id="takeaways">The boundary that matters</h2><p>Schema cannot rescue vague content. The visible page, internal-link context, metadata, and JSON-LD should describe the same entity and the same role.</p>""",
        "aeo-geo-playbook": """
    <h2 id="overview">Design passages that can survive extraction</h2>
    <p>Answer engines retrieve passages, compare sources, and synthesize a response. A page must still earn ordinary crawlability and relevance, but its most useful claims also need to remain clear when removed from the surrounding design.</p>
    <h2 id="technical-mechanics">The extraction-ready page pattern</h2>
    <ul><li><b>Answer first:</b> state the definition, comparison, number, or recommendation before adding explanation.</li><li><b>Keep the subject explicit:</b> avoid paragraphs full of pronouns whose meaning disappears outside the page.</li><li><b>Separate evidence from opinion:</b> attach dates, units, methods, and primary sources to factual claims.</li><li><b>Ground the entity:</b> keep author, organization, product, and topical schema consistent with visible content.</li><li><b>Make discovery easy:</b> use canonical URLs, stable HTML, internal links, sitemaps, and optional machine-readable summaries.</li></ul>
    <h2 id="execution-code">A compact answer block</h2>
    <div class="sandbox-card"><div class="sandbox-header"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span><span class="sandbox-title">answer-span.html</span></div><pre class="sandbox-code"><code>&lt;h2&gt;What is citation share of voice?&lt;/h2&gt;
&lt;p&gt;Citation share of voice is the percentage of tracked AI answers
that cite a brand or domain for a defined prompt set and time window.&lt;/p&gt;</code></pre></div>
    <h2 id="takeaways">Optimize the evidence chain</h2><p>There is no guaranteed citation switch. Improve the odds by making the claim easy to retrieve, easy to understand, and easy to verify against consistent first- and third-party evidence.</p>""",
        "130k-page-ymyl-recovery-mechanics": """
    <h2 id="overview">Large-site recovery starts with segmentation</h2>
    <p>A 130,000-page health platform cannot be diagnosed through a handful of example URLs. Recovery work begins by segmenting performance, crawl behavior, indexation, templates, directories, intent, and change dates so the loss can be located instead of averaged away.</p>
    <h2 id="technical-mechanics">The recovery sequence</h2>
    <ol><li>Overlay traffic and visibility changes with algorithm, release, hosting, and template events.</li><li>Inventory URLs by directory, template, status, canonical target, clicks, impressions, and last crawl.</li><li>Separate valuable historical URLs from duplicates, thin variants, and dead inventory.</li><li>Repair taxonomy and consolidation rules before expanding content.</li><li>Test changes on bounded cohorts, then monitor crawl, indexation, queries, and unintended loss.</li></ol>
    <h2 id="execution-code">A decision table before redirects</h2>
    <div class="sandbox-card"><div class="sandbox-header"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span><span class="sandbox-title">url_decisions.csv</span></div><pre class="sandbox-code"><code>url,history,intent,target,action,verification
/old-question,valuable,duplicate,/topic-hub,301,target indexed
/thin-variant,none,redundant,,410,removed from index
/core-guide,growing,unique,,keep,queries stable</code></pre></div>
    <h2 id="takeaways">Protect the site while simplifying it</h2><p>Pruning is not a volume target. Each merge, redirect, removal, and template rule needs a reason, a destination where relevant, and a post-release check. In YMYL, editorial trust and medical accuracy remain separate workstreams from technical consolidation.</p>""",
    }
    body_prose = framework_bodies[f["slug"]]

    # Inject interactive framework widget
    if f["slug"] == "llm-tracking":
        body_prose += """
        <div class="interactive-widget-box" id="widget-csov" style="margin:2.5rem 0;padding:1.75rem;background:var(--surface);border:1px solid var(--line);border-radius:18px;">
          <div class="widget-header">
            <span class="eyebrow">Interactive Calculation Model</span>
            <h3 style="margin-top:0.35rem">Citation Share of Voice (C-SoV) Calculator</h3>
            <p class="tiny">Model your brand's AI search visibility across Perplexity, Claude, and ChatGPT Search against two direct competitors.</p>
          </div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(180px, 1fr));gap:1rem;margin-top:1.25rem;">
            <div>
              <label for="csov-prompts" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Evaluated Prompts:</label>
              <input type="number" id="csov-prompts" value="50" min="5" max="500" style="width:100%;padding:0.6rem;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;">
            </div>
            <div>
              <label for="csov-brand" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Your Brand Citations:</label>
              <input type="number" id="csov-brand" value="18" min="0" max="500" style="width:100%;padding:0.6rem;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;">
            </div>
            <div>
              <label for="csov-comp-a" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Competitor A Citations:</label>
              <input type="number" id="csov-comp-a" value="22" min="0" max="500" style="width:100%;padding:0.6rem;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;">
            </div>
            <div>
              <label for="csov-comp-b" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Competitor B Citations:</label>
              <input type="number" id="csov-comp-b" value="14" min="0" max="500" style="width:100%;padding:0.6rem;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;">
            </div>
          </div>
          <div style="margin-top:1.25rem;background:var(--surface-2);border-radius:12px;padding:1.25rem;border:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;">Brand Prompt Citation Rate</div>
              <div style="font-size:1.6rem;font-weight:800;" id="csov-cit-rate">36.0%</div>
            </div>
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;">Citation Share of Voice (C-SoV)</div>
              <div style="font-size:1.6rem;font-weight:800;color:var(--primary);" id="csov-share-rate">33.3%</div>
            </div>
            <div id="csov-verdict">
              <span class="badge" style="background:#f59e0b;color:#1e1b2e;">CONTESTED VISIBILITY</span>
            </div>
          </div>
        </div>
        """
    elif f["slug"] == "entity-attribute-value-search":
        body_prose += """
        <div class="interactive-widget-box" id="widget-eav" style="margin:2.5rem 0;padding:1.75rem;background:var(--surface);border:1px solid var(--line);border-radius:18px;">
          <div class="widget-header">
            <span class="eyebrow">Interactive Builder</span>
            <h3 style="margin-top:0.35rem">Live EAV Knowledge Graph Schema Generator</h3>
            <p class="tiny">Construct verifiable Subject-Predicate-Object triples and generate standard-compliant JSON-LD schema for AI search engines.</p>
          </div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:1rem;margin-top:1.25rem;">
            <div>
              <label for="eav-subject" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Entity Subject (Primary Node):</label>
              <input type="text" id="eav-subject" value="Heat Pump Installation" style="width:100%;padding:0.6rem;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;">
            </div>
            <div>
              <label for="eav-attr1" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Predicate 1 (Property : Value):</label>
              <input type="text" id="eav-attr1" value="efficiencyRating : Up to 24 SEER2" style="width:100%;padding:0.6rem;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;">
            </div>
            <div>
              <label for="eav-attr2" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Predicate 2 (Property : Value):</label>
              <input type="text" id="eav-attr2" value="installationTimeHours : 6 to 10" style="width:100%;padding:0.6rem;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;">
            </div>
          </div>
          <div style="margin-top:1.25rem;background:#1e1b2e;border-radius:12px;padding:1.25rem;border:1px solid rgba(255,255,255,0.1);">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
              <span style="font-size:0.72rem;color:rgba(255,255,255,0.6);font-family:monospace;">PREVIEW: VALIDATED JSON-LD SCHEMA</span>
              <button type="button" id="copy-eav-btn" class="btn btn-outline" style="padding:0.25rem 0.6rem;font-size:0.72rem;color:white;border-color:rgba(255,255,255,0.2);">Copy Schema</button>
            </div>
            <pre id="eav-json-output" style="color:#f8eede;font-family:monospace;font-size:0.82rem;line-height:1.5;margin:0;white-space:pre-wrap;"></pre>
          </div>
        </div>
        """
    elif f["slug"] == "aeo-geo-playbook":
        body_prose += """
        <div class="interactive-widget-box" id="widget-aeo" style="margin:2.5rem 0;padding:1.75rem;background:var(--surface);border:1px solid var(--line);border-radius:18px;">
          <div class="widget-header">
            <span class="eyebrow">AEO Content Validator</span>
            <h3 style="margin-top:0.35rem">40-Word Semantic Answer Chunk Scorer</h3>
            <p class="tiny">Test whether an introductory heading paragraph fulfills LLM retrieval criteria (word count brevity, direct definition structure, zero fluff).</p>
          </div>
          <div style="margin-top:1rem;">
            <textarea id="aeo-text" rows="3" style="width:100%;padding:0.75rem;border-radius:10px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;font-size:0.9rem;">Heat pump efficiency is measured in SEER2 for cooling and HSPF2 for heating. Modern inverter heat pumps achieve up to 24 SEER2, reducing electrical consumption by up to 50% compared to standard baseboard heaters.</textarea>
          </div>
          <div style="margin-top:1rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;background:var(--surface-2);padding:1.25rem;border-radius:12px;border:1px solid var(--line);">
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;">Word Count (Target: 35-50)</div>
              <div style="font-size:1.5rem;font-weight:800;" id="aeo-words">31 words</div>
            </div>
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;">Definition Syntax</div>
              <div style="font-size:1.5rem;font-weight:800;color:var(--primary);" id="aeo-def-detected">Detected ✓</div>
            </div>
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;">RAG Retention Score</div>
              <div style="font-size:1.5rem;font-weight:800;color:#10b981;" id="aeo-score">94% (High)</div>
            </div>
          </div>
        </div>
        """
    elif f["slug"] == "130k-page-ymyl-recovery-mechanics":
        body_prose += """
        <div class="interactive-widget-box" id="widget-prune" style="margin:2.5rem 0;padding:1.75rem;background:var(--surface);border:1px solid var(--line);border-radius:18px;">
          <div class="widget-header">
            <span class="eyebrow">Recovery Simulation</span>
            <h3 style="margin-top:0.35rem">Crawl Budget &amp; Directory 301 Pruning Simulator</h3>
            <p class="tiny">Model how removing thin or cannibalizing URLs accelerates Googlebot re-indexing across your authoritative topic hubs.</p>
          </div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));gap:1rem;margin-top:1.25rem;">
            <div>
              <label style="font-size:0.82rem;font-weight:700;display:block;margin-bottom:0.25rem;">Baseline Indexed Scale:</label>
              <div style="font-size:1.1rem;font-weight:800;">130,000 URLs</div>
              <span style="font-size:0.75rem;color:var(--text-muted);">Historical medical catalog</span>
            </div>
            <div>
              <label for="prune-slider" style="font-size:0.82rem;font-weight:700;display:block;margin-bottom:0.25rem;">Duplicate/Thin URLs Pruned: <span id="prune-count-val" style="color:var(--primary);font-weight:800;">20,000</span></label>
              <input type="range" id="prune-slider" min="0" max="60000" step="2500" value="20000" style="width:100%;">
            </div>
            <div>
              <label for="crawl-slider" style="font-size:0.82rem;font-weight:700;display:block;margin-bottom:0.25rem;">Daily Googlebot Request Budget: <span id="crawl-rate-val" style="color:var(--accent);font-weight:800;">4,500/day</span></label>
              <input type="range" id="crawl-slider" min="1000" max="15000" step="500" value="4500" style="width:100%;">
            </div>
          </div>
          <div style="margin-top:1.25rem;background:var(--surface-2);border-radius:12px;padding:1.25rem;border:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;">Full Catalog Crawl Turnaround</div>
              <div style="font-size:1.5rem;font-weight:800;" id="prune-days-saved">24.4 days <span style="font-size:0.85rem;color:#10b981;font-weight:600;">(4.5 days faster)</span></div>
            </div>
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;">Crawl Waste Eliminated</div>
              <div style="font-size:1.5rem;font-weight:800;color:var(--primary);" id="prune-waste-pct">15.4%</div>
            </div>
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;">Domain Authority Focus</div>
              <div style="font-size:1.5rem;font-weight:800;color:#10b981;">+18.2% Concentration</div>
            </div>
          </div>
        </div>
        """

    body = page_hero(
        f"Framework · {escape(f['chip'])}",
        escape(f["title"]),
        escape(f["summary"]),
        [("Home", ""), ("Frameworks", "frameworks/"), (f["short"], None)])
    body += fragment("framework-detail.html",
                     date=f["date"], read_time=f["read_time"], author=f["author"],
                     takeaways_list=takeaways, body_html=body_prose, disciplines_cloud=disciplines)
    body += cta_band("Want to apply this framework to your site?",
                     "Let's discuss how to structure your domain's entity graph or recover visibility.")
    
    path = f"frameworks/{f['slug']}/"
    article_ld = {"@type": "TechArticle", "@id": f"{SITE_URL}/{path}#article", "headline": f["title"],
                  "description": f["summary"], "author": person_ref(), "publisher": person_ref(),
                  "datePublished": f["date"], "inLanguage": "en"}
    graph = webpage(path, f["title"], [("Home", ""), ("Frameworks", "frameworks/"), (f["short"], path)], [article_ld])
    meta = {"path": path, "slug": "framework", "graph": graph, "og_type": "article",
            "title": f"{f['title']} | Bibek Khatiwada", "description": f["summary"]}
    return write(path, page(meta, body, "frameworks", ["framework-interactive.js"]))



def build_industries():
    cards = []
    for ind in INDUSTRIES_MATRIX:
        niches = "".join(f'<span class="skill">{escape(n)}</span>' for n in ind["niches"])
        pains = "".join(f'<li>{escape(p)}</li>' for p in ind["pain_points"])
        cards.append(f"""
        <article class="tool-card ind-card">
          <div class="tool-head">
            <span class="chipline">{escape(ind['chip'])}</span>
            <h2><a href="{{{{root}}}}industries/{ind['slug']}/">{escape(ind['title'])}</a></h2>
            <p>{escape(ind['summary'])}</p>
          </div>
          <div class="tool-body">
            <div class="mini-note">Key Niches Covered</div>
            <div class="skill-cloud">{niches}</div>
            <div class="mini-note" style="margin-top:1rem">Common Sector Bottlenecks</div>
            <ul class="svc-list">{pains}</ul>
            <div class="tool-actions">
              <a class="btn btn-secondary" href="{{{{root}}}}industries/{ind['slug']}/">View Industry Blueprint →</a>
            </div>
          </div>
        </article>""")
    cards_html = "\n".join(cards)
    body = page_hero(
        "Industry Matrix",
        'Target Industry <span class="accent-text">Search Blueprints</span>.',
        "Tailored search strategies, crawl budget management, and topical authority blueprints across 20+ verified industry verticals.",
        [("Home", ""), ("Industries", None)])
    body += fragment("industry-index.html", industry_cards=cards_html)
    body += cta_band("Don't see your exact vertical?", "I have delivered search campaigns across 20+ industries. Contact me to discuss your specific domain.")
    graph = webpage("industries/", "Industry Search Blueprints", [("Home", ""), ("Industries", "industries/")])
    meta = {"path": "industries/", "slug": "industries", "graph": graph,
            "title": "Industry Search Blueprints: Local, SaaS & Programmatic | Bibek Khatiwada",
            "description": "Tailored SEO strategies across Home Services & Local Trades, B2B SaaS, and Programmatic / E-commerce Marketplaces."}
    return write("industries/", page(meta, body, "industries"))


def build_industry_detail(ind):
    niches = "".join(f'<span class="skill">{escape(n)}</span>' for n in ind["niches"])
    pains = "".join(f'<li><span class="bullet"></span><div><p>{escape(p)}</p></div></li>' for p in ind["pain_points"])
    
    approach = f"""
    <p>{escape(ind['summary'])}</p>
    <p>In this sector, search performance relies on solving specific infrastructure and intent challenges:</p>
    <ul class="svc-list">
      <li><b>Topical Hub Architecture:</b> Grouping service locations or software modules into structured parent hubs.</li>
      <li><b>Technical Hardening:</b> Ensuring crawl budget is spent on high-converting landing pages rather than dynamic parameters.</li>
      <li><b>Entity &amp; Brand Grounding:</b> Aligned schema markup to establish clear domain authority.</li>
    </ul>
    """

    # Inject interactive industry calculator
    if ind["slug"] == "home-services-hvac-plumbing":
        approach += """
        <div class="interactive-widget-box" style="margin:2.5rem 0;padding:1.75rem;background:var(--surface);border:1px solid var(--line);border-radius:18px;">
          <span class="eyebrow">Local Trade Interactive Model</span>
          <h3 style="margin-top:0.35rem">SAB Geo-Radius &amp; Local Pack Authority Model</h3>
          <p class="tiny">Estimate maximum service area radius without triggering Google Local proximity penalties.</p>
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:1rem;margin-top:1.25rem;">
            <div>
              <label for="sab-radius" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Target Service Radius: <span id="sab-radius-val" style="color:var(--primary);font-weight:800;">15 miles</span></label>
              <input type="range" id="sab-radius" min="5" max="45" step="1" value="15" style="width:100%;">
            </div>
            <div>
              <label for="sab-locations" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Secondary Cities / Townships:</label>
              <input type="number" id="sab-locations" value="4" min="1" max="25" style="width:100%;padding:0.6rem;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;">
            </div>
            <div>
              <label for="sab-reviews" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Google Business Reviews:</label>
              <input type="number" id="sab-reviews" value="75" min="5" max="2000" step="5" style="width:100%;padding:0.6rem;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;">
            </div>
          </div>
          <div style="margin-top:1.25rem;background:var(--surface-2);border-radius:12px;padding:1.25rem;border:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;">Local Pack Proximity Index</div>
              <div style="font-size:1.6rem;font-weight:800;" id="sab-pack-score">50/100</div>
            </div>
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;">Required City Landing Pages</div>
              <div style="font-size:1.6rem;font-weight:800;color:var(--primary);" id="sab-pages-needed">12 landing pages</div>
            </div>
            <div id="sab-risk-badge">
              <span class="badge badge-success">OPTIMAL PACK PROXIMITY</span>
            </div>
          </div>
        </div>
        """
    elif ind["slug"] == "b2b-saas":
        approach += """
        <div class="interactive-widget-box" style="margin:2.5rem 0;padding:1.75rem;background:var(--surface);border:1px solid var(--line);border-radius:18px;">
          <span class="eyebrow">Enterprise Valuation Model</span>
          <h3 style="margin-top:0.35rem">SaaS High-Intent Pipeline &amp; CAC Payback Model</h3>
          <p class="tiny">Calculate the enterprise pipeline and Google Ads cost-replacement value created by commercial search intent.</p>
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:1rem;margin-top:1.25rem;">
            <div>
              <label for="saas-acv" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Annual Contract Value (ACV $):</label>
              <input type="number" id="saas-acv" value="18000" min="1000" max="250000" step="1000" style="width:100%;padding:0.6rem;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;">
            </div>
            <div>
              <label for="saas-traffic" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Monthly High-Intent Clicks: <span id="saas-traffic-val" style="color:var(--primary);font-weight:800;">3,500</span></label>
              <input type="range" id="saas-traffic" min="500" max="25000" step="250" value="3500" style="width:100%;">
            </div>
            <div>
              <label for="saas-cvr" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Demo Booking CVR (%):</label>
              <input type="number" id="saas-cvr" value="1.5" min="0.2" max="10.0" step="0.1" style="width:100%;padding:0.6rem;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;">
            </div>
          </div>
          <div style="margin-top:1.25rem;background:var(--surface-2);border-radius:12px;padding:1.25rem;border:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;">Annualized Revenue Pipeline</div>
              <div style="font-size:1.6rem;font-weight:800;color:var(--primary);" id="saas-pipeline">$2,489,400</div>
            </div>
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;">Google Ads Equivalent Value</div>
              <div style="font-size:1.6rem;font-weight:800;" id="saas-ad-equiv">$50,750/mo</div>
            </div>
          </div>
        </div>
        """
    elif ind["slug"] == "programmatic-directories":
        approach += """
        <div class="interactive-widget-box" style="margin:2.5rem 0;padding:1.75rem;background:var(--surface);border:1px solid var(--line);border-radius:18px;">
          <span class="eyebrow">Catalog Diagnostics</span>
          <h3 style="margin-top:0.35rem">Programmatic Thin-Content &amp; De-indexation Risk Scorer</h3>
          <p class="tiny">Test your faceted navigation and catalog template depth against Google soft-404 and spam thresholds.</p>
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:1rem;margin-top:1.25rem;">
            <div>
              <label for="prog-urls" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Dynamic Filter URLs: <span id="prog-urls-val" style="color:var(--primary);font-weight:800;">50,000</span></label>
              <input type="range" id="prog-urls" min="5000" max="250000" step="5000" value="50000" style="width:100%;">
            </div>
            <div>
              <label for="prog-words" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Average Unique Words per Page:</label>
              <input type="number" id="prog-words" value="280" min="30" max="1500" step="10" style="width:100%;padding:0.6rem;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;">
            </div>
            <div>
              <label for="prog-links" style="font-size:0.8rem;font-weight:700;display:block;margin-bottom:0.25rem;">Internal Inbound Links / Node:</label>
              <input type="number" id="prog-links" value="5" min="1" max="50" style="width:100%;padding:0.6rem;border-radius:8px;border:1px solid var(--line);background:var(--surface-2);font-family:inherit;">
            </div>
          </div>
          <div style="margin-top:1.25rem;background:var(--surface-2);border-radius:12px;padding:1.25rem;border:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;">Algorithmic Pruning Risk</div>
              <div style="font-size:1.6rem;font-weight:800;" id="prog-risk-score">45% Risk</div>
            </div>
            <div id="prog-badge">
              <span class="badge" style="background:#f59e0b;color:#1e1b2e;">MODERATE THIN CONTENT DRIFT</span>
            </div>
          </div>
        </div>
        """
    elif ind["slug"] == "healthcare-ymyl":
        approach += """
        <div class="interactive-widget-box" style="margin:2.5rem 0;padding:1.75rem;background:var(--surface);border:1px solid var(--line);border-radius:18px;">
          <span class="eyebrow">Clinical E-E-A-T Auditor</span>
          <h3 style="margin-top:0.35rem">Medical YMYL E-E-A-T Quality Checklist &amp; Scorecard</h3>
          <p class="tiny">Verify whether your clinic or health portal fulfills Google Search Quality Rater Guidelines for medical information.</p>
          <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(240px, 1fr));gap:0.75rem;margin-top:1.25rem;">
            <label style="display:flex;align-items:center;gap:0.6rem;background:var(--surface-2);padding:0.75rem;border-radius:8px;border:1px solid var(--line);cursor:pointer;">
              <input type="checkbox" class="ymyl-check" checked>
              <span style="font-size:0.85rem;">Credentialed MD/DO Author Byline</span>
            </label>
            <label style="display:flex;align-items:center;gap:0.6rem;background:var(--surface-2);padding:0.75rem;border-radius:8px;border:1px solid var(--line);cursor:pointer;">
              <input type="checkbox" class="ymyl-check" checked>
              <span style="font-size:0.85rem;">PubMed / Clinical Trial Citations</span>
            </label>
            <label style="display:flex;align-items:center;gap:0.6rem;background:var(--surface-2);padding:0.75rem;border-radius:8px;border:1px solid var(--line);cursor:pointer;">
              <input type="checkbox" class="ymyl-check" checked>
              <span style="font-size:0.85rem;">Medical Reviewer Timestamp &amp; Policy</span>
            </label>
            <label style="display:flex;align-items:center;gap:0.6rem;background:var(--surface-2);padding:0.75rem;border-radius:8px;border:1px solid var(--line);cursor:pointer;">
              <input type="checkbox" class="ymyl-check">
              <span style="font-size:0.85rem;">Doctor / MedicalOrganization JSON-LD</span>
            </label>
          </div>
          <div style="margin-top:1.25rem;background:var(--surface-2);border-radius:12px;padding:1.25rem;border:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
            <div>
              <div style="font-size:0.72rem;color:var(--text-muted);text-transform:uppercase;">E-E-A-T Quality Score</div>
              <div style="font-size:1.6rem;font-weight:800;" id="ymyl-score">75<span style="font-size:1.1rem;color:var(--text-muted);font-weight:600;">/100</span></div>
            </div>
            <div id="ymyl-badge">
              <span class="badge" style="background:#f59e0b;color:#1e1b2e;">PARTIAL COMPLIANCE (CORE VULNERABLE)</span>
            </div>
          </div>
        </div>
        """

    industry_cases = {
        "home-services-hvac-plumbing": ["05", "06", "08"],
        "b2b-saas": ["07", "08", "06"],
        "programmatic-directories": ["02", "03", "01"],
        "healthcare-ymyl": ["01", "09", "05"],
    }
    rel_cases = "\n".join(case_card(BY_N[n]) for n in industry_cases[ind["slug"]])

    body = page_hero(
        f"Industry Blueprint · {escape(ind['chip'])}",
        escape(ind["title"]),
        escape(ind["summary"]),
        [("Home", ""), ("Industries", "industries/"), (ind["title"], None)])
    body += fragment("industry-detail.html",
                     title=escape(ind["title"]), summary=escape(ind["summary"]), slug=ind["slug"],
                     niches_cloud=niches, pain_points_list=pains, approach_html=approach, related_cases=rel_cases)
    body += cta_band(f"Need a search plan for {escape(ind['title'])}?",
                     "Let's audit your domain structure and design a custom search growth roadmap.",
                     primary=("Get Sector Strategy", f"contact/?industry={ind['slug']}"))
    
    path = f"industries/{ind['slug']}/"
    graph = webpage(path, ind["title"], [("Home", ""), ("Industries", "industries/"), (ind["title"], path)])
    meta = {"path": path, "slug": "industry", "graph": graph,
            "title": f"{ind['title']} Search Blueprint | Bibek Khatiwada", "description": ind["summary"]}
    return write(path, page(meta, body, "industries", ["industry-interactive.js"]))



def build_roi_calculator():
    body = page_hero(
        "Organic Growth Modeling",
        'Interactive SEO <span class="accent-text">ROI &amp; Revenue Forecast</span>.',
        "Model the incremental pipeline, leads, and annual revenue driven by fixing technical crawl bottlenecks, building entity topic hubs, and winning high-intent search real estate.",
        [("Home", ""), ("ROI Calculator", None)])
    body += fragment("roi-calculator.html")
    body += cta_band("Ready to build this pipeline for your domain?",
                     "Send me your site URL and current Search Console numbers. I will prepare a customized forensic strategy roadmap.",
                     primary=("Get Strategic Forecast", "contact/?topic=roi-forecast"))
    graph = webpage("roi-calculator/", "SEO ROI & Revenue Growth Calculator", [("Home", ""), ("ROI Calculator", "roi-calculator/")])
    graph.append({
        "@type": "WebApplication",
        "@id": f"{SITE_URL}/roi-calculator/#app",
        "name": "Bibek Khatiwada SEO ROI Calculator",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "All",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    })
    meta = {"path": "roi-calculator/", "slug": "roi-calc", "graph": graph,
            "title": "Interactive SEO ROI & Revenue Calculator | Bibek Khatiwada",
            "description": "Calculate projected organic clicks, conversions, and annualized revenue pipeline based on search demand, current vs target CTR, and customer lifetime value."}
    return write("roi-calculator/", page(meta, body, "roi", ["roi-calculator.js"]))


def build_glossary():
    terms_cards = []
    for t in GLOSSARY_TERMS:
        rel = ""
        if t.get("related_framework"):
            rel = f'<div class="glossary-meta"><a href="{{{{root}}}}frameworks/{t["related_framework"]}/" class="glossary-link">Read Deep-Dive Framework →</a></div>'
        terms_cards.append(f"""
        <article class="glossary-card" data-term="{escape(t['term'])}" data-cat="{escape(t['category'])}">
          <div class="glossary-head">
            <span class="chipline">{escape(t['category'])}</span>
            <h2 id="{t['slug']}">{escape(t['term'])}</h2>
          </div>
          <p class="glossary-def">{escape(t['definition'])}</p>
          <div class="glossary-details">
            <div class="mini-note">Engineering Context</div>
            <p>{escape(t['details'])}</p>
          </div>
          {rel}
        </article>""")
    terms_html = "\n".join(terms_cards)
    body = page_hero(
        "Search Knowledge Graph",
        'Technical SEO &amp; AI Search <span class="accent-text">Engineering Glossary</span>.',
        "Definitive reference guide covering Entity-Attribute-Value (EAV) modeling, Generative Engine Optimization (GEO), RAG chunking, and modern search engine mechanics.",
        [("Home", ""), ("Glossary", None)])
    body += fragment("glossary.html", terms_html=terms_html, total_terms=str(len(GLOSSARY_TERMS)))
    body += cta_band("Need an advanced search architecture audit?",
                     "Let's evaluate your website's entity schema, crawl efficiency, and AI search readiness.")
    
    defined_terms = [{
        "@type": "DefinedTerm",
        "name": t["term"],
        "description": t["definition"],
        "inDefinedTermSet": f"{SITE_URL}/glossary/#termset"
    } for t in GLOSSARY_TERMS]
    
    graph = webpage("glossary/", "Technical SEO & AI Search Glossary", [("Home", ""), ("Glossary", "glossary/")], [
        {
            "@type": "DefinedTermSet",
            "@id": f"{SITE_URL}/glossary/#termset",
            "name": "Modern Technical SEO & Generative Search Engineering Glossary",
            "hasDefinedTerm": defined_terms
        }
    ])
    meta = {"path": "glossary/", "slug": "glossary", "graph": graph,
            "title": "Technical SEO & AI Search Glossary | Bibek Khatiwada",
            "description": "Comprehensive reference glossary of technical SEO, AEO, GEO, and entity architecture concepts by Bibek Khatiwada."}
    return write("glossary/", page(meta, body, "glossary", ["glossary.js"]))



def build_blog():
    published = [art for art in ARTICLES if (SRC / "content" / f"{art['slug']}.html").exists()]
    cards = "\n        ".join(article_card(art) for art in published)
    body = page_hero(
        "Blog & Frameworks",
        'Engineering perspectives on <span class="accent-text">modern search & AI visibility</span>.',
        "Technical writeups on entity modeling, LLM tracking, prompt evaluation matrices, and search systems from real client projects and experiments.",
        [("Home", ""), ("Blog", None)],
        aside="""<div class="agg" aria-live="polite">
            <div class="agg-row"><strong>AI & Systems</strong><span>Core focus</span></div>
            <div class="agg-row"><strong>Deterministic</strong><span>Test methods</span></div>
            <div class="agg-row"><strong>Verified</strong><span>Code & data</span></div>
          </div>""")
    body += f"""
    <section class="explorer" id="blog-grid">
      <div class="wrap">
        <div class="section-head" style="margin-bottom:1.5rem">
          <div class="copy">
            <span class="eyebrow">Articles</span>
            <h2>Systems, research & frameworks</h2>
          </div>
        </div>
        <div class="cs-grid">
        {cards}
        </div>
      </div>
    </section>
"""
    body += cta_band("Have a complex search or AI-visibility challenge?",
                     "From LLM brand tracking to corpus-level technical recoveries, let's look at the data.")
    items = [{"@type": "ListItem", "position": i + 1, "url": f"{SITE_URL}/blog/{art['slug']}/",
              "name": art["title"]} for i, art in enumerate(published)]
    graph = webpage("blog/", "Blog & Technical Frameworks", [("Home", ""), ("Blog", "blog/")],
                    [{"@type": "ItemList", "@id": f"{SITE_URL}/blog/#list", "itemListElement": items}])
    graph[2]["@type"] = "CollectionPage"
    meta = {"path": "blog/", "slug": "blog", "graph": graph,
            "title": "Blog & SEO Engineering Frameworks | Bibek Khatiwada",
            "description": "Technical insights on LLM tracking, AEO, GEO, entity architecture, and search systems by SEO strategist Bibek Khatiwada."}
    return write("blog/", page(meta, body, "blog"))


def build_article_detail(i, art):
    published = [item for item in ARTICLES if (SRC / "content" / f"{item['slug']}.html").exists()]
    prev_art = published[i - 1] if i > 0 else None
    next_art = published[i + 1] if i + 1 < len(published) else None
    disciplines = "".join(f'<span class="skill">{escape(d)}</span>' for d in art["disciplines"])
    if prev_art:
        pager = f'<a class="pager-prev" href="../{prev_art["slug"]}/"><span>← Previous</span>{escape(prev_art["short"])}</a>'
    else:
        pager = "<span></span>"
    if next_art:
        pager += f'<a class="pager-next" href="../{next_art["slug"]}/"><span>Next →</span>{escape(next_art["short"])}</a>'
    glance = [("Topic", art["chip"]), ("Date", art["date"]), ("Read time", art["read_time"]),
              ("Author", art["author"])]
    glance_html = "".join(f"<div><dt>{k}</dt><dd>{escape(v)}</dd></div>" for k, v in glance)

    article_content = fragment(f"{art['slug']}.html")

    body = '    <div class="progress" aria-hidden="true"><i></i></div>\n'
    body += page_hero(f"{escape(art['chip'])} · {escape(art['date'])}", escape(art["title"]), escape(art["summary"]),
                      [("Home", ""), ("Blog", "blog/"), (art["short"], None)],
                      aside=f'<dl class="glance">{glance_html}</dl>')
    body += f"""
    <section class="cs-body">
      <div class="wrap cs-layout">
        <article class="cs-main">
          {article_content}

          <h2 id="disciplines">Disciplines & Topics</h2>
          <div class="skill-cloud">{disciplines}</div>

          <aside class="callout callout-quiet" style="margin-top:2.5rem">
            <div class="mini-note">Author</div>
            <p>Written by <strong>Bibek Khatiwada</strong>, an SEO strategist based in Kathmandu specializing in entity-based SEO, crawl architecture, automation, and AI search visibility.</p>
          </aside>
        </article>
        <aside class="cs-side">
          <nav class="toc" aria-label="On this page">
            <div class="mini-note">Contents</div>
            <a href="#paradigm-shift">The Paradigm Shift</a>
            <a href="#what-is-llm-tracking">What is LLM Tracking?</a>
            <a href="#tracking-metrics">Core Tracking Metrics</a>
            <a href="#interactive-simulator">Citation Calculator</a>
            <a href="#proof-benchmarks">Empirical Proof & GSC Data</a>
            <a href="#diff-visualizer">SERP vs. AIO vs. LLM</a>
            <a href="#prompt-matrix">Interactive Prompt Matrix</a>
            <a href="#pipeline-architecture">Pipeline Architecture</a>
            <a href="#failure-modes">Why Sites Get Dropped</a>
            <a href="#optimization-blueprint">Optimization Blueprint</a>
            <a href="#reconciling-gsc">Search Console & RAG</a>
          </nav>
          <a class="btn btn-primary side-cta" href="{{{{root}}}}contact/?topic=llm-tracking">Consult on AI Search</a>
        </aside>
      </div>
    </section>

    <section class="related">
      <div class="wrap">
        <nav class="pager" aria-label="Article navigation">{pager}</nav>
      </div>
    </section>"""
    body += cta_band("Want to build LLM tracking into your search stack?",
                     "Let's evaluate how your brand currently appears in Google AI Overviews and ChatGPT Search.",
                     primary=("Get in touch", "contact/?topic=ai-search"))
    path = f"blog/{art['slug']}/"
    article_schema = {
        "@type": "BlogPosting",
        "@id": f"{SITE_URL}/{path}#article",
        "headline": art["title"],
        "description": art["summary"],
        "datePublished": art["date"],
        "dateModified": art["date"],
        "author": person_ref(),
        "publisher": person_ref(),
        "mainEntityOfPage": {"@id": f"{SITE_URL}/{path}#webpage"},
        "inLanguage": "en",
        "image": f"{SITE_URL}/assets/bibek-khatiwada-profile.webp",
        "keywords": ", ".join(art["disciplines"]),
        "about": [{"@type": "Thing", "name": d} for d in art["disciplines"][:4]]
    }
    graph = webpage(path, art["title"], [("Home", ""), ("Blog", "blog/"), (art["short"], path)],
                    [article_schema])
    meta = {"path": path, "slug": "article", "graph": graph, "og_type": "article",
            "title": f"{art['title']} | Bibek Khatiwada", "description": art["summary"]}
    return write(path, page(meta, body, "blog", ["case-detail.js", "tabs.js", "llm-interactive.js"]))


def build_contact():
    cases = "".join(f'<option value="case-{cs["n"]}">A project like Case {cs["n"]} ({escape(cs["chip"])})</option>'
                    for cs in CASE_STUDIES)
    services = "".join(f'<option value="{s["id"]}">{escape(s["name"])}</option>' for s in SERVICES)
    body = page_hero(
        "Contact",
        'Bring me the SEO problem. <span class="accent-text">I’ll help shape the plan.</span>',
        "Email, WhatsApp, or the short brief builder below—whichever is easiest. The more context you share about the site and the goal, the more useful my first reply will be.",
        [("Home", ""), ("Contact", None)],
        aside="""<div class="clock" data-clock>
            <div class="mini-note">Local time in Kathmandu</div>
            <strong data-clock-time>--:--</strong>
            <span>Nepal Time · UTC+5:45</span>
            <small data-clock-yours></small>
          </div>""")
    body += fragment("contact.html", service_options=services, case_options=cases, email=PERSON["email"],
                     phone=PERSON["phone_display"], phone_href=PERSON["phone_href"], whatsapp=PERSON["whatsapp"],
                     linkedin=PERSON["linkedin"], linkedin_display=PERSON["linkedin_display"],
                     github=PERSON["github"], github_display=PERSON["github_display"],
                     google=PERSON["google_profile"])
    graph = webpage("contact/", "Contact Bibek Khatiwada", [("Home", ""), ("Contact", "contact/")])
    graph[2]["@type"] = "ContactPage"
    meta = {"path": "contact/", "slug": "contact", "graph": graph,
            "title": "Contact Bibek Khatiwada | SEO Strategist",
            "description": "Contact Bibek Khatiwada by email, WhatsApp, phone or LinkedIn, or build a short project brief. Based in Kathmandu, open to remote work."}
    return write("contact/", page(meta, body, "contact", ["contact.js"]))


def build_privacy():
    body = page_hero("Privacy", "Privacy notice", "What this website does, and does not do, with your data.",
                     [("Home", ""), ("Privacy", None)])
    body += fragment("privacy.html", email=PERSON["email"], updated=TODAY)
    graph = webpage("privacy/", "Privacy notice", [("Home", ""), ("Privacy", "privacy/")])
    meta = {"path": "privacy/", "slug": "privacy", "graph": graph,
            "title": "Privacy Notice | Bibek Khatiwada",
            "description": "Privacy notice for bibek-khatiwada.com.np: no cookies, no analytics, no database, and how contact messages are handled."}
    return write("privacy/", page(meta, body))


def build_404():
    body = page_hero("404", "This page doesn’t exist.",
                     "The link may be old: this site was rebuilt in 2026. Try one of these instead.",
                     [("Home", ""), ("Not found", None)])
    body += """
    <section><div class="wrap cs-grid">
      <a class="cs-card" href="/"><span class="cs-card-title">Home</span><span class="cs-card-go" aria-hidden="true">→</span></a>
      <a class="cs-card" href="/case-studies/"><span class="cs-card-title">Case studies</span><span class="cs-card-go" aria-hidden="true">→</span></a>
      <a class="cs-card" href="/services/"><span class="cs-card-title">Services</span><span class="cs-card-go" aria-hidden="true">→</span></a>
      <a class="cs-card" href="/contact/"><span class="cs-card-title">Contact</span><span class="cs-card-go" aria-hidden="true">→</span></a>
    </div></section>"""
    meta = {"path": "404.html", "slug": "notfound", "noindex": True, "absolute_root": True, "graph": [],
            "title": "Page not found | Bibek Khatiwada", "description": "This page does not exist."}
    (OUT / "404.html").write_text(page(meta, body))


def build_sitemap(paths):
    urls = "\n".join(f"  <url>\n    <loc>{SITE_URL}/{p}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>"
                     for p in paths)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')


def build_llms_txt():
    cases = "\n".join(
        f"- [{cs['short']}]({SITE_URL}/case-studies/{cs['slug']}/): "
        + (f"clicks {cs['clicks_delta']} year over year ({cs['clicks_d']} vs {cs['clicks_prev_d']})" if cs.get("yoy")
           else f"{cs['clicks_d']} clicks, {cs['impr_d']} impressions, {cs['ctr']}% CTR, average position {cs['pos']:g} over {cs['window']}")
        for cs in CASE_STUDIES)
    services = "\n".join(f"- [{s['name']}]({SITE_URL}/services/#{s['id']}): {s['summary']}" for s in SERVICES)
    frameworks = "\n".join(
        f"- [{fw['title']}]({SITE_URL}/frameworks/{fw['slug']}/): {fw['summary']}"
        for fw in FRAMEWORKS)
    tools = "\n".join(
        f"- [{t['name']}]({SITE_URL}/tools/): {t['summary']}"
        for t in TOOLS_SHOWCASE)
    industries = "\n".join(
        f"- [{ind['title']}]({SITE_URL}/industries/{ind['slug']}/): {ind['summary']}"
        for ind in INDUSTRIES_MATRIX)

    (OUT / "llms.txt").write_text(f"""# Bibek Khatiwada, SEO Strategist

> Kathmandu-based SEO strategist, open to remote work, specializing in entity-based and semantic SEO, technical SEO, content systems, SEO automation, and AI search visibility (AEO, GEO, llms.txt). 3+ years of experience with clients in {len(COUNTRIES)} countries: {", ".join(COUNTRIES)}.

Case-study figures are Google Search Console data. Client names are confidential.

## Pages
- [Home]({SITE_URL}/): overview, services, process, and selected case studies
- [About]({SITE_URL}/about/): background, career timeline, education (BCA, Tribhuvan University), tools
- [Services]({SITE_URL}/services/): what each service includes
- [Case studies]({SITE_URL}/case-studies/): all nine studies with filters and comparison charts
- [Tools Showcase]({SITE_URL}/tools/): custom & open-source Python, n8n, and llms.txt tools
- [Audit Diagnostic]({SITE_URL}/audit/): 3-step qualifying diagnostic form
- [Technical Frameworks]({SITE_URL}/frameworks/): EAV modeling, AEO/GEO engineering, and YMYL recovery mechanics
- [Industry Matrix]({SITE_URL}/industries/): local trades, B2B SaaS, and programmatic inventory blueprints
- [Contact]({SITE_URL}/contact/): {PERSON['email']}, WhatsApp {PERSON['phone_display']}

## Technical Frameworks
{frameworks}

## Tools Showcase
{tools}

## Industry Blueprints
{industries}

## Case studies
{cases}

## Services
{services}

## Profiles
- LinkedIn: {PERSON['linkedin']}
- GitHub: {PERSON['github']}
""")


def main():
    published_articles = [art for art in ARTICLES if (SRC / "content" / f"{art['slug']}.html").exists()]
    paths = [build_home(), build_about(), build_services(), build_process(), build_case_index(), build_blog()]
    paths += [build_case_detail(i, cs) for i, cs in enumerate(CASE_STUDIES)]
    paths += [build_article_detail(i, art) for i, art in enumerate(published_articles)]
    paths += [build_tools(), build_audit(), build_frameworks()]
    paths += [build_framework_detail(f) for f in FRAMEWORKS]
    paths += [build_industries()]
    paths += [build_industry_detail(ind) for ind in INDUSTRIES_MATRIX]
    paths += [build_roi_calculator(), build_glossary()]
    paths += [build_contact(), build_privacy()]
    build_404()
    build_sitemap(paths)
    build_llms_txt()
    print(f"Built {len(paths)} pages + 404, sitemap.xml, llms.txt into {OUT}")


if __name__ == "__main__":
    main()
