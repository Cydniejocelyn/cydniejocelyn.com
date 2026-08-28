/* COOKIE CONSENT
   ==================================================================
   Google Analytics does not load until a reader says yes.

   THE DECISION THIS FILE MAKES, AND WHY IT IS THE STRICT ONE
   ----------------------------------------------------------
   There are two ways to do this and only one of them is honest.

   The common way is Google's Consent Mode: load `gtag.js` immediately,
   declare `analytics_storage: denied`, and let it send cookieless pings
   until the reader agrees. No cookie is set, which satisfies the letter of
   most cookie rules, but the reader's IP and the page they are on still
   reach Google before they have agreed to anything.

   This file does the other thing. **Before consent there is no `gtag`, no
   `dataLayer`, and no request to any Google domain at all.** The tag is
   injected on accept and never otherwise. That is simpler to explain, it is
   what the privacy policy now says, and it is the only version that is true
   if somebody checks with a network tab open.

   HOW analytics.js BEHAVES IN THE MEANTIME
   ----------------------------------------
   It already guards every send with `typeof w.gtag !== "function"` and
   returns silently. So before consent it collects nothing and throws
   nothing, and no queue builds up that could be flushed later. That guard
   was written for ad blockers and turns out to be exactly the right shape
   for this too -- which is why `gtag` is deliberately NOT defined as a
   dataLayer stub here. A stub would let events pile into `dataLayer` while
   consent is denied, and they would be sent the moment the tag loaded.

   WHAT IS REMEMBERED
   ------------------
   One localStorage key holding the answer and the date. It expires after a
   year, so consent is asked for again rather than assumed forever, and the
   date is what makes that possible. Nothing is stored before a choice is
   made: a reader who ignores the banner leaves no trace at all.

   `localStorage` can throw outright in a private window or with site data
   blocked, so every read and write is wrapped. A reader whose browser
   refuses storage sees the banner each visit and analytics never loads,
   which is the right way round for that failure.
   ================================================================== */
