/**
 * Interactive modules for Framework detail pages (/frameworks/[slug]/)
 * 1. llm-tracking: Citation Share of Voice (C-SoV) Calculator
 * 2. entity-attribute-value-search: Live EAV JSON-LD Schema Generator
 * 3. aeo-geo-playbook: 40-Word Semantic Answer Chunk Scorer
 * 4. 130k-page-ymyl-recovery-mechanics: Crawl Budget & 301 Pruning Simulator
 */
document.addEventListener('DOMContentLoaded', () => {
  // 1. C-SoV Calculator (llm-tracking)
  const csovPrompts = document.getElementById('csov-prompts');
  const csovBrand = document.getElementById('csov-brand');
  const csovCompA = document.getElementById('csov-comp-a');
  const csovCompB = document.getElementById('csov-comp-b');
  const csovCitRate = document.getElementById('csov-cit-rate');
  const csovShareRate = document.getElementById('csov-share-rate');
  const csovVerdict = document.getElementById('csov-verdict');

  function updateCsov() {
    if (!csovPrompts || !csovBrand || !csovCompA || !csovCompB) return;
    const prompts = Math.max(1, parseInt(csovPrompts.value, 10) || 50);
    const brand = Math.max(0, parseInt(csovBrand.value, 10) || 0);
    const compA = Math.max(0, parseInt(csovCompA.value, 10) || 0);
    const compB = Math.max(0, parseInt(csovCompB.value, 10) || 0);

    const totalCitations = brand + compA + compB;
    const citRate = ((brand / prompts) * 100).toFixed(1);
    const sovRate = totalCitations > 0 ? ((brand / totalCitations) * 100).toFixed(1) : '0.0';

    if (csovCitRate) csovCitRate.textContent = `${citRate}%`;
    if (csovShareRate) csovShareRate.textContent = `${sovRate}%`;

    if (csovVerdict) {
      if (parseFloat(sovRate) >= 45) {
        csovVerdict.innerHTML = '<span class="badge badge-success">CATEGORY LEADER (DOMINANT)</span>';
      } else if (parseFloat(sovRate) >= 25) {
        csovVerdict.innerHTML = '<span class="badge" style="background:#f59e0b;color:#1e1b2e;">CONTESTED VISIBILITY</span>';
      } else {
        csovVerdict.innerHTML = '<span class="badge badge-error">UNDER-REPRESENTED / AT RISK</span>';
      }
    }
  }

  [csovPrompts, csovBrand, csovCompA, csovCompB].forEach(el => {
    if (el) el.addEventListener('input', updateCsov);
  });
  updateCsov();

  // 2. EAV Schema Generator (entity-attribute-value-search)
  const eavSubj = document.getElementById('eav-subject');
  const eavAttr1 = document.getElementById('eav-attr1');
  const eavAttr2 = document.getElementById('eav-attr2');
  const eavOutput = document.getElementById('eav-json-output');
  const copyEavBtn = document.getElementById('copy-eav-btn');

  function updateEavSchema() {
    if (!eavOutput) return;
    const subj = (eavSubj && eavSubj.value.trim()) || 'Target Entity';
    const a1Raw = (eavAttr1 && eavAttr1.value.trim()) || 'attribute1 : value1';
    const a2Raw = (eavAttr2 && eavAttr2.value.trim()) || 'attribute2 : value2';

    const parsePair = (str) => {
      const parts = str.split(':');
      return {
        prop: parts[0] ? parts[0].trim().replace(/[^a-zA-Z0-9_]/g, '') : 'property',
        val: parts.slice(1).join(':').trim() || 'value'
      };
    };

    const p1 = parsePair(a1Raw);
    const p2 = parsePair(a2Raw);

    const schema = {
      "@context": "https://schema.org",
      "@type": "Thing",
      "name": subj,
      "additionalProperty": [
        {
          "@type": "PropertyValue",
          "name": p1.prop,
          "value": p1.val
        },
        {
          "@type": "PropertyValue",
          "name": p2.prop,
          "value": p2.val
        }
      ],
      "disambiguatingDescription": `Machine-readable EAV semantic model verified by Bibek Khatiwada architecture suite.`
    };

    eavOutput.textContent = JSON.stringify(schema, null, 2);
  }

  [eavSubj, eavAttr1, eavAttr2].forEach(el => {
    if (el) el.addEventListener('input', updateEavSchema);
  });
  updateEavSchema();

  if (copyEavBtn && eavOutput) {
    copyEavBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(eavOutput.textContent).then(() => {
        const orig = copyEavBtn.textContent;
        copyEavBtn.textContent = 'Copied!';
        setTimeout(() => { copyEavBtn.textContent = orig; }, 1800);
      });
    });
  }

  // 3. AEO 40-Word Chunk Scorer (aeo-geo-playbook)
  const aeoInput = document.getElementById('aeo-text');
  const aeoWords = document.getElementById('aeo-words');
  const aeoDef = document.getElementById('aeo-def-detected');
  const aeoScore = document.getElementById('aeo-score');

  function updateAeoScorer() {
    if (!aeoInput || !aeoWords || !aeoScore) return;
    const text = aeoInput.value.trim();
    const words = text ? text.split(/\s+/).filter(Boolean) : [];
    const count = words.length;

    aeoWords.textContent = `${count} words`;

    // Detect direct definition keywords: "is", "refers to", "defined as", "measured in"
    const lower = text.toLowerCase();
    const hasDef = /\b(is|refers to|defined as|measures|measured in|consists of)\b/.test(lower);
    if (aeoDef) {
      aeoDef.textContent = hasDef ? 'Detected ✓' : 'Weak / Missing ✗';
      aeoDef.style.color = hasDef ? 'var(--primary)' : '#ef4444';
    }

    // Optimal chunk: 35-52 words with definition
    let score = 50;
    if (count >= 30 && count <= 55) score += 35;
    else if (count >= 20 && count <= 70) score += 18;
    else score -= 15;

    if (hasDef) score += 15;
    if (text.includes('.') && text.indexOf('.') < text.length - 1) score += 5; // multi-sentence cadence

    score = Math.min(99, Math.max(15, score));
    aeoScore.textContent = `${score}% (${score >= 80 ? 'Optimal' : score >= 60 ? 'Moderate' : 'Needs Polish'})`;
    aeoScore.style.color = score >= 80 ? '#10b981' : score >= 60 ? '#f59e0b' : '#ef4444';
  }

  if (aeoInput) {
    aeoInput.addEventListener('input', updateAeoScorer);
    updateAeoScorer();
  }

  // 4. Crawl Budget & 301 Pruning Simulator (130k-page-ymyl-recovery-mechanics)
  const pruneSlider = document.getElementById('prune-slider');
  const crawlSlider = document.getElementById('crawl-slider');
  const pruneCountVal = document.getElementById('prune-count-val');
  const crawlRateVal = document.getElementById('crawl-rate-val');
  const pruneDaysSaved = document.getElementById('prune-days-saved');
  const pruneWastePct = document.getElementById('prune-waste-pct');

  function updatePruningSim() {
    if (!pruneSlider || !crawlSlider || !pruneDaysSaved || !pruneWastePct) return;
    const pruned = parseInt(pruneSlider.value, 10) || 20000;
    const crawlRate = parseInt(crawlSlider.value, 10) || 4500;
    const totalPages = 130000;

    if (pruneCountVal) pruneCountVal.textContent = pruned.toLocaleString();
    if (crawlRateVal) crawlRateVal.textContent = `${crawlRate.toLocaleString()}/day`;

    const remainingPages = Math.max(10000, totalPages - pruned);
    const origDays = (totalPages / crawlRate);
    const newDays = (remainingPages / crawlRate);
    const daysSaved = origDays - newDays;
    const wastePct = ((pruned / totalPages) * 100).toFixed(1);

    pruneWastePct.textContent = `${wastePct}%`;
    pruneDaysSaved.innerHTML = `${newDays.toFixed(1)} days <span style="font-size:0.85rem;color:#10b981;font-weight:600;">(${daysSaved.toFixed(1)} days faster)</span>`;
  }

  [pruneSlider, crawlSlider].forEach(el => {
    if (el) el.addEventListener('input', updatePruningSim);
  });
  updatePruningSim();
});
