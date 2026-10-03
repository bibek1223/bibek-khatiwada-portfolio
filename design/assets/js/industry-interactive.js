/**
 * Interactive modules for Industry detail pages (/industries/[slug]/)
 * 1. home-services-hvac-plumbing: SAB Geo-Radius & Citation Integrity Model
 * 2. b2b-saas: SaaS Organic Pipeline & Payback Multiple Calculator
 * 3. programmatic-directories: Programmatic Indexation & Thin-URL Risk Calculator
 * 4. healthcare-ymyl: Medical & Legal YMYL E-E-A-T Quality Checklist & Scorecard
 */
document.addEventListener('DOMContentLoaded', () => {
  // 1. SAB Geo-Radius Calculator (home-services-hvac-plumbing)
  const sabRadius = document.getElementById('sab-radius');
  const sabRadiusVal = document.getElementById('sab-radius-val');
  const sabLocations = document.getElementById('sab-locations');
  const sabReviews = document.getElementById('sab-reviews');
  const sabPackScore = document.getElementById('sab-pack-score');
  const sabPagesNeeded = document.getElementById('sab-pages-needed');
  const sabRiskBadge = document.getElementById('sab-risk-badge');

  function updateSabModel() {
    if (!sabRadius || !sabPackScore) return;
    const radius = parseInt(sabRadius.value, 10) || 15;
    const submarkets = parseInt(sabLocations.value, 10) || 4;
    const reviews = parseInt(sabReviews.value, 10) || 75;

    if (sabRadiusVal) sabRadiusVal.textContent = `${radius} miles`;
    if (sabPagesNeeded) sabPagesNeeded.textContent = `${submarkets * 3} landing pages`;

    // Local pack authority index: based on review density vs radius strain
    let authority = Math.round((reviews / (radius * 1.5)) * 10);
    authority = Math.min(98, Math.max(20, authority));
    sabPackScore.textContent = `${authority}/100`;

    if (sabRiskBadge) {
      if (radius > 30) {
        sabRiskBadge.innerHTML = '<span class="badge badge-error">HIGH PROXIMITY PENALTY RISK</span>';
        sabPackScore.style.color = '#ef4444';
      } else if (radius > 18) {
        sabRiskBadge.innerHTML = '<span class="badge" style="background:#f59e0b;color:#1e1b2e;">MODERATE EXPANSION BOUNDARY</span>';
        sabPackScore.style.color = '#f59e0b';
      } else {
        sabRiskBadge.innerHTML = '<span class="badge badge-success">OPTIMAL PACK PROXIMITY</span>';
        sabPackScore.style.color = '#10b981';
      }
    }
  }

  [sabRadius, sabLocations, sabReviews].forEach(el => {
    if (el) el.addEventListener('input', updateSabModel);
  });
  updateSabModel();

  // 2. SaaS Organic Pipeline & Payback Model (b2b-saas)
  const saasAcv = document.getElementById('saas-acv');
  const saasTraffic = document.getElementById('saas-traffic');
  const saasTrafficVal = document.getElementById('saas-traffic-val');
  const saasCvr = document.getElementById('saas-cvr');
  const saasPipeline = document.getElementById('saas-pipeline');
  const saasAdEquivalent = document.getElementById('saas-ad-equiv');

  function updateSaasModel() {
    if (!saasAcv || !saasPipeline) return;
    const acv = parseFloat(saasAcv.value) || 18000;
    const traffic = parseInt(saasTraffic.value, 10) || 3500;
    const cvr = (parseFloat(saasCvr.value) || 1.5) / 100;

    if (saasTrafficVal) saasTrafficVal.textContent = traffic.toLocaleString();

    const monthlyDemos = traffic * cvr;
    const closeRate = 0.22; // verified 22% demo-to-close benchmark
    const monthlyWonDeals = monthlyDemos * closeRate;
    const annualPipeline = Math.round(monthlyWonDeals * acv * 12);
    const googleAdsCpc = 14.50; // benchmark enterprise B2B SaaS CPC
    const monthlyAdEquiv = Math.round(traffic * googleAdsCpc);

    saasPipeline.textContent = `$${annualPipeline.toLocaleString()}`;
    if (saasAdEquivalent) saasAdEquivalent.textContent = `$${monthlyAdEquiv.toLocaleString()}/mo`;
  }

  [saasAcv, saasTraffic, saasCvr].forEach(el => {
    if (el) el.addEventListener('input', updateSaasModel);
  });
  updateSaasModel();

  // 3. Programmatic Thin-Risk Calculator (programmatic-directories)
  const progUrls = document.getElementById('prog-urls');
  const progUrlsVal = document.getElementById('prog-urls-val');
  const progWords = document.getElementById('prog-words');
  const progLinks = document.getElementById('prog-links');
  const progRiskScore = document.getElementById('prog-risk-score');
  const progBadge = document.getElementById('prog-badge');

  function updateProgModel() {
    if (!progUrls || !progRiskScore) return;
    const urls = parseInt(progUrls.value, 10) || 50000;
    const words = parseInt(progWords.value, 10) || 280;
    const links = parseInt(progLinks.value, 10) || 5;

    if (progUrlsVal) progUrlsVal.textContent = urls.toLocaleString();

    let risk = 50;
    if (words < 150) risk += 35;
    else if (words < 300) risk += 15;
    else risk -= 20;

    if (links < 3) risk += 20;
    else if (links > 8) risk -= 15;

    if (urls > 100000) risk += 15;

    risk = Math.min(99, Math.max(10, risk));
    progRiskScore.textContent = `${risk}% Risk`;

    if (progBadge) {
      if (risk >= 65) {
        progBadge.innerHTML = '<span class="badge badge-error">HIGH DE-INDEXATION RISK</span>';
        progRiskScore.style.color = '#ef4444';
      } else if (risk >= 40) {
        progBadge.innerHTML = '<span class="badge" style="background:#f59e0b;color:#1e1b2e;">MODERATE THIN CONTENT DRIFT</span>';
        progRiskScore.style.color = '#f59e0b';
      } else {
        progBadge.innerHTML = '<span class="badge badge-success">HEALTHY TAXONOMY DEPTH</span>';
        progRiskScore.style.color = '#10b981';
      }
    }
  }

  [progUrls, progWords, progLinks].forEach(el => {
    if (el) el.addEventListener('input', updateProgModel);
  });
  updateProgModel();

  // 4. Healthcare YMYL E-E-A-T Scorecard (healthcare-ymyl)
  const checks = document.querySelectorAll('.ymyl-check');
  const ymylTotal = document.getElementById('ymyl-score');
  const ymylBadge = document.getElementById('ymyl-badge');

  function updateYmylScore() {
    if (!ymylTotal) return;
    let checkedCount = 0;
    checks.forEach(c => {
      if (c.checked) checkedCount++;
    });

    const score = Math.round((checkedCount / Math.max(1, checks.length)) * 100);
    ymylTotal.innerHTML = `${score}<span style="font-size:1.1rem;color:var(--text-muted);font-weight:600;">/100</span>`;

    if (ymylBadge) {
      if (score >= 80) {
        ymylBadge.innerHTML = '<span class="badge badge-success">CLINICALLY VERIFIED E-E-A-T</span>';
        ymylTotal.style.color = '#10b981';
      } else if (score >= 50) {
        ymylBadge.innerHTML = '<span class="badge" style="background:#f59e0b;color:#1e1b2e;">PARTIAL COMPLIANCE (CORE VULNERABLE)</span>';
        ymylTotal.style.color = '#f59e0b';
      } else {
        ymylBadge.innerHTML = '<span class="badge badge-error">CRITICAL YMYL RISK</span>';
        ymylTotal.style.color = '#ef4444';
      }
    }
  }

  checks.forEach(c => c.addEventListener('change', updateYmylScore));
  updateYmylScore();
});
