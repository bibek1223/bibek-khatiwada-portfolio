/**
 * Interactive modules for the LLM Tracking Blog Post:
 * 1. Citation Share of Voice (C-SoV) & Revenue Simulator
 * 2. SERP vs. AI Overview vs. LLM Citation Diff Viewer
 * 3. Copy Code buttons for technical code snippets
 */
document.addEventListener('DOMContentLoaded', function () {
  'use strict';

  // 1. LLM Visibility & Revenue Simulator
  function initSimulator() {
    var qInput = document.getElementById('sim-queries');
    var triggerInput = document.getElementById('sim-trigger');
    var csovInput = document.getElementById('sim-csov');
    var targetInput = document.getElementById('sim-target');
    var acvInput = document.getElementById('sim-acv');
    var convInput = document.getElementById('sim-conv');

    if (!qInput || !triggerInput || !csovInput || !targetInput || !acvInput || !convInput) return;

    var qVal = document.getElementById('val-queries');
    var triggerVal = document.getElementById('val-trigger');
    var csovVal = document.getElementById('val-csov');
    var targetVal = document.getElementById('val-target');
    var acvVal = document.getElementById('val-acv');
    var convVal = document.getElementById('val-conv');

    var outTriggered = document.getElementById('out-triggered-answers');
    var outCurrentCites = document.getElementById('out-current-cites');
    var outTargetCites = document.getElementById('out-target-cites');
    var outNewLeads = document.getElementById('out-monthly-leads');
    var outAnnualRev = document.getElementById('out-annual-revenue');

    function fmt(n) {
      return Math.round(n).toLocaleString();
    }

    function fmtMoney(n) {
      return '$' + Math.round(n).toLocaleString();
    }

    function calculate() {
      var queries = parseFloat(qInput.value) || 0;
      var triggerPct = (parseFloat(triggerInput.value) || 0) / 100;
      var csovPct = (parseFloat(csovInput.value) || 0) / 100;
      var targetPct = (parseFloat(targetInput.value) || 0) / 100;
      var acv = parseFloat(acvInput.value) || 0;
      var convPct = (parseFloat(convInput.value) || 0) / 100;

      // Update slider readout values
      qVal.textContent = fmt(queries);
      triggerVal.textContent = Math.round(triggerPct * 100) + '%';
      csovVal.textContent = Math.round(csovPct * 100) + '%';
      targetVal.textContent = Math.round(targetPct * 100) + '%';
      acvVal.textContent = fmtMoney(acv);
      convVal.textContent = (convPct * 100).toFixed(1) + '%';

      // Mathematical projections
      var totalAiAnswers = queries * triggerPct;
      var currentCitations = totalAiAnswers * csovPct;
      var targetCitations = totalAiAnswers * targetPct;
      var citationDelta = Math.max(0, targetCitations - currentCitations);
      
      // Estimated referral visits & assisted conversions
      // Conservative model: each citation captures ~8% referral click-through from interested readers
      var referralVisitsGained = citationDelta * 0.08;
      var monthlyLeadsGained = referralVisitsGained * convPct;
      var monthlyRevenueGained = monthlyLeadsGained * acv;
      var annualRevenueGained = monthlyRevenueGained * 12;

      if (outTriggered) outTriggered.textContent = fmt(totalAiAnswers);
      if (outCurrentCites) outCurrentCites.textContent = fmt(currentCitations);
      if (outTargetCites) outTargetCites.textContent = fmt(targetCitations);
      if (outNewLeads) outNewLeads.textContent = '+' + fmt(monthlyLeadsGained) + ' / mo';
      if (outAnnualRev) outAnnualRev.textContent = fmtMoney(annualRevenueGained);
    }

    // Preset Buttons
    var presetBtns = document.querySelectorAll('.sim-preset-btn');
    var presets = {
      b2b: { queries: 25000, trigger: 55, csov: 12, target: 45, acv: 2800, conv: 3.2 },
      hvac: { queries: 40000, trigger: 35, csov: 5, target: 30, acv: 850, conv: 6.5 },
      ecom: { queries: 85000, trigger: 40, csov: 8, target: 35, acv: 95, conv: 2.8 }
    };

    presetBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        presetBtns.forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        var p = presets[btn.dataset.preset];
        if (p) {
          qInput.value = p.queries;
          triggerInput.value = p.trigger;
          csovInput.value = p.csov;
          targetInput.value = p.target;
          acvInput.value = p.acv;
          convInput.value = p.conv;
          calculate();
        }
      });
    });

    [qInput, triggerInput, csovInput, targetInput, acvInput, convInput].forEach(function (inp) {
      inp.addEventListener('input', calculate);
    });

    calculate();
  }

  // 2. SERP vs. AI Overview vs. LLM Citation Diff Viewer
  function initDiffViewer() {
    var buttons = document.querySelectorAll('.diff-mode-btn');
    var views = document.querySelectorAll('.diff-view-panel');
    if (!buttons.length || !views.length) return;

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var mode = btn.dataset.mode;
        buttons.forEach(function (b) { b.classList.toggle('active', b === btn); });
        views.forEach(function (v) {
          v.hidden = (v.dataset.view !== mode);
        });
      });
    });
  }

  // 3. One-Click Copy Code
  function initCopyCode() {
    var codeBlocks = document.querySelectorAll('.cs-main pre');
    codeBlocks.forEach(function (block) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'copy-code-btn';
      btn.textContent = 'Copy Code';
      btn.setAttribute('aria-label', 'Copy code to clipboard');

      btn.addEventListener('click', function () {
        var code = block.querySelector('code');
        var text = code ? code.innerText : block.innerText;
        navigator.clipboard.writeText(text).then(function () {
          btn.textContent = 'Copied!';
          btn.classList.add('copied');
          setTimeout(function () {
            btn.textContent = 'Copy Code';
            btn.classList.remove('copied');
          }, 2000);
        }).catch(function () {
          btn.textContent = 'Failed';
        });
      });

      block.style.position = 'relative';
      block.appendChild(btn);
    });
  }

  initSimulator();
  initDiffViewer();
  initCopyCode();
});
