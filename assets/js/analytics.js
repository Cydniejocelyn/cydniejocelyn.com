/* GA4 EVENT TRACKING
   ==================================================================
   Measurement id G-KDB3GWPNHC. The tag itself is in every page head; this
   file only sends events to it.

   TWO RULES THIS FILE FOLLOWS ABSOLUTELY
   --------------------------------------
   1. It never changes what the page does. Every listener is delegated off
      `document`, nothing calls `preventDefault`, nothing writes to the DOM,
      nothing reads layout in a way that could force a synchronous reflow
      during a scroll. If this file were deleted the site would behave
      identically, minus the reporting.
   2. It never throws into someone else's handler. Every listener body is
      wrapped, and `track()` returns silently when `gtag` is missing --
      which is the normal state for any reader running an ad blocker, and is
      not an error.

   WHY IT IS A SEPARATE FILE AND NOT PART OF site.js
   -------------------------------------------------
   site.js is the site working. This is the site being watched. Keeping them
   apart means a measurement change can never be the reason a carousel
   stopped moving, and it means this whole file can be removed in one line
   if the tracking is ever unwanted. It costs one request, `defer`red, on a
   site that already ships two.

   NAMING
   ------
   GA4 convention: snake_case, event names under 40 characters, parameter
   names under 40, values truncated to 100. Where GA4 defines a recommended
   event for something -- `video_start`, `sign_up` -- that name is used
   rather than a bespoke one, because recommended events light up reporting
   in the GA interface that custom ones do not. `percent_scrolled` is
   likewise GA4's own parameter name from its built-in `scroll` event, kept
   so the two read the same way in a report.

   Every event and every parameter is documented in
   `tools/analytics-reference.html`. If you add one here, add it there.

   WHAT IS NOT HERE, AND WHY
   -------------------------
   Copy-to-clipboard on code samples, and filter/search on component
   listings, were both asked for. Neither exists on this site: there is not
   one `<pre>`, `<code>`, clipboard call or search input in the nine pages.
   Nothing was invented to fill the gap. The nearest real equivalent, the
   four-tab objection picker, is tracked as `filter_select` because that is
   genuinely what it is -- picking one of four filters a panel. See the
   reference page.
   ================================================================== */
