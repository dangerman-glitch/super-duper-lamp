# Automated advertising system — planning

**Pitch:** `ad-system-plan.html` — the paid acquisition plan (Meta first, YouTube second).

## Thesis

Organic view count is a free creative pretest. 70 published videos, 65,665 lifetime
views, and 60% of those views come from 8 opinion/technique shorts. Ads should
amplify posts that already passed the organic test rather than fund new creative.

## Analysis

`../analysis/youtube_catalog_analysis.py` — categorises the YouTube catalog sheet
(ID `1n3GXwOyC8r8FT_DE4-iPJcFIFeY5wyMzPiJvakkUVE4`) by format and reports views per
format. Run with `python3 analysis/youtube_catalog_analysis.py`.

Result as of 2026-08-28:

| Format                    | Videos | Views  | Median | Mean  |
|---------------------------|-------:|-------:|-------:|------:|
| Opinion / technique short |      8 | 39,395 |  1,872 | 4,924 |
| Athlete competition clip  |     12 | 14,586 |    586 | 1,216 |
| Exercise demo / tutorial  |     46 | 11,588 |     54 |   252 |
| Other                     |      4 |     96 |     18 |    24 |

## Decisions (rev 2)

| Question | Answer |
|---|---|
| Goal | Fill 1:1 coaching slots. Learn to Lift is the second-order outcome. |
| Budget | $8/day (~$240/mo), read over 90 days. |
| Control | Human approves every launch; the system pauses on its own. |
| Access | Platform APIs, not a browser session. |

Consequences of aiming at 1:1 on a trickle budget:

- **Find Your Phase becomes a router, not a destination.** Improve/Compete phases
  route to the 15-min call; Learn phase routes to nurture and Learn to Lift.
- **Optimise on quiz completions, measure on booked calls.** Booked calls are far
  too sparse at this budget to train Meta's optimiser (~50 conversions/week/ad set
  is the working threshold).
- **One ad set, not three.** $8/day split three ways starves all of them.
- **Athlete competition clips move into retargeting** as the close layer; opinion
  shorts stay top-of-funnel.
- **The Governor gains a capacity switch** — ads pause when open slots hit zero.

## Scope: the remote line only

The business has two lines. **Remote** coaching runs through Stripe — 6 active
subscriptions. **In-person** coaching runs through a separate processor and covers
most of the ~65 names on the Master Athlete Roster.

Paid social can only fill the remote line at distance, so every figure below is
remote-only by design. The roster is not a reconciliation target for this system;
the capacity switch counts active Stripe subscriptions against a ceiling.

## Economics (rev 4, from Stripe live mode)

Read from the Stripe API directly — all subscriptions plus 90 days of charges.
Sigma reporting was not available on the key, so aggregates are computed from raw
objects (`../analysis/stripe_subscription_analysis.py`).

| Metric | Value |
|---|---|
| Active subscriptions | 6 |
| MRR | $745 |
| Price range / median | $75–$150 / $125 |
| Cancelled subscriptions | 12 |
| Median completed lifetime | 5.9 months |
| Trailing 12mo: new / cancelled | 5 / 4 |
| **Implied LTV** | **~$740** (median rate × median lifetime) |

Consequences:

- **The test has one question:** can $720 of spend (90 days at $8/day) produce one
  athlete? One signing ≈ break-even, two is working, zero means stop.
- **Retention beats acquisition on the arithmetic.** Moving median tenure from 5.9
  to 9 months adds ~$390 LTV per athlete for no ad spend. New subscriptions are
  roughly replacing cancellations, so the base is close to flat.
- **Some churn is involuntary.** 2 of 12 cancellations ended in `payment_failed`,
  and 3 of 22 charge attempts in the last 90 days failed (one customer, card
  returning `transaction_not_allowed`). Dunning recovers most of this.

Note the remote line has not grown in a year: 5 added, 4 lost. With only six
athletes in it, a 5.9-month median lifetime is a proportionally enormous leak.
The in-person line converts and holds at roughly 10x the volume — that gap is a
coaching-delivery question, not an advertising one, and it is the likeliest
lever on remote LTV.

## Open

1. **Remote capacity ceiling** — how many remote athletes can be taken on, and
   roughly what each costs in hours per month. The capacity switch counts active
   Stripe subscriptions against this.
2. **National vs local split** — the plan assumes national targeting for remote.
   Local Indianapolis ads for in-person are usually cheaper and higher-intent,
   but in-person has a hard ceiling. Depends on how close to full that line is.

## Status

Plan only. No ad code, no credentials, no spend.

## Not available during planning

- Instagram-native metrics (saves, shares, profile visits) — resolved by the API
  decision above; the Instagram Graph API returns these in Phase 01.
