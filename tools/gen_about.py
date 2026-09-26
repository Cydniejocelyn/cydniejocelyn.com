"""About (/about/), rebuilt 25 September 2026 on the luxury system.

Her answers: the short version of her story first with the full story
below it; her faith stays the foundation, in its own section; the fourteen
years become what clients buy ("business development and relationship
building and creative ideas to life. Seeing a vision before it's completed
and initiating and completing it"); the best testimonials only. Removed:
Clarify / Reclaim / Build, "Come up", the exit line ("yours whether or not
we ever speak again"), and the Sounding as the only button. Her own words
are kept wherever they exist; the few bridging lines that are mine are
marked BRIDGE below so she can check them.

    cd tools && python3 gen_about.py
"""
import lux_page as L

URL = L.SITE + "/about/"
CALL, SOUND, ARW = L.CALL, L.SOUND, L.ARW

FAQ = []  # About has no FAQ; the questions live on Work with me and the Sounding.

Q = lambda quote, body, who, where: (
    '<li><figure class="hv-q"><blockquote><p>&ldquo;%s&rdquo;</p><p>%s</p></blockquote>'
    '<figcaption>%s &middot; %s</figcaption></figure></li>' % (quote, body, who, where))

MAIN = """<main id="main">

<!-- HERO. Her full name and her role in the first screen, for search and
     for AI answers. Second pass, 25 September: her note "the layouts don't
     align properly and are overloaded ... impactful, SEO driven and
     converting to who I am and wanting to work with me". -->
<section class="ww-hero" aria-labelledby="au-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <span class="hv-label">Brand &amp; business strategist</span>
      <h1 id="au-h">I&rsquo;m <em>Cydnie Jocelyn.</em></h1>
      <p class="hv-lede">I partner with founders and leaders on brand, website, operations and business development. Fourteen years in corporate marketing taught me to see a vision before it is built, and then build it with you, start to finish.</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="%(CALL)s" data-cta="free-call-about">Book a free 30-min call %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="/the-build/">Work with me</a>
      </div>
      <ul class="ww-trust" role="list"><li>14 years in corporate marketing</li><li>Forest Lake, Minnesota</li><li>Partnering nationwide</li></ul>
    </div>
    <figure class="ww-arch">
      <img src="../assets/img/cydnie-hero-1000.webp" srcset="../assets/img/cydnie-hero-700.webp 700w, ../assets/img/cydnie-hero-1000.webp 1000w, ../assets/img/cydnie-hero-1400.webp 1400w" sizes="(min-width: 64rem) 30rem, 90vw" width="1000" height="1500" alt="Cydnie Jocelyn, brand and business strategist, smiling at her laptop in her studio" fetchpriority="high">
    </figure>
  </div>
</section>

<!-- AT A GLANCE. The facts an AI answer or a skimming buyer wants, as a
     definition list. Every line is hers: her answers of 25 September and
     the site's published offer. -->
<section class="hv-sec" aria-labelledby="au-bring">
  <div class="hv-wrap au-row">
    <div>
      <span class="hv-label">What I bring</span>
      <h2 class="hv-h2" id="au-bring">I see the finished thing <em>before it exists.</em></h2>
      <p class="hv-lede">Then I start it, and see it through with you. That is what fourteen years in corporate marketing left me with, and what every client gets.</p>
    </div>
    <dl class="au-facts-dl">
      <div><dt>Experience</dt><dd>Fourteen years in corporate marketing</dd></div>
      <div><dt>Strengths</dt><dd>Business development, relationship building, bringing creative ideas to life, and seeing a vision through to completion</dd></div>
      <div><dt>I work with</dt><dd>Founders and leaders launching something new, growing past themselves, or leading with their own name</dd></div>
      <div><dt>What we build</dt><dd>Brand, websites, operations and business development, in one partnership</dd></div>
      <div><dt>Based</dt><dd>Forest Lake, Minnesota, partnering with clients nationwide</dd></div>
      <div><dt>Also</dt><dd>Small-group retreats for women</dd></div>
    </dl>
  </div>
</section>

<!-- MY STORY. Her four moments, her words, beside one photograph, both
     columns starting on the same line. -->
<section class="hv-sec au-story" aria-labelledby="au-story">
  <div class="hv-wrap au-row">
    <figure class="au-photo"><img src="../assets/img/cydnie-window-1000.webp" srcset="../assets/img/cydnie-window-600.webp 600w, ../assets/img/cydnie-window-1000.webp 1000w" sizes="(min-width: 60rem) 26rem, 92vw" width="1000" height="1500" alt="Cydnie Jocelyn smiling by a sunlit window, one hand in her hair" loading="lazy"></figure>
    <div>
      <span class="hv-label">My story</span>
      <h2 class="hv-h2" id="au-story">They told me I didn&rsquo;t have a choice. <em>I told them I did.</em></h2>
      <ol class="au-moments" role="list">
        <li><span>Fourteen years</span><p>I had been performing a strength I did not have since I was a teenager. It looked like doing well, and I could not have told you the last time I felt like myself.</p></li>
        <li><span>Then it got loud</span><p>A wedding in three months, our first son twenty weeks later, and two and a half years lost to postpartum depression while I gave everything to a company that taught me I was replaceable.</p></li>
        <li><span>2025</span><p>On a retreat I booked for myself, work told me I didn&rsquo;t have a choice. I texted back, shaking, that I did. I chose my family.</p></li>
        <li><span>After</span><p>I built what came next while my boys were in and out of the hospital and my husband had a stroke at thirty-six. The time was finally mine to choose.</p></li>
      </ol>
      <!-- BRIDGE: mine, not hers. Read it to her. -->
      <p class="au-why">That is why I build businesses that don&rsquo;t need their owner in the middle of everything. <em>I know what it costs.</em></p>
    </div>
  </div>
</section>

<!-- WHAT HELD. Her faith as the foundation, lighter: her testimony and the
     three verses, without the reflection paragraphs. -->
<section class="hv-sec au-faith" aria-labelledby="au-faith">
  <div class="hv-wrap au-row">
    <div>
      <span class="hv-label">What held</span>
      <h2 class="hv-h2" id="au-faith">God isn&rsquo;t an afterthought. <em>He is the whole foundation.</em></h2>
    </div>
    <div class="au-faith-copy">
      <p>In April 2025, at my breaking point, I joined a women&rsquo;s bible study and surrendered my life to Him. That fall I was baptized, and gave my testimony in front of eight hundred people.</p>
      <p class="au-meet">God is in my life, so He is in how I work. He does not have to be in yours. I meet you where you are.</p>
      <ul class="au-verses" role="list">
        <li><b>Ephesians 2:10</b>You were made on purpose.</li>
        <li><b>Isaiah 43:19</b>The pivots are where God does His best work.</li>
        <li><b>Galatians 1:10</b>You were never meant to stay in rooms that required you to be less.</li>
      </ul>
    </div>
  </div>
</section>

<!-- CLIENTS. Three client quotes in one row. The retreat voices and
     Melissa's video belong to the retreat pages. -->
<section class="hv-sec" aria-labelledby="au-words">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Clients</span>
      <h2 class="hv-h2" id="au-words">In <em>their words.</em></h2>
    </div>
    <ul class="hv-quotes au-quotes" role="list">
      %(Q1)s
      %(Q2)s
      %(Q3)s
    </ul>
  </div>
</section>

<!-- THE REST OF ME. One photograph and her list, word for word. -->
<section class="hv-sec au-rest" aria-labelledby="au-rest">
  <div class="hv-wrap au-row">
    <figure class="au-photo"><img src="../assets/img/cydnie-sing-1000.webp" srcset="../assets/img/cydnie-sing-600.webp 600w, ../assets/img/cydnie-sing-1000.webp 1000w" sizes="(min-width: 60rem) 26rem, 92vw" width="1000" height="1500" alt="Cydnie singing into a microphone with headphones on, eyes closed" loading="lazy"></figure>
    <div>
      <span class="hv-label">Also true</span>
      <h2 class="hv-h2" id="au-rest">The rest <em>of me.</em></h2>
      <ul class="au-facts" role="list">
        <li>I sing. Not in front of people.</li>
        <li>My spirit animal is somewhere between a cheetah and a turtle.</li>
        <li>I drink a truly unreasonable amount of water, and I am unbothered about it.</li>
        <li>Currently reading ACOTAR and a Proverb a day.</li>
        <li>There is a craft room in my house that I use more than I let on.</li>
      </ul>
    </div>
  </div>
</section>

<section class="hv-close" aria-labelledby="close-h">
  <div class="hv-wrap">
    <span class="hv-label hv-label--c">Let&rsquo;s begin</span>
    <h2 class="hv-h2" id="close-h">Let&rsquo;s build what&rsquo;s next, <em>together.</em></h2>
    <p class="hv-lede">Thirty minutes, free, and you will leave knowing whether a partnership makes sense for your business.</p>
    <div class="hv-btns">
      <a class="hv-btn hv-btn--ink" href="%(CALL)s" data-cta="free-call-about-close">Book a free 30-min call %(ARW)s</a>
    </div>
    <p class="au-also">Or <a class="hv-inline" href="/retreats/">come on a retreat</a>, or <a class="hv-inline" href="/the-letters/">read the Letters</a>.</p>
  </div>
</section>

</main>
""" % {
    "CALL": CALL, "ARW": ARW,
    "Q1": Q("She is truly an invaluable asset.", "She listens with intention, quickly understands your vision, and brings it to life with ease.", "Tamara", "Mane Alchemist Salon"),
    "Q2": Q("She helped redesign how I operate.", "Cydnie is very knowledgeable and incredibly dedicated.", "Spencer Scott", "SRS Performance"),
    "Q3": Q("Her words land right where you need them.", "Her online presence reflects the warmth and wisdom she brings to every interaction.", "Angela", "Consulting client"),
}

