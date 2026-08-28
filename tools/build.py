"""Build the deployable site into dist/, with the comments taken out.

WHY THIS EXISTS
---------------
This codebase is unusually heavily commented and that is deliberate: nearly
every rule in `site.css` and every block in `site.js` records something that
went wrong once, and the comments are the only place that knowledge lives.
They should never be removed from the source.

They should also never be sent to a reader. Measured on 28 August 2026:

    assets/css/site.css   173,109 bytes   45% comments
    assets/js/site.js      56,627 bytes   36% comments
    the nine HTML pages    349,775 bytes  16% comments

Brotli, which is what Vercel actually sends, does not make this go away:

    site.css   39,870 -> 14,570 brotli   (-63%)
    site.js    14,452 ->  7,812 brotli   (-46%)
    HTML                                 (-2.2KB per page)

The stylesheet is render blocking, so that 25KB is 25KB the browser waits
for before it paints anything. This script is the thing that lets the source
stay documented and the wire stay small.

WHAT IT DOES NOT DO
-------------------
It is not a minifier. It does not rename anything, collapse whitespace inside
rules, reorder declarations or touch a single character of code. It removes
comments and the blank lines they leave behind, and nothing else. That is
where almost all of the win is here, and it is the only transformation that
cannot change behaviour.

    python3 tools/build.py

Then deploy from `dist/`, which is what `tools/ship.sh` does.
"""
import base64, hashlib, io, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")

# Everything under here is a working document, a source library or local
# tooling. Kept in step with .vercelignore by the check at the bottom of this
# file, which fails the build if the two drift apart.
EXCLUDE_DIRS = {
    "CydnieJocelyn-Site", "Costa Rica copy", "Family Travel copy", "Fonts copy",
    "cydniejocelyn", ".git", ".vercel", ".claude", "tools", "dist", "node_modules",
    "The Build page", "Greece Retreat", "Retreat drafts", "_unused",
    "A Sounding", "The Letters Page", "the questions", "Privacy terms page",
}
EXCLUDE_FILES = {"HANDOFF.md", "BRIEF.md", "README.md", ".DS_Store", ".vercelignore", ".gitignore"}


# ---------- the strippers -------------------------------------------------
# Each one is written to fail closed: if it cannot prove a comment is a
# comment, it leaves it alone. A build that ships a few hundred extra bytes is
# a non-event. A build that eats a `//` inside a URL is a broken site.

def strip_block_comments(src, path):
    """Remove /* ... */ where it is genuinely a comment.

    Walks the file rather than running a regex over it, so an opener inside a
    string literal is skipped instead of swallowing everything to the next
    `*/`. `site.css` has no such case today and `site.js` has none either,
    both verified before this was written, but 'today' is the part of that
    sentence that expires.
    """
    out = []
    i, n = 0, len(src)
    quote = None
    while i < n:
        c = src[i]
        if quote:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(src[i + 1]); i += 2; continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c in "\"'":
            quote = c; out.append(c); i += 1; continue
        if c == "/" and i + 1 < n and src[i + 1] == "*":
            end = src.find("*/", i + 2)
            if end == -1:                      # unterminated: leave it alone
                out.append(src[i:]); break
            i = end + 2
            continue
        out.append(c); i += 1
    return "".join(out)


def collapse_blank_lines(s):
    s = re.sub(r"[ \t]+\n", "\n", s)
    return re.sub(r"\n{3,}", "\n\n", s)


def strip_css(s, path):
    return collapse_blank_lines(strip_block_comments(s, path)).lstrip("\n")


def strip_js(s, path):
    """Block comments only.

    Line comments are deliberately NOT touched. `//` appears inside every URL
    in this codebase and telling a comment from a protocol separator needs a
    real tokenizer. Both JS files were checked when this was written and
    neither contains a single `//` comment, so there is nothing to gain and a
    site to lose.
    """
    return collapse_blank_lines(strip_block_comments(s, path)).lstrip("\n")


def strip_html(s, path):
    """Remove <!-- --> outside <script> and <style>.

    Splitting on those two first is the whole safety story: a `<!--` inside a
    script is JavaScript, not a comment, and a stripper that does not know the
    difference will cut from there to the next `-->` anywhere in the file.
    Conditional comments are preserved on sight.
    """
    parts = re.split(r"(<(?:script|style)\b[^>]*>.*?</(?:script|style)>)", s, flags=re.S | re.I)
    for k in range(0, len(parts), 2):          # even indices are outside script/style
        parts[k] = re.sub(r"<!--(?!\[if)(?:(?!-->).)*?-->", "", parts[k], flags=re.S)
    out = "".join(parts)
    # a comment on its own line leaves the line behind
    out = re.sub(r"\n[ \t]*\n{2,}", "\n\n", out)
    return re.sub(r"[ \t]+\n", "\n", out)


