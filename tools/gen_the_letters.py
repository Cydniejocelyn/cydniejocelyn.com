"""The Letters (/the-letters/), rebuilt 26 September 2026 on the luxury system.

Her answers (26 September): keep the form that works (the HoneyBook
sign-up, cf_id/6a19d46a...), her latest real letter as the sample (it replaced No. 07 the same day; "it's a letter for all", so the page does not narrow to founders), weekly
is the goal, the Flodesk popup stays (form 6a8f553c..., re-added below the
shared scripts exactly as it was), and the photograph is my pick: her
writing in a journal, the page's subject, in the arch.

Changed from the old page: her face first; the letter set as a real page;
the close goes to the free call, not the Sounding; "first access" no longer
says the Greece group fills from this list (it is full). Cut: "You can
leave whenever you want" and "No onboarding sequence, and no pitch on
arrival" (exits, HANDOFF copy rule), "the car line" (the site speaks to
founders and leaders), "You are under something" (the old heavy register).
Lines that are mine, not hers, are marked BRIDGE.

    cd tools && python3 gen_the_letters.py
"""
import os
import lux_page as L

URL = L.SITE + "/the-letters/"
CALL, ARW = L.CALL, L.ARW
SIGNUP = "https://www.honeybook.com/widget/cydnie_jocelyn_collective_299013/cf_id/6a19d46a5cb4c5d7f86446a9"
I = "../assets/img/"

FLODESK = """<!-- FLODESK POPUP (form 6a8f553c...). The only Flodesk form on the site,
     kept on her word of 26 September. Its trigger and styling live in
     Flodesk, not here. To re-test it: clear localStorage and the cookie
     fd-form-<id>-dismissed-count, then reload. -->
<script>
(function (w, d) {
  if (!d.querySelector('script[src*="flodesk"]')) {
    (function (w, d, t, h, s, n) {
      w.FlodeskObject = n;
      var fn = function () { (w[n].q = w[n].q || []).push(arguments); };
      w[n] = w[n] || fn;
      var f = d.getElementsByTagName(t)[0];
      var v = '?v=' + Math.floor(new Date().getTime() / (120 * 1000)) * 60;
      var sm = d.createElement(t);
      sm.async = true; sm.type = 'module'; sm.src = h + s + '.mjs' + v;
      f.parentNode.insertBefore(sm, f);
      var sn = d.createElement(t);
      sn.async = true; sn.noModule = true; sn.src = h + s + '.js' + v;
      f.parentNode.insertBefore(sn, f);
    })(w, d, 'script', 'https://assets.flodesk.com', '/universal', 'fd');
  }
  w.fd('form', { formId: '6a8f553c9f30a024ac4f2a82' });
})(window, document);
</script>
"""

