"""POST /api/inquiry  -  the contact form and "ask a question".

Replaces the HoneyBook contact form, cf_id 69fa372c (her word, 26 September
2026). Each question is emailed to her through Resend and saved in
`submissions`, which Ops shows as the Website inbox. The email is sent
first and its outcome written on the row; the row is kept either way.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import http as H
from _lib.handler import JsonPost
from _lib.outbound import notify_question


class handler(JsonPost):
    def act(self, data, conn, ip_hash):
        if H.rate_limited(conn, ip_hash):
            raise H.Rejected(429, "That is a lot of messages. Try again shortly.")

        email = H.email_field(data)
        name = H.field(data, "name", max_len=200)
        message = H.field(data, "message", required=True, max_len=5000)
        source_path = H.field(data, "source_path", max_len=400)
        notified = notify_question(email, name, message, source_path)

        with conn.cursor() as cur:
            cur.execute(
                "insert into submissions "
                "(kind, email, name, message, source_path, referrer, ip_hash, user_agent, notified) "
                "values ('inquiry', %s, %s, %s, %s, %s, %s, %s, %s)",
                (email, name, message,
                 source_path,
                 (self.headers.get("referer") or None),
                 ip_hash,
                 (self.headers.get("user-agent") or None)[:500] if self.headers.get("user-agent") else None,
                 notified))
        return {"ok": True, "message": "Thank you. It is with me now, and I answer these myself, usually within a day."}