STRIP = {".css": strip_css, ".js": strip_js, ".html": strip_html}


# ---------- the guard that makes `immutable` safe -------------------------

def check_stamps():
    """Refuse to build if any page points at a stale ?v= hash.

    `vercel.json` marks /assets/css/ and /assets/js/ **immutable** for a year.
    That is only correct because `stamp.py` puts a content hash in the URL, so
    a changed file is a changed URL. If a page ever ships with a stale hash,
    `immutable` means a returning reader is pinned to the old stylesheet and
    will never even revalidate it. That is the exact failure the header was
    reverted for once already; see the docstring in stamp.py.

    So the rule is: the deploy cannot happen with a stale stamp. Not 'should
    not'. Cannot.
    """
    # Imported, not recomputed. See stamp.py's version() docstring for what
    # having two copies of this arithmetic cost.
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import stamp
    want = stamp.version()
    bad = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in filenames:
            if f != "index.html":
                continue
            p = os.path.join(dirpath, f)
            s = io.open(p, encoding="utf-8").read()
            for got in re.findall(r'(?:site\.css|site\.js|analytics\.js|consent\.js)\?v=([0-9a-f]+)', s):
                if got != want:
                    bad.append((os.path.relpath(p, ROOT), got))
    if bad:
        print("STALE STAMPS. Run `python3 tools/stamp.py` and commit, then build again.")
        print("   expected %s" % want)
        for p, got in sorted(set(bad)):
            print("   %-32s has %s" % (p, got))
        sys.exit(1)
    return want


def check_vercelignore():
    """The exclude list here and .vercelignore must agree.

    They are two lists of the same thing and the failure mode of them drifting
    is a working document served in production, which has happened on this
    project twice. This does not merge them; it just refuses to let a folder
    be excluded from one and not the other.
    """
    vi = io.open(os.path.join(ROOT, ".vercelignore"), encoding="utf-8").read()
    listed = {l.strip().rstrip("/") for l in vi.splitlines()
              if l.strip() and not l.strip().startswith("#")}
    known = EXCLUDE_DIRS | EXCLUDE_FILES
    missing = sorted(d for d in listed
                     if d not in known and os.path.basename(d) not in known
                     and os.path.exists(os.path.join(ROOT, d)))
    if missing:
        print("DRIFT: .vercelignore excludes these and tools/build.py does not:")
        for m in missing:
            print("   %s" % m)
        sys.exit(1)


def warn_unreferenced():
    """Say so if anything in assets/img/ has stopped being referenced.

    1MB of it accumulated silently over nine sessions: superseded lockups,
    JPEG originals of files that ship as WebP, hero crops from picture passes
    that were replaced. None of it cost page load, because nothing asked for
    it, and all of it was uploaded on every deploy. It now lives in
    assets/_unused/ with a README saying what each file was.

    This is the thing that stops that happening again quietly.
    """
    src = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in filenames:
            if os.path.splitext(f)[1].lower() in (".html", ".css", ".js", ".txt", ".xml", ".json"):
                src.append(os.path.join(dirpath, f))
    blob = "".join(io.open(p, encoding="utf-8", errors="replace").read() for p in src)
    stale = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "assets/img")):
        dirnames[:] = [d for d in dirnames if d != "_unused"]
        for f in filenames:
            if f not in blob:
                stale.append((os.path.relpath(os.path.join(dirpath, f), ROOT),
                              os.path.getsize(os.path.join(dirpath, f))))
    if stale:
        print("WARNING: %d file(s) in assets/img/ that nothing references, %d bytes."
              % (len(stale), sum(s for _, s in stale)))
        for p, s in sorted(stale, key=lambda x: -x[1]):
            print("   %-52s %8d" % (p, s))
        print("   Move them to assets/_unused/ or reference them. See that folder's README.")




