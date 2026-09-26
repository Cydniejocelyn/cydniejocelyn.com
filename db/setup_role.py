#!/usr/bin/env python3
"""Create the restricted `site_api` role, apply db/grants.sql, and record the
connection strings in .env.local.

    .venv/bin/python db/setup_role.py            reuse the existing password
    .venv/bin/python db/setup_role.py --rotate   issue a new one

REUSING IS THE DEFAULT, AND THAT IS NOT LAZINESS. db/check.py drops and
rebuilds the check schema, which destroys the grants, so it has to run this
every time. An earlier version generated a fresh password on every call, so
running the suite silently invalidated the credentials sitting in .env.local
and in Vercel. Rotation is a thing you ask for.

Run it after any migration that adds a table: a new table is not covered by
grants already applied, and the role would see either nothing or, worse,
whatever PUBLIC was given.
"""
import pathlib, re, secrets, sys, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "api"))
from _lib.db import connect, _load_env_local  # noqa: E402
from psycopg import sql  # noqa: E402

ROLE = "site_api"
OPS_ROLE = "ops_reader"
ENV = ROOT / ".env.local"


def existing_password(key="SITE_DATABASE_URL"):
    """The password already in .env.local for `key`, or None."""
    if not ENV.exists():
        return None
    for line in ENV.read_text(encoding="utf-8").splitlines():
        if line.startswith(key + "="):
            netloc = urllib.parse.urlsplit(line.split("=", 1)[1]).netloc
            if ":" in netloc and "@" in netloc:
                return urllib.parse.unquote(netloc.split(":", 1)[1].split("@", 1)[0])
    return None


def apply(env_name, label, password, role=ROLE, grants_file="grants.sql"):
    grants = (ROOT / "db" / grants_file).read_text(encoding="utf-8")
    with connect(env_name) as conn:
        with conn.cursor() as cur:
            cur.execute("select 1 from pg_roles where rolname = %s", (role,))
            exists = cur.fetchone() is not None
            # Composed with Identifier and Literal rather than string
            # formatting. This is the one statement in the project that
            # carries a password and it is not going to be the one that
            # concatenates it into SQL.
            cur.execute(sql.SQL("{} {} LOGIN PASSWORD {}").format(
                sql.SQL("ALTER ROLE" if exists else "CREATE ROLE"),
                sql.Identifier(role),
                sql.Literal(password)))
            cur.execute(grants)
        conn.commit()
    return exists


def url_for(env_name, password, role=ROLE):
    import os
    _load_env_local()
    parts = urllib.parse.urlsplit(os.environ[env_name])
    netloc = "%s:%s@%s" % (role, urllib.parse.quote(password, safe=""), parts.hostname)
    return urllib.parse.urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))


def write_env(pairs):
    text = ENV.read_text(encoding="utf-8")
    for key, value in pairs:
        line = "%s=%s" % (key, value)
        if re.search(r"^%s=" % key, text, re.M):
            text = re.sub(r"^%s=.*$" % key, line.replace("\\", "\\\\"), text, flags=re.M)
        else:
            text = text.rstrip() + "\n" + line + "\n"
    ENV.write_text(text, encoding="utf-8")


def main():
    rotate = "--rotate" in sys.argv
    password = None if rotate else existing_password()
    if password is None:
        password = secrets.token_urlsafe(32)
        why = "rotated" if rotate else "issued"
    else:
        why = "reused"

    for env_name, label in (("DATABASE_URL", "main"), ("CHECK_DATABASE_URL", "check")):
        existed = apply(env_name, label, password)
        print("  %-6s role %s, grants applied" % (label, "updated" if existed else "created"))

    write_env([("SITE_DATABASE_URL", url_for("DATABASE_URL", password)),
               ("SITE_CHECK_DATABASE_URL", url_for("CHECK_DATABASE_URL", password))])
    print("  password %s, .env.local updated" % why)

    # OPS_READER (26 September 2026): the read-only role Cydnie Ops uses for
    # the website inbox. Its own password, reused the same way; --rotate
    # rotates both. See db/ops_grants.sql.
    ops_pw = None if rotate else existing_password("SITE_OPS_READ_URL")
    ops_why = "reused" if ops_pw else ("rotated" if rotate else "issued")
    ops_pw = ops_pw or secrets.token_urlsafe(32)
    for env_name, label in (("DATABASE_URL", "main"), ("CHECK_DATABASE_URL", "check")):
        existed = apply(env_name, label, ops_pw, role=OPS_ROLE, grants_file="ops_grants.sql")
        print("  %-6s role %s %s, grants applied" % (label, OPS_ROLE, "updated" if existed else "created"))
    write_env([("SITE_OPS_READ_URL", url_for("DATABASE_URL", ops_pw, role=OPS_ROLE)),
               ("SITE_OPS_READ_CHECK_URL", url_for("CHECK_DATABASE_URL", ops_pw, role=OPS_ROLE))])
    print("  ops_reader password %s, .env.local updated" % ops_why)


if __name__ == "__main__":
    main()
