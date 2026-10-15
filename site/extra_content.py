"""Supporting copy for pages that were thin: industries, frameworks, blog, ROI calculator, process.

Rules for everything in this file (carried from HANDOFF.md): no invented statistics, no client data,
no claims about what Google guarantees. Statements describe method and trade-offs only.
"""

# ---------------------------------------------------------------- industries (per vertical)
INDUSTRY_EXTRA = {
    "home-services-hvac-plumbing": {
        "intent": [
            ("Service page", "One page per core service (for example, drain cleaning or furnace repair) that states what is included, who it is for, how booking works, and what it costs to start."),
            ("Location page", "One page per place you genuinely serve, with local proof such as real jobs, neighbourhood names, local reviews and a map. Swapping the city name in a template is not enough."),
            ("Emergency page", "A fast, scannable page for urgent searches: phone number, response window you can actually keep, and what to do before the technician arrives."),
            ("Cost and comparison page", "Honest price ranges and the factors that move them, written for someone deciding between a repair and a replacement."),
        ],
        "sequence": [
            "Confirm the Google Business Profile is verified, categorised correctly and consistent with the website name, address and phone number.",
            "Map services and service areas to a hub-and-spoke structure so each location page links to the service pages it relates to.",
            "Rewrite or merge location pages that differ only by the place name; keep the ones with real local detail.",
            "Add LocalBusiness and Service structured data that matches the visible page, and fix citation inconsistencies.",
            "Track calls, form fills and direction requests, not only rankings, so local work is judged on enquiries.",
        ],
        "mistakes": [
            "Publishing dozens of near-identical city pages that rank for nothing and dilute the strong ones.",
            "Listing a service area far larger than the business can serve, which attracts enquiries it cannot fulfil.",
            "Letting profile details, hours or phone numbers drift out of sync across directories.",
            "Measuring success only by map-pack position instead of booked jobs.",
        ],
        "faq": [
            ("Do I need a page for every town I serve?", "Only where you can say something specific and useful about that place. Fewer, stronger location pages usually outperform many thin ones, and the rest can be covered by one clear service-area page."),
            ("Does a service-area business without a storefront need a different approach?", "The profile rules differ, because the address may be hidden, but the website work is the same: clear services, genuine local proof and consistent business details."),
            ("How long does local SEO take to show results?", "It depends on competition, the current state of the profile and the site, and how quickly changes can be shipped. A diagnosis should give an honest range for your market rather than a fixed number."),
            ("Should reviews be part of the SEO plan?", "Yes. Review volume, recency and the content of reviews support both visibility and conversion, as long as they are earned through a normal request process."),
        ],
    },
    "b2b-saas": {
        "intent": [
            ("Problem page", "Targets the pain before the buyer knows your category. It explains the problem, the cost of leaving it unsolved and the shape of a good solution."),
            ("Use-case and integration page", "Shows how the product fits a specific workflow or tool, with screenshots, steps and the outcome a user can expect."),
            ("Comparison and alternative page", "Fair, factual comparisons for buyers shortlisting vendors. Credibility depends on stating where a competitor is the better fit."),
            ("Documentation and changelog", "Often the most technical and most linkable content on the site. It needs clean URLs, stable headings and crawlable HTML."),
        ],
        "sequence": [
            "Audit how the app, marketing site and docs are rendered so that content can be crawled without relying on client-side JavaScript alone.",
            "Build a topic map around the product's jobs-to-be-done, not around a list of keywords.",
            "Create the bottom-of-funnel pages first (use cases, comparisons, integrations), then supporting educational content.",
            "Align internal links so educational pages pass readers toward product and demo pages with clear intent.",
            "Connect organic landing pages to signups, demo requests and pipeline in analytics.",
        ],
        "mistakes": [
            "Treating organic search as a blog problem and ignoring product, integration and comparison pages.",
            "Shipping a single-page app whose important routes render empty HTML to crawlers.",
            "Writing comparison pages that read as advertising and earn neither trust nor links.",
            "Chasing high-volume keywords with weak buying intent while low-volume, high-intent queries go unanswered.",
        ],
        "faq": [
            ("Is a low search volume keyword worth targeting?", "Often, yes. A query used by a few dozen qualified buyers a month can be worth more than a broad term read by thousands who will never buy."),
            ("How should documentation be treated in SEO?", "As a product surface. Give docs crawlable pages, descriptive titles and stable URLs, and link them from the product pages they support."),
            ("Can SEO replace paid acquisition for a SaaS product?", "It can reduce reliance over time, but the two serve different timelines. Organic compounds slowly, while paid is immediate, so the sensible goal is a deliberate balance."),
            ("What should be measured?", "Qualified signups and demo requests from organic landing pages, plus assisted conversions, rather than sessions on their own."),
        ],
    },
    "programmatic-directories": {
        "intent": [
            ("Category and hub page", "Groups listings by a real attribute (make, region, type) and gives the reader a reason to choose a sub-category, not just a list of links."),
            ("Listing or entity page", "One URL per genuine item, with unique attributes, current status and enough original detail to justify existing."),
            ("Filter and facet combinations", "Indexed only when a combination matches real search demand and has meaningful inventory; everything else stays crawlable but not indexable."),
            ("Template-level content", "The introduction, FAQs and supporting copy that make a template page more than a database record."),
        ],
        "sequence": [
            "Segment the URL inventory by template, parameter and status, and measure which segments earn clicks and which only consume crawl.",
            "Decide the indexation rule for each segment: index, noindex, canonicalise, block or remove.",
            "Define a quality floor for template pages (minimum unique data points, content depth, internal links) and enforce it at build time.",
            "Strengthen hubs with real content and link them to the best listings, so crawl and authority flow to valuable URLs.",
            "Monitor crawl stats and indexed-page counts after each release, and roll back templates that increase low-value URLs.",
        ],
        "mistakes": [
            "Generating a page for every filter combination and letting crawlers find all of them.",
            "Filling templates with boilerplate that varies by one word.",
            "Leaving expired or out-of-stock listings live with no status, redirect or alternative.",
            "Changing a template site-wide without a staged rollout and a way to measure the effect.",
        ],
        "faq": [
            ("How do I know if I have too many indexable URLs?", "Compare the number of indexed URLs with the number that receive impressions or clicks. A large gap, especially in one template or parameter, is the first thing to investigate."),
            ("Should thin pages be deleted or improved?", "It depends on whether the page has a reason to exist. Pages with demand and real data can be improved; pages with neither are usually better consolidated, redirected or noindexed."),
            ("Is programmatic SEO risky?", "It is when scale is the strategy. It works when each page answers a real query with real data, and when quality rules are built into the template."),
            ("How is crawl budget affected?", "On large sites, crawlers spend time on whatever they find first. Cutting low-value URLs and improving internal links helps crawlers reach the pages that matter sooner."),
        ],
    },
    "healthcare-ymyl": {
        "intent": [
            ("Condition and symptom page", "Accurate, plainly written information reviewed by a qualified person, with sources, dates and clear guidance on when to seek care."),
            ("Treatment and procedure page", "Balanced coverage of options, risks and alternatives, written to inform rather than to sell."),
            ("Provider and clinic page", "Verifiable credentials, locations, services and contact details, with structured data that matches the visible information."),
            ("Research and evidence page", "Summaries that cite primary sources and state limits clearly, so both readers and quality reviewers can verify claims."),
        ],
        "sequence": [
            "Audit content for accuracy risk first: outdated guidance, unsupported claims and pages with no identifiable author or reviewer.",
            "Establish visible authorship, reviewer credentials, sourcing and update-date policies that readers can find on every article.",
            "Consolidate duplicate and overlapping condition or question pages into stronger topic hubs.",
            "Strengthen about, editorial-policy and contact pages so the organisation behind the content is easy to verify.",
            "Re-measure by topic cluster, so recovery or decline can be tied to specific hubs rather than to the whole site.",
        ],
        "mistakes": [
            "Publishing medical content without a named, qualified author or reviewer.",
            "Keeping thousands of near-duplicate question pages that compete with each other.",
            "Making claims that go further than the cited evidence supports.",
            "Treating a ranking drop as a pure technical issue when quality and trust signals are the cause.",
        ],
        "faq": [
            ("Is there a way to guarantee protection from core updates?", "No. The sensible approach is to raise quality and trust across the site and make the evidence for it visible, which lowers risk rather than eliminating it."),
            ("Do author bios and reviewer credits really matter?", "They help readers and quality reviewers judge who stands behind the content. They support, but do not replace, accurate and well-sourced writing."),
            ("Should low-performing pages be removed?", "Often they are better consolidated into a stronger page, with redirects, than left to compete. The decision should rest on traffic, accuracy and uniqueness, not on length."),
            ("What does recovery look like?", "Usually gradual and tied to the timing of later updates, so progress is tracked by segment over months rather than by week."),
        ],
    },
}

