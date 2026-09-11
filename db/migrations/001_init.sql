-- cydniejocelyn.com, first migration.
--
-- This database backs the PUBLIC website. It is deliberately not the Cydnie
-- Ops database: an endpoint on the open internet must not hold a credential
-- that can read the client book. Two tables, and both of them are an inbox
-- rather than a system of record. The system of record is Ops.
--
-- Conventions carried over from Ops on purpose:
--   * constraints are CHECKs in the database, not rules in the application
--   * money and dates are not stored here at all, so neither type trap applies
--   * no em dashes, anywhere

create table if not exists schema_migrations (
  version     text        primary key,
  applied_at  timestamptz not null default now()
);


-- ---------------------------------------------------------------- submissions
-- Everything the site captures that is not a newsletter signup: the contact
-- form and retreat interest. One table with a kind column rather than one
-- table per form, because they share every field that matters and the only
-- thing that differs is what "subject" means.
--
-- THE SITE NEVER READS THIS TABLE. The api role is granted INSERT and a
-- column level SELECT on two columns for rate limiting, and nothing else.
-- See db/grants.sql. That is what stops a leaked deploy key from dumping
-- every message anyone has ever sent her.
create table if not exists submissions (
  id           bigint      generated always as identity primary key,

  kind         text        not null
               check (kind in ('inquiry', 'retreat_interest')),

  -- Stored lowercase and enforced, not merely normalised on the way in, so a
  -- second writer cannot introduce a duplicate that differs only in case.
  email        text        not null
               check (email = lower(email))
               check (email ~ '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$'),
  name         text,
  message      text,

  -- Which retreat, which offer, whatever the form was about. A retreat
  -- interest row that does not say which retreat is not interest in
  -- anything, so the database refuses it. Same shape as the Ops rule that an
  -- expense tagged retreat_direct has to name its retreat.
  subject      text,
  constraint retreat_interest_names_a_retreat
              check (kind <> 'retreat_interest' or subject is not null),

  -- Anything the form carried that does not deserve a column yet.
  payload      jsonb       not null default '{}'::jsonb,

  source_path  text,
  referrer     text,

  -- THE RAW IP IS NEVER STORED. sha256 of the address and IP_SALT. The site
  -- publishes a privacy policy and loads no analytics at all before consent,
  -- so keeping a plain IP next to an email address would contradict the
  -- thing the rest of the site is careful about. The hash is enough to rate
  -- limit and not enough to identify.
  ip_hash      text        check (ip_hash is null or ip_hash ~ '^[0-9a-f]{64}$'),
  user_agent   text,

  status       text        not null default 'new'
               check (status in ('new', 'read', 'actioned', 'spam')),
  created_at   timestamptz not null default now(),
  actioned_at  timestamptz,
  constraint actioned_rows_say_when
              check (status <> 'actioned' or actioned_at is not null)
);

create index if not exists submissions_triage_idx
  on submissions (status, created_at desc);
-- Rate limiting reads this and nothing else.
create index if not exists submissions_ip_window_idx
  on submissions (ip_hash, created_at desc);


-- ---------------------------------------------------------------- subscribers
-- The Letters. Separate from submissions because a mailing list has a
-- lifecycle that a contact form does not: consent has to be evidenced, and
-- unsubscribing has to work forever and without a login.
create table if not exists subscribers (
  id                bigint      generated always as identity primary key,

  email             text        not null unique
                    check (email = lower(email))
                    check (email ~ '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$'),
  name              text,

  status            text        not null default 'pending'
                    check (status in ('pending', 'confirmed', 'unsubscribed', 'bounced')),

  -- Double opt in is not switched on yet, because nothing sends email yet.
  -- The column exists so that turning it on later is a change of one branch
  -- in api/subscribe.py and not a migration against live rows.
  confirm_token     text        unique,

  -- Required and permanent. An unsubscribe link that depends on a session or
  -- an account is not an unsubscribe link.
  unsubscribe_token text        not null unique,

  -- The evidence, which is the whole reason this table is not just a list of
  -- addresses. If she is ever asked to show that a given person opted in,
  -- this is the answer.
  consent_at        timestamptz,
  consent_source    text,
  consent_ip_hash   text        check (consent_ip_hash is null or consent_ip_hash ~ '^[0-9a-f]{64}$'),

  created_at        timestamptz not null default now(),
  updated_at        timestamptz not null default now(),
  unsubscribed_at   timestamptz,

  -- A confirmed subscriber with no consent timestamp is a claim with no
  -- evidence behind it, and an unsubscribed one with no date cannot be
  -- proved to have been honoured. Both are refused.
  constraint confirmed_rows_have_consent
             check (status <> 'confirmed' or consent_at is not null),
  constraint unsubscribed_rows_say_when
             check (status <> 'unsubscribed' or unsubscribed_at is not null)
);

create index if not exists subscribers_status_idx on subscribers (status);


-- updated_at maintained by the database, so it cannot be forgotten by a
-- caller and cannot be back dated by one either.
create or replace function touch_updated_at() returns trigger
language plpgsql as $$
begin
  new.updated_at := now();
  return new;
end $$;

drop trigger if exists subscribers_touch on subscribers;
create trigger subscribers_touch before update on subscribers
  for each row execute function touch_updated_at();