MAIN = """<main id="main">

<!-- HERO. What the letters are, in plain words, and one way in. -->
<section class="ww-hero" aria-labelledby="lt-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <span class="hv-label">The Letters &middot; Free, every week</span>
      <h1 id="lt-h">A weekly letter on building something <em>you believe in.</em></h1>
      <p class="hv-lede">One letter a week from me, honest about what I am learning in leadership, business, growth and people, written the week it goes out.</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="#join" data-cta="letters-hero">Get the letters %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="#letter">Read a recent one</a>
      </div>
      <ul class="ww-trust" role="list"><li>Free</li><li>Written by me</li><li>First word on retreats</li></ul>
    </div>
    <figure class="ww-arch">
      <img src="%(I)scydnie-writing-1000.webp" srcset="%(I)scydnie-writing-600.webp 600w, %(I)scydnie-writing-1000.webp 1000w" sizes="(min-width: 64rem) 30rem, 90vw" width="1000" height="1500" alt="Cydnie Jocelyn sitting on the floor with an open journal on her lap, pen in hand, smiling" fetchpriority="high">
    </figure>
  </div>
</section>

<!-- WHO IT IS FOR. Her word of 26 September: "it's a letter for all".
     The founders-and-leaders framing is the rest of the site's; the
     letters are for everyone. BRIDGE: both lines are mine. -->
<section class="hv-sec lt-for" aria-labelledby="lt-for">
  <div class="hv-wrap au-row">
    <div>
      <span class="hv-label">Who it is for</span>
      <h2 class="hv-h2" id="lt-for">A letter <em>for all.</em></h2>
    </div>
    <div class="lt-for-copy">
      <p class="hv-lede">Whether you run a business, lead a team, or are somewhere in between, these are written for you.</p>
      <p>Real weeks, not polished ones: what I am building, what I am learning, and the why underneath it.</p>
    </div>
  </div>
</section>

<!-- A RECENT LETTER. Her latest real letter in full, word for word from
     her two screenshots of 26 September, sign-off included. No subject
     line was visible, so none is invented. -->
<section class="hv-sec lt-read" id="letter" aria-labelledby="lt-read">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">A recent letter</span>
      <h2 class="hv-h2" id="lt-read">What lands <em>in your inbox.</em></h2>
    </div>
    <article class="lt-letter">
      <svg class="hv-wm lt-letter-mark" viewBox="0 0 504.2 54.4" aria-label="Cydnie Jocelyn" role="img"><use href="#cj-wordmark"/></svg>
      <p class="lt-letter-no">The latest letter <span>Word for word</span></p>
      <p>I&rsquo;m keeping this week&rsquo;s letter short because, if I&rsquo;m being real, I&rsquo;m tired.</p>
      <p>I just got home from a conference with pages and pages of notes about leadership, business, growth, people, and what it takes to keep building something you believe in. I left inspired, but I also came home still trying to wrap my head around a season that feels very much in-between. I know I&rsquo;m moving forward, but I&rsquo;m not entirely sure what I&rsquo;m moving toward yet.</p>
      <p>Of everything I wrote down this weekend, though, the thing I keep coming back to is <b>why</b>. Why am I doing any of this? Why do I keep building, creating, gathering women, trying new things, and saying yes even when I don&rsquo;t know exactly where they&rsquo;re going to lead?</p>
      <p>I don&rsquo;t think I have one perfectly packaged answer yet. But I do know it has something to do with people. Making people feel seen. Creating spaces where women can be honest about where they are. Believing in someone before they fully believe in themselves. Maybe that&rsquo;s why so much of what I&rsquo;m building looks different on the surface but somehow keeps coming back to the same place.</p>
      <p>So that&rsquo;s the question I&rsquo;m taking with me into this week, and maybe it&rsquo;s one worth asking yourself too:</p>
      <p class="lt-letter-q">When everything else gets stripped away, why are you doing what you&rsquo;re doing?</p>
      <p>Not what sounds good. Not what you think the answer should be. What is underneath all of it?</p>
      <p>I&rsquo;m still figuring out my answer too.</p>
      <p class="lt-letter-sign">Cydnie Jocelyn</p>
      <p class="lt-letter-more"><a class="hv-inline" href="#join" data-cta="letters-next">Get the next one in your inbox</a></p>
    </article>
  </div>
</section>

<!-- WHAT YOU GET. Two things, beside one photograph (photo left; the
     hero's is right). -->
<section class="hv-sec" aria-labelledby="lt-get">
  <div class="hv-wrap au-row">
    <figure class="lt-photo"><img src="%(I)scydnie-journal-1000.webp" srcset="%(I)scydnie-journal-600.webp 600w, %(I)scydnie-journal-1000.webp 1000w" sizes="(min-width: 60rem) 30rem, 92vw" width="1000" height="667" alt="Close-up of Cydnie writing in a linen-bound journal with a lavender pen" loading="lazy"></figure>
    <div>
      <span class="hv-label">What you get</span>
      <h2 class="hv-h2" id="lt-get">Two things, <em>every week.</em></h2>
      <ol class="lt-get" role="list">
        <li><h3>The letter</h3><p>Written by me, the week it goes out. Honest about what I am building and learning, in business and in life.</p></li>
        <li><h3>First access</h3><p>When a retreat or new work opens, it opens here first. Retreats cap at fifteen, so first matters.</p></li>
      </ol>
    </div>
  </div>
</section>

<section class="hv-close" id="join" aria-labelledby="close-h">
  <div class="hv-wrap">
    <span class="hv-label hv-label--c">Free, every week</span>
    <h2 class="hv-h2" id="close-h">Get <em>the letters.</em></h2>
    <p class="hv-lede">One letter a week from me, and the first word on every retreat and new way to work together.</p>
    <!-- THE SIGN-UP FORM (26 September 2026, her word "pushed to neon"):
         saved to her Neon database and sent to Flodesk by /api/subscribe.
         The HoneyBook form stays as the no-JavaScript fallback. -->
    <form class="cj-form cj-form--big" data-api="subscribe" aria-label="Get the Letters">
      <div class="cj-row">
        <label class="cj-vh" for="lt-name">First name</label>
        <input id="lt-name" name="name" type="text" autocomplete="given-name" placeholder="First name">
        <label class="cj-vh" for="lt-email">Email address</label>
        <input id="lt-email" name="email" type="email" required autocomplete="email" placeholder="Your email">
        <input class="cj-hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
        <button class="hv-btn hv-btn--ink" type="submit" data-cta="letters-close">Get the letters %(ARW)s</button>
      </div>
      <p class="cj-status" role="status" aria-live="polite"></p>
      <noscript><p><a class="hv-inline" href="%(SIGNUP)s" rel="noopener">Sign up here instead</a></p></noscript>
    </form>
    <p class="au-also">Rather talk now? <a class="hv-inline" href="%(CALL)s" data-cta="free-call-letters">Book a free 30-min call</a>.</p>
  </div>
</section>

</main>
""" % {"SIGNUP": SIGNUP, "CALL": CALL, "ARW": ARW, "I": I}

