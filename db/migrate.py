#!/usr/bin/env python3
"""Apply every migration in db/migrations that has not been applied yet.

    .venv/bin/python db/migrate.py            against DATABASE_URL
    .venv/bin/python db/migrate.py --check    against CHECK_DATABASE_URL

Migrations are numbered and applied in filename order, once each, inside a
transaction. A file that has already been recorded is skipped, so this is
safe to run again and safe to run against a database that is already current.

THE DOOR CLOSES THE DAY THE FIRST REAL SUBMISSION ARRIVES. Until then,
editing 001_init.sql and rebuilding is free. After it, every schema change is
a new numbered file, because the rows cannot be recreated from anything.
"""
import sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MIGRATIONS = ROOT / "db" / "migrations"

# The connection helper lives with the functions that use it most, and is
# imported here by path rather than copied. See the note at the top of it.
sys.path.insert(0, str(ROOT / "api"))
from _lib.db import connect  # noqa: E402


def main():
    check = "--check" in sys.argv
    print("migrating the %s branch" % ("check" if check else "main"))

    with connect("CHECK_DATABASE_URL" if check else "DATABASE_URL") as conn:
        with conn.cursor() as cur:
            cur.execute("""create table if not exists schema_migrations (
                             version text primary key,
                             applied_at timestamptz not null default now())""")
            conn.commit()
            cur.execute("select version from schema_migrations")
            done = {r[0] for r in cur.fetchall()}

        for path in sorted(MIGRATIONS.glob("*.sql")):
            version = path.stem
            if version in done:
                print("  skip    %s" % version)
                continue
            # One transaction per migration, so a failure leaves the database
            # on the last version that fully applied rather than half way
            # through this one.
            with conn.cursor() as cur:
                cur.execute(path.read_text(encoding="utf-8"))
                cur.execute("insert into schema_migrations (version) values (%s)", (version,))
            conn.commit()
            print("  applied %s" % version)

    print("done")


if __name__ == "__main__":
    main()
