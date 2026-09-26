"""POST /api/event  -  her own count of page views and button clicks.

26 September 2026, her word. Sent by assets/js/analytics.js ONLY after a
visitor accepts cookies, the same gate as Google Analytics, and described in
the privacy policy. Deliberately thin: page, button, kind of screen, which
site sent them. No name, email, raw IP or anything that links one visit to
the next. The salted ip_hash is for rate limiting and nothing else.
"""
import re, sys, pathlib
from urllib.parse import urlparse
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib import http as H
from _lib.handler import JsonPost

CTA = re.compile(r"^[a-z0-9-]{1,80}$")


class handler(JsonPost):
    def act(self, data, conn, ip_hash):
        kind = (data.get("kind") or "").strip()
        if kind not in ("view", "click"):
            raise H.Rejected(400, "Unknown event.")
        path = (data.get("path") or "/").strip()[:400]
        if not path.startswith("/"):
            raise H.Rejected(400, "Bad path.")
        cta = (data.get("cta") or "").strip().lower() or None
        if cta and not CTA.match(cta):
            cta = None
        if kind == "click" and not cta:
            raise H.Rejected(400, "A click has to name its button.")
        device = data.get("device") if data.get("device") in ("phone", "tablet", "desktop") else None
        ref = None
        try:
            host = urlparse(data.get("referrer") or "").hostname
            if host and not host.endswith("cydniejocelyn.com"):
                ref = host[:200]
        except Exception:
            pass

        if ip_hash:
            with conn.cursor() as cur:
                cur.execute("select count(*) from page_events where ip_hash = %s "
                            "and created_at > now() - interval '10 minutes'", (ip_hash,))
                if cur.fetchone()[0] >= 120:
                    return {"ok": True}      # quietly dropped, never an error
        with conn.cursor() as cur:
            cur.execute("insert into page_events (kind, path, cta, referrer_host, device, ip_hash) "
                        "values (%s, %s, %s, %s, %s, %s)", (kind, path, cta, ref, device, ip_hash))
        return {"ok": True}
