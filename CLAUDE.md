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
2. Prove it (results section)
3. Show the offer (what you actually get)
4. Show the method in depth (this is the real differentiator)
5. Remove risk (one guarantee)
6. Price, with the reason for the discount
7. Scarcity
8. A second, lower-commitment exit (the free guide)
9. Answer objections (FAQ), then ask (contact form)

Two exits, not one. High intent goes to the contact form. Low intent goes to the
guide, which captures an email. Never remove the second exit.

`/current-clients/` has a different job: **retention and referral.**

## Files

| Path | Purpose |
| --- | --- |
| `index.html` | Homepage |
| `current-clients/index.html` | Page for existing families. Public and linked, not secret |
| `thanks.html` | Where the enquiry forms redirect after submitting |
| `guide.html` | Where the guide form redirects, holds the download |
| `404.html` | Not found page (Cloudflare Pages picks this up automatically) |
| `assets/style.css` | The entire design system and every component |
| `assets/logo.png` | Logo |
| `assets/og-image.png` | 1200x630 social share card |
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
arrives.**

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

## Still open

- [ ] Google Business review link (`current-clients/index.html`, Reviews
      section) is the only remaining red "Add link" tag
- [ ] Feedback survey link, once the survey exists. The button is currently a
      non-clickable `.btn-disabled` span, deliberately, rather than a dead link
- [ ] The three review-prompt templates on the current clients page are
      placeholders. Nathan is supplying his own
- [ ] No testimonials yet. When the first parent reviews arrive they go in the
      marked slot on `index.html`, directly under the results section
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