# Person and organisation as About now states them; the page's own nodes kept.
about = {n["@id"]: n for n in L.old_graph("about/index.html") if "@id" in n}
graph = []
for n in L.old_graph("the-letters/index.html"):
    if n.get("@id") in about and n.get("@type") != "WebPage":
        n = about[n["@id"]]
    if n.get("@type") == "Newsletter":
        n["description"] = ("A free weekly letter from Cydnie Jocelyn on leadership, business, growth and people, and building "
                            "something you believe in. Written for everyone. Retreats and new work open to this list first.")
    graph.append(n)

PRELOAD = ('<link rel="preload" as="image" href="%scydnie-writing-1000.webp" '
           'imagesrcset="%scydnie-writing-600.webp 600w, %scydnie-writing-1000.webp 1000w" '
           'imagesizes="(min-width: 64rem) 30rem, 90vw" type="image/webp" fetchpriority="high">\n' % (I, I, I))

OUT = "the-letters/index.html"
L.render(
    out=OUT, depth=1, active="/the-letters/",
    title="The Letters | A Free Weekly Letter from Cydnie Jocelyn",
    description="A free weekly letter from Cydnie Jocelyn on leadership, business, growth and building something you believe in. Retreats and new work open here first.",
    canonical=URL,
    og_title="The Letters | A Free Weekly Letter from Cydnie Jocelyn",
    og_description="One honest letter a week on building something you believe in. Free, for everyone, and the first word on every retreat.",
    graph=graph, main=MAIN, preload=PRELOAD, body_class="ww-page",
    reveal=(".ww-head", ".au-row > div", ".lt-get > li", ".lt-letter"),
    reveal_imgs=(".lt-photo",),
)
p = os.path.join(L.ROOT, OUT)
s = open(p, encoding="utf-8").read()
assert s.count("</body>") == 1
s = s.replace("</body>", FLODESK + "</body>", 1)
open(p, "w", encoding="utf-8").write(s)
print("written", len(s))
