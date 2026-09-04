# Handoff — Google Ads / YouTube launch

Context for picking this up in a new session. Everything below was established
in the session that created this branch; a fresh session won't know any of it.

## What's here

- `marketing/google-ads-youtube-plan.html` — the full 90-day plan. Standalone
  HTML, opens in any browser. This is the deliverable; the notes below are just
  the reasoning behind it.

## The business, in brief

Myriad Weightlifting — Dan German, USAW Level 3 International Coach, solo
remote coaching delivered through Google Sheets, billed via Stripe. Content
brand is Dangerman OWL (YouTube + Instagram).

Funnel: cold content → **Find Your Phase** quiz → 15-minute call → 1:1 remote
coaching. Products also include **Learn to Lift** (12-week beginner on-ramp)
and a run/Hyrox bundle.

## Live numbers pulled at time of writing (Sept 2026)

From the Stripe account `Dangerman Training Systems`, live mode:

| Metric | Value |
|---|---|
| Active subscriptions | 6 |
| Recurring revenue | $745/mo |
| Average athlete | $124/mo |
| Price range | $75–150/mo |
| Estimated LTV @ 12mo retention | ~$1,488 |

**Caveat:** these are Stripe *subscriptions* only. Athletes paying by invoice,
cash, or through Myriad's gym billing don't appear, so the real roster is
likely larger. Every budget figure in the plan is conservative in that
direction. Re-pull before relying on these; they are a point-in-time snapshot.

Note: the Stripe key available in that session lacked `reporting_write`, so
Sigma query templates (MRR trend, churn, cohorts) failed. Subscription and
price data read fine. If churn or retention analysis is needed, that
permission has to be added in the Stripe dashboard first.

## Decisions already made

- **Budget: $30/month to start**, ramping on results. This is the constraint
  that shaped everything else.
- **YouTube only at launch. No Search.** At ~$5 CPC in health & fitness, $30
  buys six clicks a month — Google's bidding needs ~30 conversions in 30 days
  to leave its learning phase, so Search cannot work at this budget. YouTube is
  priced per view (~$0.04), so the same $30 buys 300–1,000 views and fills a
  remarketing list. The Search campaign is fully specced in the plan but stays
  paused until the $400/month rung.
- **Destination: the Find Your Phase quiz**, not a sales page and not checkout.
  Matches the funnel docs — the page qualifies and warms, the call closes.
- **Audience: remote 1:1 athletes US-wide + true beginners.** Not local
  Indianapolis, not the runner/Hyrox product.
- **Creative comes from the existing catalog first.** Top organic performers
  (25,593 / 5,120 / 3,074 / 1,872 / 1,553 views) become ads with a 5-second end
  card. Three new scripts are written in the plan for when there's time to shoot.

## Blocking item — do this before spending a dollar

The quiz at `https://dangerman-findyourphase.netlify.app/` is a Netlify
single-page app. If the result screen renders without changing the URL — which
is the likely case — **there is no conversion to measure and the entire plan is
unmeasurable.** Section 02 of the plan has the gtag event implementation, the
`_redirects` rule, and the verification sequence.

That domain is blocked by the cloud session's network egress proxy, so it was
never inspected directly. A local session can fetch it and confirm.

Order of operations before launch:

1. Run the 30-second URL test on the quiz (documented in the plan)
2. Add the conversion event to the results component, redeploy
3. Confirm it fires with Google Tag Assistant
4. Point a custom subdomain at the Netlify app (a bare `.netlify.app` URL in an
   ad costs clicks)
5. Then build the Google Ads account per section 02 and launch

## Open questions

- Does the quiz capture an email, or only display a phase? Changes whether
  there's a nurture sequence to feed.
- Is there a booking link (Calendly or similar) for the 15-minute call? Needed
  for the secondary "Consult Booked" conversion action.
- Which domain does Dan control for the custom subdomain?

## Connector notes

This work used Stripe and Google Drive connectors. If they aren't configured
locally, the following are unavailable: live revenue data, the Stripe Report /
Command Center / Master Athlete Roster sheets, and the Learn to Lift funnel
docs. The `dangerman-*` skills (business advisor, marketing, program planner)
carry the relevant sheet and doc IDs.
