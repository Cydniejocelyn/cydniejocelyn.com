import re, json, html as H
ROOT = "/Users/cydniebrown/Desktop/cydniejocelyn-v2"
home = open(ROOT + "/index.html").read()
old = open(ROOT + "/the-build/index.html").read()

def between(s, a, b, incl=True):
    i = s.index(a); j = s.index(b, i) + (len(b) if incl else 0)
    return s[i:j]

sprite = between(home, '<svg width="0" height="0" style="position:absolute"', '</svg>')
header = between(home, '<header class="hv-hdr"', '</header>')
footer = between(home, '<footer class="hv-ftr">', '</footer>')
scripts = between(home, '<script>\n(function () {\n  var hdr', '</body>', incl=False)
stamp = re.search(r'lux\.css\?v=([0-9a-f]+)', home).group(1)

def up(s):
    return s.replace('src="assets/', 'src="../assets/').replace('href="assets/', 'href="../assets/').replace(' assets/img', ' ../assets/img')

header = up(header).replace('<li><a href="/the-build/">Work with me</a></li>', '<li><a href="/the-build/" aria-current="page">Work with me</a></li>')
assert 'aria-current="page"' in header
footer = up(footer)
scripts = up(scripts).replace('src="/sounding-popup.js"', 'src="/sounding-popup.js"')
# the reveal list for this page
scripts = scripts.replace('var groups = [', 'var groups = [".ww-head", ".ww-problem", ".ww-fix", ".ww-profiles > li", ".ww-who-note", ".ww-steps > li", ".ww-group", ".ww-std > li", ".ww-case > *", ')
scripts = scripts.replace('var imgs = [', 'var imgs = [')

CALL = "https://clients.cydniejocelyn.com/schedule/69f9f2a095c611cc2401eec7"
SOUND = "https://clients.cydniejocelyn.com/schedule/6a185c26693e14802690e9f6"
ARW = '<svg viewBox="0 0 16 10" fill="none" aria-hidden="true"><path d="M11 1l4 4-4 4M15 5H0" stroke="currentColor" stroke-width="1.2"/></svg>'

FAQ = [
 ("Do you publish your pricing?", "Yes. Every service on this page has a published price or a starting price, and the full figure for your scope is in writing before you sign anything. Retreat pricing is on each retreat page."),
 ("How do I start working with you?", "Book a free 30-minute call. If we are a fit, the next step is the Sounding, a 90-minute strategy session with a written report of findings and recommendations two days later. The $300 comes off your project."),
 ("Can we keep working together after the project?", "Yes. Once your first project is finished, you can stay on with a Monthly Partnership: strategy every month, and hands-on help with content, operations and business development. It is scoped with you at the end of that project."),
 ("How long does a Season Partnership take?", "It is scoped in a written proposal before either of us commits. The length depends on how much operations work is in play."),
 ("Can I edit the website myself?", "No, and that is on purpose. The site is written in code, so no theme limits it and no plugin update breaks it. Content changes come through me on the Complete care plan."),
 ("Do you work with clients outside Minnesota?", "Yes. I am based in Forest Lake, Minnesota, and work with founders and leaders across the United States. Most engagements run remotely, and I work in person around the Twin Cities."),
 ("What is your background?", "Fourteen years in corporate marketing before this practice. That is where the diagnostic comes from: I have seen the inside of enough businesses to spot the pattern quickly."),
]

def price(label, amount):
    return '<span class="hv-price">%s<b>%s</b></span>' % (label, amount)

def item(name, desc, tags, pr, extra="", link=""):
    t = "".join("<li>%s</li>" % x for x in tags)
    return '<div class="ww-item%s"><h4>%s</h4>%s<p>%s</p>%s%s</div>' % (extra, name, pr, desc, ('<ul role="list">%s</ul>' % t) if tags else "", link)

