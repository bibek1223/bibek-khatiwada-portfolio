/* Shared behaviour for every page: mobile nav, number count-up, copy buttons,
   disclosure lists (timeline), footer year. No dependencies. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function initNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("site-nav");
    if (!toggle || !nav) return;

    function setOpen(open) {
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("open", open);
    }
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        setOpen(false);
        toggle.focus();
      }
    });
    window.matchMedia("(min-width: 1041px)").addEventListener("change", function (mq) {
      if (mq.matches) setOpen(false);
    });
  }

  // Animates "21.2M+", "+74%", "3+ Years", "7.3" from zero, keeping prefix,
  // suffix and decimal places exactly as authored.
  function countUp(el) {
    var text = el.textContent.trim();
    var m = text.match(/^([^\d]*)(\d+(?:\.\d+)?)(.*)$/);
    if (!m) return;
    var target = parseFloat(m[2]);
    var decimals = (m[2].split(".")[1] || "").length;
    var start = null;
    var duration = 1100;
    function frame(t) {
      if (start === null) start = t;
      var p = Math.min((t - start) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = m[1] + (target * eased).toFixed(decimals) + m[3];
      if (p < 1) requestAnimationFrame(frame);
      else el.textContent = text;
    }
    requestAnimationFrame(frame);
  }

  function initCounters() {
    var els = document.querySelectorAll("[data-count]");
    if (!els.length || reduceMotion || !("IntersectionObserver" in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        countUp(entry.target);
      });
    }, { threshold: 0.6 });
    els.forEach(function (el) { io.observe(el); });
  }

  function initCopy() {
    document.querySelectorAll("[data-copy]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var label = btn.textContent;
        function done(ok) {
          btn.textContent = ok ? "Copied" : "Press Ctrl+C";
          btn.classList.toggle("is-done", ok);
          setTimeout(function () { btn.textContent = label; btn.classList.remove("is-done"); }, 1800);
        }
        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(btn.getAttribute("data-copy")).then(function () { done(true); }, function () { done(false); });
        } else {
          done(false);
        }
      });
    });
  }

  // Timeline: button[aria-expanded] toggles the element named in aria-controls.
  function initDisclosures() {
    document.querySelectorAll("[data-accordion] [aria-controls]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var open = btn.getAttribute("aria-expanded") !== "true";
        btn.setAttribute("aria-expanded", String(open));
        document.getElementById(btn.getAttribute("aria-controls")).hidden = !open;
      });
    });
  }

  function initYear() {
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = String(new Date().getFullYear());
    });
  }

  initNav();
  initCounters();
  initCopy();
  initDisclosures();
  initYear();
})();