def check_headers():
    """Fail the build if the security headers have been weakened.

    These went in on 28 August 2026 and every one of them was verified
    against a server sending the real thing, not a <meta> approximation:
    `frame-ancestors` and `upgrade-insecure-requests` are ignored in a meta
    tag, so a meta test cannot see them at all.

    The check exists because a CSP is the easiest header in the world to
    "fix" by pasting 'unsafe-inline' into it when something breaks. That
    turns a policy that closes the whole reflected-XSS class into one that
    closes nothing while still appearing in every header dump. If a future
    inline script will not run, the answer is seal_csp() picking up its hash,
    which is automatic -- not a wildcard.
    """
    conf = io.open(os.path.join(ROOT, "vercel.json"), encoding="utf-8").read()
    data = json.loads(conf)
    catchall = [h for h in data["headers"] if h["source"] == "/(.*)"]
    if not catchall:
        print("HEADERS: no catch-all rule in vercel.json."); sys.exit(1)
    have = {h["key"]: h["value"] for h in catchall[0]["headers"]}

    required = ("Content-Security-Policy", "Strict-Transport-Security",
                "X-Content-Type-Options", "X-Frame-Options",
                "Referrer-Policy", "Permissions-Policy",
                "Cross-Origin-Opener-Policy")
    missing = [k for k in required if k not in have]
    if missing:
        print("HEADERS: vercel.json no longer sends %s" % ", ".join(missing))
        sys.exit(1)

    csp = have["Content-Security-Policy"]
    script = [d for d in csp.split(";") if d.strip().startswith("script-src")]
    if not script:
        print("HEADERS: the CSP has no script-src."); sys.exit(1)
    for bad in ("'unsafe-inline'", "'unsafe-eval'", "'strict-dynamic'", "http:", "*"):
        if bad in script[0]:
            print("HEADERS: script-src has been widened with %s." % bad)
            print("   %s" % script[0].strip())
            sys.exit(1)
    if "__INLINE_SCRIPT_HASHES__" not in script[0] and "'sha256-" not in script[0]:
        print("HEADERS: script-src carries neither the hash placeholder nor any")
        print("   sha256, so every inline script on the site would be blocked.")
        sys.exit(1)
    for d in ("frame-ancestors 'none'", "object-src 'none'", "base-uri 'none'"):
        if d not in csp:
            print("HEADERS: the CSP no longer sets %s." % d); sys.exit(1)


# ---------- the CSP script hashes ----------------------------------------

def csp_hashes():
    """sha256 of every inline executable script in the BUILT pages.

    Computed from dist/ and not from the source, because the comment
    strippers change the bytes inside an inline script and comments are 16%
    of the HTML. A hash taken from the source would be wrong for the thing
    that ships. Same reason stamp.py runs before the build.

    `type="application/ld+json"` is skipped on purpose: it is data, not
    script, CSP does not check it, and hashing it would mean nine more hashes
    that change every time a meta description does.
    """
    out = set()
    for dirpath, _dirnames, filenames in os.walk(DIST):
        for f in filenames:
            if not f.endswith(".html"):
                continue
            html = io.open(os.path.join(dirpath, f), encoding="utf-8").read()
            for m in re.finditer(r"<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>", html, re.S):
                if "ld+json" in m.group(1):
                    continue
                digest = hashlib.sha256(m.group(2).encode("utf-8")).digest()
                out.add("'sha256-" + base64.b64encode(digest).decode() + "'")
    return out


def _apply_hashes(conf, hashes):
    """Rewrite script-src so it carries exactly `hashes` and nothing stale."""
    def fix(directive):
        toks = directive.split()
        kept = [t for t in toks
                if not t.startswith("'sha256-") and t != "__INLINE_SCRIPT_HASHES__"]
        # 'self' stays first, the hashes go next, named origins after
        head = kept[:2]                      # ["script-src", "'self'"]
        return " ".join(head + sorted(hashes) + kept[2:])
    parts = conf.split("script-src ", 1)
    if len(parts) != 2:
        return conf
    rest, tail = parts[1].split(";", 1)
    return parts[0] + fix("script-src " + rest) + ";" + tail


def seal_csp():
    """Put the hashes into BOTH vercel.json copies, dist and root.

    WHY BOTH, WHICH LOOKS REDUNDANT AND IS NOT
    ------------------------------------------
    `vercel deploy --cwd dist` uploads dist/ and then reads vercel.json from
    the SHELL's working directory, not from --cwd. On 28 August 2026 that put
    a production CSP live whose script-src held the literal string
    `__INLINE_SCRIPT_HASHES__`. Browsers drop an unrecognised source
    expression and enforce the rest, so every inline script on the site was
    blocked: analytics, the js-motion flip, and the Flodesk signup. The HTML
    and CSS were correct. Only the header was wrong.

    ship.sh now cds into dist/ so the right file is read. Sealing the root
    copy as well is the second lock: whatever anyone runs, from wherever,
    there is no longer a deployable vercel.json in this repo that carries an
    unsubstituted placeholder.

    THE TRADE, STATED PLAINLY. Because this hashes whatever it finds, a new
    inline script added to a page is automatically permitted. It protects
    against injected script, not against something a person deliberately
    pastes into the head. That is the normal shape of a hash-based policy.
    """
    hashes = csp_hashes()
    if not hashes:
        print("CSP: no inline scripts found, which is suspicious. Not sealing.")
        sys.exit(1)

    for path, label in ((os.path.join(DIST, "vercel.json"), "dist"),
                        (os.path.join(ROOT, "vercel.json"), "root")):
        if not os.path.isfile(path):
            continue
        conf = io.open(path, encoding="utf-8").read()
        sealed = _apply_hashes(conf, hashes)
        if sealed != conf:
            io.open(path, "w", encoding="utf-8").write(sealed)
        if "__INLINE_SCRIPT_HASHES__" in sealed:
            print("CSP: failed to seal the %s vercel.json." % label)
            sys.exit(1)

    print("   CSP sealed with %d inline script hash(es), dist and root" % len(hashes))



