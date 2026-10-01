"""Single source of truth for every fact the site publishes.

Every value here is traced to a source document. Do not add a figure that is not
in one of these:
  - research/Bibek_Khatiwada_SEO_Portfolio.docx  (case studies, verified against
    the embedded Search Console screenshots on 2026-08-23)
  - research/Bibek_Khatiwada_Resume.docx
  - design/index.html as deployed on 2026-09-15 (Bibek's own published copy)

Figures deliberately NOT published (open contradictions, see PROJECT-LOG.md):
"150+ niches", "millions of monthly visits", "millions in revenue", "five years".
"""

SITE_URL = "https://bibek-khatiwada.com.np"

PERSON = {
    "name": "Bibek Khatiwada",
    "role": "SEO Strategist",
    "tagline": "Entity-based, Semantic & AI Search Optimization",
    "email": "bibekkhatiwada2@gmail.com",
    "phone_display": "+977 986 041 1440",
    "phone_href": "+9779860411440",
    "whatsapp": "https://wa.me/9779860411440",
    "linkedin": "https://www.linkedin.com/in/bibek-khatiwada-a907171a2/",
    "linkedin_display": "linkedin.com/in/bibek-khatiwada-a907171a2",
    "github": "https://github.com/bibek1223",
    "github_display": "github.com/bibek1223",
    "google_profile": "https://share.google/fTFCFVuIAGYnnfhLR",
    "location": "Kathmandu, Nepal",
}

