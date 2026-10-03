/**
 * 3-Step SEO Audit Diagnostic Wizard
 * Auto-compiles technical brief & enables 1-click WhatsApp transfer or email dispatch.
 */
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('audit-form');
  if (!form) return;

  const steps = form.querySelectorAll('.audit-step');
  const dots = document.querySelectorAll('.step-indicator');
  const briefBox = document.getElementById('brief-content');
  const waBtn = document.getElementById('audit-wa-btn');
  const status = document.getElementById('audit-status');
  let briefText = '';

  function stepValid(stepNum) {
    const step = form.querySelector(`.audit-step[data-step="${stepNum}"]`);
    const required = step ? step.querySelectorAll('[required]') : [];
    for (const field of required) {
      if (!field.checkValidity()) { field.reportValidity(); return false; }
    }
    return true;
  }

  function showStep(stepNum) {
    steps.forEach(s => s.classList.remove('active'));
    dots.forEach(d => d.classList.remove('active'));

    const targetStep = form.querySelector(`.audit-step[data-step="${stepNum}"]`);
    const targetDot = document.querySelector(`.step-indicator[data-step-dot="${stepNum}"]`);

    if (targetStep) targetStep.classList.add('active');
    if (targetDot) targetDot.classList.add('active');

    if (stepNum === 3) {
      compileBrief();
    }
  }

  function compileBrief() {
    const url = document.getElementById('audit-url')?.value || 'Not specified';
    const cms = document.getElementById('audit-cms')?.value || 'Not specified';
    const traffic = document.getElementById('audit-traffic')?.value || 'Not specified';
    const selectedSymptom = form.querySelector('input[name="symptom"]:checked')?.value || 'General Diagnostic';

    let focusDetail = 'Checking crawl budget limits, entity grounding, and Search Console anomaly timestamps.';
    if (selectedSymptom.includes('Core Update')) {
      focusDetail = 'Isolating specific Google broad core & spam update rollout windows, query consolidation losses, and thin taxonomy risks.';
    } else if (selectedSymptom.includes('AI Overview')) {
      focusDetail = 'Auditing semantic answer spans, RAG retrieval re-ranking chunk survival, and EAV table extraction.';
    } else if (selectedSymptom.includes('Indexation')) {
      focusDetail = 'Analyzing log file crawl efficiency, JavaScript render tree bottlenecks, and parameter URL bloat.';
    }

    const notes = document.getElementById('audit-notes')?.value.trim() || '';
    briefText = [
      'Hi Bibek,', '', 'I completed the SEO diagnostic on your portfolio:',
      `Website: ${url}`, `CMS / stack: ${cms}`, `Organic scale: ${traffic}`,
      `Primary symptom: ${selectedSymptom}`, `Suggested forensic focus: ${focusDetail}`,
      notes ? `Additional context: ${notes}` : '', '',
      'I would like to discuss the most useful first investigation.'
    ].filter(Boolean).join('\n');
    if (briefBox) {
      briefBox.replaceChildren();
      const pre = document.createElement('pre');
      pre.className = 'audit-brief-text';
      pre.textContent = briefText;
      briefBox.appendChild(pre);
    }

    // Update WhatsApp link with pre-filled message
    const waText = encodeURIComponent(
      briefText
    );
    if (waBtn) {
      waBtn.href = `https://wa.me/9779860411440?text=${waText}`;
    }
  }

  function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  form.querySelectorAll('.btn-next').forEach(btn => {
    btn.addEventListener('click', () => {
      const currentStep = parseInt(btn.closest('.audit-step').dataset.step, 10);
      if (!stepValid(currentStep)) return;
      const nextStep = parseInt(btn.dataset.next, 10);
      showStep(nextStep);
    });
  });

  form.querySelectorAll('.btn-prev').forEach(btn => {
    btn.addEventListener('click', () => {
      const prevStep = parseInt(btn.dataset.prev, 10);
      showStep(prevStep);
    });
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!stepValid(3)) return;
    compileBrief();
    const email = document.getElementById('audit-email')?.value.trim();
    const body = briefText + `\n\nReply to: ${email}`;
    window.location.href = `mailto:bibekkhatiwada2@gmail.com?subject=${encodeURIComponent('SEO diagnostic: ' + (document.getElementById('audit-url')?.value || 'website'))}&body=${encodeURIComponent(body)}`;
    if (status) status.textContent = 'Opening your email app. Review the message there before sending.';
  });

  form.addEventListener('input', () => {
    if (form.querySelector('.audit-step[data-step="3"].active')) compileBrief();
  });

  // Heuristic Scorer
  const selRender = document.getElementById('h-render');
  const selCwv = document.getElementById('h-cwv');
  const selSchema = document.getElementById('h-schema');
  const selUrls = document.getElementById('h-urls');
  const selAeo = document.getElementById('h-aeo');
  const selEeat = document.getElementById('h-eeat');
  const scoreTotalEl = document.getElementById('scorer-total');
  const scoreBadgeEl = document.getElementById('scorer-badge');
  const scoreActionsEl = document.getElementById('scorer-actions');
  const applyBtn = document.getElementById('apply-to-intake-btn');

  function calculateHeuristicScore() {
    if (!selRender || !scoreTotalEl) return;

    let score = 0;
    const actions = [];

    // 1. Render (20)
    if (selRender.value === 'ssr') score += 20;
    else if (selRender.value === 'hybrid') { score += 12; actions.push('Hydration optimization: reduce main-thread blocking JavaScript to avoid render queuing.'); }
    else { score += 4; actions.push('Critical: Migrate client-rendered routes to SSR/SSG to stop crawl budget abandonment.'); }

    // 2. CWV (18)
    if (selCwv.value === 'pass') score += 18;
    else if (selCwv.value === 'mixed') { score += 10; actions.push('Core Web Vitals: Audit INP long tasks (>50ms) on product templates.'); }
    else { score += 2; actions.push('Urgent CWV fix: INP/LCP failing field criteria; ranks at immediate risk in Core Updates.'); }

    // 3. Schema (18)
    if (selSchema.value === 'graph') score += 18;
    else if (selSchema.value === 'basic') { score += 10; actions.push('Schema enhancement: Nest entity relationships (sameAs, publisher, reviewedBy, mentions).'); }
    else { score += 2; actions.push('Structured data deficit: Inject connected JSON-LD graphs to secure Knowledge Graph entity status.'); }

    // 4. URLs (16)
    if (selUrls.value === 'clean') score += 16;
    else if (selUrls.value === 'moderate') { score += 8; actions.push('Faceted navigation: Enforce robots meta noindex or canonical pruning on filter combinations.'); }
    else { score += 2; actions.push('Crawl bloat emergency: High parameter explosion consuming crawler quota; implement directory 301 consolidation.'); }

    // 5. AEO (14)
    if (selAeo.value === 'ready') score += 14;
    else if (selAeo.value === 'partial') { score += 8; actions.push('AEO structure: Reformat top informational pages into 40-word direct semantic answer blocks.'); }
    else { score += 2; actions.push('AI search invisible: Deploy /llms.txt and structure Entity-Attribute-Value tables for LLM citation.'); }

    // 6. E-E-A-T (14)
    if (selEeat.value === 'high') score += 14;
    else if (selEeat.value === 'moderate') { score += 8; actions.push('E-E-A-T boost: Add verified expert reviewer profiles and original research datasets.'); }
    else { score += 2; actions.push('Severe E-E-A-T vulnerability: Anonymous or thin content carries acute Google Helpful Content / Core drop risk.'); }

    scoreTotalEl.innerHTML = `${score}<span style="font-size:1.2rem;color:var(--text-muted);font-weight:600;">/100</span>`;

    if (score >= 80) {
      scoreBadgeEl.innerHTML = '<span class="badge badge-success" style="font-size:0.9rem;padding:0.4rem 0.85rem;">STABLE &amp; RESILIENT</span>';
      scoreTotalEl.style.color = '#10b981';
    } else if (score >= 55) {
      scoreBadgeEl.innerHTML = '<span class="badge" style="background:#f59e0b;color:#1e1b2e;font-size:0.9rem;padding:0.4rem 0.85rem;">MODERATE VULNERABILITY</span>';
      scoreTotalEl.style.color = '#f59e0b';
    } else {
      scoreBadgeEl.innerHTML = '<span class="badge badge-error" style="font-size:0.9rem;padding:0.4rem 0.85rem;">HIGH PENALTY EXPOSURE</span>';
      scoreTotalEl.style.color = '#ef4444';
    }

    if (scoreActionsEl) {
      if (actions.length === 0) {
        scoreActionsEl.innerHTML = '<div style="background:var(--surface);padding:0.75rem 1rem;border-radius:8px;border:1px solid var(--line);font-size:0.88rem;color:#10b981;">✓ Platform architecture is clean. Focus on competitive citation expansion.</div>';
      } else {
        scoreActionsEl.innerHTML = actions.slice(0, 3).map((act, i) => `
          <div style="background:var(--surface);padding:0.75rem 1rem;border-radius:8px;border:1px solid var(--line);font-size:0.88rem;display:flex;align-items:flex-start;gap:0.6rem;">
            <span style="font-weight:800;color:var(--primary);">P${i + 1}</span>
            <span>${act}</span>
          </div>
        `).join('');
      }
    }

    return { score, actions };
  }

  const selectList = [selRender, selCwv, selSchema, selUrls, selAeo, selEeat];
  selectList.forEach(s => {
    if (s) s.addEventListener('change', calculateHeuristicScore);
  });
  calculateHeuristicScore();

  if (applyBtn) {
    applyBtn.addEventListener('click', () => {
      const res = calculateHeuristicScore();
      const notesEl = document.getElementById('audit-notes');
      if (notesEl && res) {
        notesEl.value = `Heuristic Score: ${res.score}/100. Priorities: ${res.actions.slice(0, 2).join(' ')}`;
      }

      // Auto-suggest symptom in Step 2
      if (selUrls && selUrls.value === 'severe') {
        const r = form.querySelector('input[name="symptom"][value="Indexation & Crawl Bloat"]');
        if (r) r.checked = true;
      } else if (selEeat && selEeat.value === 'low') {
        const r = form.querySelector('input[name="symptom"][value="Google Core Update Drop"]');
        if (r) r.checked = true;
      } else if (selAeo && selAeo.value === 'unready') {
        const r = form.querySelector('input[name="symptom"][value="AI Overview Zero-Click Loss"]');
        if (r) r.checked = true;
      }

      applyBtn.textContent = '✓ Applied to Wizard Above!';
      form.scrollIntoView({ behavior: 'smooth' });
      setTimeout(() => { applyBtn.textContent = 'Pre-fill Diagnostic Wizard Above ↑'; }, 2500);
    });
  }
});

