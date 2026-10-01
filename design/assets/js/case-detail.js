/* Case-study detail page: reading progress, active table-of-contents link,
   and the totals / monthly-average toggle on the results panel. */
(function () {
  "use strict";

  function compact(n) {
    var units = [[1e9, "B"], [1e6, "M"], [1e3, "K"]];
    for (var i = 0; i < units.length; i++) {
      if (n >= units[i][0]) {
        var v = n / units[i][0];
        return (v >= 100 ? v.toFixed(0) : v >= 10 ? v.toFixed(1) : v.toFixed(2)).replace(/\.?0+$/, "") + units[i][1];
      }
    }
    return String(Math.round(n));
  }

  function initProgress() {
    var bar = document.querySelector(".progress i");
    var article = document.querySelector(".cs-main");
    if (!bar || !article) return;
    var ticking = false;
    function update() {
      var rect = article.getBoundingClientRect();
      var total = rect.height - window.innerHeight * 0.6;
      var p = total > 0 ? Math.min(Math.max(-rect.top / total, 0), 1) : 1;
      bar.style.transform = "scaleX(" + p + ")";
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  function initToc() {
    var links = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
    if (!links.length || !("IntersectionObserver" in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (a) {
          a.classList.toggle("is-active", a.getAttribute("href") === "#" + entry.target.id);
        });
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    links.forEach(function (a) {
      var target = document.querySelector(a.getAttribute("href"));
      if (target) io.observe(target);
    });
  }

  function initResultsToggle() {
    var group = document.querySelector(".res-toggle");
    if (!group) return;
    var buttons = group.querySelectorAll("button");
    var values = document.querySelectorAll("[data-total]");
    var labels = document.querySelectorAll("[data-label]");
    values.forEach(function (v) { v.setAttribute("data-orig", v.textContent); });
    labels.forEach(function (l) { l.setAttribute("data-orig", l.textContent); });

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var monthly = btn.getAttribute("data-mode") === "monthly";
        buttons.forEach(function (b) { b.setAttribute("aria-pressed", String(b === btn)); });
        values.forEach(function (v) {
          v.textContent = monthly ? compact(+v.getAttribute("data-monthly")) : v.getAttribute("data-orig");
        });
        labels.forEach(function (l) {
          l.textContent = monthly ? "Average per month" : l.getAttribute("data-orig");
        });
      });
    });
  }

  initProgress();
  initToc();
  initResultsToggle();
})();
