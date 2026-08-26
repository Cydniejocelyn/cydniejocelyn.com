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

    targets.forEach(function (t) {
      watch(t, function () { t.classList.add("is-in"); }, null, true);
    });

    window.setTimeout(function () {
      targets.forEach(function (t) { t.classList.add("is-in"); });
    }, 2600);
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
      if (up !== surfaced) { surfaced = up; hdr.classList.toggle("is-surfaced", up); }
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
  function initBreath() {
    var band = document.querySelector(".rise-band");
    if (!band) return;
    var bubs = Array.prototype.slice.call(band.querySelectorAll(".bub"));
    if (!bubs.length) return;

    /* Where each one ends up, and how far behind the one in front it goes.
       The end state is also the resting state in the CSS, so if none of this
       ever runs the three still stand as a column going at the line. */
    var SET = [
      { travel: -34, grow: 0.16, delay:   0 },
      { travel: -52, grow: 0.28, delay: 220 },
      { travel: -74, grow: 0.40, delay: 440 }
    ];
    var RISE = 1500;                      /* one breath, not a hurry */

    function place(b, cfg, t) {
      b.style.transform = "translateY(" + (t * cfg.travel).toFixed(2) + "px)"
                        + " scale(" + (1 + t * cfg.grow).toFixed(3) + ")";
    }
    function settle() {
      bubs.forEach(function (b, i) { place(b, SET[i] || SET[2], 1); });
    }

    /* Reduced motion, or no frames: they are simply already up. */
    if (reduce.matches) { settle(); return; }

    /* Slow out. Fast off the floor, easing as the pressure comes off it,
       which is how a bubble actually behaves and also how a held breath
       leaves you. */
    function ease(x) { return 1 - Math.pow(1 - x, 3); }

    var started = false;

    function play() {
      if (started) return;
      started = true;

      /* They are only ever moved down from inside a frame. If frames never
         come, nothing touches them and the CSS resting state stands, which
         is the three already at the surface. Dropping them to the floor
         first and then waiting to find out would strand them there. */
      var t0 = null, done = false;
      function step(now) {
        if (done) return;
        if (t0 === null) t0 = now;
        var el = now - t0, live = false;
        bubs.forEach(function (b, i) {
          var cfg = SET[i] || SET[2];
          var t = (el - cfg.delay) / RISE;
          if (t < 1) live = true;
          place(b, cfg, ease(Math.max(0, Math.min(1, t))));
        });
        if (live) window.requestAnimationFrame(step);
        else done = true;
      }
      window.requestAnimationFrame(step);

      /* Frames are not guaranteed here. If the rise has not finished by the
         time it should have, put them where they were always going to end
         up. Never leave them on the floor. */
      window.setTimeout(function () {
        if (done) return;
        done = true;
        settle();
      }, RISE + SET[2].delay + 400);
    }

    /* It plays once, when she reaches the band. Nothing loops. */
    watch(band, play, null, true);
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

    function goTo(i, animate) {
      i = Math.max(0, Math.min(N - 1, i));
      cur = i;
      figs.forEach(function (f, n) { f.classList.toggle("is-on", n === i); });
      dotEls.forEach(function (d, n) {
        if (n === i) d.setAttribute("aria-current", "true");
        else d.removeAttribute("aria-current");
      });
      prev.disabled = i === 0;
      next.disabled = i === N - 1;
      count.textContent = pad(i + 1) + " / " + pad(N);
      place(xFor(i), animate !== false);
    }

    /* --- drag. Follows the pointer one to one, then snaps to whichever
       slide the release landed nearest. --- */
    var down = false, startX = 0, baseX = 0, dx = 0;

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

    goTo(0, false);
    window.addEventListener("resize", function () { goTo(cur, false); }, { passive: true });

    /* the faces land after this runs and every width moves when they do */
    var n = 0;
    (function settle() { if (!down) goTo(cur, false); if (++n < 12) window.setTimeout(settle, 200); })();
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
