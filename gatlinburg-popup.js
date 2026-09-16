/* ============================================================
   Wide Open: The Gatlinburg Edition. Launch popup.

   Built 16 September 2026, launch day, on Cydnie's ask: "I also want to do
   a popup that invites people to go register since it's finally here."
   The brand guide forbids modals; she has said the guide is not always
   right (14 September), and this is her call. It follows everything
   sounding-popup.js already learned: a real dialog, a focus trap, Escape,
   a remembered dismissal, a timer that only runs while the tab is visible.

     <script src="/gatlinburg-popup.js" defer></script>

   WHERE IT RUNS. Home, /retreats/, /retreats/greece/ (full, waitlist only,
   so Gatlinburg is the retreat a reader there can actually book) and
   /the-letters/. Not on The Build, A Sounding or Contact, which speak to
   founders of any gender about consulting; not on /about/, /privacy-policy/
   or /thequestions/, for the reasons in sounding-popup.js; and never on the
   Gatlinburg page itself. SKIP_PATHS repeats that so pasting the tag onto
   another page does not quietly widen it.

   ONE POPUP A VISIT. Whichever of the two fires first marks the session,
   and sounding-popup.js stands down when this one has shown. This one
   fires sooner, so on a page carrying both, a reader meets Gatlinburg.

   It stops by itself on 13 April 2027, the first day of the retreat.

   NOT INSIDE THE TEST HARNESS. `_test.html` and `_shot.html` load pages in
   a same-origin iframe; a dialog opening mid-suite steals focus from the
   lightbox and scroll assertions. A cross-origin frame (the review
   artifact) still shows it.
   ============================================================ */

