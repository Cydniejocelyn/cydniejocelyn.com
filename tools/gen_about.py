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

<!-- HERO: who she is, what she does, why she is good at it. -->
<section class="ww-hero" aria-labelledby="au-h">
  <div class="hv-wrap ww-hero-grid">
    <div class="ww-hero-copy">
      <span class="hv-label">About</span>
      <h1 id="au-h">I&rsquo;m <em>Cydnie.</em></h1>
      <p class="hv-lede">A brand and business partner for founders and leaders. Fourteen years in corporate marketing taught me to see a vision before it is built, and then to build it, start to finish.</p>
      <div class="hv-btns">
        <a class="hv-btn hv-btn--ink" href="%(CALL)s" data-cta="free-call-about">Book a free 30-min call %(ARW)s</a>
        <a class="hv-btn hv-btn--line" href="/the-build/">Work with me</a>
      </div>
      <ul class="ww-trust" role="list"><li>14 years in corporate marketing</li><li>Forest Lake, Minnesota</li><li>Partnering nationwide</li></ul>
    </div>
    <figure class="ww-arch">
      <img src="../assets/img/cydnie-hero-1000.webp" srcset="../assets/img/cydnie-hero-700.webp 700w, ../assets/img/cydnie-hero-1000.webp 1000w, ../assets/img/cydnie-hero-1400.webp 1400w" sizes="(min-width: 64rem) 30rem, 90vw" width="1000" height="1500" alt="Cydnie Jocelyn smiling at her laptop in her studio" fetchpriority="high">
    </figure>
  </div>
</section>

<!-- WHAT I BRING: the fourteen years as the thing clients buy, in her
     words of 25 September. -->
<section class="hv-sec" aria-labelledby="au-bring">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">What I bring</span>
      <h2 class="hv-h2" id="au-bring">I see the finished thing <em>before it exists.</em></h2>
      <p class="hv-lede">Fourteen years in corporate marketing, and what they left me with is what every client gets.</p>
    </div>
    <ul class="au-gifts" role="list">
      <li><svg aria-hidden="true"><use href="#i-rise"/></svg><h3>Business development</h3><p>Knowing where the next client comes from, and how to walk in the door.</p></li>
      <li><svg aria-hidden="true"><use href="#i-hand"/></svg><h3>Relationship building</h3><p>The trust that turns a first call into a partnership, and a client into a referral.</p></li>
      <li><svg aria-hidden="true"><use href="#i-spark"/></svg><h3>Ideas brought to life</h3><p>Taking the creative idea out of your head and making it real, on the page and in the market.</p></li>
      <li><svg aria-hidden="true"><use href="#i-facet"/></svg><h3>Vision to completion</h3><p>Seeing it before it is finished, starting it, and seeing it through.</p></li>
    </ul>
  </div>
</section>

<!-- MY STORY: the short version, four moments, all her own words from the
     old page, trimmed. -->
<section class="hv-sec au-story" aria-labelledby="au-story">
  <div class="hv-wrap au-story-grid">
    <div class="au-story-head">
      <span class="hv-label">My story</span>
      <h2 class="hv-h2" id="au-story">They told me I didn&rsquo;t have a choice. <em>I told them I did.</em></h2>
      <figure class="au-story-img"><img src="../assets/img/cydnie-window-1000.webp" srcset="../assets/img/cydnie-window-600.webp 600w, ../assets/img/cydnie-window-1000.webp 1000w" sizes="(min-width: 60rem) 24rem, 92vw" width="1000" height="1500" alt="Cydnie Jocelyn laughing by a sunlit window, one hand in her hair" loading="lazy"></figure>
    </div>
    <ol class="au-moments" role="list">
      <li><span>Fourteen years</span><p>I had been performing a strength I did not have since I was a teenager. It looked like doing well, and I could not have told you the last time I felt like myself.</p></li>
      <li><span>Then it got loud</span><p>A wedding planned in three months, and our first son twenty weeks later. I lost the first two and a half years of his life to postpartum depression while giving everything I had to a company that taught me I was replaceable.</p></li>
      <li><span>2025</span><p>I booked a trip for myself, a retreat, as a guest in a group of fifteen where I knew nobody. Two days in, work told me I didn&rsquo;t have a choice. I texted back, shaking, that I did, and that I chose my family and my children&rsquo;s health.</p></li>
      <li><span>After</span><p>I put my notice in, and I built what came next while my boys were in and out of the hospital and my husband had a stroke at thirty-six. Nobody was coming to do it for me. The time was finally mine to choose.</p></li>
    </ol>
  </div>
  <!-- BRIDGE: this closing line is mine, tying the story to the work. -->
  <div class="hv-wrap"><p class="au-why">That is why I build businesses that don&rsquo;t need their owner in the middle of everything. <em>I know what it costs.</em></p></div>