menu = '''
      <div class="ww-group">
        <h3>Start here</h3>
        %s
        %s
      </div>
      <div class="ww-group">
        <h3>The Build &middot; the core work</h3>
        %s
        %s
        %s
      </div>
      <div class="ww-group">
        <h3>After launch</h3>
        %s
      </div>
      <div class="ww-group">
        <h3>On its own</h3>
        %s
        %s
        %s
      </div>''' % (
  item("Free Call", "Thirty minutes to see if we are a fit. No pitch, no pressure.", [], price("30 minutes", "Free"), link='<a class="hv-link" href="%s" data-cta="free-call-menu">Book the call</a>' % CALL),
  item("The Sounding", "A 90-minute strategy session on the whole business, then my full take in writing two days later: what is load bearing, and my recommendations in order. The fee comes off your project.", [], price("Flat", "$300"), link='<a class="hv-link" href="%s">Book the Sounding</a>' % SOUND),
  item("Strategy Day", "When it needs deciding. One focused day on audit, positioning and message, delivered in writing.", [], price("Flat", "$1,500")),
  item("Season Partnership", "When it needs building. Positioning and message, then how the work moves and where the next client comes from.", ["Positioning", "Operations", "Growth plan"], price("From", "$6,000")),
  item('Full Brand Launch <span class="hv-tag">Signature</span>', "All three areas in one contract: brand guide and identity, a website built in code, and the content and launch plan.", ["Identity &amp; logo", "Website", "Launch plan"], price("From", "$15,000"), extra=" ww-item--sig"),
  item('Monthly Partnership <span class="hv-tag">New</span>', "After your first project: strategy every month, and hands-on help with content, operations and business development.", [], price("Monthly", "Scoped with you"), extra=" ww-item--new"),
  item("Website", "Built in code and yours outright. No theme, no plugins, no platform to rent.", [], price("From", "$4,000")),
  item("Social &amp; Content", "One defined quarter of strategy, calendar and writing: two reels and one static a week, posted and measured.", [], price("Per quarter", "$3,600")),
  item("Site Care", "Hosting, security and backups from $95 a month. $200 a month adds an hour of updates; design beyond that is $100 an hour.", [], price("Per month from", "$95")),
)

faq_html = "\n".join('      <details><summary>%s</summary><p>%s</p></details>' % (q, a.replace("'", "&rsquo;")) for q, a in FAQ)