(function () {
  /* ---------------- CONFIG ---------------- */
  var LINK          = '/retreats/gatlinburg/';
  var IMAGE         = '/assets/img/gatlinburg/house-dusk-600.webp';
  var DELAY_MS      = 12000;   /* visible time on the page before it opens */
  var SCROLL_SHARE  = 0.35;    /* or this much of the page read, after 4s */
  var ENDS          = Date.parse('2027-04-13T00:00:00-05:00');
  var ONLY_PATHS    = ['/', '/retreats', '/retreats/greece', '/the-letters'];
  var SKIP_PATHS    = ['/retreats/gatlinburg', '/about', '/a-sounding', '/the-build',
                       '/contact', '/privacy-policy', '/thequestions'];
  var REMEMBER_DAYS = 14;
  var MEMORY_KEY    = 'gb_pop_dismissed';
  var SESSION_KEY   = 'cj_pop_shown';     /* shared with sounding-popup.js */

  var EYEBROW = 'Booking open &middot; 13&ndash;18 April 2027';
  var TITLE   = 'Wide Open is <em>finally here.</em>';
  var BODY    = 'Five days in a private house in the Smoky Mountains, with Cydnie and Kayla. Every meal and both workshops are included, and $500 holds your room.';
  var NOTE    = 'Early rate through 31 October, from $1,490.';
  var CTA     = 'See Gatlinburg and register';
  var DISMISS = 'Maybe later';
  /* ---------------------------------------- */

  if (Date.now() >= ENDS) return;

  var path = window.location.pathname.replace(/\/$/, '') || '/';
  var i;
  for (i = 0; i < SKIP_PATHS.length; i++) {
    if (path === SKIP_PATHS[i] || path.indexOf(SKIP_PATHS[i] + '/') === 0) return;
  }
  if (ONLY_PATHS.indexOf(path) === -1) return;

  try {
    if (window.parent !== window &&
        /^\/_/.test(window.parent.location.pathname)) return;
  } catch (e) { /* cross-origin parent: a real embed, carry on */ }

  function get(store, key) { try { return window[store].getItem(key); } catch (e) { return null; } }
  function set(store, key, v) { try { window[store].setItem(key, v); } catch (e) {} }

  function seen() {
    var v = get('localStorage', MEMORY_KEY);
    return v ? (Date.now() - parseInt(v, 10)) < REMEMBER_DAYS * 864e5 : false;
  }
  if (seen() || get('sessionStorage', SESSION_KEY)) return;

  var CSS = [
    '.gb-pop{position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;padding:20px}',
    '.gb-pop[hidden]{display:none}',
    '.gb-pop-scrim{position:absolute;inset:0;background:rgba(7,26,31,.74);opacity:0;transition:opacity .45s ease}',
    '.gb-pop-card{position:relative;display:grid;grid-template-columns:minmax(0,1fr);background:var(--fathom,#071A1F);color:var(--surface,#E7ECE8);border:1px solid rgba(159,204,198,.35);max-width:760px;width:100%;max-height:calc(100dvh - 40px);overflow-y:auto;opacity:0;transform:translateY(18px) scale(.985);transition:opacity .5s cubic-bezier(.2,.7,.2,1),transform .6s cubic-bezier(.2,.7,.2,1)}',
    '.gb-pop.is-open .gb-pop-scrim{opacity:1}',
    '.gb-pop.is-open .gb-pop-card{opacity:1;transform:none}',
    '.gb-pop-fig{margin:0;position:relative;overflow:hidden;min-height:180px}',
    '.gb-pop-fig img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:40% 45%;display:block;transform:scale(1.08);transition:transform 6s cubic-bezier(.2,.6,.2,1)}',
    '.gb-pop.is-open .gb-pop-fig img{transform:scale(1)}',
    '.gb-pop-copy{padding:40px 36px 30px}',
    '.gb-pop-x{position:absolute;top:6px;right:6px;z-index:2;background:rgba(7,26,31,.55);border:0;border-radius:50%;cursor:pointer;font-size:22px;line-height:1;color:#E7ECE8;width:44px;height:44px;display:flex;align-items:center;justify-content:center}',
    '.gb-pop-eyebrow{font-family:var(--utility,"IBM Plex Mono",ui-monospace,monospace);font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--breath,#9FCCC6);margin:0 0 16px}',
    '.gb-pop-title{font-family:var(--carved,"Instrument Serif",Georgia,serif);font-weight:400;font-size:40px;line-height:1.04;letter-spacing:.01em;margin:0 0 14px;color:#E7ECE8}',
    '.gb-pop-title em{font-style:italic;color:var(--breath,#9FCCC6);display:block}',
    '.gb-pop-body{font-family:var(--level,"Instrument Sans",-apple-system,Helvetica,sans-serif);font-size:16px;line-height:1.55;color:#C9DCD9;margin:0 0 10px}',
    '.gb-pop-note{font-family:var(--utility,"IBM Plex Mono",ui-monospace,monospace);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#E3A59F;margin:0 0 24px}',
    '.gb-pop-btn{display:inline-flex;align-items:center;gap:10px;min-height:44px;font-family:var(--level,"Instrument Sans",-apple-system,Helvetica,sans-serif);font-size:12px;letter-spacing:.11em;text-transform:uppercase;padding:14px 24px;background:var(--breath,#9FCCC6);color:var(--fathom,#071A1F);text-decoration:none;border:1px solid var(--breath,#9FCCC6);transition:background .25s,color .25s}',
    '.gb-pop-btn:hover{background:#E7ECE8;border-color:#E7ECE8}',
    '.gb-pop-dismiss{display:flex;align-items:center;min-height:44px;margin-top:8px;background:none;border:0;padding:0;cursor:pointer;font-family:var(--utility,"IBM Plex Mono",ui-monospace,monospace);font-size:12px;color:#A8C4C0;text-decoration:underline;text-underline-offset:4px}',
    '.gb-pop-btn:focus-visible,.gb-pop-x:focus-visible,.gb-pop-dismiss:focus-visible{outline:2px solid var(--breath,#9FCCC6);outline-offset:3px}',
    '@media(min-width:680px){.gb-pop-card{grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr)}.gb-pop-fig{min-height:100%}}',
    '@media(max-width:679px){.gb-pop{padding:14px;align-items:flex-end}.gb-pop-fig{min-height:150px}.gb-pop-copy{padding:26px 22px 20px}.gb-pop-title{font-size:31px}.gb-pop-body{font-size:15px}.gb-pop-btn{width:100%;justify-content:center}}',
    '@media(prefers-reduced-motion:reduce){.gb-pop-scrim,.gb-pop-card,.gb-pop-fig img{transition:none;transform:none}}'
  ].join('');

  var ARROW = '<svg width="14" height="10" viewBox="0 0 14 10" fill="none" aria-hidden="true"><path d="M9 1l4 4-4 4M13 5H0" stroke="currentColor" stroke-width="1.2"/></svg>';

  function build() {
    var style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);

    var pop = document.createElement('div');
    pop.className = 'gb-pop';
    pop.hidden = true;
    pop.innerHTML =
      '<div class="gb-pop-scrim" data-gb-close></div>' +
      '<div class="gb-pop-card" role="dialog" aria-modal="true" aria-labelledby="gbPopTitle" aria-describedby="gbPopBody">' +
        '<button class="gb-pop-x" type="button" data-gb-close aria-label="Close">&times;</button>' +
        '<figure class="gb-pop-fig"><img src="' + IMAGE + '" width="600" height="409" alt="" decoding="async"></figure>' +
        '<div class="gb-pop-copy">' +
          '<p class="gb-pop-eyebrow">' + EYEBROW + '</p>' +
          '<h2 class="gb-pop-title" id="gbPopTitle">' + TITLE + '</h2>' +
          '<p class="gb-pop-body" id="gbPopBody">' + BODY + '</p>' +
          '<p class="gb-pop-note">' + NOTE + '</p>' +
          '<div><a class="gb-pop-btn" href="' + LINK + '">' + CTA + ARROW + '</a></div>' +
          '<button class="gb-pop-dismiss" type="button" data-gb-close>' + DISMISS + '</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(pop);

    var lastFocus = null, timer = null, fired = false;

    function open() {
      if (fired || get('sessionStorage', SESSION_KEY)) return;
      if (document.querySelector('.sd-pop:not([hidden])')) return;
      fired = true;
      set('sessionStorage', SESSION_KEY, 'gatlinburg');
      lastFocus = document.activeElement;
      pop.hidden = false;
      void pop.offsetWidth;
      pop.classList.add('is-open');
      document.body.style.overflow = 'hidden';
      pop.querySelector('.gb-pop-btn').focus({ preventScroll: true });
      window.removeEventListener('scroll', onScroll);
    }
    function close() {
      pop.classList.remove('is-open');
      pop.hidden = true;
      document.body.style.overflow = '';
      set('localStorage', MEMORY_KEY, String(Date.now()));
      if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    }

    pop.addEventListener('click', function (e) {
      if (e.target.hasAttribute('data-gb-close')) close();
    });
    pop.querySelector('.gb-pop-btn').addEventListener('click', function () {
      set('localStorage', MEMORY_KEY, String(Date.now()));
    });

    document.addEventListener('keydown', function (e) {
      if (pop.hidden) return;
      if (e.key === 'Escape') { close(); return; }
      if (e.key !== 'Tab') return;
      var f = pop.querySelectorAll('a[href], button:not([disabled])');
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    /* Opens after 12 seconds of looking, or once a third of the page has
       been read if that comes first (and not in the first four seconds). */
    var born = Date.now();
    function onScroll() {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      if (h > 0 && window.scrollY / h >= SCROLL_SHARE && Date.now() - born > 4000) open();
    }
    window.addEventListener('scroll', onScroll, { passive: true });

    function start() { if (!timer && !fired) timer = window.setTimeout(open, DELAY_MS); }
    function stop()  { if (timer) { window.clearTimeout(timer); timer = null; } }
    if (document.visibilityState === 'visible') start();
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'visible') start(); else stop();
    });

    window.gbPopPreview = function () { fired = false; try { sessionStorage.removeItem(SESSION_KEY); } catch (e) {} open(); };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