INDUSTRY_INDEX = {
    "how": [
        ("Understand the business model", "Revenue per lead, sales cycle and how customers decide set which pages matter. A plumber, a software vendor and a parts marketplace need different pages for the same keyword."),
        ("Find the structural constraint", "Every sector has a limiting factor: duplicate location pages, JavaScript rendering, parameter URLs or trust signals. Fixing that constraint first makes later content work count."),
        ("Build the page system", "Define the page types, templates and internal links that match search intent, then publish in an order that lets each stage be measured."),
    ],
    "faq": [
        ("Can the same framework apply to any industry?", "The method is shared (research, structure, implementation, measurement), but the page types, risks and metrics change by sector, which is what each blueprint documents."),
        ("What if my business is not listed?", "The blueprints are starting points. A short diagnostic of your site and market shows which parts transfer and which need a different plan."),
        ("Do these pages contain client results?", "Client names are confidential. The linked case studies carry Search Console figures with the vertical described, and nothing more specific."),
    ],
}

# ---------------------------------------------------------------- frameworks (per article)
FRAMEWORK_EXTRA = {
    "llm-tracking": {
        "checklist": [
            "Write a prompt set that reflects real customer questions, grouped by intent.",
            "Record the engine, date, location and settings for every run so results can be compared.",
            "Store the raw answer, not only a summary, so extraction rules can be improved later.",
            "Track mentions and citations separately; being named is not the same as being linked.",
            "Repeat runs on a schedule and report ranges, not single results.",
            "Review which of your pages and third-party sources are being cited, and fix the weak ones.",
        ],
        "pitfalls": [
            "Treating one screenshot of one answer as a trend.",
            "Changing the prompt wording between runs and comparing the results.",
            "Reporting an AI visibility score without explaining how it was calculated.",
            "Ignoring third-party sources, which are often what the model actually cites.",
        ],
        "faq": [
            ("Is LLM tracking the same as rank tracking?", "No. Rankings come from a mostly stable results page, while generated answers vary by prompt, model and time. The measurement has to sample and report variation."),
            ("How many prompts do I need?", "Enough to cover your main intents and entities, and few enough to run consistently. Start small, keep the set stable and expand only when the process is reliable."),
            ("Can I influence what an AI answer says about my brand?", "You can improve the sources it can retrieve: clear pages, consistent entity information and credible third-party coverage. There is no switch that guarantees a mention."),
        ],
    },
    "entity-attribute-value-search": {
        "checklist": [
            "Name the single entity the page is about, in a sentence a reader could repeat.",
            "List the attributes an informed reader would expect, and mark which are missing.",
            "Give each attribute an explicit value, source or example rather than a vague claim.",
            "Decide which attributes deserve their own page and which stay as sections.",
            "Make the headings, internal links and structured data describe the same entity.",
            "Review related pages for overlap and assign each one a distinct job.",
        ],
        "pitfalls": [
            "Using the model as a keyword list instead of a scoping tool.",
            "Marking up attributes in schema that are not visible on the page.",
            "Splitting one entity across many pages so none of them is complete.",
            "Merging genuinely different entities because their keywords look alike.",
        ],
        "faq": [
            ("Is EAV a Google ranking factor?", "No. It is a planning method. It helps define page scope and completeness, which supports relevance, but it is not a signal that can be switched on."),
            ("Do I need a knowledge graph to use it?", "No. A spreadsheet of entities, attributes and values is enough to guide a content plan."),
            ("How does it prevent cannibalization?", "Each page is given one entity and one role. When two pages claim the same combination, one of them is merged, redirected or repositioned."),
        ],
    },
    "aeo-geo-playbook": {
        "checklist": [
            "Open each key section with a direct answer of one to three sentences.",
            "Use descriptive headings that match how people phrase the question.",
            "State definitions, comparisons and numbers explicitly, with their source.",
            "Keep entity names consistent across the page, schema and about information.",
            "Publish a clear author, date and organisation so claims can be attributed.",
            "Offer a concise, accurate llms.txt as a convenience, without treating it as a guaranteed signal.",
        ],
        "pitfalls": [
            "Rewriting everything into short fragments and losing the explanation readers need.",
            "Stuffing definitions into pages where they do not serve a reader.",
            "Assuming schema or llms.txt alone causes citations.",
            "Chasing every new AI surface instead of fixing the underlying content quality.",
        ],
        "faq": [
            ("What is the difference between AEO and GEO?", "The terms overlap. Answer engine optimization focuses on being the direct answer, while generative engine optimization looks at being included in synthesized responses. The practical work is largely shared."),
            ("Does llms.txt improve rankings?", "There is no evidence it is a ranking factor. It is a lightweight way to point automated readers at your most useful pages, so treat it as a low-cost addition."),
            ("Will this hurt traditional SEO?", "Clear structure, direct answers and consistent entities tend to help both. The risk is over-formatting at the expense of depth."),
        ],
    },
    "130k-page-ymyl-recovery-mechanics": {
        "checklist": [
            "Overlay performance changes with known update dates and site release events.",
            "Segment URLs by directory and template before opening any single page.",
            "Separate pages that need improvement from pages that should be consolidated.",
            "Map every removed or merged URL to the best matching destination.",
            "Document author, reviewer and sourcing standards and apply them to priority hubs first.",
            "Check crawl, indexing and impressions by segment after each change batch.",
        ],
        "pitfalls": [
            "Fixing individual pages while the template or directory problem remains.",
            "Mass-deleting content without redirect mapping or a way to measure the effect.",
            "Expecting immediate recovery instead of waiting for later evaluations.",
            "Changing too many things at once to learn which change mattered.",
        ],
        "faq": [
            ("How long does a recovery take?", "It varies widely and tends to track the timing of later updates and re-evaluations, so plan in months and report progress by segment."),
            ("Is pruning always the answer?", "No. Pruning helps where pages are duplicate or empty. Where pages are thin but valuable, improving or consolidating them can be better."),
            ("Does this apply to smaller sites?", "The sequence applies, but a smaller site can often be reviewed page by page, which makes segmentation less important."),
        ],
    },
}

