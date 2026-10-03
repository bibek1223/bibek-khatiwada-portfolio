(function () {
  "use strict";

  var presets = {
    saas: { searches: 25000, currentCtr: 1.6, targetCtr: 4.2, convRate: 2.2, avgValue: 1200, label: "Avg Customer Annual Contract Value (ACV)" },
    ecommerce: { searches: 90000, currentCtr: 1.2, targetCtr: 3.4, convRate: 1.8, avgValue: 85, label: "Average Order Value (AOV)" },
    local: { searches: 8500, currentCtr: 2.4, targetCtr: 6.8, convRate: 5.2, avgValue: 480, label: "Average Job / Invoice Value" },
    health: { searches: 65000, currentCtr: 1.4, targetCtr: 3.6, convRate: 2.0, avgValue: 350, label: "Average Patient / Intake Value" }
  };

  var inputVolume = document.getElementById("input-volume");
  var inputCurrentCtr = document.getElementById("input-current-ctr");
  var inputTargetCtr = document.getElementById("input-target-ctr");
  var inputConvRate = document.getElementById("input-conv-rate");
  var inputAvgValue = document.getElementById("input-avg-value");
  var labelAvgValue = document.getElementById("label-avg-value");

  var valVolume = document.getElementById("val-volume");
  var valCurrentCtr = document.getElementById("val-current-ctr");
  var valTargetCtr = document.getElementById("val-target-ctr");
  var valConvRate = document.getElementById("val-conv-rate");
  var valAvgValue = document.getElementById("val-avg-value");

  var outMonthlyRev = document.getElementById("out-monthly-rev");
  var outAnnualRev = document.getElementById("out-annual-rev");
  var outMonthlyClicks = document.getElementById("out-monthly-clicks");
  var outMonthlyConversions = document.getElementById("out-monthly-conversions");
  var outPaybackText = document.getElementById("out-payback-text");
  var roiCtaBtn = document.getElementById("roi-cta-btn");
  var roiCopyBtn = document.getElementById("roi-copy-btn");

  if (!inputVolume) return;

  function fmtMoney(num) {
    return "$" + Math.round(num).toLocaleString();
  }

  function recalculate() {
    var vol = parseFloat(inputVolume.value);
    var cCtr = parseFloat(inputCurrentCtr.value) / 100;
    var tCtr = parseFloat(inputTargetCtr.value) / 100;
    var cRate = parseFloat(inputConvRate.value) / 100;
    var val = parseFloat(inputAvgValue.value);

    valVolume.textContent = Math.round(vol).toLocaleString();
    valCurrentCtr.textContent = (cCtr * 100).toFixed(1) + "%";
    valTargetCtr.textContent = (tCtr * 100).toFixed(1) + "%";
    valConvRate.textContent = (cRate * 100).toFixed(1) + "%";
    valAvgValue.textContent = "$" + Math.round(val).toLocaleString();

    var currentClicks = vol * cCtr;
    var targetClicks = vol * tCtr;
    var netClicks = Math.max(0, targetClicks - currentClicks);
    var netConversions = netClicks * cRate;
    var monthlyRev = netConversions * val;
    var annualRev = monthlyRev * 12;

    outMonthlyClicks.textContent = "+" + Math.round(netClicks).toLocaleString() + " clicks/mo";
    outMonthlyConversions.textContent = "+" + Math.round(netConversions).toLocaleString() + " leads/mo";
    outMonthlyRev.textContent = fmtMoney(monthlyRev);
    outAnnualRev.textContent = "+" + fmtMoney(annualRev) + " annualized revenue pipeline";

    var estRetainerCost = 3500;
    var paybackMonths = monthlyRev > 0 ? (estRetainerCost / monthlyRev).toFixed(1) : "N/A";
    outPaybackText.innerHTML = "At this scale, a typical technical systems sprint pays for itself within <strong>" + paybackMonths + " months</strong> of rankings stabilization.";

    var msg = encodeURIComponent(
      "Hi Bibek, I modeled our search ROI: " + Math.round(vol).toLocaleString() +
      " monthly searches, target CTR " + (tCtr * 100).toFixed(1) +
      "%, projecting +" + fmtMoney(monthlyRev) + "/mo in pipeline. Let's discuss."
    );
    roiCtaBtn.href = "{{root}}contact/?ref=roi-calc&notes=" + msg;
  }

  var presetBtns = document.querySelectorAll(".preset-btn");
  presetBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      presetBtns.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      var p = presets[btn.dataset.preset];
      if (p) {
        inputVolume.value = p.searches;
        inputCurrentCtr.value = p.currentCtr;
        inputTargetCtr.value = p.targetCtr;
        inputConvRate.value = p.convRate;
        inputAvgValue.value = p.avgValue;
        labelAvgValue.textContent = p.label;
        recalculate();
      }
    });
  });

  [inputVolume, inputCurrentCtr, inputTargetCtr, inputConvRate, inputAvgValue].forEach(function (el) {
    el.addEventListener("input", recalculate);
  });

  if (roiCopyBtn) {
    roiCopyBtn.addEventListener("click", function () {
      var summaryText = "Organic SEO ROI Forecast:\n" +
        "• Addressable Demand: " + valVolume.textContent + " searches/mo\n" +
        "• CTR Shift: " + valCurrentCtr.textContent + " → " + valTargetCtr.textContent + "\n" +
        "• Incremental Clicks: " + outMonthlyClicks.textContent + "\n" +
        "• Incremental Pipeline: " + outMonthlyRev.textContent + "/mo (" + outAnnualRev.textContent + ")\n" +
        "• Modeled via bibek-khatiwada.com.np/roi-calculator/";

      navigator.clipboard.writeText(summaryText).then(function () {
        var prev = roiCopyBtn.textContent;
        roiCopyBtn.textContent = "✓ Forecast Copied!";
        setTimeout(function () { roiCopyBtn.textContent = prev; }, 2200);
      });
    });
  }

  recalculate();
})();
