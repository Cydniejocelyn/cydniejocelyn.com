-- The role Cydnie Ops reads the website inbox as. 26 September 2026.
--
-- READ ONLY, AND ONLY THESE THREE TABLES. Ops is local on her machine and
-- holds the client book in its own, separate database; this role lets it
-- show the website's sign-ups, questions and page views without the site
-- ever being able to read Ops, and without Ops being able to change what
-- the site recorded. Marking a question handled can be added later as a
-- column-level UPDATE on submissions (status, actioned_at) if she wants it.
--
-- The role and its password are created by db/setup_role.py, never here.

revoke all on schema public from ops_reader;
grant usage on schema public to ops_reader;
revoke create on schema public from ops_reader;

revoke all on submissions, subscribers, page_events from ops_reader;
grant select on submissions, subscribers, page_events to ops_reader;
revoke all on schema_migrations from ops_reader;