FRAMEWORK_INDEX = {
    "how": [
        ("Who these are for", "SEO leads, technical marketers and developers who want the reasoning behind a decision, not only the checklist."),
        ("How to read them", "Each essay opens with the problem, walks through the mechanics, shows a minimal example and closes with how to interpret results. The takeaways box at the top gives the short version."),
        ("What they are not", "They are not rankings guarantees or secret tricks. They describe methods that can be tested on your own site, with their limits stated."),
    ],
}

# ---------------------------------------------------------------- blog index
BLOG_INDEX = {
    "topics": [
        ("AI search and measurement", "How brands are mentioned and cited in generated answers, and how to track it without over-reading one result."),
        ("Entity and semantic architecture", "Planning pages around entities and attributes so that content is complete, distinct and easy to retrieve."),
        ("Large-site technical SEO", "Crawl behaviour, indexation, rendering and template quality on sites with tens or hundreds of thousands of URLs."),
        ("Automation for SEO teams", "Workflows with n8n, Python and Apps Script that remove manual reporting and monitoring work."),
    ],
    "paths": [
        ("New to AI search", "Start with LLM tracking, then read the AEO and GEO playbook."),
        ("Planning a content architecture", "Start with the EAV model, then look at the industry blueprints."),
        ("Managing a large or declining site", "Start with the 130,000-page recovery mechanics, then the matching case studies."),
    ],
}

