"""The two places the site talks to on someone's behalf. 26 September 2026.

    flodesk_subscribe(email, name)   add a Letters sign-up to her Flodesk list
    notify_question(...)             email her when a question comes in

Both return one of 'synced'/'sent', 'failed' or 'not_configured', which the
endpoint writes onto the row, so Ops shows anything that did not arrive.
Neither ever raises: a Flodesk or email outage must not lose the row, and the
row is what she was promised. Both use the standard library only.

THE KEYS ARE HERS AND LIVE ONLY IN VERCEL'S ENVIRONMENT VARIABLES:

    FLODESK_API_KEY       Flodesk > Account settings > Integrations > API
    FLODESK_SEGMENT_ID    optional: the segment the Letters list lives in
    RESEND_API_KEY        resend.com > API Keys
    RESEND_FROM           optional, default "Cydnie Jocelyn website
                          <onboarding@resend.dev>" (that address only delivers
                          to the Resend account's own email until the domain
                          is verified in Resend)
    NOTIFY_TO             optional, default hello@cydniejocelyn.com
"""
import base64, json, os, urllib.request

TIMEOUT = 6


def _post(url, body, headers):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers=dict({"Content-Type": "application/json",
                                               "User-Agent": "cydniejocelyn.com"}, **headers))
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return 200 <= r.status < 300


def flodesk_subscribe(email, name=None):
    key = os.environ.get("FLODESK_API_KEY")
    if not key:
        return "not_configured"
    body = {"email": email, "double_optin": False}
    if name:
        body["first_name"] = name.split()[0][:100]
    seg = os.environ.get("FLODESK_SEGMENT_ID")
    if seg:
        body["segment_ids"] = [s.strip() for s in seg.split(",") if s.strip()]
    auth = base64.b64encode((key + ":").encode()).decode()
    try:
        return "synced" if _post("https://api.flodesk.com/v1/subscribers", body,
                                 {"Authorization": "Basic " + auth}) else "failed"
    except Exception:
        import traceback; traceback.print_exc()
        return "failed"


def notify_question(email, name, message, source_path=None):
    key = os.environ.get("RESEND_API_KEY")
    if not key:
        return "not_configured"
    who = name or email
    text = ("A new question from the website.\n\n"
            "From: %s <%s>\nPage: %s\n\n%s\n\n"
            "Reply to this email to answer them directly. It is also saved in "
            "the Website inbox in Ops." % (name or "(no name)", email, source_path or "-", message))
    body = {
        "from": os.environ.get("RESEND_FROM") or "Cydnie Jocelyn website <onboarding@resend.dev>",
        "to": [os.environ.get("NOTIFY_TO") or "hello@cydniejocelyn.com"],
        "reply_to": email,
        "subject": "New question from %s" % who[:80],
        "text": text,
    }
    try:
        return "sent" if _post("https://api.resend.com/emails", body,
                               {"Authorization": "Bearer " + key}) else "failed"
    except Exception:
        import traceback; traceback.print_exc()
        return "failed"