# Fields: n (display id), slug, short (card title), title (page H1), vertical,
# tags (explorer filters), window, clicks/impressions as raw numbers for charts,
# display strings exactly as they appear in the source document.
CASE_STUDIES = [
    {
        "n": "01", "slug": "medical-ymyl-recovery",
        "chip": "Health / YMYL recovery",
        "short": "Medical / YMYL health platform — recovery at scale",
        "title": "Recovering a 130,000-page medical platform after a multi-update drop",
        "card": "Recovered a large medical platform after a multi-update visibility drop.",
        "vertical": "Health / YMYL", "site": "Medical health platform, roughly 130,000 pages",
        "tags": ["recovery", "technical", "health"],
        "window": "16 months", "months": 16,
        "clicks": 21_200_000, "clicks_d": "21.2M",
        "impr": 1_470_000_000, "impr_d": "1.47B",
        "ctr": 1.4, "pos": 7.3,
        "situation": [
            "A large medical (YMYL) health platform of roughly 130,000 pages had lost visibility across several Google updates.",
            "In a Your-Money-or-Your-Life niche, quality and trust signals are judged more strictly, so the recovery had to address the whole site rather than a handful of pages.",
        ],
        "approach": [
            ("Diagnosed the drop by update", "Traced the losses to specific Google core and spam updates instead of treating the decline as one event."),
            ("Isolated scaled-content risk", "Identified about 20,000 duplicate pages that created scaled-content-abuse risk."),
            ("Flagged infrastructure failures", "Surfaced host and crawl-budget failures that limited how much of the site Google could process."),
            ("Built the recovery plan", "Action items across all pages, recovery of previously high-value URLs, and content gap and expansion analysis."),
            ("Restructured the taxonomy", "Moved to a blog-to-category taxonomy and built a Pregnancy Questions Center as a structured topic hub."),
            ("Audited rendering and prepared for AI search", "Ran Screaming Frog, Googlebot rendering, and Search Console audits, and prepared llms.txt for AI crawlers."),
        ],
        "update": "A large-scale 301 consolidation was recently executed across a directory, part of a deliberate query-and-page consolidation strategy responding to today's zero-click SERP environment and protecting the site's threshold value. It produced a minor, expected dip that is already recovering.",
        "disciplines": ["Algorithm diagnosis", "Technical SEO", "Crawl budget", "Content consolidation", "Information architecture", "llms.txt"],
    },
    {
        "n": "02", "slug": "programmatic-vehicle-scrapping",
        "chip": "Programmatic architecture",
        "short": "UK vehicle-scrapping service — programmatic at scale",
        "title": "Scaling a UK vehicle-scrapping service with programmatic pages that stay useful",
        "card": "Scaled a UK vehicle-scrapping service without letting pages go thin.",
        "vertical": "Automotive services (UK)", "site": "UK vehicle-scrapping service with a large programmatic page architecture",
        "tags": ["technical", "programmatic"],
        "window": "16 months", "months": 16,
        "clicks": 1_120_000, "clicks_d": "1.12M",
        "impr": 117_000_000, "impr_d": "117M",
        "ctr": 1.0, "pos": 14.8,
        "situation": [
            "A UK vehicle-scrapping service relied on a large programmatic page architecture, where templates generate pages at scale.",
            "At that scale the template itself becomes part of the ranking strategy: weak templates multiply into thousands of thin pages.",
        ],
        "approach": [
            ("Audit before action", "Opened with an initial audit, a master analysis, and a site-drop technical analysis, then a prioritized action plan."),
            ("Manufacturer pages at scale", "Built manufacturer landing pages at scale from content outlines and finalized their FAQs."),
            ("Market expansion research", "Researched expansion into scrap yards, car breakers, and the Ireland market."),
            ("Technical hardening", "Optimized robots.txt, Core Web Vitals, schema, and staging-domain linking."),
            ("Link profile cleanup", "Cleaned toxic backlinks and ran outreach."),
        ],
        "disciplines": ["Programmatic SEO", "Template design", "Technical SEO", "Market research", "Backlink audit", "Outreach"],
    },
    {
        "n": "03", "slug": "shopify-rendering-crawl-budget",
        "chip": "Shopify / e-commerce",
        "short": "Shopify e-commerce — rendering & crawl budget",
        "title": "Fixing crawl waste and rendering on a JavaScript-heavy Shopify store",
        "card": "Fixed crawl waste and rendering issues on a JavaScript-heavy Shopify store.",
        "vertical": "E-commerce", "site": "Large JavaScript-rendered Shopify store",
        "tags": ["technical", "ecommerce"],
        "window": "16 months", "months": 16,
        "clicks": 449_000, "clicks_d": "449K",
        "impr": 40_800_000, "impr_d": "40.8M",
        "ctr": 1.1, "pos": 8.2,
        "situation": [
            "A large Shopify store rendered much of its content with JavaScript and generated a large inventory of dynamic URLs.",
            "Crawl budget was being spent on URLs that did not earn revenue, while collection and product pages needed to be understood clearly by search systems.",
        ],
        "approach": [
            ("Business and entity analysis", "Ran a domain-wide business and entity analysis, an initial technical audit, and collection-page keyword research."),
            ("Collection inventory", "Optimized the collection inventory and mapped product attributes."),
            ("Pages from a controlled template", "Generated collection pages in bulk from a controlled template, and built author and brand-authority pages."),
            ("Rendering analysis", "Ran Googlebot rendering and server-side rendering (SSR) analysis."),
            ("Crawl-budget rules", "Fixed a large dynamic URL inventory through crawl-budget rules, canonicalization, redirects, and pruning."),
            ("Structured data and feeds", "Aligned dynamic schema with Google Merchant Center."),
        ],
        "disciplines": ["E-commerce SEO", "JavaScript rendering", "Crawl budget", "Canonicalization", "Schema", "Merchant Center"],
    },
    {
        "n": "04", "slug": "recovery-stability-at-scale",
        "chip": "Recovery and stability",
        "short": "Recovery and stability at scale",
        "title": "Stabilizing a large site and building a stronger growth baseline",
        "card": "I stabilized a large site and created a stronger growth baseline.",
        "vertical": "Large site", "site": "Large site requiring recovery and sustained stability",
        "tags": ["recovery"],
        "window": "16 months", "months": 16,
        "clicks": 60_400, "clicks_d": "60.4K",
        "impr": 8_870_000, "impr_d": "8.87M",
        "ctr": 0.7, "pos": 12.8,
        "situation": [
            "A large site needed to recover lost performance and then hold it, rather than chase a short-term spike.",
        ],
        "approach": [
            ("Stabilize first", "Stabilized performance before pushing for growth."),
            ("Lift output", "Combined technical cleanup, content improvements, and ongoing measurement to lift output."),
            ("Step-change", "Produced a clear step-change in early 2026."),
        ],
        "disciplines": ["Recovery", "Technical cleanup", "Content improvement", "Measurement"],
    },
    {
        "n": "05", "slug": "broad-core-update-recovery",
        "chip": "Google broad core recovery",
        "short": "Algorithm recovery — Google broad core update",
        "title": "Rebuilding organic performance after a Google broad core update",
        "card": "I rebuilt organic performance after a broad core update.",
        "vertical": "Algorithm recovery", "site": "Site impacted by a Google broad core update",
        "tags": ["recovery"],
        "window": "16 months", "months": 16,
        "clicks": 29_000, "clicks_d": "29K",
        "impr": 2_690_000, "impr_d": "2.69M",
        "ctr": 1.1, "pos": 9.7,
        "situation": [
            "The site lost rankings and clicks after a Google broad core update.",
            "Broad core updates reassess overall quality, so recovery is a quality and systems problem, not a single-page fix.",
        ],
        "approach": [
            ("Diagnose", "Diagnosed the drop."),
            ("Rebuild quality", "Rebuilt content quality and technical health."),
            ("Restore and grow", "Restored and then grew rankings."),
        ],
        "disciplines": ["Algorithm recovery", "Content quality", "Technical health"],
    },
    {
        "n": "06", "slug": "education-yoy-growth",
        "chip": "Education platform",
        "short": "Education platform — year-over-year growth",
        "title": "Sustaining year-over-year growth for an education platform",
        "card": "I sustained year-over-year growth through content and technical improvements.",
        "vertical": "Education", "site": "Education platform",
        "tags": ["growth"],
        "window": "Last 3 months vs the same period a year earlier", "months": None,
        "yoy": True,
        "clicks": 36_800, "clicks_d": "36.8K", "clicks_prev_d": "21.1K", "clicks_delta": "+74%",
        "impr": 1_080_000, "impr_d": "1.08M", "impr_prev_d": "672K", "impr_delta": "+61%",
        "ctr": 3.4, "ctr_prev": 3.1, "pos": 9.0, "pos_prev": 13.3,
        "situation": [
            "An established education platform needed growth that would hold across a full year, not a one-off spike.",
        ],
        "approach": [
            ("Consistent content strategy", "Maintained a sustained content strategy across the full year."),
            ("Technical improvement cycle", "Ran continuous technical improvements alongside the content work."),
            ("Data-led priorities", "Used performance data to prioritize the next opportunities."),
        ],
        "disciplines": ["Content strategy", "Technical SEO", "Performance analysis"],
    },
    {
        "n": "07", "slug": "saas-fast-ramp",
        "chip": "New SaaS platform",
        "short": "New SaaS platform — fast ramp, strong positions",
        "title": "Ramping a new SaaS platform into strong organic positions",
        "card": "I ramped a new SaaS platform into strong organic positions.",
        "vertical": "SaaS", "site": "New SaaS project from a standing start",
        "tags": ["newsite", "saas"],
        "window": "16 months", "months": 16,
        "clicks": 20_900, "clicks_d": "20.9K",
        "impr": 859_000, "impr_d": "859K",
        "ctr": 2.4, "pos": 6.9,
        "situation": [
            "A new SaaS project started from zero organic visibility.",
        ],
        "approach": [
            ("Entity-based foundation", "Used entity-based SEO to establish what the product is and how it relates to its topic."),
            ("Focused on-page work", "Applied focused on-page optimization to earn a rapid ramp into strong positions."),
        ],
        "disciplines": ["Entity-based SEO", "On-page SEO", "New-site launch"],
    },
    {
        "n": "08", "slug": "saas-organic-from-launch",
        "chip": "SaaS from launch",
        "short": "New SaaS platform — organic growth from launch",
        "title": "Building organic visibility into a new SaaS website from launch",
        "card": "I built organic visibility into a new SaaS website from launch.",
        "vertical": "SaaS", "site": "New SaaS website built for organic visibility from launch",
        "tags": ["newsite", "saas"],
        "window": "16 months", "months": 16,
        "clicks": 14_000, "clicks_d": "14K",
        "impr": 301_000, "impr_d": "301K",
        "ctr": 4.7, "pos": 7.6,
        "situation": [
            "A new SaaS website was built with organic search as a launch channel rather than an afterthought.",
        ],
        "approach": [
            ("Entity-based SEO", "Defined the product's entities and relationships from day one."),
            ("Topical authority build", "Planned and built topical coverage around the product's subject area."),
            ("Aligned foundations", "Aligned the on-page and technical foundation with search intent."),
        ],
        "disciplines": ["Entity-based SEO", "Topical authority", "Technical SEO", "New-site launch"],
    },
    {
        "n": "09", "slug": "medical-research-topical-authority",
        "chip": "Medical research platform",
        "short": "Medical research platform — topical authority",
        "title": "Building topical authority for a specialized medical research platform",
        "card": "I built topical authority for a specialized medical research platform.",
        "vertical": "Health / YMYL", "site": "New research-based medical platform in a specialized niche",
        "tags": ["newsite", "health"],
        "window": "16 months", "months": 16,
        "clicks": 7_700, "clicks_d": "7.7K",
        "impr": 136_000, "impr_d": "136K",
        "ctr": 5.6, "pos": 15.5,
        "situation": [
            "A new, research-based medical platform needed to earn trust in a specialized, YMYL niche.",
        ],
        "approach": [
            ("Topical authority", "Built topical authority for specialized medical queries."),
            ("On-page optimization", "Optimized pages for the intent behind those queries."),
            ("Trustworthy structure", "Structured the content to be clear and trustworthy for readers and search systems."),
        ],
        "disciplines": ["Topical authority", "On-page SEO", "YMYL content", "New-site launch"],
    },
]

