(function () {
  "use strict";
  var root = document.querySelector("[data-process-planner]");
  if (!root) return;
  var plans = {
    drop: {
      title: "Change reconstruction and loss isolation",
      summary: "Pin the decline to dates, directories, query groups and releases before prescribing content or technical work.",
      evidence: ["GSC query and page deltas", "Algorithm and release timeline", "Crawl, indexation and template changes"],
      deliverables: ["Loss map with confidence levels", "Recovery hypotheses ranked by impact", "Bounded 30-day action queue"],
      verification: ["Affected query groups stabilize", "Priority URLs regain crawl and visibility", "No regression in unaffected sections"],
      topic: "algorithm-recovery"
    },
    launch: {
      title: "Demand, entity and page-role architecture",
      summary: "Decide which pages deserve to exist, what each page must answer, and how authority should flow before production scales.",
      evidence: ["Business model and conversion paths", "Query clusters and competitor page types", "Entity, attribute and internal-link gaps"],
      deliverables: ["Page and query map", "Template and content acceptance rules", "Measurement and launch checklist"],
      verification: ["Important pages are discoverable and indexed", "Queries land on the intended page types", "Early impressions match target entities"],
      topic: "new-site-launch"
    },
    scale: {
      title: "Crawl budget and template quality control",
      summary: "Find where templates multiply weak URLs, then protect useful inventory through rules that can be enforced at scale.",
      evidence: ["URL inventory by template and status", "Googlebot rendering and log samples", "Canonical, facet and parameter behavior"],
      deliverables: ["Keep, merge, block and remove rules", "Template-level content requirements", "Crawl and indexation monitoring view"],
      verification: ["Fewer low-value crawl paths", "Higher useful-index coverage", "Stable traffic during consolidation"],
      topic: "crawl-budget"
    },
    system: {
      title: "Workflow and measurement redesign",
      summary: "Map the repeated manual work, identify the decision points, and automate only where the rule is clear and reviewable.",
      evidence: ["Current reporting and handoff flow", "Repeated tasks, delays and QA failures", "Available APIs, exports and ownership"],
      deliverables: ["Target workflow and approval gates", "Dashboard, script or automation prototype", "Runbook with failure and recovery paths"],
      verification: ["Less manual handling time", "Faster anomaly detection", "Clearer ownership and reproducible output"],
      topic: "automation"
    }
  };
  var buttons = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
  function list(target, items) {
    target.innerHTML = "";
    items.forEach(function (item) { var li = document.createElement("li"); li.textContent = item; target.appendChild(li); });
  }
  function select(button, focus) {
    var plan = plans[button.getAttribute("data-plan")];
    buttons.forEach(function (item) { var on = item === button; item.setAttribute("aria-selected", String(on)); item.tabIndex = on ? 0 : -1; });
    root.querySelector("[data-plan-title]").textContent = plan.title;
    root.querySelector("[data-plan-summary]").textContent = plan.summary;
    list(root.querySelector("[data-plan-evidence]"), plan.evidence);
    list(root.querySelector("[data-plan-deliverables]"), plan.deliverables);
    list(root.querySelector("[data-plan-verification]"), plan.verification);
    root.querySelector("[data-plan-link]").href = "../contact/?topic=" + plan.topic;
    if (focus) button.focus();
  }
  buttons.forEach(function (button, i) {
    button.addEventListener("click", function () { select(button, false); });
    button.addEventListener("keydown", function (event) {
      var next;
      if (event.key === "ArrowRight" || event.key === "ArrowDown") next = buttons[(i + 1) % buttons.length];
      if (event.key === "ArrowLeft" || event.key === "ArrowUp") next = buttons[(i - 1 + buttons.length) % buttons.length];
      if (next) { event.preventDefault(); select(next, true); }
    });
  });
  select(buttons[0], false);
})();
