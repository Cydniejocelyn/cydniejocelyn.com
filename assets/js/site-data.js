/* ============================================================
   The site's own forms and its own visit count. 26 September 2026.

   Her word: "I want it pushed to neon for the database". Two jobs:

   1. FORMS. Any <form data-api="subscribe|inquiry"> posts its fields as
      JSON to /api/<name>, which saves to her Neon database (and sends the
      sign-up to Flodesk, or emails her the question). The form answers in
      place; if the server cannot be reached it says so and gives the email
      address, so a visitor is never left guessing. The hidden "website"
      field is the honeypot the server checks.

   2. VISITS AND CLICKS. Only after a visitor accepts cookies, the same gate
      as Google Analytics (consent.js fires "cj:consented"): one "view" per
      page, and one "click" per data-cta button. Page, button, kind of
      screen and referring site only. Nothing is sent before consent and
      nothing identifies the visitor.
   ============================================================ */
(function (w, d) {
  "use strict";

  /* ---------- forms ---------- */
  function fieldsOf(form) {
    var out = { source_path: w.location.pathname };
    Array.prototype.forEach.call(form.elements, function (el) {
      if (el.name && el.type !== "submit") out[el.name] = el.value;
    });
    return out;
  }

  function say(form, text, kind) {
    var s = form.querySelector(".cj-status");
    if (!s) return;
    s.textContent = text;
    s.className = "cj-status" + (kind ? " is-" + kind : "");
  }

  d.addEventListener("submit", function (e) {
    var form = e.target;
    if (!form || !form.hasAttribute || !form.hasAttribute("data-api")) return;
    e.preventDefault();
    if (form.checkValidity && !form.checkValidity()) { form.reportValidity(); return; }
    var btn = form.querySelector("[type=submit]");
    if (btn) btn.disabled = true;
    say(form, "Sending…", "");
    fetch("/api/" + form.getAttribute("data-api"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(fieldsOf(form)),
      credentials: "same-origin"
    }).then(function (r) {
      return r.json().catch(function () { return { ok: false }; }).then(function (j) { return { r: r, j: j }; });
    }).then(function (x) {
      if (x.r.ok && x.j.ok) {
        form.classList.add("is-done");
        Array.prototype.forEach.call(form.querySelectorAll("input, textarea"), function (el) { el.value = ""; });
        say(form, x.j.message || "Thank you.", "ok");
      } else {
        say(form, (x.j && x.j.error) || "That did not go through. Please try again, or write to hello@cydniejocelyn.com.", "err");
      }
    }).catch(function () {
      say(form, "That did not go through. Please try again, or write to hello@cydniejocelyn.com.", "err");
    }).then(function () { if (btn) btn.disabled = false; });
  });

  /* ---------- her own visit count, after consent only ---------- */
  function consented() {
    if (w.cjConsented) return true;
    try {
      var s = JSON.parse(w.localStorage.getItem("cj-cookie-choice") || "null");
      return !!(s && s.choice === "yes" && Date.now() - s.at < 365 * 86400000);
    } catch (e) { return false; }
  }

  function device() {
    var x = w.innerWidth || 1200;
    return x < 768 ? "phone" : x < 1120 ? "tablet" : "desktop";
  }

  function send(kind, cta) {
    if (!consented()) return;
    var body = { kind: kind, path: w.location.pathname, device: device() };
    if (cta) body.cta = cta;
    if (kind === "view" && d.referrer) body.referrer = d.referrer;
    try {
      fetch("/api/event", { method: "POST", keepalive: true, credentials: "same-origin",
        headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
        .catch(function () {});
    } catch (e) {}
  }

  var viewed = false;
  function view() { if (!viewed && consented()) { viewed = true; send("view"); } }

  d.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("[data-cta]") : null;
    if (a) send("click", (a.getAttribute("data-cta") || "").toLowerCase());
  }, true);

  d.addEventListener("cj:consented", view);
  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", view); else view();
})(window, document);