FILTERS = [
    ("all", "All work"),
    ("recovery", "Recovery"),
    ("technical", "Technical & scale"),
    ("newsite", "New site launch"),
    ("growth", "Year-over-year growth"),
    ("health", "Health / YMYL"),
    ("saas", "SaaS"),
    ("ecommerce", "E-commerce"),
    ("programmatic", "Programmatic"),
]

# Service copy: summaries from the deployed homepage; "includes" lists from the
# resume's Areas of Expertise. `cases` links to case studies that show the work.
SERVICES = [
    {
        "id": "technical-seo", "name": "Technical SEO",
        "summary": "Fix crawl, indexation, rendering, structure, and speed issues across simple sites and huge inventories.",
        "includes": ["Crawlability and indexation", "XML sitemaps and robots.txt", "Canonical and redirect strategy",
                     "Core Web Vitals and page-speed optimization", "Site architecture", "JavaScript rendering checks",
                     "HTTPS, HTML and CSS", "Schema and structured data"],
        "cases": ["01", "03", "02"],
    },
    {
        "id": "content-architecture", "name": "Content Architecture",
        "summary": "Design topical maps and pillar-cluster systems so content earns authority instead of competing with itself.",
        "includes": ["Entity-based and semantic SEO", "Topical authority architecture", "Topical maps",
                     "Pillar and cluster strategy", "Search-intent modeling", "Entity-attribute-value (EAV) modeling",
                     "TF-IDF and n-gram expansion", "Internal linking and page consolidation"],
        "cases": ["09", "08", "01"],
    },
    {
        "id": "automation", "name": "Automation & Custom Tools",
        "summary": "Turn repetitive SEO work into reliable workflows, scripts, dashboards, and internal tools that scale delivery.",
        "includes": ["n8n automated workflows", "Python and Google Colab notebooks", "Google Apps Script on Sheets",
                     "Custom WordPress plugins and browser extensions", "LLM and custom-GPT workflows",
                     "Custom SEO tools backed by a proprietary database"],
        "cases": [],
    },
    {
        "id": "on-page-seo", "name": "On-page SEO",
        "summary": "Titles, metadata, headers, internal links, URLs, schema, and search-intent alignment.",
        "includes": ["Search-intent-driven optimization", "Titles, metadata, headers and alt text", "Internal linking",
                     "URL structure", "Location landing pages", "Large-scale content audits"],
        "cases": ["07", "09"],
    },
    {
        "id": "off-page-seo", "name": "Off-page & Authority",
        "summary": "Build trust beyond the page through white-hat links, digital PR, citations, and brand signals.",
        "includes": ["White-hat link building", "Digital PR", "Guest posting", "Broken-link building",
                     "Citation and directory building", "Brand and entity signals", "Backlink audits and toxic-link disavow"],
        "cases": ["02"],
    },
    {
        "id": "content-writing", "name": "Content Writing",
        "summary": "Write useful, intent-led content that is clear for readers and extractable for search systems.",
        "includes": ["SEO briefs", "Content writing and copywriting", "Pillar and cluster content",
                     "Answer-first content", "E-E-A-T restructuring"],
        "cases": ["06", "09"],
    },
    {
        "id": "reporting", "name": "Reporting & Analytics",
        "summary": "Make performance visible through dashboards, KPI systems, and decision-ready reporting.",
        "includes": ["Automated Looker Studio dashboards", "GA4 and Search Console analysis", "KPI and rank tracking",
                     "Google Tag Manager and conversion tracking", "Microsoft Clarity", "Weekly and monthly reporting"],
        "cases": ["06"],
    },
    {
        "id": "ai-search", "name": "AI Search & LLM Tracking",
        "summary": "Monitor how brands appear across AI answers while improving their semantic and structured-data foundations.",
        "includes": ["Answer Engine Optimization (AEO)", "Generative AI visibility (GEO)", "llms.txt for AI-crawler readiness",
                     "Knowledge-graph optimization", "schema.org structured data", "LLM prompt and answer tracking"],
        "cases": ["01"],
    },
    {
        "id": "local-ecommerce", "name": "Local & E-commerce SEO",
        "summary": "Grow local and commerce properties through GBP, location pages, collections, products, and Merchant Center.",
        "includes": ["Google Business Profile optimization", "Local citations and NAP consistency", "Review strategy",
                     "Service-area and multi-location optimization", "Shopify product and collection SEO",
                     "Rich snippets and Merchant Center"],
        "cases": ["03"],
    },
]

