"""GET /api/unsubscribe?token=...  -  leaving The Letters.

A GET reached by clicking a link in an email, so there is no origin to check
and there must not be one: the click arrives from a mail client, not from the
site. The token is the authorisation and it is the only thing that is.

It returns a small HTML page rather than JSON, because a person is looking at
it. Unknown and already used tokens get the same answer as a good one, which
is both kinder and stops the endpoint being used to test whether an address
is on the list.
"""
import sys, pathlib
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _lib.db import connect  # noqa: E402

PAGE = """<!doctype html><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Unsubscribed</title>
<style>
  body{margin:0;min-height:100vh;display:grid;place-items:center;
       background:#071A1F;color:#E7ECE8;
       font:400 1rem/1.6 "Instrument Sans",-apple-system,Segoe UI,Helvetica,sans-serif}
  main{max-width:30rem;padding:2rem;text-align:center}
  h1{font-family:"Instrument Serif",Georgia,serif;font-weight:400;font-size:1.8rem;margin:0 0 1rem}
  a{color:#9FCCC6}
</style>
<main>
  <h1>You are unsubscribed.</h1>
  <p>You will not get The Letters again. Nothing else changes, and you are
     welcome back whenever you want.</p>
  <p><a href="https://cydniejocelyn.com/">cydniejocelyn.com</a></p>
</main>"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        token = (parse_qs(urlparse(self.path).query).get("token") or [""])[0]
        try:
            if token:
                with connect("SITE_DATABASE_URL") as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            "update subscribers set status = 'unsubscribed', "
                            "unsubscribed_at = now() where unsubscribe_token = %s",
                            (token,))
                    conn.commit()
        except Exception:
            import traceback
            traceback.print_exc()

        body = PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        # This page is reached from email and must never be framed.
        self.send_header("X-Frame-Options", "DENY")
        self.end_headers()
        self.wfile.write(body)
