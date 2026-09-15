# West Scholars website

Plain static HTML/CSS — no build step, so Cloudflare Pages can deploy it as-is.

## Pages

- `index.html` — main marketing page (why West Scholars, Term 4 pricing, FAQ)
- `current-clients/index.html` — private page for existing families (Term 4 re-enrolment, referral program, review links, feedback survey)
- `assets/style.css` — shared styles (navy/gold from the logo)
- `assets/logo.png` — logo

## Deploying to Cloudflare Pages

1. Push this repo to GitHub (or connect it directly if it's already on GitHub).
2. In the Cloudflare dashboard: **Workers & Pages → Create → Pages → Connect to Git**.
3. Pick this repo. Build settings:
   - Framework preset: **None**
   - Build command: *(leave blank)*
   - Build output directory: `/`
4. Deploy. Cloudflare gives you a `*.pages.dev` URL immediately; add your custom domain (e.g. `westscholars.com.au`) under the project's **Custom domains** tab once it's registered.

## TODO before this goes live

Search for `REPLACE-WITH` and `href="#"` across both HTML files — everything marked is a placeholder:

- [ ] Email address (`mailto:REPLACE-WITH-EMAIL@westscholars.com.au`) — both pages, in the "Get in touch" section
- [ ] Phone number (`tel:REPLACE-WITH-PHONE`) — both pages
- [ ] Trustpilot review link — `current-clients/index.html`, Reviews section
- [ ] Google Business review link — same section
- [ ] Facebook Page link — same section
- [ ] Written-review form link (once built) — same section
- [ ] Feedback survey link (once built) — `current-clients/index.html`, Feedback section

Once you send me the real links, I'll drop them straight in and redeploy — no rebuild needed, just a find-and-replace.
