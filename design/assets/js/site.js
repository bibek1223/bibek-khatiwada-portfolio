/* Shared behaviour for every page: navigation, command search, automatic page
   outline, reading progress, number count-up, copy buttons and disclosures. */
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

  function initProgress() {
    var bar = document.querySelector(".site-progress i");
    if (!bar) return;
    function update() {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var value = max > 0 ? Math.min(window.scrollY / max, 1) : 0;
      bar.style.transform = "scaleX(" + value + ")";
    }
    update();
    document.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
  }

  function initSiteSearch() {
    var root = document.querySelector("[data-site-search]");
    var indexEl = root && root.querySelector("[data-search-index]");
    if (!root || !indexEl) return;
    var input = root.querySelector("[data-search-input]");
    var results = root.querySelector("[data-search-results]");
    var count = root.querySelector("[data-search-count]");
    var empty = root.querySelector("[data-search-empty]");
    var entries = JSON.parse(indexEl.textContent);
    var active = 0;
    var previousFocus = null;

    function normalize(value) {
      return value.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
    }
    function rank(entry, query) {
      if (!query) return entry.type === "page" || entry.type === "action" ? 10 : 2;
      var words = query.split(/\s+/);
      var title = normalize(entry.title);
      var text = title + " " + normalize(entry.description) + " " + normalize(entry.type);
      var score = 0;
      words.forEach(function (word) {
        if (title.indexOf(word) === 0) score += 8;
        else if (title.indexOf(word) > -1) score += 5;
        if (text.indexOf(word) > -1) score += 2;
        else score -= 20;
      });
      return score;
    }
    function render() {
      var query = normalize(input.value);
      var matches = entries.map(function (entry) { return { entry: entry, score: rank(entry, query) }; })
        .filter(function (item) { return item.score > 0; })
        .sort(function (a, b) { return b.score - a.score; }).slice(0, 9);
      active = Math.min(active, Math.max(matches.length - 1, 0));
      results.innerHTML = "";
      matches.forEach(function (item, i) {
        var link = document.createElement("a");
        link.href = item.entry.url;
        link.className = "search-result" + (i === active ? " is-active" : "");
        link.setAttribute("role", "option");
        link.setAttribute("aria-selected", String(i === active));
        link.innerHTML = '<span class="search-result-copy"><strong></strong><small></small></span><span class="search-result-type"></span><span aria-hidden="true">→</span>';
        link.querySelector("strong").textContent = item.entry.title;
        link.querySelector("small").textContent = item.entry.description;
        link.querySelector(".search-result-type").textContent = item.entry.type;
        link.addEventListener("mouseenter", function () { active = i; render(); });
        results.appendChild(link);
      });
      count.textContent = matches.length + (matches.length === 1 ? " result" : " results");
      empty.hidden = matches.length > 0;
    }
    function open() {
      previousFocus = document.activeElement;
      root.hidden = false;
      document.body.classList.add("search-open");
      input.value = "";
      active = 0;
      render();
      requestAnimationFrame(function () { input.focus(); });
    }
    function close() {
      root.hidden = true;
      document.body.classList.remove("search-open");
      if (previousFocus) previousFocus.focus();
    }
    document.querySelectorAll("[data-search-open]").forEach(function (button) { button.addEventListener("click", open); });
    root.querySelectorAll("[data-search-close]").forEach(function (button) { button.addEventListener("click", close); });
    input.addEventListener("input", function () { active = 0; render(); });
    document.addEventListener("keydown", function (event) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        root.hidden ? open() : close();
      } else if (!root.hidden && event.key === "Escape") {
        event.preventDefault(); close();
      } else if (!root.hidden && (event.key === "ArrowDown" || event.key === "ArrowUp")) {
        var links = results.querySelectorAll("a");
        if (!links.length) return;
        event.preventDefault();
        active = (active + (event.key === "ArrowDown" ? 1 : -1) + links.length) % links.length;
        links.forEach(function (link, i) { link.classList.toggle("is-active", i === active); link.setAttribute("aria-selected", String(i === active)); });
        links[active].scrollIntoView({ block: "nearest" });
      } else if (!root.hidden && event.key === "Enter") {
        var selected = results.querySelector(".is-active");
        if (selected) { event.preventDefault(); selected.click(); }
      }
    });
  }

  function initPageOutline() {
    var aside = document.querySelector("[data-page-outline]");
    var toggle = document.querySelector("[data-outline-toggle]");
    var linksRoot = document.querySelector("[data-outline-links]");
    if (!aside || !toggle || !linksRoot) return;
    var headings = Array.prototype.slice.call(document.querySelectorAll("main section h2[id], main article h2[id], main section[id] > .wrap > .section-head h2"));
    var used = {};
    headings = headings.filter(function (heading) {
      if (!heading.id) {
        var base = heading.textContent.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 46) || "section";
        var id = base, n = 2;
        while (document.getElementById(id) || used[id]) { id = base + "-" + n++; }
        heading.id = id;
      }
      if (used[heading.id]) return false;
      used[heading.id] = true;
      return true;
    }).slice(0, 12);
    if (headings.length < 3) return;
    headings.forEach(function (heading) {
      var link = document.createElement("a");
      link.href = "#" + heading.id;
      link.textContent = heading.textContent.trim();
      link.addEventListener("click", function () { setOpen(false); });
      linksRoot.appendChild(link);
    });
    toggle.hidden = false;
    function setOpen(open) {
      aside.hidden = !open;
      toggle.setAttribute("aria-expanded", String(open));
    }
    toggle.addEventListener("click", function () { setOpen(aside.hidden); });
    aside.querySelector("[data-outline-close]").addEventListener("click", function () { setOpen(false); toggle.focus(); });
    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          linksRoot.querySelectorAll("a").forEach(function (link) { link.classList.toggle("is-active", link.hash === "#" + entry.target.id); });
        });
      }, { rootMargin: "-20% 0px -65%", threshold: 0 });
      headings.forEach(function (heading) { observer.observe(heading); });
    }
  }

  initNav();
  initCounters();
  initCopy();
  initDisclosures();
  initYear();
  initProgress();
  initSiteSearch();
  initPageOutline();
})();