</section>

<!-- WHAT HELD: her faith, kept as the foundation at her word. -->
<section class="hv-sec ww-standards au-faith" aria-labelledby="au-faith">
  <div class="hv-wrap au-faith-grid">
    <div>
      <span class="hv-label">What held</span>
      <h2 class="hv-h2" id="au-faith">God isn&rsquo;t an afterthought. <em>He is the whole foundation.</em></h2>
    </div>
    <div class="au-faith-copy">
      <p>In April 2025, at my breaking point, I joined a women&rsquo;s bible study. The first day I walked into that church, I raised my hand and surrendered my life to Him.</p>
      <p>That fall I was baptized, and gave my testimony in front of eight hundred people. Days before, I almost backed out. I went under shaking, and I have never felt relief like coming up out of that water.</p>
      <p class="au-meet">God is in my life, so He is in how I work. He does not have to be in yours. I meet you where you are.</p>
    </div>
  </div>
  <div class="hv-wrap">
    <ul class="au-verses" role="list">
      <li><b>Ephesians 2:10</b><span>You were made on purpose.</span><p>For fourteen years I thought being useful was the same thing as being made for something. It took losing the job to find out how much smaller useful is.</p></li>
      <li><b>Isaiah 43:19</b><span>The pivots are where God does His best work.</span><p>Two and a half years of not moving, then three days to decide, and I still could not have told you why I booked it.</p></li>
      <li><b>Galatians 1:10</b><span>You were never meant to stay in rooms that required you to be less.</span><p>I stayed in one for fourteen years and called it being competent.</p></li>
    </ul>
  </div>
</section>

<!-- IN THEIR WORDS: the best six, clients first, and Melissa's video. -->
<section class="hv-sec" aria-labelledby="au-words">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Clients and guests</span>
      <h2 class="hv-h2" id="au-words">In <em>their words.</em></h2>
    </div>
    <div class="au-words-grid">
      <ul class="hv-quotes au-quotes" role="list">
        %(Q1)s
        %(Q2)s
        %(Q3)s
        %(Q4)s
        %(Q5)s
        %(Q6)s
      </ul>
      <figure class="au-vid">
        <a class="rt-play melissa-play" data-video="DrrP4hdw0lo" data-src="../assets/video/melissa.mp4" data-start="3" data-title="Melissa on the Costa Rica retreat" href="../assets/video/melissa.mp4#t=3">
          <img src="../assets/img/retreats/melissa-poster-405.webp" srcset="../assets/img/retreats/melissa-poster-300.webp 300w, ../assets/img/retreats/melissa-poster-405.webp 405w" sizes="(min-width: 60rem) 20rem, 74vw" width="405" height="720" loading="lazy" decoding="async" alt="Melissa, speaking to her phone camera in her car on the way home from the retreat.">
          <span class="au-play" aria-hidden="true"><svg width="18" height="20" viewBox="0 0 18 20" fill="currentColor"><path d="M0 0l18 10L0 20z"/></svg></span>
          <span class="hv-vh">Play Melissa&rsquo;s video about the Costa Rica retreat</span></a>
        <figcaption><b>&ldquo;I learned that I matter too.&rdquo;</b> Melissa, on the drive home from Costa Rica.</figcaption>
      </figure>
    </div>
  </div>
</section>

