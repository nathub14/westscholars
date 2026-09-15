# West Scholars website

Plain static HTML and CSS. No build step, so Cloudflare Pages deploys the repo
root as-is.

**If you are Claude Code, read `CLAUDE.md` first.** It carries the design system
rules, the content rules, and the gotchas that have already caused bugs here.

## Pages

| Path | Purpose |
| --- | --- |
| `index.html` | Homepage. Proof, the program, the method, pricing, guarantee, free guide, FAQ, contact |
| `current-clients/index.html` | Private page for existing families. Re-enrolment, guarantee, referrals, reviews, feedback |
| `thanks.html` | Where the enquiry forms land after submitting |
| `guide.html` | Where the guide form lands, holds the PDF download |
| `404.html` | Not found page, picked up automatically by Cloudflare Pages |

Supporting files: `assets/style.css` (the whole design system),
`assets/logo.png`, `assets/og-image.png` (social share card),
`Perth-high-schools-guide.pdf` (the lead magnet), `robots.txt`, `sitemap.xml`,
`_headers` (security and cache headers applied at the Cloudflare edge).

## The current clients page

`/current-clients/` is a normal public page, linked from the homepage nav and
footer. It holds the existing-family rate and the referral payouts, so it is
deliberately left out of `sitemap.xml`: it is reachable and indexable, but
there is no reason to actively push search engines at it ahead of the homepage.

If you ever want it hidden, the switch is a `noindex` meta tag on the page plus
removing the two links, not a `robots.txt` rule. A `Disallow` would stop
crawlers reading the `noindex` tag, which is the opposite of what you want.

## Forms

Both enquiry forms and the guide form post to
`https://formsubmit.co/contact@westscholars.com.au`, a free form-to-email
service that needs no backend. Each one redirects back to a page on this site
(`_next`) and carries a honeypot field against spam.

**The first submission after this goes live triggers a confirmation email to
`contact@westscholars.com.au` that must be clicked once before any form emails
start arriving.** Send one test enquiry yourself immediately after deploying.

## Checking your work

```sh
python -m http.server 8777     # serve at http://localhost:8777
python check.py                # structure, content rules, a11y, contrast
```

`check.py` exits non-zero on failure and catches: em and en dashes, inline
`style=` attributes, the phrase "small classes", duplicate ids, dead in-page
anchors, missing local files, images with no alt text, form controls with no
label, forms missing a redirect or honeypot, broken HTML nesting, and any design
token pair that falls below its contrast target. Contrast is read from the CSS
tokens, so it cannot drift out of step with the stylesheet.

## Deploying to Cloudflare Pages

1. Push this repo to GitHub.
2. Cloudflare dashboard: **Workers & Pages → Create → Pages → Connect to Git**.
3. Pick this repo. Build settings:
   - Framework preset: **None**
   - Build command: *(leave blank)*
   - Build output directory: `/`
4. Deploy. Cloudflare gives a `*.pages.dev` URL immediately. Add the custom
   domain under the project's **Custom domains** tab.

## Still open

- [ ] **Google Business review link** (`current-clients/index.html`, Reviews
      section). Still pending. The only remaining red "Add link" tag
- [ ] Feedback survey link. The button is currently a deliberately
      non-clickable disabled control rather than a dead link
- [ ] The three review-prompt templates on the current clients page are a first
      draft. Nathan is supplying his own
- [ ] **No testimonials yet.** There is a marked slot in `index.html` directly
      under the results section. Parent words will outrank every stat on the
      page, so this is the highest-value thing still missing
- [ ] `chart_student_trajectories.png` not supplied. The results section is
      text and stat tiles for now
- [ ] The guide form captures leads to the inbox only. Moving it to a real
      email list (MailerLite or ConvertKit free tier) is a one-line change to
      the form action when you want follow-up sequences

Phone, email, Facebook and Trustpilot links are all live and real.
