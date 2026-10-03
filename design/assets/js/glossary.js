(function () {
  "use strict";

  var searchInput = document.getElementById("glossary-search");
  var grid = document.getElementById("glossary-grid");
  var countEl = document.getElementById("glossary-count");
  var emptyEl = document.getElementById("glossary-empty");
  if (!grid || !searchInput) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll(".glossary-card"));
  var rangeBtns = Array.prototype.slice.call(document.querySelectorAll(".letter-chips .filter-chip"));
  var catBtns = Array.prototype.slice.call(document.querySelectorAll(".cat-chips .tag-chip"));

  var state = {
    query: "",
    range: "all",
    cat: "all"
  };

  function matchesRange(term, range) {
    if (range === "all") return true;
    var first = term.trim().charAt(0).toUpperCase();
    var parts = range.split("-");
    return first >= parts[0] && first <= parts[1];
  }

  function applyFilter() {
    var q = state.query.toLowerCase().trim();
    var visibleCount = 0;

    cards.forEach(function (card) {
      var term = card.dataset.term || "";
      var cat = card.dataset.cat || "";
      var text = (card.textContent || "").toLowerCase();

      var matchesQuery = !q || text.indexOf(q) !== -1;
      var matchesCat = state.cat === "all" || cat === state.cat;
      var matchesLetter = matchesRange(term, state.range);

      var isVisible = matchesQuery && matchesCat && matchesLetter;
      card.hidden = !isVisible;
      if (isVisible) visibleCount++;
    });

    if (countEl) countEl.textContent = String(visibleCount);
    if (emptyEl) emptyEl.hidden = visibleCount > 0;
  }

  searchInput.addEventListener("input", function (e) {
    state.query = e.target.value;
    applyFilter();
  });

  rangeBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      rangeBtns.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      state.range = btn.dataset.range;
      applyFilter();
    });
  });

  catBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      catBtns.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      state.cat = btn.dataset.cat;
      applyFilter();
    });
  });
})();
