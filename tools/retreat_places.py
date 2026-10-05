"""The retreat guide pages: one entry per page under /womens-retreats/, and
the single source for every link to them (footer column aside, which is in
index.html by hand).

Started 5 October 2026 on Cydnie's brief: five pages optimised for search on
"retreats, wellness retreats, leadership retreats", built to send people to
the two open retreats (Gatlinburg and Arizona). Her answers: "wellness" is
fine on retreat pages, guest reviews go on every retreat page, the podcast is
off the table. Every fact here is taken from the retreat pages themselves;
never a group size (a small group, never a count), never an average score.

    python3 tools/gen_retreat_places.py
"""
BASE = "/womens-retreats/"
PRIVATE = "https://www.honeybook.com/widget/cydnie_jocelyn_collective_299013/cf_id/69fa33ac59c6a6842e88b725"
GREECE_WAIT = "https://clients.cydniejocelyn.com/public/6a21d07b6dcfbe3d85c663b6"

# The three retreats, as cards. Facts match the event pages on 5 October 2026.
# 31 OCTOBER / 30 NOVEMBER: the early rates below change; update with
# gen_gatlinburg.py and gen_arizona.py (HANDOFF 62 and 68).
RETREATS = {
  "gat": dict(
    tag="Booking now", when="13&ndash;18 April 2027", where="Gatlinburg, Tennessee",
    name="Wide Open: The Gatlinburg Edition", href="/retreats/gatlinburg/",
    text="Five days in a private house at the edge of the Great Smoky Mountains with Kayla Freeman and me. Lodging, every meal, daily movement, two workshops and two outings are included.",
    price="Shared room $1,490 &middot; private king suite $2,790",
    note="Early rate through 31 October. $500 holds your room."),
  "az": dict(
    tag="Booking now", when="5&ndash;9 May 2027", where="Peoria, Arizona",
    name="Wild Canvas: The Arizona Edition", href="/retreats/arizona/",
    text="Five days in a painted house on the edge of the Sonoran desert, with guided creative sessions led by abstract artist Dr. Clarissa Castillo-Ramsey. Lodging, every meal and the airport shuttles are included. No art experience needed.",
    price="Shared room $1,675",
    note="Early rate through 30 November. $500 holds your room."),
  "gr": dict(
    tag="Waitlist", when="13&ndash;20 August 2027", where="Crete, Greece",
    name="Rise Into Her: The Greece Edition", href="/retreats/greece/",
    text="Eight days at Armonia Retreat Center in Crete, with daily movement, every meal and the excursions included. Every seat is taken; the waitlist is called in order.",
    price="Waitlist open", note=""),
}

QUOTES = {
  "kristi": ("The fact that you&rsquo;re even considering it should tell you that you should go.", "Kristi"),
  "bjb": ("I left being able to breathe, with old and new friends who cared about me.", "BJB"),
  "carol": ("Intimate group size, and leaders able to make us think, laugh and cry without judgement. No waiting, no rushing.", "Carol"),
  "melissa": ("I learned that I matter too.", "Melissa"),
  "kristi2": ("I was burnt out and struggling to figure out why I always felt behind. My need to be perfect and always reliable had become the reason I failed to show up for myself.", "Kristi"),
}

