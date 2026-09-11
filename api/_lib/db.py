"""The one place that knows how to open a connection to this database.

Imported by the Vercel functions in api/ and, by path, by db/migrate.py and
db/check.py. There is deliberately not a second copy: connection handling
that exists twice drifts, and the half that drifts is the half that quietly
stops verifying the certificate.
"""
import os
import pathlib
import ssl  # noqa: F401  (documents the intent; libpq does the real work)

import psycopg

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent


def _load_env_local():
    """Read .env.local into os.environ if it is there and the vars are not.

    Only used locally. On Vercel the environment is already populated and
    this file does not exist, which is why a missing file is not an error.
    """
    path = ROOT / ".env.local"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def ca_bundle():
    """Where verify-full should look for trust roots.

    certifi if it is installed, otherwise the string "system", which tells
    libpq to use the platform store. That order is not arbitrary and it is
    not a preference:

        macOS, this machine   sslrootcert=system  FAILS. OpenSSL does not
                              read the Keychain, so the store is empty and
                              every connection dies on "certificate verify
                              failed". Both were tried.
        Vercel, Linux         system is correct and needs no dependency.

    certifi is in requirements.txt so the first branch is the one that runs
    in both places, and the fallback is there for an environment that has
    libpq but not certifi. The failure this avoids is somebody hitting the
    macOS error and "fixing" it by dropping sslmode to require, which
    connects happily and verifies nothing at all.
    """
    try:
        import certifi
        return certifi.where()
    except ImportError:
        return "system"


def connect(url_env="DATABASE_URL", **kw):
    """Open a connection. Caller is responsible for closing it, or use `with`."""
    _load_env_local()
    url = os.environ.get(url_env)
    if not url:
        raise RuntimeError(
            "%s is not set. Locally that means .env.local is missing or "
            "incomplete; on Vercel it means the environment variable was "
            "never added to the project." % url_env)
    kw.setdefault("sslrootcert", ca_bundle())
    kw.setdefault("connect_timeout", 10)
    return psycopg.connect(url, **kw)
