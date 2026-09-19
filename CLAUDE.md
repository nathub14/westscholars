# West Scholars website: working notes

Read this before changing anything. It is short on purpose.

## What this is

A static marketing site for West Scholars Education (Perth ASET / GATE and
private school scholarship exam prep). Plain HTML and CSS. **No build step, no
framework, no JavaScript.** Cloudflare Pages serves the repo root as-is.

## What the site is for

The homepage has exactly one job: **turn a visitor into a contact.** Most
traffic is warm, referred by an existing family, so the page leads with proof
rather than a pitch. Order is deliberate:

1. State plainly what we do, with the headline result beside it
2. Show the cohort photo straight away, uncaptioned, with the social links
3. Prove it in numbers (results section, the chart and the table)
4. Say who teaches it
5. Show the method in depth (this is the real differentiator)
6. Show the offer (what you actually get), then how it runs
7. Where this is headed, for families outside the ASET track
8. Answer "why not a big centre"
9. Remove risk (one guarantee)
10. Price, with the reason for the discount
11. A second, lower-commitment exit (the free guide)
12. Answer objections (FAQ), then ask (contact form)

The photo and the chart are two different proofs and are deliberately not
bundled: the photo says there is a real cohort and has to land before anyone
scrolls, the chart says the term worked and needs the room to be read. "Where
this is headed" sits in the first half rather than near the footer because a
real share of the traffic is after tutoring that is not the ASET.

Every section does exactly one job. If a section cannot be described in one
sentence starting "this section's only job is to", it does not have a reason to
exist yet.

Two exits, not one. High intent goes to the contact form. Low intent goes to the
guide, which captures a name, an email and a phone number. Never remove the
second exit.

`/current-clients/` has a different job: **retention and referral.**

`/refer/` **no longer exists.** It was a near duplicate of the homepage with
four sections worth keeping, so those were folded in (who teaches it, how it
runs, where this is headed, and its richer enquiry form) and the page was
removed. `_redirects` 301s `/refer` to `/`. Do not recreate it: the demand
gauging job is now done by the interest checkboxes on the homepage enquiry
form, and everything outside the ASET track is still framed there as something
we are building, never as a course that already exists.

## Files

| Path | Purpose |
| --- | --- |
| `index.html` | Homepage |
| `current-clients/index.html` | Page for existing families. Public and linked, not secret |
| `_redirects` | Cloudflare Pages redirects. Currently just `/refer` to `/` |
| `thanks.html` | Where the enquiry forms redirect after submitting |
| `guide.html` | Where the guide form redirects, holds the download |
| `404.html` | Not found page (Cloudflare Pages picks this up automatically) |
| `assets/style.css` | The entire design system and every component |
| `assets/logo.png` | Logo |
| `assets/og-image.png` | 1200x630 social share card |
| `assets/cohort.jpg` | Cohort photo, directly under the homepage hero and on `/current-clients/`. Derived, see below |
| `Perth-high-schools-guide.pdf` | The lead magnet |
| `robots.txt`, `sitemap.xml` | Search engine directives |
| `_headers` | Cloudflare Pages security and cache headers |

## Design system rules

Everything lives in `assets/style.css`, in numbered sections. Section 1 is the
tokens.

1. **Never hardcode a value in the HTML.** No `style="..."` attributes. If you
   need a spacing or colour tweak, use a utility class (section 27) or add a
   token. There are currently zero inline styles across all five pages, and a
   check enforces it (see Verifying below).
2. **Use the role tokens, not the raw ramps.** `var(--ink-soft)`, not
   `var(--warm-600)`. Ramps exist so roles have something to point at.
3. **Gold on light backgrounds must be `--accent-text` (`brass-700`).**
   `brass-400` is for fills, and for text on navy only. `brass-400` on white is
   2.9:1 and fails contrast.
4. **Spacing is a 4px scale.** `--s-1` through `--s-32`. No arbitrary pixel
   values.
5. **Type has nine sizes.** Use the `--fs-*` tokens. Do not introduce a tenth.
6. **Three elevation tiers**, `--e1` to `--e3`. Tier by importance: `e1` for
   list items and tiles, `e2` for cards, `e3` for the price card, guarantee and
   forms.
7. **Section rhythm has three tiers**: default, `.sec-major`, `.sec-tight`.
   Alternate `.section-cream`, `.section-white` and `.section-navy` so the page
   has cadence.

## Gotchas that have already bitten

- **`.social-proof` links restyle themselves on navy.** They are white-on-glass
  inside `.hero` and `.section-navy`, and dark-on-white everywhere else. If you
  move the strip, make sure it is inside a section with a known ground, not a
  bare `<div>`. That exact mistake made the Trustpilot and Facebook links
  invisible on the old site.
