"""POST /api/interest  -  retreat interest and waitlist.

`retreat` is required and the database refuses a row without it: interest in
no particular retreat is not interest in anything.
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
        retreat = H.field(data, "retreat", required=True, max_len=120)

        with conn.cursor() as cur:
            cur.execute(
                "insert into submissions "
                "(kind, email, name, message, subject, source_path, referrer, ip_hash, user_agent) "
                "values ('retreat_interest', %s, %s, %s, %s, %s, %s, %s, %s)",
                (email,
                 H.field(data, "name", max_len=200),
                 H.field(data, "message", max_len=2000),
                 retreat,
                 H.field(data, "source_path", max_len=400),
                 (self.headers.get("referer") or None),
                 ip_hash,
                 (self.headers.get("user-agent") or None)[:500] if self.headers.get("user-agent") else None))
        return {"ok": True, "message": "You are on the list. You will hear first."}
