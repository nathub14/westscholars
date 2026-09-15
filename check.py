#!/usr/bin/env python3
"""West Scholars site checks.

No dependencies, no build step. Run from the repo root:

    python check.py

Exits non-zero if anything fails, so it can be wired into CI later.
Checks structure, house content rules, accessibility basics and colour
contrast. It does not check that the site looks good, only that it is not
broken in ways that are easy to miss by eye.
"""

import io
import os
import re
import sys
from html.parser import HTMLParser

PAGES = [
    "index.html",
    "current-clients/index.html",
    "thanks.html",
    "guide.html",
    "404.html",
]

CSS = "assets/style.css"

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}

# Phrases that must never appear again, with the reason shown on failure.
# These are decisions, not preferences: each one was explicitly retired.
BANNED = [
    (r"small class",
     'say "four kids per class" instead. A number is proof, an adjective is marketing'),
    (r"\b(10|ten)[ -]week",
     "the term is eight weeks. Every term-length reference must say eight"),
    (r"worth it guarantee",
     'the guarantee is "The Sleep Like a Baby Guarantee"'),
    (r"improvement guarantee|happiness guarantee|club a baby seal|improve,? or my shoes",
     "there is one guarantee, The Sleep Like a Baby Guarantee"),
    (r"long track record",
     'use "early results" framing instead'),
    (r"this page is just for you|here is why I|here's why I",
     "copy must not narrate its own reasoning. Write plain descriptive copy"),
    (r"no strings|right of refusal",
     "retired phrasing"),
    (r"47%",
     "the per-section improvement percentages are internal only, never public"),
]

failures = []
notes = []


def fail(page, msg):
    failures.append("%s: %s" % (page, msg))


def note(msg):
    notes.append(msg)


def read(path):
    return io.open(path, encoding="utf-8").read()


# ---------------------------------------------------------------------------
# HTML nesting
# ---------------------------------------------------------------------------

class Nesting(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append("stray </%s>" % tag)
            return
        if self.stack[-1][0] != tag:
            self.errors.append(
                "</%s> on line %d closes <%s> opened on line %d"
                % (tag, self.getpos()[0], self.stack[-1][0], self.stack[-1][1])
            )
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    return
            return
        self.stack.pop()


# ---------------------------------------------------------------------------
# Contrast
# ---------------------------------------------------------------------------

def luminance(hexcolour):
    h = hexcolour.lstrip("#")
    channels = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
              for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a, b):
    high, low = sorted([luminance(a), luminance(b)], reverse=True)
    return (high + 0.05) / (low + 0.05)


# Every colour pair that carries text, named by TOKEN so this check tracks the
# stylesheet instead of drifting from it. Targets are WCAG AA.
CONTRAST_PAIRS = [
    ("eyebrow gold on cream",         "--brass-700", "--warm-50",    4.5),
    ("eyebrow gold on white",         "--brass-700", "--white",      4.5),
    ("body text on white",            "--warm-600",  "--white",      4.5),
    ("body text on cream",            "--warm-600",  "--warm-50",    4.5),
    ("ink on cream",                  "--warm-900",  "--warm-50",    4.5),
    ("heading navy on white",         "--navy-800",  "--white",      4.5),
    ("gold stat on navy",             "--brass-300", "--navy-800",   4.5),
    ("gold rule on navy",             "--brass-400", "--navy-800",   4.5),
    ("body on navy",                  "--navy-100",  "--navy-800",   4.5),
    ("nav link on navy",              "--navy-100",  "--navy-900",   4.5),
    ("footer text on navy",           "--navy-300",  "--navy-950",   4.5),
    ("gold button label",             "--navy-900",  "--brass-400",  4.5),
    ("comparison text on warm-100",   "--warm-600",  "--warm-100",   4.5),
    ("comparison header on warm-300", "--warm-700",  "--warm-300",   4.5),
    ("success tick on white",         "--success",   "--white",      4.5),
    ("warning notice text",           "--warning",   "--warning-bg", 4.5),
    ("placeholder on cream",          "--ink-faint", "--warm-50",    4.5),
    ("optional label on white",       "--ink-faint", "--white",      4.5),
    ("disclosure on navy",            "--navy-300",  "--navy-800",   4.5),
]


