(function () {
  "use strict";

  var phaseBtns = document.querySelectorAll(".stepper-tab");
  var phasePanels = document.querySelectorAll(".stepper-panel");

  if (phaseBtns.length === 0 || phasePanels.length === 0) return;

  phaseBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var targetPhase = btn.dataset.phase;

      phaseBtns.forEach(function (b) {
        b.classList.remove("active");
        b.setAttribute("aria-selected", "false");
      });
      btn.classList.add("active");
      btn.setAttribute("aria-selected", "true");

      phasePanels.forEach(function (panel) {
        var isTarget = panel.dataset.phase === targetPhase;
        panel.hidden = !isTarget;
        if (isTarget) {
          panel.style.opacity = "0";
          setTimeout(function () { panel.style.opacity = "1"; }, 50);
        }
      });
    });
  });
})();