TOOLS = ["Google Search Console", "Google Analytics (GA4)", "Google Tag Manager", "Looker Studio", "Screaming Frog",
         "Ahrefs", "Semrush", "Microsoft Clarity", "PageSpeed Insights", "n8n", "Google Apps Script",
         "Google Colab", "Python", "LLM APIs", "ClickUp", "Zoho", "Slack"]

PLATFORMS = ["WordPress", "Shopify", "Wix", "BigCommerce", "Squarespace", "Webflow", "Custom CMS"]

COUNTRIES = ["United States", "United Kingdom", "Canada", "Australia", "Ireland", "South Africa"]

# Timeline as published on the live homepage (2026-09-15).
TIMELINE = [
    ("2021", "SEO Intern", "Built the foundation in on-page SEO, keyword research, and client delivery."),
    ("2022", "SEO Executive", "Expanded into off-page SEO, technical audits, and independent campaign management."),
    ("2023", "SEO Specialist", "Moved deeper into data analysis, entity-based SEO, and repeatable workflows."),
    ("2024 — now", "RankMeTop · Team Lead → SEO Strategist",
     "Progressed into end-to-end strategy across 150+ projects, 100+ niches, six countries, and a 50+ member team."),
]

# Resume "Selected achievements" that carry no open contradiction.
ACHIEVEMENTS = [
    "Handled 60+ client accounts concurrently without loss of delivery quality.",
    "Managed a 50+ member team operating concurrently across SEO, design, and development.",
    "Led a recovery campaign that restored a site hit by a Google broad core algorithm update.",
    "Reinstated a suspended Google Business Profile.",
    "Set up and verified a Google Business Profile for a business with no physical storefront.",
]
