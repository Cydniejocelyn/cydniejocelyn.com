/* ============================================================
   A Sounding. Site-wide popup.

   Wired on 26 August 2026. The script tag goes before </body>:

     <script src="/sounding-popup.js" defer></script>

   It is on the home page, The Build, Retreats and The Letters. It is
   deliberately NOT on three pages, and each of those is also listed in
   SKIP_PATHS below so the exclusion survives someone pasting the tag onto
   a page later:

     /a-sounding      it exists to push a reader to that page
     /about           a first-person account of postpartum depression, a
                      child's diagnosis and a husband's stroke. Nothing
                      interrupts that to sell a $300 call.
     /retreats/greece a sold-out waitlist funnel with its own action
     /privacy-policy  she is looking up what happens to her data or what
                      she signed. Nothing interrupts that to sell.
     /thequestions    that page already is this push. A modal selling what
                      the page is selling is the page arguing with itself.

   Everything below is self-contained. Edit only the CONFIG block.
   ============================================================ */

(function () {
  /* ---------------- CONFIG ---------------- */
  var LINK          = 'https://clients.cydniejocelyn.com/schedule/69f9f2a095c611cc2401eec7';
  var DELAY_MS      = 45000;   /* how long before it fires */
  var SKIP_PATHS    = ['/a-sounding', '/about', '/retreats/greece', '/privacy-policy', '/thequestions', '/contact'];
  var REMEMBER_DAYS = 30;      /* how long a dismissal is honoured */
  var MEMORY_KEY    = 'sd_pop_dismissed';

  var EYEBROW = 'Free &middot; 30 minutes';
  var TITLE   = 'Let&rsquo;s <em>talk.</em>';
  var BODY    = 'A free 30-minute call about your business and where you want it to go. You will leave knowing whether a partnership makes sense.';
  var CTA     = 'Book a free 30-min call';
  var DISMISS = 'Not now';
  /* 26 Sep 2026: the free call replaced the $300 Sounding here, on her word;
     the free call is the front door now. */
  /* ---------------------------------------- */

  var path = window.location.pathname.replace(/\/$/, '') || '/';
  for (var i = 0; i < SKIP_PATHS.length; i++) {
    if (path === SKIP_PATHS[i]) return;
  }

  function seen() {
    try {
      var v = window.localStorage.getItem(MEMORY_KEY);
      return v ? (Date.now() - parseInt(v, 10)) < REMEMBER_DAYS * 864e5 : false;
    } catch (e) { return false; }
  }
  function remember() {
    try { window.localStorage.setItem(MEMORY_KEY, String(Date.now())); } catch (e) {}
  }
  if (seen()) return;

  /* ONE POPUP A VISIT, 16 September 2026. gatlinburg-popup.js marks the
     session when it opens; this one stands down for the rest of that visit,
     and marks the session itself when it is the one that opens. */
  var SESSION_KEY = 'cj_pop_shown';
  function sessionTaken() {
    try { return !!window.sessionStorage.getItem(SESSION_KEY); } catch (e) { return false; }
  }
  if (sessionTaken()) return;

  /* The token names this file shipped with came from the wireframe's
     placeholder palette, where --held-lift was a near-white paper colour.
     On this site --held-lift is #CE908A, the hover state for the warm note,
     so the card rendered salmon pink and the border rendered mint. The
     custom properties below are the real ones from site.css section 1:
     --surface is the light ground, --fathom the ink, --meniscus the rules,
     --carved/--level/--utility the three faces. Literal hex stays as the
     fallback so the modal survives the stylesheet failing to load. */
  /* RESTYLED 26 September 2026 for the rebuilt site: white card, ink type,
     one aqua hairline, the Instrument faces, the site's rectangular ink
     button. Literal values, so it survives the stylesheet failing to load. */
  var CSS = [
    '.sd-pop{position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;padding:20px}',
    '.sd-pop[hidden]{display:none}',
    '.sd-scrim{position:absolute;inset:0;background:rgba(12,40,48,.45);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px)}',
    '.sd-card{position:relative;background:#fff;border-top:2px solid #9fccc6;max-width:440px;width:100%;max-height:calc(100dvh - 40px);overflow-y:auto;padding:48px 40px 34px;color:#0c2830;box-shadow:0 40px 80px -40px rgba(12,40,48,.5)}',
    '.sd-x{position:absolute;top:8px;right:8px;background:none;border:0;cursor:pointer;font-size:24px;line-height:1;color:#6f878b;width:44px;height:44px;display:flex;align-items:center;justify-content:center}',
    '.sd-eyebrow{font-family:"Instrument Sans",-apple-system,Helvetica,sans-serif;font-size:11px;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:#415e64;margin:0 0 18px}',
    '.sd-title{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:46px;line-height:1;letter-spacing:-.01em;margin:0 0 16px}',
    '.sd-title em{font-style:italic;color:#2f5a61}',
    '.sd-body{font-family:"Instrument Sans",-apple-system,Helvetica,sans-serif;font-size:16px;line-height:1.6;color:#415e64;margin:0 0 28px}',
    '.sd-btn{display:inline-flex;align-items:center;justify-content:center;min-height:52px;font-family:"Instrument Sans",-apple-system,Helvetica,sans-serif;font-size:12px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;padding:14px 28px;background:#0c2830;color:#fff;text-decoration:none;border:0;transition:background .3s}',
    '.sd-btn:hover{background:#2f5a61}',
    '.sd-vh{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}',
    '.sd-dismiss{display:inline-flex;align-items:center;min-height:44px;margin-top:10px;background:none;border:0;padding:0;cursor:pointer;font-family:"Instrument Sans",-apple-system,Helvetica,sans-serif;font-size:13px;color:#6f878b;text-decoration:underline;text-decoration-color:#9fccc6;text-underline-offset:4px}',
    '.sd-btn:focus-visible,.sd-x:focus-visible,.sd-dismiss:focus-visible{outline:2px solid #2f5a61;outline-offset:3px}',
    '@media(max-width:560px){.sd-pop{padding:14px;align-items:flex-end}.sd-card{padding:40px 24px 24px}.sd-title{font-size:38px}.sd-body{font-size:15px;margin-bottom:22px}.sd-btn{width:100%}}'
].join('');

  function build() {
    var style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    var pop = document.createElement('div');
    pop.className = 'sd-pop';
    pop.id = 'sdPop';
    pop.hidden = true;
    pop.innerHTML =
      '<div class="sd-scrim" data-sd-close></div>' +
      '<div class="sd-card" role="dialog" aria-modal="true" aria-labelledby="sdTitle" aria-describedby="sdBody">' +
        '<button class="sd-x" type="button" data-sd-close aria-label="Close">&times;</button>' +
        '<p class="sd-eyebrow">' + EYEBROW + '</p>' +
        '<h2 class="sd-title" id="sdTitle">' + TITLE + '</h2>' +
        '<p class="sd-body" id="sdBody">' + BODY + '</p>' +
        /* The same announcement every booking link on the site carries. This
           one is injected rather than served, so the pass that annotated the
           nine pages could not see it and the suite caught it: "Book a
           Sounding" was the one off-site link on four pages with nothing
           saying where it goes. A screen reader user in a modal has even
           less context than one on a page. */
        '<div><a class="sd-btn" href="' + LINK + '">' + CTA +
          '<span class="sd-vh"> (opens my scheduling page)</span></a></div>' +
        '<button class="sd-dismiss" type="button" data-sd-close>' + DISMISS + '</button>' +
      '</div>';
    document.body.appendChild(pop);

    var lastFocus = null;
    var timer = null;

    function focusable() {
      return pop.querySelectorAll('a[href], button:not([disabled])');
    }

    function open() {
      if (sessionTaken() || document.querySelector('.gb-pop:not([hidden])')) return;
      try { window.sessionStorage.setItem(SESSION_KEY, 'sounding'); } catch (e) {}
      lastFocus = document.activeElement;
      pop.hidden = false;
      document.body.style.overflow = 'hidden';
      pop.querySelector('.sd-btn').focus();
    }
    function close() {
      pop.hidden = true;
      document.body.style.overflow = '';
      remember();
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    pop.addEventListener('click', function (e) {
      if (e.target.hasAttribute('data-sd-close')) close();
    });

    /* aria-modal is a promise to assistive tech that focus is contained.
       Without a trap, Tab walks straight out of the dialog and into a page
       the screen reader has been told is inert, which is worse than not
       claiming it. */
    document.addEventListener('keydown', function (e) {
      if (pop.hidden) return;
      if (e.key === 'Escape') { close(); return; }
      if (e.key !== 'Tab') return;
      var f = focusable();
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    pop.querySelector('.sd-btn').addEventListener('click', remember);

    /* A background tab still counts down, so a reader who opened three
       pages and came back to one finds it already fired. The timer only
       runs while the page is actually being looked at. */
    function start() { if (!timer) timer = window.setTimeout(open, DELAY_MS); }
    function stop()  { if (timer) { window.clearTimeout(timer); timer = null; } }
    if (document.visibilityState === 'visible') start();
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'visible') start(); else stop();
    });

    window.sdPopPreview = open; /* testing: run sdPopPreview() in the console */
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