- **A white card inside `.section-navy` must set its own text colour.**
  `.section-navy` sets `h2`, `h3`, `h4` and `.lead` to the inverse ink for the
  navy ground, and those rules tie on specificity with a component's own, so a
  component that brings its own light `--surface` inherits white text on white.
  It has bitten twice: the guarantee block (`h2`, `.lead` and `.eyebrow` all
  went invisible) and the results data table, whose row labels are
  `<th scope="row">` while the only colour rule targeted `td:first-child`, so
  they matched nothing and inherited the white. That one was worse than it
  looked, because the table is the accessible fallback for the chart palette.
  The fix is to pin `color` on the component's own selectors (see `.guarantee`
  in section 15 and `.data-table tbody th` in section 27), not to move the
  section, because moving it breaks the cream and navy alternation. When you
  add a component to a navy section, check every text element in it, not just
  the heading. Third instance was the cohort photo's `figcaption` while the
  photo still sat in the results section. `.section-navy` covers `h2`, `h3`,
  `h4` and `.lead` and reaches no further, so the `figcaption` inherited the
  body ink and went near invisible on navy. That one is gone rather than fixed:
  the photo now runs on cream under the hero and carries no caption at all.
  The rule it taught still stands for anything else put on navy.
  `check.py` cannot catch this: it resolves contrast from the
  `:root` tokens and never sees the cascade. The reliable check is an iframe
  probe that composites ancestor backgrounds through their alpha and skips
  elements over a gradient ground.
- **Never write CSS hex escapes (`\\2713`) through a Python script.** Python
  will eat them as octal escapes and leave NUL bytes in the file. The stylesheet
  declares `@charset "UTF-8"` on line 1 and uses literal `✓` and `×` characters
  instead. Keep it that way.
- **The comparison block is a stack of pairs, not two columns.** Each
  `.vs-pair` is its own 2-column grid so the two halves of a claim always sit on
  the same line. On mobile it collapses into labelled cards. Do not turn it back
  into two independent lists; they drift out of alignment and become
  meaningless when stacked.
- **Mobile nav is a CSS-only checkbox disclosure.** `.nav-toggle` must stay a
  previous sibling of `.site-nav` for the `~` selector to work. Pages without a
  toggle use `.site-nav-simple`, which never collapses.
- **The nav collapses at 1050px, not at the 760px layout breakpoint.** Seven
  links plus a CTA need about 1050px; below that they squash and wrap onto two
  lines and the CTA pill deforms into a circle. If you add a nav link, re-check
  the header at 1060px and raise that breakpoint if needed.
- **`/current-clients/` is a normal public page.** It is linked from the
  homepage nav and footer and is indexable. It holds the existing-family rate
  and the referral payouts, so if that ever needs to change, the switch is a
  `noindex` meta tag plus removing those two links, not a robots.txt rule.
- **The results chart is generated, not hand-written.** Source of truth is
  `tools/chart.py`, which prints the SVG that is pasted inline into
  `index.html`. Do not hand-edit the SVG. Its four series hues were run through
  a colour-blindness and contrast validator; two of them fall below 3:1 on
  white, which is exactly why every line carries a direct end label AND the
  figures are repeated in the table view. Removing either breaks the
  accessibility case for the palette.
- **The chart's y-axis starts at zero and stays there.** A truncated axis would
  make a 30% gain look like a 3x one, which contradicts the honesty the whole
  page is positioned on.
- **Students on the chart are anonymised (Student 1 to 4).** They are named
  minors, and the chart publishes one child's declining result. Never put real
  first names on a public page.
- **`assets/cohort.jpg` is generated from `Group Photo Lighting Fix.jpg` in the
  repo root.** The source is a 3MB 4032x3024 original and must never be served.
  The shipped file is the **whole frame at its native 4:3, never cropped**,
  resized to 1440x1080 and saved as a progressive JPEG at quality 78, which
  lands around 410KB. 1440 is exactly 2x the 720px column it displays in.
  An earlier version was cropped to a 1.81:1 letterbox to drop the ceiling
  space above the group and it read as wrong, so leave the framing alone.
  The children in it are minors, so nothing around it names anyone, the same
  rule the results chart follows.
- **The cohort photo sits directly under the hero, on cream, with no
  caption.** It used to live inside the results section with a caption under
  it. Both moved for the same reason: it is the first proof a visitor meets and
  it should not need a scroll or an explanation. `.cohort-photo` caps it at the
  720px prose width, which is exactly half the 1440px file. If it ever goes
  back onto navy, it needs its own pinned text colour again, see the cascade
  note above.
