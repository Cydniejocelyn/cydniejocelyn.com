/* ============================================================
   Cydnie Jocelyn, the resurfacing business

   Every motion here is the same waterline doing something. Transforms and
   opacity only: no filters, no blend modes, no libraries.

   Nothing that affects whether content is visible is allowed to depend on
   IntersectionObserver or on animation frames arriving. Worst case the
   page is simply all there, in its final state.
   ============================================================ */
(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ---------- 0. Does a transition advance here? -------------
     One probe, once. Every reveal on this site fades in through a
     transition with a stagger delay on it, so in any browser where
     transitions do not advance, everything with a delay stays at
     opacity 0 forever. That is not hypothetical: it is sixteen of the
     twenty four revealed elements on a page, invisible.

     If the probe does not move, tweening is off wholesale and every
     element lands on its final state immediately. A page that arrives
     finished beats a page that never arrives. */
  function initTweenProbe() {
    var el = document.createElement("div");
    el.setAttribute("aria-hidden", "true");
    el.style.cssText = "position:fixed;left:-9999px;top:0;width:8px;height:8px;" +
                       "opacity:0;transition:opacity 300ms linear;pointer-events:none;";
    document.body.appendChild(el);
    void el.offsetWidth;
    el.style.opacity = "1";
    window.setTimeout(function () {
      if (parseFloat(window.getComputedStyle(el).opacity) <= 0.02) {
        document.documentElement.classList.add("no-tween");
      }
      if (el.parentNode) el.parentNode.removeChild(el);
    }, 260);
  }

  /* ---------- 1. Split a line into words -------------------- */
  function splitWords(el) {
    if (el.dataset.split === "done") return;
    var i = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.nodeValue.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var w = document.createElement("span"); w.className = "w";
            var inner = document.createElement("i");
            inner.textContent = part;
            inner.style.setProperty("--wd", (i * 40) + "ms");
            i++;
            w.appendChild(inner); frag.appendChild(w);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== "SPAN") {
          walk(n);
        }
      });
    })(el);
    el.dataset.split = "done";
  }

  /* ---------- 2. In view -------------------------------------
     A scroll and timer check rather than IntersectionObserver alone, plus
     a hard backstop, so a blocked observer can never leave the page blank. */
  var watchers = [];

  function watch(el, on, off, once) {
    watchers.push({ el: el, on: on, off: off, once: once !== false, active: false, done: false });
  }

  function pump() {
    var vh = window.innerHeight || document.documentElement.clientHeight;
    for (var i = 0; i < watchers.length; i++) {
      var w = watchers[i];
      if (w.done) continue;
      var r = w.el.getBoundingClientRect();
      var seen = r.bottom > vh * 0.06 && r.top < vh * 0.94 && (r.width > 0 || r.height > 0);
      if (seen && !w.active) {
        w.active = true; w.on();
        if (w.once) w.done = true;
      } else if (!seen && w.active && !w.once) {
        w.active = false; if (w.off) w.off();
      }
    }
  }

  function initReveals() {
    var targets = Array.prototype.slice.call(
      document.querySelectorAll(".r-up, .r-fade, .r-img, .split"));

    document.querySelectorAll("[data-stagger]").forEach(function (g) {
      var step = parseInt(g.dataset.stagger, 10) || 60;
      if (step > 60) step = 60;               /* the guide's ceiling */
      Array.prototype.slice.call(g.children).forEach(function (c, n) {
        c.style.setProperty("--d", (n * step) + "ms");
      });
    });

    var watcherWorks = false;
    targets.forEach(function (t) {
      watch(t, function () { t.classList.add("is-in"); watcherWorks = true; }, null, true);
    });

    /* The backstop used to reveal everything on the page at 2.6s. That is
       right for anything the reader can already see, and wrong for anything
       further down: the account on the about page is eight paragraphs, and
       blanket revealing them meant they were all already up before she got
       there, so nothing arrived as she read.

       So: at 2.6s reveal what is on screen or above it, which is the case
       the backstop actually exists for. Everything below the fold is left
       to the scroll watcher, with a long stop behind it in case the watcher
       never runs at all. Nothing can end up permanently invisible. */
    function revealAbove(limit) {
      var vh = window.innerHeight || document.documentElement.clientHeight;
      targets.forEach(function (t) {
        if (t.classList.contains("is-in")) return;
        if (t.getBoundingClientRect().top < vh * limit) t.classList.add("is-in");
      });
    }
    window.setTimeout(function () { revealAbove(1); }, 2600);

    /* The long stop only exists for a browser where the scroll watcher never
       runs. If the watcher has revealed anything at all it demonstrably
       works, and blanket revealing the rest would rob a slow reader of the
       arrival: eight paragraphs already up before she reached them. */
    window.setTimeout(function () {
      if (watcherWorks) return;
      targets.forEach(function (t) { t.classList.add("is-in"); });
    }, 12000);
  }

  /* ---------- 3. Header ------------------------------------- */
  function initHeader() {
    var hdr = document.querySelector(".hdr");
    if (!hdr) return;
    var light = Array.prototype.slice.call(document.querySelectorAll(".z-light, .z-silt"));
    var stuck = false, surfaced = false;

    function check() {
      var s = window.scrollY > 24;
      if (s !== stuck) { stuck = s; hdr.classList.toggle("is-stuck", s); }
      var edge = hdr.offsetHeight + 4;
      var up = light.some(function (z) {
        var r = z.getBoundingClientRect();
        return r.top <= edge && r.bottom > edge;
      });
      if (up !== surfaced) {
        surfaced = up;
        hdr.classList.toggle("is-surfaced", up);
        /* The gauge inverts on a light ground too, and its rules are written
           as a bare `.is-surfaced` descendant selector. The gauge is a
           SIBLING of the header, not a child of it, so those four rules
           never matched and the instrument stayed pale teal over every light
           section on the site. Mirroring the flag on the root makes them
           match. Every other is-surfaced rule is prefixed `.hdr`, so nothing
           else changes. This matters most on The Build, which is light from
           top to bottom apart from two bands. */
        document.documentElement.classList.toggle("is-surfaced", up);
      }
    }
    check();
    window.addEventListener("scroll", check, { passive: true });
    window.addEventListener("resize", check, { passive: true });
  }

  /* ---------- 4. The movement bar, parallax, and the pump -----
     The gauge reads how far up the reader has come: a vertical depth
     instrument on the side, not a rule across the top. Parallax is hard
     capped at 12px of travel. */
  var PAR_MAX = 12;

  function initScroll() {
    var fill = document.querySelector(".gauge-fill");
    var dot  = document.querySelector(".gauge-dot");
    var read = document.querySelector(".gauge-read");
    var pars = Array.prototype.slice.call(document.querySelectorAll(".par"));

    function frame() {
      if (fill) {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        var p = h > 0 ? Math.min(1, Math.max(0, window.scrollY / h)) : 0;
        fill.style.height = (p * 100) + "%";
        if (dot) dot.style.top = (p * 100) + "%";
        if (read) {
          var m = Math.max(0, Math.round((1 - p) * 40));
          read.textContent = m === 0 ? "Surface" : (m + "m");
        }
      }

      if (!reduce.matches) {
        var vh = window.innerHeight;
        pars.forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.bottom < -200 || r.top > vh + 200) return;
          var sp = parseFloat(el.dataset.speed || "0.08");
          var mid = (r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2);
          var y = mid * sp * -100;
          if (y >  PAR_MAX) y =  PAR_MAX;
          if (y < -PAR_MAX) y = -PAR_MAX;
          el.style.setProperty("--py", y.toFixed(2) + "px");
        });
      }
      pump();
    }

    frame();
    window.addEventListener("scroll", frame, { passive: true });
    window.addEventListener("resize", frame, { passive: true });

    var n = 0;
    (function early() { pump(); if (++n < 40) window.setTimeout(early, 120); })();
  }

  /* ---------- 5. Fifteen, filled by the scroll ---------------
     Fourteen come in as she passes and the fifteenth stays open. It used to
     be a point of light travelling the ring forever, which is a loop, and
     nothing on this site loops. This resolves once: it fills on the way
     down and it stays filled.

     The empty state and the `is-counting` class arrive together, inside the
     watcher, so the ring is never sitting empty waiting for a frame that
     may never come. A backstop fills it whatever happens. */
  function initFifteen() {
    var fig = document.querySelector(".fifteen-fig");
    if (!fig) return;
    var dots = Array.prototype.slice.call(fig.querySelectorAll(".dot:not(.is-her)"));
    if (!dots.length) return;

    /* Ring order from just past the open one, clockwise, so the count runs
       all the way round and stops at the circle that stays open. */
    var CX = 80, CY = 80, TWO = Math.PI * 2;
    dots.sort(function (a, b) {
      function ang(d) {
        var t = Math.atan2(parseFloat(d.getAttribute("cx")) - CX,
                          -(parseFloat(d.getAttribute("cy")) - CY));
        return t < 0 ? t + TWO : t;
      }
      return ang(a) - ang(b);
    });

    function fillAll() {
      dots.forEach(function (d) { d.classList.add("is-filled"); });
    }

    if (reduce.matches) return;          /* the resting ring is the whole mark */

    var live = false;

    function frame() {
      var r = fig.getBoundingClientRect();
      var vh = window.innerHeight || 1;
      /* Nought when the figure's top reaches the bottom of the screen, one
         by the time it is well up the screen. The divisor is the whole dial:
         it is the scroll distance the fourteen take to come in, so smaller
         is faster. Was 0.62vh + 0.5h, which ran about 700px on a phone and
         read as sluggish. */
      var p = (vh - r.top) / (vh * 0.38 + r.height * 0.30);
      p = Math.max(0, Math.min(1, p));
      var n = Math.round(p * dots.length);
      dots.forEach(function (d, i) { d.classList.toggle("is-filled", i < n); });
    }

    watch(fig, function () {
      if (live) return;
      live = true;
      fig.classList.add("is-counting");
      frame();                                   /* never a blank first paint */
      window.addEventListener("scroll", frame, { passive: true });
      window.addEventListener("resize", frame, { passive: true });
    }, null, true);

    /* If the watcher never reports, or frames never arrive, the mark is
       still the mark. */
    window.setTimeout(function () {
      if (!live) return;
      var any = dots.some(function (d) { return d.classList.contains("is-filled"); });
      if (!any) fillAll();
    }, 2600);
  }

  /* ---------- 5b. The breath, driven by the scroll -----------
     Three bubbles leave the dark and go up to break the surface, once, as
     the reader crosses the band. Written as a direct style, because a
     transition may never advance here and a keyframe would be a loop. */
  /* ---------- 5b. The breath ---------------------------------
     All this does is add the class. The rise itself is a CSS keyframe,
     because keyframes are the one kind of motion that can be relied on to
     advance in this build: transitions do not, and animation frames do not
     always arrive. Three earlier versions of this were driven by rAF and
     never moved for anyone.

     One iteration, forwards, and then it is done. Nothing loops. */
  function initBreath() {
    var band = document.querySelector(".rise-band");
    if (!band) return;
    if (!band.querySelector(".bub")) return;
    watch(band, function () { band.classList.add("is-breathing"); }, null, true);
  }

  /* ---------- 5c. The menu ----------------------------------
     Under 56rem the links become a panel behind a two bar mark. `has-menu`
     on the root is what turns the collapsing CSS on, and it is only set
     here, so a phone with no JS gets the links as a plain stacked list
     rather than no navigation at all. */
  function initNav() {
    var btn = document.querySelector(".nav-toggle");
    var menu = document.getElementById("nav-menu");
    if (!btn || !menu) return;

    document.documentElement.classList.add("has-menu");

    var open = false;
    var wide = window.matchMedia("(min-width: 56rem)");

    function set(next) {
      if (next === open) return;
      open = next;
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      menu.classList.toggle("is-open", open);
      /* the movement bar is fixed to the edge and would sit over the panel */
      document.documentElement.classList.toggle("menu-open", open && !wide.matches);
      /* the page behind must not scroll under an open panel */
      document.body.style.overflow = open && !wide.matches ? "hidden" : "";
    }

    btn.addEventListener("click", function () { set(!open); });

    /* a link is a destination: take the panel down on the way */
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) set(false);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape" || !open) return;
      set(false);
      btn.focus();
    });

    /* tab out of the panel, or click past it, and it closes */
    document.addEventListener("focusin", function (e) {
      if (!open) return;
      if (menu.contains(e.target) || btn.contains(e.target)) return;
      set(false);
    });
    document.addEventListener("click", function (e) {
      if (!open) return;
      if (menu.contains(e.target) || btn.contains(e.target)) return;
      set(false);
    });

    /* rotating to landscape past the breakpoint must not leave the body
       locked with a panel that is no longer on screen */
    function sync() { if (wide.matches) set(false); }
    if (wide.addEventListener) wide.addEventListener("change", sync);
    else if (wide.addListener) wide.addListener(sync);
    window.addEventListener("resize", sync, { passive: true });
  }

  /* ---------- 6. The hero waterline -------------------------
     There is no drawn rule in the hero any more. The photograph carries a
     real surface line at roughly 24% and the headline is centred, so the two
     could not be held to one height across viewports, and shipping both at
     different heights is the one thing that must not happen. This is now
     only the parallax. */
  function initHero() {
    var hero = document.querySelector(".hero");
    if (!hero) return;
    var img = hero.querySelector(".hero-water img");
    if (!img) return;

    /* 12px of travel, no more */
    if (reduce.matches) return;
    window.addEventListener("scroll", function () {
      var r = hero.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var p = Math.max(-1, Math.min(1, -r.top / (r.height || 1)));
      img.style.transform = "translate3d(0," + (p * 12).toFixed(2) + "px,0)";
    }, { passive: true });
  }

  /* ---------- 7, 8, 9. Removed ------------------------------
     The scroll progress bar, the sticky bottom bar and the slide in letter
     nudge are all out. A thin rule at the top that changes length reads as
     a waterline that moves; a sticky bar and a nudge are both forms of the
     manufactured urgency this brand does not use. The booking link stands
     on its own in the nav, in the hero and once at the close, and the
     letter is offered in the page, in the places it belongs. */

  /* ---------- 10. The condition, one recognition at a time ---
     The section holds a track five screens tall with a pinned stage
     inside it, so scrolling the page walks the five instead of scrolling
     past them. The page never stops moving under the reader: no wheel is
     swallowed, no scroll is retimed, and the scrollbar keeps telling the
     truth. All this does is read how far into the track we are and light
     the recognition that belongs there.

     Nothing here decides whether the words exist. The markup is the plain
     list of all five; `is-stepped` is added only when there is room for
     the stepped reading, and removing it puts the list straight back. */
  function initCondition() {
    var sec = document.querySelector(".cond");
    if (!sec) return;

    var track = sec.querySelector(".cond-track");
    var stage = sec.querySelector(".cond-stage");
    var slots = sec.querySelector(".cond-slots");
    var fill  = sec.querySelector(".cond-gauge span");
    var items = Array.prototype.slice.call(sec.querySelectorAll(".cond-item"));
    var ticks = Array.prototype.slice.call(sec.querySelectorAll(".cond-ticks button"));
    if (!track || !stage || !slots || items.length < 2) return;

    var N = items.length, on = false, cur = -1;
    /* the track runs half a step past the last recognition, so the fifth
       gets held rather than swept away the instant it arrives */
    var TAIL = 0.5, SPAN = N + TAIL;
    sec.style.setProperty("--cond-steps", N);
    sec.style.setProperty("--cond-tail", TAIL);

    /* a pin needs a screen tall enough to be worth pinning */
    function roomy() { return !reduce.matches && window.innerHeight >= 520; }

    /* the five are stacked on one another, so nothing gives the stack its
       height any more. Measure the tallest and hold that. */
    function measure() {
      var h = 0;
      for (var i = 0; i < items.length; i++) {
        h = Math.max(h, items[i].getBoundingClientRect().height);
      }
      if (h) slots.style.setProperty("--cond-h", Math.ceil(h) + "px");
    }

    function light(i) {
      if (i === cur) return;
      cur = i;
      items.forEach(function (el, n) {
        el.classList.toggle("is-on", n === i);
        el.classList.toggle("is-past", n < i);
      });
      ticks.forEach(function (b, n) {
        if (n === i) b.setAttribute("aria-current", "true");
        else b.removeAttribute("aria-current");
      });
    }

    /* how far through the track the pin has travelled, 0 to 1 */
    function progress() {
      var r = track.getBoundingClientRect();
      var run = r.height - stage.offsetHeight;
      if (run <= 0) return 0;
      return Math.min(1, Math.max(0, -r.top / run));
    }

    function frame() {
      if (!on) return;
      var p = progress() * SPAN;
      /* the gauge reads the five, not the tail: full once the fifth is up */
      if (fill) fill.style.transform = "scaleX(" + Math.min(1, p / N).toFixed(4) + ")";
      light(Math.min(N - 1, Math.floor(p)));
    }

    /* a tick is a real destination: it scrolls the page to the middle of
       that step rather than jumping the state out from under the scroll */
    function goto(n) {
      if (!on) { items[n].scrollIntoView({ block: "center" }); return; }
      var r = track.getBoundingClientRect();
      var run = r.height - stage.offsetHeight;
      if (run <= 0) return;
      window.scrollTo({
        top: window.scrollY + r.top + run * ((n + 0.5) / SPAN),
        behavior: reduce.matches ? "auto" : "smooth"
      });
    }

    function enable() {
      if (on) return;
      on = true; cur = -1;
      sec.classList.add("is-stepped");
      measure();
      frame();
    }

    function disable() {
      if (!on) return;
      on = false; cur = -1;
      sec.classList.remove("is-stepped");
      items.forEach(function (el) { el.classList.remove("is-on", "is-past"); });
      ticks.forEach(function (b) { b.removeAttribute("aria-current"); });
      if (fill) fill.style.transform = "";
    }

    ticks.forEach(function (b, n) {
      b.addEventListener("click", function () { goto(n); });
      b.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" || e.key === "ArrowDown" ? 1
              : e.key === "ArrowLeft"  || e.key === "ArrowUp"   ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var m = Math.min(N - 1, Math.max(0, n + d));
        ticks[m].focus();
        goto(m);
      });
    });

    function sync() {
      if (roomy()) { enable(); measure(); frame(); } else { disable(); }
    }

    sync();
    window.addEventListener("scroll", frame, { passive: true });
    window.addEventListener("resize", sync, { passive: true });
    window.addEventListener("load", function () { measure(); frame(); });

    /* type and images settle late; re-measure a few times, then stop */
    var n = 0;
    (function settle() {
      if (on) { measure(); frame(); }
      if (++n < 12) window.setTimeout(settle, 200);
    })();

    if (reduce.addEventListener) reduce.addEventListener("change", sync);
    else if (reduce.addListener) reduce.addListener(sync);
  }

  /* ---------- 11. Before you book ---------------------------
     Four worries, four answers. The markup is the pairs, all of them
     readable with no JS at all; this turns them into a picker and one
     panel, so the reader answers the objection she actually has rather
     than reading past three she does not.

     A tablist, by the book: one tab in the tab order, arrows to move,
     Home and End to the ends. Nothing here decides whether the words
     exist, only which one is in front. */
  function initReversal() {
    Array.prototype.slice.call(document.querySelectorAll("[data-reversal]"))
      .forEach(buildReversal);
  }

  function buildReversal(host) {
    var revs = Array.prototype.slice.call(host.querySelectorAll(".rev"));
    if (revs.length < 2) return;

    var picks = document.createElement("div");
    picks.className = "rev-picks";
    picks.setAttribute("role", "tablist");
    picks.setAttribute("aria-label", host.dataset.label || "Choose one");

    var panels = document.createElement("div");
    panels.className = "rev-panels";

    var tabs = [], pans = [];

    revs.forEach(function (rev, i) {
      var q = rev.querySelector(".rev-q");
      var a = rev.querySelector(".rev-a");
      if (!q || !a) return;
      var id = "rev-" + i;

      var b = document.createElement("button");
      b.type = "button";
      b.className = "rev-pick";
      b.id = id + "-t";
      b.setAttribute("role", "tab");
      b.setAttribute("aria-controls", id + "-p");
      var mark = document.createElement("span");
      mark.className = "rev-mark";
      mark.setAttribute("aria-hidden", "true");
      var label = document.createElement("span");
      label.textContent = q.textContent;
      b.appendChild(mark);
      b.appendChild(label);
      picks.appendChild(b);
      tabs.push(b);

      a.id = id + "-p";
      a.setAttribute("role", "tabpanel");
      a.setAttribute("aria-labelledby", id + "-t");
      a.setAttribute("tabindex", "0");
      panels.appendChild(a);          /* moves it out of the pair wrapper */
      pans.push(a);
    });

    if (tabs.length < 2) return;

    /* the pair wrappers have given up their contents; clear what is left */
    while (host.firstChild) host.removeChild(host.firstChild);
    host.appendChild(picks);
    host.appendChild(panels);
    host.classList.add("is-live");

    /* The lede in the markup does not tell anyone to pick, because with no
       JS there is nothing to pick. Now there is, so say so. Scoped to this
       picker's own section, and each picker carries its own line. */
    var sec = host.closest("section");
    var lede = sec && sec.querySelector(".ready-lede");
    if (lede && host.dataset.lede) lede.textContent = host.dataset.lede;

    /* Hold the panel at the height of the longest answer. Measured with
       all of them shown, because a hidden one has no height to read. */
    function measure() {
      panels.style.removeProperty("--rev-h");
      var cs = window.getComputedStyle(panels);
      /* The box is border-box, so a min-height of the answer alone would
         reserve the answer minus the padding and the rule above it, and
         the longest answer would still push the box open. */
      var chrome = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom)
                 + parseFloat(cs.borderTopWidth) + parseFloat(cs.borderBottomWidth);
      var h = 0;
      pans.forEach(function (p) {
        var was = p.hidden;
        p.hidden = false;
        h = Math.max(h, p.getBoundingClientRect().height);
        p.hidden = was;
      });
      if (h) panels.style.setProperty("--rev-h", Math.ceil(h + chrome) + "px");
    }

    var cur = -1;
    function select(i, moveFocus) {
      if (i === cur) { if (moveFocus) tabs[i].focus(); return; }
      cur = i;
      tabs.forEach(function (t, n) {
        var on = n === i;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.setAttribute("tabindex", on ? "0" : "-1");
      });
      pans.forEach(function (p, n) {
        var on = n === i;
        p.hidden = !on;
        p.setAttribute("aria-hidden", on ? "false" : "true");
      });
      if (moveFocus) tabs[i].focus();
    }

    tabs.forEach(function (b, i) {
      b.addEventListener("click", function () { select(i); });
      b.addEventListener("keydown", function (e) {
        var last = tabs.length - 1, n = null;
        if (e.key === "ArrowDown" || e.key === "ArrowRight") n = i === last ? 0 : i + 1;
        else if (e.key === "ArrowUp" || e.key === "ArrowLeft") n = i === 0 ? last : i - 1;
        else if (e.key === "Home") n = 0;
        else if (e.key === "End") n = last;
        if (n === null) return;
        e.preventDefault();
        select(n, true);
      });
    });

    measure();
    select(0);
    window.addEventListener("resize", measure, { passive: true });

    /* the faces settle after this runs, and the tallest answer can change
       line count when they do */
    var n = 0;
    (function settle() { measure(); if (++n < 12) window.setTimeout(settle, 200); })();
  }

  /* ---------- 12. Proof, one at a time ----------------------
     A carousel that can be dragged, stepped or keyed. Every quote stays
     in the document and in the accessibility tree the whole time; this
     only decides which one is in front, so a failed script leaves the
     plain stack of all of them rather than hiding the proof.

     Position comes from measuring where each slide actually sits, not
     from multiplying an assumed width, so it survives a resize, a font
     swapping in late, and quotes of different lengths. */
  function initQuotes() {
    var host = document.querySelector("[data-quotes]");
    if (!host) return;
    var figs = Array.prototype.slice.call(host.querySelectorAll(".quote"));
    if (figs.length < 2) return;

    var N = figs.length, cur = 0;

    var view = document.createElement("div");
    view.className = "q-view";
    view.tabIndex = 0;
    view.setAttribute("role", "group");
    view.setAttribute("aria-roledescription", "carousel");
    view.setAttribute("aria-label", "What people said");

    var track = document.createElement("div");
    track.className = "q-track";

    figs.forEach(function (f, i) {
      f.classList.add("q-slide");
      f.setAttribute("role", "group");
      f.setAttribute("aria-roledescription", "slide");
      f.setAttribute("aria-label", (i + 1) + " of " + N);
      track.appendChild(f);
    });
    view.appendChild(track);

    var bar = document.createElement("div");
    bar.className = "q-bar";

    function arrow(dir, label) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "q-arrow";
      b.setAttribute("data-dir", String(dir));
      b.setAttribute("aria-label", label);
      b.innerHTML = '<svg width="22" height="10" viewBox="0 0 22 10" fill="none" aria-hidden="true">' +
        '<path d="' + (dir === 1 ? "M16 1l5 4-5 4M21 5H0" : "M6 1L1 5l5 4M1 5h21") +
        '" stroke="currentColor" stroke-width="1.2"/></svg>';
      b.addEventListener("click", function () { goTo(cur + dir); });
      return b;
    }
    var prev = arrow(-1, "Previous quote");
    var next = arrow(1, "Next quote");

    var dots = document.createElement("div");
    dots.className = "q-dots";
    var dotEls = figs.map(function (f, i) {
      var d = document.createElement("button");
      d.type = "button";
      d.className = "q-dot";
      d.setAttribute("aria-label", "Quote " + (i + 1));
      d.addEventListener("click", function () { goTo(i); });
      dots.appendChild(d);
      return d;
    });

    var count = document.createElement("p");
    count.className = "q-count";
    count.setAttribute("aria-hidden", "true");

    bar.appendChild(prev);
    bar.appendChild(dots);
    bar.appendChild(next);
    bar.appendChild(count);

    while (host.firstChild) host.removeChild(host.firstChild);
    host.appendChild(view);
    host.appendChild(bar);
    host.classList.add("is-live");

    /* TWO CAROUSELS, AND THE SECOND ONE IS THE BROWSER'S.

       On a mouse this drags a transform under the pointer, which is exactly
       right: there is no competing gesture, and one to one tracking with a
       snap on release feels like handling the thing.

       On a touch screen it was wrong in a way that could not be tuned out.
       `pointerdown` captured the pointer and `pointermove` moved the track by
       raw dx with no axis lock, so a vertical flick that started anywhere on
       a review dragged it sideways by whatever few pixels the thumb wandered
       while the page scrolled underneath. Then `touch-action: pan-y` did its
       job, the browser claimed the gesture as a scroll, fired
       `pointercancel`, and the release handler animated the track back. Jerk,
       then snap, on every scroll past the section.

       So on a coarse pointer none of that runs. The view becomes a real
       horizontal scroller with CSS scroll snapping and the browser owns the
       gesture: it decides the axis, it carries the momentum, and it cannot
       fight itself. The JS only listens, to keep the dots and the dimming in
       step with wherever the scroll ended up.

       Nothing below changes the desktop path. */
    var coarse = window.matchMedia("(pointer: coarse)");
    var native = coarse.matches;
    if (native) host.classList.add("q-native");

    /* Snapping centres a slide in the scrollport, and the first and last
       cannot centre without something to scroll past. This is that
       something, measured rather than guessed because the slide is
       `min(42rem, 80vw)` and the view is whatever the gutter leaves.

       The leading side is padding and the trailing side is a real element.
       Trailing padding on a flex scroll container is not reliably counted in
       `scrollWidth`, so the scroller runs out before the last review reaches
       the middle: it ended up sitting about 19px right of centre, which on a
       350px column is enough to look like a bug. A spacer is an actual flex
       item and is always counted. */
    var tail = null;
    function padTrack() {
      if (!native) return;
      var slack = Math.max(0, (view.clientWidth - figs[0].offsetWidth) / 2);
      track.style.paddingInline = "0px";
      track.style.paddingLeft = slack + "px";
      if (!tail) {
        tail = document.createElement("span");
        tail.setAttribute("aria-hidden", "true");
        tail.style.cssText = "flex:0 0 auto;align-self:stretch";
        track.appendChild(tail);
      }
      tail.style.width = slack + "px";
    }

    function pad(n) { return (n < 10 ? "0" : "") + n; }

    /* where the track has to sit for slide i to be centred in the view */
    function xFor(i) {
      var s = figs[i];
      return Math.round(view.clientWidth / 2 - (s.offsetLeft + s.offsetWidth / 2));
    }

    /* The transition is the nice part, not the load bearing part. A
       transition that never receives a frame leaves the track wherever it
       started, which strands the reader on one quote with no way to reach
       the others, so this checks where it actually landed and forces it
       if it did not get there. Same reasoning as the reveal backstop. */
    var landT = 0;
    function place(x, animate) {
      window.clearTimeout(landT);
      track.style.transition = animate ? "" : "none";
      track.style.transform = "translate3d(" + x + "px,0,0)";
      if (!animate) return;
      landT = window.setTimeout(function () {
        var m = window.getComputedStyle(track).transform;
        var at = m.indexOf("matrix") === 0 ? parseFloat(m.slice(m.indexOf("(") + 1).split(",")[4]) : 0;
        if (Math.abs(at - x) < 1) return;
        /* It did not land. Tweening does not work here, and the same is
           true of the opacity that tells the reader which quote is live,
           so give it up wholesale rather than forcing one property. */
        host.classList.add("q-instant");
        track.style.transition = "none";
        track.style.transform = "translate3d(" + x + "px,0,0)";
      }, 700);
    }

    /* Everything that says which review you are on, and nothing that moves
       anything. Split out because the native scroller has to be able to
       repaint from a scroll event without scrolling again and looping. */
    function paint(i) {
      cur = i;
      figs.forEach(function (f, n) { f.classList.toggle("is-on", n === i); });
      dotEls.forEach(function (d, n) {
        if (n === i) d.setAttribute("aria-current", "true");
        else d.removeAttribute("aria-current");
      });
      prev.disabled = i === 0;
      next.disabled = i === N - 1;
      count.textContent = pad(i + 1) + " / " + pad(N);
    }

    /* Where the scroller has to sit for slide i to be centred.

       Measured off rectangles rather than `offsetLeft`, which is relative to
       the nearest POSITIONED ancestor and not to the scroller. Nothing
       between a slide and `.wrap` is positioned, so `offsetLeft` came back
       measured from the wrap and every target was about 60px out: the arrows
       scrolled to not-quite-a-slide and the snap dragged it the rest of the
       way, which looked like the carousel arguing with itself. Rects do not
       care what is positioned. */
    function scrollFor(i) {
      var s = figs[i].getBoundingClientRect();
      var v = view.getBoundingClientRect();
      return Math.round(view.scrollLeft + (s.left - v.left) - (v.width - s.width) / 2);
    }

    function goTo(i, animate) {
      i = Math.max(0, Math.min(N - 1, i));
      paint(i);
      if (native) {
        var opts = { left: scrollFor(i) };
        /* `smooth` is honoured unless the reader has asked for less, and a
           carousel that jumps is still a carousel that works. */
        if (animate !== false && !reduce.matches) opts.behavior = "smooth";
        if (view.scrollTo) view.scrollTo(opts); else view.scrollLeft = opts.left;
        return;
      }
      place(xFor(i), animate !== false);
    }

    /* The scroll is the source of truth in native mode. rAF because a
       momentum scroll fires this a lot, and repainting five slides on every
       one of those is how a smooth scroll turns into a stuttering one. */
    var lastScroll = 0;
    if (native) {
      var pending = false;

      function syncFromScroll() {
        pending = false;
        var at = view.scrollLeft, best = 0, bestD = Infinity;
        for (var i = 0; i < N; i++) {
          var dd = Math.abs(scrollFor(i) - at);
          if (dd < bestD) { bestD = dd; best = i; }
        }
        if (best !== cur) paint(best);
      }

      view.addEventListener("scroll", function () {
        lastScroll = Date.now();
        if (pending) return;
        pending = true;

        /* Throttled, because a momentum scroll fires this a lot and
           repainting five slides on every one of those is how a smooth
           scroll turns into a stuttering one.

           rAF where it runs, and a timer behind it where it does not.
           requestAnimationFrame does not tick in a frame the compositor has
           stopped drawing -- a background tab, an offscreen iframe, a device
           saving power -- and the first version of this held `pending` true
           waiting for a frame that was never coming. The dots then stopped
           following the scroll permanently, for the rest of the page's life,
           and only in the conditions nobody tests in. Whichever arrives
           first wins and the other becomes a no-op. */
        var done = false;
        function run() { if (done) return; done = true; syncFromScroll(); }
        if (window.requestAnimationFrame) window.requestAnimationFrame(run);
        window.setTimeout(run, 120);
      }, { passive: true });
    }

    /* --- drag. Follows the pointer one to one, then snaps to whichever
       slide the release landed nearest. --- */
    var down = false, startX = 0, baseX = 0, dx = 0;

    if (!native) {
    view.addEventListener("pointerdown", function (e) {
      if (e.button) return;
      down = true; dx = 0;
      startX = e.clientX;
      baseX = xFor(cur);
      if (view.setPointerCapture) { try { view.setPointerCapture(e.pointerId); } catch (err) {} }
      view.classList.add("is-dragging");
      place(baseX, false);
    });

    view.addEventListener("pointermove", function (e) {
      if (!down) return;
      dx = e.clientX - startX;
      place(baseX + dx, false);
    });

    function release() {
      if (!down) return;
      down = false;
      view.classList.remove("is-dragging");
      /* a third of a slide is a decision; less than that is a wobble */
      var step = figs[cur].offsetWidth * 0.33;
      var to = cur;
      if (dx <= -step) to = cur + 1;
      else if (dx >= step) to = cur - 1;
      goTo(to);
    }
    view.addEventListener("pointerup", release);
    view.addEventListener("pointercancel", release);
    view.addEventListener("lostpointercapture", release);

    view.addEventListener("keydown", function (e) {
      var to = null;
      if (e.key === "ArrowRight" || e.key === "ArrowDown") to = cur + 1;
      else if (e.key === "ArrowLeft" || e.key === "ArrowUp") to = cur - 1;
      else if (e.key === "Home") to = 0;
      else if (e.key === "End") to = N - 1;
      if (to === null) return;
      e.preventDefault();
      goTo(to);
    });

    /* a slide dragged half off screen must not drag the page with it */
    view.addEventListener("dragstart", function (e) { e.preventDefault(); });
    }

    padTrack();
    goTo(0, false);
    window.addEventListener("resize", function () {
      padTrack();
      goTo(cur, false);
    }, { passive: true });

    /* the faces land after this runs and every width moves when they do */
    var n = 0;
    (function settle() {
      /* Re-centring under the reader's thumb mid-flick is its own glitch,
         and this loop runs every 200ms for two and a half seconds while the
         webfonts land. In native mode it waits for the scroller to be still
         first; a momentum scroll keeps stamping `lastScroll`, so "still"
         means the reader has actually stopped. */
      var busy = native && (Date.now() - lastScroll) < 500;
      if (!down && !busy) { padTrack(); goTo(cur, false); }
      if (++n < 12) window.setTimeout(settle, 200);
    })();
  }

  /* ---------- 13. FAQ, one at a time ------------------------ */
  function initFaq() {
    var all = Array.prototype.slice.call(document.querySelectorAll(".faq details"));
    all.forEach(function (d) {
      d.addEventListener("toggle", function () {
        if (!d.open) return;
        all.forEach(function (o) { if (o !== d) o.open = false; });
      });
    });
  }

  /* ---------- 14. The waterline rules -----------------------
     About's head rule draws in on load like the hero's does. The class is
     taken off after a second whether or not the animation ever ran, so the
     rule ends up drawn either way: a keyframe from scaleX(0) would
     otherwise leave it invisible for as long as it sat on its first frame. */
  /* Waterline rules draw left to right, 900ms, once. On load in the head,
     on entry everywhere else. The resting state is the drawn one, so a
     browser that never advances the animation still shows the rule. */
  function initRules() {
    var rules = Array.prototype.slice.call(document.querySelectorAll(".wl-rule"));
    if (!rules.length || reduce.matches) return;

    function draw(r) {
      r.classList.add("is-drawing");
      window.setTimeout(function () { r.classList.remove("is-drawing"); }, 1000);
    }

    rules.forEach(function (r) {
      if (r.closest(".ab-head, .hero")) draw(r);
      else watch(r, function () { draw(r); }, null, true);
    });
  }

  /* ---------- 15. The video ---------------------------------
     Melissa's review, and nothing from YouTube is fetched until she asks
     for it. The markup is an anchor to the video with the real first frame
     as its poster, so with no JS at all it is a working link; here it is
     turned into a player in place.

     The poster is the true 9:16 frame, cropped out of YouTube's padded
     plate. She recorded it on her phone in her car. Framing that as a wide
     player would promise a production that does not exist. */
  function initVideo() {
    Array.prototype.slice.call(document.querySelectorAll("[data-video]"))
      .forEach(function (a) {
        a.addEventListener("click", function (e) {
          if (a.classList.contains("is-playing")) return;
          e.preventDefault();
          var f = document.createElement("iframe");
          f.src = "https://www.youtube-nocookie.com/embed/" + a.dataset.video +
                  "?autoplay=1&start=" + (a.dataset.start || "0") +
                  "&rel=0&modestbranding=1&playsinline=1";
          f.title = a.dataset.title || "Video";
          /* `allow` is a delegation of this page's permissions to a frame on
             a domain we do not control, so it lists what a video needs and
             nothing else. Dropped from the snippet YouTube hands out:
             `clipboard-write`, which lets the frame write to the reader's
             clipboard and has nothing to do with playing a video, and
             `accelerometer` and `gyroscope`, which are motion sensors that
             only matter for 360-degree footage. None of the embeds here are
             360. `encrypted-media` stays because DRM playback needs it and
             `picture-in-picture` stays because readers use it.

             `referrerpolicy` stops the full URL of the page going to Google
             with the embed request; they get the origin, which is all the
             embed needs to work. */
          f.allow = "autoplay; encrypted-media; picture-in-picture";
          f.referrerPolicy = "strict-origin-when-cross-origin";
          f.setAttribute("allowfullscreen", "");
          a.classList.add("is-playing");
          a.innerHTML = "";
          a.appendChild(f);
        });
      });
  }

  /* ---------- 16. The gallery ------------------------------
     Armonia sent a folder of photographs and the property is most of what
     a woman is deciding about, so they open. The markup is plain figures;
     this adds the control and the lightbox, and `is-live` is only added
     once both exist, so nothing on the page advertises an interaction that
     is not there.

     One lightbox for the page, built once and reused. Escape and the arrow
     keys work, focus goes into it and comes back to the tile that opened
     it, and the page behind it does not scroll. */
  function initGallery() {
    var gals = Array.prototype.slice.call(document.querySelectorAll("[data-gallery]"));
    if (!gals.length) return;

    var shots = [];
    gals.forEach(function (g) {
      /* .rt-shot is the grid tile, .gal-item is the rail tile. Both open. */
      Array.prototype.slice.call(g.querySelectorAll(".rt-shot, .gal-item")).forEach(function (fig) {
        var img = fig.querySelector("img");
        if (!img) return;
        var cap = fig.querySelector("figcaption");
        var i = shots.length;
        shots.push({
          src: fig.dataset.full || img.currentSrc || img.src,
          alt: img.getAttribute("alt") || "",
          cap: cap ? cap.textContent.trim() : "",
          fig: fig
        });
        var b = document.createElement("button");
        b.type = "button";
        /* This label used to be built with innerHTML and a `+`. The caption
           it interpolates arrives as `figcaption.textContent`, which is
           already decoded, so writing it back as HTML re-parses it: a
           caption containing an ampersand or an angle bracket would come out
           wrong, and a caption is exactly the kind of copy that eventually
           contains "R&D" or a measurement in inches. Nothing on this site is
           reader-supplied, so this was never an injection -- it is a decode
           round trip, and building the node instead of the string removes
           the whole question rather than escaping it. */
        var vh = document.createElement("span");
        vh.className = "vh";
        vh.textContent = "Open: " + (cap ? cap.textContent.trim() : "photograph");
        b.appendChild(vh);
        /* the control is passed in rather than read off document.activeElement:
           a click does not always leave focus on what was clicked, and closing
           to a focus ring on <body> puts the reader back at the top of the
           page rather than at the picture she was looking at */
        b.addEventListener("click", function () { open(i, b); });
        fig.appendChild(b);
        fig.classList.add("is-live");
        /* the tile only claims to be openable once it demonstrably is */
        if (!fig.hasAttribute("data-cursor")) {
          fig.setAttribute("data-cursor", fig.closest("[data-rail]") ? "Open" : "View");
        }
      });
    });
    if (!shots.length) return;

    var box = document.createElement("div");
    box.className = "lbx";
    box.hidden = true;
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "Photograph");
    box.innerHTML =
      '<div class="lbx-stage"><img alt=""></div>' +
      '<div class="lbx-bar">' +
        '<p class="lbx-cap"></p>' +
        '<div class="lbx-nav">' +
          '<button type="button" data-go="-1" aria-label="Previous photograph">' +
            '<svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M5 1L1 5l4 4M1 5h13" stroke="currentColor" stroke-width="1.2"/></svg></button>' +
          '<button type="button" data-go="1" aria-label="Next photograph">' +
            '<svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M13 5H0" stroke="currentColor" stroke-width="1.2"/></svg></button>' +
        '</div>' +
      '</div>' +
      '<button type="button" class="lbx-x" aria-label="Close">' +
        '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="1.2"/></svg></button>';
    document.body.appendChild(box);

    var stage = box.querySelector(".lbx-stage img");
    var cap   = box.querySelector(".lbx-cap");
    var back  = null, at = 0;

    function show(i) {
      at = (i + shots.length) % shots.length;
      var s = shots[at];
      stage.src = s.src;
      stage.alt = s.alt;
      cap.textContent = s.cap;
    }

    function open(i, from) {
      back = from || document.activeElement;
      show(i);
      box.hidden = false;
      document.documentElement.style.overflow = "hidden";
      box.querySelector(".lbx-x").focus();
    }

    function close() {
      box.hidden = true;
      document.documentElement.style.overflow = "";
      /* back to the tile she came from, not to the top of the page */
      if (back && back.focus) back.focus();
    }

    box.querySelector(".lbx-x").addEventListener("click", close);
    Array.prototype.slice.call(box.querySelectorAll("[data-go]")).forEach(function (b) {
      b.addEventListener("click", function () { show(at + parseInt(b.dataset.go, 10)); });
    });
    /* the ground around the picture closes it, the picture itself does not */
    box.addEventListener("click", function (e) {
      if (e.target === box || e.target.classList.contains("lbx-stage")) close();
    });
    document.addEventListener("keydown", function (e) {
      if (box.hidden) return;
      if (e.key === "Escape") { e.preventDefault(); close(); }
      else if (e.key === "ArrowRight") { e.preventDefault(); show(at + 1); }
      else if (e.key === "ArrowLeft")  { e.preventDefault(); show(at - 1); }
      else if (e.key === "Tab") {
        /* three controls, so the trap is a cycle rather than a calculation */
        var f = Array.prototype.slice.call(box.querySelectorAll("button"));
        var n = f.indexOf(document.activeElement);
        e.preventDefault();
        f[(n + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
      }
    });
  }

  /* ---------- 16b. The property rail ------------------------
     A real overflow container with scroll snapping, so it already works
     before this runs: a touch screen scrolls it, a keyboard tabs through
     it, and a reader with no JS loses nothing but the arrows.

     This adds pointer dragging, the two arrows, and the rule that reads
     how far along it she is. `is-live` is added at the end, so the grab
     cursor and the arrows only appear once they do something.

     It does not auto-advance and it does not wrap. "Nothing loops" is the
     guide's rule and a carousel that moves on its own is the plainest case
     of breaking it. The reader moves this one. */
  function initRail() {
    Array.prototype.slice.call(document.querySelectorAll("[data-rail]")).forEach(buildRail);
  }

  function buildRail(gal) {
    var rail = gal.querySelector(".gal-rail");
    if (!rail) return;
    var items = Array.prototype.slice.call(rail.children);
    if (items.length < 2) return;

    var foot = document.createElement("div");
    foot.className = "gal-foot";
    foot.innerHTML =
      '<div class="gal-bar" aria-hidden="true"><i></i></div>' +
      '<div class="gal-nav">' +
        '<button type="button" data-go="-1" aria-label="Scroll the gallery back">' +
          '<svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M5 1L1 5l4 4M1 5h13" stroke="currentColor" stroke-width="1.2"/></svg></button>' +
        '<button type="button" data-go="1" aria-label="Scroll the gallery on">' +
          '<svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M13 5H0" stroke="currentColor" stroke-width="1.2"/></svg></button>' +
      '</div>';
    gal.appendChild(foot);

    var fill = foot.querySelector(".gal-bar i");
    var prev = foot.querySelector('[data-go="-1"]');
    var next = foot.querySelector('[data-go="1"]');

    function read() {
      var max = rail.scrollWidth - rail.clientWidth;
      var frac = rail.clientWidth / rail.scrollWidth;
      gal.style.setProperty("--gal-w", (frac * 100).toFixed(2) + "%");
      /* the thumb travels the track's own length minus its width, which is
         what keeps its right edge landing on the right edge at the end */
      var p = max > 0 ? rail.scrollLeft / max : 0;
      gal.style.setProperty("--gal-x", "calc(" + (p * 100).toFixed(2) + "% * " +
        ((1 - frac) / (frac || 1)).toFixed(4) + ")");
      prev.disabled = rail.scrollLeft <= 1;
      next.disabled = rail.scrollLeft >= max - 1;
    }

    /* one tile plus its gap, measured rather than assumed, so the arrows
       still land on a snap point when the tile width changes at a breakpoint */
    function step() {
      var a = items[0].getBoundingClientRect();
      var b = items[1] ? items[1].getBoundingClientRect() : a;
      return Math.max(1, Math.round(b.left - a.left));
    }

    foot.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest("[data-go]") : null;
      if (!b) return;
      rail.scrollBy({ left: step() * parseInt(b.dataset.go, 10),
                      behavior: reduce.matches ? "auto" : "smooth" });
    });

    rail.addEventListener("scroll", read, { passive: true });
    window.addEventListener("resize", read, { passive: true });

    /* Pointer dragging. Snapping is turned off for the duration, or the rail
       fights the hand; it comes back on release and the nearest tile takes
       it from there. */
    var down = false, x0 = 0, left0 = 0, moved = 0;
    rail.addEventListener("pointerdown", function (e) {
      if (e.pointerType === "touch") return;      /* native scrolling is better */
      down = true; moved = 0;
      x0 = e.clientX; left0 = rail.scrollLeft;
      gal.classList.add("is-dragging");
    });
    rail.addEventListener("pointermove", function (e) {
      if (!down) return;
      var dx = e.clientX - x0;
      moved = Math.max(moved, Math.abs(dx));
      rail.scrollLeft = left0 - dx;
    });
    function release() {
      if (!down) return;
      down = false;
      gal.classList.remove("is-dragging");
      read();
    }
    rail.addEventListener("pointerup", release);
    rail.addEventListener("pointercancel", release);
    rail.addEventListener("pointerleave", release);
    /* a drag that ends on a tile must not also open it */
    rail.addEventListener("click", function (e) {
      if (moved > 6) { e.preventDefault(); e.stopPropagation(); moved = 0; }
    }, true);
    rail.addEventListener("dragstart", function (e) { e.preventDefault(); });

    gal.classList.add("is-live");
    read();
    /* the tiles are lazy images and every one of them changes the width */
    var n = 0;
    (function settle() { read(); if (++n < 12) window.setTimeout(settle, 200); })();
  }

  /* ---------- 17. The pointer companion ---------------------
     Half of the retreat pages is photographs, and a photograph that opens
     looks exactly like one that does not. This names what is under the
     cursor -- View, Play, Drag -- in the same small caps the rest of the
     page labels things in.

     It is scoped to elements that declare `data-cursor` and it never
     replaces the system cursor. Every element that declares one also sets a
     real CSS cursor, so the meaning survives with JS off, on a touch
     screen, and for a reader who has asked for less movement. */
  function initCursor() {
    if (!document.querySelector("[data-cursor]")) return;
    var fine = window.matchMedia("(hover: hover) and (pointer: fine)");
    if (!fine.matches || reduce.matches) return;

    var el = document.createElement("div");
    el.className = "crs";
    el.setAttribute("aria-hidden", "true");
    el.innerHTML = "<i></i>";
    document.body.appendChild(el);
    var label = el.firstChild, host = null, shown = false;

    /* A direct style write, which applies instantly here. The scale lives
       on the child, on a keyframe, so the two never fight. */
    function move(e) {
      el.style.transform = "translate3d(" + e.clientX + "px," + e.clientY + "px,0)";
    }

    function enter(next) {
      if (next === host) return;
      host = next;
      label.textContent = next.dataset.cursor || "";
      if (!shown) { shown = true; el.classList.remove("is-off"); el.classList.add("is-on"); }
    }

    function leave() {
      if (!shown) return;
      shown = false; host = null;
      el.classList.remove("is-on");
      el.classList.add("is-off");
    }

    document.addEventListener("pointermove", function (e) {
      if (e.pointerType && e.pointerType !== "mouse") return;
      var next = e.target && e.target.closest ? e.target.closest("[data-cursor]") : null;
      if (next) { move(e); enter(next); }
      else if (shown) { move(e); leave(); }
    }, { passive: true });

    /* leaving the window entirely fires no move, so it is caught here */
    document.addEventListener("pointerleave", leave);
    window.addEventListener("blur", leave);
    /* a plug-in mouse can arrive after load, and a plug-out can leave the
       disc stranded; either way the resting state is correct */
    if (fine.addEventListener) fine.addEventListener("change", leave);
  }

  function initYear() {
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = String(new Date().getFullYear());
    });
  }

  function boot() {
    initTweenProbe();
    document.querySelectorAll(".split").forEach(splitWords);
    initReveals();
    initHeader();
    initScroll();
    initFifteen();
    initBreath();
    initNav();
    initHero();
    initCondition();
    initReversal();
    initQuotes();
    initFaq();
    initRules();
    initVideo();
    initGallery();
    initRail();
    initCursor();
    initYear();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();

  var onChange = function () {
    if (!reduce.matches) return;
    document.querySelectorAll(".r-up, .r-fade, .r-img, .split")
      .forEach(function (el) { el.classList.add("is-in"); });
  };
  if (reduce.addEventListener) reduce.addEventListener("change", onChange);
  else if (reduce.addListener) reduce.addListener(onChange);
})();