# ---------- structured data: the old graph, updated ----------
g = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', old, re.S).group(1))
for n in g["@graph"]:
    t = n.get("@type")
    if t == "Person":
        n["jobTitle"] = ["Brand and Business Strategist", "Brand and Business Development Consultant"]
        n["description"] = "Brand and business strategist with fourteen years in corporate marketing, partnering with founders and leaders across the United States."
    if isinstance(t, list) and "ProfessionalService" in t:
        n["description"] = "Brand, website, operations and business development partnership for founders and leaders, with every price published. Based in Forest Lake, Minnesota, working with clients across the United States."
    if t == "WebPage":
        n["name"] = "Work with me: brand and business strategy partnership"
        n["breadcrumb"]["itemListElement"][1]["name"] = "Work with me"
    if t == "Service":
        cat = n["hasOfferCatalog"]["itemListElement"]
        names = [o.get("name") for o in cat]
        if "Monthly partnership" not in names:
            cat.append({"@type": "Offer", "name": "Monthly partnership", "priceCurrency": "USD", "availability": "https://schema.org/InStock",
                        "description": "Ongoing monthly strategy and hands-on support with content, operations and business development, after a first project. Scoped with the client."})
        if "Free consultation" not in names:
            cat.insert(0, {"@type": "Offer", "name": "Free consultation", "price": "0", "priceCurrency": "USD", "availability": "https://schema.org/InStock",
                           "description": "A free 30-minute call to see whether a partnership is a fit."})
    if t == "FAQPage":
        n["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]
jsonld = json.dumps(g, indent=2, ensure_ascii=False)

page = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">

<!-- WORK WITH ME, rebuilt 25 September 2026 on the luxury system the home
     page uses (assets/css/lux.css). Her answers: offer an ongoing monthly
     partnership; name the page whatever converts best ("Work with me", with
     The Build kept as the signature engagement); keep the "won't do" list in
     a luxury tone; lead with the fourteen years. The free call is the front
     door now, then the Sounding. The old page is in git at cfd6c66. -->
<title>Work With Me | Brand &amp; Business Strategy Partner, Published Pricing</title>
<meta name="description" content="Work with Cydnie Jocelyn: a brand, website, operations and business development partner for founders and leaders. Every price published, from a $1,500 strategy day to a $15,000 full brand engagement. Free first call.">
<link rel="canonical" href="https://www.cydniejocelyn.com/the-build/">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<meta name="author" content="Cydnie Jocelyn Brown">
<meta name="theme-color" content="#FFFFFF">
<meta name="geo.region" content="US-MN">
<meta name="geo.placename" content="Forest Lake, Minnesota">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Cydnie Jocelyn">
<meta property="og:url" content="https://www.cydniejocelyn.com/the-build/">
<meta property="og:title" content="Work with Cydnie Jocelyn | Brand &amp; Business Strategy Partner">
<meta property="og:description" content="Brand, website, operations and growth, in one partnership. Every price published, and the first call is free.">
<meta property="og:image" content="https://www.cydniejocelyn.com/assets/og/home-2026.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Work with Cydnie Jocelyn | Brand &amp; Business Strategy Partner">
<meta name="twitter:description" content="Brand, website, operations and growth, in one partnership. Every price published, and the first call is free.">
<meta name="twitter:image" content="https://www.cydniejocelyn.com/assets/og/home-2026.png">

<link rel="icon" href="../assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
<link rel="preload" as="image" href="../assets/img/wwm/hero-door-1100.webp" imagesrcset="../assets/img/wwm/hero-door-700.webp 700w, ../assets/img/wwm/hero-door-1100.webp 1100w, ../assets/img/wwm/hero-door-1500.webp 1500w" imagesizes="(min-width: 64rem) 30rem, 90vw" type="image/webp" fetchpriority="high">
<link rel="preload" href="/assets/fonts/instrument-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/instrument-serif-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../assets/css/site.css?v=@@STAMP@@">
<link rel="stylesheet" href="../assets/css/lux.css?v=@@STAMP@@">
<script>document.documentElement.className += " js-motion";</script>
<script type="application/ld+json">
@@JSONLD@@
</script>
</head>

<body class="hv2 ww-page">
<a class="skip" href="#main">Skip to content</a>

@@SPRITE@@

@@HEADER@@

<main id="main">

<!-- HERO. What she fixes, for whom, and the three trust signals, in the
     first screen. Rewritten 25 September at her word: "does it explain the
     business and working with me properly". -->
<section class="ww-hero" aria-labelledby="ww-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <span class="hv-label">Work with me</span>
      <h1 id="ww-h">One partner for your brand <em>and your business.</em></h1>
      <p class="hv-lede">I help founders and leaders build the brand, the website, the systems and the client pipeline behind a business that grows without running through them. Every price is on this page, and the first call is free.</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="@@CALL@@" data-cta="free-call-hero">Book a free 30-min call @@ARW@@</a>
        <a class="hv-btn hv-btn--line" href="#pricing">See every price</a>
      </div>
      <ul class="ww-trust" role="list"><li>14 years in corporate marketing</li><li>Every price published</li><li>Clients nationwide</li></ul>
    </div>
    <figure class="ww-arch">
      <img src="../assets/img/wwm/hero-door-1100.webp" srcset="../assets/img/wwm/hero-door-700.webp 700w, ../assets/img/wwm/hero-door-1100.webp 1100w, ../assets/img/wwm/hero-door-1500.webp 1500w" sizes="(min-width: 64rem) 30rem, 90vw" width="1100" height="1467" alt="Cydnie Jocelyn smiling in front of a carved wooden door, hands in her pockets" fetchpriority="high">
      <figcaption><span>Strategy days from</span><b>$1,500</b></figcaption>
    </figure>
  </div>
</section>

<!-- THE PROBLEM AND THE FIX, side by side, in one screen. The four lines
     on the left are her own, from the old page. -->
<section class="hv-sec ww-pf" aria-labelledby="ww-pf">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">The problem, and the fix</span>
      <h2 class="hv-h2" id="ww-pf">Your business shouldn&rsquo;t need <em>you in the middle</em> of everything.</h2>
    </div>
    <div class="ww-pf-grid">
      <div class="ww-problem">
        <h3>Where you are</h3>
        <ul role="list">
          <li>The revenue is fine, and the clients are happy.</li>
          <li>But every decision still runs through you.</li>
          <li>Your designer, marketer and operations help never talk to each other.</li>
          <li>Growth costs you more than it returns.</li>
        </ul>
        <p>You have outgrown doing it all yourself.</p>
      </div>
      <div class="ww-fix">
        <h3>What we build</h3>
        <dl>
          <div><dt><svg aria-hidden="true"><use href="#i-facet"/></svg>Brand</dt><dd>What you are, said so a stranger can repeat it. Positioning, identity and a website that sells it.</dd></div>
          <div><dt><svg aria-hidden="true"><use href="#i-loop"/></svg>Operations</dt><dd>How the work moves from enquiry to handoff, without you remembering every step.</dd></div>
          <div><dt><svg aria-hidden="true"><use href="#i-rise"/></svg>Business development</dt><dd>Where the next client comes from, on purpose instead of by referral luck.</dd></div>
        </dl>
        <p>One partner across all three, so nothing falls between vendors.</p>
      </div>
    </div>
  </div>
</section>

<!-- WHO THIS IS FOR. Her answer (25 September): founders launching,
     established businesses scaling, leaders building a personal brand;
     "all of the above that want a partnership and understand it comes with
     a price". Each profile names its best-fit offer. -->
<section class="hv-sec ww-who" aria-labelledby="ww-who">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Who this is for</span>
      <h2 class="hv-h2" id="ww-who">Founders and leaders who want a partner, <em>not a vendor.</em></h2>
    </div>
    <ul class="ww-profiles" role="list">
      <li>
        <h3>Launching something new</h3>
        <p>You have the vision and no brand yet. We build it from nothing and launch it to the right people.</p>
        <span class="ww-fit">Best fit <b>Full Brand Launch</b></span>
      </li>
      <li>
        <h3>Growing past yourself</h3>
        <p>The business works, but it all runs through you. We sharpen the positioning, fix how work moves and plan where the next client comes from.</p>
        <span class="ww-fit">Best fit <b>Season Partnership</b></span>
      </li>
      <li>
        <h3>Leading with your name</h3>
        <p>You are the brand. We make what you stand for clear, visible and easy to hire.</p>
        <span class="ww-fit">Best fit <b>Strategy Day</b></span>
      </li>
    </ul>
    <p class="ww-who-note">If you want someone in it with you, and you know a partnership is priced differently from a deliverable, we will work well together.</p>
  </div>
</section>

<!-- HOW IT WORKS. Four stages, a real order, so they are numbered. -->
<section class="hv-sec ww-path" aria-labelledby="ww-path">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">How it works</span>
      <h2 class="hv-h2" id="ww-path">From a first call to a <em>lasting partnership.</em></h2>
    </div>
    <ol class="ww-steps" role="list">
      <li><h3>Free call</h3><p>Thirty minutes to see if we are a fit. No pitch, no pressure.</p><span class="hv-meta">Free</span></li>
      <li><h3>The Sounding</h3><p>A 90-minute strategy session, then my full take and recommendations in writing two days later.</p><span class="hv-meta">$300, credited to your project</span></li>
      <li><h3>The Build</h3><p>The core work, scoped in writing before either of us commits.</p><span class="hv-meta">From $1,500</span></li>
      <li><h3>Monthly partnership</h3><p>If you want me in it with you after launch, I stay.</p><span class="hv-meta">Optional</span></li>
    </ol>
  </div>
</section>

<!-- THE PRICE MENU. One set of names, shared with the home page. -->
<section class="hv-sec" id="pricing" aria-labelledby="ww-price">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Investment</span>
      <h2 class="hv-h2" id="ww-price">Every price, <em>before you book.</em></h2>
      <p class="hv-lede">Starting prices, published. Your exact figure is in writing before you sign anything.</p>
    </div>
    <div class="ww-menu">@@MENU@@
    </div>
    <p class="ww-menu-note">Looking for the retreats? <a class="hv-inline" href="/retreats/">They book directly</a>, no call needed.</p>
  </div>
</section>

<!-- THE WORK. The positioning decision leads each one. -->
<section class="hv-sec ww-work" id="work" aria-labelledby="ww-work">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Client work</span>
      <h2 class="hv-h2" id="ww-work">Three businesses, <em>three decisions.</em></h2>
      <p class="hv-lede">The positioning came first. The identity followed it.</p>
    </div>
    <ul class="ww-cases" role="list">
      <li class="ww-case">
        <div class="hv-feature-media">
          <div class="hv-browser"><div><img src="../assets/img/work/mane-alchemist-desktop-1400.webp" srcset="../assets/img/work/mane-alchemist-desktop-800.webp 800w, ../assets/img/work/mane-alchemist-desktop-1400.webp 1400w" sizes="(min-width: 60rem) 42rem, 92vw" width="1400" height="788" alt="Mane Alchemist Salon website home page, dark green with a gold art deco wordmark" loading="lazy"></div></div>
          <div class="hv-phone"><div><img src="../assets/img/work/mane-alchemist-screen-500.webp" width="500" height="1095" alt="Mane Alchemist Salon website on a phone" loading="lazy"></div></div>
        </div>
        <div>
          <span class="hv-label">Full Brand Launch</span>
          <h3>Mane Alchemist Salon</h3>
          <p class="ww-decision">Positioned away from the wellness salon default and toward deliberate luxury.</p>
          <ul role="list"><li>Logo</li><li>Brand guide</li><li>Voice</li><li>Website</li><li>90-day social launch</li><li>Quarterly content</li></ul>
          <blockquote>&ldquo;She listens with intention, quickly understands your vision, and brings it to life with ease.&rdquo;<cite>Tamara, Mane Alchemist Salon</cite></blockquote>
          <a class="hv-link" href="https://manealchemistsalon.com" target="_blank" rel="noopener">Visit the site<span class="hv-vh"> (opens in a new tab)</span></a>
        </div>
      </li>
    </ul>
    <ul class="hv-cases ww-cases-2" role="list">
      <li class="hv-case">
        <div class="hv-browser"><div><img src="../assets/img/work/srs-performance-desktop-1400.webp" srcset="../assets/img/work/srs-performance-desktop-800.webp 800w, ../assets/img/work/srs-performance-desktop-1400.webp 1400w" sizes="(min-width: 48rem) 36rem, 92vw" width="1400" height="788" alt="SRS Performance website home page, purple wordmark over athletes training" loading="lazy"></div></div>
        <span class="hv-label">Brand &amp; operations</span>
        <h3>SRS Performance</h3>
        <p class="ww-decision">Narrowed from general fitness to former competitive athletes.</p>
        <p>&ldquo;She helped redesign how I operate!&rdquo; &mdash; Spencer Scott</p>
        <a class="hv-link" href="https://srsperform.com" target="_blank" rel="noopener">Visit the site<span class="hv-vh"> (opens in a new tab)</span></a>
      </li>
      <li class="hv-case">
        <div class="hv-browser"><div><img src="../assets/img/work/solyrey-desktop-1400.webp" srcset="../assets/img/work/solyrey-desktop-800.webp 800w, ../assets/img/work/solyrey-desktop-1400.webp 1400w" sizes="(min-width: 48rem) 36rem, 92vw" width="1400" height="788" alt="SolyRey website home page, a yellow van on a desert road" loading="lazy"></div></div>
        <span class="hv-label">Brand refresh</span>
        <h3>SolyRey</h3>
        <p class="ww-decision">The promise moved from the destination to the logistics being handled.</p>
        <p>Logo, brand guide and a complete website relaunch.</p>
        <a class="hv-link" href="https://solyrey.com" target="_blank" rel="noopener">Visit the site<span class="hv-vh"> (opens in a new tab)</span></a>
      </li>
    </ul>
  </div>
</section>

<!-- STANDARDS: "Here is what I won't do", in a luxury tone at her word. -->
<section class="hv-sec ww-standards" aria-labelledby="ww-std">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">My standards</span>
      <h2 class="hv-h2" id="ww-std">What you can <em>count on.</em></h2>
    </div>
    <ul class="ww-std" role="list">
      <li><b>Never more than you need.</b><span>If the honest answer is smaller, that is the answer you get.</span></li>
      <li><b>Nothing templated.</b><span>Nothing here was sold to someone else first.</span></li>
      <li><b>Positioning before logo.</b><span>Identity follows the positioning it has to carry.</span></li>
      <li><b>A finish line on every project.</b><span>After it, stay on monthly only if you want to.</span></li>
      <li><b>Straight talk, not coaching.</b><span>I will tell you what I think, clearly and kindly.</span></li>
      <li><b>No invented promises.</b><span>No one honest can promise you a revenue number.</span></li>
    </ul>
  </div>
</section>

<section class="hv-sec" id="faq" aria-labelledby="faq-h">
  <div class="hv-wrap hv-faq ww-faq">
    <div>
      <span class="hv-label">Questions</span>
      <h2 class="hv-h2" id="faq-h">Before you <em>book.</em></h2>
      <p class="hv-lede">Something not here? <a class="hv-inline" href="/contact/">Ask me directly.</a> I answer every one myself.</p>
    </div>
    <div class="hv-faq-list">
@@FAQ@@
    </div>
  </div>
</section>

<section class="hv-close" aria-labelledby="close-h">
  <div class="hv-wrap">
    <span class="hv-label hv-label--c">Let&rsquo;s begin</span>
    <h2 class="hv-h2" id="close-h">You already know what <em>isn&rsquo;t working.</em></h2>
    <p class="hv-lede">Thirty minutes, free. You will leave knowing whether a partnership makes sense, and what the first move would be.</p>
    <div class="hv-btns">
      <a class="hv-btn hv-btn--ink" href="@@CALL@@" data-cta="free-call-close">Book a free 30-min call @@ARW@@</a>
      <a class="hv-btn hv-btn--line" href="@@SOUND@@">Or book the Sounding, $300</a>
    </div>
    <small>Or write to me at <a class="hv-inline" href="mailto:hello@cydniejocelyn.com">hello@cydniejocelyn.com</a></small>
  </div>
</section>

</main>

@@FOOTER@@

@@SCRIPTS@@</body>
</html>
'''
for k, v in [("JSONLD", jsonld), ("SPRITE", sprite), ("HEADER", header), ("FOOTER", footer), ("SCRIPTS", scripts),
             ("MENU", menu), ("FAQ", faq_html), ("STAMP", stamp), ("CALL", CALL), ("SOUND", SOUND), ("ARW", ARW)]:
    page = page.replace("@@%s@@" % k, v)
open(ROOT + "/the-build/index.html", "w").write(page)
print("written", len(page))