(function (w, d) {
  "use strict";

  var KEY = "cj-cookie-choice";
  var MEASUREMENT_ID = "G-KDB3GWPNHC";
  var REMEMBER_DAYS = 365;

  /* ---------- what was decided last time ---------- */

  function stored() {
    try {
      var raw = w.localStorage.getItem(KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || !s.at) return null;
      if (Date.now() - s.at > REMEMBER_DAYS * 86400000) return null;  /* ask again */
      return s.choice === "yes" ? "yes" : "no";
    } catch (e) { return null; }
  }

  function remember(choice) {
    try {
      w.localStorage.setItem(KEY, JSON.stringify({ choice: choice, at: Date.now() }));
    } catch (e) {}
  }

  /* ---------- the tag, loaded only on yes ---------- */

  var loaded = false;
  function loadAnalytics() {
    if (loaded || typeof w.gtag === "function") return;
    loaded = true;

    w.dataLayer = w.dataLayer || [];
    w.gtag = function () { w.dataLayer.push(arguments); };

    /* Consent Mode is set as well as gating the load. Belt and braces: if a
       future change ever loads the tag earlier, these defaults are already
       in place and the storage stays denied until the line below grants it. */
    w.gtag("consent", "default", {
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
      analytics_storage: "denied"
    });
    w.gtag("consent", "update", { analytics_storage: "granted" });

    var s = d.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + MEASUREMENT_ID;
    d.head.appendChild(s);

    w.gtag("js", new Date());
    w.gtag("config", MEASUREMENT_ID);
  }

  /* ---------- the banner ---------- */

  var el = null;

  function close() {
    if (!el) return;
    el.remove();
    el = null;
  }

  /* DECLINING HAS TO REMOVE WHAT IS ALREADY THERE, not just stop adding to
     it. Analytics ran unconditionally on this site before the banner
     existed, so a returning reader arrives already carrying `_ga` and
     `_ga_KDB3GWPNHC`. Storing "no" and leaving those in place would be a
     decline that changes nothing, which is worse than not offering one.

     Both the bare host and the dot-prefixed domain are tried, and the
     parent domain too, because GA writes to the registrable domain and a
     delete only lands when the domain and path match what was set. */
  function clearAnalyticsCookies() {
    var names = ["_ga", "_ga_" + MEASUREMENT_ID.replace("G-", ""), "_gid", "_gat"];
    var host = w.location.hostname;
    var parent = host.split(".").slice(-2).join(".");
    var domains = ["", host, "." + host];
    if (parent !== host) domains.push(parent, "." + parent);
    names.forEach(function (n) {
      domains.forEach(function (dm) {
        d.cookie = n + "=; Max-Age=0; path=/" + (dm ? "; domain=" + dm : "");
      });
    });
  }

  function decide(choice) {
    remember(choice);
    if (choice === "yes") loadAnalytics();
    else clearAnalyticsCookies();
    close();
  }

  function show() {
    if (el) return;
    el = d.createElement("div");
    el.className = "cc";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-labelledby", "cc-title");
    el.setAttribute("aria-describedby", "cc-body");

    /* No interpolation anywhere in here: it is a fixed string, and the one
       place this codebase ever put reader-adjacent text through innerHTML
       is written up in site.js as a mistake. */
    el.innerHTML =
      '<div class="cc-in">' +
        '<div class="cc-copy">' +
          '<p class="cc-title" id="cc-title">Cookies</p>' +
          '<p class="cc-body" id="cc-body">I use Google Analytics to see which pages get read ' +
            'and which do not. It sets two cookies. Nothing loads until you choose, and ' +
            'declining costs you nothing on this site.</p>' +
        '</div>' +
        '<div class="cc-acts">' +
          '<button type="button" class="cc-btn cc-btn--yes" data-cc="yes">Accept</button>' +
          '<button type="button" class="cc-btn" data-cc="no">Decline</button>' +
        '</div>' +
      '</div>';

    /* Placed after the skip link so it is second in the tab order: reachable
       in one press for a keyboard reader, without stealing focus from
       somebody who is already reading. A non-modal dialog that grabs focus
       on every page load until it is answered is its own accessibility
       problem. */
    var skip = d.querySelector(".skip");
    if (skip && skip.parentNode) skip.parentNode.insertBefore(el, skip.nextSibling);
    else d.body.insertBefore(el, d.body.firstChild);

    el.addEventListener("click", function (e) {
      var b = e.target.closest("[data-cc]");
      if (b) decide(b.getAttribute("data-cc"));
    });

    /* Escape is not a decision. It dismisses the banner for this page view
       and asks again next time, which is what "I have not decided" means.

       ONLY WHEN FOCUS IS INSIDE THE BANNER. This listened on the whole
       document at first, and the suite caught what that costs: the Greece
       page has a lightbox that closes on Escape, so shutting a photograph
       also silently dismissed the cookie banner two components away. An
       Escape aimed at one thing must not answer another. */
    d.addEventListener("keydown", function onKey(e) {
      if (e.key !== "Escape" || !el) return;
      if (!el.contains(d.activeElement)) return;
      close();
      d.removeEventListener("keydown", onKey);
    });
  }

  /* ---------- changing your mind ----------
     Any `[data-cookie-settings]` control on the site clears the stored answer
     and asks again. There is one in the privacy policy, which is where a
     person goes looking for it. */
  function wireSettings() {
    Array.prototype.slice.call(d.querySelectorAll("[data-cookie-settings]"))
      .forEach(function (b) {
        b.addEventListener("click", function (e) {
          e.preventDefault();
          try { w.localStorage.removeItem(KEY); } catch (err) {}
          show();
          var first = el && el.querySelector("[data-cc]");
          if (first) first.focus();   /* asked for, so focus is right here */
        });
      });
  }

  function start() {
    var choice = stored();
    if (choice === "yes") loadAnalytics();
    else if (choice === null) show();
    wireSettings();
  }

  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", start);
  else start();
})(window, document);