# ---------------------------------------------------------------- ROI calculator
ROI_EXTRA = {
    "how": [
        ("What it calculates", "The gap between your current and target click-through rate, applied to monthly search demand, then multiplied by your conversion rate, average value and twelve months."),
        ("What it does not include", "New keywords, new pages, changes in rankings, seasonality or the cost of doing the work. It models one lever, click-through rate, and nothing else."),
        ("How to use the result", "Treat it as an order-of-magnitude check on whether a project is worth scoping, then replace each input with your own Search Console and analytics data."),
    ],
    "inputs": [
        ("Monthly search demand", "Total monthly searches across the topics you want to win, from Search Console impressions or a keyword tool."),
        ("Current and target CTR", "Your average click-through rate today, and the rate you think a better title, snippet or position could reach."),
        ("Conversion rate", "The share of organic visits that become a lead or sale in your analytics."),
        ("Average value", "Revenue or lead value per conversion, using a figure your finance team would accept."),
    ],
    "faq": [
        ("Are the preset numbers benchmarks?", "No. They are illustrative starting values so the calculator is usable on first load. Replace them with your own data."),
        ("Why might the real result differ?", "Click-through rate depends on position, search features and competition. A forecast from a single input is a guide, not a promise."),
        ("Is my data stored?", "The calculator runs in your browser. Nothing you enter is sent to a server."),
    ],
}

