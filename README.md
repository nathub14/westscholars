# West Scholars website

Plain static HTML/CSS. No build step, so Cloudflare Pages can deploy it as is.

## Pages

- `index.html`: main marketing page (the program, results, guarantees, Term 4 pricing, FAQ)
- `current-clients/index.html`: private page for existing families (Term 4 re-enrolment, guarantees, referral program, review links, feedback survey)
- `assets/style.css`: shared styles (navy/gold pulled from the logo)
- `assets/logo.png`: logo

## Contact form

Both pages' contact forms post to `https://formsubmit.co/contact@westscholars.com.au`, a free form-to-email service that needs no backend. The first submission after this goes live will trigger a confirmation email to `contact@westscholars.com.au` that needs to be clicked once before form emails start arriving.

## Deploying to Cloudflare Pages

1. Push this repo to GitHub (or connect it directly if it's already on GitHub).
2. In the Cloudflare dashboard: **Workers & Pages -> Create -> Pages -> Connect to Git**.
3. Pick this repo. Build settings:
   - Framework preset: **None**
   - Build command: *(leave blank)*
   - Build output directory: `/`
4. Deploy. Cloudflare gives you a `*.pages.dev` URL immediately; add the custom domain (`westscholars.com.au`) under the project's **Custom domains** tab once it's registered.

## Still open

- [ ] Google Business review link (`current-clients/index.html`, Reviews section) - only one still marked with a red "Add link" tag
- [ ] Feedback survey link, once the survey is built (`current-clients/index.html`, Feedback section)
- [ ] The "steal one of these" review-prompt templates on the current clients page are a first draft. Nathan wants to redo these with his own template, said he'd send it over
- [ ] Sibling referral bonus set at $150 (standard referral is $100 each way) as a placeholder "a bit larger" amount. Confirm the number
- [ ] chart_student_trajectories.png (Term 1 results visual) not yet supplied. The Results section on the main page is text-only stats for now; send the PNG and it can be added

Everything else (phone, email, Facebook, Trustpilot) is live and real.