PLACES = [
  {
    "slug": "minnesota",
    "short": "From Minnesota",
    "label": "Women&rsquo;s retreats for Minnesota women",
    "title": "Women's Retreats for Minnesota Women | Cydnie Jocelyn",
    "description": "Women's retreats and wellness getaways hosted by Cydnie Jocelyn of Forest Lake, Minnesota: the Smoky Mountains in April, Arizona in May 2027.",
    "display": "A Minnesota winter is long. <em>Plan the thaw.</em>",
    "lede": "I&rsquo;m Cydnie Jocelyn, and I host small retreats for women from my home in Forest Lake. They take you out of Minnesota on purpose: the Smoky Mountains in April, the Arizona desert in May. Lodging, every meal and the plans are handled.",
    "img": ("home/retreat-walk-%s.webp", (600, 1000), 1000, 1500, "Cydnie walking arm in arm with two women along a garden path"),
    "cap": ("Hosted from", "Forest Lake, MN"),
    "why_label": "Why Minnesota women come",
    "why_h2": "You hold it together <em>all winter.</em>",
    "why_p": [
      "Minnesota women are very good at carrying things: the house, the job, the business, the people. Through a long winter, most of us stop noticing how much.",
      "The retreats are timed for the moment that weight shows. Spring comes to the Smokies and the desert weeks before it reaches the Twin Cities, and you come home with the season already turned.",
    ],
    "why_items": [
      ("A short flight away", "Both open retreats are a single trip from MSP: Knoxville for Gatlinburg, Phoenix for Arizona, with the Arizona shuttles included."),
      ("Hosted by a neighbor", "I live and work in Forest Lake. You can meet me before you book."),
      ("Nothing to organize", "Rooms, meals, movement and the plan for each day are handled. You pack and get on the plane."),
    ],
    "retreats": ["gat", "az"],
    "quotes": ["kristi", "bjb", "melissa"],
    "faq": [
      ("Are there women's retreats in Minnesota?",
       "My open retreats are in Tennessee and Arizona, on purpose: getting out of your usual place is half of what makes a retreat work. If you have a group and want a week in Minnesota, a private retreat can be built here."),
      ("How do I get there from the Twin Cities?",
       "For Gatlinburg you fly into Knoxville (TYS). For Arizona you fly into Phoenix Sky Harbor (PHX) and the airport shuttles are included. Airfare is not included in either retreat."),
      ("Can I meet you before I book?",
       "Yes. I am based in Forest Lake, north of Saint Paul. Ask through the contact page and we will find a time, in person or by phone."),
      ("Do I need to own a business to come?",
       "No. The retreats are for women who hold everything together, whatever that looks like for you."),
    ],
    "close_h2": "Your spring, <em>planned.</em>",
  },
  {
    "slug": "smoky-mountains",
    "short": "Tennessee",
    "label": "A women&rsquo;s retreat in the Smoky Mountains, Tennessee",
    "title": "Smoky Mountains Women's Retreat, Tennessee | Cydnie Jocelyn",
    "description": "A women's wellness retreat in Gatlinburg, Tennessee, 13 to 18 April 2027: a private house at the edge of the Great Smoky Mountains, meals included.",
    "display": "Five days at the edge of <em>the Smokies.</em>",
    "lede": "Wide Open is a small women&rsquo;s retreat in a private house in Gatlinburg, Tennessee, 13 to 18 April 2027. Daily movement, two workshops, two outings and every meal are included, and the mountains are right outside.",
    "img": ("gatlinburg/house-dusk-portrait-%s.webp", (600, 834), 834, 1112, "The private house in Gatlinburg lit up at dusk against the Smoky Mountains"),
    "cap": ("13&ndash;18 April 2027", "Gatlinburg, TN"),
    "why_label": "Why the Smokies",
    "why_h2": "Mountains that <em>slow you down.</em>",
    "why_p": [
      "The Great Smoky Mountains are the most visited national park in the country, and April is when they turn green: wildflowers on the lower trails, cool mornings, warm afternoons on the deck.",
      "The house sits at the edge of all of it. You can walk into the mountains or not move from the hot tub, and nobody needs anything from you either way.",
    ],
    "why_items": [
      ("Close to home for the Southeast", "Gatlinburg is about an hour from Knoxville&rsquo;s airport and within a few hours&rsquo; drive of Nashville, Atlanta, Asheville and Chattanooga."),
      ("A house, not a hotel", "One private house for the group: shared rooms or a private king suite, a deck facing the mountains and a hot tub."),
      ("Two hosts", "Kayla Freeman and I lead the week together: movement, two workshops and the two outings."),
    ],
    "retreats": ["gat"],
    "quotes": ["kristi", "carol", "bjb"],
    "faq": [
      ("When is the Smoky Mountains retreat?",
       "13 to 18 April 2027 in Gatlinburg, Tennessee. Five days in a private house at the edge of the Great Smoky Mountains."),
      ("What does it cost?",
       "A shared room is $1,490 and a private king suite $2,790 at the early rate through 31 October 2026, then $1,600 and $2,900. $500 holds your room."),
      ("Which airport do I fly into?",
       "Knoxville (TYS), about an hour from Gatlinburg. If you live in the Southeast, driving is often easier. Airfare is not included."),
      ("Is it a wellness retreat?",
       "Yes, in the plain sense: rest, daily movement, good food and quiet. It is not a spa week and there is no forced sharing."),
    ],
    "close_h2": "The mountains in April, <em>with room for you.</em>",
  },
  {
    "slug": "arizona",
    "short": "Arizona",
    "label": "A women&rsquo;s retreat in Arizona, near Phoenix",
    "title": "Women's Retreat in Arizona near Phoenix | Cydnie Jocelyn",
    "description": "A women's creative retreat in Peoria, Arizona, 5 to 9 May 2027, with abstract artist Clarissa Castillo-Ramsey. Meals and PHX shuttles included.",
    "display": "The desert, a paintbrush <em>and no rush.</em>",
    "lede": "Wild Canvas is a small creative retreat for women in Peoria, Arizona, northwest of Phoenix, 5 to 9 May 2027. Guided creative sessions, every meal, the house and the airport shuttles are included. No art experience needed.",
    "img": ("arizona/table-set-portrait-%s.webp", (600, 848), 848, 1130, "A long table set for dinner under a covered patio at dusk, small bonsai trees down the middle."),
    "cap": ("5&ndash;9 May 2027", "Peoria, AZ"),
    "why_label": "Why Arizona",
    "why_h2": "Warm days, cool evenings, <em>wide open sky.</em>",
    "why_p": [
      "Peoria sits in the West Valley, on the edge of the Sonoran desert, close enough to Phoenix that the flight is easy and far enough out that the evenings are quiet.",
      "May in the desert is warm and dry, and the light at dusk is the kind people come to paint. That is the point of this one: five days of making something with your hands, guided by an artist, with nothing else to manage.",
    ],
    "why_items": [
      ("Easy from anywhere", "Fly into Phoenix Sky Harbor (PHX) and the shuttles bring you to the house. Valley locals can simply drive over."),
      ("A creative retreat", "Guided sessions with abstract artist Dr. Clarissa Castillo-Ramsey. Every supply is provided and no experience is needed."),
      ("A house to play in", "A painted house with a long dinner table outside, a games room, mini golf and bowling, for the hours nobody has planned."),
    ],
    "retreats": ["az"],
    "quotes": ["kristi", "carol", "melissa"],
    "faq": [
      ("When is the Arizona retreat?",
       "5 to 9 May 2027 in Peoria, Arizona, northwest of Phoenix."),
      ("What does it cost?",
       "A shared room is $1,675 at the early rate through 30 November 2026, then $1,800. $500 holds your room, and the balance can be paid in five monthly payments."),
      ("Do I need to be artistic?",
       "No. The sessions are guided, every supply is there, and they are built for women who have not painted since school."),
      ("How do I get there?",
       "Fly into Phoenix Sky Harbor (PHX) and land by 3 pm on 5 May; the shuttles to and from the airport are included. Airfare is not."),
    ],
    "close_h2": "Five days in the desert, <em>made by hand.</em>",
  },
  {
    "slug": "wellness",
    "short": "Wellness retreats",
    "label": "Wellness retreats for women",
    "title": "Wellness Retreats for Women, 2027 | Cydnie Jocelyn",
    "description": "Small wellness retreats for women in 2027: the Smoky Mountains in April and Arizona in May. Rest, daily movement, every meal included, no forced sharing.",
    "display": "Rest is the whole <em>point of the week.</em>",
    "lede": "My retreats are wellness retreats in the plainest sense: you sleep, you move, you eat well and you are left alone when you want to be. A small group of women, a house, and a week where you are not the one holding it together.",
    "img": ("retreats/cr-floor-%s.webp", (600, 1000), 1000, 1613, "Women sitting together in a circle on the floor of an open-air pavilion in Costa Rica"),
    "cap": ("Two retreats", "Booking for 2027"),
    "why_label": "What wellness means here",
    "why_h2": "Not a spa. <em>Not a bootcamp.</em>",
    "why_p": [
      "A lot of wellness retreats sell a schedule: early yoga, a cleanse, a talk at every meal. Mine are built the other way round, around structured solitude inside a small group.",
      "There is daily movement and there are sessions, and every one of them is optional. Nobody asks you to share. If you spend the first two days catching up on sleep, that is the retreat working.",
    ],
    "why_items": [
      ("Everything handled", "Lodging, every meal and the plan for each day. You do not cook, book or organize anything."),
      ("Movement, your way", "Daily movement led for the group, and skipping it needs no explanation."),
      ("A small group", "Small enough that you know everyone by the second night. No forced sharing, ever."),
    ],
    "retreats": ["gat", "az", "gr"],
    "quotes": ["kristi2", "carol", "melissa"],
    "faq": [
      ("What is included in a wellness retreat?",
       "Lodging, every meal, daily movement and the sessions for the week. Each retreat page lists exactly what is and is not included; airfare and travel insurance never are."),
      ("Are the retreats for women only?",
       "Yes. Every open retreat is for women, and you do not need to own a business to come."),
      ("Do I have to take part in everything?",
       "No. Every session is optional, and there is no forced sharing. Rest is a perfectly good way to spend the week."),
      ("How do I hold a place?",
       "$500 holds your room on any open retreat, and the balance can be spread out. A place is held only once the deposit is received."),
    ],
    "close_h2": "A week where <em>you rest.</em>",
  },
  {
    "slug": "leadership",
    "short": "Leadership retreats",
    "label": "Women&rsquo;s leadership retreats, Minnesota and beyond",
    "title": "Women's Leadership Retreats, Minnesota | Cydnie Jocelyn",
    "description": "Private leadership retreats for women's teams, groups and communities: your dates, your location, built by Cydnie Jocelyn of Forest Lake, Minnesota.",
    "display": "Take your team away. <em>Bring them back clearer.</em>",
    "lede": "If you lead a team, a group or a community of women, I will build the retreat for you: your people, your dates, your location, in Minnesota or anywhere you want to go. The price depends on where and how long, so it starts with a conversation.",
    "img": ("cydnie-stand-%s.webp", (700, 1000, 1400), 1000, 1408, "Cydnie Jocelyn smiling with one hand on her hip, a white shirt over a white tee, beside an olive tree"),
    "cap": ("Private retreats", "By inquiry"),
    "why_label": "Why a leadership retreat",
    "why_h2": "The work you never get to <em>in the office.</em>",
    "why_p": [
      "Teams rarely lack ideas. They lack the room to think together without the next meeting pressing in. A few days away, with the logistics handled, gives them that room.",
      "I come to this from both sides. I host retreats, and my other work is brand and business strategy for founders and leaders, so I know what a team needs to bring home besides a good week.",
    ],
    "why_items": [
      ("Your group, your dates", "A private retreat is built around your people and your calendar, not fitted into someone else&rsquo;s."),
      ("Minnesota or away", "Stay close to the Twin Cities or travel. The location is part of what we decide together."),
      ("Work and rest, balanced", "Working sessions where you want them, real rest around them, and every meal and room handled."),
    ],
    "retreats": [],
    "quotes": ["carol", "bjb", "kristi"],
    "faq": [
      ("What is a private leadership retreat?",
       "A retreat built for your own group of women: a team, a leadership circle, a membership or a community. You bring the people; I build and host the week."),
      ("How much does a private retreat cost?",
       "It depends on the location and the length, so it is the one price I do not publish. Send an inquiry and you will have a proposal in writing."),
      ("Can the week include strategy sessions?",
       "It can. Brand and business strategy is the other half of my work, so working sessions can be built into the week if your group wants them."),
      ("Can it be in Minnesota?",
       "Yes. I am based in Forest Lake, north of Saint Paul, and a private retreat can be here or wherever your group wants to go."),
    ],
    "close_h2": "Let&rsquo;s plan your <em>team&rsquo;s week away.</em>",
  },
]


def url(p):
    return BASE + p["slug"] + "/"