def parse_tokens(css):
    """Pull the literal hex values out of the :root block."""
    root = css[css.index(":root {"):css.index("\n}", css.index(":root {"))]
    return dict(re.findall(r"(--[\w-]+):\s*(#[0-9a-fA-F]{6})\s*;", root))


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def main():
    if not os.path.exists(CSS):
        print("Run this from the repo root (cannot see %s)." % CSS)
        return 1

    css = read(CSS)
    css_classes = set(re.findall(r"\.([a-zA-Z][\w-]*)", css))

    # -- stylesheet ---------------------------------------------------------
    if not css.startswith('@charset "UTF-8";'):
        fail(CSS, 'must start with @charset "UTF-8"; because it uses literal '
                  "non-ASCII characters in content: values")
    if "\x00" in css:
        fail(CSS, "contains NUL bytes, almost certainly a mangled CSS escape")
    backslash_escape = 'content: "' + chr(92)
    if backslash_escape in css:
        fail(CSS, "uses a CSS hex escape in a content: value. Use the literal "
                  "character instead, see CLAUDE.md")

    # -- pages --------------------------------------------------------------
    for page in PAGES:
        if not os.path.exists(page):
            fail(page, "missing")
            continue
        s = read(page)

        # House style: no dashes.
        for char, name in ((u"—", "em dash"), (u"–", "en dash")):
            for m in re.finditer(re.escape(char), s):
                ctx = s[max(0, m.start() - 40):m.start() + 20].replace("\n", " ")
                fail(page, "%s found near: ...%s..." % (name, ctx.strip()))

        # No inline styles: everything belongs in the design system.
        for m in re.finditer(r'style="([^"]*)"', s):
            fail(page, 'inline style="%s"' % m.group(1))

        # Retired wording.
        for pattern, why in BANNED:
            for m in re.finditer(pattern, s, re.I):
                ctx = s[max(0, m.start() - 30):m.start() + 40].replace("\n", " ")
                fail(page, 'banned phrase "%s": %s. Near: ...%s...'
                     % (m.group(0), why, ctx.strip()))

        # Structure.
        ids = re.findall(r'\sid="([^"]+)"', s)
        for i in {x for x in ids if ids.count(x) > 1}:
            fail(page, 'duplicate id="%s"' % i)

        for anchor in sorted(set(re.findall(r'href="#([^"]+)"', s))):
            if anchor not in ids:
                fail(page, "anchor #%s has no matching element" % anchor)

        for m in re.finditer(r'(?:href|src)="(/[^"#?]+)"', s):
            target = m.group(1).lstrip("/")
            if target.endswith("/"):
                target += "index.html"
            if not os.path.exists(target):
                fail(page, "links to missing file %s" % m.group(1))

        # Accessibility basics.
        if "<main" not in s:
            fail(page, "has no <main> landmark")
        if s.count("<h1") != 1:
            fail(page, "must have exactly one <h1>, found %d" % s.count("<h1"))
        for m in re.finditer(r"<img\b(?![^>]*\balt=)[^>]*>", s):
            fail(page, "img with no alt attribute: %s" % m.group(0)[:60])
        for m in re.finditer(r'<(input|select|textarea)\b[^>]*id="([^"]+)"', s):
            if 'for="%s"' % m.group(2) not in s:
                fail(page, "form control #%s has no label" % m.group(2))

        # Forms.
        for m in re.finditer(r'<form\b[^>]*action="([^"]+)"', s):
            end = s.find("</form>", m.start())
            block = s[m.start():end if end != -1 else len(s)]
            if 'name="_next"' not in block:
                fail(page, "form has no _next redirect, so it would dump the "
                           "visitor on a third party page")
            if 'name="_honey"' not in block:
                fail(page, "form has no honeypot")

        # Nesting.
        parser = Nesting()
        parser.feed(s)
        for e in parser.errors:
            fail(page, "nesting: %s" % e)
        if parser.stack:
            fail(page, "unclosed tags: %s" % [t for t, _ in parser.stack])

        # Typo catcher, informational only.
        used = set()
        for m in re.finditer(r'class="([^"]+)"', s):
            used.update(m.group(1).split())
        unknown = sorted(c for c in used if c not in css_classes)
        if unknown:
            note("%s uses classes with no CSS rule: %s" % (page, unknown))

    # -- contrast -----------------------------------------------------------
    tokens = parse_tokens(css)
    for name, fg_token, bg_token, need in CONTRAST_PAIRS:
        if fg_token not in tokens or bg_token not in tokens:
            missing = [t for t in (fg_token, bg_token) if t not in tokens]
            fail("contrast", "%s references undefined token(s) %s" % (name, missing))
            continue
        ratio = contrast(tokens[fg_token], tokens[bg_token])
        if ratio < need:
            fail("contrast", "%s (%s on %s) is %.2f:1, needs %.1f:1"
                 % (name, fg_token, bg_token, ratio, need))

    # -- report -------------------------------------------------------------
    for n in notes:
        print("note: %s" % n)
    if notes:
        print("")

    if failures:
        for f in failures:
            print("FAIL %s" % f)
        print("\n%d failure(s)." % len(failures))
        return 1

    print("All checks passed (%d pages)." % len(PAGES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
