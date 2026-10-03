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
    ("all", "All (9)"),
    ("recovery", "Algorithmic Recovery (3)"),
    ("programmatic", "Programmatic SEO"),
    ("ecommerce", "E-Commerce & Crawl"),
    ("saas", "High-Growth SaaS (2)"),
    ("health", "Healthcare / YMYL (2)"),
    ("technical", "Technical & Scale (3)"),
]

# Service copy: summaries from the deployed homepage; "includes" lists from the
# resume's Areas of Expertise. `cases` links to case studies that show the work.
SERVICES = [
    {
        "id": "entity-architecture", "name": "Entity-Based Architecture & Topical Maps",
        "summary": "Design semantic topical maps and pillar-cluster systems so content earns authority instead of competing with itself. Knowledge graph triples, EAV modeling, and internal linking networks.",
        "includes": ["Entity-based & semantic SEO", "Topical authority architecture", "Topical maps & cluster strategy",
                     "Entity-Attribute-Value (EAV) modeling", "Search-intent alignment", "Internal linking & directory consolidation",
                     "Wikidata & Google Knowledge Graph alignment", "Content decay & cannibalization resolution"],
        "cases": ["09", "08", "01"],
    },
    {
        "id": "technical-infrastructure", "name": "Technical Infrastructure & Crawl Forensics",
        "summary": "Fix crawl waste, JavaScript rendering bottlenecks, indexation bloat, and URL architecture across sites scaling to hundreds of thousands of pages.",
        "includes": ["Crawlability & log-file forensics", "JavaScript rendering & SSR verification", "XML sitemaps & robots.txt directives",
                     "Canonicalization & redirect chain resolution", "Core Web Vitals & critical rendering path",
                     "Schema.org structured data graphs", "Scaled parameter & facet pruning", "E-commerce collection architecture"],
        "cases": ["01", "03", "02"],
    },
    {
        "id": "aeo-geo-search", "name": "AEO, GEO & Generative Engine Visibility",
        "summary": "Engineer web content for extraction and citation in Google AI Overviews, Perplexity, and ChatGPT with structured answer spans, entity grounding, and machine-readable endpoints.",
        "includes": ["Answer Engine Optimization (AEO)", "Generative Engine Optimization (GEO)", "llms.txt standard implementation",
                     "Knowledge Graph entity grounding", "LLM prompt matrix & C-SoV tracking", "RAG semantic chunking & extraction testing",
                     "Brand citation share measurement", "Structured entity attribution schema"],
        "cases": ["01"],
    },
    {
        "id": "algorithm-recovery", "name": "Algorithmic Core Update Remediation",
        "summary": "Systematic forensic recovery from Google broad core updates, helpful content penalties, and quality reassessments through site-wide quality re-architecting and taxonomy cleanup.",
        "includes": ["Core update loss diagnosis by timestamp", "Scaled content risk isolation & pruning", "Taxonomy & category restructuring",
                     "E-E-A-T trust signal reinforcement", "Backlink profile audit & toxic link disavow", "301 consolidation protecting domain threshold value"],
        "cases": ["01", "05", "04"],
    },
    {
        "id": "automation-tools", "name": "Custom SEO Automation & Internal Tools",
        "summary": "Turn repetitive SEO bottlenecks into reliable automated workflows, Python scripts, Google Search Console anomaly detectors, and custom data pipelines.",
        "includes": ["n8n automated workflow pipelines", "Python & Google Colab analysis scripts", "Search Console API anomaly detection",
                     "Google Apps Script automation on Sheets", "spaCy & sentence-transformers NLP pipelines",
                     "Custom WordPress plugins & browser extensions", "Automated Looker Studio KPI reporting"],
        "cases": [],
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

# Technical Frameworks & Essays (Phase E Content Engine)
FRAMEWORKS = [
    {
        "slug": "llm-tracking",
        "title": "LLM Tracking: How to Monitor Brand Visibility, Citations, and Retrieval in AI Search",
        "short": "LLM Tracking: Brand Visibility in AI Search",
        "chip": "AI Search & AEO",
        "date": "2026-10-02",
        "read_time": "12 min read",
        "author": "Bibek Khatiwada",
        "summary": "A technical guide to tracking brand presence across ChatGPT, Perplexity, and Google AI Overviews using automated prompt matrices, RAG chunking, and machine-readable context.",
        "tags": ["ai-search", "llm-tracking", "aeo", "geo", "technical"],
        "disciplines": [
            "LLM Tracking",
            "Answer Engine Optimization (AEO)",
            "Generative Engine Optimization (GEO)",
            "llms.txt",
            "Knowledge Graphs",
            "RAG Retrieval",
        ],
        "takeaways": [
            "Traditional rank tracking fails in generative search; LLM tracking monitors Citation Share of Voice (C-SoV), token distance, and anchor placement.",
            "Retrieval-Augmented Generation (RAG) relies on semantic chunking and cross-encoder re-ranking; high-density 40-word answer spans prevent chunk pruning.",
            "Deterministic prompt evaluation matrices (temperature=0.0) combined with /llms.txt and entity schema establish verifiable machine visibility.",
        ],
    },
    {
        "slug": "entity-attribute-value-search",
        "title": "The EAV (Entity-Attribute-Value) Model for Modern Search",
        "short": "EAV Model for Semantic Search",
        "chip": "Semantic Architecture",
        "date": "2026-10-02",
        "read_time": "10 min read",
        "author": "Bibek Khatiwada",
        "summary": "Moving beyond keyword density into knowledge graph triples. How structuring content as Entity-Attribute-Value triples establishes defensible topical authority for semantic search engines.",
        "tags": ["semantic-seo", "eav-model", "knowledge-graphs", "technical"],
        "disciplines": [
            "Entity-Attribute-Value (EAV)",
            "Semantic SEO",
            "Knowledge Graphs",
            "Topical Authority",
            "Structured Data",
        ],
        "takeaways": [
            "Search engines evaluate entities and their relationships, not just ungrounded keywords.",
            "Structuring content into explicit triplets (Subject -> Predicate -> Object) powers clear extraction by LLMs and Google Knowledge Graph.",
            "EAV modeling prevents internal content cannibalization by maintaining strict entity scopes across pillar-cluster networks.",
        ],
    },
    {
        "slug": "aeo-geo-playbook",
        "title": "AEO & GEO: Engineering Content for LLM Extraction & AI Overviews",
        "short": "Engineering Content for LLMs & AEO",
        "chip": "AI Search & AEO",
        "date": "2026-10-02",
        "read_time": "12 min read",
        "author": "Bibek Khatiwada",
        "summary": "Technical formatting, structured citations, schema grounding, and machine-readable llms.txt endpoints designed to maximize citation rate in Google AI Overviews, Perplexity, and ChatGPT.",
        "tags": ["aeo", "geo", "ai-search", "llms-txt", "citations"],
        "disciplines": [
            "Answer Engine Optimization (AEO)",
            "Generative Engine Optimization (GEO)",
            "llms.txt Standard",
            "Schema Grounding",
            "LLM Prompt Tracking",
        ],
        "takeaways": [
            "LLMs prioritize content structured with clean semantic headers, explicit definitions, and answer-first summaries.",
            "Publishing a standardized /llms.txt file gives AI crawlers direct access to core entity summaries and authoritative markdown links.",
            "Entity grounding via JSON-LD schema increases direct brand citation probability in AI search engines.",
        ],
    },
    {
        "slug": "130k-page-ymyl-recovery-mechanics",
        "title": "Anatomy of a 130,000-Page YMYL Recovery",
        "short": "130k-Page YMYL Recovery Mechanics",
        "chip": "Algorithm Recovery",
        "date": "2026-10-02",
        "read_time": "15 min read",
        "author": "Bibek Khatiwada",
        "summary": "The technical mechanics behind Case 01: crawl budget consolidation, pruning 20,000 dead/duplicate URLs, building structured topic hubs, and recovering visibility across core Google updates.",
        "tags": ["recovery", "ymyl", "crawl-budget", "technical-seo", "taxonomy"],
        "disciplines": [
            "Algorithm Recovery",
            "Crawl Budget Optimization",
            "Content Pruning",
            "Taxonomy Restructuring",
            "YMYL Trust Signals",
        ],
        "takeaways": [
            "YMYL recovery requires site-wide quality alignment rather than isolated page fixes.",
            "Pruning 20,000 duplicate/thin pages freed up crawl budget for high-value medical answer hubs.",
            "301 directory consolidation protects overall domain threshold value in zero-click search environments.",
        ],
    },
]

ARTICLES = FRAMEWORKS

# Proprietary & Open-Source Tools Showcase
TOOLS_SHOWCASE = [
    {
        "slug": "semantic-flow",
        "name": "Content Semantic Flow Checker",
        "chip": "NLP & Semantic Pipeline",
        "summary": "spaCy + sentence-transformers (all-MiniLM-L6-v2) pipeline for analyzing semantic similarity, topic drift, and entity coverage between content headers and search intent.",
        "tech_stack": ["Python 3.11", "spaCy", "sentence-transformers", "PyTorch", "Streamlit"],
        "github": "https://github.com/bibek1223/semantic-flow-checker",
        "demo": "https://github.com/bibek1223",
        "features": [
            "Cosine similarity matrix across document headings",
            "Entity extraction and Wikidata link mapping",
            "Sub-topic coverage scoring against top-ranking SERP competitors",
            "Automated suggestion engine for missing semantic attributes",
        ],
    },
    {
        "slug": "automation-engine",
        "name": "n8n & Colab GSC Anomaly Detector",
        "chip": "Search Automation",
        "summary": "Automated workflow engine monitoring daily Google Search Console API data for unexpected click/impression drops, cannibalization flags, and SERP layout shifts.",
        "tech_stack": ["n8n", "Python", "Google Colab", "Search Console API", "Slack Webhooks"],
        "github": "https://github.com/bibek1223/gsc-anomaly-detector",
        "demo": "https://github.com/bibek1223",
        "features": [
            "Daily statistical Z-score anomaly alerts sent to Slack/Email",
            "Page-level vs query-level drop isolation",
            "Automated Google Sheets dashboard sync via Apps Script",
            "AI Overview zero-click loss tracking",
        ],
    },
    {
        "slug": "llms-txt",
        "name": "Automated llms.txt & Markdown Generator",
        "chip": "AI Search Readiness",
        "summary": "Static generator module that automatically parses HTML site structure and builds a standardized, clean markdown /llms.txt file for AI web crawlers.",
        "tech_stack": ["Python", "BeautifulSoup4", "Jinja2", "Markdown"],
        "github": "https://github.com/bibek1223",
        "demo": "/llms.txt",
        "features": [
            "Automatic extraction of core site entities and case study metrics",
            "Strip out tracking scripts, CSS, and navigation bloat for clean LLM ingestion",
            "Hierarchical markdown formatting with canonical link attribution",
            "Seamless integration with Python static site build scripts",
        ],
    },
]

# Industry Matrix Hubs
INDUSTRIES_MATRIX = [
    {
        "slug": "home-services-hvac-plumbing",
        "title": "Home Trades & Multi-Location Services",
        "chip": "Local & Multi-Location",
        "summary": "HVAC, Plumbing, Electrical, Roofing, and Emergency Services. Optimizing local service-area pages, GBP listings, citation consistency, and hyper-local intent.",
        "niches": ["HVAC & Cooling", "Plumbing & Drainage", "Electrical Services", "Roofing & Exterior", "Emergency Restoration"],
        "pain_points": [
            "Duplicate content across dozens of location/city landing pages",
            "Google Business Profile suspensions and unverified storefronts",
            "High CPCs in Google Ads driving demand for organic local capture",
        ],
    },
    {
        "slug": "b2b-saas",
        "title": "B2B SaaS & Enterprise Tech",
        "chip": "SaaS & Software",
        "summary": "Product-led SEO, documentation search, comparison pages, and high-intent bottom-of-funnel keyword capturing for software platforms.",
        "niches": ["Developer Tools", "Workflow Automation", "Enterprise ERP/CRM", "Fintech SaaS", "Healthcare Tech"],
        "pain_points": [
            "Low-volume, high-value search intent requiring specialized technical content",
            "Complex JavaScript SPA rendering causing indexation delays",
            "High customer acquisition cost (CAC) requiring scalable organic acquisition",
        ],
    },
    {
        "slug": "programmatic-directories",
        "title": "Programmatic & Large Inventories",
        "chip": "Programmatic & E-commerce",
        "summary": "Automotive marketplaces, directory portals, real estate listings, and large e-commerce catalogs with hundreds of thousands of dynamic URLs.",
        "niches": ["Vehicle Scrapping & Auto Parts", "Property Listings", "Service Directories", "E-commerce Catalogs"],
        "pain_points": [
            "Crawl budget waste on thin, dynamic parameter URLs",
            "Template-level quality issues scaling into site-wide penalties",
            "Facet and filter indexation bloat",
        ],
    },
    {
        "slug": "healthcare-ymyl",
        "title": "Healthcare, Health Tech & YMYL Platforms",
        "chip": "YMYL & Healthcare",
        "summary": "Medical health platforms, telehealth portals, clinical research databases, and health tech providers requiring strict E-E-A-T trust signals, topic hub authority, and core update resilience.",
        "niches": ["Medical Information Portals", "Telehealth & Clinic Portals", "Health Tech SaaS", "Patient Education Hubs", "Medical Research Databases"],
        "pain_points": [
            "Heightened algorithmic scrutiny under Google Core and Helpful Content updates",
            "Medical consensus conflicts and unverified author credential attribution",
            "Crawl budget exhaustion across tens of thousands of duplicate condition and question pages",
        ],
    },
]

