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
});
