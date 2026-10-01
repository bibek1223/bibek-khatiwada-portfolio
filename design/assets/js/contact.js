/* Contact page: Kathmandu clock and the brief builder. The builder only
   composes text in the browser; sending happens in the visitor's own email
   app or WhatsApp, so this site never receives or stores the message. */
(function () {
  "use strict";

  var EMAIL = "bibekkhatiwada2@gmail.com";
  var WHATSAPP = "https://wa.me/9779860411440";
  var KTM = "Asia/Kathmandu";

  function initClock() {
    var timeEl = document.querySelector("[data-clock-time]");
    var yoursEl = document.querySelector("[data-clock-yours]");
    if (!timeEl) return;
    var fmt = new Intl.DateTimeFormat(undefined, { hour: "numeric", minute: "2-digit", weekday: "short", timeZone: KTM });

    function offsetMinutes(zone, date) {
      var parts = new Intl.DateTimeFormat("en-US", {
        timeZone: zone, hour12: false, year: "numeric", month: "2-digit", day: "2-digit",
        hour: "2-digit", minute: "2-digit"
      }).formatToParts(date).reduce(function (o, p) { o[p.type] = p.value; return o; }, {});
      var asUTC = Date.UTC(+parts.year, +parts.month - 1, +parts.day, +parts.hour % 24, +parts.minute);
      return Math.round((asUTC - date.getTime()) / 60000);
    }

    function tick() {
      var now = new Date();
      timeEl.textContent = fmt.format(now);
      if (yoursEl) {
        var diff = offsetMinutes(KTM, now) + now.getTimezoneOffset();
        if (Math.abs(diff) < 1) {
          yoursEl.textContent = "Same time zone as you.";
        } else {
          var h = Math.floor(Math.abs(diff) / 60), m = Math.abs(diff) % 60;
          yoursEl.textContent = "That’s " + h + "h" + (m ? " " + m + "m" : "") + (diff > 0 ? " ahead of" : " behind") + " your local time.";
        }
      }
    }
    tick();
    setInterval(tick, 30000);
  }

  function initBrief() {
    var form = document.getElementById("brief");
    if (!form) return;
    var site = form.elements.site;
    var topic = form.elements.topic;
    var msg = form.elements.message;
    var out = document.getElementById("brief-out");
    var count = document.getElementById("b-msg-count");
    var status = form.querySelector(".form-status");

    var preset = new URLSearchParams(location.search).get("topic");
    if (preset && topic.querySelector('option[value="' + CSS.escape(preset) + '"]')) topic.value = preset;

    function stage() {
      var checked = form.querySelector('input[name="stage"]:checked');
      return checked ? checked.value : "";
    }

    function compose() {
      var lines = [];
      var name = form.elements.name.value.trim();
      lines.push("Hi Bibek,", "");
      if (site.value.trim()) lines.push("Website: " + site.value.trim());
      if (topic.value) lines.push("Looking for: " + topic.options[topic.selectedIndex].text);
      if (stage()) lines.push("Where things are: " + stage());
      if (msg.value.trim()) lines.push("", msg.value.trim());
      lines.push("", "Thanks,", name || "");
      return lines.join("\n").trim();
    }

    function subject() {
      var s = site.value.trim();
      return "SEO enquiry" + (s ? ": " + s : "");
    }

    function validSite(v) {
      return /^(https?:\/\/)?([a-z0-9-]+\.)+[a-z]{2,}(\/\S*)?$/i.test(v.trim());
    }

    function showError(input, errId, bad) {
      input.setAttribute("aria-invalid", String(bad));
      document.getElementById(errId).hidden = !bad;
    }

    function validate() {
      var siteBad = !validSite(site.value);
      var msgBad = msg.value.trim().length < 20;
      showError(site, "b-site-err", siteBad);
      showError(msg, "b-msg-err", msgBad);
      if (siteBad) site.focus(); else if (msgBad) msg.focus();
      return !siteBad && !msgBad;
    }

    function refresh() {
      count.textContent = msg.value.length + " / 2000";
      out.textContent = compose();
    }
    form.addEventListener("input", function (e) {
      if (e.target.getAttribute("aria-invalid") === "true") {
        if (e.target === site && validSite(site.value)) showError(site, "b-site-err", false);
        if (e.target === msg && msg.value.trim().length >= 20) showError(msg, "b-msg-err", false);
      }
      refresh();
    });
    form.addEventListener("change", refresh);

    function send(kind) {
      status.textContent = "";
      if (kind !== "copy" && !validate()) return;
      var body = compose();
      if (kind === "email") {
        location.href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent(subject()) + "&body=" + encodeURIComponent(body);
        status.textContent = "Opening your email app…";
      } else if (kind === "whatsapp") {
        window.open(WHATSAPP + "?text=" + encodeURIComponent(body), "_blank", "noopener");
        status.textContent = "Opening WhatsApp…";
      } else if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(body).then(function () {
          status.textContent = "Copied. Paste it into any channel above.";
        }, function () { status.textContent = "Copy failed. Select the preview text instead."; });
      } else {
        status.textContent = "Copy isn’t available here. Select the preview text instead.";
      }
    }

    form.addEventListener("submit", function (e) { e.preventDefault(); send("email"); });
    form.querySelectorAll("[data-send]").forEach(function (btn) {
      if (btn.type !== "submit") btn.addEventListener("click", function () { send(btn.getAttribute("data-send")); });
    });
    refresh();
  }

  initClock();
  initBrief();
})();
