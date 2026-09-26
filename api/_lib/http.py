"""Request handling shared by every endpoint in api/.

Each function in api/ is a Vercel Python serverless function. The rules that
have to hold for all of them live here rather than in each one, because a
guard that is copied four times is a guard that is three quarters applied
the day somebody adds a fifth endpoint.
"""
import hashlib
import json
import os
import re
import secrets
from urllib.parse import urlparse

# The only origins allowed to post to this API. A form endpoint with no
# origin check can be submitted from anybody's page, which is how a quiet
# endpoint turns into someone else's spam relay. Browsers do not block a
# cross origin POST, they only block reading the reply, so this has to be
# checked on the server.
ALLOWED_HOSTS = {
    "cydniejocelyn.com",
    "www.cydniejocelyn.com",
    "localhost",
    "127.0.0.1",
}
# A Vercel preview is its own host (<deployment>.vercel.app). Vercel sets
# these two per deployment, so a preview accepts posts from itself and from
# nothing else; production does not need them. 26 September 2026.
for _name in ("VERCEL_URL", "VERCEL_BRANCH_URL"):
    if os.environ.get(_name):
        ALLOWED_HOSTS.add(os.environ[_name].split(":")[0].lower())

# A body larger than this is not a contact form.
MAX_BODY = 16 * 1024

# The field no human fills in. It is rendered, visually hidden, and left
# empty; a bot that fills every input gives itself away. A submission that
# trips it is answered with success and thrown away, because telling a bot
# it failed is how it learns to stop tripping.
HONEYPOT = "website"

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Rejected(Exception):
    """Raised with the status and the message the caller should be given."""

    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


def origin_ok(headers):
    """True if this request came from the site.

    Origin is present on cross origin posts and on same origin fetch. Referer
    is the fallback for a plain form post. A request with neither is refused:
    that is a script, not a browser, and this API has no non browser client.
    """
    for name in ("origin", "referer"):
        raw = headers.get(name)
        if not raw:
            continue
        host = urlparse(raw).hostname
        return host in ALLOWED_HOSTS
    return False


def client_ip(headers):
    """The visitor's address, as Vercel reports it.

    x-forwarded-for is a list and the LAST entry is the one the platform
    appended; the earlier ones are whatever the client claimed. Taking the
    first is the usual mistake and it lets anyone forge their address, which
    would defeat rate limiting entirely.
    """
    fwd = headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[-1].strip()
    return headers.get("x-real-ip") or ""


def hash_ip(ip):
    """sha256 of the address and IP_SALT, or None if there is no address.

    The raw value is never stored or logged. See the note in the migration.
    """
    if not ip:
        return None
    salt = os.environ.get("IP_SALT")
    if not salt:
        # Failing closed: a missing salt would otherwise produce an unsalted
        # hash, which is reversible for IPv4 by brute force in seconds.
        raise Rejected(500, "Server is not configured.")
    return hashlib.sha256(("%s%s" % (salt, ip)).encode("utf-8")).hexdigest()


def read_json(raw):
    if raw is None or len(raw) == 0:
        raise Rejected(400, "Empty request.")
    if len(raw) > MAX_BODY:
        raise Rejected(413, "That is too long to be a message.")
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        raise Rejected(400, "That was not valid JSON.")
    if not isinstance(data, dict):
        raise Rejected(400, "Expected an object.")
    return data


def field(data, name, required=False, max_len=2000):
    value = data.get(name)
    if value is None:
        value = ""
    if not isinstance(value, str):
        raise Rejected(400, "%s must be text." % name)
    value = value.strip()
    if required and not value:
        raise Rejected(400, "%s is required." % name)
    if len(value) > max_len:
        raise Rejected(400, "%s is too long." % name)
    return value or None


def email_field(data, name="email"):
    value = (field(data, name, required=True, max_len=320) or "").lower()
    if not EMAIL.match(value):
        raise Rejected(400, "That does not look like an email address.")
    return value


def token():
    return secrets.token_urlsafe(32)


def rate_limited(conn, ip_hash, limit=5, minutes=10):
    """True if this address has posted too often lately.

    Counts rows in `submissions` by ip_hash. The site role can read exactly
    two columns of that table, ip_hash and created_at, which is enough to
    count and not enough to read anybody's message. See db/grants.sql.
    """
    if not ip_hash:
        return False
    with conn.cursor() as cur:
        cur.execute(
            "select count(*) from submissions "
            "where ip_hash = %s and created_at > now() - make_interval(mins => %s)",
            (ip_hash, minutes))
        return cur.fetchone()[0] >= limit