graph = L.old_graph("about/index.html")
for n in graph:
    t = n.get("@type")
    if t in ("AboutPage", "WebPage", "ProfilePage") or (isinstance(t, list) and "AboutPage" in t):
        n["name"] = "About Cydnie Jocelyn, brand and business strategist"
        n["mainEntity"] = {"@id": "https://www.cydniejocelyn.com/#cydnie"}
    if t == "Person":
        n["jobTitle"] = ["Brand and Business Strategist", "Retreat Host"]
        n["knowsAbout"] = ["brand strategy", "business development", "relationship building", "business operations", "website design", "retreat design"]
        n["homeLocation"] = {"@type": "Place", "name": "Forest Lake, Minnesota"}
        n["image"] = "https://www.cydniejocelyn.com/assets/img/cydnie-hero-1000.webp"
        n["description"] = ("Brand and business strategist with fourteen years in corporate marketing: business development, "
                            "relationship building and bringing creative ideas to life. Based in Forest Lake, Minnesota, "
                            "partnering with founders and leaders across the United States.")
    if isinstance(t, list) and "ProfessionalService" in t:
        n["description"] = ("Brand, website, operations and business development partnership for founders and leaders, "
                            "with every price published. Based in Forest Lake, Minnesota, working with clients across the United States.")

PRELOAD = ('<link rel="preload" as="image" href="../assets/img/cydnie-hero-1000.webp" '
           'imagesrcset="../assets/img/cydnie-hero-700.webp 700w, ../assets/img/cydnie-hero-1000.webp 1000w, '
           '../assets/img/cydnie-hero-1400.webp 1400w" imagesizes="(min-width: 64rem) 30rem, 90vw" '
           'type="image/webp" fetchpriority="high">\n')

n = L.render(
    out="about/index.html", depth=1, active="/about/",
    title="About Cydnie Jocelyn | Brand & Business Strategist, Minnesota",
    description="Cydnie Jocelyn is a brand and business strategist with fourteen years in corporate marketing. Forest Lake, Minnesota, partnering with founders nationwide.",
    canonical=URL,
    og_title="About Cydnie Jocelyn | Brand & Business Strategist, Minnesota",
    og_description="Fourteen years in corporate marketing, one partner for your brand and your business. Her story, her faith, and why she does this work.",
    graph=graph, main=MAIN, preload=PRELOAD, body_class="ww-page",
    reveal=(".ww-head", ".au-row > div", ".au-facts-dl > div", ".au-moments > li", ".au-quotes > li"),
    reveal_imgs=(".au-photo",),
)
print("written", n)
