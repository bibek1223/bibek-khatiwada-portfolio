/* Case-study index: filter + sort the cards, keep running totals, and draw two
   comparison charts (log-scale dot plot, CTR-vs-position scatter) as inline SVG.
   Data comes from <script id="cs-data">, generated from site/data.py. */
(function () {
  "use strict";

  var dataEl = document.getElementById("cs-data");
  var grid = document.getElementById("cs-grid");
  if (!dataEl || !grid) return;

  var STUDIES = JSON.parse(dataEl.textContent);
  var byN = {};
  STUDIES.forEach(function (s) { byN[s.n] = s; });
  var cards = Array.prototype.slice.call(grid.querySelectorAll(".cs-card"));
  var chips = Array.prototype.slice.call(document.querySelectorAll(".filter-chip"));
  var sortEl = document.getElementById("cs-sort");
  var emptyEl = document.querySelector(".explorer-empty");
  var state = { filter: "all", sort: "impact" };
  var SVGNS = "http://www.w3.org/2000/svg";

  // ---------- formatting ----------
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

  // ---------- ranking ----------
  // "Most impact" is the default sort, so it decides which projects a visitor
  // sees first. Each study has: clicks, impr, ctr (%), pos (lower is better),
  // months (16, or null for the year-over-year study), yoy (boolean).
  // Return a number; higher sorts first.
  function impactScore(s) {
    // TODO(Bibek): define what "impact" means for your portfolio.
    // Stand-in until then: raw 16-month clicks, with the YoY study last.
    return s.yoy ? -1 : s.clicks;
  }

  var SORTS = {
    impact: function (a, b) { return impactScore(b) - impactScore(a); },
    clicks: function (a, b) { return (a.yoy - b.yoy) || (b.clicks - a.clicks); },
    impr: function (a, b) { return (a.yoy - b.yoy) || (b.impr - a.impr); },
    ctr: function (a, b) { return b.ctr - a.ctr; },
    pos: function (a, b) { return a.pos - b.pos; },
    n: function (a, b) { return a.n.localeCompare(b.n); }
  };

  function matches(s) {
    return state.filter === "all" || s.tags.indexOf(state.filter) !== -1;
  }

  // ---------- explorer ----------
  function apply() {
    var visible = STUDIES.filter(matches).sort(SORTS[state.sort] || SORTS.impact);
    var shown = {};
    visible.forEach(function (s) { shown[s.n] = true; });

    cards.forEach(function (card) { card.hidden = !shown[card.getAttribute("data-n")]; });
    visible.forEach(function (s) {
      grid.appendChild(grid.querySelector('[data-n="' + s.n + '"]'));
    });
    emptyEl.hidden = visible.length > 0;

    chips.forEach(function (c) {
      c.setAttribute("aria-pressed", String(c.getAttribute("data-filter") === state.filter));
    });
    sortEl.value = state.sort;

    var summable = visible.filter(function (s) { return !s.yoy; });
    setAgg("clicks", compact(summable.reduce(function (t, s) { return t + s.clicks; }, 0)));
    setAgg("impr", compact(summable.reduce(function (t, s) { return t + s.impr; }, 0)));
    setAgg("count", String(visible.length));

    document.querySelectorAll(".chart .mark").forEach(function (m) {
      m.classList.toggle("dim", !shown[m.getAttribute("data-n")]);
    });

    var params = new URLSearchParams(location.search);
    if (state.filter === "all") params.delete("filter"); else params.set("filter", state.filter);
    if (state.sort === "impact") params.delete("sort"); else params.set("sort", state.sort);
    var qs = params.toString();
    history.replaceState(null, "", location.pathname + (qs ? "?" + qs : "") + location.hash);
  }

  function setAgg(key, value) {
    var el = document.querySelector('[data-agg="' + key + '"]');
    if (el) el.textContent = value;
  }

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      state.filter = chip.getAttribute("data-filter");
      apply();
    });
  });
  sortEl.addEventListener("change", function () {
    state.sort = sortEl.value;
    apply();
  });

  var params = new URLSearchParams(location.search);
  if (params.get("filter") && chips.some(function (c) { return c.getAttribute("data-filter") === params.get("filter"); })) {
    state.filter = params.get("filter");
  }
  if (params.get("sort") && SORTS[params.get("sort")]) state.sort = params.get("sort");

  // ---------- charts ----------
  function el(name, attrs, parent) {
    var node = document.createElementNS(SVGNS, name);
    Object.keys(attrs || {}).forEach(function (k) { node.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(node);
    return node;
  }
  function text(parent, x, y, str, cls, anchor) {
    var t = el("text", { x: x, y: y, class: cls || "lbl", "text-anchor": anchor || "start" }, parent);
    t.textContent = str;
    return t;
  }

  function tipFor(container) {
    var tip = container.querySelector(".chart-tip");
    if (!tip) {
      tip = document.createElement("div");
      tip.className = "chart-tip";
      tip.hidden = true;
      container.appendChild(tip);
    }
    return tip;
  }

  function bindMark(mark, s, container, anchorFn) {
    var tip = tipFor(container);
    var body = s.yoy
      ? "3-month YoY window<br>" + s.clicks_d + " clicks · " + s.impr_d + " impressions"
      : s.clicks_d + " clicks · " + s.impr_d + " impressions<br>16 months";
    function show() {
      var p = anchorFn();
      tip.innerHTML = "<b>Case " + s.n + "</b>" + s.short + "<br>" + body +
        "<br>CTR " + s.ctr + "% · Avg. position " + s.pos;
      tip.style.left = p.x + "px";
      tip.style.top = p.y + "px";
      tip.hidden = false;
    }
    function hide() { tip.hidden = true; }
    mark.addEventListener("mouseenter", show);
    mark.addEventListener("mouseleave", hide);
    mark.addEventListener("focus", show);
    mark.addEventListener("blur", hide);
  }

  function markLink(parent, s) {
    var a = el("a", { class: "mark", href: s.slug + "/", "data-n": s.n }, parent);
    a.setAttribute("aria-label", "Case " + s.n + ", " + s.short + ": " +
      (s.yoy ? "" : s.clicks_d + " clicks, " + s.impr_d + " impressions, ") +
      s.ctr + "% CTR, average position " + s.pos);
    return a;
  }

  function drawVolume(container) {
    var data = STUDIES.filter(function (s) { return !s.yoy; }).sort(SORTS.clicks);
    var W = Math.max(container.clientWidth, 300);
    var narrow = W < 560;
    var padL = narrow ? 62 : 250, padR = 24, padT = 34, rowH = narrow ? 42 : 40;
    var H = padT + data.length * rowH + 8;
    var lo = 3, hi = Math.log10(3e9);
    function x(v) { return padL + (Math.log10(v) - lo) / (hi - lo) * (W - padL - padR); }

    container.innerHTML = "";
    var svg = el("svg", { viewBox: "0 0 " + W + " " + H, width: W, height: H, role: "group",
      "aria-label": "Clicks and impressions per case study, log scale" }, container);
    var defs = el("defs", {}, svg);
    var grad = el("linearGradient", { id: "dumbGrad", x1: "0", x2: "1" }, defs);
    el("stop", { offset: "0", "stop-color": "#7c3aed" }, grad);
    el("stop", { offset: "1", "stop-color": "#ff8a65" }, grad);

    var g = el("g", { class: "grid axis" }, svg);
    [1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9].forEach(function (v, i) {
      if (narrow && i % 2) return;
      el("line", { x1: x(v), x2: x(v), y1: padT - 10, y2: H - 4 }, g);
      text(g, x(v), padT - 16, compact(v), "lbl", "middle");
    });

    var legend = el("g", {}, svg);
    el("circle", { cx: W - padR - 150, cy: 10, r: 6, fill: "#7c3aed" }, legend);
    text(legend, W - padR - 140, 14, "Clicks");
    el("circle", { cx: W - padR - 80, cy: 10, r: 6, fill: "#fff", stroke: "#ff8a65", "stroke-width": 3 }, legend);
    text(legend, W - padR - 70, 14, "Impressions");

    data.forEach(function (s, i) {
      var cy = padT + i * rowH + rowH / 2;
      var a = markLink(svg, s);
      el("rect", { x: 0, y: cy - rowH / 2, width: W, height: rowH, fill: "transparent" }, a);
      text(a, 0, cy + 4, "Case " + s.n, "lbl-strong");
      if (!narrow) text(a, 58, cy + 4, s.chip.length > 28 ? s.chip.slice(0, 27) + "…" : s.chip);
      el("line", { x1: x(s.clicks), x2: x(s.impr), y1: cy, y2: cy, stroke: "url(#dumbGrad)", "stroke-width": 4, "stroke-linecap": "round" }, a);
      el("circle", { class: "dot", cx: x(s.clicks), cy: cy, r: 7 }, a);
      el("circle", { cx: x(s.impr), cy: cy, r: 6, fill: "#fff", stroke: "#ff8a65", "stroke-width": 3 }, a);
      bindMark(a, s, container, function () { return { x: (x(s.clicks) + x(s.impr)) / 2, y: cy - 10 }; });
    });
  }

  function drawEfficiency(container) {
    var W = Math.max(container.clientWidth, 300);
    var narrow = W < 560;
    var H = narrow ? 300 : 380;
    var padL = 46, padR = 20, padT = 18, padB = 44;
    var xMin = 5, xMax = 17, yMin = 0, yMax = 6;
    function x(v) { return padL + (v - xMin) / (xMax - xMin) * (W - padL - padR); }
    function y(v) { return padT + (1 - (v - yMin) / (yMax - yMin)) * (H - padT - padB); }

    container.innerHTML = "";
    var svg = el("svg", { viewBox: "0 0 " + W + " " + H, width: W, height: H, role: "group",
      "aria-label": "Average CTR against average position per case study" }, container);
    var g = el("g", { class: "grid axis" }, svg);
    for (var p = 6; p <= 16; p += 2) {
      el("line", { x1: x(p), x2: x(p), y1: padT, y2: H - padB }, g);
      text(g, x(p), H - padB + 18, String(p), "lbl", "middle");
    }
    for (var c = 0; c <= 6; c += 2) {
      el("line", { x1: padL, x2: W - padR, y1: y(c), y2: y(c) }, g);
      text(g, padL - 8, y(c) + 4, c + "%", "lbl", "end");
    }
    text(svg, (padL + W - padR) / 2, H - 6, "Average position (lower is better) →", "lbl", "middle");

    var maxImpr = Math.max.apply(null, STUDIES.map(function (s) { return s.impr; }));
    STUDIES.forEach(function (s) {
      var a = markLink(svg, s);
      var r = 7 + 11 * Math.sqrt(s.impr / maxImpr);
      el("circle", { class: "dot", cx: x(s.pos), cy: y(s.ctr), r: r, "fill-opacity": 0.85 }, a);
      text(a, x(s.pos), y(s.ctr) - r - 5, s.n, "lbl-strong", "middle");
      bindMark(a, s, container, function () { return { x: x(s.pos), y: y(s.ctr) - r }; });
    });
  }

  var volEl = document.getElementById("chart-volume");
  var effEl = document.getElementById("chart-efficiency");
  function drawAll() {
    if (volEl && volEl.offsetParent !== null) drawVolume(volEl);
    if (effEl && effEl.offsetParent !== null) drawEfficiency(effEl);
    apply();
  }
  var tabsRoot = document.querySelector("#compare [data-tabs]");
  if (tabsRoot) tabsRoot.addEventListener("tabchange", drawAll);
  var resizeTimer;
  window.addEventListener("resize", function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(drawAll, 150);
  });

  drawAll();
})();
