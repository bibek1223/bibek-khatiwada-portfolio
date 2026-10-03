(function () {
  "use strict";

  var plans = {
    recovery: {
      title: "Algorithmic Core Recovery Sprint",
      timeline: "Estimated Timeline: 4–6 Weeks",
      deliverables: [
        "Directory-level Search Console core update loss correlation",
        "Scaled duplicate URL identification & 301 consolidation mapping",
        "E-E-A-T and medical/consensus entity grounding schema graphs",
        "Log-file crawl budget verification & robots.txt hardening"
      ]
    },
    aeo: {
      title: "Generative Engine & AEO Architecture",
      timeline: "Estimated Timeline: 3–4 Weeks",
      deliverables: [
        "Standardized /llms.txt endpoint architecture deployment",
        "40-word concise answer-span refactoring below primary H2/H3 tags",
        "Entity-Attribute-Value (EAV) Knowledge Graph schema markup",
        "Deterministic prompt matrix tracking across ChatGPT & Perplexity"
      ]
    },
    programmatic: {
      title: "Programmatic Scale & Dynamic Inventory",
      timeline: "Estimated Timeline: 5–8 Weeks",
      deliverables: [
        "Controlled database-driven template architecture design",
        "Faceted parameter indexing controls and canonicalization",
        "Long-tail entity attribute injection to prevent thin-content flags",
        "Google Merchant Center feed & schema synchronization"
      ]
    },
    technical: {
      title: "Technical Infrastructure & Crawl Hardening",
      timeline: "Estimated Timeline: 2–4 Weeks",
      deliverables: [
        "Googlebot JavaScript rendering and Server-Side Rendering (SSR) checks",
        "Crawl waste pruning across parameter and untracked tag URLs",
        "Core Web Vitals critical rendering path optimization (LCP, INP, CLS)",
        "Internal link graph restructuring and redirect chain resolution"
      ]
    }
  };

  var scaleBtns = document.querySelectorAll(".scope-btn[data-scale]");
  var platformBtns = document.querySelectorAll(".scope-btn[data-platform]");
  var goalBtns = document.querySelectorAll(".scope-btn[data-goal]");

  var planTitleEl = document.getElementById("scope-plan-title");
  var timelineEl = document.getElementById("scope-timeline");
  var deliverablesEl = document.getElementById("scope-deliverables-list");
  var waBtn = document.getElementById("scope-wa-btn");
  var contactBtn = document.getElementById("scope-contact-btn");

  if (!planTitleEl) return;

  var currentScale = "small";
  var currentPlatform = "wordpress";
  var currentGoal = "recovery";

  function update() {
    var p = plans[currentGoal] || plans.recovery;
    planTitleEl.textContent = p.title;
    timelineEl.textContent = p.timeline;

    deliverablesEl.innerHTML = p.deliverables.map(function (d) {
      return "<li>" + d + "</li>";
    }).join("");

    var msg = encodeURIComponent(
      "Hi Bibek, I used your Scope Estimator on your portfolio: Scale: " + currentScale +
      ", Platform: " + currentPlatform + ", Objective: " + p.title +
      ". I would like to discuss this engagement scope."
    );

    if (waBtn) waBtn.href = "https://wa.me/9779860411440?text=" + msg;
    if (contactBtn) contactBtn.href = "{{root}}contact/?ref=scope&goal=" + currentGoal + "&notes=" + msg;
  }

  function setupGroup(buttons, callback) {
    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        buttons.forEach(function (b) { b.classList.remove("active"); });
        btn.classList.add("active");
        callback(btn);
        update();
      });
    });
  }

  setupGroup(scaleBtns, function (b) { currentScale = b.dataset.scale; });
  setupGroup(platformBtns, function (b) { currentPlatform = b.dataset.platform; });
  setupGroup(goalBtns, function (b) { currentGoal = b.dataset.goal; });

  update();
})();