(function (w, d) {
  "use strict";

  var MEASUREMENT_ID = "G-KDB3GWPNHC";

  /* ---------- the one way anything leaves this file ---------- */

  /* GA4 truncates parameter values at 100 characters server side and keeps
     the first 100 rather than rejecting the hit, so a long value does not
     lose the event -- it loses the end of the string. Truncating here means
     what we send is what we meant to send, and the ellipsis makes it obvious
     in a report that there was more. */
  function clean(s, max) {
    if (s == null) return "";
    s = String(s).replace(/\s+/g, " ").trim();
    max = max || 100;
    return s.length > max ? s.slice(0, max - 1) + "…" : s;
  }

  function track(name, params) {
    /* No gtag means an ad blocker, a consent tool, or a local file open. All
       three are ordinary and none of them is this file's business. */
    if (typeof w.gtag !== "function") return;
    try {
      var p = params || {};
      p.page_path = d.location.pathname;
      w.gtag("event", name, p);
      if (w.__analyticsDebug) w.console.log("[ga4]", name, p);
    } catch (e) {}
  }

  /* Exposed so `tools/analytics-reference.html` can list what is wired
     without duplicating the list, and so a person can type
     `__analyticsDebug = true` in a console and watch events fire. */
  w.__analytics = { track: track, id: MEASUREMENT_ID };

  function guard(fn) {
    return function (e) { try { fn(e); } catch (err) {} };
  }

  function textOf(el) {
    return clean(el && el.textContent);
  }

  /* ---------- where a link lives, which is most of its meaning ----------
     "Retreats" clicked in the header and "Retreats" clicked in the footer
     are different facts about a reader: one is navigation, the other is
     usually the end of a page they read to the bottom of. Reporting them as
     one number throws that away, so every link event carries where it was.

     Order matters here. The mobile menu markup is inside the header, so
     the menu test has to come first or every menu click reports as header. */
  /* The SAME media query site.js uses in initNav, deliberately, so the two
     can never disagree about which mode the menu is in. `.nav-menu` is one
     element serving both the desktop bar and the phone panel, and
     `has-menu` on the root is set at every width, so neither the markup nor
     that class can tell them apart. Only the width can.

     This was wrong first time round: every desktop header click reported as
     `mobile_menu`, which would have read as a site whose visitors are
     almost entirely on phones and using a menu most of them never open. */
  var WIDE = "(min-width: 56rem)";
  function menuIsPanel() {
    try { return !w.matchMedia(WIDE).matches; } catch (e) { return false; }
  }

  function locationOf(a) {
    if (a.closest(".nav-menu, #nav-menu")) {
      return menuIsPanel() ? "mobile_menu" : "site_header";
    }
    if (a.classList.contains("brand") || a.closest(".brand")) return "brand";
    if (a.closest(".hdr, header")) return "site_header";
    if (a.closest(".ftr-legal, .ftr-btm")) return "footer_legal";
    if (a.closest(".ftr-social, .social")) return "footer_social";
    if (a.closest(".ftr, footer")) return "site_footer";
    if (a.classList.contains("skip") || a.closest(".skip")) return "skip_link";
    return "page_body";
  }

  /* The nearest section with an id is the most useful "where on the page"
     answer available, because the ids on this site are already the names of
     the sections in the brief: #private, #booking, #terms. Falls back to the
     nearest landmark so the answer is never empty. */
  function sectionOf(el) {
    var s = el.closest("section[id], article[id], div[id]");
    if (s && s.id) return clean(s.id, 40);
    var l = el.closest("main, header, footer, nav");
    return l ? l.tagName.toLowerCase() : "document";
  }

  function isExternal(href) {
    return /^https?:\/\//i.test(href) && href.indexOf(w.location.host) === -1;
  }

  /* Where a click actually goes matters more than what it is called. A
     booking link is the thing this whole site exists to produce, and it is
     on a subdomain, so it would otherwise be counted as "external" and sit
     in the same bucket as a link to Instagram. */
  function destinationOf(href) {
    if (!href) return "none";
    if (href.indexOf("clients.cydniejocelyn.com") > -1) return "booking";
    if (href.indexOf("honeybook.com") > -1) return "booking";
    if (href.indexOf("mailto:") === 0) return "email";
    if (href.indexOf("tel:") === 0) return "phone";
    if (href.charAt(0) === "#") return "anchor";
    return isExternal(href) ? "external" : "internal";
  }

  /* ---------- clicks ----------
     One delegated listener for every anchor and button on the site. It runs
     on the bubble phase, after any handler that might have called
     preventDefault, and it does not care whether the navigation actually
     happened: an intent to click is the thing being measured. */
  d.addEventListener("click", guard(function (e) {
    var a = e.target.closest("a[href]");
    if (a) return onLink(a);

    var b = e.target.closest("button");
    if (b) return onButton(b, e);
  }));

  function onLink(a) {
    /* The video poster is an <a href="youtube.com/watch?v=..."> so that it
       is a working link out with no JS. With JS it never navigates: site.js
       swaps it for an in-place embed. Counting it as an outbound click would
       put a click that stayed on the site into the same number as one that
       left it, and it is the only element on the site where the href is a
       fallback rather than a destination. onVideo owns it.

       If site.js ever fails to load, this click IS a real exit and will be
       recorded as video_start rather than outbound_click. That is the better
       of the two wrong answers: the reader did go to watch the video. */
    if (a.hasAttribute("data-video")) return;

    var href = a.getAttribute("href") || "";
    var dest = destinationOf(href);
    var where = locationOf(a);
    var label = textOf(a) || a.getAttribute("aria-label") || "";

    /* A .btn is a considered decision and a nav link is a glance. They are
       counted apart so the funnel is not diluted by chrome. */
    if (a.classList.contains("btn") || dest === "booking") {
      track("cta_click", {
        cta_text: label,
        cta_location: where === "page_body" ? sectionOf(a) : where,
        link_url: clean(href),
        destination_type: dest
      });
    } else if (where === "site_header" || where === "mobile_menu" ||
               where === "site_footer" || where === "footer_legal" ||
               where === "footer_social" || where === "brand" ||
               where === "skip_link") {
      track("navigation_click", {
        link_text: label,
        link_url: clean(href),
        nav_location: where
      });
    }

    /* Fired IN ADDITION to the above, never instead of it. An outbound
       booking link is both a CTA and an exit, and collapsing the two would
       mean choosing which question you are allowed to ask later. */
    if (dest === "external" || dest === "booking") {
      track("outbound_click", {
        link_url: clean(href),
        link_domain: clean((href.split("/")[2] || ""), 60),
        link_text: label,
        nav_location: where
      });
    }
  }

  function onButton(b, e) {
    /* The objection picker. Four tabs, one panel shown at a time, built by
       site.js at runtime -- which is exactly why this is delegated off
       document rather than bound at load. This is the closest thing on the
       site to the "filter a listing" interaction, and it is a real one. */
    var tab = b.closest(".rev-picks [role=tab], [role=tablist] [role=tab]");
    if (tab) {
      var tabs = Array.prototype.slice.call(
        tab.closest("[role=tablist]").querySelectorAll("[role=tab]"));
      return track("filter_select", {
        filter_group: "objections",
        filter_value: textOf(tab),
        filter_position: tabs.indexOf(tab) + 1,
        filter_count: tabs.length
      });
    }

    /* Lightbox openers. Every gallery tile is a button whose accessible
       name is "Open: <caption>", so the caption is the useful half. */
    var tile = b.closest(".gal-item, .rt-shot");
    if (tile) {
      var fig = tile.querySelector("figcaption");
      var all = Array.prototype.slice.call(
        (tile.closest("[data-gallery], [data-rail]") || d)
          .querySelectorAll(".gal-item, .rt-shot"));
      return track("image_view", {
        image_caption: fig ? textOf(fig) : textOf(b).replace(/^Open:\s*/, ""),
        gallery_name: sectionOf(tile),
        image_position: all.indexOf(tile) + 1
      });
    }

    /* Rail arrows and story ticks both carry data-go / data-step. */
    if (b.hasAttribute("data-go")) {
      return track("gallery_navigate", {
        direction: b.getAttribute("data-go") === "1" ? "forward" : "back",
        gallery_name: sectionOf(b)
      });
    }

    if (b.closest(".cond-ticks")) {
      var ticks = Array.prototype.slice.call(
        b.closest(".cond-ticks").querySelectorAll("button"));
      return track("content_step", {
        step_index: ticks.indexOf(b) + 1,
        step_count: ticks.length,
        step_label: textOf(b) || b.getAttribute("aria-label") || ""
      });
    }

    /* The video poster is an <a data-video>, handled here because site.js
       swaps it for an iframe on click and the anchor has no href. */
    var v = b.closest("[data-video]");
    if (v) return onVideo(v);
  }

  /* The menu toggle, on the CAPTURE phase and nowhere else.

     Both this file and site.js listen for the same click on the bubble
     phase, and site.js registered first because it is the earlier <script>,
     so it flips `aria-expanded` before a bubble-phase reader here can see
     it. First attempt reported every open as a close and every close as an
     open -- exactly inverted, and perfectly plausible looking in a report.
     Capture runs before any of it. */
  d.addEventListener("click", guard(function (e) {
    var t = e.target.closest(".nav-toggle");
    if (!t) return;
    track("menu_toggle", {
      menu_state: t.getAttribute("aria-expanded") === "true" ? "close" : "open",
      viewport: menuIsPanel() ? "panel" : "bar"
    });
  }), true);

  /* CAPTURE, for the same reason the menu toggle is on capture. site.js
     registered its click handler first and adds `is-playing` inside it, so a
     bubble-phase reader here always sees the class already set and always
     skips. The `is-playing` test is what stops a second click on a playing
     video counting as a second start, and it is only true on capture. */
  d.addEventListener("click", guard(function (e) {
    var v = e.target.closest("[data-video]");
    if (v && !v.classList.contains("is-playing")) onVideo(v);
  }), true);

  function onVideo(v) {
    /* GA4's own recommended event and its own parameter names. Using them
       means this shows up in the Video engagement report rather than only
       in a custom exploration. */
    track("video_start", {
      video_title: clean(v.getAttribute("data-title") || textOf(v)),
      video_provider: "youtube",
      video_url: "https://www.youtube-nocookie.com/embed/" +
                 clean(v.getAttribute("data-video"), 40),
      video_current_time: 0
    });
  }

  /* ---------- the questions ----------
     `toggle` does not bubble, so this cannot be delegated off document the
     way the clicks are. Bound per element at ready, which is safe because
     every <details> on this site is in the served HTML and none is created
     later. site.js also listens here, to close the others; two listeners on
     one element do not interfere. */
  function wireDetails() {
    var all = Array.prototype.slice.call(d.querySelectorAll("details"));
    all.forEach(function (det, i) {
      det.addEventListener("toggle", guard(function () {
        if (!det.open) return;            /* closing is not a signal */
        var q = det.querySelector("summary");
        track("faq_open", {
          question_text: q ? textOf(q) : "",
          question_position: i + 1,
          question_count: all.length
        });
      }));
    });
  }

  /* ---------- the signup ----------
     The Flodesk form is a third-party widget that is injected after load, so
     this listens on the capture phase at document level: the widget calls
     preventDefault and submits over fetch, and a bubble-phase listener on a
     form that never natively submits can be skipped. Capture always sees it.

     `sign_up` is a GA4 recommended event. `method` names which list, because
     there will eventually be more than one. */
  var signalled = false;
  d.addEventListener("submit", guard(function (e) {
    var f = e.target;
    if (!f || f.tagName !== "FORM" || signalled) return;
    signalled = true;
    track("sign_up", {
      method: /flodesk/.test(f.action || "") ? "flodesk" : "form",
      form_destination: clean(f.getAttribute("action") || ""),
      form_location: sectionOf(f)
    });
  }), true);

  /* ---------- scroll depth ----------
     Fires once each at 25, 50, 75 and 100 per page load.

     ONLY ON PAGES LONG ENOUGH FOR IT TO MEAN ANYTHING. On a page that is
     barely taller than the window, 100% is reached by existing, and four
     events that always fire together are four events that say nothing. The
     gate is 1.5 viewports of scrollable content, which on this site keeps
     the eight long pages in and leaves /thequestions/ out, that being a
     single-screen card people scan at a table.

     Measured in a rAF off a passive listener, so nothing here can make a
     scroll janky: the handler sets a flag and returns, and the read happens
     once per frame at most. */
  var THRESHOLDS = [25, 50, 75, 100];
  var fired = {};
  var ticking = false;
  var armed = false;

  function docHeight() {
    var b = d.body, e = d.documentElement;
    return Math.max(b.scrollHeight, b.offsetHeight,
                    e.clientHeight, e.scrollHeight, e.offsetHeight);
  }

  function measure() {
    ticking = false;
    var vh = w.innerHeight || d.documentElement.clientHeight;
    var scrollable = docHeight() - vh;
    if (scrollable <= 0) return;

    var pct = ((w.pageYOffset || d.documentElement.scrollTop) / scrollable) * 100;
    /* Rounding up at the bottom: a page whose last pixel is unreachable
       because of a sub-pixel layout height would otherwise never report 100
       and every page on the site would look like nobody finished it. */
    if (pct > 99) pct = 100;

    for (var i = 0; i < THRESHOLDS.length; i++) {
      var t = THRESHOLDS[i];
      if (pct >= t && !fired[t]) {
        fired[t] = true;
        track("scroll_depth", {
          percent_scrolled: t,
          page_length_px: Math.round(docHeight()),
          viewports: Math.round((docHeight() / vh) * 10) / 10
        });
      }
    }
  }

  function onScroll() {
    if (!armed || ticking) return;
    ticking = true;
    /* rAF is the right place to read layout, and it is not guaranteed to
       run: a throttled or uncomposited frame can stop calling it entirely
       while scroll events keep arriving. Measured exactly that in headless
       Chrome. The timeout is the floor, `ran` makes sure only one of the two
       ever does the work, and 200ms is far below the time it takes a person
       to cross a threshold. */
    var ran = false;
    function once() { if (ran) return; ran = true; measure(); }
    if (w.requestAnimationFrame) w.requestAnimationFrame(once);
    w.setTimeout(once, 200);
  }

  function armScroll() {
    var vh = w.innerHeight || d.documentElement.clientHeight;
    armed = (docHeight() - vh) > vh * 1.5;
    if (!armed) return;
    w.addEventListener("scroll", onScroll, { passive: true });
    /* A reader who lands mid-page from an anchor link has already passed
       some of these. Measure once at rest so the first real scroll is not
       reporting four thresholds at once. */
    measure();
  }

  /* ---------- start ---------- */
  function ready() {
    wireDetails();
    armScroll();
    /* Images and web fonts change the height of every page on this site,
       and the scroll gate is a height comparison. Re-arming on load stops a
       page being judged short because it was measured before the hero
       image had a size. */
    w.addEventListener("load", guard(function () {
      if (!armed) armScroll();
    }));
  }

  if (d.readyState === "loading") {
    d.addEventListener("DOMContentLoaded", guard(ready));
  } else {
    ready();
  }
})(window, document);