def purge_icloud_conflicts():
    """Delete the "name 2" copies iCloud leaves inside dist/.

    THIS PROJECT LIVES ON THE DESKTOP AND THE DESKTOP IS SYNCED TO iCLOUD
    DRIVE. `build()` does `shutil.rmtree(DIST)` and recreates the whole tree
    on every run, and iCloud reads a wipe-and-recreate as a conflict, so it
    helpfully writes duplicates beside the real thing:

        dist/about 2   dist/assets 2   dist/assets 3   dist/privacy-policy 2
        dist/sounding-popup 2.js       dist/.vercel/README 2.txt

    On 28 August 2026 this took a production deploy down. `vercel deploy`
    listed the directory, started walking `dist/privacy-policy 2`, and iCloud
    removed it mid-scan:

        ENOENT: no such file or directory, scandir '.../dist/privacy-policy 2'

    That is a failure with no bad commit behind it, which is the worst kind
    to debug from the error alone. Even when they survive the scan they are
    stale part-copies of real routes and would be uploaded.

    Nothing legitimate in dist/ is named "<something> <digit>", because every
    byte of dist/ is generated by this file. So the shape is safe to delete
    on sight. `ship.sh` runs the same sweep again immediately before the
    deploy, because iCloud can write a new one in the seconds between.
    """
    pat = re.compile(r" \d+(\.[A-Za-z0-9]+)?$")
    killed = []
    for dirpath, dirnames, filenames in os.walk(DIST, topdown=False):
        for name in list(dirnames):
            if pat.search(name):
                shutil.rmtree(os.path.join(dirpath, name), ignore_errors=True)
                dirnames.remove(name)
                killed.append(os.path.relpath(os.path.join(dirpath, name), DIST))
        for name in filenames:
            if pat.search(name):
                try:
                    os.remove(os.path.join(dirpath, name))
                    killed.append(os.path.relpath(os.path.join(dirpath, name), DIST))
                except OSError:
                    pass
    if killed:
        print("   swept %d iCloud conflict cop%s out of dist/"
              % (len(killed), "y" if len(killed) == 1 else "ies"))
        for k in sorted(killed)[:8]:
            print("      %s" % k)
    return killed


# ---------- build ---------------------------------------------------------

def build():
    check_vercelignore()
    check_headers()
    stamp = check_stamps()

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    before = after = 0
    counts = {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        rel = os.path.relpath(dirpath, ROOT)
        for f in filenames:
            if f in EXCLUDE_FILES:
                continue
            src = os.path.join(dirpath, f)
            dst = os.path.join(DIST, rel, f) if rel != "." else os.path.join(DIST, f)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            ext = os.path.splitext(f)[1].lower()
            if ext in STRIP:
                s = io.open(src, encoding="utf-8").read()
                out = STRIP[ext](s, src)
                a, b = len(s.encode()), len(out.encode())
                before += a; after += b
                c = counts.setdefault(ext, [0, 0, 0])
                c[0] += 1; c[1] += a; c[2] += b
                io.open(dst, "w", encoding="utf-8").write(out)
            else:
                shutil.copy2(src, dst)

    # the project link, so `vercel deploy --cwd dist` knows what it is
    link = os.path.join(ROOT, ".vercel")
    if os.path.isdir(link):
        shutil.copytree(link, os.path.join(DIST, ".vercel"), dirs_exist_ok=True)

    purge_icloud_conflicts()
    seal_csp()
    warn_unreferenced()
    print("built dist/ at stamp %s" % stamp)
    for ext in sorted(counts):
        n, a, b = counts[ext]
        print("   %-6s %2d files  %8d -> %8d bytes  (-%.0f%%)" % (ext, n, a, b, 100 * (a - b) / a))
    print("   %-6s    total    %8d -> %8d bytes  (-%.0f%%)" %
          ("", before, after, 100 * (before - after) / before))
    try:
        import brotli
        css = os.path.join(DIST, "assets/css/site.css")
        src = os.path.join(ROOT, "assets/css/site.css")
        ba = len(brotli.compress(io.open(src, "rb").read(), quality=11))
        bb = len(brotli.compress(io.open(css, "rb").read(), quality=11))
        print("   site.css over the wire (brotli): %d -> %d bytes" % (ba, bb))
    except ImportError:
        pass


if __name__ == "__main__":
    build()
