(function () {
  "use strict";

  var scaleData = {
    impressions: {
      title: "1.47 Billion Impressions Handled",
      stat: "1,470,000,000+",
      desc: "Measured across 16-month Google Search Console windows on enterprise medical and programmatic architectures. Required crawl-budget hardening, directory consolidation, and sub-second server response times.",
      tag: "Enterprise Scale"
    },
    sitemaps: {
      title: "130,000+ Page Architectures",
      stat: "130,000+ URLs",
      desc: "Managed large faceted taxonomies, programmatic vehicle scrapping databases, and multi-tier medical hubs. Solved Googlebot rendering bottlenecks and pruned 20k duplicate pages to preserve domain threshold value.",
      tag: "Technical Architecture"
    },
    team: {
      title: "50+ Cross-Functional Team Leadership",
      stat: "50+ Members",
      desc: "Directed multidisciplinary teams across technical SEO, content writers, frontend developers, and UI designers. Maintained uniform quality standards and sprint velocity across 60+ concurrent accounts.",
      tag: "Operations & Leadership"
    },
    accounts: {
      title: "60+ Concurrent Accounts Managed",
      stat: "60+ Accounts",
      desc: "Built automated Looker Studio dashboards, n8n Slack webhook alert systems, and Google Apps Script pipelines to monitor traffic anomalies and delivery milestones across 6 countries without quality loss.",
      tag: "Systematized Delivery"
    }
  };

  var buttons = document.querySelectorAll(".scale-btn");
  var displayCard = document.getElementById("scale-display");
  var titleEl = document.getElementById("scale-title");
  var statEl = document.getElementById("scale-stat");
  var descEl = document.getElementById("scale-desc");
  var tagEl = document.getElementById("scale-tag");

  if (!displayCard || buttons.length === 0) return;

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      buttons.forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");

      var key = btn.dataset.scale;
      var data = scaleData[key];
      if (!data) return;

      displayCard.style.opacity = "0";
      setTimeout(function () {
        titleEl.textContent = data.title;
        statEl.textContent = data.stat;
        descEl.textContent = data.desc;
        tagEl.textContent = data.tag;
        displayCard.style.opacity = "1";
      }, 150);
    });
  });
})();
