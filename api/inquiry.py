"""POST /api/inquiry  -  the contact form and "ask a question".

Replaces the HoneyBook contact form, cf_id 69fa372c. Nothing here sends
email yet; the row lands in `submissions` and is triaged from Ops.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import http as H
from _lib.handler import JsonPost


class handler(JsonPost):
    def act(self, data, conn, ip_hash):
        if H.rate_limited(conn, ip_hash):
            raise H.Rejected(429, "That is a lot of messages. Try again shortly.")

        email = H.email_field(data)
        name = H.field(data, "name", max_len=200)
        message = H.field(data, "message", required=True, max_len=5000)

        with conn.cursor() as cur:
            cur.execute(
                "insert into submissions "
                "(kind, email, name, message, source_path, referrer, ip_hash, user_agent) "
                "values ('inquiry', %s, %s, %s, %s, %s, %s, %s)",
                (email, name, message,
                 H.field(data, "source_path", max_len=400),
                 (self.headers.get("referer") or None),
                 ip_hash,
                 (self.headers.get("user-agent") or None)[:500] if self.headers.get("user-agent") else None))
        return {"ok": True, "message": "Thank you. I answer these myself."}
