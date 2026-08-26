/* ============================================================
   A Sounding. Site-wide popup.
   Upload to the site root, then add one line before </body>
   on every page:

     <script src="/sounding-popup.js" defer></script>

   Everything below is self-contained. Edit only the CONFIG block.
   ============================================================ */

(function () {
  /* ---------------- CONFIG ---------------- */
  var LINK          = 'https://clients.cydniejocelyn.com/schedule/6a185c26693e14802690e9f6';
  var DELAY_MS      = 45000;   /* how long before it fires */
  var SKIP_PATHS    = [];      /* e.g. ['/a-sounding'] to exclude a page */
  var REMEMBER_DAYS = 30;      /* how long a dismissal is honoured */
  var MEMORY_KEY    = 'sd_pop_dismissed';

  var EYEBROW = 'Ninety minutes \u00A0/\u00A0 $300';
  var TITLE   = 'A Sounding';
  var BODY    = 'One conversation about what is actually happening in your business, and a written page two days later. Nothing to prepare beforehand.';
  var CTA     = 'Book a Sounding';
  var DISMISS = 'Not now';
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

  var CSS = [
    '.sd-pop{position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;padding:20px}',
    '.sd-pop[hidden]{display:none}',
    '.sd-scrim{position:absolute;inset:0;background:rgba(10,26,34,.62)}',
    '.sd-card{position:relative;background:var(--held-lift,#FBFAF7);border:1px solid var(--breath,#C9D6D8);border-radius:0;max-width:430px;width:100%;padding:44px 38px 34px;color:var(--fathom,#0A1A22)}',
    '.sd-x{position:absolute;top:10px;right:12px;background:none;border:0;cursor:pointer;font-size:22px;line-height:1;color:var(--silt,#8C8578);padding:6px}',
    '.sd-eyebrow{font-family:var(--mono,"IBM Plex Mono",monospace);font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--silt,#8C8578);margin:0 0 16px}',
    '.sd-title{font-family:var(--display,"IvyPresto Display",Georgia,serif);font-weight:400;font-size:38px;line-height:1;margin:0 0 14px}',
    '.sd-body{font-family:var(--body,"Instrument Sans",Arial,sans-serif);font-size:16px;line-height:1.55;color:var(--deepwater,#123240);margin:0 0 26px}',
    '.sd-btn{display:inline-block;font-family:var(--body,"Instrument Sans",Arial,sans-serif);font-size:12px;letter-spacing:.11em;text-transform:uppercase;padding:15px 26px;background:var(--fathom,#0A1A22);color:var(--held-lift,#FBFAF7);text-decoration:none;border:1px solid var(--fathom,#0A1A22)}',
    '.sd-dismiss{display:block;margin-top:20px;background:none;border:0;padding:0;cursor:pointer;font-family:var(--mono,"IBM Plex Mono",monospace);font-size:12px;color:var(--silt,#8C8578);text-decoration:underline;text-underline-offset:4px}',
    '.sd-btn:focus-visible,.sd-x:focus-visible,.sd-dismiss:focus-visible{outline:2px solid var(--meniscus,#7E9AA3);outline-offset:3px}',
    '@media(max-width:480px){.sd-card{padding:38px 26px 28px}.sd-title{font-size:32px}}'
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
        '<a class="sd-btn" href="' + LINK + '">' + CTA + '</a>' +
        '<button class="sd-dismiss" type="button" data-sd-close>' + DISMISS + '</button>' +
      '</div>';
    document.body.appendChild(pop);

    var lastFocus = null;

    function open() {
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
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !pop.hidden) close();
    });
    pop.querySelector('.sd-btn').addEventListener('click', remember);

    window.setTimeout(open, DELAY_MS);
    window.sdPopPreview = open; /* testing: run sdPopPreview() in the console */
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
