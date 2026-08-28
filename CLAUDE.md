# Dangerman Training Systems — remote coaching ad system

Automated advertising for Dan German's **remote** weightlifting coaching line.
Meta first, YouTube second. Planned in a cloud session on 2026-08-28; this file
exists so a local session can pick up without re-deriving anything.

## Read these first

- `docs/ad-system-plan.html` — the growth plan (rev 6). Published as an artifact.
- `docs/meta-setup.html` — Meta account/pixel/API walkthrough, values pre-filled.
- `docs/README.md` — decisions log, economics, Phase 01 status.

## The thesis

Organic view count is a free creative pretest, already run 70 times. Ads should
amplify posts that passed it rather than fund new creative. Opinion/technique
shorts are 11% of the catalog and 60% of all views (mean 4,924); exercise demos
are 65% of the catalog with a median of 54 views. Demos are coaching
infrastructure, not reach — do not confuse the two.

## Two business lines — this system touches only one

| Line | Payments | Scale | In scope |
|---|---|---|---|
| **Remote** | Stripe (`acct_1NmnHkF8oFTIyLUG`) | 6 active, capacity 20 | **Yes** |
| In-person | Separate processor | ~65 on the roster | No |

Paid social can only fill the remote line at distance. The ~65-name Master
Athlete Roster is **not** a reconciliation target — the capacity switch counts
active Stripe subscriptions against a ceiling of 20.

## Settled parameters

| | |
|---|---|
| Goal | $20,000 Stripe income across a year (~9 concurrent athletes at $200) |
| Reach | National, **excluding the Indianapolis metro** |
| Price | $200/mo for new athletes; leave the existing six unchanged |
| Opening test | $100 over ~4 days at $25/day |
| Standing budget | $25–30/day, pending the $100 test result |
| Control | Dan approves every launch; the system pauses on its own |
| Access | Platform APIs, not a browser session |
| Margin | 90% remote. LTV ~$1,180, contribution ~$1,062 |

## Numbers that drive the plan

- YTD 2026 Stripe: **$6,935**. Calendar-2026 $20k is not reachable — say so
  plainly if it comes up again.
- Forward 12 months: **1.5 signings/month clears $20k** ($20,586 collected).
  0.5/month lands at $9,873 — a year of work to stand still.
- Median completed subscription lifetime **5.9 months** (11.1%/month churn).
  Moving it to 9 months adds ~$390/athlete for zero ad spend.
- The remote line has not grown in a year: 5 added, 4 lost.

**Retention outweighs acquisition on the arithmetic.** Do not let the ad build
crowd it out. 2 of 12 cancellations were `payment_failed` — dunning is the
cheapest revenue available.

## Funnel

Cold ad → **Find Your Phase quiz** (the sorter, not the destination) → Improve
and Compete phases go to a 15-min call and 1:1; Learn phase goes to nurture and
Learn to Lift. Never point a cold ad straight at a booking page.

Optimise on `quiz_completed` (frequent enough to train the optimiser), measure
on `call_booked`. Never set `call_booked` as the optimisation event — it is far
too sparse at this budget.

## What is built

`ads` schema in Supabase project `tinlmpddcjeasulelohe` ("Dangerman App"),
deliberately separate from the coaching app in `public`. Nine tables:
`creatives`, `creative_metrics`, `creative_scores`, `promotions`,
`ad_entities`, `ad_metrics`, `conversions`, `capacity_state`, `settings`.

RLS is enabled on all of them with **no permissive policies**, and anon and
authenticated are revoked from the schema — service role only.

Seeded: 69 videos + a 2026-08-28 metrics snapshot, capacity at 20/6 with ads
disabled, settings carrying budget and thresholds.

## Analysis scripts

Reproduce any number in the plan:

```
python3 analysis/youtube_catalog_analysis.py     # format vs reach
python3 analysis/stripe_subscription_analysis.py # MRR, churn, LTV
python3 analysis/goal_model.py                   # paths to $20k
python3 analysis/week_one_test.py                # what $100 can measure
python3 analysis/seed_creatives.py               # emits the backfill SQL
```

## Next task — needs Chrome

**Meta account setup.** Dan is logged into Facebook in Chrome and wants help
clicking through it. The cloud session had no browser; a local session with the
Claude in Chrome extension does. Follow `docs/meta-setup.html`.

Order matters — business verification takes days and blocks the API:

1. New business portfolio for **Dangerman Training Systems** (not Myriad's —
   he may go independent, and a pixel under the gym's portfolio goes with it)
2. Start business verification, then continue while it reviews
3. Connect the Dangerman OWL Instagram and Page
4. Ad account — USD, `America/Indiana/Indianapolis`, **both permanent**;
   $150 account spending limit during testing
5. Pixel on the quiz + booking page
6. `quiz_completed` and `call_booked` events; pass phase as a parameter;
   verify with Meta Pixel Helper before spending anything
7. Marketing API app + system user token

Then Phase 02: the collector and scorer, which produces the first ranked table
of every post. That runs on data, not spend, so it can proceed while
verification is pending.

## Open questions

- Hours per remote athlete per month, so the capacity switch protects the
  calendar rather than an arbitrary count.
- **Find Your Phase and Learn to Lift appear to sit under Myriad.** If Dan is
  going independent, building his acquisition funnel on the gym's assets means
  handing back the funnel exactly when he needs it. Worth resolving before
  spend goes behind it.

## Conventions

- Never paste the Meta system user token into chat — it carries spending
  authority. Environment variable, and reference it by name.
- Branch: `claude/social-media-ads-automation-njjd5w`.
- One sheet row ("Forefoot Elevated Split Squat", 810 views) is malformed — its
  URL column repeats the title, so it has no video ID and was skipped in the
  seed. The YouTube Data API backfill will recover it.