<!-- THE REST OF ME: her list, word for word. -->
<section class="hv-sec au-rest" aria-labelledby="au-rest">
  <div class="hv-wrap au-rest-grid">
    <div class="au-rest-imgs">
      <img src="../assets/img/cydnie-sing-1000.webp" srcset="../assets/img/cydnie-sing-600.webp 600w, ../assets/img/cydnie-sing-1000.webp 1000w" sizes="(min-width: 60rem) 16rem, 44vw" width="1000" height="1500" alt="Cydnie singing into a microphone with headphones on, eyes closed" loading="lazy">
      <img src="../assets/img/cydnie-mug-600.webp" width="600" height="900" alt="Cydnie laughing on a sofa with a mug of tea" loading="lazy">
    </div>
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

<!-- WHERE TO BEGIN: the three doors, in the site's one set of names. -->
<section class="hv-sec" aria-labelledby="au-begin">
  <div class="hv-wrap">
    <div class="ww-head">
      <span class="hv-label">Where to begin</span>
      <h2 class="hv-h2" id="au-begin">Three ways <em>in.</em></h2>
    </div>
    <ul class="ww-profiles au-doors" role="list">
      <li><h3>Work with me</h3><p>Brand, website, operations and growth, in one partnership. It starts with a free 30-minute call, then the Sounding.</p><a class="hv-link" href="%(CALL)s" data-cta="free-call-about-doors">Book a free call</a></li>
      <li><h3>Come on a retreat</h3><p>Small groups for women who hold everything together. I went to one as a guest first, and it is the reason all of this exists.</p><a class="hv-link" href="/retreats/">See the retreats</a></li>
      <li><h3>Read the Letters</h3><p>One letter a week about what it costs to run the thing you built. Free, and written the week it goes out.</p><a class="hv-link" href="/the-letters/">Get the Letters</a></li>
    </ul>
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
    <p class="hv-sign">Cydnie</p>
  </div>
</section>

</main>
""" % {
    "CALL": CALL, "ARW": ARW,
    "Q1": Q("She is truly an invaluable asset.", "She listens with intention, quickly understands your vision, and brings it to life with ease.", "Tamara", "Mane Alchemist Salon"),
    "Q2": Q("She helped redesign how I operate.", "Cydnie is very knowledgeable and incredibly dedicated.", "Spencer Scott", "SRS Performance"),
    "Q3": Q("Her words land right where you need them.", "Her online presence reflects the warmth and wisdom she brings to every interaction.", "Angela", "Consulting client"),
    "Q4": Q("The fact that you&rsquo;re even considering it should tell you that you should go.", "You&rsquo;ll come out the other end with new people in your life.", "Kristi", "Retreat guest, Costa Rica"),
    "Q5": Q("No waiting, no rushing.", "Intimate group size, and leaders able to make us think, laugh and cry without judgement.", "Carol", "Retreat guest, Costa Rica"),
    "Q6": Q("I left being able to breathe.", "I walked in carrying fear that the experience would take more from me than I had to give.", "BJB", "Retreat guest, Costa Rica"),
}

graph = L.old_graph("about/index.html")
for n in graph:
    t = n.get("@type")
    if t in ("AboutPage", "WebPage", "ProfilePage") or (isinstance(t, list) and "AboutPage" in t):
        n["name"] = "About Cydnie Jocelyn, brand and business strategist"
    if t == "Person":
        n["jobTitle"] = ["Brand and Business Strategist", "Retreat Host"]
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
    title="About Cydnie Jocelyn | Brand & Business Strategist",
    description="Cydnie Jocelyn is a brand and business strategist with fourteen years in corporate marketing: business development, relationship building and bringing ideas to life. Forest Lake, Minnesota, partnering nationwide.",
    canonical=URL,
    og_title="About Cydnie Jocelyn | Brand & Business Strategist",
    og_description="Fourteen years in corporate marketing, one partner for your brand and your business. Her story, her faith, and why she does this work.",
    graph=graph, main=MAIN, preload=PRELOAD, body_class="ww-page",
    reveal=(".ww-head", ".au-gifts > li", ".au-moments > li", ".au-why", ".au-faith-grid > div", ".au-verses > li",
            ".au-quotes > li", ".au-rest-grid > div:last-child", ".au-doors > li"),
    reveal_imgs=(".au-story-img", ".au-rest-imgs img", ".au-vid"),
)
print("written", n)