- **The cohort photo is an `img` element, not a CSS background.** It was a
  background behind the hero for one deploy and it vanished on the live site:
  Cloudflare served a stale stylesheet against fresh markup, the `.hero-photo`
  rule did not exist yet at the edge, and the hero fell back to its plain
  gradient with nothing in place of the photo. An image element renders with no
  CSS at all, which is the property that matters for the only piece of visual
  proof on the site. Keep it that way.
- **The edge caches `/assets/*` for four hours, so a CSS change does not reach
  people on its own.** `_headers` asks for `max-age=3600` but the live response
  is `max-age=14400`, so that rule is not taking effect as written and is worth
  a look. Until it is fixed, the stylesheet link on every page carries a
  version query (`/assets/style.css?v=2`). **Bump that number on every page
  whenever you change the stylesheet in a way the HTML depends on**, otherwise
  new markup meets old CSS at the edge and the page renders wrong for hours.
  `check.py` skips link targets containing `?`, so the version does not trip
  the missing-file check.
- **Never write a literal img tag inside an HTML comment.** `check.py` scans
  raw text, so a commented-out one reads as a real image with no alt attribute
  and fails the run. Write "image element" in prose instead.
- **Headless Chrome will not make a window narrower than about 500px on
  Windows.** Screenshots at `--window-size=390` render wider and clip. Measure
  responsive behaviour with an iframe probe instead. The probe must exempt
  anything inside an `overflow-x: auto` ancestor, or the data table inside its
  scroller reads as a false positive.

## Content rules

Most of these are enforced by `check.py`, which carries a `BANNED` list with
the reason for each retirement. If a check fires, the phrase was retired on
purpose. Do not work around it.

- **No em dashes or en dashes anywhere.** Use commas, full stops or a colon.
- **Copy must never narrate its own reasoning.** No "this page is just for you",
  no "here is why I included this". That reads as AI self-talk. Write plain
  descriptive copy, or a plain list of what is on the page.
- **Never say "small classes". Say "four kids per class".** A number is proof, an
  adjective is marketing.
- **The term is eight weeks.** Every term-length reference says eight.
- **Two fixed proper nouns**, used verbatim everywhere they appear:
  - **The Sleep Like a Baby Guarantee** wherever the refund is mentioned.
  - **The Zero Gaps Scientific Scholar System** for the Workshop, practice,
    Clinic, patch cycle.
- **Workshop** is the two hour weekly group class. **Clinic** is the 45 minute
  weekly one-on-one. Always capitalised, never described generically.
- **The headline stat is "30% from baseline to final mock, across an eight week
  term", always with the early-results disclosure nearby.** Do not quote
  per-student or per-section percentages from the results data. They are
  mathematically correct but come from tiny samples, and a selectively framed
  statistic is a real problem under Australian Consumer Law, not just a
  credibility one. The 47% reading figure is retired and is in the banned list.
- **"Science-based" must always be cashable.** Wherever the copy leans on it,
  there is a nearby line naming spaced repetition and deliberate practice
  specifically, and the FAQ answers it in full. If a parent asks what makes it
  scientific, the site must already have answered. Do not add a science claim
  without that anchor.
- Never invent testimonials. There is a commented placeholder in `index.html`
  marking where real ones go once they exist.

## Forms

Both enquiry forms and the guide form post to FormSubmit
(`https://formsubmit.co/contact@westscholars.com.au`), which needs no backend.

Every form must carry:
- `_next` pointing at an absolute URL on this site, so the parent lands on our
  own confirmation page instead of a FormSubmit branded one
- a `_honey` honeypot input inside a `.hp` wrapper
- `_captcha` set to `false` and `_template` set to `table`

**The very first submission after go-live triggers a confirmation email to
`contact@westscholars.com.au` that must be clicked once before any form email
arrives.** That activation has been done, and the endpoint is live: a POST
carrying a `Referer` from this site answers `302` to the `_next` URL. A POST
with no referer at all gets FormSubmit's "open this page through a web server"
page instead, so testing with bare `curl` looks like a failure when it is not.
Send a referer header when you test.

**A filled `_honey` makes FormSubmit drop the submission and answer `200`
instead of the `302`.** The parent still reaches the thank-you page, so the
enquiry looks sent and simply never arrives. That is why `.hp` is `display:
none` and not an offscreen shift: an input parked at `left:-9999px` is a real,
focusable field that browser autofill or a password manager can fill. Keep it
`display: none`. A `display: none` input is still submitted, which is all the
honeypot needs.

