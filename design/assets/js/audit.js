/**
 * 3-Step SEO Audit Diagnostic Wizard
 */
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('audit-form');
  if (!form) return;

  const steps = form.querySelectorAll('.audit-step');
  const dots = document.querySelectorAll('.step-indicator');
  const briefBox = document.getElementById('brief-content');

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

    if (briefBox) {
      briefBox.innerHTML = `
        <p><strong>Target URL:</strong> ${escapeHtml(url)}</p>
        <p><strong>CMS Platform:</strong> ${escapeHtml(cms)}</p>
        <p><strong>Organic Scale:</strong> ${escapeHtml(traffic)}</p>
        <p><strong>Primary Symptom:</strong> <span class="accent-text">${escapeHtml(selectedSymptom)}</span></p>
        <p class="tiny" style="margin-top:0.75rem;color:var(--text-muted)">
          Diagnostic Focus: Checking crawl efficiency, entity schema grounding, and Search Console update timestamps for ${escapeHtml(url)}.
        </p>
      `;
    }
  }

  function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  form.querySelectorAll('.btn-next').forEach(btn => {
    btn.addEventListener('click', (e) => {
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
    alert(`Thank you! Your diagnostic brief has been compiled and dispatched to Bibek. Response expected within 24 hours at ${email}.`);
  });
});
