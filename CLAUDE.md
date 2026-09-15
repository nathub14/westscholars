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
- **Headless Chrome will not make a window narrower than about 500px on
  Windows.** Screenshots at `--window-size=390` render wider and clip. Measure
  responsive behaviour with an iframe probe instead (see Verifying below).

## Content rules

- **No em dashes or en dashes anywhere.** Use commas, full stops or a colon.
  This is enforced by the check script.
- **Never say "small classes". Say "four kids per class".** A number is proof, an
  adjective is marketing.
- **The headline stat is "30% growth from baseline to final mark, in one term",
  always with the pilot-cohort disclosure nearby.** Do not quote per-student or
  per-section percentages from the results data. They are mathematically correct
  but come from tiny samples, and a selectively framed statistic is a real
  problem under Australian Consumer Law, not just a credibility one.
- **One guarantee, called the Worth It Guarantee.** Full refund, any time, any
  reason, no conditions.
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
