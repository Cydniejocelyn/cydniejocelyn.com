#!/usr/bin/env python3
"""Prove the constraints and the grants, against the `check` branch only.

    .venv/bin/python db/check.py

Most of these are writes that MUST be refused. That is the half that
silently stops mattering the day somebody drops a constraint to make an
insert work, and it is the reason this suite is worth its length.

It wipes and rebuilds the check branch from db/migrations every run, so it
never touches real submissions.
"""
import pathlib, sys, traceback

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api"))
from _lib.db import connect  # noqa: E402

PASS, FAIL = [], []


def ok(label, condition):
    (PASS if condition else FAIL).append(label)
    print("%s  %s" % ("pass" if condition else "FAIL", label))


def refused(conn, label, sql, params=()):
    """The write must be rejected. A rejection is the pass."""
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.rollback()
        ok("refused: " + label, False)
    except Exception:
        conn.rollback()
        ok("refused: " + label, True)


def accepted(conn, label, sql, params=()):
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()
        ok("accepted: " + label, True)
    except Exception as e:
        conn.rollback()
        ok("accepted: " + label + "  [" + str(e).splitlines()[0][:70] + "]", False)


def main():
    # ---- rebuild ---------------------------------------------------------
    with connect("CHECK_DATABASE_URL") as conn:
        with conn.cursor() as cur:
            cur.execute("drop schema public cascade; create schema public;")
            cur.execute("grant usage on schema public to site_api;")
        conn.commit()
    import subprocess
    subprocess.run([sys.executable, str(ROOT / "db" / "migrate.py"), "--check"],
                   check=True, capture_output=True)
    subprocess.run([sys.executable, str(ROOT / "db" / "setup_role.py")],
                   check=True, capture_output=True)
    print("check branch rebuilt from db/migrations\n")

    owner = connect("CHECK_DATABASE_URL")
    site = connect("SITE_CHECK_DATABASE_URL")

    # ---- shape -----------------------------------------------------------
    print("Shape")
    with owner.cursor() as cur:
        cur.execute("select table_name from information_schema.tables "
                    "where table_schema='public' order by 1")
        tables = [r[0] for r in cur.fetchall()]
    ok("the three tables exist", tables == ["schema_migrations", "submissions", "subscribers"])

    # ---- submissions constraints ----------------------------------------
    print("\nSubmissions")
    accepted(owner, "a plain inquiry",
             "insert into submissions (kind,email,message) values ('inquiry','a@b.co','hi')")
    refused(owner, "an email with an uppercase letter",
            "insert into submissions (kind,email) values ('inquiry','A@b.co')")
    refused(owner, "an email with no domain",
            "insert into submissions (kind,email) values ('inquiry','nope')")
    refused(owner, "a kind that is not one of the two",
            "insert into submissions (kind,email) values ('newsletter','a@b.co')")
    refused(owner, "retreat interest that does not name a retreat",
            "insert into submissions (kind,email) values ('retreat_interest','a@b.co')")
    accepted(owner, "retreat interest that names one",
             "insert into submissions (kind,email,subject) values "
             "('retreat_interest','a@b.co','Gatlinburg')")
    refused(owner, "a status outside the four",
            "insert into submissions (kind,email,status) values ('inquiry','a@b.co','urgent')")
    refused(owner, "actioned with no actioned_at",
            "insert into submissions (kind,email,status) values ('inquiry','a@b.co','actioned')")
    accepted(owner, "actioned with a date",
             "insert into submissions (kind,email,status,actioned_at) values "
             "('inquiry','a@b.co','actioned',now())")
    refused(owner, "an ip_hash that is not a sha256",
            "insert into submissions (kind,email,ip_hash) values ('inquiry','a@b.co','abc')")
    accepted(owner, "a real sha256 ip_hash",
             "insert into submissions (kind,email,ip_hash) values ('inquiry','a@b.co',%s)",
             ("a" * 64,))

    # ---- subscribers constraints ----------------------------------------
    print("\nSubscribers")
    accepted(owner, "a pending subscriber",
             "insert into subscribers (email,unsubscribe_token) values ('p@b.co','t1')")
    refused(owner, "a second row with the same address",
            "insert into subscribers (email,unsubscribe_token) values ('p@b.co','t2')")
    refused(owner, "confirmed with no consent date",
            "insert into subscribers (email,unsubscribe_token,status) values "
            "('c@b.co','t3','confirmed')")
    accepted(owner, "confirmed with one",
             "insert into subscribers (email,unsubscribe_token,status,consent_at) values "
             "('c@b.co','t4','confirmed',now())")
    refused(owner, "unsubscribed with no date",
            "insert into subscribers (email,unsubscribe_token,status) values "
            "('u@b.co','t5','unsubscribed')")
    refused(owner, "a subscriber with no unsubscribe token",
            "insert into subscribers (email) values ('n@b.co')")

    with owner.cursor() as cur:
        cur.execute("select updated_at from subscribers where email='p@b.co'")
        before = cur.fetchone()[0]
        cur.execute("update subscribers set name='Renamed' where email='p@b.co'")
        owner.commit()
        cur.execute("select updated_at from subscribers where email='p@b.co'")
        after = cur.fetchone()[0]
    ok("accepted: updated_at moves on its own", after > before)

    # ---- the grants, which are the point --------------------------------
    print("\nWhat the website may and may not do")
    accepted(site, "the site can file a submission",
             "insert into submissions (kind,email,message) values "
             "('inquiry','site@b.co','from the site')")
    refused(site, "the site cannot read a message back",
            "select message from submissions limit 1")
    refused(site, "the site cannot read an email address back",
            "select email from submissions limit 1")
    accepted(site, "the site can count by ip_hash, for rate limiting",
             "select count(*) from submissions where ip_hash is null")
    refused(site, "the site cannot update a submission",
            "update submissions set status='spam' where true")
    refused(site, "the site cannot delete a submission",
            "delete from submissions where true")
    accepted(site, "the site can add a subscriber",
             "insert into subscribers (email,unsubscribe_token,status,consent_at) "
             "values ('new@b.co','t9','confirmed',now())")
    refused(site, "the site cannot rewrite a subscriber's address",
            "update subscribers set email='x@b.co' where email='new@b.co'")
    accepted(site, "the site can unsubscribe somebody",
             "update subscribers set status='unsubscribed', unsubscribed_at=now() "
             "where email='new@b.co'")
    refused(site, "the site cannot read the migration history",
            "select * from schema_migrations")
    refused(site, "the site cannot create a table",
            "create table sneaky (id int)")

    owner.close(); site.close()

    print("\n%d pass / %d fail" % (len(PASS), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(1)
