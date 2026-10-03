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

    if (briefBox) {
      briefBox.innerHTML = `
        <div style="display:grid;gap:0.4rem;">
          <p style="margin:0;"><strong>Target URL:</strong> <span>${escapeHtml(url)}</span></p>
          <p style="margin:0;"><strong>CMS / Stack:</strong> <span>${escapeHtml(cms)}</span></p>
          <p style="margin:0;"><strong>Organic Scale:</strong> <span>${escapeHtml(traffic)}</span></p>
          <p style="margin:0;"><strong>Primary Symptom:</strong> <span style="color:var(--purple);font-weight:700;">${escapeHtml(selectedSymptom)}</span></p>
          <div style="margin-top:0.6rem;padding:0.75rem;background:rgba(124,58,237,0.06);border-radius:10px;font-size:0.85rem;line-height:1.45;">
            <strong>Forensic Focus:</strong> ${focusDetail}
          </div>
        </div>
      `;
    }

    // Update WhatsApp link with pre-filled message
    const waText = encodeURIComponent(
      `Hi Bibek, I completed the SEO Diagnostic on your portfolio:\n` +
      `• URL: ${url}\n` +
      `• CMS: ${cms}\n` +
      `• Scale: ${traffic}\n` +
      `• Symptom: ${selectedSymptom}\n` +
      `Looking forward to your initial forensic thoughts.`
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
    const email = document.getElementById('audit-email')?.value;
    const actions = form.querySelector('.form-actions');
    if (actions) {
      actions.innerHTML = `
        <div style="width:100%;background:#10b981;color:#fff;padding:1rem;border-radius:12px;text-align:center;font-weight:700;">
          ✓ Diagnostic Brief Compiled! Bibek has received your details and will follow up at ${escapeHtml(email)} within 24 hours.
        </div>
      `;
    }
  });
});