# ---------------------------------------------------------------- process page
PROCESS_EXTRA = {
    "deliverables": [
        ("Diagnose", "A written findings document that separates confirmed issues from hypotheses, with the evidence for each and a first priority list."),
        ("Architect", "A page and entity map, the target internal-link structure and a template specification for the pages that will be created or changed."),
        ("Implement", "A change log of what shipped, when, and on which URLs, along with the checks used to confirm each release."),
        ("Measure", "A report that compares results with the baseline, explains what changed and why, and names the next experiments."),
    ],
}

# ---------------------------------------------------------------- title / meta overrides
# Applied in layout.head() by path. Titles <= 60 chars, descriptions 110-160 chars.
SEO_META = {
    "blog/llm-tracking/": ("LLM Tracking: Measure Brand Visibility in AI Search",
                           "How to track brand mentions and citations in ChatGPT, Perplexity and Google AI Overviews with a stable prompt set, repeat runs and clear scoring."),
    "frameworks/llm-tracking/": ("LLM Tracking Framework: The Evaluation Loop",
                                 "The short version of the LLM tracking method: prompt matrix, repeat runs, citation extraction and how to read movement in AI answers."),
    "frameworks/": ("SEO Frameworks & AI Search Playbooks | Bibek Khatiwada",
                    "Technical essays by Bibek Khatiwada: Entity-Attribute-Value search modeling, AEO/GEO engineering, and 130k-page YMYL recovery mechanics."),
    "frameworks/130k-page-ymyl-recovery-mechanics/": (
        "Anatomy of a 130,000-Page YMYL Recovery | Bibek Khatiwada",
        "How a 130,000-page health site was diagnosed and restructured: segmentation, pruning duplicate URLs, topic hubs and recovery across core updates."),
    "frameworks/aeo-geo-playbook/": (
        "AEO & GEO Playbook for AI Overviews | Bibek Khatiwada",
        "Answer-first structure, explicit entities, schema grounding and llms.txt: how to make pages easier for AI Overviews, Perplexity and ChatGPT to cite."),
    "frameworks/entity-attribute-value-search/": (
        "EAV Model for Semantic SEO | Bibek Khatiwada",
        "Use the Entity-Attribute-Value model to scope pages, find missing attributes and stop cannibalization, with a worked example and checklist."),
    "industries/": ("Industry SEO Blueprints | Bibek Khatiwada",
                    "SEO blueprints for home services, B2B SaaS, programmatic directories and healthcare: the page types, risks and order of work each sector needs."),
    "industries/b2b-saas/": ("B2B SaaS SEO Blueprint | Bibek Khatiwada", None),
    "industries/healthcare-ymyl/": ("Healthcare & YMYL SEO Blueprint | Bibek Khatiwada",
                                    "SEO for medical, telehealth and health tech sites: E-E-A-T signals, topic hubs, content consolidation and resilience through Google core updates."),
    "industries/home-services-hvac-plumbing/": ("Local SEO for Home Services & Trades | Bibek Khatiwada", None),
    "industries/programmatic-directories/": ("Programmatic SEO for Large Sites | Bibek Khatiwada", None),
    "process/": ("How I Work: SEO Process & Delivery | Bibek Khatiwada", None),
    "services/": ("SEO Services by Bibek Khatiwada: Technical, Content, AI",
                  "Technical SEO, content architecture, automation, AI search, local and e-commerce SEO: what each service includes and the case studies behind it."),
}

# Pages whose content is a subset of another page: canonical points at the fuller page,
# and they are left out of the sitemap.
CANONICAL_TO = {"frameworks/llm-tracking/": "blog/llm-tracking/"}

