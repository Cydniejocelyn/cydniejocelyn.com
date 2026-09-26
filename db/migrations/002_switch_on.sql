-- cydniejocelyn.com, second migration. 26 September 2026.
--
-- Her word: "I want it pushed to neon for the database", and all four of
-- the options put to her: Letters sign-ups saved here AND sent to Flodesk,
-- the contact question saved here AND emailed to her, her own count of page
-- views and button clicks for visitors who accept cookies, and a read-only
-- inbox in Ops. HANDOFF section 78.
--
-- Same rules as 001: constraints live in the database, the raw IP is never
-- stored, and the site's own role can add rows and not read them back.


-- ---------------------------------------------------------------- delivery
-- Whether the side effect reached where it was going, recorded on the row
-- itself, so a sign-up that never reached Flodesk or a question that never
-- reached her inbox is visible in Ops instead of lost. 'not_configured'
-- means the key was not set in Vercel yet: the row is kept either way.
alter table subscribers add column if not exists flodesk_status text
  check (flodesk_status is null or flodesk_status in ('synced', 'failed', 'not_configured'));
alter table subscribers add column if not exists flodesk_checked_at timestamptz;

alter table submissions add column if not exists notified text
  check (notified is null or notified in ('sent', 'failed', 'not_configured'));


-- ---------------------------------------------------------------- page_events
-- Her own record of visits and clicks, written only after a visitor accepts
-- cookies (assets/js/analytics.js sends nothing before that). Deliberately
-- thin: which page, which button, what kind of screen, which site sent
-- them. No name, no email, no raw IP, no cookie id, nothing that follows a
-- person from one visit to the next.
create table if not exists page_events (
  id             bigint      generated always as identity primary key,
  kind           text        not null check (kind in ('view', 'click')),
  path           text        not null check (path ~ '^/' and length(path) <= 400),
  -- The data-cta name of the button, e.g. free-call-hero. A click that does
  -- not say which button is not a click on anything.
  cta            text        check (cta is null or (cta ~ '^[a-z0-9-]+$' and length(cta) <= 80)),
  constraint clicks_name_a_button check (kind <> 'click' or cta is not null),
  referrer_host  text        check (referrer_host is null or length(referrer_host) <= 200),
  device         text        check (device is null or device in ('phone', 'tablet', 'desktop')),
  -- Salted hash, for rate limiting only, exactly as on submissions. Enough
  -- to stop one address filling the table, not enough to identify anyone.
  ip_hash        text        check (ip_hash is null or ip_hash ~ '^[0-9a-f]{64}$'),
  created_at     timestamptz not null default now()
);

create index if not exists page_events_time_idx on page_events (created_at desc);
create index if not exists page_events_path_idx on page_events (path, created_at desc);
create index if not exists page_events_ip_window_idx on page_events (ip_hash, created_at desc);
