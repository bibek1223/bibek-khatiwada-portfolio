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
                  INDUSTRIES_MATRIX, PERSON, PLATFORMS, SERVICES, SITE_URL,
                  TIMELINE, TOOLS, TOOLS_SHOWCASE)
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
    return f"""<a class="cs-card" href="{{{{root}}}}case-studies/{cs['slug']}/" data-n="{cs['n']}">
          <span class="cs-card-top"><span class="case-id">Case {cs['n']}</span><span class="chipline">{escape(cs['chip'])}</span></span>
          <span class="cs-card-title">{escape(cs['card'])}</span>
          <span class="cs-card-metric">{headline}</span>
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
    sec = f'<a class="btn btn-secondary" href="{secondary[1]}">{secondary[0]}</a>' if secondary else ""
    return f"""
    <section class="cta-band">
      <div class="wrap cta-band-in">
        <div>
          <span class="kicker">let's talk</span>
          <h2>{title}</h2>
          <p>{text}</p>
        </div>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{{{{root}}}}{primary[1]}">{primary[0]} <span aria-hidden="true">→</span></a>
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
    body = fragment("home.html") + fragment("calculator.html") + fragment("leakage-funnel.html")
    return write("", page(meta, body, "", ["calculator.js"]))


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
    return write("about/", page(meta, body, "about"))


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
    return write("services/", page(meta, body, "services", ["tabs.js"]))


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
            <a href="#results">Results</a><a href="#situation">The situation</a><a href="#approach">What I did</a><a href="#disciplines">Disciplines</a>
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
    return write(path, page(meta, body, "work", ["case-detail.js"]))


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
    return write("tools/", page(meta, body, "tools"))


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
        <article class="cs-card fw-card">
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
    return write("frameworks/", page(meta, body, "frameworks"))


def build_framework_detail(f):
    takeaways = "".join(f'<li>{escape(t)}</li>' for t in f["takeaways"])
    disciplines = "".join(f'<span class="skill">{escape(d)}</span>' for d in f["disciplines"])
    
    body_prose = f"""
    <h2 id="overview">Overview &amp; Core Concept</h2>
    <p>{escape(f['summary'])}</p>
    <p>Modern search engines like Google and AI answer engines (ChatGPT, Perplexity) evaluate web content not as isolated keywords, but as interconnected entity nodes inside a structured knowledge graph.</p>

    <h2 id="technical-mechanics">Technical Mechanics</h2>
    <p>To ensure content is properly extracted, indexed, and cited, search engineering must align with machine-readable representations.</p>
    <ul>
      <li><b>Structured Entity Grounding:</b> Explicit schema.org JSON-LD definitions connecting Subject, Predicate, and Object triples.</li>
      <li><b>Machine-Readable Endpoints:</b> Deploying <code>/llms.txt</code> files that expose canonical markdown links for AI web crawlers.</li>
      <li><b>Crawl &amp; Rendering Hygiene:</b> Consolidating thin or redundant URLs to maintain high domain threshold values.</li>
    </ul>

    <h2 id="execution-code">Implementation &amp; Code Example</h2>
    <div class="sandbox-card">
      <div class="sandbox-header">
        <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
        <span class="sandbox-title">eav_triple_generator.py</span>
      </div>
      <pre class="sandbox-code"><code><span class="comment"># Entity-Attribute-Value (EAV) Knowledge Graph Triple Structurer</span>
eav_triplets = [
    {{"subject": "{escape(f['title'])}", "predicate": "hasCategory", "object": "{escape(f['chip'])}"}},
    {{"subject": "{escape(f['title'])}", "predicate": "author", "object": "Bibek Khatiwada"}},
    {{"subject": "{escape(f['title'])}", "predicate": "targetEngine", "object": "Google Knowledge Graph & LLM Retrieval"}}
]
<span class="fn">print</span>(eav_triplets)</code></pre>
    </div>

    <h2 id="takeaways">Summary &amp; Strategic Value</h2>
    <p>By shifting from legacy keyword targeting to structured entity modeling, brands build defensible search authority that survives Google core updates and excels in AI answer engines.</p>
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
    return write(path, page(meta, body, "frameworks"))


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

    rel_cases = "\n".join(case_card(cs) for cs in CASE_STUDIES[:3])

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
    return write(path, page(meta, body, "industries"))


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
    prev_art = ARTICLES[i - 1] if i > 0 else None
    next_art = ARTICLES[i + 1] if i + 1 < len(ARTICLES) else None
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
    paths = [build_home(), build_about(), build_services(), build_case_index(), build_blog()]
    paths += [build_case_detail(i, cs) for i, cs in enumerate(CASE_STUDIES)]
    paths += [build_article_detail(i, art) for i, art in enumerate(published_articles)]
    paths += [build_tools(), build_audit(), build_frameworks()]
    paths += [build_framework_detail(f) for f in FRAMEWORKS]
    paths += [build_industries()]
    paths += [build_industry_detail(ind) for ind in INDUSTRIES_MATRIX]
    paths += [build_contact(), build_privacy()]
    build_404()
    build_sitemap(paths)
    build_llms_txt()
    print(f"Built {len(paths)} pages + 404, sitemap.xml, llms.txt into {OUT}")


if __name__ == "__main__":
    main()