**`_next` points at the extensionless URL (`/guide`, `/thanks`).** Cloudflare
Pages serves the canonical path without `.html` and `308`s the `.html` spelling
to it, so the old value cost a redirect hop on the way back from a cross origin
POST. Firefox and Safari enforce `form-action` across redirects, Chrome does
not, so the shorter chain is the safer one.

## Verifying a change

There is no test runner. Serve the site and run the checks:

```sh
python -m http.server 8777          # from the repo root
python check.py                     # structure, dashes, contrast, links
```

`check.py` fails on: em or en dashes, inline `style=` attributes, the phrase
"small classes", duplicate `id`s, in-page anchors with no target, missing local
files, images with no alt text, form inputs with no label, forms missing
`_next` or a honeypot, broken HTML nesting, and any design token pair below its
contrast target. Contrast is resolved from the `:root` tokens in the stylesheet,
so the check tracks the CSS instead of drifting from it.

**`_headers` rules match the path the edge actually serves, not the file
name.** The noindex rules for the two confirmation pages need `/guide` and
`/thanks` as well as the `.html` spellings. A `308` does not carry a header
onto the page the crawler finally reads, so keying the rule only to
`/guide.html` left the live `/guide` with no `X-Robots-Tag` at all. The
`noindex` meta tag in the markup was the only thing de-indexing it.

`robots.txt` stays permissive on purpose. A `Disallow` rule stops a crawler
reading the page at all, including any `noindex` meta tag on it, so the two
fight each other. Use `noindex` to de-index, never `Disallow`.

For layout, render with headless Chrome:

```sh
chrome --headless=new --disable-gpu --hide-scrollbars \
  --force-prefers-reduced-motion --virtual-time-budget=9000 \
  --window-size=1280,14000 --screenshot=out.png http://localhost:8777/index.html
```

`--force-prefers-reduced-motion` matters: without it the smooth-scroll animation
is caught mid-flight and the sticky header renders in the wrong place.

## Deploying

Cloudflare Pages, connected to this repo. Framework preset **None**, build
command **blank**, output directory `/`. Push to the default branch and it
deploys. `_headers` is applied at the edge with no build involved.

**`www` is bound to the Pages project as a second custom domain**, so it
serves the site directly rather than redirecting to the apex. Both hostnames
answer `200` on every path. The only thing keeping the www copy out of the
index is a `<link rel="canonical">` naming the apex, so every indexable page
needs one and it must name the apex, never www. All three content pages carry
one. The two confirmation pages do not, which does not matter, because they
carry `noindex`.

## Still open

- [ ] **Cloudflare Email Address Obfuscation (Scrape Shield) is on**, so every
      `mailto:` is rewritten at the edge into `/cdn-cgi/l/email-protection#...`
      and a decoder script is injected. The address renders as
      "[email protected]" until that script runs. It contradicts the no
      JavaScript rule the CSP comment states, and it makes the "Email us" exit
      depend on JS. It leaves the FormSubmit `action` attributes alone today,
      which is the only reason the forms still work. Turn it off in Scrape
      Shield unless there is a reason to keep it
- [ ] Feedback survey link, once the survey exists. The button is currently a
      non-clickable `.btn-disabled` span, deliberately, rather than a dead link
- [ ] The three review-prompt templates on the current clients page are
      placeholders. Nathan is supplying his own
- [ ] No testimonials yet. When the first parent reviews arrive they go in the
      marked slot on `index.html`, directly under the results section, and a
      quote or two belongs near the results section as well. Until then every page proves
      social proof by linking out to Google, Facebook and Trustpilot through
      the `.social-proof` strip. No review text is quoted anywhere on the site,
      because there is none to quote yet
- [ ] `chart_student_trajectories.png` not supplied. The results section is
      text and stat tiles only for now
- [ ] Consider moving the guide form to a real email list (MailerLite or
      ConvertKit) so leads land somewhere followable, rather than only in the
      inbox. The form action is a one-line swap when that happens

## tools/

Two helpers, not part of the deployed site.

- `tools/chart.py` builds the results chart. Run it from the repo root, then
  paste the printed `chart.svg` over the existing `<svg>` block in
  `index.html`. Edit the data at the top of the file, never the SVG.
- `tools/responsive-probe.html` measures every page at ten viewport widths and
  reports any element overflowing the viewport. Serve the site, open
  `/tools/responsive-probe.html`, and read the output. It is the reliable way
  to check mobile layout, because headless screenshots at phone widths clip
  rather than reflow on Windows.
