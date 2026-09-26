-- The role the website actually runs as.
--
-- WHY THIS EXISTS. api/ is reachable by anyone on the internet. If the
-- credential it holds were the database owner, then one mistake in a handler,
-- one leaked environment variable, one misconfigured preview deployment, and
-- whoever found it could read every message anyone has ever sent her and the
-- entire mailing list. Owner rights on a public endpoint buy nothing: the site
-- has no feature that needs to read submissions back.
--
-- So the grants below are the smallest set that lets the site do its job:
--
--   submissions   INSERT only. Plus SELECT on exactly two columns, ip_hash
--                 and created_at, because rate limiting has to count recent
--                 rows from one address. It cannot read a name, an email or
--                 a message. Column level SELECT is doing real work here.
--   subscribers   INSERT, and SELECT on the columns needed to recognise a
--                 duplicate signup and to look a token up. UPDATE is limited
--                 to the three columns that confirming and unsubscribing
--                 touch, so the endpoint cannot rewrite an address or forge
--                 a consent record.
--
-- Run against both branches. Idempotent.

-- THE ROLE ITSELF IS CREATED BY db/setup_role.py, NOT HERE, and its password
-- is never in this file. This file is committed; a password in it would be
-- in git history forever. Everything below is safe to read.

-- No inherited rights from PUBLIC, and no ability to create anything.
revoke all on schema public from site_api;
grant usage on schema public to site_api;
revoke create on schema public from site_api;

revoke all on submissions from site_api;
grant insert on submissions to site_api;
grant select (ip_hash, created_at) on submissions to site_api;

revoke all on subscribers from site_api;
grant insert on subscribers to site_api;
grant select (id, email, status, confirm_token, unsubscribe_token) on subscribers to site_api;
grant update (status, consent_at, unsubscribed_at, flodesk_status, flodesk_checked_at) on subscribers to site_api;

-- page_events (002, 26 September 2026): INSERT, plus the same two columns
-- for rate limiting that submissions allows. It cannot read which pages
-- anyone visited back out.
revoke all on page_events from site_api;
grant insert on page_events to site_api;
grant select (ip_hash, created_at) on page_events to site_api;

-- schema_migrations is none of its business.
revoke all on schema_migrations from site_api;
