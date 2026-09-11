"""POST /api/subscribe  -  The Letters.

Replaces the Flodesk form on /the-letters/.

SINGLE OPT IN, DELIBERATELY, FOR NOW. The row is written straight to
`confirmed` with consent_at set, because the form itself is the act of
consent and nothing on this site can send a confirmation email yet. The
column that double opt in needs, confirm_token, already exists and is
written on every row, so switching later is a change to this one branch
plus whatever sends the mail. It is not a migration against live rows.

Every row records what consent was given to and from where, which is the
thing that matters if she is ever asked to evidence it.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import http as H
from _lib.handler import JsonPost


class handler(JsonPost):
    def act(self, data, conn, ip_hash):
        email = H.email_field(data)
        name = H.field(data, "name", max_len=200)
        source = H.field(data, "source_path", max_len=400) or "/the-letters/"

        with conn.cursor() as cur:
            # A second signup from the same address is not an error and must
            # not be reported as one: it is usually somebody who forgot, and
            # sometimes somebody who unsubscribed and changed their mind.
            # Re-subscribing clears the unsubscribe date and records fresh
            # consent. The unsubscribe token is left alone so old links in
            # old emails keep working.
            cur.execute(
                """insert into subscribers
                     (email, name, status, confirm_token, unsubscribe_token,
                      consent_at, consent_source, consent_ip_hash)
                   values (%s, %s, 'confirmed', %s, %s, now(), %s, %s)
                   on conflict (email) do update
                     set status = 'confirmed',
                         consent_at = now(),
                         unsubscribed_at = null
                   """,
                (email, name, H.token(), H.token(), source, ip_hash))

        # THE ANSWER IS THE SAME WHETHER SHE WAS ALREADY ON THE LIST OR NOT,
        # and that is on purpose twice over.
        #
        # It closes an enumeration oracle. A form that says "you were already
        # on the list" will tell anybody who asks whether a given address is
        # subscribed, one address at a time, for as long as they care to.
        #
        # And the first version of this could not have told the difference
        # anyway: it used `returning (xmax = 0)`, which reads the system
        # column xmax, which a column level grant does not cover, so Postgres
        # refused the whole statement. The restriction caught a query that was
        # reaching past what this endpoint is allowed to know. That is the
        # grants working, not a problem with them.
        return {"ok": True, "message": "You are on the list."}