# ---------------------------------------------------------------- contextual links
# (anchor text, site-relative path). Rendered as a "Related reading" block in the article body.
RELATED_LINKS = {
    "home-services-hvac-plumbing": [
        ("Algorithm recovery service", "services/#algorithm-recovery"),
        ("Entity-based architecture for service hubs", "services/#entity-architecture"),
        ("Case 05: broad core update recovery", "case-studies/broad-core-update-recovery/"),
        ("What keyword cannibalization means", "glossary/#keyword-cannibalization"),
        ("Model the value of a better click-through rate", "roi-calculator/"),
    ],
    "b2b-saas": [
        ("Technical infrastructure and rendering", "services/#technical-infrastructure"),
        ("JavaScript rendering and SSR, explained", "glossary/#javascript-rendering-ssr"),
        ("Case 07: new SaaS platform ramp", "case-studies/saas-fast-ramp/"),
        ("The EAV model for planning product pages", "frameworks/entity-attribute-value-search/"),
        ("AEO and GEO for software comparisons", "frameworks/aeo-geo-playbook/"),
    ],
    "programmatic-directories": [
        ("Case 02: programmatic pages at scale", "case-studies/programmatic-vehicle-scrapping/"),
        ("Case 03: Shopify rendering and crawl budget", "case-studies/shopify-rendering-crawl-budget/"),
        ("What crawl budget is", "glossary/#crawl-budget"),
        ("Programmatic SEO, defined", "glossary/#programmatic-seo"),
        ("Technical infrastructure service", "services/#technical-infrastructure"),
    ],
    "healthcare-ymyl": [
        ("Anatomy of a 130,000-page YMYL recovery", "frameworks/130k-page-ymyl-recovery-mechanics/"),
        ("Case 09: topical authority for medical research", "case-studies/medical-research-topical-authority/"),
        ("What E-E-A-T covers", "glossary/#eeat"),
        ("Directory consolidation, explained", "glossary/#directory-consolidation"),
        ("Algorithm recovery service", "services/#algorithm-recovery"),
    ],
    "llm-tracking": [
        ("Read the full LLM tracking guide", "blog/llm-tracking/"),
        ("Citation share of voice, defined", "glossary/#citation-share-of-voice"),
        ("AEO and GEO playbook", "frameworks/aeo-geo-playbook/"),
        ("AEO, GEO and AI search service", "services/#aeo-geo-search"),
    ],
    "entity-attribute-value-search": [
        ("Entity-based architecture service", "services/#entity-architecture"),
        ("Topical authority, defined", "glossary/#topical-authority"),
        ("Keyword cannibalization, defined", "glossary/#keyword-cannibalization"),
        ("B2B SaaS blueprint", "industries/b2b-saas/"),
        ("Case 08: SaaS organic growth from launch", "case-studies/saas-organic-from-launch/"),
    ],
    "aeo-geo-playbook": [
        ("LLM tracking guide", "blog/llm-tracking/"),
        ("The llms.txt standard", "glossary/#llms-txt-standard"),
        ("Schema and JSON-LD", "glossary/#schema-json-ld"),
        ("AEO, GEO and AI search service", "services/#aeo-geo-search"),
        ("llms.txt generator on the tools page", "tools/"),
    ],
    "130k-page-ymyl-recovery-mechanics": [
        ("Healthcare and YMYL blueprint", "industries/healthcare-ymyl/"),
        ("Case 05: broad core update recovery", "case-studies/broad-core-update-recovery/"),
        ("Crawl budget, defined", "glossary/#crawl-budget"),
        ("Log file forensics, defined", "glossary/#log-file-forensics"),
        ("Algorithm recovery service", "services/#algorithm-recovery"),
    ],
}

# ---------------------------------------------------------------- case evidence
# Search Console screenshots in design/assets/gsc/, keyed by case number. Totals in each image
# were checked against CASE_STUDIES. Case 01 is held back until its attribution is settled.
CASE_CHARTS = {
    "02": ("gsc/programmatic-scale.jpg", 1100, 468,
           "Google Search Console performance report, 16 months: 1.12M clicks, 117M impressions, 1% CTR, average position 14.8"),
    "03": ("gsc/shopify-rendering.jpg", 1100, 475,
           "Google Search Console performance report, 16 months: 449K clicks, 40.8M impressions, 1.1% CTR, average position 8.2"),
}
