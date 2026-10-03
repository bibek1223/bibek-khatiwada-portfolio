/**
 * Interactive Lab Widgets for /tools/
 * 1. Live In-Browser Semantic Similarity & Vector Scoring
 * 2. Instant llms.txt File Generator & Validator
 */
document.addEventListener('DOMContentLoaded', () => {
  // 1. Semantic Similarity Engine Demo
  const runBtn = document.getElementById('run-sim-btn');
  const queryInp = document.getElementById('sim-query-input');
  const h1Inp = document.getElementById('sim-h1-input');
  const h2Inp = document.getElementById('sim-h2-input');
  const h3Inp = document.getElementById('sim-h3-input');
  const simResults = document.getElementById('sim-results-output');

  // Lightweight client-side token overlap & semantic heuristic (simulating all-MiniLM-L6-v2)
  function computeSemanticScore(query, heading) {
    if (!query || !heading) return 0;
    const qWords = query.toLowerCase().replace(/[^a-z0-9 ]/g, '').split(/\s+/).filter(Boolean);
    const hWords = heading.toLowerCase().replace(/[^a-z0-9 ]/g, '').split(/\s+/).filter(Boolean);

    // Exact matches
    const intersection = qWords.filter(w => hWords.includes(w));
    let score = (intersection.length / Math.max(qWords.length, 1)) * 0.6;

    // Stemming / partial matches
    const relatedTerms = ['crawl', 'budget', 'shopify', 'javascript', 'rendering', 'ymyl', 'medical', 'algorithm', 'update', 'seo', 'architecture', 'recovery'];
    const qRelated = qWords.filter(w => relatedTerms.includes(w));
    const hRelated = hWords.filter(w => relatedTerms.includes(w));
    const sharedTerms = qRelated.filter(w => hRelated.includes(w));
    score += (sharedTerms.length * 0.2);

    // Add baseline natural language coherence
    score += 0.15;
    return Math.min(0.96, Math.max(0.08, score));
  }

  if (runBtn && queryInp && simResults) {
    runBtn.addEventListener('click', () => {
      const q = queryInp.value.trim();
      const h1 = h1Inp ? h1Inp.value.trim() : '';
      const h2 = h2Inp ? h2Inp.value.trim() : '';
      const h3 = h3Inp ? h3Inp.value.trim() : '';

      const s1 = computeSemanticScore(q, h1);
      const s2 = computeSemanticScore(q, h2);
      const s3 = computeSemanticScore(q, h3);

      function renderBadge(score) {
        if (score >= 0.70) return `<span class="badge badge-success">High (${(score * 100).toFixed(1)}%) — RAG Retained</span>`;
        if (score >= 0.40) return `<span class="badge" style="background:#f59e0b;">Moderate (${(score * 100).toFixed(1)}%) — Borderline</span>`;
        return `<span class="badge badge-error">Drift (${(score * 100).toFixed(1)}%) — Pruned by LLM</span>`;
      }

      simResults.innerHTML = `
        <div style="display:grid;gap:0.75rem;margin-top:1rem;">
          <div style="background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:0.85rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">
            <span><strong>Header 1:</strong> ${h1 || 'Empty'}</span>
            ${renderBadge(s1)}
          </div>
          <div style="background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:0.85rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">
            <span><strong>Header 2:</strong> ${h2 || 'Empty'}</span>
            ${renderBadge(s2)}
          </div>
          <div style="background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:0.85rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">
            <span><strong>Header 3:</strong> ${h3 || 'Empty'}</span>
            ${renderBadge(s3)}
          </div>
        </div>
      `;
    });
  }

  // 2. llms.txt Live Generator
  const genBtn = document.getElementById('gen-llmstxt-btn');
  const siteNameInp = document.getElementById('llms-sitename');
  const siteUrlInp = document.getElementById('llms-url');
  const siteTopicsInp = document.getElementById('llms-topics');
  const llmsOutput = document.getElementById('llms-code-output');

  if (genBtn && siteNameInp && siteUrlInp && llmsOutput) {
    genBtn.addEventListener('click', () => {
      const name = siteNameInp.value.trim() || 'My Brand';
      const url = siteUrlInp.value.trim() || 'https://example.com';
      const topics = (siteTopicsInp.value.trim() || 'Core Services, Case Studies, Pricing')
        .split(',')
        .map(t => t.trim())
        .filter(Boolean);

      let text = `# ${name}\n\n`;
      text += `> Official knowledge base and technical specifications for LLM indexers and AI search crawlers.\n\n`;
      text += `## Core Entity Architecture\n`;
      text += `- Primary Domain: ${url}\n`;
      text += `- Canonical URL Scheme: HTTPS with trailing slashes\n\n`;
      text += `## Key Information Hubs\n`;
      topics.forEach(t => {
        const slug = t.toLowerCase().replace(/[^a-z0-9]+/g, '-');
        text += `- [${t}](${url}/${slug}/): Detailed technical breakdown and entity definitions.\n`;
      });
      text += `\n## Data Freshness & Verification\n`;
      text += `- Last Updated: ${new Date().toISOString().split('T')[0]}\n`;
      text += `- Machine-Readable Schema: ${url}/#website\n`;

      llmsOutput.textContent = text;
    });
  }

  // 3. GSC Statistical Anomaly Detector Simulator
  const anomMean = document.getElementById('anomaly-mean');
  const anomStd = document.getElementById('anomaly-stddev');
  const anomObserved = document.getElementById('anomaly-observed');
  const anomObservedVal = document.getElementById('anomaly-observed-val');
  const anomThreshold = document.getElementById('anomaly-threshold');
  const anomThresholdVal = document.getElementById('anomaly-threshold-val');
  const anomZDisplay = document.getElementById('anomaly-zscore-display');
  const anomDeltaDisplay = document.getElementById('anomaly-delta-display');
  const anomStatusBadge = document.getElementById('anomaly-status-badge');
  const anomJsonOutput = document.getElementById('anomaly-json-output');
  const copyAnomalyBtn = document.getElementById('copy-anomaly-json-btn');

  function updateAnomalySimulator() {
    if (!anomMean || !anomStd || !anomObserved || !anomThreshold || !anomZDisplay) return;

    const mean = parseFloat(anomMean.value) || 3000;
    const std = parseFloat(anomStd.value) || 250;
    const observed = parseFloat(anomObserved.value) || 2000;
    const thresh = parseFloat(anomThreshold.value) || 2.0;

    anomObservedVal.textContent = Number(observed).toLocaleString();
    anomThresholdVal.textContent = '-' + thresh.toFixed(2) + 'σ';

    const delta = observed - mean;
    const pct = ((delta / mean) * 100).toFixed(1);
    const zScore = (delta / std);

    anomZDisplay.textContent = `Z = ${zScore > 0 ? '+' : ''}${zScore.toFixed(2)}σ`;
    anomDeltaDisplay.textContent = `${delta > 0 ? '+' : ''}${Number(Math.round(delta)).toLocaleString()} clicks (${pct > 0 ? '+' : ''}${pct}%)`;

    const isCritical = zScore <= -thresh;
    const isWarning = zScore <= -1.2 && !isCritical;

    if (isCritical) {
      anomStatusBadge.innerHTML = '<span class="badge badge-error">CRITICAL ANOMALY DETECTED</span>';
      anomZDisplay.style.color = '#ef4444';
      anomDeltaDisplay.style.color = '#ef4444';
    } else if (isWarning) {
      anomStatusBadge.innerHTML = '<span class="badge" style="background:#f59e0b;color:#1e1b2e;">ELEVATED VARIANCE (WATCH)</span>';
      anomZDisplay.style.color = '#f59e0b';
      anomDeltaDisplay.style.color = '#f59e0b';
    } else {
      anomStatusBadge.innerHTML = '<span class="badge badge-success">WITHIN NORMAL NOISE BAND</span>';
      anomZDisplay.style.color = '#10b981';
      anomDeltaDisplay.style.color = '#10b981';
    }

    const payload = {
      timestamp: new Date().toISOString(),
      event_type: isCritical ? "CRITICAL_GSC_TRAFFIC_DROP_ANOMALY" : (isWarning ? "ELEVATED_VARIANCE_WARNING" : "NORMAL_MONITORING_PULSE"),
      severity: isCritical ? "CRITICAL" : (isWarning ? "WARNING" : "INFO"),
      statistical_telemetry: {
        baseline_90d_mean: mean,
        standard_deviation: std,
        observed_clicks_last_24h: observed,
        absolute_delta: delta,
        percentage_deviation: `${pct}%`,
        z_score: Number(zScore.toFixed(2)),
        configured_alert_threshold: `-${thresh.toFixed(2)}σ`,
        anomaly_detected: isCritical
      },
      recommended_triage_protocol: isCritical ? [
        "1. Cross-reference Google Search Status Dashboard & Search Central update rollouts.",
        "2. Query BigQuery GSC partitioned table for URL directory-level drops.",
        "3. Inspect server access logs for crawler 4xx/5xx spike or robots.txt blockages.",
        "4. Audit Core Web Vitals field data (LCP/INP) for degradation."
      ] : [
        "Routine automated pulse. No manual intervention required."
      ],
      dispatched_to: "#seo-telemetry-alerts",
      engineer: "Bibek Khatiwada (bibek-khatiwada.com.np)"
    };

    if (anomJsonOutput) {
      anomJsonOutput.textContent = JSON.stringify(payload, null, 2);
    }
  }

  if (anomMean && anomStd && anomObserved && anomThreshold) {
    [anomMean, anomStd, anomObserved, anomThreshold].forEach(el => {
      el.addEventListener('input', updateAnomalySimulator);
    });
    updateAnomalySimulator();
  }

  if (copyAnomalyBtn && anomJsonOutput) {
    copyAnomalyBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(anomJsonOutput.textContent).then(() => {
        const orig = copyAnomalyBtn.textContent;
        copyAnomalyBtn.textContent = 'Copied!';
        setTimeout(() => { copyAnomalyBtn.textContent = orig; }, 1800);
      });
    });
  }

  // 4. AI Crawler Robots.txt Configurator
  const botOaiSearch = document.getElementById('bot-oai-search');
  const botPerplexity = document.getElementById('bot-perplexity');
  const botClaudebot = document.getElementById('bot-claudebot');
  const botGptbot = document.getElementById('bot-gptbot');
  const botGoogleExt = document.getElementById('bot-google-extended');
  const botBytespider = document.getElementById('bot-bytespider');
  const robotsOutput = document.getElementById('robots-code-output');
  const copyRobotsBtn = document.getElementById('copy-robots-btn');

  function updateRobotsConfig() {
    if (!robotsOutput) return;

    let txt = `# Enterprise AI Crawler & Search Engine Policy\n# Configured via Bibek Khatiwada Architecture Suite\n\n`;
    txt += `User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /admin/\nDisallow: /*?*filter=\n\n`;

    const bots = [
      { id: botOaiSearch, name: 'OAI-SearchBot', purpose: 'OpenAI Search Citations' },
      { id: botPerplexity, name: 'PerplexityBot', purpose: 'Perplexity AI Search Cards' },
      { id: botClaudebot, name: 'ClaudeBot', purpose: 'Anthropic Real-time Grounding' },
      { id: botGptbot, name: 'GPTBot', purpose: 'OpenAI Foundation Model Training' },
      { id: botGoogleExt, name: 'Google-Extended', purpose: 'Google Gemini Training Scraper' },
      { id: botBytespider, name: 'Bytespider', purpose: 'ByteDance Scraper' }
    ];

    bots.forEach(b => {
      if (b.id) {
        txt += `# ${b.purpose}\nUser-agent: ${b.name}\n${b.id.checked ? 'Allow: /' : 'Disallow: /'}\n\n`;
      }
    });

    txt += `Sitemap: https://yourdomain.com/sitemap.xml\n`;
    robotsOutput.textContent = txt.trim();
  }

  const botCheckboxes = [botOaiSearch, botPerplexity, botClaudebot, botGptbot, botGoogleExt, botBytespider];
  botCheckboxes.forEach(cb => {
    if (cb) cb.addEventListener('change', updateRobotsConfig);
  });
  updateRobotsConfig();

  if (copyRobotsBtn && robotsOutput) {
    copyRobotsBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(robotsOutput.textContent).then(() => {
        const orig = copyRobotsBtn.textContent;
        copyRobotsBtn.textContent = 'Copied!';
        setTimeout(() => { copyRobotsBtn.textContent = orig; }, 1800);
      });
    });
  }
});

